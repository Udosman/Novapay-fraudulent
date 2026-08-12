FROM python:3.11-slim

WORKDIR /app

COPY Requirements-docker.txt .

RUN pip install --no-cache-dir -r Requirements-docker.txt

COPY api ./api
COPY Models ./models

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]