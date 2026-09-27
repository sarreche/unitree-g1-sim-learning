# Mjlab: simulador C++, FSM y ONNX

El proyecto oficial ofrece entrenamiento con mjlab/MuJoCo y despliegue. En este trabajo se ejecutó el despliegue existente, no entrenamiento. Dos procesos: simulate/build/unitree_mujoco y deploy/robots/g1/build/g1_ctrl. El controlador contiene FSM, observaciones y carga ONNX; el simulador usa su propio bridge. La configuración local usa domain_id=0, interface=lo y use_joystick=0.

## Ejecutar la instalación existente

Terminal 1:

```bash
cd ~/unitree_rl_mjlab
./simulate/build/unitree_mujoco
```

Terminal 2:

```bash
cd ~/unitree_rl_mjlab/deploy/robots/g1/build
./g1_ctrl --network=lo
```

Para compilar una instalación nueva, seguir doc/setup_en.md del commit registrado. Después de modificar FSMState.h, recompilar el controlador:

```bash
cd ~/unitree_rl_mjlab/deploy/robots/g1/build
cmake ..
make -j"$(nproc)"
```

Si cambia simulate/src/main.cc, recompilar también el simulador siguiendo su configuración oficial. No basta recompilar g1_ctrl.

## Estados y entradas

| Transición | Gamepad en config.yaml | Teclado local |
|---|---|---|
| Passive → FixStand | LT + up.on_pressed | 1 |
| FixStand → Velocity | RT + A.on_pressed | 2 |
| Velocity → Mimic_Dance1_subject2 | RB + A.on_pressed | 5 |
| Mimic → Velocity | RT + A.on_pressed | 3 |
| FixStand/Velocity/Mimic → Passive | LT + B.on_pressed | No agregado |

Passive usa amortiguación; FixStand interpola hacia postura; Velocity usa locomoción; Mimic carga la referencia y policy del baile. El timeout de estado registra un retorno a Passive. No confundir IDs de estado con teclas.

main.cpp ya inicializaba Keyboard; keyboard.h lee stdin del proceso. Durante el chat se encontraron inicialmente 1 y 2, y después se agregaron 5 y 3. La comparación contra HEAD local muestra que los cuatro bloques son modificaciones respecto de ese commit: el parche incluye los cuatro, sin afirmar que 1 y 2 fueran oficiales en esa revisión.

Pulsar las teclas con foco en la terminal de g1_ctrl, no en MuJoCo. El relato registró cambios rápidos repetidos entre Velocity y Mimic. Usar pulsaciones breves; auto-repeat es una hipótesis del chat, no una causa demostrada por inspección.

## Otros cambios recuperados

simulate/config.yaml deshabilita joystick. scene_g1.xml agrega keyframe home con altura 0.793, postura de piernas y brazos de FixStand. main.cc aplica ese keyframe al cargar el modelo. Backspace sigue usando mj_resetData, de modo que no aplica automáticamente home. La copia .bak se excluyó.

Estos cambios están separados en parches para no perder trabajo que no figuraba en la propuesta inicial. Ninguno se aplicó a los repos originales durante la documentación.

## Dependencias de despliegue verificadas

El build local usa SDK C++ en /usr/local y bibliotecas ddsc/ddscxx; el CMake del simulador resuelve unitree_sdk2_DIR=/usr/local/lib/cmake/unitree_sdk2. MuJoCo C++ es 3.3.6 dentro de simulate/mujoco, que está incluido en esta revisión del checkout. El controlador usa ONNX Runtime 1.22.0 de deploy/thirdparty. No son las versiones pip de los venvs.

La config actual tiene enable_elastic_band=0. Las teclas de banda no tendrán efecto allí hasta habilitarla. El build del controlador necesita Boost program_options, yaml-cpp, fmt, Eigen y ZLIB/cnpy; el simulador necesita además GLFW. La [guía Windows/WSL](10-windows11-wsl-setup.md) incluye el orden de instalación y compilación.

## Teclas de velocidad: soporte registrado, configuración distinta

State_RLBase.cpp registra keyboard_velocity_commands y comenta que hay que sustituir velocity_commands por ese nombre en el deploy.yaml para seleccionarlo. El deploy.yaml local inspeccionado conserva velocity_commands; agregar teclas de FSM no activa automáticamente esta observación.

| Tecla en el ejemplo mjlab | Vector definido [vx, vy, yaw_rate] |
|---|---|
| W | [1,0,0] |
| S | [-1,0,0] |
| A | [0,1,0] |
| D | [0,-1,0] |
| Q | [0,0,1] |
| E | [0,0,-1] |

Son los valores escritos en ese ejemplo, no recomendaciones ni una prueba de cumplimiento de los rangos del deploy.yaml. La función retorna cero si la tecla leída no coincide. El mapeo difiere del script RL gym entregado, donde A/D giran y Q/E mueven lateralmente. No se cambió deploy.yaml ni se añadió un experimento nuevo durante la documentación.

Las primeras pruebas de mjlab relatadas en unitreerobotics incluyeron caídas al reanudar desde Pause, incluso con Velocity activa y después de agregar home. Su causa quedó abierta. Los cambios y resultados de la segunda charla deben interpretarse en su propia sesión.
