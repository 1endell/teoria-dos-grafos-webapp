"""
Implementação de importação de grafos a partir do formato JSON.

Este módulo contém funções para importar grafos a partir do formato JSON,
um formato de texto estruturado para representação de dados.
"""

import networkx as nx
import json
import os
from typing import Dict, List, Any, Optional
from core.grafo import Grafo


def importar_json(caminho: str, nome: str = None) -> Optional[Grafo]:
    """
    Importa um grafo a partir de um arquivo no formato JSON.
    
    Args:
        caminho: Caminho do arquivo de entrada.
        nome: Nome a ser atribuído ao grafo. Se None, usa o nome do arquivo sem extensão ou o nome definido no JSON.
        
    Returns:
        Optional[Grafo]: Grafo importado ou None se a importação falhar.
    """
    try:
        # Carrega os dados do arquivo JSON
        with open(caminho, 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)
        
        # Define o nome do grafo
        if nome is None:
            nome = dados.get("nome", os.path.splitext(os.path.basename(caminho))[0])
        
        # Cria um novo grafo
        grafo = Grafo(nome)
        g_nx = nx.Graph()
        
        # Adiciona os vértices
        for vertice_dados in dados.get("vertices", []):
            id_vertice = vertice_dados.get("id")
            atributos = vertice_dados.get("atributos", {})
            g_nx.add_node(id_vertice, **atributos)
        
        # Adiciona as arestas
        for aresta_dados in dados.get("arestas", []):
            origem = aresta_dados.get("origem")
            destino = aresta_dados.get("destino")
            peso = aresta_dados.get("peso", 1.0)
            atributos = aresta_dados.get("atributos", {})
            
            # Garante que o peso esteja nos atributos
            atributos["weight"] = peso
            
            g_nx.add_edge(origem, destino, **atributos)
        
        # Define o grafo NetworkX importado
        grafo.definir_grafo_networkx(g_nx)
        
        return grafo
    except Exception as e:
        print(f"Erro ao importar grafo de JSON: {e}")
        return None
