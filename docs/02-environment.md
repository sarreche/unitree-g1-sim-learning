# Entorno comprobado

Inspección: 2026-09-27. WSL2, distribución Ubuntu-22.04, Ubuntu 22.04.5 LTS, usuario Linux sarreche. Repos y virtualenvs bajo /home/sarreche. También hay otra distribución Ubuntu y docker-desktop; no se usaron para esta inspección.

| Componente | unitree-env | unitree-rl-env |
|---|---|---|
| Python | 3.10.12 | 3.10.12 |
| MuJoCo Python | 3.14.0 | 3.2.3 |
| NumPy | 2.2.6 | 2.2.6 |
| PyTorch | No instalado en el inventario | 2.14.0 |
| CycloneDDS Python | 0.10.2 | No instalado en el inventario |
| SDK Python | unitree_sdk2py 1.0.1 | No instalado en el inventario |
| PyYAML | No instalado en el inventario | 6.0.3 |

GCC 11.4.0 y CMake 3.22.1. GPU visible: NVIDIA GeForce RTX 5060 Ti, 8151 MiB. nvidia-smi informa driver 591.86, NVIDIA-SMI 590.57 y compatibilidad CUDA 13.1. Esa cifra no acredita qué toolkit compiló PyTorch. El entorno RL contiene cuda-toolkit 13.0.3.0; no se probó entrenamiento ni rendimiento GPU.

La versión Python de MuJoCo no determina la versión de la biblioteca C++ usada por el binario mjlab. El inventario completo de paquetes y datos de GPU está en environment-inventory.txt.

## Repos externos

Las URLs, commits y archivos modificados están en [upstream-revisions.json](upstream-revisions.json). Para obtener un checkout nuevo de cada repo:

```bash
git clone https://github.com/unitreerobotics/unitree_mujoco.git ~/unitree_mujoco
git clone https://github.com/unitreerobotics/unitree_sdk2_python.git ~/unitree_sdk2_python
git clone https://github.com/unitreerobotics/unitree_rl_gym.git ~/unitree_rl_gym
git clone https://github.com/unitreerobotics/unitree_rl_mjlab.git ~/unitree_rl_mjlab
```

Ejecutar estos comandos solamente si los destinos no existen. En un checkout nuevo, seleccionar el commit correspondiente del manifiesto con git checkout COMMIT. Consultar el README/setup oficial de esa revisión para dependencias y submódulos. No resetear los checkouts existentes: contienen los experimentos originales.

Para low-level se necesita el SDK Python y su CycloneDDS; para deploy RL gym, MuJoCo, torch, numpy y PyYAML. El paquete de entrenamiento RL gym pide isaacgym; no hace falta instalarlo para el deploy que usamos. PYTHONPATH permite encontrar legged_gym, pero no instala sus demás dependencias.

El inventario es una fotografía del entorno, no un lockfile garantizado ni una receta de instalación limpia comprobada.

## Verificación manual

```bash
cat /etc/os-release
~/unitree-env/bin/python --version
~/unitree-env/bin/pip list
~/unitree-rl-env/bin/python --version
~/unitree-rl-env/bin/pip list
gcc --version
cmake --version
nvidia-smi
ip link show lo
```

## Ampliación: instalación Windows, C++ y Conda

La guía [10-windows11-wsl-setup.md](10-windows11-wsl-setup.md) reconstruye instalación, dependencias, venvs, SDK C++ y compilación. Se apoya en comandos locales y fuentes oficiales y distingue recomendaciones de hechos comprobados.

El SDK C++ unitree_sdk2 está instalado bajo /usr/local, con ddsc y ddscxx. Su commit se añadió al manifiesto. El simulador mjlab enlaza MuJoCo C++ 3.3.6; g1_ctrl enlaza ONNX Runtime 1.22.0. ldd resolvió sus dependencias sin entradas not found.

Existe también Miniconda en ~/miniconda3 y un entorno llamado unitree-rl. Es distinto del venv ~/unitree-rl-env; la tabla original solo inventariaba los dos venvs. El soporte gráfico usa WSLg. No se acreditó entrenamiento ni se reinstaló el entorno al documentarlo.

| Componente adicional | Versión inspeccionada |
|---|---|
| Python de Conda unitree-rl | 3.11.16 |
| mjlab en Conda | 1.2.0 |
| unitree_rl_mjlab en Conda | 0.0.1 |
| MuJoCo en Conda | 3.14.0 |
| mujoco-warp en Conda | 3.5.0 |
| NumPy en Conda | 2.4.6 |
| PyTorch en Conda | 2.14.0 |
| ONNX en Conda | 1.23.0 |
| WSLg | 1.0.66 |

La presencia del paquete de entrenamiento en Conda acredita instalación, no una sesión de entrenamiento completada. Se corrige así el alcance del inventario inicial, que omitía ese tercer entorno.
