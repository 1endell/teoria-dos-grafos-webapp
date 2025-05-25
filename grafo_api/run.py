"""
Arquivo principal para execução da API de Teoria dos Grafos.
"""

import uvicorn
from app.main import create_app

# Cria a aplicação FastAPI
app = create_app()

if __name__ == "__main__":
    # Executa o servidor Uvicorn
    uvicorn.run(
        "run:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
