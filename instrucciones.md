| Proyecto      |     | Final:   |     | Navegación |         |           | Autónoma |           | con |
| ------------- | --- | -------- | --- | ---------- | ------- | --------- | -------- | --------- | --- |
| Planificación |     |          | de  | Rutas      |         | o SLAM    |          | en Webots |     |
|               |     | Robótica |     | y Sistemas |         | Autónomos | 2026-01  |           |     |
|               |     |          |     |            | Código: | ICI 4150  |          |           |     |
|               |     |          |     |            | Sandra  | Cano      |          |           |     |
sandra.cano@pucv.cl
| 1. Contexto |     | del | proyecto |     |     |     |     |     |     |
| ----------- | --- | --- | -------- | --- | --- | --- | --- | --- | --- |
Durante los Laboratorios 1 y 2 se trabajaron los fundamentos necesarios para desarrollar
un sistema de navegación autónoma en un robot móvil diferencial. En el Laboratorio 1 se
abordó el control cinemático del robot mediante las velocidades de las ruedas izquierda y
derecha, analizando movimiento recto, trayectorias curvas, rotación en el lugar y generación
de trayectorias simples. En el Laboratorio 2 se incorporó percepción del entorno mediante
sensores de distancia y encoders, filtrado de mediciones, estimación con filtro de Kalman y
| navegación | reactiva | para | evitar | obstáculos. |     |     |     |     |     |
| ---------- | -------- | ---- | ------ | ----------- | --- | --- | --- | --- | --- |
El proyecto final debe integrar y extender estos aprendizajes. No basta con que el robot
evite obstáculos de manera reactiva: ahora debe navegar con un propósito global, ya sea
planificando una ruta hacia una meta o construyendo un mapa del entorno mediante una
| estrategia  | simplificada | de      | SLAM. |     |     |     |     |     |     |
| ----------- | ------------ | ------- | ----- | --- | --- | --- | --- | --- | --- |
| 2. Objetivo |              | general |       |     |     |     |     |     |     |
Diseñar, implementar y evaluar en Webots un sistema de navegación autónoma para un
robot móvil diferencial, integrando control cinemático, percepción sensorial, estimación de
movimiento y toma de decisiones mediante una solución basada en planificación de rutas
| o en SLAM/mapeo |     | autónomo.   |     |     |     |     |     |     |     |
| --------------- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- |
| 3. Objetivos    |     | específicos |     |     |     |     |     |     |     |
1. Reutilizar el modelo de control diferencial trabajado en el Laboratorio 1 para ejecutar
| desplazamientos, |     | giros | y seguimiento |     | de  | trayectorias. |     |     |     |
| ---------------- | --- | ----- | ------------- | --- | --- | ------------- | --- | --- | --- |
2. Integrar sensores de distancia, LiDAR o proximidad, junto con encoders de rueda, para
| percibir | el entorno | y   | estimar | el movimiento |     | del robot. |     |     |     |
| -------- | ---------- | --- | ------- | ------------- | --- | ---------- | --- | --- | --- |
3. Aplicar filtrado simple o fusión sensorial para mejorar la estabilidad de las mediciones
| utilizadas | por | el sistema | de  | navegación. |     |     |     |     |     |
| ---------- | --- | ---------- | --- | ----------- | --- | --- | --- | --- | --- |
4. Implementar una de las dos líneas de desarrollo: planificación de rutas hacia una meta o
| SLAM/mapeo |     | autónomo. |     |     |     |     |     |     |     |
| ---------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
1

5. Evaluar el desempeño del robot en al menos dos escenarios de Webots, considerando
eficiencia, estabilidad, colisiones, calidad de la ruta o calidad del mapa generado.
| 4. Grupo |     | de  | trabajo |     |     |     |
| -------- | --- | --- | ------- | --- | --- | --- |
El proyecto se desarrollará en grupos de hasta 5 estudiantes. Cada grupo deberá or-
ganizar roles de trabajo, por ejemplo: programación del controlador, diseño del entorno,
| análisis       | de datos, | documentación |     | y       | preparación | de evidencias. |
| -------------- | --------- | ------------- | --- | ------- | ----------- | -------------- |
| 5. Descripción |           |               |     | general | del         | proyecto       |
Cada grupo deberá implementar un robot móvil diferencial en Webots, preferentemente
e-puck o un robot equivalente, capaz de desplazarse en un entorno con obstáculos. El robot
deberá utilizar sensores y encoders para tomar decisiones de navegación y deberá demostrar
| una estrategia |     | global | para | alcanzar | un objetivo. |     |
| -------------- | --- | ------ | ---- | -------- | ------------ | --- |
El sistema debe considerar al menos los siguientes componentes:
Control de movimiento: uso de motores diferenciales y velocidades de rueda para
| avanzar, | girar | y seguir | una | trayectoria. |     |     |
| -------- | ----- | -------- | --- | ------------ | --- | --- |
Percepción del entorno:usodesensoresdedistancia,proximidad,ultrasonidooLiDAR
| para | detectar | obstáculos. |     |     |     |     |
| ---- | -------- | ----------- | --- | --- | --- | --- |
Estimación de movimiento: uso de encoders para estimar desplazamiento, orientación
| o posición |     | aproximada | del | robot. |     |     |
| ---------- | --- | ---------- | --- | ------ | --- | --- |
Navegación local: evitación de obstáculos usando reglas reactivas o control basado en
sensores.
Navegación global: planificación de rutas o construcción de mapa del entorno.
Evaluación experimental: registro de resultados, métricas, gráficos y análisis del com-
| portamiento |     | del robot. |            |     |     |     |
| ----------- | --- | ---------- | ---------- | --- | --- | --- |
| 6. Líneas   |     | de         | desarrollo |     |     |     |
Cada grupo deberá seleccionar una de las siguientes líneas. Ambas son válidas, pero
| deben cumplir |       | con los | requisitos    | mínimos | indicados. |     |
| ------------- | ----- | ------- | ------------- | ------- | ---------- | --- |
| 6.1.          | Línea | A:      | Planificación |         | de rutas   |     |
Esta línea corresponde al nivel base recomendado para el proyecto final. El robot debe
navegar desde una posición inicial hasta una meta dentro de un entorno con obstáculos,
| utilizando | un  | algoritmo | de  | planificación | de rutas. |     |
| ---------- | --- | --------- | --- | ------------- | --------- | --- |
2

| Requisitos | mínimos |     |     |     |
| ---------- | ------- | --- | --- | --- |
Diseñar un entorno en Webots con obstáculos, pasillos o zonas restringidas.
| Definir una | posición | inicial y una | meta. |     |
| ----------- | -------- | ------------- | ----- | --- |
Representar el entorno mediante una grilla de ocupación, matriz 2D, grafo, nodos o mapa
discreto.
Implementar un algoritmo de planificación, por ejemplo A*, Dijkstra, BFS, RRT básico
| u otro algoritmo | justificado. |                 |                |     |
| ---------------- | ------------ | --------------- | -------------- | --- |
| Generar          | una ruta     | desde el inicio | hasta la meta. |     |
Convertir la ruta planificada en puntos intermedios o comandos de movimiento para el
robot.
Usar sensores para evitar obstáculos, corregir la trayectoria o detener el robot ante riesgo
de colisión.
Registrar y analizar el comportamiento del robot durante la ejecución de la ruta.
| Resultado | esperado |     |     |     |
| --------- | -------- | --- | --- | --- |
El robot debe desplazarse de manera autónoma desde el punto inicial hasta la meta,
siguiendounarutaplanificadayevitandocolisiones.Elgrupodebemostrarlarutacalculada,
| la trayectoria | ejecutada | y el análisis | de diferencias | entre ambas. |
| -------------- | --------- | ------------- | -------------- | ------------ |
| 6.2. Línea     | B: SLAM   | o mapeo       | autónomo       | simplificado |
Esta línea corresponde a un nivel avanzado. El robot debe explorar un entorno desco-
nocido o parcialmente conocido, estimar su movimiento y construir una representación del
entorno.
| Requisitos | mínimos |     |     |     |
| ---------- | ------- | --- | --- | --- |
Diseñar un entorno desconocido o parcialmente conocido en Webots.
Utilizar sensores de distancia, proximidad o LiDAR para detectar obstáculos.
Utilizar encoders para estimar desplazamiento y orientación mediante odometría.
Construir o actualizar un mapa del entorno, por ejemplo una grilla de ocupación 2D.
Implementar una estrategia de exploración o navegación que permita recorrer el entorno.
Visualizar el mapa generado o presentar gráficos que evidencien el proceso de mapeo.
Analizar los errores de localización, acumulación de error odométrico o limitaciones del
| mapa generado. |          |     |     |     |
| -------------- | -------- | --- | --- | --- |
| Resultado      | esperado |     |     |     |
El robot debe recorrer el entorno y generar una representación del espacio explorado. No
se exige una implementación profesional de SLAM, pero sí se espera que el grupo demuestre
la idea central: estimar dónde está el robot y actualizar un mapa a partir de sus sensores.
3

| 7.  | Modelo | de  | movimiento |     |     |     | sugerido |     |     |     |
| --- | ------ | --- | ---------- | --- | --- | --- | -------- | --- | --- | --- |
Para conectar el proyecto con el Laboratorio 1, se recomienda utilizar el modelo cine-
mático diferencial. Si v es la velocidad de la rueda derecha, v la velocidad de la rueda
|           |        |           | r     |         |     |           |      |     | l   |     |
| --------- | ------ | --------- | ----- | ------- | --- | --------- | ---- | --- | --- | --- |
| izquierda | y L la | distancia | entre | ruedas, |     | entonces: |      |     |     |     |
|           |        |           |       |         |     |           | v +v |     |     |     |
|           |        |           |       |         |     |           | r    | l   |     |     |
|           |        |           |       |         |     | v =       |      |     |     | (1) |
2
|     |     |     |     |     |     |     | v −v |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- |
|     |     |     |     |     |     |     | r    | l   |     |     |
|     |     |     |     |     |     | ω = |      |     |     | (2) |
L
Para estimar el movimiento a partir de encoders, se puede utilizar:
|     |     |     |     | ∆s  | = r∆θ | ,      | ∆s       | = r∆θ  |          | (3) |
| --- | --- | --- | --- | --- | ----- | ------ | -------- | ------ | -------- | --- |
|     |     |     |     |     | r     | r      |          | l l    |          |     |
|     |     |     |     | ∆s  | +∆s   |        |          | ∆s −∆s |          |     |
|     |     |     | ∆s  | =   | r     | l ,    | ∆φ       | = r    | l        | (4) |
|     |     |     |     |     | 2     |        |          | L      |          |     |
|     |     |     |     |     |       |        | (cid:18) | ∆φ     | (cid:19) |     |
|     |     |     |     | x = | x     | +∆scos |          | φ +    |          | (5) |
|     |     |     |     | k   | k−1   |        |          | k−1    |          |     |
2
|     |     |     |     |     |     |        | (cid:18) | ∆φ (cid:19) |     |     |
| --- | --- | --- | --- | --- | --- | ------ | -------- | ----------- | --- | --- |
|     |     |     |     | y = | y   | +∆ssin |          | φ +         |     | (6) |
|     |     |     |     | k   | k−1 |        |          | k−1         |     |     |
2
|     |     |     |     |     | φ   | = φ | +∆φ |     |     | (7) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     | k   | k−1 |     |     |     |
Estas ecuaciones pueden utilizarse para estimar la trayectoria del robot, corregir desvia-
ciones, alimentar una grilla de ocupación o apoyar el seguimiento de rutas.
| 8.         | Tecnologías |         | y           | herramientas |              |     |     |     |     |     |
| ---------- | ----------- | ------- | ----------- | ------------ | ------------ | --- | --- | --- | --- | --- |
| Simulador: |             | Webots. |             |              |              |     |     |     |     |     |
| Robot:     | e-puck      | o robot | diferencial |              | equivalente. |     |     |     |     |     |
| Lenguaje:  | Python      |         | o C++.      |              |              |     |     |     |     |     |
Sensores: sensores de distancia, proximidad, ultrasonido o LiDAR; encoders de rueda.
Control: cinemática diferencial, seguimiento de puntos intermedios, control proporcional
| o reglas | de navegación. |     |     |     |     |     |     |     |     |     |
| -------- | -------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Algoritmos posibles: A*, Dijkstra, BFS, RRT, grilla de ocupación, odometría, mapeo
| 2D, | SLAM simplificado, |     |     | filtrado | simple | o   | Kalman. |     |     |     |
| --- | ------------------ | --- | --- | -------- | ------ | --- | ------- | --- | --- | --- |
Gestión del proyecto: repositorio GitHub con código, documentación, evidencias y
resultados.
4

| 9. Escenarios |     |     | de  | prueba |     |     |     |
| ------------- | --- | --- | --- | ------ | --- | --- | --- |
Cada grupo deberá evaluar su sistema en al menos dos escenarios:
1. Escenario simple: pocos obstáculos, ruta relativamente directa y baja complejidad.
2. Escenario complejo: mayor cantidad de obstáculos, pasillos estrechos, curvas, zonas de
| bloqueo | o rutas | alternativas. |     |     |     |     |     |
| ------- | ------- | ------------- | --- | --- | --- | --- | --- |
En ambos escenarios se debe analizar si el robot logra navegar de manera estable, si
evita colisiones, si llega a la meta o si genera un mapa coherente del entorno.
| 10. | Métricas |     | de evaluación |     |     | experimental |     |
| --- | -------- | --- | ------------- | --- | --- | ------------ | --- |
El informe final debe incluir resultados cuantitativos y cualitativos. Algunas métricas
| sugeridas   | son:          |                   |             |               |             |          |            |
| ----------- | ------------- | ----------------- | ----------- | ------------- | ----------- | -------- | ---------- |
| Tiempo      | total hasta   | llegar            | a           | la meta.      |             |          |            |
| Longitud    | de la         | ruta planificada. |             |               |             |          |            |
| Longitud    | aproximada    |                   | de la       | trayectoria   | ejecutada.  |          |            |
| Diferencia  | entre         | ruta              | planificada | y             | trayectoria | real.    |            |
| Número      | de colisiones |                   | o casi      | colisiones.   |             |          |            |
| Número      | de giros      | innecesarios.     |             |               |             |          |            |
| Error       | de posición   | u orientación     |             | estimado      |             | mediante | odometría. |
| Estabilidad | de            | las mediciones    |             | crudas,       | filtradas   | y        | estimadas. |
| Calidad     | del mapa      | generado,         |             | si se trabaja |             | con SLAM | o mapeo.   |
| Porcentaje  | de            | ejecuciones       | exitosas    |               | en varias   | pruebas. |            |
| 11.         | Entregables   |                   |             |               |             |          |            |
| 11.1.       | Repositorio   |                   | GitHub      |               |             |          |            |
El repositorio debe ser público o compartido con el docente. Debe incluir:
| Código | fuente | completo | del | controlador |     | del robot. |     |
| ------ | ------ | -------- | --- | ----------- | --- | ---------- | --- |
Archivos de mundo de Webots y recursos necesarios para ejecutar la simulación.
| Archivos  | de datos | registrados, |        | si corresponde. |                     |     |     |
| --------- | -------- | ------------ | ------ | --------------- | ------------------- | --- | --- |
| Gráficos, | capturas | o            | videos | cortos          | del funcionamiento. |     |     |
README.md completo y ordenado, el cual actuará como informe del proyecto.
5

| 11.2. | README.md |     |     |     |     |     |     |     |
| ----- | --------- | --- | --- | --- | --- | --- | --- | --- |
El archivo README.md debe actuar como informe técnico del proyecto. Toda la do-
cumentación del diseño, implementación, evaluación, resultados y conclusiones debe estar
integrada en el README.md del repositorio. No se debe entregar un informe final en PDF.
| El README.md        |           | debe          | incluir        |                  | al menos:  |                |               |     |
| ------------------- | --------- | ------------- | -------------- | ---------------- | ---------- | -------------- | ------------- | --- |
| Nombre              | del       | proyecto      | e              | integrantes      |            | del            | grupo.        |     |
| Línea seleccionada: |           |               | planificación  |                  |            | de rutas       | o SLAM/mapeo. |     |
| Objetivo            | del       | proyecto.     |                |                  |            |                |               |     |
| Descripción         |           | del robot,    |                | sensores         | y          | actuadores     | utilizados.   |     |
| Descripción         |           | de los        | escenarios     |                  | de prueba. |                |               |     |
| Explicación         |           | del algoritmo |                | implementado.    |            |                |               |     |
| Diagrama            | de        | flujo         | o pseudocódigo |                  |            | de la          | solución.     |     |
| Relación            | explícita |               | con            | los Laboratorios |            |                | 1 y 2.        |     |
| Resultados          | obtenidos |               |                | y métricas       |            | de desempeño.  |               |     |
| Capturas,           | gráficos  |               | o enlaces      |                  | a videos.  |                |               |     |
| Instrucciones       |           | claras        | para           | ejecutar         |            | la simulación. |               |     |
| Conclusiones,       |           | limitaciones  |                | y                | posibles   | mejoras.       |               |     |
| 11.3.               | Formato   |               | de             | entrega          |            |                |               |     |
La entrega se realizará solo mediante el repositorio GitHub. No se debe entregar
informe final en PDF. El README.md será considerado el informe oficial del proyecto y
debecontenerlaexplicacióncompletadelasolución,lasevidencias,losresultados,elanálisis
y las conclusiones.
| 11.4. | Video | demostrativo |     |     |     |     |     |     |
| ----- | ----- | ------------ | --- | --- | --- | --- | --- | --- |
El video debe estar enlazado o incluido en el repositorio y mostrar la ejecución del robot
en Webots. Debe evidenciar el comportamiento del sistema en los escenarios de prueba, la
ruta seguida o el mapa generado, y el resultado final de la navegación.
| 12. Criterios |     |     | de          | evaluación |     |     |     |         |
| ------------- | --- | --- | ----------- | ---------- | --- | --- | --- | ------- |
| Criterio      |     |     | Descripción |            |     |     |     | Puntaje |
Configuración del Configura correctamente Webots, robot diferencial, 10 pts
entorno, robot y motores, sensores y encoders. Diseña al menos dos
| sensores |     |     | escenarios |     | de  | prueba | reproducibles. |     |
| -------- | --- | --- | ---------- | --- | --- | ------ | -------------- | --- |
6

| Criterio |     | Descripción |     |     |     |     |     |     | Puntaje |
| -------- | --- | ----------- | --- | --- | --- | --- | --- | --- | ------- |
Integración de Evidencia uso del control cinemático diferencial, 15 pts
Laboratorios 1 y 2 lectura de sensores, encoders, filtrado o estimación.
|     |     | Explica | cómo | el  | proyecto | extiende | lo aprendido | en  |     |
| --- | --- | ------- | ---- | --- | -------- | -------- | ------------ | --- | --- |
los laboratorios.
Implementación Implementa correctamente el algoritmo de 25 pts
| del algoritmo |     | planificación |     | de          | rutas    | o la estrategia   | de         |        |     |
| ------------- | --- | ------------- | --- | ----------- | -------- | ----------------- | ---------- | ------ | --- |
| principal     |     | SLAM/mapeo.   |     | La          | solución | está justificada, |            |        |     |
|               |     | documentada   |     | y conectada |          | con la            | navegación | global |     |
del robot.
Control de El robot ejecuta la ruta, sigue puntos intermedios, 15 pts
movimiento y corrige desviaciones, evita obstáculos y se detiene
ejecución de la adecuadamente al alcanzar la meta o completar la
| navegación |     | exploración. |     |     |     |     |     |     |     |
| ---------- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- |
Uso de sensores, Utiliza información sensorial para tomar decisiones. 15 pts
| encoders | y   | Incluye | lectura | de  | sensores, | uso de | encoders, |     |     |
| -------- | --- | ------- | ------- | --- | --------- | ------ | --------- | --- | --- |
estimación odometría y, cuando corresponda, filtrado simple o
Kalman.
Evaluación Presenta resultados en dos escenarios, compara 10 pts
experimental y desempeño, analiza métricas, limitaciones, errores y
| análisis     |         | posibles      | mejoras.    |           |           |          |            |     |         |
| ------------ | ------- | ------------- | ----------- | --------- | --------- | -------- | ---------- | --- | ------- |
| Repositorio, |         | Entrega       | repositorio |           | completo, | ordenado | y          |     | 10 pts  |
| README       | y       | reproducible, |             | con       | código,   | mundo    | de Webots, |     |         |
| evidencias   |         | README,       |             | informe,  | capturas, | gráficos | o video.   |     |         |
| Total        |         |               |             |           |           |          |            |     | 100 pts |
| 13.          | Niveles | de logro      |             | esperados |           |          |            |     |         |
Excelente
El robot navega de forma autónoma en ambos escenarios, llega a la meta o genera
un mapa coherente, usa sensores y encoders de forma efectiva, documenta claramente el
| algoritmo | y presenta | un análisis | experimental |     |     | completo. |     |     |     |
| --------- | ---------- | ----------- | ------------ | --- | --- | --------- | --- | --- | --- |
Bueno
El robot cumple la mayor parte de los objetivos, aunque presenta limitaciones menores
en seguimiento de ruta, estabilidad del movimiento, documentación o análisis de resultados.
Suficiente
El robot logra una navegación parcial o un mapeo básico, pero la implementación, la
| evaluación | o la documentación |     | son | incompletas. |     |     |     |     |     |
| ---------- | ------------------ | --- | --- | ------------ | --- | --- | --- | --- | --- |
7

Insuficiente
No se evidencia una implementación funcional de navegación autónoma, planificación de
rutas o mapeo. Faltan código, evidencias o instrucciones para reproducir el proyecto.
14. Recomendación final
Para la mayoría de los grupos se recomienda implementar la Línea A: planificación de
rutas con A* sobre una grilla de ocupación, complementada con evitación reactiva de
obstáculos. Los grupos que deseen mayor desafío pueden desarrollar la Línea B: SLAM o
mapeo autónomo simplificado, utilizando odometría, sensores de distancia y una grilla
de ocupación.
8