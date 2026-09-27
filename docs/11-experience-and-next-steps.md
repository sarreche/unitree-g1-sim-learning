# Experiencia, decisiones y posibles aplicaciones

## Qué se pudo recuperar de unitreerobotics

La lectura del chat proporcionó sus últimos cinco intercambios: explicación de equilibrio, propuestas de aplicaciones, decisión de detener la expansión del stack NVIDIA, propuesta de verificar GPU y salida de nvidia-smi de Windows. La herramienta informó hasMore=false y no entregó cursor a los mensajes anteriores. El intento de abrir el chat completo con el navegador falló por un problema del runtime. Por tanto, no se afirma haber revisado todo el historial ni reconstruido cada incidencia de instalación.

Para completar la experiencia se contrastaron esos intercambios con comandos pertinentes de .bash_history, READMEs locales, CMakeCache, install_manifest, ldd y paquetes instalados. Solo se recuperaron comandos relacionados con el laboratorio; no se publica el historial completo. Un comando presente en history acredita que fue escrito, no que terminó exitosamente. Los artefactos de instalación y binarios aportan evidencia adicional.

## Cambió el nivel del problema

El interés por aplicaciones como patrullaje llevó a descubrir una separación importante: enviar mensajes compatibles con el SDK no aporta automáticamente los servicios de locomoción de alto nivel del G1 físico. unitree_mujoco anuncia soporte low-level; el bridge implementa mensajes y dinámica, no todos los servicios internos del robot.

Así, mantener una postura en MuJoCo terminó requiriendo comprender control dinámico, sensores y contactos. El ejemplo conceptual Move del chat no debe entenderse como una API de alto nivel ya disponible y probada en este simulador. Esa integración no se implementó.

FixStand fija o interpola objetivos articulares. El equilibrio necesita reaccionar al estado y perturbaciones continuamente; una pose plausible no demuestra un controlador estable. El siguiente trabajo con policies oficiales en unitreerobotics2 aportó otra forma de abordar esa dificultad, sin entrenar una red propia.

## El desvío hacia Isaac se detuvo

El chat consideró Isaac Sim, Isaac Lab y unitree_sim_isaaclab para aplicaciones, sensores y whole-body, y discutió compatibilidad de RTX 50 y límites de 8 GB de VRAM. Después el usuario decidió no seguir con esa instalación. No se encontró evidencia en los intercambios accesibles de una instalación funcional de ese stack, y no se presenta como resultado del laboratorio.

Las recomendaciones de versión y compatibilidad hechas allí fueron propuestas históricas, no una matriz vigente validada aquí. No se convierten en instrucciones de instalación en esta documentación. El dato comprobado fue la GPU/driver en Windows y, posteriormente, su visibilidad en WSL.

## Ideas propuestas, todavía no desarrolladas

| Idea del chat | Qué permitiría aprender | Estado |
|---|---|---|
| Monitor de articulaciones e IMU | Lectura e interpretación de LowState | Hay lectura en scripts; no un monitor completo separado |
| Secuencias de brazos/HOME | Coordinación articular | Propuesta, sin implementación recuperada |
| STANDING / TILTED / FALLEN | Clasificación orientativa desde IMU | Propuesta; no se definieron ni validaron umbrales |
| API propia G1Robot | Separar aplicación y backend | Propuesta; nombres del chat son pseudocódigo |
| FSM IDLE/PATROL/OBSERVE/ALERT/RETURN | Lógica de aplicación | Propuesta, distinta de la FSM de control mjlab |
| Watchdog y estado SAFE | Gestión de pérdida de telemetría | Propuesta; scripts actuales no lo implementan |
| Mocks de locomoción/cámara/audio | Desarrollo sin hardware | Propuesta; no equivale a simular balance real |

La orientación sugerida fue priorizar componentes reutilizables de aplicación sobre seguir ampliando el ecosistema de simulación. Una API con backends y mocks puede aislar dependencias, pero pasar de simulación a G1 físico requiere implementar y verificar cada servicio disponible en el modelo/firmware; no basta cambiar la interfaz de red.

No se añadieron estas funcionalidades durante la documentación. Los próximos pasos quedan como posibilidades de aprendizaje, separados de los experimentos terminados.

## Orden de instalación y recorrido pedagógico

El historial recuperado contiene clonación/instalación de mjlab y SDK C++ antes de las pruebas finales de stand/balance y antes del venv RL gym. La progresión de tres stacks del README organiza lo aprendido; no pretende reproducir el orden literal de cada instalación o sesión.

Miniconda y unitree-rl sí están instalados, con mjlab y unitree_rl_mjlab. Esto debe distinguirse de Isaac Sim/Isaac Lab, cuya instalación no se acredita. Instalar un paquete de entrenamiento tampoco prueba que se haya entrenado una policy propia.
