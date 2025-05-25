"""
Endpoints para persistência de grafos em diferentes formatos.
"""

from fastapi import APIRouter, HTTPException, Path, Depends, UploadFile, File, Response
from typing import Dict, Any, Optional
import base64
import io

from app.schemas.grafo import ImportacaoGrafo, ExportacaoGrafo, GrafoInfo
from app.services.grafo_service import GrafoService
from app.services.persistencia_service import PersistenciaService

# Cria o roteador
router = APIRouter()

# Instâncias dos serviços
grafo_service = GrafoService()
persistencia_service = PersistenciaService(grafo_service)


@router.post("/importar", response_model=GrafoInfo)
def importar_grafo(importacao: ImportacaoGrafo):
    """
    Importa um grafo a partir de uma representação em um formato específico.
    
    - **nome**: Nome do grafo a ser criado
    - **formato**: Formato do grafo (graphml, gml, gexf, json, csv)
    - **conteudo**: Conteúdo do arquivo codificado em base64
    """
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


@router.post("/importar/arquivo", response_model=GrafoInfo)
def importar_grafo_arquivo(
    nome: str,
    formato: str,
    arquivo: UploadFile = File(...)
):
    """
    Importa um grafo a partir de um arquivo.
    
    - **nome**: Nome do grafo a ser criado
    - **formato**: Formato do grafo (graphml, gml, gexf, json, csv)
    - **arquivo**: Arquivo contendo a representação do grafo
    """
    try:
        # Lê o conteúdo do arquivo
        conteudo = arquivo.file.read()
        conteudo_str = conteudo.decode('utf-8')
        
        # Importa o grafo
        grafo_id = persistencia_service.importar_grafo(
            nome=nome,
            formato=formato,
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


@router.get("/{grafo_id}/exportar", response_model=Dict[str, Any])
def exportar_grafo(
    grafo_id: str = Path(..., description="ID do grafo"),
    formato: str = "graphml"
):
    """
    Exporta um grafo para um formato específico.
    
    - **grafo_id**: ID do grafo
    - **formato**: Formato de exportação (graphml, gml, gexf, json, csv)
    """
    try:
        # Exporta o grafo
        conteudo = persistencia_service.exportar_grafo(
            grafo_id=grafo_id,
            formato=formato
        )
        
        # Codifica o conteúdo em base64
        conteudo_bytes = conteudo.encode('utf-8')
        conteudo_base64 = base64.b64encode(conteudo_bytes).decode('utf-8')
        
        return {
            "grafo_id": grafo_id,
            "formato": formato,
            "conteudo": conteudo_base64
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao exportar grafo: {str(e)}")


@router.get("/{grafo_id}/exportar/arquivo")
def exportar_grafo_arquivo(
    grafo_id: str = Path(..., description="ID do grafo"),
    formato: str = "graphml"
):
    """
    Exporta um grafo para um arquivo.
    
    - **grafo_id**: ID do grafo
    - **formato**: Formato de exportação (graphml, gml, gexf, json, csv)
    """
    try:
        # Exporta o grafo
        conteudo = persistencia_service.exportar_grafo(
            grafo_id=grafo_id,
            formato=formato
        )
        
        # Prepara o arquivo para download
        conteudo_bytes = conteudo.encode('utf-8')
        
        # Define o tipo de conteúdo e nome do arquivo
        content_type = "application/xml"
        if formato == "json":
            content_type = "application/json"
        elif formato == "csv":
            content_type = "text/csv"
        
        # Obtém o nome do grafo
        metadados = grafo_service.obter_metadados(grafo_id)
        nome_grafo = metadados["nome"].replace(" ", "_")
        
        # Define o nome do arquivo
        filename = f"{nome_grafo}.{formato}"
        
        # Retorna o arquivo para download
        return Response(
            content=conteudo_bytes,
            media_type=content_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao exportar grafo: {str(e)}")
