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
