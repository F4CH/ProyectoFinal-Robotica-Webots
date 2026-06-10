"""
Seguimiento de waypoints usando control diferencial simple.
"""

import math

from config import (
    ACCION_GIRAR_A_WAYPOINT,
    ACCION_META_ALCANZADA,
    ACCION_SEGUIR_RUTA,
    DISTANCIA_RUEDAS,
    RADIO_RUEDA,
    VELOCIDAD_MAX,
    WAYPOINT_GANANCIA_ANGULAR,
    WAYPOINT_GIRO_EN_SITIO,
    WAYPOINT_TOLERANCIA,
    WAYPOINT_VEL_LINEAL,
    limitar,
)


def normalizar_angulo(angulo):
    return (angulo + math.pi) % (2.0 * math.pi) - math.pi


class WaypointFollower:
    """Genera velocidades de rueda para avanzar por una lista de waypoints."""

    def __init__(
        self,
        waypoints,
        tolerancia=WAYPOINT_TOLERANCIA,
        vel_lineal=WAYPOINT_VEL_LINEAL,
        ganancia_angular=WAYPOINT_GANANCIA_ANGULAR,
    ):
        self.waypoints = waypoints
        self.tolerancia = tolerancia
        self.vel_lineal = vel_lineal
        self.ganancia_angular = ganancia_angular
        self.indice = 0

    def terminado(self):
        return self.indice >= len(self.waypoints)

    def waypoint_actual(self):
        if self.terminado():
            return None
        return self.waypoints[self.indice]

    def actualizar(self, x, y, theta):
        if self.terminado():
            return 0.0, 0.0, ACCION_META_ALCANZADA

        objetivo_x, objetivo_y = self.waypoint_actual()
        dx = objetivo_x - x
        dy = objetivo_y - y
        distancia = math.sqrt(dx * dx + dy * dy)

        if distancia <= self.tolerancia:
            self.indice += 1
            if self.terminado():
                return 0.0, 0.0, ACCION_META_ALCANZADA
            objetivo_x, objetivo_y = self.waypoint_actual()
            dx = objetivo_x - x
            dy = objetivo_y - y
            distancia = math.sqrt(dx * dx + dy * dy)

        angulo_objetivo = math.atan2(dy, dx)
        error_angular = normalizar_angulo(angulo_objetivo - theta)

        velocidad_lineal = self.vel_lineal
        accion = ACCION_SEGUIR_RUTA

        if abs(error_angular) > WAYPOINT_GIRO_EN_SITIO:
            velocidad_lineal = 0.0
            accion = ACCION_GIRAR_A_WAYPOINT

        velocidad_angular = self.ganancia_angular * error_angular

        vel_izq = (velocidad_lineal - velocidad_angular * DISTANCIA_RUEDAS / 2.0) / RADIO_RUEDA
        vel_der = (velocidad_lineal + velocidad_angular * DISTANCIA_RUEDAS / 2.0) / RADIO_RUEDA

        vel_izq = limitar(vel_izq, -VELOCIDAD_MAX, VELOCIDAD_MAX)
        vel_der = limitar(vel_der, -VELOCIDAD_MAX, VELOCIDAD_MAX)

        return vel_izq, vel_der, accion
