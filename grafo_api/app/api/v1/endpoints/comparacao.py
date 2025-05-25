"""
Endpoints para comparação entre grafos.
"""

from fastapi import APIRouter, HTTPException, Path, Depends
from typing import Dict, Any

from app.schemas.grafo import ComparacaoGrafos, ResultadoComparacao
from app.services.grafo_service import GrafoService
from app.services.comparacao_service import ComparacaoService

# Cria o roteador
router = APIRouter()

# Instâncias dos serviços
grafo_service = GrafoService()
comparacao_service = ComparacaoService(grafo_service)


@router.post("/", response_model=ResultadoComparacao)
def comparar_grafos(comparacao: ComparacaoGrafos):
    """
    Compara dois grafos usando uma métrica específica.
    
    - **grafo_id1**: ID do primeiro grafo
    - **grafo_id2**: ID do segundo grafo
    - **metrica**: Métrica de comparação (isomorfismo, similaridade, subgrafo)
    """
    try:
        resultado, tempo_execucao = comparacao_service.comparar_grafos(
            grafo_id1=comparacao.grafo_id1,
            grafo_id2=comparacao.grafo_id2,
            metrica=comparacao.metrica
        )
        
        return {
            "grafo_id1": comparacao.grafo_id1,
            "grafo_id2": comparacao.grafo_id2,
            "metrica": comparacao.metrica,
            "resultado": resultado,
            "tempo_execucao": tempo_execucao
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao comparar grafos: {str(e)}")


@router.get("/isomorfismo/{grafo_id1}/{grafo_id2}", response_model=ResultadoComparacao)
def verificar_isomorfismo(
    grafo_id1: str = Path(..., description="ID do primeiro grafo"),
    grafo_id2: str = Path(..., description="ID do segundo grafo")
):
    """
    Verifica se dois grafos são isomorfos.
    
    - **grafo_id1**: ID do primeiro grafo
    - **grafo_id2**: ID do segundo grafo
    """
    try:
        resultado, tempo_execucao = comparacao_service.verificar_isomorfismo(
            grafo_id1=grafo_id1,
            grafo_id2=grafo_id2
        )
        
        return {
            "grafo_id1": grafo_id1,
            "grafo_id2": grafo_id2,
            "metrica": "isomorfismo",
            "resultado": resultado,
            "tempo_execucao": tempo_execucao
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao verificar isomorfismo: {str(e)}")


@router.get("/similaridade/{grafo_id1}/{grafo_id2}", response_model=ResultadoComparacao)
def calcular_similaridade(
    grafo_id1: str = Path(..., description="ID do primeiro grafo"),
    grafo_id2: str = Path(..., description="ID do segundo grafo"),
    metrica: str = "espectral"
):
    """
    Calcula a similaridade entre dois grafos.
    
    - **grafo_id1**: ID do primeiro grafo
    - **grafo_id2**: ID do segundo grafo
    - **metrica**: Métrica de similaridade (espectral, estrutural)
    """
    try:
        resultado, tempo_execucao = comparacao_service.calcular_similaridade(
            grafo_id1=grafo_id1,
            grafo_id2=grafo_id2,
            metrica=metrica
        )
        
        return {
            "grafo_id1": grafo_id1,
            "grafo_id2": grafo_id2,
            "metrica": f"similaridade_{metrica}",
            "resultado": resultado,
            "tempo_execucao": tempo_execucao
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular similaridade: {str(e)}")


@router.get("/subgrafo/{grafo_id1}/{grafo_id2}", response_model=ResultadoComparacao)
def verificar_subgrafo(
    grafo_id1: str = Path(..., description="ID do primeiro grafo"),
    grafo_id2: str = Path(..., description="ID do segundo grafo")
):
    """
    Verifica se o primeiro grafo é subgrafo do segundo.
    
    - **grafo_id1**: ID do grafo a verificar como subgrafo
    - **grafo_id2**: ID do grafo maior
    """
    try:
        resultado, tempo_execucao = comparacao_service.verificar_subgrafo(
            grafo_id1=grafo_id1,
            grafo_id2=grafo_id2
        )
        
        return {
            "grafo_id1": grafo_id1,
            "grafo_id2": grafo_id2,
            "metrica": "subgrafo",
            "resultado": resultado,
            "tempo_execucao": tempo_execucao
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao verificar subgrafo: {str(e)}")
