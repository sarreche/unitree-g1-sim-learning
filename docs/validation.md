# Validación de entrega

Fecha: 2026-09-27.

- Repos, commits y diferencias inspeccionados sin modificarlos.
- Scripts compilados para comprobar sintaxis, sin lanzar publishers DDS ni viewer.
- Parches comprobados en modo --reverse --check contra los cambios existentes, sin aplicarlos.
- Inventarios de paquetes, GPU y estructura del npz obtenidos de la máquina.
- No se ejecutó entrenamiento ni una nueva sesión de locomoción/baile.
- No se validó instalación desde cero ni despliegue físico.
- El posible segfault y la repetición de transiciones siguen sin diagnóstico confirmado.

La limpieza mantiene las fórmulas y configuración recuperadas. Sintaxis correcta y parches aplicables no prueban estabilidad dinámica.

## Comprobaciones automáticas

- deploy_mujoco_keyboard.py: syntax OK
- g1_balance_test.py: syntax OK
- g1_stand_test.py: syntax OK
- unitree-mujoco-simulation-config.patch: reverse apply check OK against current local modifications
- sdk2-simulation-example.patch: reverse apply check OK against current local modifications
- rl-gym-runtime-config.patch: reverse apply check OK against current local modifications
- rl_mjlab-keyboard-transitions.patch: reverse apply check OK against current local modifications
- rl-mjlab-simulator-config.patch: reverse apply check OK against current local modifications
- rl-mjlab-home-keyframe.patch: reverse apply check OK against current local modifications

## Comprobación final

- Imports de ambos controladores comprobados en unitree-env, sin iniciar canales DDS.
- CLI --help del deploy comprobada en unitree-rl-env con PYTHONPATH externo.
- YAML verificado: 47 observaciones y vectores articulares de 12 elementos.
- El cuerpo efectivo original de LowCmdWrite coincide por AST con el recuperado, antes de añadir docstrings.
- Enlaces internos comprobados; no hay policies ni binarios copiados.
- Procedencia y hashes de scripts originales/entregados en script-provenance.json.
