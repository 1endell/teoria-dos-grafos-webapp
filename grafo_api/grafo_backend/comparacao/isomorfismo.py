"""
Implementação de verificação de isomorfismo entre grafos.

Este módulo contém funções para verificar se dois grafos são isomorfos,
ou seja, se possuem a mesma estrutura, independentemente dos rótulos dos vértices.
"""

import networkx as nx
from typing import Dict, List, Any, Optional, Set, Tuple
from core.grafo import Grafo


def verificar_isomorfismo(grafo1: Grafo, grafo2: Grafo) -> bool:
    """
    Verifica se dois grafos são isomorfos.
    
    Args:
        grafo1: Primeiro grafo.
        grafo2: Segundo grafo.
        
    Returns:
        bool: True se os grafos são isomorfos, False caso contrário.
    """
    # Obtém os grafos NetworkX subjacentes
    g1_nx = grafo1.obter_grafo_networkx()
    g2_nx = grafo2.obter_grafo_networkx()
    
    # Verifica se os grafos são isomorfos
    return nx.is_isomorphic(g1_nx, g2_nx)


def encontrar_mapeamento_isomorfismo(grafo1: Grafo, grafo2: Grafo) -> Optional[Dict[Any, Any]]:
    """
    Encontra um mapeamento de isomorfismo entre dois grafos.
    
    Args:
        grafo1: Primeiro grafo.
        grafo2: Segundo grafo.
        
    Returns:
        Optional[Dict[Any, Any]]: Dicionário mapeando vértices do primeiro grafo para vértices do segundo grafo,
                                ou None se os grafos não forem isomorfos.
    """
    # Obtém os grafos NetworkX subjacentes
    g1_nx = grafo1.obter_grafo_networkx()
    g2_nx = grafo2.obter_grafo_networkx()
    
    # Verifica se os grafos são isomorfos e obtém o mapeamento
    matcher = nx.isomorphism.GraphMatcher(g1_nx, g2_nx)
    if matcher.is_isomorphic():
        return matcher.mapping
    else:
        return None


def verificar_isomorfismo_com_atributos(grafo1: Grafo, grafo2: Grafo, 
                                       atributos_vertice: List[str] = None,
                                       atributos_aresta: List[str] = None) -> bool:
    """
    Verifica se dois grafos são isomorfos, considerando atributos específicos de vértices e arestas.
    
    Args:
        grafo1: Primeiro grafo.
        grafo2: Segundo grafo.
        atributos_vertice: Lista de atributos de vértices a serem considerados na verificação.
        atributos_aresta: Lista de atributos de arestas a serem considerados na verificação.
        
    Returns:
        bool: True se os grafos são isomorfos considerando os atributos, False caso contrário.
    """
    # Obtém os grafos NetworkX subjacentes
    g1_nx = grafo1.obter_grafo_networkx()
    g2_nx = grafo2.obter_grafo_networkx()
    
    # Define as funções de comparação de atributos
    node_match = None
    edge_match = None
    
    if atributos_vertice:
        def node_match_func(n1, n2):
            return all(n1.get(attr) == n2.get(attr) for attr in atributos_vertice)
        node_match = node_match_func
    
    if atributos_aresta:
        def edge_match_func(e1, e2):
            return all(e1.get(attr) == e2.get(attr) for attr in atributos_aresta)
        edge_match = edge_match_func
    
    # Verifica se os grafos são isomorfos considerando os atributos
    return nx.is_isomorphic(g1_nx, g2_nx, node_match=node_match, edge_match=edge_match)


def encontrar_automorfismos(grafo: Grafo) -> List[Dict[Any, Any]]:
    """
    Encontra todos os automorfismos de um grafo.
    
    Um automorfismo é um isomorfismo de um grafo para ele mesmo.
    
    Args:
        grafo: Grafo a ser analisado.
        
    Returns:
        List[Dict[Any, Any]]: Lista de dicionários, cada um representando um automorfismo.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Encontra os automorfismos
    automorfismos = list(nx.isomorphism.GraphMatcher(g_nx, g_nx).isomorphisms_iter())
    
    return automorfismos


def calcular_invariantes(grafo: Grafo) -> Dict[str, Any]:
    """
    Calcula invariantes do grafo que podem ser usados para comparação rápida.
    
    Invariantes são propriedades que não mudam sob isomorfismo.
    
    Args:
        grafo: Grafo a ser analisado.
        
    Returns:
        Dict[str, Any]: Dicionário com os invariantes calculados.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Calcula invariantes básicos
    invariantes = {
        "num_vertices": g_nx.number_of_nodes(),
        "num_arestas": g_nx.number_of_edges(),
        "graus": sorted([d for _, d in g_nx.degree()]),
        "eh_conexo": nx.is_connected(g_nx),
        "num_componentes": nx.number_connected_components(g_nx),
        "tamanho_componentes": sorted([len(c) for c in nx.connected_components(g_nx)], reverse=True),
        "diametro": nx.diameter(g_nx) if nx.is_connected(g_nx) else float('inf'),
        "raio": nx.radius(g_nx) if nx.is_connected(g_nx) else float('inf'),
        "eh_bipartido": nx.is_bipartite(g_nx),
    }
    
    # Tenta calcular invariantes adicionais que podem falhar em alguns grafos
    try:
        invariantes["autovalores"] = sorted(nx.laplacian_spectrum(g_nx))
    except:
        invariantes["autovalores"] = None
    
    return invariantes
