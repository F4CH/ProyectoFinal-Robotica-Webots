"""
Indices y utilidades de lectura para sensores del e-puck.
"""

from config import TIME_STEP

IDX_FRONTAL_DER = 0
IDX_FRONTAL_IZQ = 7
IDX_LATERAL_DER = 2
IDX_LATERAL_IZQ = 5


def inicializar_sensores_proximidad(robot):
    sensores_ps = []
    for i in range(8):
        sensor = robot.getDevice(f"ps{i}")
        sensor.enable(TIME_STEP)
        sensores_ps.append(sensor)
    return sensores_ps


def leer_sensores_proximidad(sensores_ps):
    return [sensor.getValue() for sensor in sensores_ps]


def obtener_senal_frontal(valores_ps):
    frontal_izq = valores_ps[IDX_FRONTAL_IZQ]
    frontal_der = valores_ps[IDX_FRONTAL_DER]
    return (frontal_izq + frontal_der) / 2.0
