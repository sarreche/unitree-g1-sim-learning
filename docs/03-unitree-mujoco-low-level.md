# MuJoCo + SDK: articulaciones, DDS e IMU

Se usó simulate_python/unitree_mujoco.py con ROBOT="g1", escena ../unitree_robots/g1/scene.xml, domain 1 e interfaz lo. USE_JOYSTICK=0 y ENABLE_ELASTIC_BAND=True. El controlador crea mensajes unitree_hg LowCmd/LowState para el G1 y configura 29 motores. El bridge selecciona el tipo de mensaje según el modelo; comprobar los actuadores y sensores impresos al iniciar.

LowCmd llega por rt/lowcmd. El bridge calcula torque = tau + kp*(q_objetivo-q) + kd*(dq_objetivo-dq) y lo coloca en ctrl de MuJoCo. LowState publica q, dq, tau_est e IMU por rt/lowstate. El CRC se calcula antes de publicar el comando. No equivale a ejecutar los servicios internos de un robot físico.

lo es loopback: el tráfico permanece en la máquina Linux. Publisher y subscriber deben usar el mismo domain; aquí ChannelFactoryInitialize(1, "lo"). El mjlab de este laboratorio usa domain 0, de modo que no mezclar sus procesos con este controlador.

El ejemplo oficial llama MotionSwitcherClient y consulta CheckMode. En el simulador ese servicio no respondió como esperaba el ejemplo: result era None y result['name'] fallaba. Se omitió ese bloque para la simulación y se cambió domain 0 por 1. No interpretar esto como un cambio recomendado para un robot real.

## Ejecutar con repos ya configurados

Aplicar primero el parche de configuración si se usa un checkout nuevo; ver patches/README.md.

Terminal del simulador:

```bash
source ~/unitree-env/bin/activate
cd ~/unitree_mujoco/simulate_python
python unitree_mujoco.py
```

Otra terminal:

```bash
source ~/unitree-env/bin/activate
export LAB=/mnt/c/Users/Usuario/Documents/Code-Projects/unitree-g1-sim-learning
python "$LAB/scripts/g1_stand_test.py"
# En una ejecución separada:
python "$LAB/scripts/g1_balance_test.py"
```

Ejecutar un solo publisher de LowCmd. Los scripts esperan el primer estado antes de iniciar. Detener con Ctrl+C; esa salida no implementa una secuencia de apagado físico.

## Elastic band

La banda es una fuerza externa tipo resorte con amortiguación, aplicada al torso; puede sostener al robot y ocultar que el controlador no equilibra el cuerpo. En el código Python local: rigidez 200, amortiguación 100, punto [0,0,3], longitud inicial 0.

| Tecla en ventana MuJoCo | Operación comprobada en código |
|---|---|
| 7 | length -= 0.1: acorta y aumenta la tensión a igual distancia |
| 8 | length += 0.1: alarga y reduce la tensión a igual distancia |
| 9 | Alterna enable |

Las etiquetas informales subir/bajar no describen una posición absoluta. El efecto depende del estado del cuerpo y del resorte. En mjlab también hay flechas arriba/abajo. No se volvió a medir visualmente la respuesta durante esta documentación.

## IMU

PublishLowState rellena quaternion, gyroscope y accelerometer desde los sensores. No asigna rpy en ese método, lo que explica sus ceros en este bridge. No significa ausencia de inclinación. El quaternion se interpreta como [w,x,y,z].

```text
roll  = atan2(2*(w*x+y*z), 1-2*(x*x+y*y))
pitch = asin(clip(2*(w*y-z*x), -1, 1))
yaw   = atan2(2*(w*z+x*y), 1-2*(y*y+z*z))
```

Los ángulos salen en radianes; se convierten a grados solo para imprimir. gyroscope[1] se usó como velocidad de pitch, en rad/s, bajo la convención de ejes del modelo. El signo y el marco deben verificarse antes de extrapolar a otros modelos.

El movimiento de articulaciones y las lecturas reales de motor_state permitieron comprobar que llegaban comandos. Un robot acostado con joints moviéndose prueba comunicación y control articular, no equilibrio.

## Diferencia concreta con el README local

El readme.md oficial inspeccionado etiqueta 7 como bajar y 8 como levantar. El callback Python local hace length -= 0.1 con 7 y length += 0.1 con 8. En el resorte, a igual distancia, acortar aumenta la tensión y alargar la reduce. Se conserva la operación del código como referencia precisa y no se afirma una dirección absoluta del cuerpo en toda condición.

El README oficial de esta revisión declara soporte de desarrollo low-level. Publicar SportModeState en el simulador no demuestra disponibilidad de los servicios de locomoción high-level. Ver [experiencia y alcance](11-experience-and-next-steps.md).

## Primer monitor y fallo que mantuvo la física sin avanzar

El historial completo recuperó read_g1.py. La evolución fue Read() manual → callback de un motor → impresión de todos los slots una vez por segundo. Deshabilitar USE_JOYSTICK permitió que los estados variaran: SetupJoystick sin gamepad salía antes de iniciar el bucle físico. Recibir callbacks con ceros y ver una ventana no bastaba para comprobar dinámica.

tick tampoco se rellena en el bridge inspeccionado. No usarlo como prueba única de frescura. La primera orden real fue move_elbow.py sobre motor 25; ver [cronología](12-recovered-history.md). El experimento de sliders de hombro fue fallido: los actuadores motor del XML reciben señales de actuación, no un objetivo de posición equivalente a LowCmd.q.
