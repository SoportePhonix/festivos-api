"""Genera publico/festivos.json: festivos de los próximos 12 meses (hora Colombia).
Incluye festivos legales y días cerrados de dias_especiales.json; excluye los marcados como hábiles.
Lo ejecuta la GitHub Action mensual."""
import json
from datetime import date, datetime, timedelta
from pathlib import Path

from festivos import TZ, consultar

ahora = datetime.now(TZ)
inicio = ahora.date()
# 12 meses: desde hoy hasta el último día del 12.º mes contando el actual
fin = (date(inicio.year + (inicio.month + 11) // 12, (inicio.month + 11) % 12 + 1, 1) + timedelta(days=31)).replace(day=1) - timedelta(days=1)

dias = []
d = inicio
while d <= fin:
    r = consultar(d)
    if r["festivo"]:
        dias.append({"fecha": r["fecha"], "dia": ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"][d.weekday()],
                     "nombre": r["nombre"], "fuente": r["fuente"]})
    d += timedelta(days=1)

salida = {"desde": inicio.isoformat(), "hasta": fin.isoformat(), "total": len(dias),
          "generado": ahora.isoformat(timespec="seconds"), "festivos": dias}
destino = Path(__file__).with_name("publico") / "festivos.json"
destino.write_text(json.dumps(salida, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"{len(dias)} festivos entre {inicio} y {fin}")
