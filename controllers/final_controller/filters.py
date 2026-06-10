"""
Filtros usados para suavizar y fusionar la senal frontal.
"""


class FiltroMediaMovil:
    """Filtro simple que promedia las ultimas N muestras."""

    def __init__(self, ventana):
        self.ventana = ventana
        self.buffer = []

    def actualizar(self, valor):
        self.buffer.append(valor)
        if len(self.buffer) > self.ventana:
            self.buffer.pop(0)
        return sum(self.buffer) / len(self.buffer)


class FiltroKalman1D:
    """
    Filtro de Kalman escalar para estimar la proximidad frontal.

    Usa una prediccion basada en encoders y una correccion basada en los
    sensores frontales.
    """

    def __init__(self, q, r):
        self.q = q
        self.r = r
        self.d_hat = None
        self.p = 1.0
        self.k = 0.0
        self.d_pred = 0.0
        self.p_pred = 0.0

    def inicializado(self):
        return self.d_hat is not None

    def inicializar(self, primera_medicion):
        self.d_hat = primera_medicion
        self.p = 1.0
        self.k = 0.0
        self.d_pred = primera_medicion
        self.p_pred = self.p

    def predecir(self, delta_encoder):
        self.d_pred = self.d_hat + delta_encoder
        self.p_pred = self.p + self.q

    def corregir(self, medicion):
        self.k = self.p_pred / (self.p_pred + self.r)
        self.d_hat = self.d_pred + self.k * (medicion - self.d_pred)
        self.p = (1.0 - self.k) * self.p_pred
        return self.d_hat

    def actualizar(self, delta_encoder, medicion):
        if not self.inicializado():
            self.inicializar(medicion)
            return self.d_hat

        self.predecir(delta_encoder)
        return self.corregir(medicion)
