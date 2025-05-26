"""
Implementação do algoritmo de Dijkstra para caminhos mínimos em grafos.
"""

from typing import Dict, Any, Tuple, List, Optional
import heapq

from grafo_backend.core.grafo import Grafo


def dijkstra(grafo: Grafo, origem: Any) -> Tuple[Dict[Any, float], Dict[Any, Any]]:
    """
    Implementa o algoritmo de Dijkstra para encontrar caminhos mínimos.
    
    Args:
        grafo: Grafo para executar o algoritmo.
        origem: Vértice de origem.
        
    Returns:
        Tuple[Dict[Any, float], Dict[Any, Any]]: Tupla contendo as distâncias e os predecessores.
    """
    # Inicializa as distâncias com infinito
    distancias = {v: float('inf') for v in grafo.obter_vertices()}
    distancias[origem] = 0
    
    # Inicializa os predecessores
    predecessores = {}
    
    # Inicializa a fila de prioridade
    fila = [(0, origem)]
    
    # Conjunto de vértices visitados
    visitados = set()
    
    while fila:
        # Obtém o vértice com menor distância
        dist_atual, v_atual = heapq.heappop(fila)
        
        # Se o vértice já foi visitado, ignora
        if v_atual in visitados:
            continue
        
        # Marca o vértice como visitado
        visitados.add(v_atual)
        
        # Para cada vizinho do vértice atual
        for vizinho in grafo.obter_vizinhos(v_atual):
            # Se o vizinho já foi visitado, ignora
            if vizinho in visitados:
                continue
            
            # Obtém o peso da aresta
            peso = 1.0
            if hasattr(grafo, 'obter_peso_aresta'):
                peso = grafo.obter_peso_aresta(v_atual, vizinho)
            
            # Calcula a nova distância
            nova_dist = dist_atual + peso
            
            # Se a nova distância for menor que a distância atual, atualiza
            if nova_dist < distancias[vizinho]:
                distancias[vizinho] = nova_dist
                predecessores[vizinho] = v_atual
                heapq.heappush(fila, (nova_dist, vizinho))
    
    return distancias, predecessores
