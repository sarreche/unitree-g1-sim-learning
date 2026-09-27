# Recorrido y alcance

El objetivo fue entender qué se controla en cada nivel. Primero se conectó el simulador al SDK, se comprobaron comandos y estado, y se construyó una postura fija. Después se usó orientación y velocidad angular para corregir ambos tobillos. La caída del cuerpo aunque las articulaciones mantuvieran sus ángulos mostró la diferencia entre postura y balance.

El segundo enfoque sustituyó el balance artesanal por una policy oficial de locomoción. Se probaron quietud, avance, lateral y giro, y se agregó teclado para cambiar el comando mientras la simulación seguía funcionando.

El tercer enfoque introdujo una FSM: Passive → FixStand → Velocity → Mimic_Dance1_subject2. Se agregaron accesos por teclado y se observó el baile y el regreso a locomoción.

Usar low-level cuando el objetivo sea estudiar sensores, mensajes y control articular; RL gym cuando se quiera estudiar la interfaz entre comandos y locomoción aprendida; mjlab cuando interese la composición de estados y policies de cuerpo completo. Son flujos diferentes, no tres componentes que deban correr juntos.

No se entrenaron redes ni se probó hardware físico. Los resultados históricos son cualitativos: no hay mediciones de tasa de caída, errores de tracking ni ensayos estadísticos. Los chats orientan el relato; código, configuraciones y cambios locales son la evidencia técnica recuperada.
