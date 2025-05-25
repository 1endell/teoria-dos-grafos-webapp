"""
Roteadores da API v1.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import grafos, algoritmos, operacoes, persistencia, comparacao, visualizacao

# Cria o roteador principal da API v1
api_router = APIRouter()

# Inclui os roteadores dos endpoints
api_router.include_router(grafos.router, prefix="/grafos", tags=["grafos"])
api_router.include_router(algoritmos.router, prefix="/algoritmos", tags=["algoritmos"])
api_router.include_router(operacoes.router, prefix="/operacoes", tags=["operacoes"])
api_router.include_router(persistencia.router, prefix="/persistencia", tags=["persistencia"])
api_router.include_router(comparacao.router, prefix="/comparacao", tags=["comparacao"])
api_router.include_router(visualizacao.router, prefix="/visualizacao", tags=["visualizacao"])
