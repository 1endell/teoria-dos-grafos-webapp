"""
Endpoints para algoritmos de grafos.
"""

from fastapi import APIRouter, HTTPException, Path, Query, Depends, status, Body
from typing import Dict, Any, Optional, List

from app.schemas.grafo import AlgoritmoInfo, AlgoritmoResultado
from app.core.session import get_grafo_service, get_algoritmo_service
from app.services.grafo_service import GrafoService
from app.services.algoritmo_service import AlgoritmoService

# Cria o roteador
router = APIRouter()


@router.get("/", response_model=List[AlgoritmoInfo])
def listar_algoritmos(
    algoritmo_service: AlgoritmoService = Depends(get_algoritmo_service)
):
    """
    Lista todos os algoritmos disponíveis.
    """
    return algoritmo_service.listar_algoritmos()


@router.get("/categorias", response_model=Dict[str, List[AlgoritmoInfo]])
def listar_algoritmos_por_categoria(
    algoritmo_service: AlgoritmoService = Depends(get_algoritmo_service)
):
    """
    Lista os algoritmos disponíveis agrupados por categoria.
    """
    return algoritmo_service.listar_algoritmos_por_categoria()


@router.get("/categoria/{categoria}", response_model=List[AlgoritmoInfo])
def listar_algoritmos_por_categoria_especifica(
    categoria: str = Path(..., description="Categoria de algoritmos"),
    algoritmo_service: AlgoritmoService = Depends(get_algoritmo_service)
):
    """
    Lista os algoritmos disponíveis de uma categoria específica.
    
    - **categoria**: Categoria de algoritmos (caminhos, coloracao, etc.)
    """
    # Lista os algoritmos da categoria
    algoritmos = algoritmo_service.listar_algoritmos_por_categoria_especifica(categoria)
    
    # Retorna lista vazia se não houver algoritmos na categoria, em vez de erro 404
    return algoritmos


@router.get("/algoritmo/{algoritmo_id}", response_model=AlgoritmoInfo)
def obter_algoritmo(
    algoritmo_id: str = Path(..., description="ID do algoritmo"),
    algoritmo_service: AlgoritmoService = Depends(get_algoritmo_service)
):
    """
    Obtém informações sobre um algoritmo específico.
    
    - **algoritmo_id**: ID do algoritmo
    """
    algoritmo = algoritmo_service.obter_algoritmo(algoritmo_id)
    if not algoritmo:
        raise HTTPException(status_code=404, detail=f"Algoritmo com ID {algoritmo_id} não encontrado")
    return algoritmo


@router.post("/executar/{algoritmo_id}/{grafo_id}", response_model=AlgoritmoResultado)
def executar_algoritmo(
    algoritmo_id: str = Path(..., description="ID do algoritmo"),
    grafo_id: str = Path(..., description="ID do grafo"),
    params: Dict[str, Any] = Body(default={"parametros": {}}, description="Parâmetros para o algoritmo"),
    algoritmo_service: AlgoritmoService = Depends(get_algoritmo_service),
    grafo_service: GrafoService = Depends(get_grafo_service)
):
    """
    Executa um algoritmo em um grafo.
    
    - **algoritmo_id**: ID do algoritmo
    - **grafo_id**: ID do grafo
    - **params**: Corpo da requisição contendo os parâmetros para o algoritmo (opcional)
    """
    # Extrai os parâmetros do corpo da requisição
    parametros = params.get("parametros", {})
    
    # Verifica se o grafo existe
    grafo = grafo_service.obter_grafo(grafo_id)
    if not grafo:
        raise HTTPException(status_code=404, detail=f"Grafo com ID {grafo_id} não encontrado")
    
    # Verifica se o algoritmo existe
    algoritmo = algoritmo_service.obter_algoritmo(algoritmo_id)
    if not algoritmo:
        raise HTTPException(status_code=404, detail=f"Algoritmo com ID {algoritmo_id} não encontrado")
    
    # Verifica se os parâmetros obrigatórios foram fornecidos
    parametros_obrigatorios = algoritmo.parametros_obrigatorios
    for param in parametros_obrigatorios:
        if param not in parametros:
            raise HTTPException(
                status_code=400,  # Código correto para parâmetros inválidos
                detail=f"Parâmetro obrigatório '{param}' não fornecido"
            )
    
    try:
        # Executa o algoritmo
        resultado = algoritmo_service.executar_algoritmo(algoritmo_id, grafo_id, parametros)
        return resultado
    except ValueError as e:
        # Erro de validação (parâmetros inválidos)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Erro interno
        raise HTTPException(status_code=500, detail=f"Erro ao executar algoritmo: {str(e)}")


@router.get("/{categoria}", response_model=List[AlgoritmoInfo])
def listar_algoritmos_por_categoria_especifica(
    categoria: str = Path(..., description="Categoria de algoritmos"),
    algoritmo_service: AlgoritmoService = Depends(get_algoritmo_service)
):
    """
    Lista os algoritmos disponíveis de uma categoria específica.
    
    - **categoria**: Categoria de algoritmos (caminhos, coloracao, etc.)
    """
    # Verifica se a categoria é um ID de algoritmo específico
    algoritmo = algoritmo_service.obter_algoritmo(categoria)
    if algoritmo:
        # Se for um ID de algoritmo, redireciona para o endpoint de obter algoritmo
        return [algoritmo]
    
    # Caso contrário, lista os algoritmos da categoria
    algoritmos = algoritmo_service.listar_algoritmos_por_categoria_especifica(categoria)
    
    # Retorna lista vazia se não houver algoritmos na categoria, em vez de erro 404
    return algoritmos
