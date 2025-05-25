"""
Endpoints para visualização de grafos.
"""

from fastapi import APIRouter, HTTPException, Path, Depends
from typing import Dict, Any

from app.schemas.grafo import VisualizacaoGrafo, DadosVisualizacao
from app.services.grafo_service import GrafoService
from app.services.visualizacao_service import VisualizacaoService

# Cria o roteador
router = APIRouter()

# Instâncias dos serviços
grafo_service = GrafoService()
visualizacao_service = VisualizacaoService(grafo_service)


@router.post("/", response_model=DadosVisualizacao)
def visualizar_grafo(visualizacao: VisualizacaoGrafo):
    """
    Gera dados para visualização de um grafo.
    
    - **grafo_id**: ID do grafo
    - **layout**: Layout de visualização (spring, circular, spectral, etc.)
    - **incluir_atributos**: Se deve incluir atributos dos vértices e arestas
    """
    try:
        dados = visualizacao_service.gerar_dados_visualizacao(
            grafo_id=visualizacao.grafo_id,
            layout=visualizacao.layout,
            incluir_atributos=visualizacao.incluir_atributos
        )
        
        return dados
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar visualização: {str(e)}")


@router.get("/{grafo_id}", response_model=DadosVisualizacao)
def visualizar_grafo_por_id(
    grafo_id: str = Path(..., description="ID do grafo"),
    layout: str = "spring",
    incluir_atributos: bool = True
):
    """
    Gera dados para visualização de um grafo pelo ID.
    
    - **grafo_id**: ID do grafo
    - **layout**: Layout de visualização (spring, circular, spectral, etc.)
    - **incluir_atributos**: Se deve incluir atributos dos vértices e arestas
    """
    try:
        dados = visualizacao_service.gerar_dados_visualizacao(
            grafo_id=grafo_id,
            layout=layout,
            incluir_atributos=incluir_atributos
        )
        
        return dados
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar visualização: {str(e)}")


@router.get("/layouts", response_model=Dict[str, Any])
def listar_layouts():
    """
    Lista os layouts de visualização disponíveis.
    """
    return visualizacao_service.listar_layouts()


@router.get("/{grafo_id}/imagem")
def gerar_imagem_grafo(
    grafo_id: str = Path(..., description="ID do grafo"),
    layout: str = "spring",
    formato: str = "png",
    tamanho: str = "800x600"
):
    """
    Gera uma imagem de visualização do grafo.
    
    - **grafo_id**: ID do grafo
    - **layout**: Layout de visualização (spring, circular, spectral, etc.)
    - **formato**: Formato da imagem (png, svg, pdf)
    - **tamanho**: Tamanho da imagem em pixels (largura x altura)
    """
    try:
        # Extrai largura e altura do tamanho
        try:
            largura, altura = map(int, tamanho.split('x'))
        except:
            largura, altura = 800, 600
        
        # Gera a imagem
        imagem_bytes, content_type = visualizacao_service.gerar_imagem_grafo(
            grafo_id=grafo_id,
            layout=layout,
            formato=formato,
            largura=largura,
            altura=altura
        )
        
        # Obtém o nome do grafo
        metadados = grafo_service.obter_metadados(grafo_id)
        nome_grafo = metadados["nome"].replace(" ", "_")
        
        # Define o nome do arquivo
        filename = f"{nome_grafo}.{formato}"
        
        # Retorna a imagem
        from fastapi import Response
        return Response(
            content=imagem_bytes,
            media_type=content_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar imagem: {str(e)}")
