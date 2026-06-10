# Grillas de ocupacion

Convencion usada en los CSV:

- `0`: celda libre
- `1`: obstaculo
- `2`: posicion inicial del robot
- `3`: meta

Las grillas `scenario1_grid.csv`, `scenario2_grid.csv` y `scenario3_grid.csv`
fueron generadas desde los archivos `.wbt` correspondientes usando una
resolucion de `0.2 m` por celda, consistente con `TAMANO_CELDA` en
`controllers/final_controller/config.py`.

Los obstaculos se marcaron con un margen de seguridad de `0.10 m`, consistente
con `MARGEN_SEGURIDAD_GRILLA`, para que A* no planifique pegado a paredes u
obstaculos.

Para `scenario2.wbt` se uso una posicion inicial aproximada en
`(-1.28, -1.28)`, porque ese mundo no contiene un nodo `MyProto` con robot.
