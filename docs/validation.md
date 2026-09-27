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

## Ampliación del historial e instalación

- Rama de trabajo: docs/windows11-setup-and-experience; main no se editó.
- Lectura de los cinco intercambios disponibles de unitreerobotics. El acceso al historial anterior no estuvo disponible; no se afirma revisión completa.
- Se inspeccionaron comandos pertinentes del historial Linux, instrucciones locales, caches CMake, manifest de instalación y ldd de ambos binarios.
- Confirmado SDK C++ en /usr/local, MuJoCo C++ 3.3.6, ONNX Runtime 1.22.0 y entorno Conda adicional.
- Se verificaron fuentes oficiales de Microsoft y NVIDIA para los pasos Windows/WSL y la separación del driver host.
- Comandos de instalación incluidos como documentación: no se ejecutaron instalaciones, nuevas compilaciones ni cambios a los repos oficiales.
- No se probó una instalación limpia, entrenamiento ni hardware físico.

## Recuperación mediante enlace público

El límite de acceso anterior quedó superado para el texto publicado mediante el enlace público del usuario: docs/shared-conversation-source.json registra la fuente y el método. Se revisaron instalación y experimentos del primer chat; las capturas originales no se reexaminaron y las salidas redactadas no se reconstruyeron.

Se contrastaron joystick Python, campos tick/rpy, actuadores motor y selección de observaciones por teclado con el código local. Se recuperaron read_g1.py, move_elbow.py y stand_g1.py del home Linux: solo se añadieron cabeceras y se verificó su sintaxis, sin importarlos, publicar DDS ni ejecutar física. Procedencia y hashes en script-provenance.json.

Las nuevas comprobaciones distinguen incidencias históricas de recomendaciones de reproducción. No se cambiaron repos oficiales, dependencias, servicios Windows, BIOS, políticas o términos de Conda; no se ejecutaron nuevas sesiones de simulación.
