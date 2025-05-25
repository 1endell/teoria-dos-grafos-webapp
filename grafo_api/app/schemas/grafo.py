"""
Modelos Pydantic para validação e serialização de grafos na API.
"""

from pydantic import BaseModel, Field, validator
from typing import Dict, List, Any, Optional, Union, Set
from datetime import datetime
import uuid


class VerticeBase(BaseModel):
    """Modelo base para vértices."""
    id: Any
    atributos: Dict[str, Any] = Field(default_factory=dict)


class VerticeCreate(VerticeBase):
    """Modelo para criação de vértices."""
    conjunto: Optional[str] = None  # Para grafos bipartidos


class VerticeUpdate(BaseModel):
    """Modelo para atualização de vértices."""
    atributos: Dict[str, Any] = Field(default_factory=dict)


class Vertice(VerticeBase):
    """Modelo completo de vértice."""
    grau: int = 0
    
    class Config:
        orm_mode = True


class ArestaBase(BaseModel):
    """Modelo base para arestas."""
    origem: Any
    destino: Any
    peso: float = 1.0
    atributos: Dict[str, Any] = Field(default_factory=dict)


class ArestaCreate(ArestaBase):
    """Modelo para criação de arestas."""
    pass


class ArestaUpdate(BaseModel):
    """Modelo para atualização de arestas."""
    peso: Optional[float] = None
    atributos: Optional[Dict[str, Any]] = None


class Aresta(ArestaBase):
    """Modelo completo de aresta."""
    
    class Config:
        orm_mode = True


class GrafoBase(BaseModel):
    """Modelo base para grafos."""
    nome: str
    direcionado: bool = False
    ponderado: bool = False
    bipartido: bool = False


class GrafoCreate(GrafoBase):
    """Modelo para criação de grafos."""
    vertices: List[VerticeCreate] = Field(default_factory=list)
    arestas: List[ArestaCreate] = Field(default_factory=list)


class GrafoUpdate(BaseModel):
    """Modelo para atualização de grafos."""
    nome: Optional[str] = None
    direcionado: Optional[bool] = None
    ponderado: Optional[bool] = None
    bipartido: Optional[bool] = None


class Grafo(GrafoBase):
    """Modelo completo de grafo."""
    id: str
    num_vertices: int = 0
    num_arestas: int = 0
    data_criacao: datetime
    data_atualizacao: Optional[datetime] = None
    vertices: List[Vertice] = Field(default_factory=list)
    arestas: List[Aresta] = Field(default_factory=list)
    
    class Config:
        orm_mode = True


class GrafoInfo(BaseModel):
    """Modelo para informações resumidas de um grafo."""
    id: str
    nome: str
    direcionado: bool
    ponderado: bool
    bipartido: bool
    num_vertices: int
    num_arestas: int
    data_criacao: datetime
    data_atualizacao: Optional[datetime] = None


class GrafoListResponse(BaseModel):
    """Modelo para resposta de listagem de grafos."""
    total: int
    grafos: List[GrafoInfo]


class AlgoritmoParams(BaseModel):
    """Modelo para parâmetros de algoritmos."""
    parametros: Dict[str, Any] = Field(default_factory=dict)


class ResultadoAlgoritmo(BaseModel):
    """Modelo para resultado de algoritmos."""
    algoritmo: str
    grafo_id: str
    resultado: Dict[str, Any]
    tempo_execucao: float  # em segundos


class OperacaoGrafos(BaseModel):
    """Modelo para operações entre grafos."""
    grafo_id1: str
    grafo_id2: str
    nome_resultado: Optional[str] = None


class ImportacaoGrafo(BaseModel):
    """Modelo para importação de grafos."""
    nome: str
    formato: str
    conteudo: str  # Conteúdo do arquivo codificado em base64


class ExportacaoGrafo(BaseModel):
    """Modelo para exportação de grafos."""
    formato: str = "graphml"  # Formato padrão


class ComparacaoGrafos(BaseModel):
    """Modelo para comparação entre grafos."""
    grafo_id1: str
    grafo_id2: str
    metrica: str = "isomorfismo"  # Métrica padrão


class ResultadoComparacao(BaseModel):
    """Modelo para resultado de comparação entre grafos."""
    grafo_id1: str
    grafo_id2: str
    metrica: str
    resultado: Any
    tempo_execucao: float  # em segundos


class VisualizacaoGrafo(BaseModel):
    """Modelo para dados de visualização de grafos."""
    grafo_id: str
    layout: str = "spring"  # Layout padrão
    incluir_atributos: bool = True


class DadosVisualizacao(BaseModel):
    """Modelo para dados de visualização."""
    vertices: List[Dict[str, Any]]
    arestas: List[Dict[str, Any]]
    layout: str


class ErrorResponse(BaseModel):
    """Modelo para respostas de erro."""
    detail: str
    code: Optional[str] = None
