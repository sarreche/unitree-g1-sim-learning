# Locomoción preentrenada y comandos en runtime

Este flujo usa deploy/deploy_mujoco/deploy_mujoco.py y su propio modelo MuJoCo: no requiere iniciar el bridge DDS anterior. Policy: deploy/pre_train/g1/motion.pt (TorchScript). Escena: resources/robots/g1_description/scene.xml. Config oficial: deploy/deploy_mujoco/configs/g1.yaml.

El vector cmd_init=[vx,vy,yaw_rate] expresa velocidad longitudinal, lateral y angular deseada. No son ángulos articulares. La policy genera 12 acciones para las seis articulaciones de cada pierna.

| Observación | Cantidad |
|---|---:|
| Velocidad angular escalada | 3 |
| Gravedad proyectada | 3 |
| Comando escalado | 3 |
| Posiciones relativas | 12 |
| Velocidades articulares | 12 |
| Acción anterior | 12 |
| Seno y coseno de fase | 2 |
| Total | 47 |

La acción se transforma en objetivo articular = acción*0.25 + postura nominal. Un PD aplica los torques. simulation_dt=0.002 y control_decimation=10: física nominal a 500 Hz e inferencia a 50 Hz. La fase usa un periodo de 0.8 s. No importar las dimensiones de la policy ONNX de mjlab a este flujo.

Se observaron quietud con [0,0,0], avance, lateral, giro y avance combinado con giro, con estabilidad cualitativa y pequeñas oscilaciones en quietud. No se registró una evaluación cuantitativa. La interfaz de teclado recuperada sustituye el vector entero: no combina W y A automáticamente. Para avance+giro, editar cmd_init en una copia de config y ejecutar sin pulsar otra tecla.

## Teclado recuperado

| Tecla | cmd |
|---|---|
| W | [0.3,0,0] |
| S | [-0.3,0,0] |
| A | [0,0,0.4] |
| D | [0,0,-0.4] |
| Q | [0,0.2,0] |
| E | [0,-0.2,0] |
| Espacio | [0,0,0] |
| X | Salir |

El script usa sys/select/termios/tty y lee stdin sin bloquear. La limpieza restaura la terminal con try/finally, acepta una ruta explícita de configuración y conserva los valores de comandos. El comando persistirá al soltar una tecla. Espacio significa velocidad objetivo cero; la policy sigue funcionando.

Ver el quick start del README. Para reproducir el deploy oficial sin teclado:

```bash
source ~/unitree-rl-env/bin/activate
export PYTHONPATH="$HOME/unitree_rl_gym${PYTHONPATH:+:$PYTHONPATH}"
cd ~/unitree_rl_gym/deploy/deploy_mujoco
python deploy_mujoco.py g1.yaml
```

pip install -e . falló por isaacgym. PYTHONPATH permitió importar legged_gym para este deploy sin instalar el stack de entrenamiento. El archivo .pt se carga con torch.jit.load; registrar el texto exacto de warnings antes de atribuir una causa. El relato menciona un warning pero no permite identificarlo de forma inequívoca.

La config original terminaba a los 60 segundos de reloj; la local se amplió a 3600.0. El final al minuto era un límite del bucle, no una caída de la policy. Se reportó posible segfault al cerrar el viewer; no se confirmó su causa ni se afirma haberlo resuelto.
