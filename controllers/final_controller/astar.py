"""
Planificacion de rutas con A* sobre una grilla de ocupacion.
"""

import heapq
import math


MOVIMIENTOS_4 = [
    (-1, 0, 1.0),
    (1, 0, 1.0),
    (0, -1, 1.0),
    (0, 1, 1.0),
]

MOVIMIENTOS_8 = MOVIMIENTOS_4 + [
    (-1, -1, math.sqrt(2.0)),
    (-1, 1, math.sqrt(2.0)),
    (1, -1, math.sqrt(2.0)),
    (1, 1, math.sqrt(2.0)),
]


def heuristica(celda, meta, tipo_movimiento="4"):
    """
    Estima el costo restante.

    Para movimiento 4-direcciones se usa Manhattan porque cada paso cambia una
    sola coordenada. Para 8-direcciones se usa Euclidiana porque se permiten
    diagonales.
    """
    fila, columna = celda
    fila_meta, columna_meta = meta
    df = abs(fila - fila_meta)
    dc = abs(columna - columna_meta)

    if str(tipo_movimiento) == "8":
        return math.sqrt(df * df + dc * dc)

    return df + dc


def obtener_movimientos(tipo_movimiento):
    if str(tipo_movimiento) == "8":
        return MOVIMIENTOS_8
    return MOVIMIENTOS_4


def dentro_de_limites(grilla, celda):
    fila, columna = celda

    if hasattr(grilla, "dentro_de_limites"):
        return grilla.dentro_de_limites(celda)

    return 0 <= fila < len(grilla) and 0 <= columna < len(grilla[0])


def es_libre(grilla, celda):
    if hasattr(grilla, "es_libre"):
        return grilla.es_libre(celda)

    if not dentro_de_limites(grilla, celda):
        return False

    fila, columna = celda
    return grilla[fila][columna] != 1


def vecinos_validos(grilla, celda, tipo_movimiento="4"):
    fila, columna = celda

    for df, dc, costo in obtener_movimientos(tipo_movimiento):
        vecino = (fila + df, columna + dc)

        if es_libre(grilla, vecino):
            yield vecino, costo


def reconstruir_ruta(came_from, inicio, meta):
    """Reconstruye la ruta desde inicio hasta meta en orden."""
    if meta not in came_from and meta != inicio:
        return []

    actual = meta
    ruta = [actual]

    while actual != inicio:
        actual = came_from[actual]
        ruta.append(actual)

    ruta.reverse()
    return ruta


def validar_ruta(grilla, ruta):
    """Verifica que la ruta no tenga celdas ocupadas ni fuera de limite."""
    return bool(ruta) and all(es_libre(grilla, celda) for celda in ruta)


def astar(grilla, inicio, meta, tipo_movimiento="4"):
    """
    Ejecuta A* y devuelve una lista de celdas desde inicio hasta meta.

    Si no existe ruta valida, devuelve una lista vacia.
    """
    if not dentro_de_limites(grilla, inicio) or not dentro_de_limites(grilla, meta):
        return []

    if not es_libre(grilla, inicio) or not es_libre(grilla, meta):
        return []

    frontera = []
    contador = 0
    heapq.heappush(frontera, (0.0, contador, inicio))

    came_from = {}
    costo_g = {inicio: 0.0}
    visitados = set()

    while frontera:
        _, _, actual = heapq.heappop(frontera)

        if actual in visitados:
            continue

        if actual == meta:
            ruta = reconstruir_ruta(came_from, inicio, meta)
            return ruta if validar_ruta(grilla, ruta) else []

        visitados.add(actual)

        for vecino, costo_movimiento in vecinos_validos(
            grilla,
            actual,
            tipo_movimiento,
        ):
            nuevo_costo = costo_g[actual] + costo_movimiento

            if vecino not in costo_g or nuevo_costo < costo_g[vecino]:
                costo_g[vecino] = nuevo_costo
                prioridad = nuevo_costo + heuristica(
                    vecino,
                    meta,
                    tipo_movimiento,
                )
                contador += 1
                heapq.heappush(frontera, (prioridad, contador, vecino))
                came_from[vecino] = actual

    return []
