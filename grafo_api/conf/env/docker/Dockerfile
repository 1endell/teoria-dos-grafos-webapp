# ./conf/env/docker/Dockerfile

# Use uma imagem base do Python 3.9 slim
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Primeiro copia o requirements.txt para aproveitar o cache do Docker
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o conteúdo do projeto para o container
COPY . .

# Expõe a porta que será usada pelo FastAPI
EXPOSE 8000

# Comando para iniciar o servidor UVicorn com configurações específicas
CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "debug"]
