"""
Odometria diferencial calculada a partir de los encoders del e-puck.
"""

import math

from config import DISTANCIA_RUEDAS, RADIO_RUEDA, TS


class OdometriaDiferencial:
    """Mantiene la pose odometrica y calcula velocidades desde encoders."""

    def __init__(self):
        self.encoder_izq_anterior = None
        self.encoder_der_anterior = None
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

    def actualizar(self, enc_izq, enc_der):
        if self.encoder_izq_anterior is None:
            self.encoder_izq_anterior = enc_izq
            self.encoder_der_anterior = enc_der
            return 0.0, 0.0, 0.0

        d_izq = RADIO_RUEDA * (enc_izq - self.encoder_izq_anterior)
        d_der = RADIO_RUEDA * (enc_der - self.encoder_der_anterior)

        self.encoder_izq_anterior = enc_izq
        self.encoder_der_anterior = enc_der

        ds = (d_izq + d_der) / 2.0
        dtheta = (d_der - d_izq) / DISTANCIA_RUEDAS

        self.theta = (self.theta + dtheta + math.pi) % (2.0 * math.pi) - math.pi
        self.x += ds * math.cos(self.theta)
        self.y += ds * math.sin(self.theta)

        velocidad_lineal = ds / TS
        velocidad_angular = dtheta / TS

        return ds, velocidad_lineal, velocidad_angular
