"""API de festivos de Colombia para workflows de respond.io.

GET /festivo            -> ¿hoy (hora Colombia) es festivo?
GET /festivo?fecha=AAAA-MM-DD -> consulta una fecha puntual (pruebas)
GET /salud              -> chequeo de vida

Festivos legales: librería `holidays` (Ley Emiliani incluida).
Ajustes manuales: dias_especiales.json (se relee en cada consulta, no requiere reinicio).
"""
import json, os
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import holidays
from fastapi import FastAPI, Header, HTTPException, Query

TZ = ZoneInfo("America/Bogota")
ESPECIALES = Path(os.getenv("DIAS_ESPECIALES", Path(__file__).with_name("dias_especiales.json")))
API_KEY = os.getenv("API_KEY")  # si se define, se exige el header X-API-Key

app = FastAPI(title="Festivos Colombia", docs_url=None, redoc_url=None)


def cargar_especiales() -> tuple[dict, set]:
    try:
        data = json.loads(ESPECIALES.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}, set()
    cerrados = {d["fecha"]: d.get("nombre", "Día no laboral") for d in data.get("cerrados", [])}
    habiles = {d["fecha"] for d in data.get("habiles", [])}
    return cerrados, habiles


@app.get("/salud")
def salud():
    return {"ok": True}


@app.get("/festivo")
def festivo(fecha: str | None = Query(None, pattern=r"^\d{4}-\d{2}-\d{2}$"),
            x_api_key: str | None = Header(None)):
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="no autorizado")
    try:
        dia = date.fromisoformat(fecha) if fecha else datetime.now(TZ).date()
    except ValueError:
        raise HTTPException(status_code=400, detail="fecha inválida")
    iso = dia.isoformat()
    cerrados, habiles = cargar_especiales()

    if iso in habiles:
        return {"fecha": iso, "festivo": False, "nombre": None, "fuente": "manual"}
    if iso in cerrados:
        return {"fecha": iso, "festivo": True, "nombre": cerrados[iso], "fuente": "manual"}
    nombre = holidays.CO(years=dia.year, language="es").get(dia)
    return {"fecha": iso, "festivo": nombre is not None, "nombre": nombre, "fuente": "ley" if nombre else None}
