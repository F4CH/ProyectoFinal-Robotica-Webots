"""
Registro de metricas y exportacion CSV del controlador.
"""

import csv
import os
from datetime import datetime

from config import separador, negrita


class MetricsLogger:
    """Acumula muestras y las guarda en un CSV al finalizar la simulacion."""

    def __init__(self):
        self.registros = []

    def agregar(self, registro):
        self.registros.append(registro)

    def guardar_csv(self, robot, modo):
        if not self.registros:
            return

        ruta_mundo = robot.getWorldPath()
        escenario = os.path.splitext(os.path.basename(ruta_mundo))[0]

        fecha_hora = datetime.now().strftime("%d%m%Y-%H%M%S")
        nombre_archivo = f"log_{fecha_hora}_Mundo={escenario}_Modo={modo}.csv"
        ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), nombre_archivo)

        with open(ruta, "w", newline="") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=list(self.registros[0].keys()))
            escritor.writeheader()
            escritor.writerows(self.registros)

        separador()
        print(negrita(" SIMULACION FINALIZADA"))
        print(f" CSV guardado          : {ruta}")
        print(f" Archivo               : {nombre_archivo}")
        print(f" Escenario             : {escenario}")
        print(f" Muestras registradas  : {len(self.registros)}")
        print(f" Modo utilizado        : {modo}")
        separador()
