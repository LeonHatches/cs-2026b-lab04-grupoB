"""E5 BiblioUNSA: comparación determinista de agente único y multiagente."""
import json
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory

from agente.herramientas import Herramientas
from agente.modelos import ModeloGrabado
from agente.nucleo import Agente
from agente.politica import Politica

ROOT = Path(__file__).resolve().parent
ORIGINAL = ROOT / "trabajo"
TRAYECTORIAS = ROOT / "trayectorias"
TRAZAS = ROOT / "trazas"
TRAZAS.mkdir(exist_ok=True)


def ejecutar_rol(nombre, archivo, herramientas, politica, objetivo, sufijo):
    agente = Agente(
        nombre,
        ModeloGrabado(TRAYECTORIAS / archivo),
        herramientas,
        politica,
        objetivo,
        TRAZAS / f"issue02_{sufijo}.jsonl"
    )
    resultado = agente.ejecutar()

    acciones = [e for e in agente.eventos if e["tipo"] == "accion"]

    return {
        "rol": nombre,
        "acciones": len(acciones),
        "caracteres_historial": sum(
            len(m["content"]) for m in agente.historial
        ),
        "resultado": resultado
    }


def comparar(multiagente):
    modo = "multiagente" if multiagente else "unico"

    with TemporaryDirectory(prefix=f"bibliounsa-e5-{modo}-") as temporal:
        copia = Path(temporal) / "copia"
        shutil.copytree(
            ORIGINAL, copia,
            ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache")
        )

        h = Herramientas(copia, ORIGINAL)
        roles = []

        if multiagente:
            plan = ejecutar_rol(
                "planificador", "issue02_planificador_demo.json",
                h, Politica(herramientas_permitidas=set()),
                "Planificar la resolución de ISSUE-02",
                "planificador_e5"
            )
            roles.append(plan)

            ejecutor = ejecutar_rol(
                "ejecutor", "issue02_ejecutor_demo.json",
                h, Politica(),
                "Resolver ISSUE-02. Plan: " + plan["resultado"],
                "ejecutor_e5"
            )
            roles.append(ejecutor)

            revisor = ejecutar_rol(
                "revisor", "issue02_revisor_demo.json",
                h,
                Politica(herramientas_permitidas={
                    "ver_cambios", "ejecutar_pruebas"
                }),
                "Revisar ISSUE-02. Resultado: " + ejecutor["resultado"],
                "revisor_e5"
            )
            roles.append(revisor)

        else:
            roles.append(ejecutar_rol(
                "agente_unico", "issue02_unico_demo.json",
                h, Politica(),
                "Resolver y verificar ISSUE-02",
                "unico_e5"
            ))

        pruebas = h.ejecutar_pruebas("tests/test_issue_02.py")
        diff = h.ver_cambios()

        (TRAZAS / f"issue02_{modo}_e5.diff").write_text(
            diff + "\n", encoding="utf-8"
        )

        aprobado = (
            "returncode=0" in pruebas
            and "2 passed" in pruebas
            and "MATRICULA_NO_VIGENTE" in diff
        )

        return {
            "modo": modo,
            "roles": roles,
            "acciones_totales": sum(r["acciones"] for r in roles),
            "caracteres_historial": sum(
                r["caracteres_historial"] for r in roles
            ),
            "pruebas": pruebas,
            "correccion_verificada": aprobado
        }


def main():
    resultados = [comparar(False), comparar(True)]

    (TRAZAS / "issue02_e5_comparacion.json").write_text(
        json.dumps(resultados, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )

    print("\n=== E5: COMPARACIÓN DE AGENTES — ISSUE-02 ===")
    for r in resultados:
        print(f"\nConfiguración: {r['modo']}")
        for rol in r["roles"]:
            print(f"  {rol['rol']}: {rol['acciones']} acciones")
        print(f"Total de acciones: {r['acciones_totales']}")
        print(f"Caracteres acumulados: {r['caracteres_historial']}")
        print(r["pruebas"])
        print(f"Corrección verificada: {r['correccion_verificada']}")

    if not all(r["correccion_verificada"] for r in resultados):
        raise SystemExit("ERROR: alguna configuración no superó la verificación")


if __name__ == "__main__":
    main()
