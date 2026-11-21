# ISSUE-03 · BiblioUNSA · Préstamo devuelto figura vencido
**Origen:** caso sugerido para BiblioUNSA, Guía Lab 10, p. 17. **Tipo:** fallo sembrado en copia aislada.
**Observado:** `prestamo_vencido("DEVUELTO", fecha_pasada, hoy)` devuelve `True`.
**Esperado:** un préstamo ya devuelto no figura vencido, independientemente de fecha límite.
**Prueba:** `tests/test_issue_03.py::test_issue03_devuelto_no_sigue_vencido`.
**Contexto:** máquina de estados Lab 05 y State Lab 07.
