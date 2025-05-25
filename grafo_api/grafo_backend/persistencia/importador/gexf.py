"""
Implementação de importação de grafos a partir do formato GEXF.

Este módulo contém funções para importar grafos a partir do formato GEXF (Graph Exchange XML Format),
um formato XML para representação de grafos, especialmente utilizado pelo software Gephi.
"""

import networkx as nx
import os
from typing import Dict, List, Any, Optional
from grafo_backend.core.grafo import Grafo


def importar_gexf(caminho: str, nome: str = None) -> Optional[Grafo]:
    """
    Importa um grafo a partir de um arquivo no formato GEXF.
    
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
        
        # Importa o grafo do formato GEXF
        g_nx = nx.read_gexf(caminho)
        
        # Cria um novo grafo
        grafo = Grafo(nome)
        
        # Define o grafo NetworkX importado
        grafo.definir_grafo_networkx(g_nx)
        
        return grafo
    except Exception as e:
        print(f"Erro ao importar grafo de GEXF: {e}")
        return None
