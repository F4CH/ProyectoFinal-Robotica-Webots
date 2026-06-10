"""
Configuracion compartida para el controlador final del e-puck.
"""

# Modo de decision:
#   "crudo" o "raw"
#   "filtrado" o "filtered"
#   "kalman"
LAB2_MODO = "kalman"

# Constantes fisicas y de muestreo
RADIO_RUEDA = 0.0205
DISTANCIA_RUEDAS = 0.052
VELOCIDAD_MAX = 6.28

TIME_STEP = 64
TS = TIME_STEP / 1000.0
FS = 1.0 / TS

# Navegacion reactiva
UMBRAL_FRONTAL = 105.0
UMBRAL_LATERAL = 150.0
ZONA_MUERTA_LATERAL = 45.0

PASOS_ESCAPE = 40
UMBRAL_LATERAL_EXTREMO = 350.0

# Velocidades y control de centrado
VEL_AVANCE = 3.0
VEL_GIRO = 2.5

GANANCIA_CENTRADO = 0.004
CORRECCION_MAX = 0.45

# Filtrado y fusion sensorial
VENTANA_MEDIA_MOVIL = 5
Q_KALMAN = 0.8
R_KALMAN = 22.0
ESCALA_SENSOR = 120.0

# Navegacion global auxiliar. Estas constantes quedan disponibles para probar
# grillas y rutas aparte, pero final_controller.py no las usa por defecto.
TAMANO_CELDA = 0.2
MARGEN_SEGURIDAD_GRILLA = 0.10
ORIGEN_WEBOTS = (0.0, 0.0)

WAYPOINT_TOLERANCIA = 0.08
WAYPOINT_VEL_LINEAL = 0.045
WAYPOINT_GANANCIA_ANGULAR = 3.2
WAYPOINT_GIRO_EN_SITIO = 0.35

ACCION_SEGUIR_RUTA = "SEGUIR_RUTA"
ACCION_GIRAR_A_WAYPOINT = "GIRAR_A_WAYPOINT"
ACCION_META_ALCANZADA = "META_ALCANZADA"

# Etiquetas de acciones
ACCION_AVANZAR = "AVANZAR"
ACCION_GIRAR_IZQUIERDA = "GIRAR_IZQUIERDA"
ACCION_GIRAR_DERECHA = "GIRAR_DERECHA"
ACCION_ESCAPE_IZQUIERDA = "ESCAPE_IZQUIERDA"
ACCION_ESCAPE_DERECHA = "ESCAPE_DERECHA"
ACCION_SALIDA_ESCAPE = "SALIDA_ESCAPE"
ACCION_CENTRAR_IZQUIERDA = "CENTRAR_IZQUIERDA"
ACCION_CENTRAR_DERECHA = "CENTRAR_DERECHA"

ACCIONES = [
    ACCION_AVANZAR,
    ACCION_GIRAR_IZQUIERDA,
    ACCION_GIRAR_DERECHA,
    ACCION_ESCAPE_IZQUIERDA,
    ACCION_ESCAPE_DERECHA,
    ACCION_SALIDA_ESCAPE,
    ACCION_CENTRAR_IZQUIERDA,
    ACCION_CENTRAR_DERECHA,
]

BOLD = "\033[1m"
RESET = "\033[0m"


def negrita(texto):
    """Devuelve texto con codigo ANSI de negrita para consolas compatibles."""
    return f"{BOLD}{texto}{RESET}"


def separador():
    print("=" * 60)


def limitar(valor, minimo, maximo):
    """Limita un valor al intervalo [minimo, maximo]."""
    return max(minimo, min(maximo, valor))
