"""
Implementação do algoritmo de Bellman-Ford para encontrar caminhos mínimos em grafos ponderados.

O algoritmo de Bellman-Ford encontra o caminho mais curto entre um vértice de origem
e todos os outros vértices em um grafo ponderado, mesmo com arestas de peso negativo.
Também detecta ciclos de peso negativo.
"""

from typing import Dict, List, Any, Optional, Tuple
import networkx as nx
from ...core.grafo import Grafo


def bellman_ford(grafo: Grafo, origem: Any) -> Tuple[Dict[Any, float], Dict[Any, Any], bool]:
    """
    Implementa o algoritmo de Bellman-Ford para encontrar caminhos mínimos.
    
    Args:
        grafo: Grafo ponderado.
        origem: Vértice de origem.
        
    Returns:
        Tuple[Dict[Any, float], Dict[Any, Any], bool]: Tupla contendo:
            - Dicionário de distâncias mínimas para cada vértice
            - Dicionário de predecessores para reconstrução do caminho
            - Booleano indicando se existe ciclo de peso negativo alcançável a partir da origem
            
    Raises:
        ValueError: Se o vértice de origem não existir no grafo.
    """
    # Verifica se o vértice de origem existe no grafo
    if not grafo.existe_vertice(origem):
        raise ValueError(f"Vértice de origem '{origem}' não existe no grafo.")
    
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Inicializa as estruturas de dados
    distancias = {vertice: float('infinity') for vertice in grafo.obter_vertices()}
    distancias[origem] = 0
    predecessores = {vertice: None for vertice in grafo.obter_vertices()}
    
    # Obtém todas as arestas do grafo
    arestas = []
    for u, v, attrs in g_nx.edges(data=True):
        peso = attrs.get('weight', 1.0)
        arestas.append((u, v, peso))
    
    # Relaxamento das arestas |V| - 1 vezes
    n_vertices = len(grafo.obter_vertices())
    for _ in range(n_vertices - 1):
        for u, v, peso in arestas:
            # Relaxamento: se podemos melhorar o caminho para v passando por u
            if distancias[u] != float('infinity') and distancias[u] + peso < distancias[v]:
                distancias[v] = distancias[u] + peso
                predecessores[v] = u
    
    # Verifica se há ciclos de peso negativo
    ciclo_negativo = False
    for u, v, peso in arestas:
        if distancias[u] != float('infinity') and distancias[u] + peso < distancias[v]:
            ciclo_negativo = True
            break
    
    return distancias, predecessores, ciclo_negativo


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
    Encontra o caminho mínimo entre dois vértices usando o algoritmo de Bellman-Ford.
    
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
        ValueError: Se existir ciclo de peso negativo alcançável a partir da origem.
    """
    # Verifica se os vértices existem no grafo
    if not grafo.existe_vertice(origem):
        raise ValueError(f"Vértice de origem '{origem}' não existe no grafo.")
    if not grafo.existe_vertice(destino):
        raise ValueError(f"Vértice de destino '{destino}' não existe no grafo.")
    
    # Executa o algoritmo de Bellman-Ford
    distancias, predecessores, ciclo_negativo = bellman_ford(grafo, origem)
    
    # Verifica se existe ciclo de peso negativo
    if ciclo_negativo:
        raise ValueError("O grafo contém ciclo de peso negativo alcançável a partir da origem.")
    
    # Verifica se existe caminho para o destino
    if distancias[destino] == float('infinity'):
        raise ValueError(f"Não existe caminho de '{origem}' para '{destino}'.")
    
    # Reconstrói o caminho
    caminho = reconstruir_caminho(predecessores, origem, destino)
    
    return caminho, distancias[destino]


def detectar_ciclo_negativo(grafo: Grafo) -> Optional[List[Any]]:
    """
    Detecta um ciclo de peso negativo no grafo, se existir.
    
    Args:
        grafo: Grafo ponderado.
        
    Returns:
        Optional[List[Any]]: Lista de vértices que formam um ciclo de peso negativo,
                           ou None se não existir ciclo de peso negativo.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Adiciona um vértice artificial conectado a todos os outros
    vertice_artificial = object()  # Objeto único para garantir que não colide com vértices existentes
    
    # Cria um novo grafo com o vértice artificial
    novo_grafo = Grafo("Grafo com vértice artificial")
    
    # Adiciona todos os vértices e arestas do grafo original
    for vertice in grafo.obter_vertices():
        novo_grafo.adicionar_vertice(vertice)
    
    for u, v, attrs in g_nx.edges(data=True):
        peso = attrs.get('weight', 1.0)
        novo_grafo.adicionar_aresta(u, v, peso)
    
    # Adiciona o vértice artificial e arestas com peso zero para todos os vértices
    novo_grafo.adicionar_vertice(vertice_artificial)
    for vertice in grafo.obter_vertices():
        novo_grafo.adicionar_aresta(vertice_artificial, vertice, 0)
    
    # Executa o algoritmo de Bellman-Ford a partir do vértice artificial
    distancias, predecessores, ciclo_negativo = bellman_ford(novo_grafo, vertice_artificial)
    
    # Se não há ciclo negativo, retorna None
    if not ciclo_negativo:
        return None
    
    # Encontra um vértice que faz parte de um ciclo negativo
    g_novo_nx = novo_grafo.obter_grafo_networkx()
    for u, v, attrs in g_novo_nx.edges(data=True):
        peso = attrs.get('weight', 1.0)
        if distancias[u] != float('infinity') and distancias[u] + peso < distancias[v]:
            # Encontrou uma aresta que viola a condição de otimalidade
            # Agora precisamos encontrar o ciclo
            
            # Marca os vértices visitados para encontrar o ciclo
            visitados = set()
            vertice_atual = u
            
            # Avança até encontrar um vértice já visitado (que faz parte do ciclo)
            while vertice_atual not in visitados and vertice_atual != vertice_artificial:
                visitados.add(vertice_atual)
                vertice_atual = predecessores[vertice_atual]
            
            # Se chegou ao vértice artificial, tenta outra aresta
            if vertice_atual == vertice_artificial:
                continue
            
            # Reconstrói o ciclo
            ciclo = [vertice_atual]
            v_ciclo = predecessores[vertice_atual]
            while v_ciclo != vertice_atual:
                ciclo.append(v_ciclo)
                v_ciclo = predecessores[v_ciclo]
            
            # Inverte o ciclo para ordem natural
            ciclo.reverse()
            
            return ciclo
    
    # Não deveria chegar aqui se ciclo_negativo for True
    return None
