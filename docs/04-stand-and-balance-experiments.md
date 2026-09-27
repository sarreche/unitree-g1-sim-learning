# Postura fija y balance P/PD

g1_stand_test.py se recuperó de example/g1/low_level. La postura de cada pierna, en orden hip pitch, hip roll, hip yaw, knee, ankle pitch, ankle roll, es [-0.1, 0, 0, 0.3, -0.2, 0] rad. Se fijan los primeros 12 objetivos; cintura y brazos tienen objetivo cero, pero los 29 motores quedan habilitados.

Ganancias articulares heredadas: por pierna Kp=[60,60,60,100,40,40], Kd=[1,1,1,2,1,1]; cintura Kp=[60,40,40], Kd=[1,1,1]; brazos Kp=40 y Kd=1. No confundirlas con las ganancias del lazo externo de balance.

Se comprobaron posiciones reales y movimiento, pero sin banda el cuerpo podía caer como un bloque conservando aproximadamente la postura. Controlar ángulos internos no garantiza que el centro de masa permanezca sobre la base de apoyo.

## Evolución de balance

El relato del experimento describe lectura de quaternion, cálculo de pitch y referencia cercana a 3.67° medida en esa postura. Se probó P con Kp=0.5, después Kp=1.0 y PD con Kd=0.08. La corrección máxima pasó de 0.08 a 0.12 rad. La versión local final conserva 1.0, 0.08 y 0.12.

La fórmula recuperada se conserva exactamente:

```text
error = radians(3.67) - pitch
correction = -(1.0 * error - 0.08 * gyroscope[1])
correction = clip(correction, -0.12, 0.12)
ankle_pitch_left  = -0.2 + correction
ankle_pitch_right = -0.2 + correction
```

El término derivativo entra con signo positivo al expandir esta expresión. No se corrigió ni se afirma que proporcione amortiguación estabilizante: el signo efectivo depende de la convención y la respuesta de la planta. Se preserva para documentar lo que se probó.

El controlador saturaba y la banda se liberaba progresivamente. La ankle strategy ilustra cómo cambiar tobillos afecta inclinación, pero faltan coordinación de caderas, contactos, estimación dinámica y tratamiento de caídas. Se decidió no seguir calibrando manualmente y pasar a policies oficiales.

## Limpieza de scripts

Se eliminaron imports duplicados, bloques comentados de MotionSwitcherClient, identificadores sin uso y una primera definición de LowCmdWrite que Python sobrescribía en stand. Se mantuvieron la postura, ganancias, corrección, domain, periodo y mensajes. Se expandieron tabs a espacios. No se añadió una nueva estrategia de balance ni se volvió a experimentar.

Los archivos son derivados de ejemplos oficiales, con modificaciones experimentales; no son creación íntegramente original. Ver avisos y licencias. No ejecutar en un robot físico.
