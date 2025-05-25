"""
Implementação de exportação de grafos para o formato GEXF.

Este módulo contém funções para exportar grafos para o formato GEXF (Graph Exchange XML Format),
um formato XML para representação de grafos, especialmente utilizado pelo software Gephi.
"""

import networkx as nx
from typing import Dict, List, Any, Optional
from grafo_backend.core.grafo import Grafo


def exportar_gexf(grafo: Grafo, caminho: str) -> bool:
    """
    Exporta um grafo para o formato GEXF.
    
    Args:
        grafo: Grafo a ser exportado.
        caminho: Caminho do arquivo de saída.
        
    Returns:
        bool: True se a exportação foi bem-sucedida, False caso contrário.
    """
    try:
        # Obtém o grafo NetworkX subjacente
        g_nx = grafo.obter_grafo_networkx()
        
        # Exporta o grafo para o formato GEXF
        nx.write_gexf(g_nx, caminho)
        
        return True
    except Exception as e:
        print(f"Erro ao exportar grafo para GEXF: {e}")
        return False
