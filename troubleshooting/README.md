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
