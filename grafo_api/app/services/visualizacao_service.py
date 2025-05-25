"""
Serviço para visualização de grafos.
"""

import time
import io
import base64
from typing import Dict, List, Any, Optional, Tuple

# Importações do backend de grafos
import sys
import os
sys.path.append('/home/ubuntu')  # Adiciona o diretório raiz ao path
from grafo_backend.core.grafo import Grafo
from grafo_backend.visualizacao import gerar_layout, visualizar_grafo

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Usa o backend Agg para gerar imagens sem interface gráfica


class VisualizacaoService:
    """
    Serviço para visualização de grafos.
    """
    
    def __init__(self, grafo_service):
        """
        Inicializa o serviço de visualização.
        
        Args:
            grafo_service: Serviço de grafos para acesso aos grafos.
        """
        self.grafo_service = grafo_service
        self.layouts_disponiveis = {
            "spring": {
                "funcao": nx.spring_layout,
                "descricao": "Layout baseado em forças de mola (Fruchterman-Reingold)"
            },
            "circular": {
                "funcao": nx.circular_layout,
                "descricao": "Layout circular"
            },
            "random": {
                "funcao": nx.random_layout,
                "descricao": "Layout aleatório"
            },
            "shell": {
                "funcao": nx.shell_layout,
                "descricao": "Layout em camadas concêntricas"
            },
            "spectral": {
                "funcao": nx.spectral_layout,
                "descricao": "Layout baseado em autovetores da matriz laplaciana"
            },
            "kamada_kawai": {
                "funcao": nx.kamada_kawai_layout,
                "descricao": "Layout baseado no algoritmo Kamada-Kawai"
            },
            "planar": {
                "funcao": nx.planar_layout,
                "descricao": "Layout para grafos planares"
            }
        }
    
    def listar_layouts(self) -> Dict[str, str]:
        """
        Lista os layouts de visualização disponíveis.
        
        Returns:
            Dict[str, str]: Dicionário mapeando nomes de layouts para suas descrições.
        """
        return {
            layout: info["descricao"]
            for layout, info in self.layouts_disponiveis.items()
        }
    
    def gerar_dados_visualizacao(self, grafo_id: str, layout: str = "spring", incluir_atributos: bool = True) -> Dict[str, Any]:
        """
        Gera dados para visualização de um grafo.
        
        Args:
            grafo_id: ID do grafo.
            layout: Layout de visualização.
            incluir_atributos: Se deve incluir atributos dos vértices e arestas.
            
        Returns:
            Dict[str, Any]: Dados para visualização.
            
        Raises:
            ValueError: Se o grafo não existir ou o layout não for suportado.
        """
        # Verifica se o layout é suportado
        if layout not in self.layouts_disponiveis:
            raise ValueError(f"Layout '{layout}' não suportado.")
        
        # Obtém o grafo
        grafo = self.grafo_service.obter_grafo(grafo_id)
        if not grafo:
            raise ValueError(f"Grafo com ID {grafo_id} não encontrado.")
        
        # Obtém o grafo NetworkX subjacente
        g_nx = grafo.obter_grafo_networkx()
        
        # Gera o layout
        pos = self.layouts_disponiveis[layout]["funcao"](g_nx)
        
        # Prepara os dados dos vértices
        vertices = []
        for v in g_nx.nodes():
            vertice_data = {
                "id": str(v),
                "x": float(pos[v][0]),
                "y": float(pos[v][1]),
                "grau": g_nx.degree(v)
            }
            
            # Adiciona atributos se solicitado
            if incluir_atributos:
                atributos = grafo.obter_atributos_vertice(v)
                vertice_data["atributos"] = atributos
            
            vertices.append(vertice_data)
        
        # Prepara os dados das arestas
        arestas = []
        for u, v in g_nx.edges():
            aresta_data = {
                "origem": str(u),
                "destino": str(v)
            }
            
            # Adiciona peso e atributos se solicitado
            if incluir_atributos:
                if hasattr(grafo, 'obter_peso_aresta'):
                    aresta_data["peso"] = grafo.obter_peso_aresta(u, v)
                atributos = grafo.obter_atributos_aresta(u, v)
                aresta_data["atributos"] = atributos
            
            arestas.append(aresta_data)
        
        return {
            "vertices": vertices,
            "arestas": arestas,
            "layout": layout
        }
    
    def gerar_imagem_grafo(self, grafo_id: str, layout: str = "spring", formato: str = "png", largura: int = 800, altura: int = 600) -> Tuple[bytes, str]:
        """
        Gera uma imagem de visualização do grafo.
        
        Args:
            grafo_id: ID do grafo.
            layout: Layout de visualização.
            formato: Formato da imagem (png, svg, pdf).
            largura: Largura da imagem em pixels.
            altura: Altura da imagem em pixels.
            
        Returns:
            Tuple[bytes, str]: Bytes da imagem e seu MIME type.
            
        Raises:
            ValueError: Se o grafo não existir, o layout não for suportado ou o formato não for suportado.
        """
        # Verifica se o layout é suportado
        if layout not in self.layouts_disponiveis:
            raise ValueError(f"Layout '{layout}' não suportado.")
        
        # Verifica se o formato é suportado
        formatos_suportados = {"png", "svg", "pdf"}
        if formato not in formatos_suportados:
            raise ValueError(f"Formato '{formato}' não suportado. Formatos suportados: {', '.join(formatos_suportados)}")
        
        # Obtém o grafo
        grafo = self.grafo_service.obter_grafo(grafo_id)
        if not grafo:
            raise ValueError(f"Grafo com ID {grafo_id} não encontrado.")
        
        # Obtém o grafo NetworkX subjacente
        g_nx = grafo.obter_grafo_networkx()
        
        # Gera o layout
        pos = self.layouts_disponiveis[layout]["funcao"](g_nx)
        
        # Configura a figura
        plt.figure(figsize=(largura/100, altura/100), dpi=100)
        
        # Desenha o grafo
        nx.draw(g_nx, pos, with_labels=True, node_color='skyblue', node_size=700, 
                edge_color='gray', width=1, font_size=10, font_weight='bold')
        
        # Se o grafo for ponderado, adiciona os pesos das arestas
        if hasattr(grafo, 'eh_ponderado') and grafo.eh_ponderado():
            edge_labels = {}
            for u, v in g_nx.edges():
                edge_labels[(u, v)] = grafo.obter_peso_aresta(u, v)
            nx.draw_networkx_edge_labels(g_nx, pos, edge_labels=edge_labels)
        
        # Salva a imagem em um buffer
        buf = io.BytesIO()
        plt.savefig(buf, format=formato, bbox_inches='tight')
        plt.close()
        
        # Obtém os bytes da imagem
        buf.seek(0)
        imagem_bytes = buf.getvalue()
        
        # Define o MIME type
        mime_types = {
            "png": "image/png",
            "svg": "image/svg+xml",
            "pdf": "application/pdf"
        }
        
        return imagem_bytes, mime_types[formato]
