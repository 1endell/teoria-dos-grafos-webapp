WORKDIR /app

# Copia os requirements primeiro
COPY requirements.txt .

# Instala dependências principais
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o conteúdo
COPY . .

# Instala o grafo_backend como pacote editável
RUN pip install -e .

EXPOSE 8000

CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "debug"]
