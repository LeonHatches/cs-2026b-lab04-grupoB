import json

import pytest
from jsonschema import ValidationError

from bibliounsa_lab09 import GeneradorCriterios, GeneradorSQL

class ProveedorPrueba:
    """Simula el proveedor LLM del Lab07."""

    def __init__(self, respuesta):
        self.respuesta = respuesta
        self.llamadas = 0
        self.ultimo_prompt = None

    def completar(self, prompt):
        self.llamadas += 1
        self.ultimo_prompt = prompt
        return self.respuesta


CRITERIOS_VALIDOS = {
    "historia_id": "HU-05",
    "invest_ok": True,
    "preguntas": [],
    "escenarios": [
        {
            "titulo": "Inicio de sesión exitoso",
            "tipo": "exito",
            "dado": ["El usuario está registrado"],
            "cuando": "Ingresa sus credenciales correctas",
            "entonces": ["El sistema permite el acceso"]
        }
    ]
}

CRITERIOS_ACLARACION = {
    "historia_id": "HU-05",
    "invest_ok": False,
    "preguntas": ["¿Qué roles pueden iniciar sesión?"],
    "escenarios": []
}

SQL_VALIDO = {
    "consulta_sql": "SELECT * FROM libros WHERE autor = :autor",
    "parametros": {"autor": "Gabriel García Márquez"},
    "requiere_aclaracion": False,
    "preguntas": []
}

SQL_ACLARACION = {
    "consulta_sql": None,
    "parametros": {},
    "requiere_aclaracion": True,
    "preguntas": ["¿Qué usuario desea consultar?"]
}

class TestGeneradorCriterios:

    def test_generar_criterios_validos(self):
        proveedor = ProveedorPrueba(json.dumps(CRITERIOS_VALIDOS))
        generador = GeneradorCriterios(proveedor)

        resultado = generador.generar(
            "HU-05",
            "Como usuario quiero iniciar sesión."
        )

        assert resultado == CRITERIOS_VALIDOS
        assert proveedor.llamadas == 1

    def test_generar_criterios_con_aclaraciones(self):
        proveedor = ProveedorPrueba(json.dumps(CRITERIOS_ACLARACION))
        generador = GeneradorCriterios(proveedor)

        resultado = generador.generar(
            "HU-05",
            "Como usuario quiero iniciar sesión."
        )

        assert resultado["invest_ok"] is False
        assert len(resultado["preguntas"]) >= 1
        assert resultado["escenarios"] == []

    def test_rechazar_json_invalido(self):
        proveedor = ProveedorPrueba("Esto no es JSON")
        generador = GeneradorCriterios(proveedor)

        with pytest.raises(json.JSONDecodeError):
            generador.generar(
                "HU-05",
                "Historia de usuario"
            )

    def test_rechazar_campos_obligatorios_ausentes(self):
        respuesta = {
            "historia_id": "HU-05",
            "invest_ok": True,
            "preguntas": []
        }

        proveedor = ProveedorPrueba(json.dumps(respuesta))
        generador = GeneradorCriterios(proveedor)

        with pytest.raises(ValidationError):
            generador.generar(
                "HU-05",
                "Historia de usuario"
            )

    def test_rechazar_tipo_de_escenario_invalido(self):
        respuesta = json.loads(json.dumps(CRITERIOS_VALIDOS))
        respuesta["escenarios"][0]["tipo"] = "incorrecto"

        proveedor = ProveedorPrueba(json.dumps(respuesta))
        generador = GeneradorCriterios(proveedor)

        with pytest.raises(ValidationError):
            generador.generar(
                "HU-05",
                "Historia de usuario"
            )

    def test_rechazar_investigacion_sin_preguntas(self):
        respuesta = {
            "historia_id": "HU-05",
            "invest_ok": False,
            "preguntas": [],
            "escenarios": []
        }

        proveedor = ProveedorPrueba(json.dumps(respuesta))
        generador = GeneradorCriterios(proveedor)

        with pytest.raises(ValidationError):
            generador.generar(
                "HU-05",
                "Historia de usuario"
            )

    def test_rechazar_historia_vacia(self):
        proveedor = ProveedorPrueba("{}")
        generador = GeneradorCriterios(proveedor)

        with pytest.raises(ValueError):
            generador.generar("HU-05", "")

        assert proveedor.llamadas == 0

class TestGeneradorSQL:

    def test_generar_consulta_sql_valida(self):
        proveedor = ProveedorPrueba(json.dumps(SQL_VALIDO))
        generador = GeneradorSQL(proveedor)

        resultado = generador.generar(
            "Consultar los libros de un autor."
        )

        assert resultado == SQL_VALIDO
        assert resultado["consulta_sql"].startswith("SELECT")
        assert proveedor.llamadas == 1

    def test_generar_respuesta_con_aclaracion(self):
        proveedor = ProveedorPrueba(json.dumps(SQL_ACLARACION))
        generador = GeneradorSQL(proveedor)

        resultado = generador.generar(
            "Consultar los libros de un autor."
        )

        assert resultado["consulta_sql"] is None
        assert resultado["requiere_aclaracion"] is True
        assert len(resultado["preguntas"]) > 0

    def test_rechazar_json_invalido(self):
        proveedor = ProveedorPrueba("Respuesta incorrecta")
        generador = GeneradorSQL(proveedor)

        with pytest.raises(json.JSONDecodeError):
            generador.generar("Consultar libros")

    def test_rechazar_campos_obligatorios_ausentes(self):
        respuesta = {
            "consulta_sql": "SELECT * FROM libros",
            "parametros": {}
        }

        proveedor = ProveedorPrueba(json.dumps(respuesta))
        generador = GeneradorSQL(proveedor)

        with pytest.raises(ValidationError):
            generador.generar("Consultar libros")

    def test_rechazar_tipo_incorrecto(self):
        respuesta = {
            **SQL_VALIDO,
            "requiere_aclaracion": "no"
        }

        proveedor = ProveedorPrueba(json.dumps(respuesta))
        generador = GeneradorSQL(proveedor)

        with pytest.raises(ValidationError):
            generador.generar("Consultar libros")

    def test_rechazar_consulta_delete(self):
        respuesta = {
            **SQL_VALIDO,
            "consulta_sql": "DELETE FROM usuarios"
        }

        proveedor = ProveedorPrueba(json.dumps(respuesta))
        generador = GeneradorSQL(proveedor)

        with pytest.raises(ValueError):
            generador.generar("Eliminar usuarios")

    def test_rechazar_consulta_insert(self):
        respuesta = {
            **SQL_VALIDO,
            "consulta_sql": "INSERT INTO usuarios VALUES (1)"
        }

        proveedor = ProveedorPrueba(json.dumps(respuesta))
        generador = GeneradorSQL(proveedor)

        with pytest.raises(ValueError):
            generador.generar("Insertar usuario")

    def test_rechazar_consulta_multiple(self):
        respuesta = {
            **SQL_VALIDO,
            "consulta_sql": "SELECT * FROM libros; DELETE FROM libros"
        }

        proveedor = ProveedorPrueba(json.dumps(respuesta))
        generador = GeneradorSQL(proveedor)

        with pytest.raises(ValueError):
            generador.generar("Consultar libros")

    def test_rechazar_solicitud_vacia(self):
        proveedor = ProveedorPrueba("{}")
        generador = GeneradorSQL(proveedor)

        with pytest.raises(ValueError):
            generador.generar("")

        assert proveedor.llamadas == 0

    def test_criterios_reemplaza_variables_del_prompt(self):
        proveedor = ProveedorPrueba(json.dumps(CRITERIOS_VALIDOS))
        generador = GeneradorCriterios(proveedor)

        generador.generar(
            "HU-05",
            "Como lector quiero consultar libros."
        )

        assert "HU-05" in proveedor.ultimo_prompt
        assert "Como lector quiero consultar libros." in proveedor.ultimo_prompt
        assert "{{id}}" not in proveedor.ultimo_prompt
        assert "{{historia}}" not in proveedor.ultimo_prompt

    def test_sql_reemplaza_variables_del_prompt(self):
        proveedor = ProveedorPrueba(json.dumps(SQL_VALIDO))
        generador = GeneradorSQL(proveedor)

        generador.generar("Consultar los libros de un autor.")

        assert "Consultar los libros de un autor." in proveedor.ultimo_prompt
        assert "{{pregunta}}" not in proveedor.ultimo_prompt
        assert "{{esquema_bd}}" not in proveedor.ultimo_prompt

    def test_sql_rechaza_tabla_no_permitida(self):
        consulta = "SELECT * FROM usuarios"

        with pytest.raises(ValueError):
            GeneradorSQL._validar_consulta(consulta)

    def test_sql_rechaza_columna_no_permitida(self):
        consulta = "SELECT contrasena FROM libros"

        with pytest.raises(ValueError):
            GeneradorSQL._validar_consulta(consulta)

    def test_sql_rechaza_comentarios(self):
        consulta = "SELECT * FROM libros -- comentario"

        with pytest.raises(ValueError):
            GeneradorSQL._validar_consulta(consulta)

    def test_sql_permite_consulta_con_parametro(self):
        consulta = "SELECT titulo FROM libros WHERE autor = :autor"

        GeneradorSQL._validar_consulta(consulta)
