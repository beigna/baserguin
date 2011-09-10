Snoopy OO
=========

Descripción
-----------

Snoopy OO (cuyo nombre clave es Baserguín, en honor a Juan Pablo Baserga) es la segunda generación de Snoopy, el sistema de envío y cobro de mensajería SMS/MMS, con soporte para trabajo distribuido y orientado a objetos.

Snoopy era un sistema multiproceso condenado a correr en un solo servidor, pero replicable. Baserguín mejora esto y añade muchas características.

Snoopy OO no se encuentra completo, sólo implementa una de los 5 pilares que maneja Snoopy, pero es productivo.

Para los nostálgicos y llorones (como yo), Snoopy OO jamás será terminado ya que:

1. No trabajo en la empresa donde se producía.
2. Dicha empresa ha sido absorvida y sus plataformas deprecadas.

Si bien es algo egocéntrico, es una gran pieza de software que diseñé junto a Damián Lacapra con asistencia de Ángel Velásquez y se basa en el diseño anterior que hice con la ayuda de Pablo Moreno, que a su vez tiene mucho de lo que hicimos hace años junto a Ángel Freire.

Dejo esto aquí para consulta y referencia sobre el uso de threading y processing en Python ;)

Hasta siempre Baserguín, aquí y en mi corazón.

Atte. Ignacio Juan Martín Benedetti.


Curiosidades
------------

* El nombre clave Baserguín estuvo oculto durante su desarrollo y salida a producción dado que era un apodo chistoso basado en el apellido de Juan Pablo Baserga, quién fuera gerente de tecnología. Él acusaba al "perro estúpido" (Snoopy) por ciertas fallas de la plataforma de cobros y por eso un día "enojado" empecé con Baserguín, quién demostró ser un perro muy ágil :P

* La versión actual tiene un Bug que, pese a ser reportado por mí antes y luego de dejar la empresa, nunca se solucionó. Baserguín no cierra la conexión que abre contra RabbitMQ en el caso de que falle el cobro contra CCO, dejándola perdida. Conforme se acumulen estas conexiones se saturan los FileDescriptor de RabbitMQ y este queda fuera de servicio. Pero reiniciado el rabbit, problema resuelto. Juan Pablo Baserga, José Mária Fassiato, Holly Skorich y yo sabemos de esto :P
