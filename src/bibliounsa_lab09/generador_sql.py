from pathlib import Path
import json
import re

import jsonschema
import sqlglot
from sqlglot import exp

from bibliounsa_lab07.ia import ProveedorLLM

RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
DIRECTORIO_PROMPTS = RAIZ_PROYECTO / "prompts" / "sql"

TABLAS_PERMITIDAS = {
    "libros": {
        "id", "titulo", "autor", "categoria", "fecha_ingreso"
    },
    "ejemplares": {
        "id", "libro_id", "estado"
    },
    "prestamos": {
        "id", "ejemplar_id", "fecha_vencimiento", "fecha_devolucion"
    }
}

class GeneradorSQL:

    def __init__(self, proveedor: ProveedorLLM, version="v3"):
        if version not in {"v1", "v2", "v3"}:
            raise ValueError("Versión de prompt no válida")

        self.proveedor = proveedor
        self.version = version

        self.prompt_path = DIRECTORIO_PROMPTS / f"{version}.txt"
        self.esquema_path = DIRECTORIO_PROMPTS / "esquema.json"
        self.bd_path = DIRECTORIO_PROMPTS / "esquema_bd_pruebas.txt"

    def generar(self, solicitud: str):
        if not isinstance(solicitud, str) or not solicitud.strip():
            raise ValueError("La solicitud no puede estar vacía")

        prompt = self.prompt_path.read_text(encoding="utf-8")
        esquema = json.loads(
            self.esquema_path.read_text(encoding="utf-8")
        )
        esquema_bd = self.bd_path.read_text(encoding="utf-8")

        prompt = prompt.replace("{{esquema_bd}}", esquema_bd)
        prompt = prompt.replace("{{pregunta}}", solicitud)

        respuesta = self.proveedor.completar(prompt)
        resultado = json.loads(respuesta)

        jsonschema.validate(
            instance=resultado,
            schema=esquema
        )

        if resultado["requiere_aclaracion"]:
            if resultado["consulta_sql"] is not None:
                raise ValueError(
                    "No debe generarse SQL cuando se requiere aclaración"
                )

            if not resultado["preguntas"]:
                raise ValueError(
                    "Debe especificarse al menos una pregunta de aclaración"
                )

            return resultado

        consulta = resultado["consulta_sql"]

        if not isinstance(consulta, str) or not consulta.strip():
            raise ValueError("La consulta SQL es obligatoria")

        self._validar_consulta(consulta)

        return resultado

    @staticmethod
    def _validar_consulta(consulta):
        # Rechazar comentarios SQL.
        if re.search(r"--|/\*|\*/|#", consulta):
            raise ValueError("No se permiten comentarios SQL")

        try:
            sentencias = sqlglot.parse(consulta)
        except sqlglot.errors.ParseError as error:
            raise ValueError("La consulta SQL no es válida") from error

        # Debe existir exactamente una sentencia.
        if len(sentencias) != 1 or sentencias[0] is None:
            raise ValueError("Solo se permite una sentencia SQL")

        expresion = sentencias[0]

        # Solo se permite SELECT.
        if not isinstance(expresion, exp.Select):
            raise ValueError("Solo se permiten consultas SELECT")

        # No se permiten operaciones de escritura.
        if expresion.find(exp.Into):
            raise ValueError("No se permite SELECT INTO")

        # No permitimos CTE en esta primera versión.
        if expresion.find(exp.With):
            raise ValueError("No se permiten expresiones WITH")

        tablas = {}
        tablas_utilizadas = set()

        for tabla in expresion.find_all(exp.Table):
            nombre = tabla.name.lower()

            if nombre not in TABLAS_PERMITIDAS:
                raise ValueError(f"Tabla no permitida: {nombre}")

            alias = tabla.alias_or_name.lower()
            tablas[alias] = nombre
            tablas_utilizadas.add(nombre)

        # Comprobar columnas existentes.
        for columna in expresion.find_all(exp.Column):
            nombre_columna = columna.name.lower()

            if nombre_columna == "*":
                continue

            if columna.table:
                alias = columna.table.lower()

                if alias not in tablas:
                    raise ValueError(
                        f"Alias o tabla desconocida: {alias}"
                    )

                tabla_real = tablas[alias]

                if nombre_columna not in TABLAS_PERMITIDAS[tabla_real]:
                    raise ValueError(
                        f"Columna no permitida: {nombre_columna}"
                    )
            else:
                existe = any(
                    nombre_columna in TABLAS_PERMITIDAS[tabla]
                    for tabla in tablas_utilizadas
                )

                if not existe:
                    raise ValueError(
                        f"Columna no permitida: {nombre_columna}"
                    )
