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
