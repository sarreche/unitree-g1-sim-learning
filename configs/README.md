# Configuración recuperada

rl_gym_g1.yaml conserva la config local: simulation_duration=3600.0 y cmd_init=[0,0,0], con ganancias, escalas y dimensiones compatibles con motion.pt. No contiene pesos ni rutas privadas: LEGGED_GYM_ROOT_DIR lo resuelve legged_gym desde el repo externo.

Usar --config con una ruta absoluta al ejecutar el script entregado. No mezclar esta configuración de 12 acciones con el G1 de 29 joints de mjlab. Los cambios de otros stacks están en patches/.
