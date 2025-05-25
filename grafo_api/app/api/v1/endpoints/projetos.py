"""
Endpoints para gerenciamento de projetos de estudo de teoria dos grafos.

Este módulo implementa os endpoints para criar, gerenciar, importar e exportar
projetos de estudo, com suporte a isolamento por sessão.
"""

from typing import Dict, List, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Request, Response, File, UploadFile, Form
from fastapi.responses import FileResponse, StreamingResponse
import json
import io
import base64
from datetime import datetime

from app.schemas.projeto import (
    ProjetoCreate, ProjetoInfo, ProjetoUpdate, ProjetoExport,
    ProjetoImport, ProjetoList, NotaCreate, TagUpdate
)
from app.services.projeto_service import GerenciadorProjetos
from app.services.relatorio_service import RelatorioGrafoPDF

router = APIRouter()

# Dependência para obter o gerenciador de projetos
def get_projeto_service(request: Request):
    return request.app.state.projeto_service

# Dependência para obter o serviço de relatórios
def get_relatorio_service(request: Request):
    return request.app.state.relatorio_service

# Dependência para obter o ID da sessão atual
def get_session_id(request: Request) -> str:
    return request.state.session_id


@router.post("/", response_model=ProjetoInfo, status_code=201)
def criar_projeto(
    projeto: ProjetoCreate,
    request: Request,
    session_id: str = Depends(get_session_id),
    projeto_service: GerenciadorProjetos = Depends(get_projeto_service)
):
    """
    Cria um novo projeto de estudo na sessão atual.
    """
    # Cria o projeto
    projeto_id = projeto_service.criar_projeto(
        titulo=projeto.titulo,
        descricao=projeto.descricao,
        autor=projeto.autor
    )
    
    # Associa o projeto à sessão atual
    request.app.state.session_storage.store_data(
        session_id=session_id,
        data_type="projetos",
        data_id=projeto_id,
        data={"projeto_id": projeto_id}
    )
    
    # Obtém o projeto criado
    projeto_obj = projeto_service.obter_projeto(projeto_id)
    if not projeto_obj:
        raise HTTPException(status_code=500, detail="Erro ao criar projeto")
    
    # Retorna os metadados do projeto
    return projeto_obj.obter_metadados()


@router.get("/", response_model=ProjetoList)
def listar_projetos(
    request: Request,
    session_id: str = Depends(get_session_id),
    projeto_service: GerenciadorProjetos = Depends(get_projeto_service),
    skip: int = 0,
    limit: int = 100
):
    """
    Lista todos os projetos disponíveis na sessão atual.
    """
    # Obtém os projetos associados à sessão
    projetos_sessao = request.app.state.session_storage.list_data(
        session_id=session_id,
        data_type="projetos"
    )
    
    # Filtra os projetos pelo ID da sessão
    projetos_ids = [data["projeto_id"] for data in projetos_sessao.values()]
    
    # Obtém os metadados de cada projeto
    projetos = []
    for projeto_id in projetos_ids:
        projeto = projeto_service.obter_projeto(projeto_id)
        if projeto:
            projetos.append(projeto.obter_metadados())
    
    # Aplica paginação
    total = len(projetos)
    projetos = projetos[skip:skip+limit]
    
    return {"total": total, "projetos": projetos}


@router.get("/{projeto_id}", response_model=ProjetoInfo)
def obter_projeto(
    projeto_id: str,
    request: Request,
    session_id: str = Depends(get_session_id),
    projeto_service: GerenciadorProjetos = Depends(get_projeto_service)
):
    """
    Obtém os detalhes de um projeto específico.
    """
    # Verifica se o projeto pertence à sessão atual
    projeto_data = request.app.state.session_storage.get_data(
        session_id=session_id,
        data_type="projetos",
        data_id=projeto_id
    )
    
    if not projeto_data:
        raise HTTPException(status_code=404, detail="Projeto não encontrado na sessão atual")
    
    # Obtém o projeto
    projeto = projeto_service.obter_projeto(projeto_id)
    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    
    # Retorna os metadados do projeto
    return projeto.obter_metadados()


@router.put("/{projeto_id}", response_model=ProjetoInfo)
def atualizar_projeto(
    projeto_id: str,
    projeto_update: ProjetoUpdate,
    request: Request,
    session_id: str = Depends(get_session_id),
    projeto_service: GerenciadorProjetos = Depends(get_projeto_service)
):
    """
    Atualiza os metadados de um projeto.
    """
    # Verifica se o projeto pertence à sessão atual
    projeto_data = request.app.state.session_storage.get_data(
        session_id=session_id,
        data_type="projetos",
        data_id=projeto_id
    )
    
    if not projeto_data:
        raise HTTPException(status_code=404, detail="Projeto não encontrado na sessão atual")
    
    # Obtém o projeto
    projeto = projeto_service.obter_projeto(projeto_id)
    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    
    # Atualiza os campos
    if projeto_update.titulo is not None:
        projeto.titulo = projeto_update.titulo
    if projeto_update.descricao is not None:
        projeto.descricao = projeto_update.descricao
    if projeto_update.autor is not None:
        projeto.autor = projeto_update.autor
    
    # Atualiza a data de atualização
    projeto.data_atualizacao = datetime.now()
    
    # Salva o projeto
    projeto_service.salvar_projeto(projeto_id)
    
    # Retorna os metadados atualizados
    return projeto.obter_metadados()


@router.delete("/{projeto_id}", status_code=204)
def excluir_projeto(
    projeto_id: str,
    request: Request,
    session_id: str = Depends(get_session_id),
    projeto_service: GerenciadorProjetos = Depends(get_projeto_service)
):
    """
    Exclui um projeto.
    """
    # Verifica se o projeto pertence à sessão atual
    projeto_data = request.app.state.session_storage.get_data(
        session_id=session_id,
        data_type="projetos",
        data_id=projeto_id
    )
    
    if not projeto_data:
        raise HTTPException(status_code=404, detail="Projeto não encontrado na sessão atual")
    
    # Exclui o projeto
    if not projeto_service.excluir_projeto(projeto_id):
        raise HTTPException(status_code=500, detail="Erro ao excluir projeto")
    
    # Remove a associação com a sessão
    request.app.state.session_storage.delete_data(
        session_id=session_id,
        data_type="projetos",
        data_id=projeto_id
    )
    
    return Response(status_code=204)


@router.post("/{projeto_id}/grafos/{grafo_id}", response_model=ProjetoInfo)
def adicionar_grafo_ao_projeto(
    projeto_id: str,
    grafo_id: str,
    request: Request,
    session_id: str = Depends(get_session_id),
    projeto_service: GerenciadorProjetos = Depends(get_projeto_service)
):
    """
    Adiciona um grafo existente ao projeto.
    """
    # Verifica se o projeto pertence à sessão atual
    projeto_data = request.app.state.session_storage.get_data(
        session_id=session_id,
        data_type="projetos",
        data_id=projeto_id
    )
    
    if not projeto_data:
        raise HTTPException(status_code=404, detail="Projeto não encontrado na sessão atual")
    
    # Verifica se o grafo pertence à sessão atual
    grafo_data = request.app.state.session_storage.get_data(
        session_id=session_id,
        data_type="grafos",
        data_id=grafo_id
    )
    
    if not grafo_data:
        raise HTTPException(status_code=404, detail="Grafo não encontrado na sessão atual")
    
    # Obtém o projeto
    projeto = projeto_service.obter_projeto(projeto_id)
    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    
    # Obtém o grafo
    grafo_service = request.app.state.grafo_service
    grafo = grafo_service.obter_grafo(session_id, grafo_id)
    if not grafo:
        raise HTTPException(status_code=404, detail="Grafo não encontrado")
    
    # Adiciona o grafo ao projeto
    projeto.adicionar_grafo(grafo, grafo_id)
    
    # Salva o projeto
    projeto_service.salvar_projeto(projeto_id)
    
    # Retorna os metadados atualizados
    return projeto.obter_metadados()


@router.delete("/{projeto_id}/grafos/{grafo_id}", status_code=204)
def remover_grafo_do_projeto(
    projeto_id: str,
    grafo_id: str,
    request: Request,
    session_id: str = Depends(get_session_id),
    projeto_service: GerenciadorProjetos = Depends(get_projeto_service)
):
    """
    Remove um grafo do projeto.
    """
    # Verifica se o projeto pertence à sessão atual
    projeto_data = request.app.state.session_storage.get_data(
        session_id=session_id,
        data_type="projetos",
        data_id=projeto_id
    )
    
    if not projeto_data:
        raise HTTPException(status_code=404, detail="Projeto não encontrado na sessão atual")
    
    # Obtém o projeto
    projeto = projeto_service.obter_projeto(projeto_id)
    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    
    # Remove o grafo do projeto
    if not projeto.remover_grafo(grafo_id):
        raise HTTPException(status_code=404, detail="Grafo não encontrado no projeto")
    
    # Salva o projeto
    projeto_service.salvar_projeto(projeto_id)
    
    return Response(status_code=204)


@router.get("/{projeto_id}/grafos", response_model=List[Dict[str, Any]])
def listar_grafos_do_projeto(
    projeto_id: str,
    request: Request,
    session_id: str = Depends(get_session_id),
    projeto_service: GerenciadorProjetos = Depends(get_projeto_service)
):
    """
    Lista todos os grafos de um projeto.
    """
    # Verifica se o projeto pertence à sessão atual
    projeto_data = request.app.state.session_storage.get_data(
        session_id=session_id,
        data_type="projetos",
        data_id=projeto_id
    )
    
    if not projeto_data:
        raise HTTPException(status_code=404, detail="Projeto não encontrado na sessão atual")
    
    # Obtém o projeto
    projeto = projeto_service.obter_projeto(projeto_id)
    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    
    # Lista os grafos do projeto
    return projeto.listar_grafos()


@router.post("/{projeto_id}/notas", response_model=Dict[str, Any])
def adicionar_nota(
    projeto_id: str,
    nota: NotaCreate,
    request: Request,
    session_id: str = Depends(get_session_id),
    projeto_service: GerenciadorProjetos = Depends(get_projeto_service)
):
    """
    Adiciona uma nota ao projeto.
    """
    # Verifica se o projeto pertence à sessão atual
    projeto_data = request.app.state.session_storage.get_data(
        session_id=session_id,
        data_type="projetos",
        data_id=projeto_id
    )
    
    if not projeto_data:
        raise HTTPException(status_code=404, detail="Projeto não encontrado na sessão atual")
    
    # Obtém o projeto
    projeto = projeto_service.obter_projeto(projeto_id)
    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    
    # Adiciona a nota
    nota_id = projeto.adicionar_nota(
        texto=nota.texto,
        grafo_id=nota.grafo_id
    )
    
    # Salva o projeto
    projeto_service.salvar_projeto(projeto_id)
    
    # Retorna os dados da nota
    return {
        "id": nota_id,
        "texto": nota.texto,
        "grafo_id": nota.grafo_id,
        "timestamp": projeto.notas[nota_id]["timestamp"].isoformat()
    }


@router.get("/{projeto_id}/notas", response_model=List[Dict[str, Any]])
def listar_notas(
    projeto_id: str,
    request: Request,
    session_id: str = Depends(get_session_id),
    projeto_service: GerenciadorProjetos = Depends(get_projeto_service)
):
    """
    Lista todas as notas de um projeto.
    """
    # Verifica se o projeto pertence à sessão atual
    projeto_data = request.app.state.session_storage.get_data(
        session_id=session_id,
        data_type="projetos",
        data_id=projeto_id
    )
    
    if not projeto_data:
        raise HTTPException(status_code=404, detail="Projeto não encontrado na sessão atual")
    
    # Obtém o projeto
    projeto = projeto_service.obter_projeto(projeto_id)
    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    
    # Formata as notas para retorno
    notas = []
    for i, nota in enumerate(projeto.notas):
        notas.append({
            "id": i,
            "texto": nota["texto"],
            "grafo_id": nota.get("grafo_id"),
            "timestamp": nota["timestamp"].isoformat()
        })
    
    return notas


@router.put("/{projeto_id}/tags", response_model=List[str])
def atualizar_tags(
    projeto_id: str,
    tags_update: TagUpdate,
    request: Request,
    session_id: str = Depends(get_session_id),
    projeto_service: GerenciadorProjetos = Depends(get_projeto_service)
):
    """
    Atualiza as tags de um projeto.
    """
    # Verifica se o projeto pertence à sessão atual
    projeto_data = request.app.state.session_storage.get_data(
        session_id=session_id,
        data_type="projetos",
        data_id=projeto_id
    )
    
    if not projeto_data:
        raise HTTPException(status_code=404, detail="Projeto não encontrado na sessão atual")
    
    # Obtém o projeto
    projeto = projeto_service.obter_projeto(projeto_id)
    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    
    # Adiciona novas tags
    for tag in tags_update.adicionar:
        projeto.adicionar_tag(tag)
    
    # Remove tags
    for tag in tags_update.remover:
        projeto.remover_tag(tag)
    
    # Salva o projeto
    projeto_service.salvar_projeto(projeto_id)
    
    # Retorna a lista atualizada de tags
    return list(projeto.tags)


@router.get("/{projeto_id}/historico", response_model=List[Dict[str, Any]])
def obter_historico(
    projeto_id: str,
    request: Request,
    session_id: str = Depends(get_session_id),
    projeto_service: GerenciadorProjetos = Depends(get_projeto_service)
):
    """
    Obtém o histórico de ações de um projeto.
    """
    # Verifica se o projeto pertence à sessão atual
    projeto_data = request.app.state.session_storage.get_data(
        session_id=session_id,
        data_type="projetos",
        data_id=projeto_id
    )
    
    if not projeto_data:
        raise HTTPException(status_code=404, detail="Projeto não encontrado na sessão atual")
    
    # Obtém o projeto
    projeto = projeto_service.obter_projeto(projeto_id)
    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    
    # Formata o histórico para retorno
    historico = []
    for acao in projeto.obter_historico():
        historico.append({
            "tipo": acao["tipo"],
            "descricao": acao["descricao"],
            "detalhes": acao["detalhes"],
            "timestamp": acao["timestamp"].isoformat()
        })
    
    return historico


@router.post("/{projeto_id}/exportar", response_model=ProjetoExport)
def exportar_projeto(
    projeto_id: str,
    request: Request,
    formato: str = "json",
    session_id: str = Depends(get_session_id),
    projeto_service: GerenciadorProjetos = Depends(get_projeto_service)
):
    """
    Exporta um projeto para um formato específico.
    """
    # Verifica se o projeto pertence à sessão atual
    projeto_data = request.app.state.session_storage.get_data(
        session_id=session_id,
        data_type="projetos",
        data_id=projeto_id
    )
    
    if not projeto_data:
        raise HTTPException(status_code=404, detail="Projeto não encontrado na sessão atual")
    
    # Exporta o projeto
    conteudo = projeto_service.exportar_projeto(projeto_id, formato)
    if not conteudo:
        raise HTTPException(status_code=500, detail=f"Erro ao exportar projeto para formato {formato}")
    
    # Codifica o conteúdo em base64
    conteudo_base64 = base64.b64encode(conteudo.encode('utf-8')).decode('utf-8')
    
    # Obtém o projeto para metadados
    projeto = projeto_service.obter_projeto(projeto_id)
    
    return {
        "projeto_id": projeto_id,
        "titulo": projeto.titulo,
        "formato": formato,
        "conteudo": conteudo_base64,
        "timestamp": datetime.now().isoformat()
    }


@router.post("/{projeto_id}/exportar/arquivo")
def exportar_projeto_arquivo(
    projeto_id: str,
    request: Request,
    formato: str = "json",
    session_id: str = Depends(get_session_id),
    projeto_service: GerenciadorProjetos = Depends(get_projeto_service)
):
    """
    Exporta um projeto para um arquivo.
    """
    # Verifica se o projeto pertence à sessão atual
    projeto_data = request.app.state.session_storage.get_data(
        session_id=session_id,
        data_type="projetos",
        data_id=projeto_id
    )
    
    if not projeto_data:
        raise HTTPException(status_code=404, detail="Projeto não encontrado na sessão atual")
    
    # Exporta o projeto
    conteudo = projeto_service.exportar_projeto(projeto_id, formato)
    if not conteudo:
        raise HTTPException(status_code=500, detail=f"Erro ao exportar projeto para formato {formato}")
    
    # Obtém o projeto para metadados
    projeto = projeto_service.obter_projeto(projeto_id)
    
    # Cria um arquivo em memória
    arquivo = io.BytesIO(conteudo.encode('utf-8'))
    
    # Define o nome do arquivo
    nome_arquivo = f"{projeto.titulo.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.{formato}"
    
    # Retorna o arquivo como resposta
    return StreamingResponse(
        arquivo,
        media_type="application/json" if formato == "json" else "application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={nome_arquivo}"}
    )


@router.post("/importar", response_model=ProjetoInfo)
def importar_projeto(
    projeto_import: ProjetoImport,
    request: Request,
    session_id: str = Depends(get_session_id),
    projeto_service: GerenciadorProjetos = Depends(get_projeto_service)
):
    """
    Importa um projeto a partir de uma representação.
    """
    try:
        # Decodifica o conteúdo de base64
        conteudo = base64.b64decode(projeto_import.conteudo).decode('utf-8')
        
        # Importa o projeto
        projeto_id = projeto_service.importar_projeto(conteudo, projeto_import.formato)
        if not projeto_id:
            raise HTTPException(status_code=500, detail=f"Erro ao importar projeto do formato {projeto_import.formato}")
        
        # Associa o projeto à sessão atual
        request.app.state.session_storage.store_data(
            session_id=session_id,
            data_type="projetos",
            data_id=projeto_id,
            data={"projeto_id": projeto_id}
        )
        
        # Obtém o projeto importado
        projeto = projeto_service.obter_projeto(projeto_id)
        if not projeto:
            raise HTTPException(status_code=500, detail="Erro ao obter projeto importado")
        
        # Retorna os metadados do projeto
        return projeto.obter_metadados()
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao importar projeto: {str(e)}")


@router.post("/importar/arquivo", response_model=ProjetoInfo)
async def importar_projeto_arquivo(
    request: Request,
    arquivo: UploadFile = File(...),
    formato: str = Form("json"),
    session_id: str = Depends(get_session_id),
    projeto_service: GerenciadorProjetos = Depends(get_projeto_service)
):
    """
    Importa um projeto a partir de um arquivo.
    """
    try:
        # Lê o conteúdo do arquivo
        conteudo = await arquivo.read()
        conteudo_str = conteudo.decode('utf-8')
        
        # Importa o projeto
        projeto_id = projeto_service.importar_projeto(conteudo_str, formato)
        if not projeto_id:
            raise HTTPException(status_code=500, detail=f"Erro ao importar projeto do formato {formato}")
        
        # Associa o projeto à sessão atual
        request.app.state.session_storage.store_data(
            session_id=session_id,
            data_type="projetos",
            data_id=projeto_id,
            data={"projeto_id": projeto_id}
        )
        
        # Obtém o projeto importado
        projeto = projeto_service.obter_projeto(projeto_id)
        if not projeto:
            raise HTTPException(status_code=500, detail="Erro ao obter projeto importado")
        
        # Retorna os metadados do projeto
        return projeto.obter_metadados()
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao importar projeto: {str(e)}")


@router.post("/{projeto_id}/relatorio")
def gerar_relatorio_projeto(
    projeto_id: str,
    request: Request,
    formato: str = "pdf",
    incluir_teoria: bool = True,
    incluir_passos: bool = True,
    incluir_referencias: bool = True,
    estilo: str = "padrao",
    session_id: str = Depends(get_session_id),
    projeto_service: GerenciadorProjetos = Depends(get_projeto_service),
    relatorio_service: RelatorioGrafoPDF = Depends(get_relatorio_service)
):
    """
    Gera um relatório didático de um projeto.
    """
    # Verifica se o projeto pertence à sessão atual
    projeto_data = request.app.state.session_storage.get_data(
        session_id=session_id,
        data_type="projetos",
        data_id=projeto_id
    )
    
    if not projeto_data:
        raise HTTPException(status_code=404, detail="Projeto não encontrado na sessão atual")
    
    # Obtém o projeto
    projeto = projeto_service.obter_projeto(projeto_id)
    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    
    # Configurações do relatório
    config = {
        "incluir_teoria": incluir_teoria,
        "incluir_passos": incluir_passos,
        "incluir_referencias": incluir_referencias,
        "estilo": estilo
    }
    
    try:
        # Gera o relatório
        pdf_bytes = relatorio_service.gerar_relatorio_projeto(projeto, config)
        
        # Define o nome do arquivo
        nome_arquivo = f"{projeto.titulo.replace(' ', '_')}_relatorio_{datetime.now().strftime('%Y%m%d')}.pdf"
        
        # Cria um arquivo em memória
        arquivo = io.BytesIO(pdf_bytes)
        
        # Retorna o arquivo como resposta
        return StreamingResponse(
            arquivo,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={nome_arquivo}"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar relatório: {str(e)}")
