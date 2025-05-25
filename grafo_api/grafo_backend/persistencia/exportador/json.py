"""
Implementação de exportação de grafos para o formato JSON.

Este módulo contém funções para exportar grafos para o formato JSON,
um formato de texto estruturado para representação de dados.
"""

import networkx as nx
import json
from typing import Dict, List, Any, Optional
from grafo_backend.core.grafo import Grafo


def exportar_json(grafo: Grafo, caminho: str) -> bool:
    """
    Exporta um grafo para o formato JSON.
    
    Args:
        grafo: Grafo a ser exportado.
        caminho: Caminho do arquivo de saída.
        
    Returns:
        bool: True se a exportação foi bem-sucedida, False caso contrário.
    """
    try:
        # Obtém o grafo NetworkX subjacente
        g_nx = grafo.obter_grafo_networkx()
        
        # Converte o grafo para um dicionário
        dados = {
            "nome": grafo.nome,
            "vertices": [],
            "arestas": []
        }
        
        # Adiciona os vértices
        for vertice in g_nx.nodes():
            atributos = dict(g_nx.nodes[vertice])
            dados["vertices"].append({
                "id": vertice,
                "atributos": atributos
            })
        
        # Adiciona as arestas
        for origem, destino, atributos in g_nx.edges(data=True):
            dados["arestas"].append({
                "origem": origem,
                "destino": destino,
                "peso": atributos.get("weight", 1.0),
                "atributos": atributos
            })
        
        # Exporta para JSON
        with open(caminho, 'w', encoding='utf-8') as arquivo:
            json.dump(dados, arquivo, indent=2)
        
        return True
    except Exception as e:
        print(f"Erro ao exportar grafo para JSON: {e}")
        return False
