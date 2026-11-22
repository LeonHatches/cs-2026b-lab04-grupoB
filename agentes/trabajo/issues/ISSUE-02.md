# ISSUE-02 · BiblioUNSA · Reserva sin matrícula vigente
**Origen:** caso sugerido para BiblioUNSA, Guía Lab 10, p. 17. **Tipo:** fallo sembrado en copia aislada.
**Observado:** `reservar_ejemplar(False, True)` devuelve `RESERVADA`.
**Esperado:** matrícula vencida rechazada antes de confirmar reserva.
**Prueba:** `tests/test_issue_02.py::test_issue02_matricula_vencida_rechazada`.
**Contexto:** HU-05 y servicio académico simulado de Labs 05–07. No se conecta a datos institucionales reales.
