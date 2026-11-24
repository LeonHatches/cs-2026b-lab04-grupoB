# MCP Inspector de BiblioUNSA

Desde la raíz del repositorio, con el SDK instalado en `.venv`, inicia el Inspector en PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pip install "mcp==2.3.0"
$pythonLab = (Resolve-Path .\.venv\Scripts\python.exe).Path
$servidorLab = (Resolve-Path .\bibliounsa_mcp\servidor_mcp\bibliounsa_mcp.py).Path
npx.cmd -y @modelcontextprotocol/inspector@0.21.1 $pythonLab $servidorLab
```

1. En **Tools**, pulsa **List Tools** y captura las tres herramientas. **Resources** muestra el reglamento y la plantilla de ADR. **Prompts** muestra `aviso_vencimiento`.
2. Ejecuta `prestamos_vencidos` con `hoy = 2026-11-23` y captura el resultado estructurado con `cantidad = 1` y el préstamo `P-001`.
3. Ejecuta la misma herramienta con `hoy = ayer` y captura el error con la indicación `AAAA-MM-DD`.

Junto con el resultado de pytest, estas tres vistas corresponden a la Figura 4 del informe.

Para verificar el servidor por stdio desde la terminal:

```powershell
.\.venv\Scripts\python.exe bibliounsa_mcp/cliente/explorar.py
Push-Location bibliounsa_mcp
..\.venv\Scripts\python.exe -m pytest -q pruebas
Pop-Location
```
