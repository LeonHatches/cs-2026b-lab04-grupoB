# No determinismo

Se ejecutó la mejor versión del prompt (v3) tres veces sobre los mismos tres casos, obteniendo nueve respuestas por experimento.

1. Con el proveedor grabado, sin consultar una IA real, las nueve ejecuciones produjeron respuestas idénticas, demostrando que las pruebas con fixtures son reproducibles.
2. Con Gemini, se observaron variaciones en las respuestas, como el cambio del nombre del parámetro SQL.
3. En el caso SQL02, Gemini utilizó un parámetro de autor vacío en lugar de solicitar una aclaración, incumpliendo el comportamiento esperado.
4. Algunas respuestas incluyeron explicaciones y bloques Markdown antes del JSON.
5. Se concluye que los fixtures permiten pruebas controladas y repetibles, pero no reflejan toda la variabilidad de una IA real, por lo que deben complementarse con evaluaciones usando modelos reales.