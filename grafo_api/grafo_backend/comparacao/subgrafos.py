"""
Implementação de funcionalidades para subgrafos e busca de padrões em grafos.

Este módulo contém funções para verificar subgrafos, encontrar subgrafos induzidos
e buscar padrões em grafos.
"""

import networkx as nx
from typing import Dict, List, Any, Optional, Set, Tuple
from grafo_backend.core.grafo import Grafo


def verificar_subgrafo(grafo: Grafo, subgrafo: Grafo) -> bool:
    """
    Verifica se um grafo é subgrafo de outro.
    
    Um grafo H é subgrafo de um grafo G se os vértices de H são um subconjunto
    dos vértices de G e as arestas de H são um subconjunto das arestas de G.
    
    Args:
        grafo: Grafo principal.
        subgrafo: Grafo candidato a subgrafo.
        
    Returns:
        bool: True se o segundo grafo é subgrafo do primeiro, False caso contrário.
    """
    # Obtém os grafos NetworkX subjacentes
    g_nx = grafo.obter_grafo_networkx()
    s_nx = subgrafo.obter_grafo_networkx()
    
    # Verifica se todos os vértices do subgrafo estão no grafo principal
    for v in s_nx.nodes():
        if v not in g_nx.nodes():
            return False
    
    # Verifica se todas as arestas do subgrafo estão no grafo principal
    for u, v in s_nx.edges():
        if not g_nx.has_edge(u, v):
            return False
    
    return True


def verificar_subgrafo_induzido(grafo: Grafo, subgrafo: Grafo) -> bool:
    """
    Verifica se um grafo é subgrafo induzido de outro.
    
    Um grafo H é subgrafo induzido de um grafo G se H contém todas as arestas
    de G que conectam vértices em H.
    
    Args:
        grafo: Grafo principal.
        subgrafo: Grafo candidato a subgrafo induzido.
        
    Returns:
        bool: True se o segundo grafo é subgrafo induzido do primeiro, False caso contrário.
    """
    # Obtém os grafos NetworkX subjacentes
    g_nx = grafo.obter_grafo_networkx()
    s_nx = subgrafo.obter_grafo_networkx()
    
    # Obtém os vértices do subgrafo
    vertices_subgrafo = set(s_nx.nodes())
    
    # Verifica se todos os vértices do subgrafo estão no grafo principal
    if not vertices_subgrafo.issubset(set(g_nx.nodes())):
        return False
    
    # Cria o subgrafo induzido pelos vértices do subgrafo no grafo principal
    subgrafo_induzido = g_nx.subgraph(vertices_subgrafo)
    
    # Verifica se o número de arestas é o mesmo
    if s_nx.number_of_edges() != subgrafo_induzido.number_of_edges():
        return False
    
    # Verifica se todas as arestas do subgrafo estão no subgrafo induzido
    for u, v in s_nx.edges():
        if not subgrafo_induzido.has_edge(u, v):
            return False
    
    return True


def criar_subgrafo_induzido(grafo: Grafo, vertices: List[Any], nome: str = None) -> Grafo:
    """
    Cria um subgrafo induzido por um conjunto de vértices.
    
    Args:
        grafo: Grafo principal.
        vertices: Lista de vértices para induzir o subgrafo.
        nome: Nome do subgrafo. Se None, usa "Subgrafo induzido de {grafo.nome}".
        
    Returns:
        Grafo: Subgrafo induzido.
        
    Raises:
        ValueError: Se algum vértice não existir no grafo.
    """
    # Verifica se todos os vértices existem no grafo
    for v in vertices:
        if not grafo.existe_vertice(v):
            raise ValueError(f"Vértice '{v}' não existe no grafo.")
    
    # Define o nome do subgrafo
    if nome is None:
        nome = f"Subgrafo induzido de {grafo.nome}"
    
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Cria o subgrafo induzido
    s_nx = g_nx.subgraph(vertices)
    
    # Cria um novo grafo
    subgrafo = Grafo(nome)
    
    # Define o grafo NetworkX
    subgrafo.definir_grafo_networkx(s_nx)
    
    return subgrafo


def encontrar_subgrafo_isomorfo(grafo: Grafo, padrao: Grafo) -> List[Dict[Any, Any]]:
    """
    Encontra todas as ocorrências de um padrão em um grafo.
    
    Args:
        grafo: Grafo principal onde buscar o padrão.
        padrao: Grafo padrão a ser buscado.
        
    Returns:
        List[Dict[Any, Any]]: Lista de dicionários, cada um mapeando vértices do padrão para vértices do grafo.
    """
    # Obtém os grafos NetworkX subjacentes
    g_nx = grafo.obter_grafo_networkx()
    p_nx = padrao.obter_grafo_networkx()
    
    # Busca por subgrafos isomorfos
    matcher = nx.isomorphism.GraphMatcher(g_nx, p_nx)
    
    # Retorna todos os mapeamentos encontrados
    return list(matcher.subgraph_isomorphisms_iter())


def encontrar_cliques_maximais(grafo: Grafo, tamanho_minimo: int = 3) -> List[Set[Any]]:
    """
    Encontra todos os cliques maximais no grafo.
    
    Um clique é um subgrafo completo, e um clique maximal é um clique que
    não está contido em nenhum outro clique.
    
    Args:
        grafo: Grafo a ser analisado.
        tamanho_minimo: Tamanho mínimo dos cliques a serem retornados.
        
    Returns:
        List[Set[Any]]: Lista de conjuntos, cada um contendo os vértices de um clique maximal.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Encontra os cliques maximais
    cliques = list(nx.find_cliques(g_nx))
    
    # Filtra por tamanho mínimo
    return [set(clique) for clique in cliques if len(clique) >= tamanho_minimo]


def encontrar_componentes_conexos(grafo: Grafo) -> List[Set[Any]]:
    """
    Encontra todos os componentes conexos do grafo.
    
    Args:
        grafo: Grafo a ser analisado.
        
    Returns:
        List[Set[Any]]: Lista de conjuntos, cada um contendo os vértices de um componente conexo.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Encontra os componentes conexos
    return list(nx.connected_components(g_nx))
