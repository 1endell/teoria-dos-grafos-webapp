"""
Implementação de exportação de grafos para o formato GML.

Este módulo contém funções para exportar grafos para o formato GML (Graph Modeling Language),
um formato de texto para representação de grafos.
"""

import networkx as nx
from typing import Dict, List, Any, Optional
from grafo_backend.core.grafo import Grafo


def exportar_gml(grafo: Grafo, caminho: str) -> bool:
    """
    Exporta um grafo para o formato GML.
    
    Args:
        grafo: Grafo a ser exportado.
        caminho: Caminho do arquivo de saída.
        
    Returns:
        bool: True se a exportação foi bem-sucedida, False caso contrário.
    """
    try:
        # Obtém o grafo NetworkX subjacente
        g_nx = grafo.obter_grafo_networkx()
        
        # Exporta o grafo para o formato GML
        nx.write_gml(g_nx, caminho)
        
        return True
    except Exception as e:
        print(f"Erro ao exportar grafo para GML: {e}")
        return False
