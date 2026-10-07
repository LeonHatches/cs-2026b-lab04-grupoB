# HU-05 — Reservar un libro con matrícula vigente
**Como** estudiante de la UNSA, **quiero** reservar un ejemplar disponible de un libro, previa validación de mi matrícula vigente, **para** recogerlo en la biblioteca sin conflictos de disponibilidad.

## Criterios de aceptación
1. **Dado** un estudiante autenticado con matrícula vigente y un ejemplar DISPONIBLE, **cuando** solicita la reserva, **entonces** el sistema registra una única reserva RESERVADA, marca el ejemplar RESERVADO y envía la confirmación.
2. **Dado** un estudiante cuya matrícula no está vigente, **cuando** intenta reservar, **entonces** se rechaza la solicitud sin modificar la disponibilidad del ejemplar.
3. **Dado** un ejemplar ya reservado o prestado, **cuando** dos estudiantes intentan reservarlo concurrentemente, **entonces** solo una transacción puede confirmar la reserva y la otra recibe aviso de falta de disponibilidad.
4. **Dado** que la API académica no responde o se agota el tiempo de espera, **cuando** se solicita una reserva, **entonces** se rechaza temporalmente sin asumir matrícula vigente y sin crear una reserva.

## Reglas de negocio y decisiones de diseño
- Una reserva pertenece a un estudiante y a exactamente un ejemplar.
- Un ejemplar no puede tener más de una reserva activa a la vez; se usa bloqueo transaccional/condición de unicidad en PostgreSQL (ADR-002).
- La matrícula se consulta exclusivamente a través de la interfaz ServicioMatricula, implementada por ApiAcademicaAdapter (ADR-003), nunca directamente a la base de datos académica.
- Los nombres de estados son una propuesta de diseño del Lab 05; no se presentan como estados previamente implementados.
