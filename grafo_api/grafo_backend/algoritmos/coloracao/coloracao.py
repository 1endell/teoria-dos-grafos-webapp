"""
Implementação de algoritmos de coloração de grafos.

Este módulo contém implementações de algoritmos para coloração de vértices e arestas em grafos,
incluindo algoritmos gulosos e o algoritmo de Welsh-Powell.
"""

import networkx as nx
from typing import Dict, List, Any, Set, Tuple, Optional
from core.grafo import Grafo


def coloracao_gulosa(grafo: Grafo, ordem_vertices: List[Any] = None) -> Dict[Any, int]:
    """
    Implementa o algoritmo guloso de coloração de vértices.
    
    O algoritmo atribui a menor cor possível a cada vértice, garantindo que
    vértices adjacentes tenham cores diferentes.
    
    Args:
        grafo: Grafo a ser colorido.
        ordem_vertices: Ordem em que os vértices serão processados. Se None,
                       usa a ordem padrão do grafo.
        
    Returns:
        Dict[Any, int]: Dicionário mapeando vértices para suas cores (inteiros começando de 0).
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Se não foi fornecida uma ordem, usa a ordem padrão
    if ordem_vertices is None:
        ordem_vertices = list(g_nx.nodes())
    
    # Inicializa o dicionário de cores
    cores = {}
    
    # Para cada vértice na ordem especificada
    for v in ordem_vertices:
        # Obtém as cores já usadas pelos vizinhos
        cores_vizinhos = {cores.get(vizinho) for vizinho in g_nx.neighbors(v) if vizinho in cores}
        
        # Encontra a menor cor não usada pelos vizinhos
        cor = 0
        while cor in cores_vizinhos:
            cor += 1
        
        # Atribui a cor ao vértice
        cores[v] = cor
    
    return cores


def coloracao_welsh_powell(grafo: Grafo) -> Dict[Any, int]:
    """
    Implementa o algoritmo de Welsh-Powell para coloração de vértices.
    
    O algoritmo ordena os vértices por grau decrescente e atribui cores
    sequencialmente, garantindo que vértices adjacentes tenham cores diferentes.
    
    Args:
        grafo: Grafo a ser colorido.
        
    Returns:
        Dict[Any, int]: Dicionário mapeando vértices para suas cores (inteiros começando de 0).
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Ordena os vértices por grau decrescente
    vertices_ordenados = sorted(g_nx.nodes(), key=lambda v: g_nx.degree(v), reverse=True)
    
    # Usa o algoritmo guloso com a ordem específica
    return coloracao_gulosa(grafo, vertices_ordenados)


def coloracao_dsatur(grafo: Grafo) -> Dict[Any, int]:
    """
    Implementa o algoritmo DSatur (Degree of Saturation) para coloração de vértices.
    
    O algoritmo considera o grau de saturação (número de cores diferentes adjacentes)
    para decidir qual vértice colorir a seguir.
    
    Args:
        grafo: Grafo a ser colorido.
        
    Returns:
        Dict[Any, int]: Dicionário mapeando vértices para suas cores (inteiros começando de 0).
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Inicializa o dicionário de cores
    cores = {}
    
    # Inicializa o grau de saturação de cada vértice
    saturacao = {v: 0 for v in g_nx.nodes()}
    
    # Enquanto houver vértices não coloridos
    while len(cores) < len(g_nx.nodes()):
        # Encontra o vértice não colorido com maior saturação
        # Em caso de empate, escolhe o de maior grau
        max_saturacao = -1
        max_grau = -1
        proximo_vertice = None
        
        for v in g_nx.nodes():
            if v in cores:
                continue  # Vértice já colorido
            
            if saturacao[v] > max_saturacao or (saturacao[v] == max_saturacao and g_nx.degree(v) > max_grau):
                max_saturacao = saturacao[v]
                max_grau = g_nx.degree(v)
                proximo_vertice = v
        
        # Obtém as cores já usadas pelos vizinhos
        cores_vizinhos = {cores.get(vizinho) for vizinho in g_nx.neighbors(proximo_vertice) if vizinho in cores}
        
        # Encontra a menor cor não usada pelos vizinhos
        cor = 0
        while cor in cores_vizinhos:
            cor += 1
        
        # Atribui a cor ao vértice
        cores[proximo_vertice] = cor
        
        # Atualiza a saturação dos vizinhos não coloridos
        for vizinho in g_nx.neighbors(proximo_vertice):
            if vizinho not in cores:
                # Calcula o conjunto de cores adjacentes ao vizinho
                cores_adjacentes = {cores.get(v) for v in g_nx.neighbors(vizinho) if v in cores}
                saturacao[vizinho] = len(cores_adjacentes)
    
    return cores


def coloracao_arestas(grafo: Grafo) -> Dict[Tuple[Any, Any], int]:
    """
    Implementa um algoritmo para coloração de arestas.
    
    O algoritmo atribui cores às arestas de forma que arestas adjacentes
    (que compartilham um vértice) tenham cores diferentes.
    
    Args:
        grafo: Grafo a ser colorido.
        
    Returns:
        Dict[Tuple[Any, Any], int]: Dicionário mapeando arestas para suas cores.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Cria o grafo de linha (onde vértices são arestas do grafo original)
    linha_g = nx.line_graph(g_nx)
    
    # Aplica o algoritmo de coloração de vértices no grafo de linha
    cores_vertices = nx.greedy_color(linha_g)
    
    # Converte as cores de vértices do grafo de linha para cores de arestas do grafo original
    cores_arestas = {}
    for aresta_como_vertice, cor in cores_vertices.items():
        # No grafo de linha, os vértices são representados como tuplas (u, v)
        if isinstance(aresta_como_vertice, tuple):
            u, v = aresta_como_vertice
            cores_arestas[(u, v)] = cor
        else:
            # Para grafos direcionados, pode ser necessário um tratamento especial
            pass
    
    return cores_arestas


def calcular_numero_cromatico_aproximado(grafo: Grafo) -> int:
    """
    Calcula uma aproximação do número cromático do grafo.
    
    O número cromático é o menor número de cores necessárias para colorir
    os vértices de um grafo de forma que vértices adjacentes tenham cores diferentes.
    
    Args:
        grafo: Grafo a ser analisado.
        
    Returns:
        int: Aproximação do número cromático.
    """
    # Aplica o algoritmo DSatur, que geralmente produz boas colorações
    cores = coloracao_dsatur(grafo)
    
    # O número cromático aproximado é o número de cores distintas usadas
    return max(cores.values()) + 1 if cores else 0


def verificar_k_colorivel(grafo: Grafo, k: int) -> bool:
    """
    Verifica se um grafo é k-colorível.
    
    Um grafo é k-colorível se seus vértices podem ser coloridos com no máximo k cores
    de forma que vértices adjacentes tenham cores diferentes.
    
    Args:
        grafo: Grafo a ser verificado.
        k: Número de cores.
        
    Returns:
        bool: True se o grafo é k-colorível, False caso contrário.
    """
    # Para k=1, o grafo precisa ser independente (sem arestas)
    if k == 1:
        return grafo.numero_arestas() == 0
    
    # Para k=2, o grafo precisa ser bipartido
    if k == 2:
        return grafo.eh_bipartido()
    
    # Para k>=3, usamos uma heurística (DSatur) e verificamos se o número de cores é <= k
    cores = coloracao_dsatur(grafo)
    return max(cores.values()) + 1 <= k if cores else True


def obter_classes_de_cor(grafo: Grafo, cores: Dict[Any, int]) -> Dict[int, Set[Any]]:
    """
    Obtém as classes de cor de uma coloração.
    
    Uma classe de cor é o conjunto de vértices que receberam a mesma cor.
    
    Args:
        grafo: Grafo colorido.
        cores: Dicionário mapeando vértices para suas cores.
        
    Returns:
        Dict[int, Set[Any]]: Dicionário mapeando cores para conjuntos de vértices.
    """
    classes = {}
    
    for vertice, cor in cores.items():
        if cor not in classes:
            classes[cor] = set()
        classes[cor].add(vertice)
    
    return classes


def verificar_coloracao_valida(grafo: Grafo, cores: Dict[Any, int]) -> bool:
    """
    Verifica se uma coloração é válida.
    
    Uma coloração é válida se vértices adjacentes têm cores diferentes.
    
    Args:
        grafo: Grafo colorido.
        cores: Dicionário mapeando vértices para suas cores.
        
    Returns:
        bool: True se a coloração é válida, False caso contrário.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Verifica cada aresta
    for u, v in g_nx.edges():
        if u in cores and v in cores and cores[u] == cores[v]:
            return False
    
    return True
