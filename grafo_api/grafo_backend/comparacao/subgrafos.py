"""
Módulo para verificação e busca de subgrafos.
"""

from typing import List, Dict, Any, Optional
import networkx as nx
from grafo_backend.core.grafo import Grafo

def verificar_subgrafo(grafo_principal: Grafo, subgrafo: Grafo) -> bool:
    """
    Verifica se um grafo é um subgrafo de outro.

    Args:
        grafo_principal: O grafo maior.
        subgrafo: O grafo menor a ser verificado.

    Returns:
        bool: True se o subgrafo for um subgrafo do grafo principal, False caso contrário.
    """
    g_principal_nx = grafo_principal.obter_grafo_networkx()
    subgrafo_nx = subgrafo.obter_grafo_networkx()

    # Verifica se todos os vértices e arestas do subgrafo existem no grafo principal
    if not set(subgrafo_nx.nodes()).issubset(set(g_principal_nx.nodes())):
        return False
    if not set(subgrafo_nx.edges()).issubset(set(g_principal_nx.edges())):
        return False

    return True

def encontrar_ocorrencias_subgrafo(grafo_principal: Grafo, subgrafo_padrao: Grafo) -> List[Dict[Any, Any]]:
    """
    Encontra todas as ocorrências (isomorfismos) de um subgrafo padrão dentro de um grafo principal.

    Args:
        grafo_principal: O grafo maior onde a busca será realizada.
        subgrafo_padrao: O grafo padrão a ser encontrado.

    Returns:
        List[Dict[Any, Any]]: Uma lista de dicionários, onde cada dicionário representa um mapeamento
                              dos vértices do subgrafo padrão para os vértices do grafo principal,
                              indicando uma ocorrência isomorfa.
    """
    g_principal_nx = grafo_principal.obter_grafo_networkx()
    subgrafo_padrao_nx = subgrafo_padrao.obter_grafo_networkx()

    # Usa o algoritmo VF2 para encontrar isomorfismos de subgrafos
    matcher = nx.isomorphism.GraphMatcher(g_principal_nx, subgrafo_padrao_nx)
    
    ocorrencias = []
    for subgraph_mapping in matcher.subgraph_isomorphisms_iter():
        # Inverte o mapeamento para {vertice_subgrafo: vertice_principal}
        ocorrencia = {v: k for k, v in subgraph_mapping.items()}
        ocorrencias.append(ocorrencia)

    return ocorrencias

# Outras funções relacionadas a subgrafos podem ser adicionadas aqui

