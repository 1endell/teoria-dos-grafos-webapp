"""
Implementação de algoritmos para verificação de planaridade e análise de grafos planares.

Este módulo contém implementações de algoritmos para verificar se um grafo é planar,
detectar subgrafos proibidos (K3,3 e K5) e calcular propriedades de grafos planares.
"""

import networkx as nx
from typing import Dict, List, Any, Set, Tuple, Optional
from core.grafo import Grafo


def verificar_planaridade(grafo: Grafo) -> bool:
    """
    Verifica se um grafo é planar.
    
    Um grafo é planar se pode ser desenhado em um plano sem que suas arestas se cruzem.
    
    Args:
        grafo: Grafo a ser analisado.
        
    Returns:
        bool: True se o grafo é planar, False caso contrário.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Usa a implementação do NetworkX para verificar planaridade
    return nx.is_planar(g_nx)


def encontrar_embedding_planar(grafo: Grafo) -> Optional[Dict]:
    """
    Encontra um embedding planar para o grafo, se ele for planar.
    
    Um embedding planar é uma representação do grafo em um plano sem cruzamento de arestas.
    
    Args:
        grafo: Grafo a ser analisado.
        
    Returns:
        Optional[Dict]: Dicionário representando o embedding planar, ou None se o grafo não for planar.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Verifica se o grafo é planar
    if not nx.is_planar(g_nx):
        return None
    
    # Encontra um embedding planar
    return nx.combinatorial_embedding(g_nx)


def detectar_subgrafo_kuratowski(grafo: Grafo) -> Optional[List[Any]]:
    """
    Detecta um subgrafo de Kuratowski (K5 ou K3,3) no grafo, se existir.
    
    Pelo teorema de Kuratowski, um grafo é planar se e somente se não contém
    um subgrafo que é uma subdivisão de K5 ou K3,3.
    
    Args:
        grafo: Grafo a ser analisado.
        
    Returns:
        Optional[List[Any]]: Lista de vértices formando um subgrafo de Kuratowski,
                           ou None se o grafo for planar.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Verifica se o grafo é planar
    if nx.is_planar(g_nx):
        return None
    
    # Encontra um subgrafo de Kuratowski
    subgrafo = nx.kuratowski_subgraph(g_nx)
    
    # Retorna os vértices do subgrafo
    return list(subgrafo.nodes())


def calcular_faces(grafo: Grafo) -> List[List[Any]]:
    """
    Calcula as faces de um grafo planar.
    
    Uma face é uma região delimitada por arestas em um embedding planar.
    
    Args:
        grafo: Grafo planar a ser analisado.
        
    Returns:
        List[List[Any]]: Lista de faces, onde cada face é uma lista de vértices.
        
    Raises:
        ValueError: Se o grafo não for planar.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Verifica se o grafo é planar
    if not nx.is_planar(g_nx):
        raise ValueError("O grafo não é planar.")
    
    # Encontra um embedding planar
    embedding = nx.combinatorial_embedding(g_nx)
    
    # Calcula as faces
    faces = []
    for face in nx.face_boundaries(g_nx, embedding):
        faces.append(list(face))
    
    return faces


def verificar_formula_euler(grafo: Grafo) -> bool:
    """
    Verifica se o grafo planar satisfaz a fórmula de Euler: V - E + F = 2.
    
    Args:
        grafo: Grafo planar a ser analisado.
        
    Returns:
        bool: True se a fórmula de Euler é satisfeita, False caso contrário.
        
    Raises:
        ValueError: Se o grafo não for planar.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Verifica se o grafo é planar
    if not nx.is_planar(g_nx):
        raise ValueError("O grafo não é planar.")
    
    # Calcula o número de vértices (V)
    V = g_nx.number_of_nodes()
    
    # Calcula o número de arestas (E)
    E = g_nx.number_of_edges()
    
    # Calcula o número de faces (F)
    embedding = nx.combinatorial_embedding(g_nx)
    F = len(list(nx.face_boundaries(g_nx, embedding)))
    
    # Verifica a fórmula de Euler: V - E + F = 2
    return V - E + F == 2


def calcular_genero(grafo: Grafo) -> int:
    """
    Calcula o gênero aproximado de um grafo.
    
    O gênero de um grafo é o menor número de alças que devem ser adicionadas
    a uma esfera para que o grafo possa ser desenhado sem cruzamento de arestas.
    
    Args:
        grafo: Grafo a ser analisado.
        
    Returns:
        int: Gênero aproximado do grafo.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Calcula o número de vértices (V)
    V = g_nx.number_of_nodes()
    
    # Calcula o número de arestas (E)
    E = g_nx.number_of_edges()
    
    # Se o grafo é planar, seu gênero é 0
    if nx.is_planar(g_nx):
        return 0
    
    # Usa a fórmula de Euler generalizada para estimar o gênero:
    # V - E + F = 2 - 2g, onde g é o gênero
    # Reorganizando: g = (2 + E - V - F) / 2
    
    # Para um grafo conexo, podemos estimar F usando a fórmula de Euler para grafos planares
    # F ≈ 2 + E - V (assumindo planaridade)
    # Substituindo: g ≈ (E - V - 2) / 2 + 1 = (E - V) / 2
    
    # Esta é uma estimativa grosseira do limite inferior do gênero
    return max(0, (E - V + 1) // 2)


def eh_grafo_outerplanar(grafo: Grafo) -> bool:
    """
    Verifica se um grafo é outerplanar.
    
    Um grafo é outerplanar se pode ser desenhado no plano de forma que
    todos os vértices estejam na face externa.
    
    Args:
        grafo: Grafo a ser analisado.
        
    Returns:
        bool: True se o grafo é outerplanar, False caso contrário.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Usa a implementação do NetworkX para verificar se é outerplanar
    return nx.is_outerplanar(g_nx)


def calcular_espessura_aproximada(grafo: Grafo) -> int:
    """
    Calcula uma aproximação da espessura do grafo.
    
    A espessura de um grafo é o menor número de grafos planares em que
    suas arestas podem ser particionadas.
    
    Args:
        grafo: Grafo a ser analisado.
        
    Returns:
        int: Aproximação da espessura do grafo.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Se o grafo é planar, sua espessura é 1
    if nx.is_planar(g_nx):
        return 1
    
    # Calcula o número de vértices (V)
    V = g_nx.number_of_nodes()
    
    # Calcula o número de arestas (E)
    E = g_nx.number_of_edges()
    
    # Usa a fórmula aproximada: espessura ≈ ceil(E / (3V - 6))
    # Esta é uma estimativa baseada no fato de que um grafo planar tem no máximo 3V - 6 arestas
    import math
    return math.ceil(E / (3 * V - 6)) if V > 2 else 1
