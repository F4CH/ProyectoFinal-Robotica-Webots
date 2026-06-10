"""
Laboratorio 2 - Robotica y Sistemas Autonomos 2026-01
ICI 4150 - Navegacion reactiva con filtrado y fusion de sensores en Webots

Controlador principal para robot e-puck.
"""

from controller import Supervisor

from config import (
    ACCIONES,
    ESCALA_SENSOR,
    FS,
    LAB2_MODO,
    Q_KALMAN,
    R_KALMAN,
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
from odometry import OdometriaDiferencial
from reactive_navigation import NavegacionReactiva
from sensors import (
    IDX_LATERAL_DER,
    IDX_LATERAL_IZQ,
    inicializar_sensores_proximidad,
    leer_sensores_proximidad,
    obtener_senal_frontal,
)


class ControladorEpuckLab2:
    """
    Controlador de navegacion reactiva para e-puck.

    La decision principal puede hacerse con:
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

        self._imprimir_encabezado()

    def _leer_modo_decision(self):
        modo_ingresado = LAB2_MODO.strip().lower()

        if modo_ingresado not in self.MODOS_VALIDOS:
            print(f"[ADVERTENCIA] Modo invalido: {LAB2_MODO}")
            print("[ADVERTENCIA] Se utilizara: kalman")
            return "kalman"

        return self.MODOS_VALIDOS[modo_ingresado]

    def _imprimir_encabezado(self):
        separador()
        print(negrita(" CONTROLADOR LABORATORIO 2 - E-PUCK"))
        separador()
        print(f" Modo de decision      : {self.modo}")
        print(f" Tiempo de muestreo Ts : {TS:.3f} s")
        print(f" Frecuencia fs         : {FS:.2f} Hz")
        print(f" Umbral frontal        : {UMBRAL_FRONTAL:.1f}")
        print(f" Umbral lateral        : {UMBRAL_LATERAL:.1f}")
        print(f" Media movil           : ventana = {VENTANA_MEDIA_MOVIL}")
        print(f" Kalman                : Q = {Q_KALMAN}, R = {R_KALMAN}")
        print(f" Acciones              : {', '.join(ACCIONES)}")
        separador()
        print(negrita(" EJECUCION - E-PUCK"))
        separador()
        print()

    def _seleccionar_valor_decision(self, frontal_crudo, frontal_filtrado, frontal_kalman):
        if self.modo == "crudo":
            return frontal_crudo
        if self.modo == "filtrado":
            return frontal_filtrado
        return frontal_kalman

    def _imprimir_estado(
        self,
        tiempo,
        frontal_crudo,
        frontal_filtrado,
        frontal_kalman,
        valores_ps,
        velocidad_lineal,
        velocidad_angular,
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

            frontal_crudo = obtener_senal_frontal(valores_ps)
            frontal_filtrado = self.filtro_media.actualizar(frontal_crudo)

            delta_encoder = ds * ESCALA_SENSOR
            frontal_kalman = self.filtro_kalman.actualizar(delta_encoder, frontal_crudo)

            valor_decision = self._seleccionar_valor_decision(
                frontal_crudo,
                frontal_filtrado,
                frontal_kalman,
            )

            vel_izq, vel_der, accion = self.navegacion.decidir_movimiento(
                valores_ps,
                valor_decision,
            )
            aplicar_velocidades(self.motor_izq, self.motor_der, vel_izq, vel_der)

            if self.muestra % 20 == 0:
                self._imprimir_estado(
                    tiempo,
                    frontal_crudo,
                    frontal_filtrado,
                    frontal_kalman,
                    valores_ps,
                    velocidad_lineal,
                    velocidad_angular,
                    accion,
                )

            self.logger.agregar({
                "t_s": round(tiempo, 4),
                "muestra": self.muestra,
                "modo_decision": self.modo,
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
    ControladorEpuckLab2().ejecutar()
