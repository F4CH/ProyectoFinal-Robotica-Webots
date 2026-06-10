"""
Inicializacion y control de motores diferenciales del e-puck.
"""

from config import TIME_STEP


def inicializar_motores(robot):
    motor_izq = robot.getDevice("left wheel motor")
    motor_der = robot.getDevice("right wheel motor")

    motor_izq.setPosition(float("inf"))
    motor_der.setPosition(float("inf"))
    motor_izq.setVelocity(0.0)
    motor_der.setVelocity(0.0)

    return motor_izq, motor_der


def inicializar_encoders(robot):
    encoder_izq = robot.getDevice("left wheel sensor")
    encoder_der = robot.getDevice("right wheel sensor")

    encoder_izq.enable(TIME_STEP)
    encoder_der.enable(TIME_STEP)

    return encoder_izq, encoder_der


def aplicar_velocidades(motor_izq, motor_der, vel_izq, vel_der):
    motor_izq.setVelocity(vel_izq)
    motor_der.setVelocity(vel_der)
