"""API de festivos de Colombia para workflows de respond.io (opción con servidor).

GET /festivo                   -> ¿hoy (hora Colombia) es festivo?
GET /festivo?fecha=AAAA-MM-DD  -> consulta una fecha puntual (pruebas)
GET /salud                     -> chequeo de vida
"""
import os
from datetime import date, datetime

from fastapi import FastAPI, Header, HTTPException, Query

from festivos import TZ, consultar

API_KEY = os.getenv("API_KEY")  # si se define, se exige el header X-API-Key

app = FastAPI(title="Festivos Colombia", docs_url=None, redoc_url=None)


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
    return consultar(dia)
