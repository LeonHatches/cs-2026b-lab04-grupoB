# E6 - Métricas antes / después 

## Tabla de comparación de uso de 'radon'

| Medida | Antes | Después |
|---|---|---|
| Complejidad de `ServicioBiblioteca.reservar` | 13 (C) | 5 (A) |
| Complejidad de `ServicioBiblioteca.calcular_multa` | 4 (A) | 2 (A) |
| Complejidad de `ServicioBiblioteca.__init__` | 3 (A) | 7 (B) |
| Complejidad de clase `ServicioBiblioteca` | 8 (B) | 6 (B) |
| Complejidad promedio | 3.75 (A) | 1.71 (A) |
| Lineas de código (SLOC) | 76 | 276 |
|  Indice de mantenibilidad de `servicios.py` | 52.10 (A) | 65.92 (B) |

## Análisis de trade-off

La aplicación de patrones de diseño permitió reducir la complejidad ciclomática promedio de 3.75 a 1.71 y separar las responsabilidades del sistema. 

Además, se facilitó la incorporación de nuevas variantes y el mantenimiento de los componentes. Esto incrementó la complejidad estructural y el esfuerzo necesario para comprender el funcionamiento del sistema.

Si la biblioteca mantuviera una sola API y una sola política, la versión simple podría ser suficiente.

## Patrón rechazado

Se decidió no aplicar Singleton al servicio de reservas porque no se requiere una instancia única y global para gestionar las operaciones. Además, podría introducir estado compartido y dificultar las pruebas unitarias.