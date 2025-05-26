"""
Módulo de algoritmos de coloração.

Este módulo contém implementações de algoritmos para coloração de vértices e arestas em grafos.
"""

from typing import Dict, List, Any, Set, Tuple
import networkx as nx
from grafo_backend.core.grafo import Grafo


def coloracao_gulosa(grafo: Grafo, ordem_vertices: List[Any] = None) -> Dict[Any, int]:
    """
    Implementa o algoritmo guloso para coloração de vértices.
    
    Args:
        grafo: Grafo a ser colorido.
        ordem_vertices: Ordem de processamento dos vértices (opcional).
        
    Returns:
        Dict[Any, int]: Dicionário mapeando vértices para cores (representadas por inteiros).
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Define a ordem dos vértices
    if ordem_vertices is None:
        ordem_vertices = list(g_nx.nodes())
    
    # Inicializa o dicionário de cores
    cores = {}
    
    # Para cada vértice na ordem especificada
    for v in ordem_vertices:
        # Obtém as cores dos vizinhos
        cores_vizinhos = {cores.get(vizinho) for vizinho in g_nx.neighbors(v) if vizinho in cores}
        
        # Encontra a menor cor não utilizada pelos vizinhos
        cor = 0
        while cor in cores_vizinhos:
            cor += 1
        
        # Atribui a cor ao vértice
        cores[v] = cor
    
    return cores


def coloracao_welsh_powell(grafo: Grafo) -> Dict[Any, int]:
    """
    Implementa o algoritmo de Welsh-Powell para coloração de vértices.
    
    Args:
        grafo: Grafo a ser colorido.
        
    Returns:
        Dict[Any, int]: Dicionário mapeando vértices para cores (representadas por inteiros).
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Ordena os vértices por grau decrescente
    vertices_ordenados = sorted(g_nx.nodes(), key=lambda v: g_nx.degree(v), reverse=True)
    
    # Inicializa o dicionário de cores
    cores = {}
    
    # Para cada vértice na ordem de grau decrescente
    for v in vertices_ordenados:
        # Se o vértice já foi colorido, pula
        if v in cores:
            continue
        
        # Obtém as cores dos vizinhos
        cores_vizinhos = {cores.get(vizinho) for vizinho in g_nx.neighbors(v) if vizinho in cores}
        
        # Encontra a menor cor não utilizada pelos vizinhos
        cor = 0
        while cor in cores_vizinhos:
            cor += 1
        
        # Atribui a cor ao vértice
        cores[v] = cor
        
        # Tenta atribuir a mesma cor a outros vértices não adjacentes
        for u in vertices_ordenados:
            # Se o vértice já foi colorido, pula
            if u in cores:
                continue
            
            # Verifica se o vértice é adjacente a algum vértice já colorido com a cor atual
            adjacente_mesma_cor = False
            for vizinho in g_nx.neighbors(u):
                if vizinho in cores and cores[vizinho] == cor:
                    adjacente_mesma_cor = True
                    break
            
            # Se não for adjacente a nenhum vértice com a cor atual, atribui a cor
            if not adjacente_mesma_cor:
                cores[u] = cor
    
    return cores


def coloracao_dsatur(grafo: Grafo) -> Dict[Any, int]:
    """
    Implementa o algoritmo DSatur para coloração de vértices.
    
    Args:
        grafo: Grafo a ser colorido.
        
    Returns:
        Dict[Any, int]: Dicionário mapeando vértices para cores (representadas por inteiros).
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Inicializa o dicionário de cores
    cores = {}
    
    # Inicializa o grau de saturação de cada vértice
    saturacao = {v: 0 for v in g_nx.nodes()}
    
    # Enquanto houver vértices não coloridos
    while len(cores) < len(g_nx.nodes()):
        # Encontra o vértice não colorido com maior grau de saturação
        # Em caso de empate, escolhe o de maior grau
        max_saturacao = -1
        max_grau = -1
        vertice_escolhido = None
        
        for v in g_nx.nodes():
            if v in cores:
                continue
            
            if saturacao[v] > max_saturacao or (saturacao[v] == max_saturacao and g_nx.degree(v) > max_grau):
                max_saturacao = saturacao[v]
                max_grau = g_nx.degree(v)
                vertice_escolhido = v
        
        # Obtém as cores dos vizinhos
        cores_vizinhos = {cores.get(vizinho) for vizinho in g_nx.neighbors(vertice_escolhido) if vizinho in cores}
        
        # Encontra a menor cor não utilizada pelos vizinhos
        cor = 0
        while cor in cores_vizinhos:
            cor += 1
        
        # Atribui a cor ao vértice
        cores[vertice_escolhido] = cor
        
        # Atualiza o grau de saturação dos vizinhos não coloridos
        for vizinho in g_nx.neighbors(vertice_escolhido):
            if vizinho not in cores:
                # Calcula o novo grau de saturação
                cores_vizinhos_do_vizinho = {cores.get(v) for v in g_nx.neighbors(vizinho) if v in cores}
                saturacao[vizinho] = len(cores_vizinhos_do_vizinho)
    
    return cores


def coloracao_arestas(grafo: Grafo) -> Dict[Tuple[Any, Any], int]:
    """
    Implementa um algoritmo para coloração de arestas.
    
    Args:
        grafo: Grafo a ser colorido.
        
    Returns:
        Dict[Tuple[Any, Any], int]: Dicionário mapeando arestas para cores (representadas por inteiros).
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Inicializa o dicionário de cores
    cores = {}
    
    # Para cada aresta
    for u, v in g_nx.edges():
        # Obtém as cores das arestas adjacentes
        cores_adjacentes = set()
        
        # Arestas adjacentes a u
        for vizinho in g_nx.neighbors(u):
            if (u, vizinho) in cores:
                cores_adjacentes.add(cores[(u, vizinho)])
            elif (vizinho, u) in cores:
                cores_adjacentes.add(cores[(vizinho, u)])
        
        # Arestas adjacentes a v
        for vizinho in g_nx.neighbors(v):
            if (v, vizinho) in cores:
                cores_adjacentes.add(cores[(v, vizinho)])
            elif (vizinho, v) in cores:
                cores_adjacentes.add(cores[(vizinho, v)])
        
        # Encontra a menor cor não utilizada pelas arestas adjacentes
        cor = 0
        while cor in cores_adjacentes:
            cor += 1
        
        # Atribui a cor à aresta
        cores[(u, v)] = cor
    
    return cores


def calcular_numero_cromatico_aproximado(grafo: Grafo) -> int:
    """
    Calcula uma aproximação do número cromático do grafo.
    
    Args:
        grafo: Grafo a ser analisado.
        
    Returns:
        int: Aproximação do número cromático.
    """
    # Obtém a coloração usando o algoritmo DSatur
    coloracao = coloracao_dsatur(grafo)
    
    # O número cromático é o número de cores distintas utilizadas
    return len(set(coloracao.values()))
