FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
# Instalamos los requisitos y añadimos la pieza que falta para que Starlette no explote
RUN pip install --no-cache-dir -r requirements.txt && pip install itsdangerous
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

#holi
