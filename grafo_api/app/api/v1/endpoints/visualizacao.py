"""
Endpoints para visualização de grafos.
"""

from fastapi import APIRouter, HTTPException, Path, Query, Depends
from typing import Dict, Any, Optional, List

from app.schemas.grafo import VisualizacaoGrafo, DadosVisualizacao
from app.core.session import get_grafo_service, get_visualizacao_service
from app.services.grafo_service import GrafoService
from app.services.visualizacao_service import VisualizacaoService

# Cria o roteador
router = APIRouter()


@router.get("/layouts", response_model=List[str])
def listar_layouts(
    visualizacao_service: VisualizacaoService = Depends(get_visualizacao_service)
):
    """
    Lista os layouts de visualização disponíveis.
    """
    try:
        # Lista os layouts disponíveis
        layouts = visualizacao_service.listar_layouts()
        return layouts
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar layouts: {str(e)}")


@router.get("/{grafo_id}/imagem", response_model=Dict[str, Any])
def gerar_imagem_grafo(
    grafo_id: str = Path(..., description="ID do grafo"),
    formato: str = Query("png", description="Formato da imagem (png, svg, etc.)"),
    layout: str = Query("spring", description="Layout de visualização"),
    grafo_service: GrafoService = Depends(get_grafo_service),
    visualizacao_service: VisualizacaoService = Depends(get_visualizacao_service)
):
    """
    Gera uma imagem de um grafo.
    
    - **grafo_id**: ID do grafo
    - **formato**: Formato da imagem (png, svg, etc.)
    - **layout**: Layout de visualização
    """
    # Verifica se o grafo existe
    grafo = grafo_service.obter_grafo(grafo_id)
    if not grafo:
        raise HTTPException(status_code=404, detail=f"Grafo com ID {grafo_id} não encontrado")
    
    try:
        # Gera a imagem
        imagem = visualizacao_service.gerar_imagem(grafo_id, formato, layout)
        return imagem
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar imagem: {str(e)}")


@router.get("/{grafo_id}", response_model=DadosVisualizacao)
def visualizar_grafo(
    grafo_id: str = Path(..., description="ID do grafo"),
    layout: str = Query("spring", description="Layout de visualização"),
    incluir_atributos: bool = Query(True, description="Incluir atributos dos vértices e arestas"),
    grafo_service: GrafoService = Depends(get_grafo_service),
    visualizacao_service: VisualizacaoService = Depends(get_visualizacao_service)
):
    """
    Obtém dados para visualização de um grafo.
    
    - **grafo_id**: ID do grafo
    - **layout**: Layout de visualização (spring, circular, etc.)
    - **incluir_atributos**: Incluir atributos dos vértices e arestas
    """
    # Verifica se o grafo existe
    grafo = grafo_service.obter_grafo(grafo_id)
    if not grafo:
        raise HTTPException(status_code=404, detail=f"Grafo com ID {grafo_id} não encontrado")
    
    try:
        # Obtém os dados de visualização
        dados = visualizacao_service.visualizar_grafo(grafo_id, layout, incluir_atributos)
        return dados
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao visualizar grafo: {str(e)}")
