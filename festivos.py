"""Lógica común: ¿una fecha es festivo en Colombia?

Festivos legales: librería `holidays` (Ley Emiliani incluida).
Ajustes manuales: dias_especiales.json ("cerrados" y "habiles").
"""
import json, os
from datetime import date
from pathlib import Path
from zoneinfo import ZoneInfo

import holidays

TZ = ZoneInfo("America/Bogota")
ESPECIALES = Path(os.getenv("DIAS_ESPECIALES", Path(__file__).with_name("dias_especiales.json")))


def cargar_especiales() -> tuple[dict, set]:
    try:
        data = json.loads(ESPECIALES.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}, set()
    cerrados = {d["fecha"]: d.get("nombre", "Día no laboral") for d in data.get("cerrados", [])}
    habiles = {d["fecha"] for d in data.get("habiles", [])}
    return cerrados, habiles


def consultar(dia: date) -> dict:
    iso = dia.isoformat()
    cerrados, habiles = cargar_especiales()
    if iso in habiles:
        return {"fecha": iso, "festivo": False, "nombre": None, "fuente": "manual"}
    if iso in cerrados:
        return {"fecha": iso, "festivo": True, "nombre": cerrados[iso], "fuente": "manual"}
    nombre = holidays.CO(years=dia.year, language="es").get(dia)
    return {"fecha": iso, "festivo": nombre is not None, "nombre": nombre, "fuente": "ley" if nombre else None}
