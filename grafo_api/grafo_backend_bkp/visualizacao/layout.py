"""
Módulo para funções de layout de grafos.
"""

import networkx as nx
from grafo_backend.core.grafo import Grafo

def gerar_layout(grafo: Grafo, tipo_layout: str = 'spring') -> dict:
    """
    Gera as posições dos vértices para visualização usando um layout específico.

    Args:
        grafo: O objeto Grafo.
        tipo_layout: O tipo de layout a ser usado (ex: 'spring', 'circular', 'kamada_kawai').

    Returns:
        dict: Um dicionário mapeando cada vértice para suas coordenadas (x, y).
    """
    g_nx = grafo.obter_grafo_networkx()
    pos = {}
    try:
        if tipo_layout == 'spring':
            pos = nx.spring_layout(g_nx)
        elif tipo_layout == 'circular':
            pos = nx.circular_layout(g_nx)
        elif tipo_layout == 'kamada_kawai':
            pos = nx.kamada_kawai_layout(g_nx)
        elif tipo_layout == 'random':
            pos = nx.random_layout(g_nx)
        elif tipo_layout == 'shell':
            pos = nx.shell_layout(g_nx)
        elif tipo_layout == 'spectral':
            pos = nx.spectral_layout(g_nx)
        else:
            # Layout padrão caso o tipo seja inválido
            pos = nx.spring_layout(g_nx)
    except Exception as e:
        # Fallback em caso de erro no layout específico
        print(f"Erro ao gerar layout {tipo_layout}: {e}. Usando layout spring.")
        pos = nx.spring_layout(g_nx)
        
    # Converte as posições para um formato serializável (listas)
    pos_serializavel = {vertice: list(coord) for vertice, coord in pos.items()}
    
    return pos_serializavel

# Adicionar outras funções de visualização se necessário, como visualizar_grafo
# def visualizar_grafo(grafo: Grafo, layout: dict = None, arquivo: str = None):
#     pass

