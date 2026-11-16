from pathlib import Path
import json
import jsonschema

from bibliounsa_lab07.ia import ProveedorLLM

RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
DIRECTORIO_PROMPTS = RAIZ_PROYECTO / "prompts" / "criterios"

class GeneradorCriterios:

    def __init__(self, proveedor: ProveedorLLM, version="v3"):
        if version not in {"v1", "v2", "v3"}:
            raise ValueError("Versión de prompt no válida")

        self.proveedor = proveedor
        self.version = version

        self.prompt_path = DIRECTORIO_PROMPTS / f"{version}.txt"
        self.esquema_path = DIRECTORIO_PROMPTS / "esquema.json"

    def generar(self, historia_id: str, historia_usuario: str):
        if not isinstance(historia_id, str) or not historia_id.strip():
            raise ValueError("El ID de la historia no puede estar vacío")

        if not isinstance(historia_usuario, str) or not historia_usuario.strip():
            raise ValueError("La historia de usuario no puede estar vacía")

        prompt = self.prompt_path.read_text(encoding="utf-8")
        esquema = json.loads(
            self.esquema_path.read_text(encoding="utf-8")
        )

        prompt = prompt.replace("{{id}}", historia_id)
        prompt = prompt.replace("{{historia}}", historia_usuario)

        respuesta = self.proveedor.completar(prompt)
        resultado = json.loads(respuesta)

        jsonschema.validate(
            instance=resultado,
            schema=esquema
        )

        if resultado["historia_id"] != historia_id:
            raise ValueError("El ID devuelto no coincide con la historia solicitada")

        return resultado
