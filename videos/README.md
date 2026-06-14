# Videos demostrativos

Esta carpeta contiene los videos de demostración del robot navegando en ambos escenarios.

## Videos requeridos

| Archivo esperado | Escenario | Duración sugerida |
|-----------------|-----------|-------------------|
| `demo_maze_simple.mp4` | Laberinto simple | Desde inicio hasta META_ALCANZADA (~2 min) |
| `demo_maze_complex.mp4` | Laberinto complejo | Desde inicio hasta META_ALCANZADA (~3 min) |

## Cómo grabar el video

### Opción 1 — Grabación con OBS Studio (recomendada)

1. Abrir el escenario en Webots (`worlds/maze_simple.wbt`).
2. Abrir OBS Studio → agregar fuente "Captura de ventana" → seleccionar Webots.
3. Iniciar grabación en OBS.
4. Presionar ▶ en Webots y dejar correr hasta que el robot llegue a la meta.
5. Detener grabación.
6. Repetir para `maze_complex.wbt`.

### Opción 2 — Grabación integrada de Webots

Webots permite grabar video directamente:

1. Ir a `Tools → Movie Recorder...`
2. Configurar resolución y FPS (720p, 30 fps es suficiente).
3. Presionar ▶ para iniciar simulación y grabación.
4. Detener cuando el robot llegue a la meta.
5. El video se guarda automáticamente.

## Qué debe mostrar el video

- La ventana 3D de Webots con el robot moviéndose.
- El robot siguiendo la ruta planificada por A\*.
- La evasión de paredes en los pasillos.
- El robot llegando a la meta (celda superior derecha).
- Idealmente la consola de Webots visible mostrando el estado (`SEGUIR_RUTA`, `META_ALCANZADA`, etc.).

## Nota sobre tamaño

No subir archivos de más de 100 MB directamente al repositorio. Si el video es pesado, subir a YouTube (modo no listado) y actualizar la sección "Video demostrativo" del README principal con el enlace.
