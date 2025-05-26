"""
Endpoints para manipulação de grafos.
"""

from fastapi import APIRouter, HTTPException, Path, Query, Depends, Response, status
from typing import Dict, List, Any, Optional

from app.schemas.grafo import (
    GrafoCreate, GrafoUpdate, Grafo, GrafoInfo, GrafoListResponse,
    VerticeCreate, VerticeUpdate, Vertice,
    ArestaCreate, ArestaUpdate, Aresta
)
from app.core.session import get_grafo_service
from app.services.grafo_service import GrafoService

# Cria o roteador
router = APIRouter()


@router.post("/", response_model=GrafoInfo, status_code=status.HTTP_201_CREATED)
def criar_grafo(
    grafo: GrafoCreate,
    grafo_service: GrafoService = Depends(get_grafo_service)
):
    """
    Cria um novo grafo.
    
    - **nome**: Nome do grafo
    - **direcionado**: Se o grafo é direcionado
    - **ponderado**: Se o grafo é ponderado
    - **bipartido**: Se o grafo é bipartido
    - **vertices**: Lista de vértices iniciais (opcional)
    - **arestas**: Lista de arestas iniciais (opcional)
    """
    # Cria o grafo
    grafo_id = grafo_service.criar_grafo(
        nome=grafo.nome,
        direcionado=grafo.direcionado,
        ponderado=grafo.ponderado,
        bipartido=grafo.bipartido
    )
    
    # Adiciona os vértices iniciais
    for v in grafo.vertices:
        grafo_service.adicionar_vertice(
            grafo_id=grafo_id,
            vertice_id=v.id,
            atributos=v.atributos,
            conjunto=v.conjunto if grafo.bipartido else None
        )
    
    # Adiciona as arestas iniciais
    for a in grafo.arestas:
        grafo_service.adicionar_aresta(
            grafo_id=grafo_id,
            origem=a.origem,
            destino=a.destino,
            peso=a.peso,
            atributos=a.atributos
        )
    
    # Retorna os metadados do grafo criado
    metadados = grafo_service.obter_metadados(grafo_id)
    
    # Adiciona informações de número de vértices e arestas
    grafo_obj = grafo_service.obter_grafo(grafo_id)
    metadados["num_vertices"] = grafo_obj.numero_vertices()
    metadados["num_arestas"] = grafo_obj.numero_arestas()
    
    return metadados


@router.get("/", response_model=GrafoListResponse)
def listar_grafos(
    skip: int = Query(0, description="Número de itens para pular"),
    limit: int = Query(100, description="Número máximo de itens para retornar"),
    grafo_service: GrafoService = Depends(get_grafo_service)
):
    """
    Lista todos os grafos.
    
    - **skip**: Número de itens para pular
    - **limit**: Número máximo de itens para retornar
    """
    # Obtém os metadados de todos os grafos
    metadados = grafo_service.listar_metadados(skip, limit)
    
    # Conta o número total de grafos
    total = len(grafo_service.grafos)
    
    # Adiciona informações de número de vértices e arestas
    for meta in metadados:
        grafo_id = meta["id"]
        grafo_obj = grafo_service.obter_grafo(grafo_id)
        meta["num_vertices"] = grafo_obj.numero_vertices()
        meta["num_arestas"] = grafo_obj.numero_arestas()
    
    # Retorna a resposta
    return {
        "total": total,
        "grafos": metadados
    }


@router.get("/{grafo_id}", response_model=Grafo)
def obter_grafo(
    grafo_id: str = Path(..., description="ID do grafo"),
    grafo_service: GrafoService = Depends(get_grafo_service)
):
    """
    Obtém um grafo pelo ID.
    
    - **grafo_id**: ID do grafo
    """
    # Verifica se o grafo existe
    grafo = grafo_service.obter_grafo(grafo_id)
    if not grafo:
        raise HTTPException(status_code=404, detail=f"Grafo com ID {grafo_id} não encontrado")
    
    # Serializa o grafo
    grafo_serializado = grafo_service.serializar_grafo(grafo_id)
    
    # Retorna o grafo serializado
    return grafo_serializado


@router.put("/{grafo_id}", response_model=GrafoInfo)
def atualizar_grafo(
    grafo: GrafoUpdate,
    grafo_id: str = Path(..., description="ID do grafo"),
    grafo_service: GrafoService = Depends(get_grafo_service)
):
    """
    Atualiza um grafo.
    
    - **grafo_id**: ID do grafo
    - **nome**: Novo nome do grafo (opcional)
    - **direcionado**: Se o grafo é direcionado (opcional)
    - **ponderado**: Se o grafo é ponderado (opcional)
    - **bipartido**: Se o grafo é bipartido (opcional)
    """
    # Verifica se o grafo existe
    if not grafo_service.obter_grafo(grafo_id):
        raise HTTPException(status_code=404, detail=f"Grafo com ID {grafo_id} não encontrado")
    
    # Atualiza o grafo
    grafo_service.atualizar_grafo(
        grafo_id=grafo_id,
        nome=grafo.nome,
        direcionado=grafo.direcionado,
        ponderado=grafo.ponderado,
        bipartido=grafo.bipartido
    )
    
    # Retorna os metadados do grafo atualizado
    metadados = grafo_service.obter_metadados(grafo_id)
    
    # Adiciona informações de número de vértices e arestas
    grafo_obj = grafo_service.obter_grafo(grafo_id)
    metadados["num_vertices"] = grafo_obj.numero_vertices()
    metadados["num_arestas"] = grafo_obj.numero_arestas()
    
    return metadados


@router.delete("/{grafo_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_grafo(
    grafo_id: str = Path(..., description="ID do grafo"),
    grafo_service: GrafoService = Depends(get_grafo_service)
):
    """
    Remove um grafo.
    
    - **grafo_id**: ID do grafo
    """
    # Verifica se o grafo existe
    if not grafo_service.obter_grafo(grafo_id):
        raise HTTPException(status_code=404, detail=f"Grafo com ID {grafo_id} não encontrado")
    
    # Remove o grafo
    grafo_service.remover_grafo(grafo_id)
    
    # Retorna resposta sem conteúdo
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{grafo_id}/vertices", response_model=Vertice)
def adicionar_vertice(
    vertice: VerticeCreate,
    grafo_id: str = Path(..., description="ID do grafo"),
    grafo_service: GrafoService = Depends(get_grafo_service)
):
    """
    Adiciona um vértice a um grafo.
    
    - **grafo_id**: ID do grafo
    - **id**: ID do vértice
    - **atributos**: Atributos do vértice (opcional)
    - **conjunto**: Conjunto do vértice para grafos bipartidos (opcional)
    """
    # Verifica se o grafo existe
    grafo = grafo_service.obter_grafo(grafo_id)
    if not grafo:
        raise HTTPException(status_code=404, detail=f"Grafo com ID {grafo_id} não encontrado")
    
    # Verifica se o vértice já existe
    if grafo.existe_vertice(vertice.id):
        raise HTTPException(status_code=400, detail=f"Vértice com ID {vertice.id} já existe no grafo")
    
    # Adiciona o vértice
    grafo_service.adicionar_vertice(
        grafo_id=grafo_id,
        vertice_id=vertice.id,
        atributos=vertice.atributos,
        conjunto=vertice.conjunto
    )
    
    # Obtém o grau do vértice
    grau = grafo.calcular_grau(vertice.id)
    
    # Retorna o vértice adicionado
    return {
        "id": vertice.id,
        "atributos": vertice.atributos,
        "grau": grau
    }


@router.get("/{grafo_id}/vertices", response_model=List[Vertice])
def listar_vertices(
    grafo_id: str = Path(..., description="ID do grafo"),
    grafo_service: GrafoService = Depends(get_grafo_service)
):
    """
    Lista todos os vértices de um grafo.
    
    - **grafo_id**: ID do grafo
    """
    # Verifica se o grafo existe
    grafo = grafo_service.obter_grafo(grafo_id)
    if not grafo:
        raise HTTPException(status_code=404, detail=f"Grafo com ID {grafo_id} não encontrado")
    
    # Obtém os vértices
    vertices = []
    for v in grafo.obter_vertices():
        atributos = grafo.obter_atributos_vertice(v)
        grau = grafo.calcular_grau(v)
        vertices.append({
            "id": v,
            "atributos": atributos,
            "grau": grau
        })
    
    # Retorna os vértices
    return vertices


@router.get("/{grafo_id}/vertices/{vertice_id}", response_model=Vertice)
def obter_vertice(
    grafo_id: str = Path(..., description="ID do grafo"),
    vertice_id: str = Path(..., description="ID do vértice"),
    grafo_service: GrafoService = Depends(get_grafo_service)
):
    """
    Obtém um vértice de um grafo.
    
    - **grafo_id**: ID do grafo
    - **vertice_id**: ID do vértice
    """
    # Verifica se o grafo existe
    grafo = grafo_service.obter_grafo(grafo_id)
    if not grafo:
        raise HTTPException(status_code=404, detail=f"Grafo com ID {grafo_id} não encontrado")
    
    # Verifica se o vértice existe
    if not grafo.existe_vertice(vertice_id):
        raise HTTPException(status_code=404, detail=f"Vértice com ID {vertice_id} não encontrado no grafo")
    
    # Obtém os atributos do vértice
    atributos = grafo.obter_atributos_vertice(vertice_id)
    
    # Obtém o grau do vértice
    grau = grafo.calcular_grau(vertice_id)
    
    # Retorna o vértice
    return {
        "id": vertice_id,
        "atributos": atributos,
        "grau": grau
    }


@router.put("/{grafo_id}/vertices/{vertice_id}", response_model=Vertice)
def atualizar_vertice(
    vertice: VerticeUpdate,
    grafo_id: str = Path(..., description="ID do grafo"),
    vertice_id: str = Path(..., description="ID do vértice"),
    grafo_service: GrafoService = Depends(get_grafo_service)
):
    """
    Atualiza um vértice de um grafo.
    
    - **grafo_id**: ID do grafo
    - **vertice_id**: ID do vértice
    - **atributos**: Novos atributos do vértice
    """
    # Verifica se o grafo existe
    grafo = grafo_service.obter_grafo(grafo_id)
    if not grafo:
        raise HTTPException(status_code=404, detail=f"Grafo com ID {grafo_id} não encontrado")
    
    # Verifica se o vértice existe
    if not grafo.existe_vertice(vertice_id):
        raise HTTPException(status_code=404, detail=f"Vértice com ID {vertice_id} não encontrado no grafo")
    
    # Atualiza os atributos do vértice
    grafo_service.atualizar_vertice(
        grafo_id=grafo_id,
        vertice_id=vertice_id,
        atributos=vertice.atributos
    )
    
    # Obtém os atributos atualizados do vértice
    atributos = grafo.obter_atributos_vertice(vertice_id)
    
    # Obtém o grau do vértice
    grau = grafo.calcular_grau(vertice_id)
    
    # Retorna o vértice atualizado
    return {
        "id": vertice_id,
        "atributos": atributos,
        "grau": grau
    }


@router.delete("/{grafo_id}/vertices/{vertice_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_vertice(
    grafo_id: str = Path(..., description="ID do grafo"),
    vertice_id: str = Path(..., description="ID do vértice"),
    grafo_service: GrafoService = Depends(get_grafo_service)
):
    """
    Remove um vértice de um grafo.
    
    - **grafo_id**: ID do grafo
    - **vertice_id**: ID do vértice
    """
    # Verifica se o grafo existe
    grafo = grafo_service.obter_grafo(grafo_id)
    if not grafo:
        raise HTTPException(status_code=404, detail=f"Grafo com ID {grafo_id} não encontrado")
    
    # Verifica se o vértice existe
    if not grafo.existe_vertice(vertice_id):
        raise HTTPException(status_code=404, detail=f"Vértice com ID {vertice_id} não encontrado no grafo")
    
    # Remove o vértice
    grafo_service.remover_vertice(grafo_id, vertice_id)
    
    # Retorna resposta sem conteúdo
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{grafo_id}/arestas", response_model=Aresta)
def adicionar_aresta(
    aresta: ArestaCreate,
    grafo_id: str = Path(..., description="ID do grafo"),
    grafo_service: GrafoService = Depends(get_grafo_service)
):
    """
    Adiciona uma aresta a um grafo.
    
    - **grafo_id**: ID do grafo
    - **origem**: ID do vértice de origem
    - **destino**: ID do vértice de destino
    - **peso**: Peso da aresta (opcional)
    - **atributos**: Atributos da aresta (opcional)
    """
    # Verifica se o grafo existe
    grafo = grafo_service.obter_grafo(grafo_id)
    if not grafo:
        raise HTTPException(status_code=404, detail=f"Grafo com ID {grafo_id} não encontrado")
    
    # Verifica se os vértices existem
    if not grafo.existe_vertice(aresta.origem):
        raise HTTPException(status_code=404, detail=f"Vértice de origem com ID {aresta.origem} não encontrado no grafo")
    
    if not grafo.existe_vertice(aresta.destino):
        raise HTTPException(status_code=404, detail=f"Vértice de destino com ID {aresta.destino} não encontrado no grafo")
    
    # Verifica se a aresta já existe
    if grafo.existe_aresta(aresta.origem, aresta.destino):
        raise HTTPException(status_code=400, detail=f"Aresta de {aresta.origem} para {aresta.destino} já existe no grafo")
    
    # Adiciona a aresta
    grafo_service.adicionar_aresta(
        grafo_id=grafo_id,
        origem=aresta.origem,
        destino=aresta.destino,
        peso=aresta.peso,
        atributos=aresta.atributos
    )
    
    # Retorna a aresta adicionada
    return {
        "origem": aresta.origem,
        "destino": aresta.destino,
        "peso": aresta.peso,
        "atributos": aresta.atributos
    }


@router.get("/{grafo_id}/arestas", response_model=List[Aresta])
def listar_arestas(
    grafo_id: str = Path(..., description="ID do grafo"),
    grafo_service: GrafoService = Depends(get_grafo_service)
):
    """
    Lista todas as arestas de um grafo.
    
    - **grafo_id**: ID do grafo
    """
    # Verifica se o grafo existe
    grafo = grafo_service.obter_grafo(grafo_id)
    if not grafo:
        raise HTTPException(status_code=404, detail=f"Grafo com ID {grafo_id} não encontrado")
    
    # Obtém as arestas
    arestas = []
    for u, v in grafo.obter_arestas():
        atributos = grafo.obter_atributos_aresta(u, v)
        peso = 1.0
        if hasattr(grafo, 'obter_peso_aresta'):
            peso = grafo.obter_peso_aresta(u, v)
        arestas.append({
            "origem": u,
            "destino": v,
            "peso": peso,
            "atributos": atributos
        })
    
    # Retorna as arestas
    return arestas


@router.get("/{grafo_id}/arestas/{origem}/{destino}", response_model=Aresta)
def obter_aresta(
    grafo_id: str = Path(..., description="ID do grafo"),
    origem: str = Path(..., description="ID do vértice de origem"),
    destino: str = Path(..., description="ID do vértice de destino"),
    grafo_service: GrafoService = Depends(get_grafo_service)
):
    """
    Obtém uma aresta de um grafo.
    
    - **grafo_id**: ID do grafo
    - **origem**: ID do vértice de origem
    - **destino**: ID do vértice de destino
    """
    # Verifica se o grafo existe
    grafo = grafo_service.obter_grafo(grafo_id)
    if not grafo:
        raise HTTPException(status_code=404, detail=f"Grafo com ID {grafo_id} não encontrado")
    
    # Verifica se a aresta existe
    if not grafo.existe_aresta(origem, destino):
        raise HTTPException(status_code=404, detail=f"Aresta de {origem} para {destino} não encontrada no grafo")
    
    # Obtém os atributos da aresta
    atributos = grafo.obter_atributos_aresta(origem, destino)
    
    # Obtém o peso da aresta
    peso = 1.0
    if hasattr(grafo, 'obter_peso_aresta'):
        peso = grafo.obter_peso_aresta(origem, destino)
    
    # Retorna a aresta
    return {
        "origem": origem,
        "destino": destino,
        "peso": peso,
        "atributos": atributos
    }


@router.put("/{grafo_id}/arestas/{origem}/{destino}", response_model=Aresta)
def atualizar_aresta(
    aresta: ArestaUpdate,
    grafo_id: str = Path(..., description="ID do grafo"),
    origem: str = Path(..., description="ID do vértice de origem"),
    destino: str = Path(..., description="ID do vértice de destino"),
    grafo_service: GrafoService = Depends(get_grafo_service)
):
    """
    Atualiza uma aresta de um grafo.
    
    - **grafo_id**: ID do grafo
    - **origem**: ID do vértice de origem
    - **destino**: ID do vértice de destino
    - **peso**: Novo peso da aresta (opcional)
    - **atributos**: Novos atributos da aresta (opcional)
    """
    # Verifica se o grafo existe
    grafo = grafo_service.obter_grafo(grafo_id)
    if not grafo:
        raise HTTPException(status_code=404, detail=f"Grafo com ID {grafo_id} não encontrado")
    
    # Verifica se a aresta existe
    if not grafo.existe_aresta(origem, destino):
        raise HTTPException(status_code=404, detail=f"Aresta de {origem} para {destino} não encontrada no grafo")
    
    # Atualiza a aresta
    grafo_service.atualizar_aresta(
        grafo_id=grafo_id,
        origem=origem,
        destino=destino,
        peso=aresta.peso,
        atributos=aresta.atributos
    )
    
    # Obtém os atributos atualizados da aresta
    atributos = grafo.obter_atributos_aresta(origem, destino)
    
    # Obtém o peso atualizado da aresta
    peso = 1.0
    if hasattr(grafo, 'obter_peso_aresta'):
        peso = grafo.obter_peso_aresta(origem, destino)
    
    # Retorna a aresta atualizada
    return {
        "origem": origem,
        "destino": destino,
        "peso": peso,
        "atributos": atributos
    }


@router.delete("/{grafo_id}/arestas/{origem}/{destino}", status_code=status.HTTP_204_NO_CONTENT)
def remover_aresta(
    grafo_id: str = Path(..., description="ID do grafo"),
    origem: str = Path(..., description="ID do vértice de origem"),
    destino: str = Path(..., description="ID do vértice de destino"),
    grafo_service: GrafoService = Depends(get_grafo_service)
):
    """
    Remove uma aresta de um grafo.
    
    - **grafo_id**: ID do grafo
    - **origem**: ID do vértice de origem
    - **destino**: ID do vértice de destino
    """
    # Verifica se o grafo existe
    grafo = grafo_service.obter_grafo(grafo_id)
    if not grafo:
        raise HTTPException(status_code=404, detail=f"Grafo com ID {grafo_id} não encontrado")
    
    # Verifica se a aresta existe
    if not grafo.existe_aresta(origem, destino):
        raise HTTPException(status_code=404, detail=f"Aresta de {origem} para {destino} não encontrada no grafo")
    
    # Remove a aresta
    grafo_service.remover_aresta(grafo_id, origem, destino)
    
    # Retorna resposta sem conteúdo
    return Response(status_code=status.HTTP_204_NO_CONTENT)
