"""
Endpoints para comparação entre grafos.
"""

from fastapi import APIRouter, HTTPException, Path, Query, Depends
from typing import Dict, Any, Optional, List

from app.schemas.grafo import ComparacaoGrafos, ResultadoComparacao
from app.core.session import get_grafo_service, get_comparacao_service
from app.services.grafo_service import GrafoService
from app.services.comparacao_service import ComparacaoService

# Cria o roteador
router = APIRouter()


@router.post("/", response_model=ResultadoComparacao)
def comparar_grafos(
    comparacao: ComparacaoGrafos,
    grafo_service: GrafoService = Depends(get_grafo_service),
    comparacao_service: ComparacaoService = Depends(get_comparacao_service)
):
    """
    Compara dois grafos usando a métrica especificada.
    
    - **grafo_id1**: ID do primeiro grafo
    - **grafo_id2**: ID do segundo grafo
    - **metrica**: Métrica de comparação (isomorfismo, similaridade, subgrafo)
    """
    # Verifica se os grafos existem
    grafo1 = grafo_service.obter_grafo(comparacao.grafo_id1)
    grafo2 = grafo_service.obter_grafo(comparacao.grafo_id2)
    
    if not grafo1 or not grafo2:
        raise HTTPException(status_code=404, detail="Um ou ambos os grafos não foram encontrados")
    
    # Verifica a métrica
    if comparacao.metrica not in ["isomorfismo", "similaridade", "subgrafo", "similaridade_espectral"]:
        raise HTTPException(status_code=404, detail=f"Métrica '{comparacao.metrica}' não suportada")
    
    try:
        # Realiza a comparação
        resultado = comparacao_service.comparar(
            comparacao.grafo_id1,
            comparacao.grafo_id2,
            comparacao.metrica
        )
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao comparar grafos: {str(e)}")


@router.get("/isomorfismo/{grafo_id1}/{grafo_id2}", response_model=ResultadoComparacao)
def verificar_isomorfismo(
    grafo_id1: str = Path(..., description="ID do primeiro grafo"),
    grafo_id2: str = Path(..., description="ID do segundo grafo"),
    grafo_service: GrafoService = Depends(get_grafo_service),
    comparacao_service: ComparacaoService = Depends(get_comparacao_service)
):
    """
    Verifica se dois grafos são isomorfos.
    
    - **grafo_id1**: ID do primeiro grafo
    - **grafo_id2**: ID do segundo grafo
    """
    # Verifica se os grafos existem
    grafo1 = grafo_service.obter_grafo(grafo_id1)
    grafo2 = grafo_service.obter_grafo(grafo_id2)
    
    if not grafo1 or not grafo2:
        raise HTTPException(status_code=404, detail="Um ou ambos os grafos não foram encontrados")
    
    try:
        # Realiza a verificação de isomorfismo
        resultado = comparacao_service.comparar(grafo_id1, grafo_id2, "isomorfismo")
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao verificar isomorfismo: {str(e)}")


@router.get("/similaridade/{grafo_id1}/{grafo_id2}", response_model=ResultadoComparacao)
def calcular_similaridade(
    grafo_id1: str = Path(..., description="ID do primeiro grafo"),
    grafo_id2: str = Path(..., description="ID do segundo grafo"),
    metrica: str = Query("espectral", description="Tipo de similaridade (espectral, jaccard, etc.)"),
    grafo_service: GrafoService = Depends(get_grafo_service),
    comparacao_service: ComparacaoService = Depends(get_comparacao_service)
):
    """
    Calcula a similaridade entre dois grafos.
    
    - **grafo_id1**: ID do primeiro grafo
    - **grafo_id2**: ID do segundo grafo
    - **metrica**: Tipo de similaridade (espectral, jaccard, etc.)
    """
    # Verifica se os grafos existem
    grafo1 = grafo_service.obter_grafo(grafo_id1)
    grafo2 = grafo_service.obter_grafo(grafo_id2)
    
    if not grafo1 or not grafo2:
        raise HTTPException(status_code=404, detail="Um ou ambos os grafos não foram encontrados")
    
    # Formata a métrica
    metrica_completa = f"similaridade_{metrica}"
    
    try:
        # Calcula a similaridade
        resultado = comparacao_service.comparar(grafo_id1, grafo_id2, metrica_completa)
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular similaridade: {str(e)}")


@router.get("/subgrafo/{grafo_id1}/{grafo_id2}", response_model=ResultadoComparacao)
def verificar_subgrafo(
    grafo_id1: str = Path(..., description="ID do primeiro grafo"),
    grafo_id2: str = Path(..., description="ID do segundo grafo"),
    grafo_service: GrafoService = Depends(get_grafo_service),
    comparacao_service: ComparacaoService = Depends(get_comparacao_service)
):
    """
    Verifica se o primeiro grafo é subgrafo do segundo.
    
    - **grafo_id1**: ID do primeiro grafo (potencial subgrafo)
    - **grafo_id2**: ID do segundo grafo (grafo maior)
    """
    # Verifica se os grafos existem
    grafo1 = grafo_service.obter_grafo(grafo_id1)
    grafo2 = grafo_service.obter_grafo(grafo_id2)
    
    if not grafo1 or not grafo2:
        raise HTTPException(status_code=404, detail="Um ou ambos os grafos não foram encontrados")
    
    try:
        # Verifica se é subgrafo
        resultado = comparacao_service.comparar(grafo_id1, grafo_id2, "subgrafo")
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao verificar subgrafo: {str(e)}")
