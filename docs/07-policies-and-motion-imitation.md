# Policies y motion imitation

Todos estos archivos permanecen en el repo oficial externo. No se copian a este laboratorio.

| Función | Ruta relativa a unitree_rl_mjlab |
|---|---|
| Velocity policy | deploy/robots/g1/config/policy/velocity/v0/exported/policy.onnx |
| Velocity parámetros | deploy/robots/g1/config/policy/velocity/v0/params/deploy.yaml |
| Mimic policy | deploy/robots/g1/config/policy/mimic/dance1_subject2/exported/policy.onnx |
| Tensores externos ONNX | deploy/robots/g1/config/policy/mimic/dance1_subject2/exported/policy.onnx.data |
| Referencia motion | deploy/robots/g1/config/policy/mimic/dance1_subject2/params/dance1_subject2.npz |
| Mimic parámetros | deploy/robots/g1/config/policy/mimic/dance1_subject2/params/deploy.yaml |

Velocity acepta comandos de velocidad y usa observaciones de velocidad angular, gravedad, comando, fase, posiciones, velocidades y acción previa. Sus parámetros mapean 29 articulaciones y step_dt=0.02. No es la policy de 12 acciones de RL gym.

Mimic incluye motion_command y orientación del anchor en sus observaciones. La referencia npz describe la trayectoria a seguir; policy.onnx representa la función aprendida que transforma observaciones en acciones. policy.onnx.data contiene tensores externos requeridos por ese modelo: mantenerlo junto al ONNX. deploy.yaml define escalas, ganancias y orden de observaciones/articulaciones.

El baile no consiste solo en mover gráficamente los joints frame por frame: el controlador usa una policy para intentar seguir una referencia bajo la dinámica de la simulación. Tener el npz no equivale a tener una policy entrenada para cualquier motion nueva.

En el chat se reportó entrada real a Mimic_Dance1_subject2, baile y regreso a Velocity. También transiciones rápidas repetidas. No se midió fidelidad del tracking ni se validó en robot real.

La estructura real del archivo npz inspeccionado está en motion-reference-inventory.json; se leyó con allow_pickle=False, sin alterar el archivo ni ejecutar entrenamiento. Obtener modelos y referencias desde la revisión oficial correspondiente; no asumir que todas las licencias de datos y dependencias son iguales a la licencia raíz.

## Referencia inspeccionada

El npz contiene 6574 frames a 50 fps: duración nominal 131.48 s al contar todos los samples (el intervalo entre primer y último frame es 131.46 s). Incluye joint_pos y joint_vel con 29 articulaciones, y posición, quaternion, velocidad lineal y angular de 30 cuerpos. Esto describe el archivo; no demuestra que una sesión de baile completara toda la secuencia.
