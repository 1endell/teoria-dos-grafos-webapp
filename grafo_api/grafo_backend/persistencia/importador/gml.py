"""
Implementação de importação de grafos a partir do formato GML.

Este módulo contém funções para importar grafos a partir do formato GML (Graph Modeling Language),
um formato de texto para representação de grafos.
"""

import networkx as nx
import os
from typing import Dict, List, Any, Optional
from grafo_backend.core.grafo import Grafo


def importar_gml(caminho: str, nome: str = None) -> Optional[Grafo]:
    """
    Importa um grafo a partir de um arquivo no formato GML.
    
    Args:
        caminho: Caminho do arquivo de entrada.
        nome: Nome a ser atribuído ao grafo. Se None, usa o nome do arquivo sem extensão.
        
    Returns:
        Optional[Grafo]: Grafo importado ou None se a importação falhar.
    """
    try:
        # Define o nome do grafo
        if nome is None:
            nome = os.path.splitext(os.path.basename(caminho))[0]
        
        # Importa o grafo do formato GML
        g_nx = nx.read_gml(caminho)
        
        # Cria um novo grafo
        grafo = Grafo(nome)
        
        # Define o grafo NetworkX importado
        grafo.definir_grafo_networkx(g_nx)
        
        return grafo
    except Exception as e:
        print(f"Erro ao importar grafo de GML: {e}")
        return None
