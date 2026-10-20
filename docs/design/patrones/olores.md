# E1 — Olores del flujo de reserva BiblioUNSA

## Base y alcance

Se adapta el ZIP de referencia al flujo de `docs/design/secuencia-reservar-libro.puml`
del Lab05: validar matrícula, comprobar disponibilidad, reservar y confirmar.
`src/reservas/reservas.py` contiene interfaces y métodos sin implementar;
el módulo `src/bibliounsa_lab07/` es una implementación didáctica simulada.

`antes/servicio.py` conserva la versión inicial. `servicio.py` aplica únicamente
Strategy, Adapter y Factory. El puerto `ServicioMatricula.validar_vigente`
corresponde al del Lab05; los identificadores de las pruebas son cadenas y
el catálogo en memoria sustituye a los repositorios para este ejercicio.
La reserva devuelve `RESERVADA`; no implementa el controlador ni una API web.
Las tarifas de multa son datos del ejemplo, no una norma institucional.

## Olores y decisiones de E1–E2

| Olor concreto | Ubicación inicial | Patrón y principio | Decisión y costo |
|---|---|---|---|
| El servicio interpreta dos interfaces y formatos académicos | `ServicioBiblioteca.reservar` | Adapter; DIP | Adoptar adaptadores que implementan `ServicioMatricula`; agrega dos clases |
| Selección de proveedor mediante `if/elif` dentro de la reserva | `ServicioBiblioteca.reservar` | Factory de registro; OCP | Adoptar `FabricaMatricula`; se registra un tercer adaptador sin editar el servicio |
| La multa depende de condicionales por tipo de usuario | `ServicioBiblioteca.calcular_multa` | Strategy; OCP | Adoptar `PoliticaMulta`, con estrategias para estudiante y docente |
| Selección de la política mezclada con el cálculo | `ServicioBiblioteca.calcular_multa` | Factory de registro; SRP y OCP | Adoptar `FabricaMultas`; añadir una tarifa requiere estrategia y registro |
| Reintentos duplicados en ambas ramas académicas | `ServicioBiblioteca.reservar` | Adapter en E2; Decorator en E4 | Unificar la consulta por el puerto en E2; conservar el bucle de reintentos en el servicio para la extracción de E4 |
| Confirmación y auditoría escritas dentro del caso de uso | `ServicioBiblioteca.reservar` | Observer; SRP | Conservar los avisos iniciales en E2; la extracción corresponde a E4 |

## Propuesta de IA descartada

Se considera y se rechaza Singleton para las fábricas: los registros no necesitan
una instancia global. Las fábricas se inyectan por constructor y cada prueba
puede registrar variantes sin contaminar las demás. El registro de creadores
es suficiente; no se requieren familias de productos de Abstract Factory.

## Contrato protegido por las pruebas

- Misma suite parametrizada sobre la implementación inicial y E2.
- Matrícula rechazada y errores distintos de `TimeoutError` no se reintentan.
- Una consulta académica admite tres intentos en total. Este límite del ZIP
  corresponde a matrícula; no representa el reintento transaccional del Lab05.
- Una reserva duplicada, un ejemplar no disponible o un conflicto al confirmar
  no generan una nueva confirmación ni auditoría.
- Los servicios académicos y el catálogo son simulados; no se contactan APIs.
- El préstamo reutiliza la clase inicial con condicionales. No se aplica State
  en E2; se conservan sus pruebas como contrato para la siguiente entrega.

## Verificación reproducible

```powershell
python -m pytest -v tests/test_comportamiento.py
python -m pytest -v tests/test_patrones.py -k "factory or adapter or strategy"
python -m radon cc -s -a src/bibliounsa_lab07/antes/
```

La salida inicial de radon se conserva en `e1-radon.txt`, en esta carpeta.
Las métricas finales antes/después se consolidan en E6.
