"""
Implementação de importação de grafos a partir do formato GraphML.

Este módulo contém funções para importar grafos a partir do formato GraphML,
um formato baseado em XML para representação de grafos.
"""

import networkx as nx
import os
from typing import Dict, List, Any, Optional
from core.grafo import Grafo


def importar_graphml(caminho: str, nome: str = None) -> Optional[Grafo]:
    """
    Importa um grafo a partir de um arquivo no formato GraphML.
    
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
        
        # Importa o grafo do formato GraphML
        g_nx = nx.read_graphml(caminho)
        
        # Cria um novo grafo
        grafo = Grafo(nome)
        
        # Define o grafo NetworkX importado
        grafo.definir_grafo_networkx(g_nx)
        
        return grafo
    except Exception as e:
        print(f"Erro ao importar grafo de GraphML: {e}")
        return None
