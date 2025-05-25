"""
Endpoints para gerenciamento de grafos.
"""

from fastapi import APIRouter, HTTPException, Query, Path, Depends
from typing import List, Dict, Any, Optional

from app.schemas.grafo import (
    GrafoCreate, GrafoUpdate, Grafo, GrafoInfo, GrafoListResponse,
    VerticeCreate, VerticeUpdate, Vertice,
    ArestaCreate, ArestaUpdate, Aresta
)
from app.services.grafo_service import GrafoService

# Cria o roteador
router = APIRouter()

# Instância do serviço de grafos
grafo_service = GrafoService()


@router.post("/", response_model=GrafoInfo, status_code=201)
def criar_grafo(grafo: GrafoCreate):
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
    
    # Adiciona os vértices
    for v in grafo.vertices:
        grafo_service.adicionar_vertice(
            grafo_id=grafo_id,
            vertice_id=v.id,
            atributos=v.atributos,
            conjunto=v.conjunto
        )
    
    # Adiciona as arestas
    for a in grafo.arestas:
        grafo_service.adicionar_aresta(
            grafo_id=grafo_id,
            origem=a.origem,
            destino=a.destino,
            peso=a.peso,
            atributos=a.atributos
        )
    
    # Obtém os metadados do grafo criado
    metadados = grafo_service.obter_metadados(grafo_id)
    if not metadados:
        raise HTTPException(status_code=500, detail="Erro ao criar grafo")
    
    # Adiciona informações de número de vértices e arestas
    grafo_obj = grafo_service.obter_grafo(grafo_id)
    metadados["num_vertices"] = grafo_obj.numero_vertices()
    metadados["num_arestas"] = grafo_obj.numero_arestas()
    
    return metadados


@router.get("/", response_model=GrafoListResponse)
def listar_grafos(
    skip: int = Query(0, ge=0, description="Número de grafos a pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de grafos a retornar")
):
    """
    Lista os grafos disponíveis.
    
    - **skip**: Número de grafos a pular
    - **limit**: Número máximo de grafos a retornar
    """
    total, grafos = grafo_service.listar_grafos(skip=skip, limit=limit)
    return {"total": total, "grafos": grafos}


@router.get("/{grafo_id}", response_model=Grafo)
def obter_grafo(
    grafo_id: str = Path(..., description="ID do grafo")
):
    """
    Obtém um grafo pelo ID.
    
    - **grafo_id**: ID do grafo
    """
    try:
        grafo_serializado = grafo_service.serializar_grafo(grafo_id)
        return grafo_serializado
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{grafo_id}", response_model=GrafoInfo)
def atualizar_grafo(
    grafo: GrafoUpdate,
    grafo_id: str = Path(..., description="ID do grafo")
):
    """
    Atualiza um grafo.
    
    - **grafo_id**: ID do grafo
    - **nome**: Novo nome do grafo (opcional)
    - **direcionado**: Se o grafo é direcionado (opcional)
    - **ponderado**: Se o grafo é ponderado (opcional)
    - **bipartido**: Se o grafo é bipartido (opcional)
    """
    # Atualiza o grafo
    sucesso = grafo_service.atualizar_grafo(
        grafo_id=grafo_id,
        nome=grafo.nome,
        direcionado=grafo.direcionado,
        ponderado=grafo.ponderado,
        bipartido=grafo.bipartido
    )
    
    if not sucesso:
        raise HTTPException(status_code=404, detail=f"Grafo com ID {grafo_id} não encontrado")
    
    # Obtém os metadados do grafo atualizado
    metadados = grafo_service.obter_metadados(grafo_id)
    
    # Adiciona informações de número de vértices e arestas
    grafo_obj = grafo_service.obter_grafo(grafo_id)
    metadados["num_vertices"] = grafo_obj.numero_vertices()
    metadados["num_arestas"] = grafo_obj.numero_arestas()
    
    return metadados


@router.delete("/{grafo_id}", status_code=204)
def excluir_grafo(
    grafo_id: str = Path(..., description="ID do grafo")
):
    """
    Exclui um grafo.
    
    - **grafo_id**: ID do grafo
    """
    sucesso = grafo_service.excluir_grafo(grafo_id)
    
    if not sucesso:
        raise HTTPException(status_code=404, detail=f"Grafo com ID {grafo_id} não encontrado")


@router.post("/{grafo_id}/vertices", response_model=Vertice)
def adicionar_vertice(
    vertice: VerticeCreate,
    grafo_id: str = Path(..., description="ID do grafo")
):
    """
    Adiciona um vértice a um grafo.
    
    - **grafo_id**: ID do grafo
    - **id**: ID do vértice
    - **atributos**: Atributos do vértice (opcional)
    - **conjunto**: Conjunto do vértice para grafos bipartidos (opcional)
    """
    sucesso = grafo_service.adicionar_vertice(
        grafo_id=grafo_id,
        vertice_id=vertice.id,
        atributos=vertice.atributos,
        conjunto=vertice.conjunto
    )
    
    if not sucesso:
        raise HTTPException(status_code=404, detail=f"Grafo com ID {grafo_id} não encontrado")
    
    # Obtém informações do vértice adicionado
    vertice_info = grafo_service.obter_vertice(grafo_id, vertice.id)
    
    if not vertice_info:
        raise HTTPException(status_code=500, detail="Erro ao adicionar vértice")
    
    return vertice_info


@router.get("/{grafo_id}/vertices/{vertice_id}", response_model=Vertice)
def obter_vertice(
    grafo_id: str = Path(..., description="ID do grafo"),
    vertice_id: str = Path(..., description="ID do vértice")
):
    """
    Obtém informações de um vértice.
    
    - **grafo_id**: ID do grafo
    - **vertice_id**: ID do vértice
    """
    vertice_info = grafo_service.obter_vertice(grafo_id, vertice_id)
    
    if not vertice_info:
        raise HTTPException(status_code=404, detail=f"Vértice com ID {vertice_id} não encontrado no grafo {grafo_id}")
    
    return vertice_info


@router.put("/{grafo_id}/vertices/{vertice_id}", response_model=Vertice)
def atualizar_vertice(
    vertice: VerticeUpdate,
    grafo_id: str = Path(..., description="ID do grafo"),
    vertice_id: str = Path(..., description="ID do vértice")
):
    """
    Atualiza os atributos de um vértice.
    
    - **grafo_id**: ID do grafo
    - **vertice_id**: ID do vértice
    - **atributos**: Novos atributos do vértice
    """
    sucesso = grafo_service.atualizar_vertice(
        grafo_id=grafo_id,
        vertice_id=vertice_id,
        atributos=vertice.atributos
    )
    
    if not sucesso:
        raise HTTPException(status_code=404, detail=f"Vértice com ID {vertice_id} não encontrado no grafo {grafo_id}")
    
    # Obtém informações do vértice atualizado
    vertice_info = grafo_service.obter_vertice(grafo_id, vertice_id)
    
    if not vertice_info:
        raise HTTPException(status_code=500, detail="Erro ao atualizar vértice")
    
    return vertice_info


@router.delete("/{grafo_id}/vertices/{vertice_id}", status_code=204)
def remover_vertice(
    grafo_id: str = Path(..., description="ID do grafo"),
    vertice_id: str = Path(..., description="ID do vértice")
):
    """
    Remove um vértice de um grafo.
    
    - **grafo_id**: ID do grafo
    - **vertice_id**: ID do vértice
    """
    sucesso = grafo_service.remover_vertice(grafo_id, vertice_id)
    
    if not sucesso:
        raise HTTPException(status_code=404, detail=f"Vértice com ID {vertice_id} não encontrado no grafo {grafo_id}")


@router.post("/{grafo_id}/arestas", response_model=Aresta)
def adicionar_aresta(
    aresta: ArestaCreate,
    grafo_id: str = Path(..., description="ID do grafo")
):
    """
    Adiciona uma aresta a um grafo.
    
    - **grafo_id**: ID do grafo
    - **origem**: Vértice de origem
    - **destino**: Vértice de destino
    - **peso**: Peso da aresta (opcional, padrão: 1.0)
    - **atributos**: Atributos da aresta (opcional)
    """
    sucesso = grafo_service.adicionar_aresta(
        grafo_id=grafo_id,
        origem=aresta.origem,
        destino=aresta.destino,
        peso=aresta.peso,
        atributos=aresta.atributos
    )
    
    if not sucesso:
        raise HTTPException(status_code=404, detail=f"Grafo com ID {grafo_id} não encontrado ou vértices não existem")
    
    # Obtém informações da aresta adicionada
    aresta_info = grafo_service.obter_aresta(grafo_id, aresta.origem, aresta.destino)
    
    if not aresta_info:
        raise HTTPException(status_code=500, detail="Erro ao adicionar aresta")
    
    return aresta_info


@router.get("/{grafo_id}/arestas/{origem}/{destino}", response_model=Aresta)
def obter_aresta(
    grafo_id: str = Path(..., description="ID do grafo"),
    origem: str = Path(..., description="Vértice de origem"),
    destino: str = Path(..., description="Vértice de destino")
):
    """
    Obtém informações de uma aresta.
    
    - **grafo_id**: ID do grafo
    - **origem**: Vértice de origem
    - **destino**: Vértice de destino
    """
    aresta_info = grafo_service.obter_aresta(grafo_id, origem, destino)
    
    if not aresta_info:
        raise HTTPException(status_code=404, detail=f"Aresta ({origem}, {destino}) não encontrada no grafo {grafo_id}")
    
    return aresta_info


@router.put("/{grafo_id}/arestas/{origem}/{destino}", response_model=Aresta)
def atualizar_aresta(
    aresta: ArestaUpdate,
    grafo_id: str = Path(..., description="ID do grafo"),
    origem: str = Path(..., description="Vértice de origem"),
    destino: str = Path(..., description="Vértice de destino")
):
    """
    Atualiza uma aresta.
    
    - **grafo_id**: ID do grafo
    - **origem**: Vértice de origem
    - **destino**: Vértice de destino
    - **peso**: Novo peso da aresta (opcional)
    - **atributos**: Novos atributos da aresta (opcional)
    """
    sucesso = grafo_service.atualizar_aresta(
        grafo_id=grafo_id,
        origem=origem,
        destino=destino,
        peso=aresta.peso,
        atributos=aresta.atributos
    )
    
    if not sucesso:
        raise HTTPException(status_code=404, detail=f"Aresta ({origem}, {destino}) não encontrada no grafo {grafo_id}")
    
    # Obtém informações da aresta atualizada
    aresta_info = grafo_service.obter_aresta(grafo_id, origem, destino)
    
    if not aresta_info:
        raise HTTPException(status_code=500, detail="Erro ao atualizar aresta")
    
    return aresta_info


@router.delete("/{grafo_id}/arestas/{origem}/{destino}", status_code=204)
def remover_aresta(
    grafo_id: str = Path(..., description="ID do grafo"),
    origem: str = Path(..., description="Vértice de origem"),
    destino: str = Path(..., description="Vértice de destino")
):
    """
    Remove uma aresta de um grafo.
    
    - **grafo_id**: ID do grafo
    - **origem**: Vértice de origem
    - **destino**: Vértice de destino
    """
    sucesso = grafo_service.remover_aresta(grafo_id, origem, destino)
    
    if not sucesso:
        raise HTTPException(status_code=404, detail=f"Aresta ({origem}, {destino}) não encontrada no grafo {grafo_id}")
