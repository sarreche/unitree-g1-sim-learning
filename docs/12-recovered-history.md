# Cronología recuperada y correcciones del relato

Fuente principal: [unitreerobotics, conversación pública](https://chatgpt.com/share/6ab97458-3858-83e9-8b87-6f4cbc25416a). Se contrastó con los scripts y repos existentes. No se incorporan datos comerciales o personales ajenos al objetivo técnico del laboratorio.

## 1. Motivación y elección del stack

El objetivo era prepararse para desarrollar aplicaciones sobre un G1 EDU, con interés en patrullaje y otras skills. Se eligió empezar con SDK2 Python para reducir capas de integración. ROS2 se discutió como alternativa/ecosistema, no se instaló ni se demostró necesario para estos experimentos. Mac y VPS fueron opciones consideradas, no plataformas probadas.

El G1 EDU era el hardware objetivo; el resultado documentado es simulación de un modelo G1 de 29 joints. No se acredita compra, acceso a robot físico o integración de manos/cámaras/audio.

## 2. Primer equipo: Windows 10

El relato describió Windows 10 Pro 22H2, build 19045.2486, un i7-8700 y placa ASUS PRIME H310M-E. Muchas comprobaciones se hicieron mediante capturas que aquí no se reexaminaron.

Se habilitaron componentes de WSL; apareció 0x8024001e y luego faltaba el kernel. wsl --update permitió continuar. La virtualización estaba deshabilitada y se habilitó Intel VMX. Ubuntu 22.04 y el SDK Python se instalaron; un error de permisos globales de pip llevó a usar venv. Un intento de clonación con http falló en el puerto 80; se repitió con https.

MuJoCo/SDK importaban correctamente, pero xeyes y el viewer no se mostraban. DISPLAY=:0, WAYLAND_DISPLAY=wayland-0 y /mnt/wslg existían: esas señales no bastaban para demostrar que una ventana podía presentarse. El relato del log incluyó rdp_peer is not initialized y errores de RemoteApp.

Se investigó Windows Update: servicio wuauserv deshabilitado, error 1058 y políticas DisableWindowsUpdateAccess/DisableOSUpgrade. Se probaron cambios de servicio y registro, pero el servicio volvió a quedar deshabilitado; no se identificó concluyentemente qué lo reescribía ni se resolvió el problema gráfico. No se incluyen esos cambios como receta de instalación ni se afirma que Windows Update fuera la causa demostrada de WSLg.

Se revisaron TPM 2.0, UEFI y Secure Boot para una posible actualización a Windows 11. El usuario confirmó haber activado Secure Boot, pero no confirmó una actualización de ese equipo. Después indicó que empezó en otra máquina con Windows 11. Por tanto, no documentar una migración in-place exitosa como resultado del proyecto.

## 3. Segunda PC: Windows 11 y base funcional

Se corrigió la distribución predeterminada de docker-desktop a Ubuntu, se detectó Ubuntu 26.04.1 y se instaló Ubuntu-22.04 sin borrar la otra distribución. La nueva selección confirmó Ubuntu 22.04.5.

Se instalaron herramientas base, clonaron los repos Python y se creó unitree-env. El log confirma SDK Python 1.0.1 y CycloneDDS 0.10.2; después MuJoCo 3.14.0. xeyes sí abrió en Windows 11, confirmado directamente por el usuario. Se configuró G1 y apareció el viewer.

Esto resolvió el obstáculo práctico usando otra PC. No prueba que Windows 10 en general sea incapaz de ejecutar WSLg ni cuál era la causa exacta del primer equipo.

## 4. Lectura de estado: una ventana no basta

Primero se inicializó ChannelFactoryInitialize(1, "lo") y se leyó unitree_hg.LowState por rt/lowstate en el intérprete Python. El warning de multicast no impidió inicializar DDS. Se creó read_g1.py con callback, inicialmente mirando motor 0 y después todos los slots una vez por segundo.

Los valores persistían en cero. La hipótesis inicial de pausa fue corregida: Run/Pause no se manejaban igual en el viewer Python pasivo. La causa concreta recuperada fue USE_JOYSTICK=1 sin gamepad, que cortaba el thread de física antes de mj_step. Al deshabilitar joystick hubo variación en q/dq y el cuerpo cayó por gravedad.

Los motores efectivos eran 0–28; el mensaje también mostraba slots reservados 29–34. El bridge local no actualiza tick ni rpy, así que sus ceros no prueban ausencia de mensajes ni orientación plana. El monitor histórico imprime rpy; ese campo debe interpretarse con esta limitación.

## 5. Primera orden: codo derecho

move_elbow.py tomó la posición del motor 25, pidió +0.30 rad durante 3 s, con kp=20, kd=1, y publicó LowCmd con CRC a intervalos nominales de 2 ms. El usuario reportó un movimiento breve. Las ejecuciones sucesivas partían de posiciones diferentes: el objetivo era relativo a la lectura de cada ejecución.

Fue una prueba de comunicación bidireccional con robot simulado en el suelo, no una skill coordinada ni una trayectoria validada. El prototipo no limita target_q al rango del joint y no implementa retorno, watchdog ni parada de torque al finalizar. No repetirlo como demostración de postura estable.

## 6. La demo de postura cero falló

stand_g1.py habilitó 29 motores con q=0 y ganancias del ejemplo oficial. Se probó arrancar el script antes del simulador para evitar que el cuerpo cayera antes de recibir comandos. Aun así no sostuvo el equilibrio: estiró articulaciones en el suelo o cayó manteniendo aproximadamente su pose.

No es el mismo script que g1_stand_test.py de la segunda conversación: este último fija una postura flexionada de piernas. Ambos aportaron la diferencia entre pose y balance, pero ninguno fue un stand_up/recovery desde el piso validado.

## 7. Mjlab: instalación y primeras teclas

Se instaló Miniconda, se superó el bloqueo de términos de canales y se creó unitree-rl con Python 3.11. pip install -e . de mjlab terminó exitosamente; no se confunde con el fallo por isaacgym de RL gym posterior.

El controlador C++ necesitó SDK2 C++ en /usr/local. El simulador necesitó libglfw3-dev. Se resolvió un crash de joystick desactivándolo. Un gamepad USB conectado al host no apareció como /dev/input en WSL; no se configuró passthrough.

State_RLBase.cpp ya registraba una observación de velocidad por teclado, pero las transiciones de estado usaban gamepad. Se añadieron 1 para Passive→FixStand y 2 para FixStand→Velocity. El log confirmó la transición con 1. En unitreerobotics2 se agregaron 5 y 3 para Mimic. Los cuatro bloques son locales respecto del commit registrado.

## 8. Pause, home y locomoción inicialmente fallida

Se intentó pausar el simulador C++, pasar a FixStand/Velocity y después reanudar. Los logs confirmaron transiciones, pero el usuario relató caída y movimientos descontrolados en el suelo. Tener Velocity activo no demostró locomoción estable en esas pruebas.

Se encontró que la escena no aplicaba una postura home al cargar. Se agregó el keyframe de 7 valores de floating base más 29 joints, y mj_resetDataKeyframe al crear mjData. El cuerpo comenzó con rodillas flexionadas pero igualmente cayó hacia atrás. Esto confirmó el efecto del cambio inicial; no resolvió el balance.

Se revisaron joint_ids_map, ganancias, postura nominal y conversión de IMU. El chat planteó posibles problemas de observaciones/inicialización, pero no aisló la causa dinámica. Evitar repetir diagnósticos categóricos del asistente como fallos demostrados de la policy.

El historial termina dejando ese diagnóstico abierto y considerando otros enfoques. Los resultados posteriores de locomoción y baile se documentan desde unitreerobotics2. No reescribir los ensayos iniciales fallidos como éxitos retrospectivos.

## 9. Correcciones útiles para quien reproduce

- Control en el viewer no significa necesariamente q objetivo en radianes. El XML G1 usa actuadores motor; sus controles son entradas al actuador y el bridge escribe torques. El intento de introducir -1.5 como postura del hombro en la GUI no obtuvo el resultado esperado. No entregar esos valores del chat como receta validada.
- Una biblioteca Python no instala necesariamente headers C++; SDK Python y SDK C++, y glfw pip y libglfw3-dev, son casos distintos.
- Un campo de mensaje a cero puede estar sin implementar. Para comprobar física y DDS, mirar varios joints, IMU implementada y estado del thread.
- Python frente a C++ es una elección de implementación. El cambio importante fue pasar de comandos articulares a un controlador con policy, no una supuesta capacidad de balance inherente al lenguaje.
- El LocoClient para el robot físico no estaba implementado como servicio por el bridge usado. FixStand no equivale a levantarse del suelo.

Los tres prototipos iniciales se preservan en [scripts/historical](../scripts/historical/README.md) como evidencia del aprendizaje, con sus limitaciones y sin cambios de comportamiento.
