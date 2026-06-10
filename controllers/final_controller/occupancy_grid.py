import csv
import math

from config import ORIGEN_WEBOTS, TAMANO_CELDA


def coordenadas_grilla_a_webots(
    celda,
    tamano_celda=TAMANO_CELDA,
    origen_webots=ORIGEN_WEBOTS,
    celda_origen=(0, 0),
):
    """
    Convierte una celda de la grilla a coordenadas reales de Webots.

    La fila aumenta hacia abajo en la matriz, mientras que en Webots el eje Y
    positivo apunta hacia adelante. Por eso el desplazamiento en filas invierte
    el signo de Y.
    """
    fila, columna = celda
    fila_origen, columna_origen = celda_origen
    origen_x, origen_y = origen_webots

    x = origen_x + (columna - columna_origen) * tamano_celda
    y = origen_y - (fila - fila_origen) * tamano_celda

    return x, y


def coordenadas_webots_a_grilla(
    x,
    y,
    tamano_celda=TAMANO_CELDA,
    origen_webots=ORIGEN_WEBOTS,
    celda_origen=(0, 0),
):
    """
    Convierte coordenadas reales de Webots al indice de celda de la grilla.

    Retorna una tupla (fila, columna), lista para usar en A*, BFS u otro
    planificador discreto.
    """
    fila_origen, columna_origen = celda_origen
    origen_x, origen_y = origen_webots

    columna = columna_origen + round((x - origen_x) / tamano_celda)
    fila = fila_origen - round((y - origen_y) / tamano_celda)

    return fila, columna


class OccupancyGrid:
    LIBRE = 0
    OBSTACULO = 1
    INICIO = 2
    META = 3

    def __init__(
        self,
        ruta_csv,
        tamano_celda=TAMANO_CELDA,
        origen_webots=ORIGEN_WEBOTS,
        celda_origen=None,
    ):
        self.ruta_csv = ruta_csv
        self.tamano_celda = tamano_celda
        self.origen_webots = origen_webots
        self.grid = self._cargar_csv(ruta_csv)

        self.filas = len(self.grid)
        self.columnas = len(self.grid[0]) if self.filas > 0 else 0

        self.inicio = self._buscar_valor(self.INICIO)
        self.meta = self._buscar_valor(self.META)

        if self.inicio is None:
            raise ValueError("La grilla no tiene celda de inicio marcada con 2.")

        if self.meta is None:
            raise ValueError("La grilla no tiene celda de meta marcada con 3.")

        self.celda_origen = celda_origen if celda_origen is not None else self.inicio

    def _cargar_csv(self, ruta_csv):
        matriz = []

        with open(ruta_csv, "r", newline="") as archivo:
            lector = csv.reader(archivo)

            for fila in lector:
                if not fila:
                    continue

                matriz.append([int(valor.strip()) for valor in fila])

        if not matriz:
            raise ValueError("La grilla CSV está vacía.")

        return matriz

    def _buscar_valor(self, valor_buscado):
        for fila in range(self.filas):
            for columna in range(self.columnas):
                if self.grid[fila][columna] == valor_buscado:
                    return fila, columna

        return None

    def dentro_de_limites(self, celda):
        fila, columna = celda

        return (
            0 <= fila < self.filas
            and 0 <= columna < self.columnas
        )

    def es_libre(self, celda):
        if not self.dentro_de_limites(celda):
            return False

        fila, columna = celda
        return self.grid[fila][columna] != self.OBSTACULO

    def vecinos(self, celda):
        fila, columna = celda

        candidatos = [
            (fila - 1, columna),
            (fila + 1, columna),
            (fila, columna - 1),
            (fila, columna + 1),
        ]

        return [celda for celda in candidatos if self.es_libre(celda)]

    def celda_a_mundo(self, celda):
        return coordenadas_grilla_a_webots(
            celda,
            tamano_celda=self.tamano_celda,
            origen_webots=self.origen_webots,
            celda_origen=self.celda_origen,
        )

    def mundo_a_celda(self, x, y):
        return coordenadas_webots_a_grilla(
            x,
            y,
            tamano_celda=self.tamano_celda,
            origen_webots=self.origen_webots,
            celda_origen=self.celda_origen,
        )

    def ruta_a_waypoints(self, ruta):
        """Convierte una ruta de celdas en waypoints reales para Webots."""
        return [self.celda_a_mundo(celda) for celda in ruta]

    def calcular_longitud_ruta(self, ruta):
        if not ruta or len(ruta) < 2:
            return 0.0

        longitud = 0.0

        for i in range(1, len(ruta)):
            x1, y1 = self.celda_a_mundo(ruta[i - 1])
            x2, y2 = self.celda_a_mundo(ruta[i])

            longitud += math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        return longitud
