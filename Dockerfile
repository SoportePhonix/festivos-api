FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py festivos.py ./
# dias_especiales.json se monta como volumen para editarlo sin reconstruir
ENV DIAS_ESPECIALES=/data/dias_especiales.json
EXPOSE 8000
USER nobody
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
