# De Windows 11 a los entornos del laboratorio

Esta guía combina comandos recuperados del historial Linux, configuración y binarios inspeccionados, y pasos actuales de las fuentes oficiales. No es una transcripción completa del chat ni una instalación desde cero ensayada. Los pasos de Windows son una guía para reproducir la base; no se conserva evidencia de cada comando usado originalmente allí.

## 1. Mapa del entorno

```text
Windows 11
 ├─ driver NVIDIA del host
 ├─ WSL2 + Ubuntu-22.04 + WSLg
 │   ├─ ~/unitree-env       → SDK Python + MuJoCo + DDS
 │   ├─ ~/unitree-rl-env    → deploy TorchScript en MuJoCo
 │   ├─ ~/miniconda3       → instalación adicional de Conda
 │   └─ /usr/local        → SDK C++ + bibliotecas DDS
 └─ C:\...\unitree-g1-sim-learning → documentación, scripts y parches
```

Los repos oficiales usados están bajo /home/sarreche, dentro de Ubuntu. El laboratorio vive en Windows y es accesible mediante /mnt/c. El usuario Linux puede tener otro nombre: ~ y $HOME deben resolver a su propio directorio.

## 2. WSL2 y Ubuntu desde PowerShell

En Windows, abrir PowerShell como administrador. En una máquina nueva:

```powershell
wsl --list --online
wsl --install -d Ubuntu-22.04
```

Reiniciar si el instalador lo solicita y crear usuario/contraseña Linux al abrir Ubuntu. Si ya existe esa distribución, no reinstalarla. Verificar y abrir explícitamente la correcta:

```powershell
wsl --list --verbose
wsl --version
wsl -d Ubuntu-22.04
```

La columna VERSION debe mostrar 2. Si muestra 1, convertir esa distribución con wsl --set-version Ubuntu-22.04 2. Consultar [instalación oficial de WSL](https://learn.microsoft.com/en-us/windows/wsl/install) para los requisitos y errores de instalación.

Si falta soporte gráfico en una instalación antigua, actualizar WSL desde PowerShell con wsl --update y reiniciar la sesión de Ubuntu cuando termine. WSLg integra ventanas Linux en Windows; no se documentó el uso de un servidor X externo. Fuente: [aplicaciones gráficas con WSL](https://learn.microsoft.com/en-us/windows/wsl/tutorials/gui-apps).

## 3. Driver, GPU y gráficos

El driver NVIDIA se instala en Windows. Comprobar nvidia-smi primero en PowerShell y luego en Ubuntu. El chat aportó salida del host para RTX 5060 Ti de 8 GB, driver 591.86 y compatibilidad CUDA 13.1; la inspección posterior comprobó visibilidad también en WSL.

No instalar un driver NVIDIA Linux dentro de WSL para este flujo: el host proporciona el acceso GPU. CUDA indicado por nvidia-smi no equivale al toolkit instalado ni a torch.version.cuda. Fuente: [NVIDIA CUDA on WSL](https://docs.nvidia.com/cuda/wsl-user-guide/).

En Ubuntu:

```bash
cat /etc/os-release
uname -m
nvidia-smi
test -d /mnt/wslg && echo "WSLg disponible"
printf 'DISPLAY=%s\nWAYLAND_DISPLAY=%s\n' "$DISPLAY" "$WAYLAND_DISPLAY"
```

El deploy RL gym recuperado carga la policy sin enviarla a CUDA. Una GPU visible no es una condición suficiente para el viewer ni demuestra entrenamiento GPU. El viewer necesita una sesión gráfica y OpenGL; no exportar DISPLAY arbitrariamente si WSLg ya lo proporciona.

## 4. Herramientas base en Ubuntu

Se recuperaron del historial la instalación de Git, pip, venv, CMake y build-essential, seguida por las dependencias C++ y GLFW. Una secuencia consolidada es:

```bash
sudo apt update
sudo apt install -y git python3-pip python3-venv cmake build-essential \
  libyaml-cpp-dev libboost-all-dev libeigen3-dev libspdlog-dev libfmt-dev \
  libglfw3-dev zlib1g-dev
```

zlib1g-dev se incluye porque el CMake del controlador exige ZLIB; no se afirma que formara parte del primer comando histórico. No hace falta reinstalar las dependencias para usar los binarios existentes.

## 5. Obtener repos y conservar revisiones

Clonar cada repo en Linux, solo si no existe. Los cuatro principales y sus commits están en [upstream-revisions.json](upstream-revisions.json). Para el despliegue C++ también hace falta [unitree_sdk2](https://github.com/unitreerobotics/unitree_sdk2), cuya revisión se añadió al manifiesto.

```bash
cd ~
git clone https://github.com/unitreerobotics/unitree_mujoco.git
git clone https://github.com/unitreerobotics/unitree_sdk2_python.git
git clone https://github.com/unitreerobotics/unitree_rl_gym.git
git clone https://github.com/unitreerobotics/unitree_rl_mjlab.git
git clone https://github.com/unitreerobotics/unitree_sdk2.git
```

En cada checkout nuevo seleccionar el commit registrado, antes de aplicar nuestros parches. No resetear ni reemplazar los originales con cambios locales. Los repos, sus bibliotecas y modelos siguen externos al laboratorio.

## 6. Entorno low-level Python

Estos pasos sí tienen correspondencia en el historial: creación de unitree-env, instalación editable del SDK, import de comprobación e instalación de mujoco/pygame.

```bash
python3 -m venv ~/unitree-env
source ~/unitree-env/bin/activate
python -m pip install --upgrade pip
cd ~/unitree_sdk2_python
python -m pip install -e .
python -m pip install mujoco==3.14.0 pygame==2.6.1 numpy==2.2.6
python -c "import unitree_sdk2py, mujoco; print('SDK OK; MuJoCo', mujoco.__version__)"
```

Las versiones fijadas reflejan la fotografía entregada; los comandos históricos de MuJoCo y pygame no fijaban versión. El SDK requiere cyclonedds 0.10.2. No hay evidencia recuperada de haber compilado CycloneDDS manualmente para instalar este paquete Python.

Si falla con Could not locate cyclonedds, el README oficial del SDK ofrece compilar releases/0.10.x y exportar CYCLONEDDS_HOME. Es una alternativa condicional, no un paso demostrado de nuestra instalación. No confundirla con ddsc/ddscxx instalados por el SDK C++.

Aplicar la configuración G1/sin joystick/banda según [patches](../patches/README.md). Después iniciar el simulador desde su directorio, para que las rutas relativas de la escena se resuelvan:

```bash
cd ~/unitree_mujoco/simulate_python
python unitree_mujoco.py
```

Desde otra terminal activar el mismo venv y ejecutar uno de nuestros controladores como explica [low-level](03-unitree-mujoco-low-level.md). Domain 1 / lo en ambos procesos. Tener una ventana visible y recibir LowState son comprobaciones diferentes.

## 7. Entorno de deploy RL gym

El historial confirma un venv separado y pip install torch mujoco==3.2.3 pyyaml. Para preservar la versión inspeccionada de las bibliotecas principales:

```bash
python3 -m venv ~/unitree-rl-env
source ~/unitree-rl-env/bin/activate
python -m pip install --upgrade pip
python -m pip install torch==2.14.0 mujoco==3.2.3 numpy==2.2.6 PyYAML==6.0.3
export PYTHONPATH="$HOME/unitree_rl_gym${PYTHONPATH:+:$PYTHONPATH}"
python -c "import torch, mujoco, legged_gym; print(torch.__version__, mujoco.__version__)"
```

No se comprobó disponibilidad futura de esas versiones en todos los índices/plataformas. El inventario no es un lockfile. No instalar isaacgym para ejecutar este deploy: el intento de pip install -e . del paquete de entrenamiento falló por esa dependencia. PYTHONPATH resuelve legged_gym, no instala dependencias.

Para ejecutar el código oficial con la config ajustada:

```bash
cd ~/unitree_rl_gym
python deploy/deploy_mujoco/deploy_mujoco.py g1.yaml
```

Para nuestro teclado ver README y [RL gym](05-unitree-rl-gym.md). No iniciar otro simulador DDS: este script crea su propio MuJoCo. El límite de 60 s original se cambió a 3600 s.

## 8. SDK C++ requerido por mjlab

El historial registra cmake .., make -j4 y sudo make install. CMakeCache e install_manifest confirman prefijo /usr/local. No fue /opt/unitree_robotics, aunque ese sea un destino recomendado en el README de Unitree.

En un checkout nuevo:

```bash
cmake -S ~/unitree_sdk2 -B ~/unitree_sdk2/build -DCMAKE_INSTALL_PREFIX=/usr/local
cmake --build ~/unitree_sdk2/build -j4
sudo cmake --install ~/unitree_sdk2/build
sudo ldconfig
```

ldconfig es un paso de reproducción para actualizar la búsqueda de bibliotecas, no un comando recuperado del historial seleccionado. El SDK instala headers, biblioteca Unitree y DDS C/C++; el controlador utiliza /usr/local/include/ddscxx. No cambiar de prefijo en un build existente sin revisar sus caches y rutas de búsqueda.

## 9. Compilar los dos componentes mjlab

En la revisión inspeccionada, simulate/mujoco forma parte del checkout y contiene libmujoco.so.3.3.6; no es un enlace a ~/.mujoco. La biblioteca C++ es independiente de ambos paquetes Python. ONNX Runtime 1.22.0 está bajo deploy/thirdparty/onnxruntime-linux-x64-1.22.0.

```bash
cmake -S ~/unitree_rl_mjlab/simulate -B ~/unitree_rl_mjlab/simulate/build
cmake --build ~/unitree_rl_mjlab/simulate/build -j4
cmake -S ~/unitree_rl_mjlab/deploy/robots/g1 -B ~/unitree_rl_mjlab/deploy/robots/g1/build
cmake --build ~/unitree_rl_mjlab/deploy/robots/g1/build -j4
```

Si ONNX Runtime o MuJoCo vendorizados faltan, comprobar checkout, arquitectura x86_64 y las instrucciones de esa revisión. No copiar los binarios al laboratorio ni sustituirlos por el paquete pip suponiendo equivalencia.

Aplicar los parches en un checkout limpio y recompilar los componentes afectados. FSMState.h afecta g1_ctrl; main.cc afecta el simulador. Ver [mjlab](06-unitree-rl-mjlab.md) para iniciar ambos procesos y usar las teclas. Este flujo usa domain 0 / lo y banda deshabilitada en la config local.

El README de instalación oficial también describe Conda/Python 3.11 y pip install -e . para el paquete Python de entrenamiento. El despliegue C++ anterior no requiere activar ese entorno para ejecutar sus dos binarios. Se encontró Miniconda y un entorno unitree-rl; no confundir ese nombre con el venv ~/unitree-rl-env. No se ensayó entrenamiento.

## 10. Comprobar cada capa antes de seguir

| Capa | Comprobación | Qué acredita |
|---|---|---|
| Windows/WSL | wsl --list --verbose | Distribución correcta y WSL2 |
| Gráficos | Viewer abre desde Ubuntu | Sesión gráfica funcional |
| SDK Python | Import unitree_sdk2py | Paquete accesible en ese venv |
| DDS | LowState llega en domain correcto | Comunicación de ese flujo |
| RL gym | Import legged_gym con PYTHONPATH | Resolución del módulo |
| C++ | ldd de los dos binarios | Bibliotecas resueltas, sin not found |
| FSM | Registros de transición | Cambio efectivo de estado |

Ejemplo sin ejecutar simulación:

```bash
ldd ~/unitree_rl_mjlab/simulate/build/unitree_mujoco
ldd ~/unitree_rl_mjlab/deploy/robots/g1/build/g1_ctrl
```

Ver [troubleshooting](../troubleshooting/README.md) y [validación](validation.md). Esta ampliación inspeccionó una instalación existente; no reinstaló WSL, paquetes, SDK ni entornos, ni repitió las pruebas dinámicas.
## Prueba gráfica que también aparece en el historial

El historial conserva sudo apt install -y x11-apps. Se puede usar como comprobación independiente de MuJoCo:

```bash
sudo apt install -y x11-apps
xeyes
```

La ventana prueba conectividad gráfica X11; no prueba aceleración OpenGL, DDS ni equilibrio. No se recuperó una salida de esa prueba, así que no se afirma un resultado histórico concreto.

## Entorno Conda adicional

Se recuperó conda create -n unitree-rl python=3.11 -y y posterior pip install -e . desde el checkout mjlab. En una instalación nueva, con Miniconda ya instalado e inicializado, ese flujo opcional es:

```bash
conda create -n unitree-rl python=3.11
conda activate unitree-rl
cd ~/unitree_rl_mjlab
python -m pip install -e .
```

Este paso instala el paquete Python y sus dependencias de entrenamiento; no es necesario para lanzar los binarios C++ del despliegue. No ejecutarlo para sustituir los dos venvs recuperados. Las versiones del Conda actual están en 02-environment.md; su instalación no demuestra entrenamiento propio.
