"""
Endpoints para operações entre grafos.
"""

from fastapi import APIRouter, HTTPException, Path, Depends
from typing import Dict, Any

from app.schemas.grafo import OperacaoGrafos, GrafoInfo
from app.core.session import get_grafo_service, get_operacao_service
from app.services.grafo_service import GrafoService
from app.services.operacao_service import OperacaoService

# Cria o roteador
router = APIRouter()


@router.post("/uniao", response_model=GrafoInfo)
def uniao_grafos(
    operacao: OperacaoGrafos,
    grafo_service: GrafoService = Depends(get_grafo_service),
    operacao_service: OperacaoService = Depends(get_operacao_service)
):
    """
    Realiza a união de dois grafos.
    
    - **grafo_id1**: ID do primeiro grafo
    - **grafo_id2**: ID do segundo grafo
    - **nome_resultado**: Nome do grafo resultante (opcional)
    """
    # Verifica se os grafos existem
    grafo1 = grafo_service.obter_grafo(operacao.grafo_id1)
    grafo2 = grafo_service.obter_grafo(operacao.grafo_id2)
    
    if not grafo1:
        raise HTTPException(status_code=404, detail=f"Grafo com ID {operacao.grafo_id1} não encontrado")
    
    if not grafo2:
        raise HTTPException(status_code=404, detail=f"Grafo com ID {operacao.grafo_id2} não encontrado")
    
    # Define o nome do grafo resultante
    nome_resultado = operacao.nome_resultado
    if not nome_resultado:
        nome_resultado = f"União de {grafo_service.obter_metadados(operacao.grafo_id1)['nome']} e {grafo_service.obter_metadados(operacao.grafo_id2)['nome']}"
    
    # Realiza a operação
    grafo_id = operacao_service.uniao(
        grafo_id1=operacao.grafo_id1,
        grafo_id2=operacao.grafo_id2,
        nome_resultado=nome_resultado
    )
    
    # Obtém os metadados do grafo resultante
    metadados = grafo_service.obter_metadados(grafo_id)
    
    # Adiciona informações de número de vértices e arestas
    grafo_obj = grafo_service.obter_grafo(grafo_id)
    metadados["num_vertices"] = grafo_obj.numero_vertices()
    metadados["num_arestas"] = grafo_obj.numero_arestas()
    
    return metadados


@router.post("/intersecao", response_model=GrafoInfo)
def intersecao_grafos(
    operacao: OperacaoGrafos,
    grafo_service: GrafoService = Depends(get_grafo_service),
    operacao_service: OperacaoService = Depends(get_operacao_service)
):
    """
    Realiza a interseção de dois grafos.
    
    - **grafo_id1**: ID do primeiro grafo
    - **grafo_id2**: ID do segundo grafo
    - **nome_resultado**: Nome do grafo resultante (opcional)
    """
    # Verifica se os grafos existem
    grafo1 = grafo_service.obter_grafo(operacao.grafo_id1)
    grafo2 = grafo_service.obter_grafo(operacao.grafo_id2)
    
    if not grafo1:
        raise HTTPException(status_code=404, detail=f"Grafo com ID {operacao.grafo_id1} não encontrado")
    
    if not grafo2:
        raise HTTPException(status_code=404, detail=f"Grafo com ID {operacao.grafo_id2} não encontrado")
    
    # Define o nome do grafo resultante
    nome_resultado = operacao.nome_resultado
    if not nome_resultado:
        nome_resultado = f"Interseção de {grafo_service.obter_metadados(operacao.grafo_id1)['nome']} e {grafo_service.obter_metadados(operacao.grafo_id2)['nome']}"
    
    # Realiza a operação
    grafo_id = operacao_service.intersecao(
        grafo_id1=operacao.grafo_id1,
        grafo_id2=operacao.grafo_id2,
        nome_resultado=nome_resultado
    )
    
    # Obtém os metadados do grafo resultante
    metadados = grafo_service.obter_metadados(grafo_id)
    
    # Adiciona informações de número de vértices e arestas
    grafo_obj = grafo_service.obter_grafo(grafo_id)
    metadados["num_vertices"] = grafo_obj.numero_vertices()
    metadados["num_arestas"] = grafo_obj.numero_arestas()
    
    return metadados


@router.post("/diferenca", response_model=GrafoInfo)
def diferenca_grafos(
    operacao: OperacaoGrafos,
    grafo_service: GrafoService = Depends(get_grafo_service),
    operacao_service: OperacaoService = Depends(get_operacao_service)
):
    """
    Realiza a diferença entre dois grafos.
    
    - **grafo_id1**: ID do primeiro grafo
    - **grafo_id2**: ID do segundo grafo
    - **nome_resultado**: Nome do grafo resultante (opcional)
    """
    # Verifica se os grafos existem
    grafo1 = grafo_service.obter_grafo(operacao.grafo_id1)
    grafo2 = grafo_service.obter_grafo(operacao.grafo_id2)
    
    if not grafo1:
        raise HTTPException(status_code=404, detail=f"Grafo com ID {operacao.grafo_id1} não encontrado")
    
    if not grafo2:
        raise HTTPException(status_code=404, detail=f"Grafo com ID {operacao.grafo_id2} não encontrado")
    
    # Define o nome do grafo resultante
    nome_resultado = operacao.nome_resultado
    if not nome_resultado:
        nome_resultado = f"Diferença de {grafo_service.obter_metadados(operacao.grafo_id1)['nome']} e {grafo_service.obter_metadados(operacao.grafo_id2)['nome']}"
    
    # Realiza a operação
    grafo_id = operacao_service.diferenca(
        grafo_id1=operacao.grafo_id1,
        grafo_id2=operacao.grafo_id2,
        nome_resultado=nome_resultado
    )
    
    # Obtém os metadados do grafo resultante
    metadados = grafo_service.obter_metadados(grafo_id)
    
    # Adiciona informações de número de vértices e arestas
    grafo_obj = grafo_service.obter_grafo(grafo_id)
    metadados["num_vertices"] = grafo_obj.numero_vertices()
    metadados["num_arestas"] = grafo_obj.numero_arestas()
    
    return metadados


@router.post("/diferenca-simetrica", response_model=GrafoInfo)
def diferenca_simetrica_grafos(
    operacao: OperacaoGrafos,
    grafo_service: GrafoService = Depends(get_grafo_service),
    operacao_service: OperacaoService = Depends(get_operacao_service)
):
    """
    Realiza a diferença simétrica entre dois grafos.
    
    - **grafo_id1**: ID do primeiro grafo
    - **grafo_id2**: ID do segundo grafo
    - **nome_resultado**: Nome do grafo resultante (opcional)
    """
    # Verifica se os grafos existem
    grafo1 = grafo_service.obter_grafo(operacao.grafo_id1)
    grafo2 = grafo_service.obter_grafo(operacao.grafo_id2)
    
    if not grafo1:
        raise HTTPException(status_code=404, detail=f"Grafo com ID {operacao.grafo_id1} não encontrado")
    
    if not grafo2:
        raise HTTPException(status_code=404, detail=f"Grafo com ID {operacao.grafo_id2} não encontrado")
    
    # Define o nome do grafo resultante
    nome_resultado = operacao.nome_resultado
    if not nome_resultado:
        nome_resultado = f"Diferença Simétrica de {grafo_service.obter_metadados(operacao.grafo_id1)['nome']} e {grafo_service.obter_metadados(operacao.grafo_id2)['nome']}"
    
    # Realiza a operação
    grafo_id = operacao_service.diferenca_simetrica(
        grafo_id1=operacao.grafo_id1,
        grafo_id2=operacao.grafo_id2,
        nome_resultado=nome_resultado
    )
    
    # Obtém os metadados do grafo resultante
    metadados = grafo_service.obter_metadados(grafo_id)
    
    # Adiciona informações de número de vértices e arestas
    grafo_obj = grafo_service.obter_grafo(grafo_id)
    metadados["num_vertices"] = grafo_obj.numero_vertices()
    metadados["num_arestas"] = grafo_obj.numero_arestas()
    
    return metadados


@router.post("/composicao", response_model=GrafoInfo)
def composicao_grafos(
    operacao: OperacaoGrafos,
    grafo_service: GrafoService = Depends(get_grafo_service),
    operacao_service: OperacaoService = Depends(get_operacao_service)
):
    """
    Realiza a composição de dois grafos.
    
    - **grafo_id1**: ID do primeiro grafo
    - **grafo_id2**: ID do segundo grafo
    - **nome_resultado**: Nome do grafo resultante (opcional)
    """
    # Verifica se os grafos existem
    grafo1 = grafo_service.obter_grafo(operacao.grafo_id1)
    grafo2 = grafo_service.obter_grafo(operacao.grafo_id2)
    
    if not grafo1:
        raise HTTPException(status_code=404, detail=f"Grafo com ID {operacao.grafo_id1} não encontrado")
    
    if not grafo2:
        raise HTTPException(status_code=404, detail=f"Grafo com ID {operacao.grafo_id2} não encontrado")
    
    # Define o nome do grafo resultante
    nome_resultado = operacao.nome_resultado
    if not nome_resultado:
        nome_resultado = f"Composição de {grafo_service.obter_metadados(operacao.grafo_id1)['nome']} e {grafo_service.obter_metadados(operacao.grafo_id2)['nome']}"
    
    # Realiza a operação
    grafo_id = operacao_service.composicao(
        grafo_id1=operacao.grafo_id1,
        grafo_id2=operacao.grafo_id2,
        nome_resultado=nome_resultado
    )
    
    # Obtém os metadados do grafo resultante
    metadados = grafo_service.obter_metadados(grafo_id)
    
    # Adiciona informações de número de vértices e arestas
    grafo_obj = grafo_service.obter_grafo(grafo_id)
    metadados["num_vertices"] = grafo_obj.numero_vertices()
    metadados["num_arestas"] = grafo_obj.numero_arestas()
    
    return metadados
