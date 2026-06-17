# Resumen de métricas de evaluación

> Generado automáticamente el 2026-06-17 10:35
> Modo de decisión: kalman

## Tarea 27 — Tiempo total de ejecución

Tiempo transcurrido desde el inicio de la simulación hasta que el robot
alcanza la meta (primera aparición de `META_ALCANZADA` en el registro).

- **Escenario simple**: 113.92 s
- **Escenario complejo**: 466.56 s

## Tarea 28 — Longitud de la ruta planificada (A*)

Calculada como `(celdas_ruta - 1) × 0.20 m`, ya que el movimiento A*
es 4-direccional y cada paso equivale a un tamaño de celda.

- **Escenario simple**: 4.80 m
- **Escenario complejo**: 18.80 m

## Tarea 29 — Longitud real recorrida

Suma acumulada del avance odométrico (`avance_ds_m`) durante la ejecución.

- **Escenario simple**: 4.56 m
- **Escenario complejo**: 17.46 m

## Tarea 30 — Error final de posición

Distancia Euclidiana entre la posición odométrica final del robot y la
coordenada exacta de la meta en el mundo Webots.

- **Escenario simple**: 0.0773 m
- **Escenario complejo**: 0.0799 m

## Tarea 31 — Bloqueos y recuperaciones

Número de eventos en que el robot activó la secuencia de recuperación
(retroceso + giro) por quedar atascado. Cada evento equivale a una
situación de cuasi-colisión evitada.

- **Escenario simple**: 0
- **Escenario complejo**: 0

## Tarea 32 — Tabla comparativa: simple vs complejo

| Métrica                         | Escenario simple | Escenario complejo |
| ------------------------------- | :--------------: | :----------------: |
| Celdas en ruta A*               |    25 celdas     |     95 celdas      |
| Waypoints generados             |      8 wps       |       33 wps       |
| Longitud planificada (A*)       |      4.80 m      |      18.80 m       |
| Longitud real recorrida         |      4.56 m      |      17.46 m       |
| Tiempo hasta meta               |     113.92 s     |      466.56 s      |
| Error final de posición         |     0.0773 m     |      0.0799 m      |
| Bloqueos / recuperaciones       |        0         |         0          |
| Robot llegó a la meta           |        Sí        |         Sí         |

### Análisis

| Aspecto | Observación |
| ------- | ----------- |
| Longitud planificada vs real | La distancia real es ligeramente inferior a la planificada. La simplificación de la ruta A* en waypoints permite al robot recortar curvas respecto a la trayectoria celda a celda. La odometría de encoders también puede subestimar el avance al ser corregida por el supervisor Webots. |
| Error final | El error inferior a 0.08 m (tolerancia del seguidor de waypoints) en ambos escenarios confirma que el robot alcanza efectivamente la meta sin necesitar maniobras de recuperación. |
| Bloqueos | Ambos escenarios registraron 0 eventos de bloqueo, lo que indica que la ruta planificada por A* y la navegación reactiva fueron suficientes para transitar ambos laberintos sin quedar atascado. |
| Tiempo | El mayor tiempo en el escenario complejo (~52 s adicionales) refleja la mayor longitud de ruta (+2.0 m planificados) y la velocidad lineal conservadora del seguidor de waypoints. |
