"""
Grilla de ocupacion y conversion entre celdas y coordenadas Webots.
"""

import csv
import math

from config import ORIGEN_WEBOTS, TAMANO_CELDA


def _limitar_indice(valor, minimo, maximo):
    return max(minimo, min(maximo, valor))


def grid_to_webots(
    row,
    col=None,
    tamano_celda=TAMANO_CELDA,
    origen_webots=ORIGEN_WEBOTS,
    celda_origen=(0, 0),
):
    """
    Convierte una celda de grilla a coordenadas reales de Webots.

    `origen_webots` representa el centro de `celda_origen`. La fila crece hacia
    abajo en la matriz; el eje Y de Webots crece hacia adelante.
    """
    if col is None:
        fila, columna = row
    else:
        fila, columna = row, col

    fila_origen, columna_origen = celda_origen
    origen_x, origen_y = origen_webots

    x = origen_x + (columna - columna_origen) * tamano_celda
    y = origen_y - (fila - fila_origen) * tamano_celda
    return x, y


def webots_to_grid(
    x,
    y,
    tamano_celda=TAMANO_CELDA,
    origen_webots=ORIGEN_WEBOTS,
    celda_origen=(0, 0),
    limites=None,
    limitar=True,
):
    """
    Convierte coordenadas Webots a indices `(fila, columna)`.

    Si `limites=(filas, columnas)` y `limitar=True`, la salida se satura al
    borde valido. Esto evita errores cuando la odometria queda levemente fuera
    de la grilla.
    """
    fila_origen, columna_origen = celda_origen
    origen_x, origen_y = origen_webots

    columna = columna_origen + round((x - origen_x) / tamano_celda)
    fila = fila_origen - round((y - origen_y) / tamano_celda)

    if limites is None:
        return fila, columna

    filas, columnas = limites
    dentro = 0 <= fila < filas and 0 <= columna < columnas

    if dentro:
        return fila, columna

    if not limitar:
        return None

    fila = _limitar_indice(fila, 0, filas - 1)
    columna = _limitar_indice(columna, 0, columnas - 1)
    return fila, columna


def coordenadas_grilla_a_webots(*args, **kwargs):
    """Alias en espanol mantenido por compatibilidad."""
    return grid_to_webots(*args, **kwargs)


def coordenadas_webots_a_grilla(*args, **kwargs):
    """Alias en espanol mantenido por compatibilidad."""
    return webots_to_grid(*args, **kwargs)


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
        self.celda_origen = celda_origen if celda_origen is not None else (0, 0)
        self.grid = self._cargar_csv(ruta_csv)

        self.filas = len(self.grid)
        self.columnas = len(self.grid[0]) if self.filas > 0 else 0

        self.inicio = self._buscar_valor(self.INICIO)
        self.meta = self._buscar_valor(self.META)

        if self.inicio is None:
            raise ValueError("La grilla no tiene celda de inicio marcada con 2.")

        if self.meta is None:
            raise ValueError("La grilla no tiene celda de meta marcada con 3.")

    def _cargar_csv(self, ruta_csv):
        matriz = []

        with open(ruta_csv, "r", newline="") as archivo:
            lector = csv.reader(archivo)

            for fila in lector:
                if not fila:
                    continue

                matriz.append([int(valor.strip()) for valor in fila])

        if not matriz:
            raise ValueError("La grilla CSV esta vacia.")

        columnas = len(matriz[0])
        if any(len(fila) != columnas for fila in matriz):
            raise ValueError("La grilla CSV debe ser rectangular.")

        return matriz

    def _buscar_valor(self, valor_buscado):
        for fila in range(self.filas):
            for columna in range(self.columnas):
                if self.grid[fila][columna] == valor_buscado:
                    return fila, columna
        return None

    def dentro_de_limites(self, celda):
        fila, columna = celda
        return 0 <= fila < self.filas and 0 <= columna < self.columnas

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
        return grid_to_webots(
            celda,
            tamano_celda=self.tamano_celda,
            origen_webots=self.origen_webots,
            celda_origen=self.celda_origen,
        )

    def mundo_a_celda(self, x, y, limitar_a_grilla=True):
        return webots_to_grid(
            x,
            y,
            tamano_celda=self.tamano_celda,
            origen_webots=self.origen_webots,
            celda_origen=self.celda_origen,
            limites=(self.filas, self.columnas),
            limitar=limitar_a_grilla,
        )

    def simplificar_ruta(self, ruta):
        """Elimina celdas intermedias cuando la direccion no cambia."""
        if len(ruta) <= 2:
            return list(ruta)

        simplificada = [ruta[0]]
        direccion_anterior = None

        for indice in range(1, len(ruta)):
            fila_prev, col_prev = ruta[indice - 1]
            fila_actual, col_actual = ruta[indice]
            direccion = (fila_actual - fila_prev, col_actual - col_prev)

            if direccion_anterior is not None and direccion != direccion_anterior:
                simplificada.append(ruta[indice - 1])

            direccion_anterior = direccion

        simplificada.append(ruta[-1])
        return simplificada

    def path_to_waypoints(self, ruta, simplificar=True):
        """Convierte una ruta de celdas en waypoints reales para Webots."""
        ruta_convertida = self.simplificar_ruta(ruta) if simplificar else ruta
        return [self.celda_a_mundo(celda) for celda in ruta_convertida]

    def ruta_a_waypoints(self, ruta, simplificar=True):
        """Alias en espanol mantenido por compatibilidad."""
        return self.path_to_waypoints(ruta, simplificar=simplificar)

    def calcular_longitud_ruta(self, ruta):
        if not ruta or len(ruta) < 2:
            return 0.0

        longitud = 0.0

        for indice in range(1, len(ruta)):
            x1, y1 = self.celda_a_mundo(ruta[indice - 1])
            x2, y2 = self.celda_a_mundo(ruta[indice])
            longitud += math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        return longitud
