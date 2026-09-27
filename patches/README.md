# Cambios recuperados

Los parches son git diff del checkout local respecto del commit en docs/upstream-revisions.json. No se aplicaron durante esta preparación. Contienen el contexto mínimo de upstream necesario para representar el cambio.

| Parche | Repo destino | Efecto |
|---|---|---|
| unitree-mujoco-simulation-config.patch | unitree_mujoco | G1, sin gamepad, banda activada |
| sdk2-simulation-example.patch | unitree_sdk2_python | Omite MotionSwitcher y usa domain 1 / lo |
| rl-gym-runtime-config.patch | unitree_rl_gym | Quietud inicial y duración 3600 s |
| rl_mjlab-keyboard-transitions.patch | unitree_rl_mjlab | Teclas 1,2,5,3 en FSM |
| rl-mjlab-simulator-config.patch | unitree_rl_mjlab | Deshabilita joystick |
| rl-mjlab-home-keyframe.patch | unitree_rl_mjlab | Keyframe home y aplicación al cargar modelo |

El parche SDK conserva incluso la expresión suelta MotionSwitcherClient al final del archivo histórico: no es necesaria ni recomendada. Los scripts limpios no la incluyen. El parche registra evidencia, no reemplaza los scripts entregados.

Para una revisión nueva sin cambios, desde el repo destino:

```bash
export LAB=/mnt/c/Users/Usuario/Documents/Code-Projects/unitree-g1-sim-learning
git apply --check "$LAB/patches/rl_mjlab-keyboard-transitions.patch"
git apply "$LAB/patches/rl_mjlab-keyboard-transitions.patch"
```

Cambiar el nombre del parche según la tabla. Usar commits compatibles. En los repos actuales los cambios ya existen; no volver a aplicarlos. git apply --reverse --check permite comprobar si un parche corresponde al estado actual sin revertirlo. Recompilar componentes C++ afectados; ver docs/06-unitree-rl-mjlab.md.

Los avisos de origen se encuentran en THIRD_PARTY_NOTICES.md y licenses/. No se copiaron repos completos ni binarios.
