"""
Implementação do algoritmo de Floyd-Warshall para encontrar caminhos mínimos entre todos os pares de vértices.

O algoritmo de Floyd-Warshall encontra os caminhos mais curtos entre todos os pares de vértices
em um grafo ponderado, permitindo arestas com pesos negativos desde que não haja ciclos negativos.
"""

from typing import Dict, List, Any, Tuple, Optional
import numpy as np
import networkx as nx
from ...core.grafo import Grafo


def floyd_warshall(grafo: Grafo) -> Tuple[Dict[Tuple[Any, Any], float], Dict[Tuple[Any, Any], Any]]:
    """
    Implementa o algoritmo de Floyd-Warshall para encontrar caminhos mínimos entre todos os pares de vértices.
    
    Args:
        grafo: Grafo ponderado.
        
    Returns:
        Tuple[Dict[Tuple[Any, Any], float], Dict[Tuple[Any, Any], Any]]: Tupla contendo:
            - Dicionário mapeando pares de vértices (origem, destino) para distâncias mínimas
            - Dicionário mapeando pares de vértices (origem, destino) para o próximo vértice no caminho
            
    Raises:
        ValueError: Se o grafo contiver ciclo de peso negativo.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Obtém a lista de vértices
    vertices = list(grafo.obter_vertices())
    n = len(vertices)
    
    # Cria um mapeamento de vértices para índices
    indice_vertice = {vertice: i for i, vertice in enumerate(vertices)}
    
    # Inicializa a matriz de distâncias
    dist = np.full((n, n), float('infinity'))
    
    # Inicializa a matriz de próximos vértices
    prox = np.full((n, n), None, dtype=object)
    
    # Inicializa as diagonais com zeros
    for i in range(n):
        dist[i, i] = 0
    
    # Inicializa com as arestas existentes
    for u, v, attrs in g_nx.edges(data=True):
        peso = attrs.get('weight', 1.0)
        i, j = indice_vertice[u], indice_vertice[v]
        dist[i, j] = peso
        prox[i, j] = v
    
    # Algoritmo de Floyd-Warshall
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i, k] != float('infinity') and dist[k, j] != float('infinity'):
                    if dist[i, j] > dist[i, k] + dist[k, j]:
                        dist[i, j] = dist[i, k] + dist[k, j]
                        prox[i, j] = prox[i, k]
    
    # Verifica se há ciclos de peso negativo
    for i in range(n):
        if dist[i, i] < 0:
            raise ValueError("O grafo contém ciclo de peso negativo.")
    
    # Converte as matrizes para dicionários
    distancias = {}
    proximos = {}
    
    for i in range(n):
        for j in range(n):
            u, v = vertices[i], vertices[j]
            distancias[(u, v)] = dist[i, j]
            proximos[(u, v)] = prox[i, j]
    
    return distancias, proximos


def reconstruir_caminho(proximos: Dict[Tuple[Any, Any], Any], origem: Any, destino: Any) -> List[Any]:
    """
    Reconstrói o caminho mínimo a partir do dicionário de próximos vértices.
    
    Args:
        proximos: Dicionário de próximos vértices.
        origem: Vértice de origem.
        destino: Vértice de destino.
        
    Returns:
        List[Any]: Lista de vértices que formam o caminho mínimo.
        
    Raises:
        ValueError: Se não existir caminho entre origem e destino.
    """
    if proximos[(origem, destino)] is None:
        raise ValueError(f"Não existe caminho de '{origem}' para '{destino}'.")
    
    caminho = [origem]
    while origem != destino:
        origem = proximos[(origem, destino)]
        caminho.append(origem)
    
    return caminho


def caminho_minimo(grafo: Grafo, origem: Any, destino: Any) -> Tuple[List[Any], float]:
    """
    Encontra o caminho mínimo entre dois vértices usando o algoritmo de Floyd-Warshall.
    
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
        ValueError: Se o grafo contiver ciclo de peso negativo.
    """
    # Verifica se os vértices existem no grafo
    if not grafo.existe_vertice(origem):
        raise ValueError(f"Vértice de origem '{origem}' não existe no grafo.")
    if not grafo.existe_vertice(destino):
        raise ValueError(f"Vértice de destino '{destino}' não existe no grafo.")
    
    # Executa o algoritmo de Floyd-Warshall
    distancias, proximos = floyd_warshall(grafo)
    
    # Verifica se existe caminho para o destino
    if distancias[(origem, destino)] == float('infinity'):
        raise ValueError(f"Não existe caminho de '{origem}' para '{destino}'.")
    
    # Reconstrói o caminho
    caminho = reconstruir_caminho(proximos, origem, destino)
    
    return caminho, distancias[(origem, destino)]


def calcular_diametro(grafo: Grafo) -> Tuple[float, Tuple[Any, Any]]:
    """
    Calcula o diâmetro do grafo usando o algoritmo de Floyd-Warshall.
    
    O diâmetro é a maior distância entre quaisquer dois vértices do grafo.
    
    Args:
        grafo: Grafo ponderado.
        
    Returns:
        Tuple[float, Tuple[Any, Any]]: Tupla contendo:
            - Valor do diâmetro
            - Par de vértices (u, v) que realiza o diâmetro
            
    Raises:
        ValueError: Se o grafo não for conexo.
        ValueError: Se o grafo contiver ciclo de peso negativo.
    """
    # Executa o algoritmo de Floyd-Warshall
    distancias, _ = floyd_warshall(grafo)
    
    # Inicializa o diâmetro
    diametro = 0
    par_diametro = None
    
    # Encontra a maior distância finita
    for (u, v), dist in distancias.items():
        if u != v and dist != float('infinity') and dist > diametro:
            diametro = dist
            par_diametro = (u, v)
    
    # Verifica se o grafo é conexo
    if diametro == 0 and len(grafo.obter_vertices()) > 1:
        raise ValueError("O grafo não é conexo.")
    
    return diametro, par_diametro


def calcular_centro(grafo: Grafo) -> List[Any]:
    """
    Calcula o centro do grafo usando o algoritmo de Floyd-Warshall.
    
    O centro é o conjunto de vértices cuja maior distância a qualquer outro vértice é mínima.
    
    Args:
        grafo: Grafo ponderado.
        
    Returns:
        List[Any]: Lista de vértices que formam o centro do grafo.
            
    Raises:
        ValueError: Se o grafo não for conexo.
        ValueError: Se o grafo contiver ciclo de peso negativo.
    """
    # Executa o algoritmo de Floyd-Warshall
    distancias, _ = floyd_warshall(grafo)
    
    # Calcula a excentricidade de cada vértice
    excentricidades = {}
    for vertice in grafo.obter_vertices():
        # A excentricidade é a maior distância do vértice a qualquer outro
        excentricidade = 0
        for outro in grafo.obter_vertices():
            if vertice != outro:
                dist = distancias[(vertice, outro)]
                if dist == float('infinity'):
                    # Se há um vértice inalcançável, o grafo não é conexo
                    raise ValueError("O grafo não é conexo.")
                excentricidade = max(excentricidade, dist)
        excentricidades[vertice] = excentricidade
    
    # Encontra a menor excentricidade
    min_excentricidade = min(excentricidades.values())
    
    # Retorna os vértices com a menor excentricidade
    return [v for v, e in excentricidades.items() if e == min_excentricidade]


def calcular_matriz_distancias(grafo: Grafo) -> Dict[Tuple[Any, Any], float]:
    """
    Calcula a matriz de distâncias entre todos os pares de vértices.
    
    Args:
        grafo: Grafo ponderado.
        
    Returns:
        Dict[Tuple[Any, Any], float]: Dicionário mapeando pares de vértices para suas distâncias mínimas.
            
    Raises:
        ValueError: Se o grafo contiver ciclo de peso negativo.
    """
    # Executa o algoritmo de Floyd-Warshall
    distancias, _ = floyd_warshall(grafo)
    
    return distancias


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
    
    # Obtém a lista de vértices
    vertices = list(grafo.obter_vertices())
    n = len(vertices)
    
    # Cria um mapeamento de vértices para índices
    indice_vertice = {vertice: i for i, vertice in enumerate(vertices)}
    vertice_indice = {i: vertice for i, vertice in enumerate(vertices)}
    
    # Inicializa a matriz de distâncias
    dist = np.full((n, n), float('infinity'))
    
    # Inicializa a matriz de predecessores
    pred = np.full((n, n), None, dtype=object)
    
    # Inicializa as diagonais com zeros
    for i in range(n):
        dist[i, i] = 0
    
    # Inicializa com as arestas existentes
    for u, v, attrs in g_nx.edges(data=True):
        peso = attrs.get('weight', 1.0)
        i, j = indice_vertice[u], indice_vertice[v]
        dist[i, j] = peso
        pred[i, j] = i
    
    # Algoritmo de Floyd-Warshall
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i, k] != float('infinity') and dist[k, j] != float('infinity'):
                    if dist[i, j] > dist[i, k] + dist[k, j]:
                        dist[i, j] = dist[i, k] + dist[k, j]
                        pred[i, j] = pred[k, j]
    
    # Verifica se há ciclos de peso negativo
    for i in range(n):
        if dist[i, i] < 0:
            # Encontrou um ciclo negativo, reconstrói o ciclo
            ciclo = []
            visitados = set()
            atual = i
            
            while atual not in visitados:
                visitados.add(atual)
                ciclo.append(vertice_indice[atual])
                atual = pred[atual, i]
            
            # Adiciona o vértice que fecha o ciclo
            ciclo.append(vertice_indice[atual])
            
            # Encontra o início do ciclo
            inicio = ciclo.index(vertice_indice[atual])
            
            # Retorna apenas o ciclo
            return ciclo[inicio:]
    
    # Não há ciclo negativo
    return None
