# Alcance de sim-to-real

Este laboratorio solo documenta simulación. No hay despliegue físico ni validación de seguridad, balance o tolerancia a fallos sobre hardware.

El bridge simplifica el sistema: el ejemplo MotionSwitcherClient no respondió como en el robot; se omitió para esta simulación. La banda aporta fuerzas externas ausentes en uso normal. Cambian latencias, contactos, fricción, calibración, límites de torque y condiciones iniciales. Una policy que camina en este modelo no acredita resultados en otra configuración.

Los scripts publican comandos low-level y habilitan 29 motores, con brazos y cintura a cero. No implementan una secuencia física de arranque, liberación, parada ni recuperación ante caída. Domain 1 y lo son parte del aislamiento local de la simulación; no modificar la interfaz para enviar estos experimentos a hardware.

Un proyecto de robot real requeriría validar modelo y firmware, convenciones de joints/IMU, límites, servicios de modo, watchdogs y procedimientos oficiales bajo supervisión adecuada. Eso queda fuera del trabajo realizado.

## Interfaz de aplicación y servicios

El chat propuso una capa G1Robot y mocks para patrullaje, sensores y audio. Esos nombres son pseudocódigo de una arquitectura futura, no métodos implementados aquí. Compatibilidad de mensajes DDS no garantiza que el simulador exponga LocoClient u otros servicios del firmware real.

Cambiar lo por una interfaz física no transforma este laboratorio en una aplicación lista para hardware. La implementación y validación de cada backend debe comprobar servicios, modos y semántica del dispositivo. Los umbrales de caída y watchdogs propuestos no están implementados en los scripts entregados.
