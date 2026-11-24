"""Datos estrictamente ficticios de BiblioUNSA. No contienen credenciales ni DNI."""
LIBROS = [
    {"id": "LIB-001", "titulo": "Algoritmos y estructuras de datos", "autor": "A. Docente", "ejemplares": 3},
    {"id": "LIB-002", "titulo": "Ingenieria de software", "autor": "B. Docente", "ejemplares": 1},
    {"id": "LIB-003", "titulo": "Bases de datos", "autor": "C. Docente", "ejemplares": 0},
]
PRESTAMOS = [
    {"id": "P-001", "usuario": "EST-001", "libro": "LIB-001", "estado": "PRESTADO", "vencimiento": "2026-11-10"},
    {"id": "P-002", "usuario": "EST-002", "libro": "LIB-002", "estado": "DEVUELTO", "vencimiento": "2026-11-08"},
    {"id": "P-003", "usuario": "EST-001", "libro": "LIB-003", "estado": "PRESTADO", "vencimiento": "2026-12-15"},
]
