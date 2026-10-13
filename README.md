# API de festivos Colombia

Responde si una fecha es festivo en Colombia, para el workflow "Asignación por horario" de respond.io.
El horario de atención NO está aquí: lo define el paso Date & Time del workflow.

## Respuesta
`GET /festivo` (hoy, hora Colombia) o `GET /festivo?fecha=2026-11-02`
```json
{"fecha": "2026-11-02", "festivo": true, "nombre": "Día de Todos los Santos (observado)", "fuente": "ley"}
```
- `fuente`: `ley` (librería holidays) o `manual` (dias_especiales.json).
- Si se define la variable `API_KEY`, la petición debe traer el header `X-API-Key`.

## Ajustes manuales — dias_especiales.json
- `cerrados`: días sin atención aunque no sean festivo legal (24 y 31 dic, cierres).
- `habiles`: festivos legales en que sí se atiende.
Se relee en cada consulta: editar el archivo aplica de inmediato.

## Mantenimiento
Actualizar la librería una vez al año o cuando cambie la ley: `pip install -U holidays` (o reconstruir la imagen).
Prueba rápida: `curl -H "X-API-Key: $API_KEY" "https://<dominio>/festivo?fecha=2027-07-12"`

## Opción A: Docker Compose (recomendada)
```bash
cp .env.example .env          # editar API_KEY
docker compose up -d --build
docker compose ps             # debe quedar "healthy"
curl -H "X-API-Key: <clave>" "http://127.0.0.1:8000/festivo?fecha=2026-11-02"
```
- Editar `dias_especiales.json` en el host aplica sin reiniciar (está montado como volumen).
- Actualizar festivos de la librería: `docker compose build --no-cache && docker compose up -d`.

## Opción B: systemd
```bash
sudo mkdir -p /opt/festivos-api && sudo cp app.py dias_especiales.json requirements.txt /opt/festivos-api/
cd /opt/festivos-api && sudo python3 -m venv venv && sudo venv/bin/pip install -r requirements.txt
sudo cp festivos-api.service /etc/systemd/system/   # editar API_KEY antes
sudo systemctl daemon-reload && sudo systemctl enable --now festivos-api
```

En ambos casos queda en 127.0.0.1:8000: publícalo detrás de tu proxy inverso (nginx/Caddy) con HTTPS.
respond.io necesita alcanzarlo desde internet.
