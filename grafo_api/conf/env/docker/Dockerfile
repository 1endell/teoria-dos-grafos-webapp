# grafo_api/conf/env/docker/Dockerfile

FROM python:3.9-slim

WORKDIR /app

# Copia primeiro o requirements.txt
COPY ./requirements.txt .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia TODO o conteúdo do grafo_api (incluindo grafo_backend)
COPY . .

# Configura o Python Path
ENV PYTHONPATH="${PYTHONPATH}:/app/grafo_backend"

EXPOSE 8000

CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "debug"]
