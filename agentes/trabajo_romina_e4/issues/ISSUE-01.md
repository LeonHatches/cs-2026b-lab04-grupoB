# ISSUE-01 · BiblioUNSA · Multas calculadas incluyendo domingos
**Origen:** caso sugerido para BiblioUNSA, Guía Lab 10, p. 17. **Tipo:** fallo sembrado en copia aislada.
**Observado:** `dias_multa` cuenta todos los días, incluidos domingos.
**Esperado:** los domingos no se contabilizan; intervalo (vencimiento, devolución].
**Prueba:** `tests/test_issue_01.py::test_issue01_no_multa_domingo`.
**Contexto:** continuidad del módulo de multas y patrón Strategy de Lab 07. La norma de excluir domingos es una regla de prueba de esta práctica, no una norma institucional verificada.
