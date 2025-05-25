"""
Implementação do algoritmo de Dijkstra para encontrar caminhos mínimos em grafos ponderados.

O algoritmo de Dijkstra encontra o caminho mais curto entre um vértice de origem
e todos os outros vértices em um grafo ponderado com pesos não-negativos.
"""

import heapq
from typing import Dict, List, Any, Optional, Tuple, Set
import networkx as nx
from core.grafo import Grafo


def dijkstra(grafo: Grafo, origem: Any) -> Tuple[Dict[Any, float], Dict[Any, Any]]:
    """
    Implementa o algoritmo de Dijkstra para encontrar caminhos mínimos.
    
    Args:
        grafo: Grafo ponderado.
        origem: Vértice de origem.
        
    Returns:
        Tuple[Dict[Any, float], Dict[Any, Any]]: Tupla contendo:
            - Dicionário de distâncias mínimas para cada vértice
            - Dicionário de predecessores para reconstrução do caminho
            
    Raises:
        ValueError: Se o vértice de origem não existir no grafo.
        ValueError: Se o grafo contiver arestas com pesos negativos.
    """
    # Verifica se o vértice de origem existe no grafo
    if not grafo.existe_vertice(origem):
        raise ValueError(f"Vértice de origem '{origem}' não existe no grafo.")
    
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Verifica se há arestas com pesos negativos
    for u, v, attrs in g_nx.edges(data=True):
        peso = attrs.get('weight', 1.0)
        if peso < 0:
            raise ValueError("O algoritmo de Dijkstra não suporta arestas com pesos negativos.")
    
    # Inicializa as estruturas de dados
    distancias = {vertice: float('infinity') for vertice in grafo.obter_vertices()}
    distancias[origem] = 0
    predecessores = {vertice: None for vertice in grafo.obter_vertices()}
    visitados = set()
    
    # Fila de prioridade para selecionar o vértice com menor distância
    fila_prioridade = [(0, origem)]
    
    while fila_prioridade:
        # Obtém o vértice com menor distância
        dist_atual, vertice_atual = heapq.heappop(fila_prioridade)
        
        # Se o vértice já foi visitado, ignora
        if vertice_atual in visitados:
            continue
        
        # Marca o vértice como visitado
        visitados.add(vertice_atual)
        
        # Se a distância atual é maior que a distância conhecida, ignora
        if dist_atual > distancias[vertice_atual]:
            continue
        
        # Para cada vértice adjacente
        for adjacente in grafo.obter_adjacentes(vertice_atual):
            # Se o vértice adjacente já foi visitado, ignora
            if adjacente in visitados:
                continue
            
            # Calcula a nova distância
            peso = grafo.obter_peso_aresta(vertice_atual, adjacente)
            nova_distancia = distancias[vertice_atual] + peso
            
            # Se a nova distância é menor que a distância conhecida, atualiza
            if nova_distancia < distancias[adjacente]:
                distancias[adjacente] = nova_distancia
                predecessores[adjacente] = vertice_atual
                heapq.heappush(fila_prioridade, (nova_distancia, adjacente))
    
    return distancias, predecessores


def reconstruir_caminho(predecessores: Dict[Any, Any], origem: Any, destino: Any) -> List[Any]:
    """
    Reconstrói o caminho mínimo a partir do dicionário de predecessores.
    
    Args:
        predecessores: Dicionário de predecessores.
        origem: Vértice de origem.
        destino: Vértice de destino.
        
    Returns:
        List[Any]: Lista de vértices que formam o caminho mínimo.
        
    Raises:
        ValueError: Se não existir caminho entre origem e destino.
    """
    if predecessores[destino] is None and destino != origem:
        raise ValueError(f"Não existe caminho de '{origem}' para '{destino}'.")
    
    caminho = []
    vertice_atual = destino
    
    while vertice_atual is not None:
        caminho.append(vertice_atual)
        vertice_atual = predecessores[vertice_atual]
    
    # Inverte o caminho para que comece na origem
    return list(reversed(caminho))


def caminho_minimo(grafo: Grafo, origem: Any, destino: Any) -> Tuple[List[Any], float]:
    """
    Encontra o caminho mínimo entre dois vértices usando o algoritmo de Dijkstra.
    
    Args:
        grafo: Grafo ponderado.
        origem: Vértice de origem.
        destino: Vértice de destino.
        
    Returns:
        Tuple[List[Any], float]: Tupla contendo:
            - Lista de vértices que formam o caminho mínimo
            - Distância total do caminho
            
    Raises:
        ValueError: Se algum dos vértices não existir no grafo.
        ValueError: Se não existir caminho entre origem e destino.
        ValueError: Se o grafo contiver arestas com pesos negativos.
    """
    # Verifica se os vértices existem no grafo
    if not grafo.existe_vertice(origem):
        raise ValueError(f"Vértice de origem '{origem}' não existe no grafo.")
    if not grafo.existe_vertice(destino):
        raise ValueError(f"Vértice de destino '{destino}' não existe no grafo.")
    
    # Executa o algoritmo de Dijkstra
    distancias, predecessores = dijkstra(grafo, origem)
    
    # Verifica se existe caminho para o destino
    if distancias[destino] == float('infinity'):
        raise ValueError(f"Não existe caminho de '{origem}' para '{destino}'.")
    
    # Reconstrói o caminho
    caminho = reconstruir_caminho(predecessores, origem, destino)
    
    return caminho, distancias[destino]
