# Problemas encontrados

| Stack | Síntoma | Causa o hipótesis | Solución / estado |
|---|---|---|---|
| SDK / DDS | CheckMode devuelve None | Servicio de motion switcher no responde como espera el ejemplo en simulación | Omitir el bloque solo en el flujo simulado; no indexar None. |
| Low-level | No llegan LowState o comandos | Domain distinto entre procesos | Usar domain 1 y lo en simulador y script; mjlab local usa 0. |
| DDS | Warning sobre multicast en lo | Loopback puede carecer de flag multicast; el warning por sí solo no prueba fallo | Comprobar mensajes reales, interfaz y configuración CycloneDDS. No se conserva una configuración XML validada adicional. |
| IMU | rpy permanece en cero | El bridge inspeccionado no lo rellena | Calcular Euler desde quaternion [w,x,y,z]; usar gyroscope para tasas. |
| Python | TabError | Mezcla de tabs y espacios en código editado | Normalizar indentación; scripts entregados se verifican con ast/compile. |
| Low-level | Robot acostado, joints se mueven | La comunicación funciona pero no hay balance global | Separar prueba de joints de equilibrio; usar banda para inspección y no atribuirle estabilidad al PD. |
| Simuladores | La banda sostiene demasiado o no responde | Longitud/enable y foco de ventana | 7 acorta, 8 alarga, 9 alterna; comprobar enable_elastic_band y dar foco a MuJoCo. |
| Balance | correction queda en el límite | La corrección requerida supera 0.08/0.12 rad o dinámica/signos no estabilizan | Registrar pitch/rate/correction; se pasó a policy oficial. No hay ajuste manual validado. |
| RL gym | ModuleNotFoundError: legged_gym | Repo fuera de sys.path | Exportar PYTHONPATH al repo antes de ejecutar. |
| RL gym | pip install -e . pide isaacgym | Dependencias del entrenamiento | Para este deploy, usar entorno de inferencia y PYTHONPATH; no instalar todo entrenamiento. |
| RL gym | Warning al cargar .pt | Texto exacto del warning no conservado | Usar torch.jit.load para el TorchScript oficial. Capturar warning completo si reaparece. |
| RL gym | Termina al minuto | simulation_duration original 60.0 | Config local y entregada usan 3600.0 segundos de reloj. |
| Viewer | Posible segmentation fault al cerrar | Causa no confirmada | Guardar log y versiones; restauración de terminal mejorada no garantiza resolver el fallo nativo. |
| Mjlab | Cambiar header no cambia comportamiento | Binario compilado anterior | Recompilar g1_ctrl; si cambia main.cc del simulador, recompilar también ese binario. |
| Teclado | Teclas no producen transiciones | stdin de otra terminal o foco en viewer | En mjlab enfocar g1_ctrl; en RL gym enfocar terminal Python. |
| Gamepad | No gamepad detected | Joystick activado sin dispositivo | USE_JOYSTICK=0 o use_joystick=0 según stack. |
| Mjlab | No entra a baile con teclado | Falta transición en FSM | Aplicar parche y recompilar; 5 desde Velocity, 3 para volver. |
| Mjlab | Transiciones rápidas repetidas | Posible repetición de teclas, no confirmada | Pulsaciones breves y revisar registros; no se implementó debounce. |
| Mjlab | Backspace no vuelve a home | Callback usa mj_resetData | El parche home actúa al cargar el modelo; reiniciar simulador si se busca esa condición inicial. |

## Windows/WSL e instalación C++

| Stack | Síntoma | Comprobación y respuesta |
|---|---|---|
| Windows/WSL | Entorno o repos no encontrados | Abrir Ubuntu-22.04 explícitamente; Ubuntu y Ubuntu-22.04 tienen homes distintos. |
| WSLg | No abre el viewer | Comprobar WSL2, /mnt/wslg y DISPLAY/Wayland; actualizar WSL si falta soporte gráfico. No se conserva un fallo gráfico histórico concreto. |
| GPU | nvidia-smi funciona solo en Windows | Comprobar también dentro de WSL; seguir la guía NVIDIA de WSL, sin instalar driver Linux. |
| SDK Python | Could not locate cyclonedds | Alternativa oficial: compilar CycloneDDS y definir CYCLONEDDS_HOME. No se demuestra que fuera necesaria en esta máquina. |
| CMake | No encuentra unitree_sdk2 | Verificar instalación C++ y CMAKE_PREFIX_PATH; la real está en /usr/local, no /opt/unitree_robotics. |
| CMake/linker | Falta GLFW, yaml-cpp, Boost, fmt o ZLIB | Instalar sus paquetes -dev; consultar la lista consolidada de la guía. |
| Loader C++ | Biblioteca .so no encontrada | Revisar ldd, prefijo del SDK y bibliotecas vendorizadas. No mezclar pip mujoco con la biblioteca C++. |
| Entornos | Activación no cambia el binario | unitree-rl de Conda y unitree-rl-env de venv son distintos; g1_ctrl es un ejecutable C++ compilado. |

Estas filas incorporan comprobaciones para reproducir el entorno. No todas representan errores históricos confirmados. Ver [instalación Windows/WSL](../docs/10-windows11-wsl-setup.md).

## Incidencias confirmadas o relatadas en el historial público

| Incidencia | Evidencia / respuesta aplicada | Alcance |
|---|---|---|
| WSL sin kernel o virtualización | En el primer equipo se actualizó WSL y habilitó Intel VMX | Relato de capturas; no se reconfiguró BIOS en este trabajo |
| xeyes no abre y RemoteApp falla | Log relató rdp_peer is not initialized; se cambió de PC | Causa raíz del primer equipo no demostrada |
| Windows Update error 1058 | Se investigaron servicio y políticas; el bloqueo persistió | No es una receta validada para arreglar WSLg |
| pip Permission denied global | Crear/activar unitree-env y repetir instalación | No fue un fallo de CycloneDDS |
| docker-desktop predeterminado | Seleccionar Ubuntu-22.04 y verificar lsb_release | No borrar la distribución de Docker |
| LowState todo cero | Deshabilitar joystick en Python y reiniciar | Callback activo no acredita física en marcha |
| tick/rpy siempre cero | No se asignan en el bridge local | Mirar campos implementados |
| CondaToSNonInteractiveError seguido por EnvironmentNameNotFound | Revisar/aceptar canales elegidos y repetir creación | El entorno no existía después de fallar create |
| Falta go2/go2.h al compilar G1 | Instalar SDK2 C++ en /usr/local | Dependencia compartida, no robot mal seleccionado |
| Falta GLFW/glfw3.h y -lglfw | Instalar libglfw3-dev y repetir make | pip glfw no aporta los headers del sistema |
| Joystick open failed + segfault al arrancar C++ | use_joystick=0 evitó ese arranque fallido | Distinto del posible segfault al cerrar viewer |
| Gamepad host ausente en /dev/input | Se optó por teclas FSM | Passthrough USB no probado |
| 1/2 funcionan pero WASD no controla Velocity | La config usa velocity_commands, no keyboard_velocity_commands | No se activó ese cambio durante documentación |
| GUI Control no produce postura esperada | Revisar tipo de actuador motor y bridge de torques | No interpretar todo Control como posición |
| HOME correcto pero el cuerpo cae | Se confirmó postura inicial, no equilibrio | No atribuir causa definitiva a policy/observaciones |
