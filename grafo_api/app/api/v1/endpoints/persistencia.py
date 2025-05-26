"""
Endpoints para persistência de grafos.
"""

from fastapi import APIRouter, HTTPException, Path, Query, Depends, Response
from typing import Dict, Any, Optional
import base64
import json

from app.schemas.grafo import ImportacaoGrafo, GrafoInfo
from app.core.session import get_grafo_service, get_persistencia_service
from app.services.grafo_service import GrafoService
from app.services.persistencia_service import PersistenciaService

# Cria o roteador
router = APIRouter()


@router.post("/importar", response_model=GrafoInfo, status_code=201)
def importar_grafo(
    importacao: ImportacaoGrafo,
    grafo_service: GrafoService = Depends(get_grafo_service),
    persistencia_service: PersistenciaService = Depends(get_persistencia_service)
):
    """
    Importa um grafo a partir de uma representação.
    
    - **nome**: Nome do grafo importado
    - **formato**: Formato da representação (graphml, gml, gexf, json, csv)
    - **conteudo**: Conteúdo da representação codificado em base64
    """
    # Verifica se o formato é válido
    formatos_validos = ["graphml", "gml", "gexf", "json", "csv"]
    if importacao.formato not in formatos_validos:
        raise HTTPException(status_code=400, detail=f"Formato '{importacao.formato}' inválido. Formatos válidos: {', '.join(formatos_validos)}")
    
    try:
        # Decodifica o conteúdo
        conteudo_bytes = base64.b64decode(importacao.conteudo)
        conteudo_str = conteudo_bytes.decode('utf-8')
        
        # Importa o grafo
        grafo_id = persistencia_service.importar_grafo(
            nome=importacao.nome,
            formato=importacao.formato,
            conteudo=conteudo_str
        )
        
        # Obtém os metadados do grafo importado
        metadados = grafo_service.obter_metadados(grafo_id)
        
        # Adiciona informações de número de vértices e arestas
        grafo_obj = grafo_service.obter_grafo(grafo_id)
        metadados["num_vertices"] = grafo_obj.numero_vertices()
        metadados["num_arestas"] = grafo_obj.numero_arestas()
        
        return metadados
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao importar grafo: {str(e)}")


@router.get("/{grafo_id}/exportar")
def exportar_grafo(
    grafo_id: str = Path(..., description="ID do grafo"),
    formato: str = Query("graphml", description="Formato de exportação"),
    grafo_service: GrafoService = Depends(get_grafo_service),
    persistencia_service: PersistenciaService = Depends(get_persistencia_service)
):
    """
    Exporta um grafo para um formato específico.
    
    - **grafo_id**: ID do grafo
    - **formato**: Formato de exportação (graphml, gml, gexf, json, csv)
    """
    # Verifica se o grafo existe
    grafo = grafo_service.obter_grafo(grafo_id)
    if not grafo:
        raise HTTPException(status_code=404, detail=f"Grafo com ID {grafo_id} não encontrado")
    
    # Verifica se o formato é válido
    formatos_validos = ["graphml", "gml", "gexf", "json", "csv"]
    if formato not in formatos_validos:
        raise HTTPException(status_code=400, detail=f"Formato '{formato}' inválido. Formatos válidos: {', '.join(formatos_validos)}")
    
    try:
        # Exporta o grafo
        conteudo = persistencia_service.exportar_grafo(grafo_id, formato)
        
        # Codifica o conteúdo em base64
        conteudo_bytes = conteudo.encode('utf-8')
        conteudo_base64 = base64.b64encode(conteudo_bytes).decode('utf-8')
        
        # Retorna o conteúdo codificado
        return {
            "grafo_id": grafo_id,
            "formato": formato,
            "conteudo": conteudo_base64
        }
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao exportar grafo: {str(e)}")


@router.get("/{grafo_id}/exportar/arquivo")
def exportar_grafo_arquivo(
    grafo_id: str = Path(..., description="ID do grafo"),
    formato: str = Query("graphml", description="Formato de exportação"),
    grafo_service: GrafoService = Depends(get_grafo_service),
    persistencia_service: PersistenciaService = Depends(get_persistencia_service)
):
    """
    Exporta um grafo para um arquivo.
    
    - **grafo_id**: ID do grafo
    - **formato**: Formato de exportação (graphml, gml, gexf, json, csv)
    """
    # Verifica se o grafo existe
    grafo = grafo_service.obter_grafo(grafo_id)
    if not grafo:
        raise HTTPException(status_code=404, detail=f"Grafo com ID {grafo_id} não encontrado")
    
    # Verifica se o formato é válido
    formatos_validos = ["graphml", "gml", "gexf", "json", "csv"]
    if formato not in formatos_validos:
        raise HTTPException(status_code=400, detail=f"Formato '{formato}' inválido. Formatos válidos: {', '.join(formatos_validos)}")
    
    try:
        # Exporta o grafo
        conteudo = persistencia_service.exportar_grafo(grafo_id, formato)
        
        # Define o nome do arquivo
        nome_arquivo = f"grafo_{grafo_id}.{formato}"
        
        # Define o tipo de conteúdo
        content_type = "application/octet-stream"
        
        # Retorna o arquivo para download
        return Response(
            content=conteudo,
            media_type=content_type,
            headers={"Content-Disposition": f"attachment; filename={nome_arquivo}"}
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao exportar grafo: {str(e)}")
