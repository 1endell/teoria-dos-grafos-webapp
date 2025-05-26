"""
Serviço para visualização de grafos.
"""

import logging
import time
import base64
from typing import Dict, Any, Optional, List
import io
import matplotlib.pyplot as plt
import networkx as nx

from app.schemas.grafo import DadosVisualizacao
from app.services.grafo_service import GrafoService

# Configuração de logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class VisualizacaoService:
    """
    Serviço para visualização de grafos.
    """
    
    def __init__(self, grafo_service: GrafoService = None):
        """
        Inicializa o serviço de visualização.
        
        Args:
            grafo_service: Serviço de grafos.
        """
        self.grafo_service = grafo_service
        self._layouts = {
            "spring": nx.spring_layout,
            "circular": nx.circular_layout,
            "random": nx.random_layout,
            "shell": nx.shell_layout,
            "spectral": nx.spectral_layout,
            "kamada_kawai": nx.kamada_kawai_layout
        }
        logger.debug(f"VisualizacaoService inicializado com ID: {id(self)}")
    
    def _get_grafo_service(self):
        """
        Obtém o serviço de grafos, seja o injetado no construtor ou via importação local.
        
        Returns:
            Serviço de grafos
        """
        if self.grafo_service is None:
            # Importação local para evitar ciclo de importação
            from app.core.session import get_grafo_service
            self.grafo_service = get_grafo_service()
        return self.grafo_service
    
    def listar_layouts(self) -> List[str]:
        """
        Lista os layouts de visualização disponíveis.
        
        Returns:
            List[str]: Lista de layouts disponíveis.
        """
        return list(self._layouts.keys())
    
    def visualizar_grafo(self, grafo_id: str, layout: str = "spring", incluir_atributos: bool = True) -> Dict[str, Any]:
        """
        Obtém dados para visualização de um grafo.
        
        Args:
            grafo_id: ID do grafo.
            layout: Layout de visualização.
            incluir_atributos: Incluir atributos dos vértices e arestas.
            
        Returns:
            Dict[str, Any]: Dados para visualização.
            
        Raises:
            ValueError: Se o grafo não existir ou o layout não for suportado.
        """
        # Obtém o serviço de grafos
        grafo_service = self._get_grafo_service()
        
        # Obtém o grafo
        grafo = grafo_service.obter_grafo(grafo_id)
        if not grafo:
            raise ValueError(f"Grafo com ID {grafo_id} não encontrado.")
        
        # Verifica se o layout é suportado
        if layout not in self._layouts:
            raise ValueError(f"Layout '{layout}' não suportado.")
        
        try:
            # Cria um grafo NetworkX
            G = nx.Graph() if not grafo.eh_direcionado() else nx.DiGraph()
            
            # Adiciona os vértices
            for v in grafo.obter_vertices():
                atributos = grafo.obter_atributos_vertice(v) if incluir_atributos else {}
                G.add_node(str(v), **atributos)
            
            # Adiciona as arestas com peso numérico para evitar erro no NetworkX
            for u, v, atributos_aresta in grafo.obter_arestas():
                # Extrai o peso como valor numérico ou usa 1.0 como padrão
                peso = 1.0
                if 'weight' in atributos_aresta and isinstance(atributos_aresta['weight'], (int, float)):
                    peso = float(atributos_aresta['weight'])
                
                # Cria uma cópia dos atributos sem o peso para evitar conflito
                atributos_sem_peso = {k: v for k, v in atributos_aresta.items() if k != 'weight'}
                
                # Adiciona a aresta com peso numérico e outros atributos separados
                G.add_edge(str(u), str(v), weight=peso, **atributos_sem_peso)
            
            # Calcula o layout
            pos = self._layouts[layout](G)
            
            # Prepara os dados de visualização
            vertices = []
            for v in G.nodes():
                node_data = {
                    "id": v,
                    "x": float(pos[v][0]),
                    "y": float(pos[v][1])
                }
                
                # Adiciona atributos se solicitado
                if incluir_atributos:
                    node_data["atributos"] = dict(G.nodes[v])
                
                vertices.append(node_data)
            
            arestas = []
            for u, v, data in G.edges(data=True):
                edge_data = {
                    "origem": u,
                    "destino": v
                }
                
                # Adiciona atributos se solicitado
                if incluir_atributos:
                    # Recria os atributos incluindo o peso como parte do dicionário
                    atributos = {k: v for k, v in data.items()}
                    edge_data["atributos"] = atributos
                
                arestas.append(edge_data)
            
            # Retorna os dados de visualização como dicionário
            return {
                "vertices": vertices,
                "arestas": arestas,
                "layout": layout
            }
        except Exception as e:
            logger.error(f"Erro ao visualizar grafo {grafo_id}: {e}", exc_info=True)
            raise ValueError(f"Erro ao visualizar grafo: {str(e)}")
    
    def gerar_imagem(self, grafo_id: str, formato: str = "png", layout: str = "spring") -> Dict[str, Any]:
        """
        Gera uma imagem de um grafo.
        
        Args:
            grafo_id: ID do grafo.
            formato: Formato da imagem (png, svg, etc.).
            layout: Layout de visualização.
            
        Returns:
            Dict[str, Any]: Dados da imagem.
            
        Raises:
            ValueError: Se o grafo não existir, o layout não for suportado ou o formato não for suportado.
        """
        # Obtém o serviço de grafos
        grafo_service = self._get_grafo_service()
        
        # Obtém o grafo
        grafo = grafo_service.obter_grafo(grafo_id)
        if not grafo:
            raise ValueError(f"Grafo com ID {grafo_id} não encontrado.")
        
        # Verifica se o layout é suportado
        if layout not in self._layouts:
            raise ValueError(f"Layout '{layout}' não suportado.")
        
        # Verifica se o formato é suportado
        formatos_suportados = ["png", "svg", "pdf", "jpg", "jpeg"]
        if formato not in formatos_suportados:
            raise ValueError(f"Formato '{formato}' não suportado. Formatos suportados: {', '.join(formatos_suportados)}")
        
        try:
            # Cria um grafo NetworkX
            G = nx.Graph() if not grafo.eh_direcionado() else nx.DiGraph()
            
            # Adiciona os vértices
            for v in grafo.obter_vertices():
                G.add_node(str(v))
            
            # Adiciona as arestas com peso numérico para evitar erro no NetworkX
            for u, v, atributos_aresta in grafo.obter_arestas():
                # Extrai o peso como valor numérico ou usa 1.0 como padrão
                peso = 1.0
                if 'weight' in atributos_aresta and isinstance(atributos_aresta['weight'], (int, float)):
                    peso = float(atributos_aresta['weight'])
                
                G.add_edge(str(u), str(v), weight=peso)
            
            # Calcula o layout
            pos = self._layouts[layout](G)
            
            # Gera a imagem
            plt.figure(figsize=(10, 8))
            nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, edge_color='black', linewidths=1, font_size=15)
            
            # Salva a imagem em um buffer
            buf = io.BytesIO()
            plt.savefig(buf, format=formato)
            plt.close()
            
            # Codifica a imagem em base64
            buf.seek(0)
            imagem_base64 = base64.b64encode(buf.read()).decode('utf-8')
            
            # Retorna os dados da imagem
            return {
                "grafo_id": grafo_id,
                "formato": formato,
                "layout": layout,
                "conteudo": imagem_base64
            }
        except Exception as e:
            logger.error(f"Erro ao gerar imagem do grafo {grafo_id}: {e}", exc_info=True)
            raise ValueError(f"Erro ao gerar imagem: {str(e)}")
