"""
Endpoints para execução de algoritmos em grafos.
"""

from fastapi import APIRouter, HTTPException, Path, Depends
from typing import List, Dict, Any, Optional

from app.schemas.grafo import AlgoritmoParams, ResultadoAlgoritmo
from app.services.algoritmo_service import AlgoritmoService
from app.services.grafo_service import GrafoService

# Cria o roteador
router = APIRouter()

# Instâncias dos serviços
grafo_service = GrafoService()
algoritmo_service = AlgoritmoService(grafo_service)


@router.get("/", response_model=List[Dict[str, Any]])
def listar_algoritmos(
    categoria: Optional[str] = None
):
    """
    Lista os algoritmos disponíveis.
    
    - **categoria**: Categoria de algoritmos a listar (opcional)
    """
    return algoritmo_service.listar_algoritmos(categoria)


@router.get("/{categoria}", response_model=List[Dict[str, Any]])
def listar_algoritmos_por_categoria(
    categoria: str = Path(..., description="Categoria de algoritmos")
):
    """
    Lista os algoritmos de uma categoria específica.
    
    - **categoria**: Categoria de algoritmos
    """
    algoritmos = algoritmo_service.listar_algoritmos(categoria)
    
    if not algoritmos:
        raise HTTPException(status_code=404, detail=f"Categoria '{categoria}' não encontrada")
    
    return algoritmos


@router.post("/{algoritmo_id}/{grafo_id}", response_model=ResultadoAlgoritmo)
def executar_algoritmo(
    algoritmo_id: str = Path(..., description="ID do algoritmo"),
    grafo_id: str = Path(..., description="ID do grafo"),
    params: AlgoritmoParams = AlgoritmoParams()
):
    """
    Executa um algoritmo em um grafo.
    
    - **algoritmo_id**: ID do algoritmo
    - **grafo_id**: ID do grafo
    - **parametros**: Parâmetros para o algoritmo (opcional)
    """
    try:
        resultado, tempo_execucao = algoritmo_service.executar_algoritmo(
            algoritmo_id=algoritmo_id,
            grafo_id=grafo_id,
            parametros=params.parametros
        )
        
        return {
            "algoritmo": algoritmo_id,
            "grafo_id": grafo_id,
            "resultado": resultado,
            "tempo_execucao": tempo_execucao
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao executar algoritmo: {str(e)}")
