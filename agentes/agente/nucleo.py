"""Bucle del agente: pensar -> actuar -> observar (ReAct), modelado como máquina de estados.

Estados: DECIDIENDO -> VALIDANDO_CONTRATO -> EVALUANDO_POLITICA -> EJECUTANDO -> OBSERVANDO -> DECIDIENDO ...
Estados finales: FINALIZADO (respuesta final) o LIMITE_ALCANZADO (presupuesto de pasos agotado).
"""
import json
import time
from pathlib import Path

from agente.contrato import validar_decision


class Agente:
    def __init__(self, nombre, modelo, herramientas, politica, objetivo, traza_archivo):
        self.nombre, self.modelo, self.h, self.politica = nombre, modelo, herramientas, politica
        self.historial = [{"role": "user", "content": objetivo}]       # memoria de corto plazo
        self.traza_archivo, self.eventos = traza_archivo, []

    def _registrar(self, **evento):
        evento["t"] = round(time.perf_counter() - self._t0, 3)
        evento["agente"] = self.nombre
        self.eventos.append(evento)

    def ejecutar(self) -> str:
        self._t0 = time.perf_counter()
        self._registrar(tipo="objetivo", estado="INICIO", texto=self.historial[0]["content"])
        ruta = Path(self.traza_archivo)
        ruta.parent.mkdir(parents=True, exist_ok=True)
        try:
            return self._iterar()
        finally:
            with ruta.open("w", encoding="utf-8") as archivo:
                for evento in self.eventos:
                    archivo.write(json.dumps(evento, ensure_ascii=False) + "\n")

    def _iterar(self) -> str:
        conocidas = set(self.h.catalogo())
        for paso in range(1, self.politica.max_pasos + 2):
            self._registrar(tipo="estado", estado="DECIDIENDO", paso=paso)
            d = self.modelo.decidir(self.historial)
            self.historial.append({"role": "assistant", "content": json.dumps(d, ensure_ascii=False)})
            self._registrar(tipo="estado", estado="VALIDANDO_CONTRATO", paso=paso)
            ok, motivo = validar_decision(d, conocidas)
            if not ok:
                obs = f"ERROR DE CONTRATO: {motivo}. Responda solo con el JSON del protocolo."
                self._registrar(tipo="accion", estado="CONTRATO_INVALIDO", paso=paso, pensamiento=str(d)[:200],
                                accion="(ninguna)", args={}, observacion=obs, bloqueada=True)
            elif "final" in d:
                self._registrar(tipo="final", estado="FINALIZADO", paso=paso, pensamiento=d["pensamiento"], texto=d["final"])
                return d["final"]
            else:
                accion, args = d["accion"], d["args"]

                def registrar_aprobacion():
                    self._registrar(tipo="estado", estado="ESPERANDO_APROBACION", paso=paso,
                                    accion=accion, texto="Se solicitó decisión del humano")

                self._registrar(tipo="estado", estado="EVALUANDO_POLITICA", paso=paso, accion=accion)
                veredicto = self.politica.evaluar(
                    accion, args, paso, al_solicitar_aprobacion=registrar_aprobacion,
                )
                if veredicto.permitido:
                    self._registrar(tipo="estado", estado="EJECUTANDO", paso=paso, accion=accion)
                    try:
                        obs = getattr(self.h, accion)(**args)             # EJECUTANDO
                    except Exception as e:                                # el error también es una observación
                        obs = f"ERROR: {type(e).__name__}: {e}"
                    self._registrar(tipo="accion", estado="OBSERVANDO", paso=paso, pensamiento=d["pensamiento"],
                                    accion=accion, args=args, observacion=obs[:600], bloqueada=False)
                else:
                    obs = f"BLOQUEADO POR LA POLÍTICA: {veredicto.motivo}"
                    self._registrar(tipo="accion", estado="BLOQUEADO", paso=paso,
                                    pensamiento=d["pensamiento"], accion=accion, args=args, observacion=obs, bloqueada=True)
            self.historial.append({"role": "user", "content": f"Observación: {obs}"})   # OBSERVANDO -> DECIDIENDO
        texto = "Se agotó el presupuesto de pasos."
        self._registrar(tipo="final", estado="LIMITE_ALCANZADO", paso=paso, texto=texto)
        return texto
