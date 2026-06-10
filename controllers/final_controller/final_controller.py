"""
Controlador final Linea A para e-puck en Webots.

Arquitectura: sensores + filtrado + odometria + grilla de ocupacion + A* +
waypoints + control diferencial + navegacion reactiva.
"""

import math
import os

from controller import Supervisor

from astar import astar
from config import (
    ACCIONES,
    ACCION_GIRAR_A_WAYPOINT,
    ACCION_META_ALCANZADA,
    ACCION_RECUPERAR_GIRAR,
    ACCION_RECUPERAR_RETROCEDER,
    BLOQUEO_AVANCE_MIN,
    BLOQUEO_CICLOS,
    ESCALA_SENSOR,
    ESCENARIO_SIMPLE,
    FS,
    LAB2_MODO,
    MAPAS_ESCENARIOS,
    MOVIMIENTO_ASTAR,
    Q_KALMAN,
    R_KALMAN,
    RECUPERACION_GIRO_PASOS,
    RECUPERACION_RETROCESO_PASOS,
    RECUPERACION_VEL_GIRO,
    RECUPERACION_VEL_RETROCESO,
    TAMANO_CELDA,
    TIME_STEP,
    TS,
    UMBRAL_FRONTAL,
    UMBRAL_LATERAL,
    VENTANA_MEDIA_MOVIL,
    negrita,
    separador,
)
from differential_drive import (
    aplicar_velocidades,
    inicializar_encoders,
    inicializar_motores,
)
from filters import FiltroKalman1D, FiltroMediaMovil
from metrics_logger import MetricsLogger
from occupancy_grid import OccupancyGrid
from odometry import OdometriaDiferencial
from reactive_navigation import NavegacionReactiva
from sensors import (
    IDX_LATERAL_DER,
    IDX_LATERAL_IZQ,
    inicializar_sensores_proximidad,
    leer_sensores_proximidad,
    obtener_senal_frontal,
)
from waypoint_follower import WaypointFollower


class ControladorEpuckFinal:
    """
    Controlador autonomo para planificar y ejecutar una ruta en grilla.

    La decision de proximidad puede usar:
        crudo    -> senal frontal sin filtrar
        filtrado -> senal frontal con media movil
        kalman   -> estimacion fusionada con encoders y sensores frontales
    """

    MODOS_VALIDOS = {
        "raw": "crudo",
        "crudo": "crudo",
        "filtered": "filtrado",
        "filtrado": "filtrado",
        "kalman": "kalman",
    }

    def __init__(self):
        self.robot = Supervisor()

        self.motor_izq, self.motor_der = inicializar_motores(self.robot)
        self.encoder_izq, self.encoder_der = inicializar_encoders(self.robot)
        self.sensores_ps = inicializar_sensores_proximidad(self.robot)

        self.filtro_media = FiltroMediaMovil(VENTANA_MEDIA_MOVIL)
        self.filtro_kalman = FiltroKalman1D(Q_KALMAN, R_KALMAN)
        self.odometria = OdometriaDiferencial()
        self.navegacion = NavegacionReactiva()
        self.logger = MetricsLogger()

        self.muestra = 0
        self.modo = self._leer_modo_decision()

        self.escenario = None
        self.grid = None
        self.ruta_celdas = []
        self.waypoints = []
        self.seguidor = None

        self.bloqueo_contador = 0
        self.recuperacion_retroceso = 0
        self.recuperacion_giro = 0
        self.usando_pose_supervisor = False
        self.ultima_pose_supervisor = None

        self._cargar_navegacion_global()
        self._imprimir_encabezado()

    def _leer_modo_decision(self):
        modo_ingresado = LAB2_MODO.strip().lower()

        if modo_ingresado not in self.MODOS_VALIDOS:
            print(f"[ADVERTENCIA] Modo invalido: {LAB2_MODO}")
            print("[ADVERTENCIA] Se utilizara: kalman")
            return "kalman"

        return self.MODOS_VALIDOS[modo_ingresado]

    def _nombre_escenario_actual(self):
        ruta_mundo = self.robot.getWorldPath() or ""
        nombre = os.path.splitext(os.path.basename(ruta_mundo))[0]
        return nombre or ESCENARIO_SIMPLE

    def _ruta_mapa(self, nombre_csv):
        raiz_repo = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        return os.path.join(raiz_repo, "maps", nombre_csv)

    def _yaw_desde_rotacion(self, rotacion):
        eje_x, eje_y, eje_z, angulo = rotacion

        if abs(eje_z) >= max(abs(eje_x), abs(eje_y)):
            return eje_z * angulo

        return angulo

    def _yaw_desde_matriz_orientacion(self, orientacion):
        return math.atan2(orientacion[3], orientacion[0])

    def _leer_pose_supervisor(self):
        try:
            nodo = self.robot.getSelf()
            posicion = nodo.getPosition()
            orientacion = nodo.getOrientation()
            theta = self._yaw_desde_matriz_orientacion(orientacion)
            return posicion[0], posicion[1], theta
        except Exception:
            try:
                nodo = self.robot.getSelf()
                posicion = nodo.getPosition()
                campo_rotacion = nodo.getField("rotation")
                rotacion = campo_rotacion.getSFRotation()
                return posicion[0], posicion[1], self._yaw_desde_rotacion(rotacion)
            except Exception:
                return None

    def _sincronizar_pose_supervisor(self):
        pose = self._leer_pose_supervisor()

        if pose is None:
            return None

        avance_real = None
        if self.ultima_pose_supervisor is not None:
            dx = pose[0] - self.ultima_pose_supervisor[0]
            dy = pose[1] - self.ultima_pose_supervisor[1]
            avance_real = math.sqrt(dx * dx + dy * dy)

        self.ultima_pose_supervisor = pose
        self.usando_pose_supervisor = True
        self.odometria.establecer_pose(*pose)
        return avance_real

    def _cargar_navegacion_global(self):
        self.escenario = self._nombre_escenario_actual()
        config_mapa = MAPAS_ESCENARIOS.get(self.escenario)

        if config_mapa is None:
            print(
                f"[ADVERTENCIA] No hay mapa configurado para {self.escenario}. "
                f"Se usara {ESCENARIO_SIMPLE}."
            )
            self.escenario = ESCENARIO_SIMPLE
            config_mapa = MAPAS_ESCENARIOS[self.escenario]

        ruta_csv = self._ruta_mapa(config_mapa["csv"])

        try:
            self.grid = OccupancyGrid(
                ruta_csv,
                tamano_celda=TAMANO_CELDA,
                origen_webots=config_mapa["origen_webots"],
            )
            self.ruta_celdas = astar(
                self.grid,
                self.grid.inicio,
                self.grid.meta,
                tipo_movimiento=MOVIMIENTO_ASTAR,
            )

            if not self.ruta_celdas:
                print("[ADVERTENCIA] A* no encontro ruta. Se usara navegacion reactiva.")
                return

            self.waypoints = self.grid.path_to_waypoints(self.ruta_celdas)
            self.seguidor = WaypointFollower(self.waypoints)

            pose = self._leer_pose_supervisor()
            if pose is None:
                inicio_x, inicio_y = self.grid.celda_a_mundo(self.grid.inicio)
                pose = (inicio_x, inicio_y, config_mapa["theta_inicial"])
            else:
                self.usando_pose_supervisor = True
                self.ultima_pose_supervisor = pose

            self.odometria.establecer_pose(*pose)
        except Exception as exc:
            print(f"[ADVERTENCIA] No se pudo cargar navegacion global: {exc}")
            print("[ADVERTENCIA] Se usara navegacion reactiva como respaldo.")
            self.grid = None
            self.ruta_celdas = []
            self.waypoints = []
            self.seguidor = None

    def _imprimir_encabezado(self):
        separador()
        print(negrita(" CONTROLADOR FINAL LINEA A - E-PUCK"))
        separador()
        print(f" Escenario             : {self.escenario}")
        print(f" Modo de decision      : {self.modo}")
        print(f" Tiempo de muestreo Ts : {TS:.3f} s")
        print(f" Frecuencia fs         : {FS:.2f} Hz")
        print(f" Umbral frontal        : {UMBRAL_FRONTAL:.1f}")
        print(f" Umbral lateral        : {UMBRAL_LATERAL:.1f}")
        print(f" Media movil           : ventana = {VENTANA_MEDIA_MOVIL}")
        print(f" Kalman                : Q = {Q_KALMAN}, R = {R_KALMAN}")
        print(f" Acciones              : {', '.join(ACCIONES)}")

        if self.grid is not None and self.ruta_celdas:
            print(f" Mapa                  : {os.path.basename(self.grid.ruta_csv)}")
            print(
                " Pose para seguimiento : "
                f"{'Supervisor Webots' if self.usando_pose_supervisor else 'odometria encoders'}"
            )
            print(f" Resolucion grilla     : {self.grid.tamano_celda:.2f} m/celda")
            print(f" Inicio grilla         : {self.grid.inicio}")
            print(f" Meta grilla           : {self.grid.meta}")
            print(f" Celdas ruta A*        : {len(self.ruta_celdas)}")
            print(f" Waypoints             : {len(self.waypoints)}")
            print(f" Longitud estimada     : {self.grid.calcular_longitud_ruta(self.ruta_celdas):.2f} m")
        else:
            print(" Planificador          : desactivado")

        separador()
        print(negrita(" EJECUCION AUTONOMA"))
        separador()
        print()

    def _seleccionar_valor_decision(self, frontal_crudo, frontal_filtrado, frontal_kalman):
        if self.modo == "crudo":
            return frontal_crudo
        if self.modo == "filtrado":
            return frontal_filtrado
        return frontal_kalman

    def _distancia_waypoint_actual(self):
        if self.seguidor is None or self.seguidor.terminado():
            return None

        objetivo_x, objetivo_y = self.seguidor.waypoint_actual()
        dx = objetivo_x - self.odometria.x
        dy = objetivo_y - self.odometria.y
        return math.sqrt(dx * dx + dy * dy)

    def _ejecutar_recuperacion(self):
        if self.recuperacion_retroceso > 0:
            self.recuperacion_retroceso -= 1
            return (
                RECUPERACION_VEL_RETROCESO,
                RECUPERACION_VEL_RETROCESO,
                ACCION_RECUPERAR_RETROCEDER,
            )

        if self.recuperacion_giro > 0:
            self.recuperacion_giro -= 1
            return (
                -RECUPERACION_VEL_GIRO,
                RECUPERACION_VEL_GIRO,
                ACCION_RECUPERAR_GIRAR,
            )

        return None

    def _recuperacion_activa(self):
        return self.recuperacion_retroceso > 0 or self.recuperacion_giro > 0

    def _iniciar_recuperacion(self):
        self.recuperacion_retroceso = RECUPERACION_RETROCESO_PASOS
        self.recuperacion_giro = RECUPERACION_GIRO_PASOS
        self.bloqueo_contador = 0

    def _actualizar_bloqueo(self, ds, accion, vel_izq, vel_der):
        if accion in (
            ACCION_GIRAR_A_WAYPOINT,
            ACCION_META_ALCANZADA,
            ACCION_RECUPERAR_RETROCEDER,
            ACCION_RECUPERAR_GIRAR,
        ):
            self.bloqueo_contador = 0
            return

        intentando_avanzar = vel_izq > 0.5 and vel_der > 0.5

        if intentando_avanzar and abs(ds) < BLOQUEO_AVANCE_MIN:
            self.bloqueo_contador += 1
        else:
            self.bloqueo_contador = 0

        if self.bloqueo_contador >= BLOQUEO_CICLOS and not self._recuperacion_activa():
            self._iniciar_recuperacion()

    def _seleccionar_movimiento(self, valores_ps, valor_decision):
        if self.navegacion.requiere_intervencion(valores_ps, valor_decision):
            return self.navegacion.decidir_movimiento(valores_ps, valor_decision)

        recuperacion = self._ejecutar_recuperacion()
        if recuperacion is not None:
            return recuperacion

        if self.seguidor is not None:
            return self.seguidor.actualizar(
                self.odometria.x,
                self.odometria.y,
                self.odometria.theta,
            )

        return self.navegacion.decidir_movimiento(valores_ps, valor_decision)

    def _imprimir_estado(
        self,
        tiempo,
        frontal_crudo,
        frontal_filtrado,
        frontal_kalman,
        valores_ps,
        velocidad_lineal,
        velocidad_angular,
        distancia_waypoint,
        accion,
    ):
        print(f"* [{negrita('Tiempo')}: {tiempo:.2f}s] [{negrita('Muestra')}: {self.muestra}]")
        print(
            f"   > {negrita('Frontal')}: "
            f"raw={frontal_crudo:.2f}  filt={frontal_filtrado:.2f}  "
            f"kal={frontal_kalman:.2f}  K={self.filtro_kalman.k:.3f}"
        )
        print(
            f"   > {negrita('Lateral')}: "
            f"izq={valores_ps[IDX_LATERAL_IZQ]:.2f}  "
            f"der={valores_ps[IDX_LATERAL_DER]:.2f}"
        )
        print(
            f"   > {negrita('Odometria')}: "
            f"x={self.odometria.x:.3f}  "
            f"y={self.odometria.y:.3f}  "
            f"th={self.odometria.theta:.3f}"
        )
        print(
            f"   > {negrita('Velocidad')}: "
            f"v={velocidad_lineal:.3f}m/s  w={velocidad_angular:.3f}rad/s"
        )

        if self.seguidor is not None:
            print(
                f"   > {negrita('Ruta')}: "
                f"wp={self.seguidor.indice + 1}/{len(self.waypoints)}  "
                f"dist={distancia_waypoint if distancia_waypoint is not None else 0.0:.3f}m"
            )

        print(f"   > {negrita('Movimiento')}: {negrita(accion)}")
        print(" ")

    def ejecutar(self):
        """Bucle principal de Webots."""
        while self.robot.step(TIME_STEP) != -1:
            self.muestra += 1
            tiempo = self.muestra * TS

            valores_ps = leer_sensores_proximidad(self.sensores_ps)

            enc_izq = self.encoder_izq.getValue()
            enc_der = self.encoder_der.getValue()
            ds, velocidad_lineal, velocidad_angular = self.odometria.actualizar(
                enc_izq,
                enc_der,
            )
            avance_supervisor = self._sincronizar_pose_supervisor()
            avance_para_bloqueo = (
                avance_supervisor
                if avance_supervisor is not None
                else abs(ds)
            )

            frontal_crudo = obtener_senal_frontal(valores_ps)
            frontal_filtrado = self.filtro_media.actualizar(frontal_crudo)

            delta_encoder = ds * ESCALA_SENSOR
            frontal_kalman = self.filtro_kalman.actualizar(delta_encoder, frontal_crudo)

            valor_decision = self._seleccionar_valor_decision(
                frontal_crudo,
                frontal_filtrado,
                frontal_kalman,
            )

            distancia_waypoint = self._distancia_waypoint_actual()
            vel_izq, vel_der, accion = self._seleccionar_movimiento(
                valores_ps,
                valor_decision,
            )
            aplicar_velocidades(self.motor_izq, self.motor_der, vel_izq, vel_der)
            self._actualizar_bloqueo(
                avance_para_bloqueo,
                accion,
                vel_izq,
                vel_der,
            )

            if self.muestra % 20 == 0:
                self._imprimir_estado(
                    tiempo,
                    frontal_crudo,
                    frontal_filtrado,
                    frontal_kalman,
                    valores_ps,
                    velocidad_lineal,
                    velocidad_angular,
                    distancia_waypoint,
                    accion,
                )

            celda_actual = None
            if self.grid is not None:
                celda_actual = self.grid.mundo_a_celda(self.odometria.x, self.odometria.y)

            self.logger.agregar({
                "t_s": round(tiempo, 4),
                "muestra": self.muestra,
                "escenario": self.escenario,
                "modo_decision": self.modo,
                "pose_fuente": (
                    "supervisor"
                    if self.usando_pose_supervisor
                    else "encoders"
                ),
                "mapa_csv": os.path.basename(self.grid.ruta_csv) if self.grid else "",
                "ruta_celdas": len(self.ruta_celdas),
                "waypoints_total": len(self.waypoints),
                "waypoint_indice": self.seguidor.indice if self.seguidor else -1,
                "distancia_waypoint_m": (
                    round(distancia_waypoint, 5)
                    if distancia_waypoint is not None
                    else ""
                ),
                "grid_fila": celda_actual[0] if celda_actual else "",
                "grid_columna": celda_actual[1] if celda_actual else "",
                "ps0_frontal_der": round(valores_ps[0], 3),
                "ps7_frontal_izq": round(valores_ps[7], 3),
                "ps2_lateral_der": round(valores_ps[2], 3),
                "ps5_lateral_izq": round(valores_ps[5], 3),
                "frontal_crudo": round(frontal_crudo, 3),
                "frontal_filtrado": round(frontal_filtrado, 3),
                "frontal_kalman": round(frontal_kalman, 3),
                "kalman_ganancia": round(self.filtro_kalman.k, 5),
                "kalman_p": round(self.filtro_kalman.p, 5),
                "encoder_izq_rad": round(enc_izq, 5),
                "encoder_der_rad": round(enc_der, 5),
                "avance_ds_m": round(ds, 6),
                "velocidad_lineal_m_s": round(velocidad_lineal, 5),
                "velocidad_angular_rad_s": round(velocidad_angular, 5),
                "odom_x_m": round(self.odometria.x, 5),
                "odom_y_m": round(self.odometria.y, 5),
                "odom_theta_rad": round(self.odometria.theta, 5),
                "valor_decision": round(valor_decision, 3),
                "vel_motor_izq_rad_s": round(vel_izq, 3),
                "vel_motor_der_rad_s": round(vel_der, 3),
                "accion": accion,
            })

        self.logger.guardar_csv(self.robot, self.modo)


if __name__ == "__main__":
    ControladorEpuckFinal().ejecutar()
