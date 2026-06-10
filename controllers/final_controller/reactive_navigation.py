"""
Navegacion reactiva basada en sensores frontales y laterales.
"""

from config import (
    ACCION_AVANZAR,
    ACCION_CENTRAR_DERECHA,
    ACCION_CENTRAR_IZQUIERDA,
    ACCION_ESCAPE_DERECHA,
    ACCION_ESCAPE_IZQUIERDA,
    ACCION_GIRAR_DERECHA,
    ACCION_GIRAR_IZQUIERDA,
    ACCION_SALIDA_ESCAPE,
    CORRECCION_MAX,
    GANANCIA_CENTRADO,
    PASOS_ESCAPE,
    UMBRAL_FRONTAL,
    UMBRAL_LATERAL,
    UMBRAL_LATERAL_EXTREMO,
    VEL_AVANCE,
    VEL_GIRO,
    VELOCIDAD_MAX,
    ZONA_MUERTA_LATERAL,
    limitar,
)
from sensors import (
    IDX_FRONTAL_DER,
    IDX_FRONTAL_IZQ,
    IDX_LATERAL_DER,
    IDX_LATERAL_IZQ,
)


class NavegacionReactiva:
    """Decide velocidades de ruedas usando reglas reactivas."""

    def __init__(self):
        self.escape_pasos = 0
        self.escape_direccion = None
        self.salida_pasos = 0

    def _lecturas_principales(self, valores_ps):
        frontal_izq = valores_ps[IDX_FRONTAL_IZQ]
        frontal_der = valores_ps[IDX_FRONTAL_DER]
        lateral_izq = valores_ps[IDX_LATERAL_IZQ]
        lateral_der = valores_ps[IDX_LATERAL_DER]
        return frontal_izq, frontal_der, lateral_izq, lateral_der

    def requiere_intervencion(self, valores_ps, valor_decision):
        """Indica si la capa reactiva debe tomar prioridad sobre la ruta."""
        if self.escape_pasos > 0 or self.salida_pasos > 0:
            return True

        frontal_izq, frontal_der, lateral_izq, lateral_der = self._lecturas_principales(
            valores_ps,
        )

        return (
            valor_decision > UMBRAL_FRONTAL
            or frontal_izq > UMBRAL_FRONTAL
            or frontal_der > UMBRAL_FRONTAL
            or lateral_izq > UMBRAL_LATERAL_EXTREMO
            or lateral_der > UMBRAL_LATERAL_EXTREMO
        )

    def decidir_movimiento(self, valores_ps, valor_decision):
        frontal_izq, frontal_der, lateral_izq, lateral_der = self._lecturas_principales(
            valores_ps,
        )

        if self.escape_pasos > 0:
            self.escape_pasos -= 1

            if self.escape_pasos == 0:
                self.salida_pasos = 10

            if self.escape_direccion == "derecha":
                return -0.5, -2.0, ACCION_ESCAPE_DERECHA
            return -2.0, -0.5, ACCION_ESCAPE_IZQUIERDA

        if self.salida_pasos > 0:
            self.salida_pasos -= 1
            return VEL_AVANCE, VEL_AVANCE, ACCION_SALIDA_ESCAPE

        lateral_extremo = (
            lateral_izq > UMBRAL_LATERAL_EXTREMO
            or lateral_der > UMBRAL_LATERAL_EXTREMO
        )
        frontal_peligroso = (
            valor_decision > UMBRAL_FRONTAL
            or frontal_izq > UMBRAL_FRONTAL
            or frontal_der > UMBRAL_FRONTAL
        )

        if lateral_extremo or frontal_peligroso:
            self.escape_pasos = PASOS_ESCAPE

            if lateral_izq > lateral_der:
                self.escape_direccion = "derecha"
                return -0.5, -2.0, ACCION_ESCAPE_DERECHA

            self.escape_direccion = "izquierda"
            return -2.0, -0.5, ACCION_ESCAPE_IZQUIERDA

        obstaculo_frontal = valor_decision > UMBRAL_FRONTAL
        lateral_izq_cerca = lateral_izq > UMBRAL_LATERAL
        lateral_der_cerca = lateral_der > UMBRAL_LATERAL

        if obstaculo_frontal:
            diferencia_lateral = lateral_izq - lateral_der

            if abs(diferencia_lateral) > ZONA_MUERTA_LATERAL:
                girar_derecha = lateral_izq > lateral_der
            else:
                girar_derecha = frontal_izq > frontal_der

            if girar_derecha:
                return VEL_GIRO, -VEL_GIRO, ACCION_GIRAR_DERECHA
            return -VEL_GIRO, VEL_GIRO, ACCION_GIRAR_IZQUIERDA

        if lateral_izq_cerca or lateral_der_cerca:
            error = lateral_izq - lateral_der
            correccion = limitar(
                GANANCIA_CENTRADO * error,
                -CORRECCION_MAX,
                CORRECCION_MAX,
            )

            vel_izq = limitar(VEL_AVANCE + correccion, -VELOCIDAD_MAX, VELOCIDAD_MAX)
            vel_der = limitar(VEL_AVANCE - correccion, -VELOCIDAD_MAX, VELOCIDAD_MAX)

            accion = ACCION_CENTRAR_DERECHA if error > 0 else ACCION_CENTRAR_IZQUIERDA
            return vel_izq, vel_der, accion

        return VEL_AVANCE, VEL_AVANCE, ACCION_AVANZAR
