# Unitree G1 — laboratorio de simulación

From joint-level control to learned locomotion: experiments with the Unitree G1 in MuJoCo.

Este proyecto documenta el aprendizaje de Sarreche con el G1: enviar comandos articulares, leer la IMU, sostener una postura, experimentar con balance P/PD, ejecutar locomoción preentrenada y entrar a una policy de imitación de baile mediante una FSM.

Es un laboratorio educativo independiente, no un fork ni un producto oficial de Unitree. No contiene los repos completos, meshes, pesos, motion references o binarios oficiales. Los scripts recuperados derivan de ejemplos de Unitree y se identifican como tales en [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Qué se hizo y por qué hay tres stacks

| Stack | Control | Policy | Simulación | Aprendizaje |
|---|---|---|---|---|
| unitree_mujoco + unitree_sdk2_python | Articulaciones y PD por DDS | Sin policy aprendida | MuJoCo con bridge | Estado, IMU, postura y límites del balance manual |
| unitree_rl_gym | vx, vy, yaw_rate | TorchScript motion.pt | MuJoCo dentro del deploy Python | Locomoción aprendida y comandos en runtime |
| unitree_rl_mjlab | FSM, locomoción y tracking | ONNX | Simulador y controlador C++ separados | Transiciones entre postura, velocidad y baile |

Los experimentos usaron policies existentes: no se entrenó una policy propia en este trabajo. Mantener una pose no demostró mantener el equilibrio. El balance manual saturaba y se pasó a locomoción aprendida; luego se habilitó el baile por teclado.

## Prerrequisitos y primer recorrido

El entorno comprobado es Ubuntu 22.04.5 en WSL2. Los scripts de teclado requieren una terminal Linux real y una sesión gráfica para MuJoCo. Las dependencias y revisiones exactas están en [02-environment.md](docs/02-environment.md). Windows es la ubicación de esta documentación; ejecutar los scripts desde WSL.

Con los repos y entornos existentes, la prueba más directa es locomoción sin DDS:

```bash
export LAB=/mnt/c/Users/Usuario/Documents/Code-Projects/unitree-g1-sim-learning
source ~/unitree-rl-env/bin/activate
export PYTHONPATH="$HOME/unitree_rl_gym${PYTHONPATH:+:$PYTHONPATH}"
python "$LAB/scripts/deploy_mujoco_keyboard.py" --config "$LAB/configs/rl_gym_g1.yaml"
```

Usar W/S para avance y retroceso, A/D para giro, Q/E para desplazamiento lateral, espacio para detener el comando y X para salir. El foco debe estar en la terminal. Cada tecla sustituye el vector completo; los comandos permanecen activos hasta otra tecla. No cambia los pesos de la policy.

Para una instalación nueva, consultar [environment](docs/02-environment.md), obtener las revisiones indicadas y seguir las instrucciones oficiales de dependencias de cada stack. Este laboratorio no instala el stack de entrenamiento Isaac Gym.

## Arquitectura

```text
Low-level: Python → LowCmd → DDS (domain 1, lo) → MuJoCo → LowState → Python
RL gym: comando → observación → TorchScript → target joints → PD → MuJoCo
Mjlab: teclado/gamepad → FSM → policy ONNX → LowCmd → simulador DDS (domain 0, lo)
```

## Documentación

1. [Visión general](docs/01-overview.md)
2. [Entorno y dependencias](docs/02-environment.md)
3. [Low-level, DDS e IMU](docs/03-unitree-mujoco-low-level.md)
4. [Postura y balance](docs/04-stand-and-balance-experiments.md)
5. [Locomoción y teclado en RL gym](docs/05-unitree-rl-gym.md)
6. [Mjlab, FSM y modificaciones](docs/06-unitree-rl-mjlab.md)
7. [Policies e imitación](docs/07-policies-and-motion-imitation.md)
8. [Sim-to-real](docs/08-sim-to-real-notes.md)
9. [Aprendizajes](docs/09-lessons-learned.md)
10. [Problemas y soluciones](troubleshooting/README.md)
11. [Parches y reproducción](patches/README.md)
12. [Validación realizada](docs/validation.md)

Los controladores low-level son experimentos educativos exclusivos de simulación. No constituyen un controlador validado para un G1 físico. Ver los límites concretos en sim-to-real.

## Fuentes oficiales

- [unitree_mujoco](https://github.com/unitreerobotics/unitree_mujoco)
- [unitree_sdk2_python](https://github.com/unitreerobotics/unitree_sdk2_python)
- [unitree_rl_gym](https://github.com/unitreerobotics/unitree_rl_gym)
- [unitree_rl_mjlab](https://github.com/unitreerobotics/unitree_rl_mjlab)

La documentación refleja el estado local inspeccionado el 27 de septiembre de 2026. Las observaciones de movimiento proceden de los chats unitreerobotics y unitreerobotics2; no se repitieron las pruebas visuales al preparar este repositorio.

## Preparar el repositorio Git

La carpeta está preparada, pero Git no se inicializó y no se creó ni publicó un repositorio remoto. Desde esta carpeta, cuando quieras hacerlo:

```bash
git init
git status --short
git add README.md docs scripts configs patches troubleshooting licenses LICENSE THIRD_PARTY_NOTICES.md .gitignore
git diff --cached --stat
git commit -m "Document Unitree G1 simulation learning lab"
```

La documentación y los aportes originales de Sarreche se ofrecen bajo [licencia MIT](LICENSE). El material de terceros y las partes derivadas conservan sus licencias BSD-3-Clause o Apache-2.0 y sus atribuciones; ver [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

