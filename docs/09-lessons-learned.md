# Aprendizajes

1. Recibir LowState y mover articulaciones confirma comunicación; no confirma equilibrio.
2. Postura y balance son problemas distintos: el cuerpo puede caer manteniendo ángulos.
3. Los campos de un mensaje no necesariamente están todos poblados. rpy en cero no contradice un quaternion inclinado.
4. El domain DDS debe coincidir por flujo. Low-level usa 1; mjlab local usa 0; RL gym directo no necesita DDS.
5. La banda es una ayuda de experimentación y modifica las condiciones dinámicas.
6. Un PD de tobillos muestra principios de control, pero saturar no resuelve el balance de cuerpo completo.
7. La policy recibe comandos de alto nivel y decide acciones: el teclado cambia comandos, no aprendizaje.
8. Una FSM permite alternar controladores con objetivos diferentes.
9. Motion reference y policy son artefactos distintos. El baile requiere ambos y sus parámetros compatibles.
10. Reproducibilidad requiere commits, cambios locales, entorno y rutas; conservar solo comandos de terminal no alcanza.

El próximo paso quedó intencionalmente abierto: estudiar observaciones y referencia con más detalle. No se agregaron nuevos experimentos durante la organización del proyecto.

## Lo que aportó el primer chat

- Una infraestructura que permite leer estado y enviar comandos ya sirve para aprender, aunque no resuelva locomoción.
- Separar lógica de aplicación de control dinámico ayuda a identificar qué necesita realmente un proyecto de patrullaje.
- Los mocks pueden desarrollar comportamientos; no acreditan física, sensores reales ni equilibrio.
- La GPU y su VRAM orientan decisiones de stack, pero una propuesta compatible no demuestra una instalación funcional.
- Detener una ampliación del entorno también fue una decisión explícita: Isaac quedó como alternativa considerada, no logro del proyecto.

Ver [experiencia y próximos pasos](11-experience-and-next-steps.md) y [cronología recuperada](12-recovered-history.md) para distinguir propuestas, resultados y límites de las fuentes.

## Lecciones recuperadas del historial público

- Los errores de presentación gráfica del primer equipo se separan de SDK/DDS: xeyes sirvió como prueba mínima y funcionó en la nueva PC.
- USE_JOYSTICK puede impedir que la física arranque aun con viewer abierto; mirar el estado del proceso antes de atribuir ceros a sensores.
- Las primeras órdenes al codo fueron exitosas como prueba de comunicación, pero no establecieron una skill con límites y trayectoria.
- Activar teclas de una FSM y activar una observación de velocidad por teclado son cambios diferentes.
- Los ensayos fallidos, hipótesis corregidas y cambios de equipo también forman parte de la experiencia: no deben desaparecer de una documentación orientada a reproducirla.
