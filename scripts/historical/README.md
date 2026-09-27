# Primeros prototipos recuperados

Estos archivos se recuperaron de /home/sarreche después de revisar la conversación pública. Se agregó únicamente cabecera de procedencia/licencia; su comportamiento se conserva como evidencia histórica. No se ejecutaron al recuperarlos. No son los scripts depurados del directorio padre.

| Archivo | Objetivo y resultado histórico | Limitación |
|---|---|---|
| read_g1.py | Monitor LowState mediante callback, una impresión por segundo | Imprime todos los slots y rpy, aunque rpy no se rellena en el bridge |
| move_elbow.py | Motor 25, objetivo relativo +0.30 rad durante 3 s; movimiento breve observado | Sin límites de target, watchdog, retorno ni secuencia de parada |
| stand_g1.py | q=0 para 29 motores con ganancias del ejemplo; no sostuvo equilibrio | No es stand_up/recovery ni controlador de balance |

Los tres usan domain 1 / lo del simulador Python. No usarlos con el domain 0 de mjlab ni con hardware físico. Importar los módulos ejecuta su código superior: no importarlos como librerías, especialmente los publishers. Para revisar su sintaxis usar compile/AST sin ejecutarlos.

El monitor es el único de estos archivos que solo suscribe estado. Con el simulador Python configurado como se documenta y unitree-env activo, se puede lanzar como script desde una terminal aparte. El estado publicado por el simulador puede tener 35 slots, aunque solo 29 sean motores efectivos.

MIT para los prototipos locales read_g1/move_elbow; stand_g1 conserva atribución BSD-3-Clause por las ganancias del ejemplo oficial. Ver LICENSE y THIRD_PARTY_NOTICES.md en la raíz, y la [cronología](../../docs/12-recovered-history.md).
