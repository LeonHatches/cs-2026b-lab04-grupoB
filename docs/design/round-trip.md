# Round-trip — BiblioUNSA

## Comparación entre diagrama de diseño y diagrama obtenido del código

| Diferencia observada | Causa | Acción |
|---|---|---|
| Nombres en snake_case | Convención de Python | Aceptable |
| Las interfaces aparecen como clases | Pyreverse no detecta interfaces | Aceptable para Python |
| Las clases enumeradas no muestran sus datos | Pyreverse no representa los datos dentro de una clase enumerada | Corregir, agregar los datos de las clases enumeradas |
| No hay multiplicidades | El código no representa las multiplicidades | Verificar multiplicidades |
| Relaciones por retorno de función no existen | Pyreverse no representa ciertas relaciones de las clases explicitamente | Aceptable en Python |
| No hay modificadores de acceso | Python no utiliza modificadores de acceso cómunes | Aceptable en Python |
