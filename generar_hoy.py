"""Genera publico/hoy.json con el estado del día actual (hora Colombia).
Lo ejecuta la GitHub Action diaria; respond.io lee el archivo por su URL raw."""
import json
from datetime import datetime
from pathlib import Path

from festivos import TZ, consultar

ahora = datetime.now(TZ)
salida = consultar(ahora.date()) | {"generado": ahora.isoformat(timespec="seconds")}
destino = Path(__file__).with_name("publico") / "hoy.json"
destino.write_text(json.dumps(salida, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(salida)
