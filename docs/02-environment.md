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
