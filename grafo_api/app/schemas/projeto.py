"""
Esquemas Pydantic para projetos de estudo.

Este módulo define os esquemas para validação de dados relacionados a projetos
de estudo, incluindo criação, atualização, importação e exportação.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class ProjetoCreate(BaseModel):
    """Esquema para criação de um novo projeto."""
    titulo: str = Field(..., description="Título do projeto")
    descricao: str = Field("", description="Descrição do projeto")
    autor: str = Field("Usuário", description="Nome do autor do projeto")


class ProjetoUpdate(BaseModel):
    """Esquema para atualização de um projeto existente."""
    titulo: Optional[str] = Field(None, description="Novo título do projeto")
    descricao: Optional[str] = Field(None, description="Nova descrição do projeto")
    autor: Optional[str] = Field(None, description="Novo autor do projeto")


class ProjetoInfo(BaseModel):
    """Esquema para informações de um projeto."""
    id: str = Field(..., description="ID único do projeto")
    titulo: str = Field(..., description="Título do projeto")
    descricao: str = Field(..., description="Descrição do projeto")
    autor: str = Field(..., description="Nome do autor do projeto")
    data_criacao: str = Field(..., description="Data de criação do projeto (ISO format)")
    data_atualizacao: str = Field(..., description="Data da última atualização do projeto (ISO format)")
    num_grafos: int = Field(..., description="Número de grafos no projeto")
    num_operacoes: Optional[int] = Field(None, description="Número de operações registradas")
    num_algoritmos: Optional[int] = Field(None, description="Número de algoritmos aplicados")
    num_notas: Optional[int] = Field(None, description="Número de notas no projeto")
    tags: List[str] = Field(default_factory=list, description="Tags do projeto")


class ProjetoList(BaseModel):
    """Esquema para lista paginada de projetos."""
    total: int = Field(..., description="Número total de projetos")
    projetos: List[ProjetoInfo] = Field(..., description="Lista de projetos")


class NotaCreate(BaseModel):
    """Esquema para criação de uma nota."""
    texto: str = Field(..., description="Texto da nota")
    grafo_id: Optional[str] = Field(None, description="ID do grafo relacionado (opcional)")


class TagUpdate(BaseModel):
    """Esquema para atualização de tags."""
    adicionar: List[str] = Field(default_factory=list, description="Tags a serem adicionadas")
    remover: List[str] = Field(default_factory=list, description="Tags a serem removidas")


class ProjetoExport(BaseModel):
    """Esquema para exportação de um projeto."""
    projeto_id: str = Field(..., description="ID do projeto exportado")
    titulo: str = Field(..., description="Título do projeto")
    formato: str = Field(..., description="Formato de exportação")
    conteudo: str = Field(..., description="Conteúdo do projeto em base64")
    timestamp: str = Field(..., description="Timestamp da exportação (ISO format)")


class ProjetoImport(BaseModel):
    """Esquema para importação de um projeto."""
    nome: str = Field(..., description="Nome a ser dado ao projeto importado")
    formato: str = Field(..., description="Formato do conteúdo")
    conteudo: str = Field(..., description="Conteúdo do projeto em base64")
