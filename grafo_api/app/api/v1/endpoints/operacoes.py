"""
Endpoints para operações entre grafos.
"""

from fastapi import APIRouter, HTTPException, Path, Depends
from typing import Dict, Any

from app.schemas.grafo import OperacaoGrafos, GrafoInfo
from app.services.grafo_service import GrafoService
from app.services.operacao_service import OperacaoService

# Cria o roteador
router = APIRouter()

# Instâncias dos serviços
grafo_service = GrafoService()
operacao_service = OperacaoService(grafo_service)


@router.post("/uniao", response_model=GrafoInfo)
def uniao_grafos(operacao: OperacaoGrafos):
    """
    Realiza a união de dois grafos.
    
    - **grafo_id1**: ID do primeiro grafo
    - **grafo_id2**: ID do segundo grafo
    - **nome_resultado**: Nome do grafo resultante (opcional)
    """
    try:
        grafo_id = operacao_service.uniao_grafos(
            grafo_id1=operacao.grafo_id1,
            grafo_id2=operacao.grafo_id2,
            nome_resultado=operacao.nome_resultado
        )
        
        # Obtém os metadados do grafo resultante
        metadados = grafo_service.obter_metadados(grafo_id)
        
        # Adiciona informações de número de vértices e arestas
        grafo_obj = grafo_service.obter_grafo(grafo_id)
        metadados["num_vertices"] = grafo_obj.numero_vertices()
        metadados["num_arestas"] = grafo_obj.numero_arestas()
        
        return metadados
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao realizar união: {str(e)}")


@router.post("/intersecao", response_model=GrafoInfo)
def intersecao_grafos(operacao: OperacaoGrafos):
    """
    Realiza a interseção de dois grafos.
    
    - **grafo_id1**: ID do primeiro grafo
    - **grafo_id2**: ID do segundo grafo
    - **nome_resultado**: Nome do grafo resultante (opcional)
    """
    try:
        grafo_id = operacao_service.intersecao_grafos(
            grafo_id1=operacao.grafo_id1,
            grafo_id2=operacao.grafo_id2,
            nome_resultado=operacao.nome_resultado
        )
        
        # Obtém os metadados do grafo resultante
        metadados = grafo_service.obter_metadados(grafo_id)
        
        # Adiciona informações de número de vértices e arestas
        grafo_obj = grafo_service.obter_grafo(grafo_id)
        metadados["num_vertices"] = grafo_obj.numero_vertices()
        metadados["num_arestas"] = grafo_obj.numero_arestas()
        
        return metadados
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao realizar interseção: {str(e)}")


@router.post("/diferenca", response_model=GrafoInfo)
def diferenca_grafos(operacao: OperacaoGrafos):
    """
    Realiza a diferença entre dois grafos.
    
    - **grafo_id1**: ID do primeiro grafo
    - **grafo_id2**: ID do segundo grafo
    - **nome_resultado**: Nome do grafo resultante (opcional)
    """
    try:
        grafo_id = operacao_service.diferenca_grafos(
            grafo_id1=operacao.grafo_id1,
            grafo_id2=operacao.grafo_id2,
            nome_resultado=operacao.nome_resultado
        )
        
        # Obtém os metadados do grafo resultante
        metadados = grafo_service.obter_metadados(grafo_id)
        
        # Adiciona informações de número de vértices e arestas
        grafo_obj = grafo_service.obter_grafo(grafo_id)
        metadados["num_vertices"] = grafo_obj.numero_vertices()
        metadados["num_arestas"] = grafo_obj.numero_arestas()
        
        return metadados
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao realizar diferença: {str(e)}")


@router.post("/diferenca-simetrica", response_model=GrafoInfo)
def diferenca_simetrica_grafos(operacao: OperacaoGrafos):
    """
    Realiza a diferença simétrica entre dois grafos.
    
    - **grafo_id1**: ID do primeiro grafo
    - **grafo_id2**: ID do segundo grafo
    - **nome_resultado**: Nome do grafo resultante (opcional)
    """
    try:
        grafo_id = operacao_service.diferenca_simetrica_grafos(
            grafo_id1=operacao.grafo_id1,
            grafo_id2=operacao.grafo_id2,
            nome_resultado=operacao.nome_resultado
        )
        
        # Obtém os metadados do grafo resultante
        metadados = grafo_service.obter_metadados(grafo_id)
        
        # Adiciona informações de número de vértices e arestas
        grafo_obj = grafo_service.obter_grafo(grafo_id)
        metadados["num_vertices"] = grafo_obj.numero_vertices()
        metadados["num_arestas"] = grafo_obj.numero_arestas()
        
        return metadados
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao realizar diferença simétrica: {str(e)}")


@router.post("/composicao", response_model=GrafoInfo)
def composicao_grafos(operacao: OperacaoGrafos):
    """
    Realiza a composição de dois grafos.
    
    - **grafo_id1**: ID do primeiro grafo
    - **grafo_id2**: ID do segundo grafo
    - **nome_resultado**: Nome do grafo resultante (opcional)
    """
    try:
        grafo_id = operacao_service.composicao_grafos(
            grafo_id1=operacao.grafo_id1,
            grafo_id2=operacao.grafo_id2,
            nome_resultado=operacao.nome_resultado
        )
        
        # Obtém os metadados do grafo resultante
        metadados = grafo_service.obter_metadados(grafo_id)
        
        # Adiciona informações de número de vértices e arestas
        grafo_obj = grafo_service.obter_grafo(grafo_id)
        metadados["num_vertices"] = grafo_obj.numero_vertices()
        metadados["num_arestas"] = grafo_obj.numero_arestas()
        
        return metadados
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao realizar composição: {str(e)}")
