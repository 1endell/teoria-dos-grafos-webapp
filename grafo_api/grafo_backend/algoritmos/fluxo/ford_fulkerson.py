"""
Implementação do algoritmo de Ford-Fulkerson para encontrar o fluxo máximo em redes.

O algoritmo de Ford-Fulkerson encontra o fluxo máximo em uma rede de fluxo,
utilizando caminhos de aumento iterativamente até que não seja possível
aumentar o fluxo.
"""

from typing import Dict, List, Any, Optional, Tuple, Set
import networkx as nx
from collections import deque
from ...core.grafo import Grafo


def bfs_caminho_aumento(grafo: nx.DiGraph, fonte: Any, sumidouro: Any, 
                       capacidade_residual: Dict[Tuple[Any, Any], float]) -> Tuple[bool, Dict[Any, Any]]:
    """
    Busca em largura para encontrar um caminho de aumento na rede residual.
    
    Args:
        grafo: Grafo direcionado representando a rede.
        fonte: Vértice fonte.
        sumidouro: Vértice sumidouro.
        capacidade_residual: Dicionário de capacidades residuais.
        
    Returns:
        Tuple[bool, Dict[Any, Any]]: Tupla contendo:
            - Booleano indicando se existe um caminho de aumento
            - Dicionário de predecessores para reconstrução do caminho
    """
    # Inicializa o dicionário de predecessores
    predecessores = {vertice: None for vertice in grafo.nodes()}
    
    # Inicializa a fila para BFS
    fila = deque([fonte])
    
    # Marca a fonte como visitada
    visitados = {fonte}
    
    # Enquanto houver vértices na fila
    while fila:
        # Remove o primeiro vértice da fila
        vertice_atual = fila.popleft()
        
        # Para cada vértice adjacente
        for adjacente in grafo.neighbors(vertice_atual):
            # Se o vértice adjacente não foi visitado e há capacidade residual
            if adjacente not in visitados and capacidade_residual.get((vertice_atual, adjacente), 0) > 0:
                # Marca o vértice como visitado
                visitados.add(adjacente)
                # Registra o predecessor
                predecessores[adjacente] = vertice_atual
                # Adiciona o vértice à fila
                fila.append(adjacente)
                
                # Se chegou ao sumidouro, termina a busca
                if adjacente == sumidouro:
                    return True, predecessores
    
    # Se não encontrou caminho até o sumidouro
    return False, predecessores


def ford_fulkerson(grafo: Grafo, fonte: Any, sumidouro: Any) -> Tuple[Dict[Tuple[Any, Any], float], float]:
    """
    Implementa o algoritmo de Ford-Fulkerson para encontrar o fluxo máximo.
    
    Args:
        grafo: Grafo direcionado representando a rede de fluxo.
        fonte: Vértice fonte.
        sumidouro: Vértice sumidouro.
        
    Returns:
        Tuple[Dict[Tuple[Any, Any], float], float]: Tupla contendo:
            - Dicionário de fluxos nas arestas
            - Valor do fluxo máximo
            
    Raises:
        ValueError: Se algum dos vértices não existir no grafo.
        ValueError: Se o grafo não for direcionado.
        ValueError: Se houver arestas com capacidades negativas.
    """
    # Verifica se os vértices existem no grafo
    if not grafo.existe_vertice(fonte):
        raise ValueError(f"Vértice fonte '{fonte}' não existe no grafo.")
    if not grafo.existe_vertice(sumidouro):
        raise ValueError(f"Vértice sumidouro '{sumidouro}' não existe no grafo.")
    
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Verifica se o grafo é direcionado
    if not isinstance(g_nx, nx.DiGraph):
        raise ValueError("O algoritmo de Ford-Fulkerson requer um grafo direcionado.")
    
    # Verifica se há arestas com capacidades negativas
    for u, v, attrs in g_nx.edges(data=True):
        capacidade = attrs.get('capacity', attrs.get('weight', 1.0))
        if capacidade < 0:
            raise ValueError("O algoritmo de Ford-Fulkerson não suporta arestas com capacidades negativas.")
    
    # Inicializa o fluxo com zero em todas as arestas
    fluxo = {(u, v): 0 for u, v in g_nx.edges()}
    
    # Inicializa a capacidade residual
    capacidade_residual = {}
    for u, v, attrs in g_nx.edges(data=True):
        # Usa o atributo 'capacity' se existir, caso contrário usa 'weight' ou 1.0
        capacidade = attrs.get('capacity', attrs.get('weight', 1.0))
        capacidade_residual[(u, v)] = capacidade
        # Inicializa a capacidade residual da aresta reversa
        capacidade_residual[(v, u)] = 0
    
    # Enquanto existir um caminho de aumento
    existe_caminho, predecessores = bfs_caminho_aumento(g_nx, fonte, sumidouro, capacidade_residual)
    while existe_caminho:
        # Encontra a capacidade residual mínima no caminho
        caminho_residual = float('infinity')
        v = sumidouro
        while v != fonte:
            u = predecessores[v]
            caminho_residual = min(caminho_residual, capacidade_residual[(u, v)])
            v = u
        
        # Atualiza o fluxo e a capacidade residual ao longo do caminho
        v = sumidouro
        while v != fonte:
            u = predecessores[v]
            fluxo[(u, v)] = fluxo.get((u, v), 0) + caminho_residual
            fluxo[(v, u)] = fluxo.get((v, u), 0) - caminho_residual
            capacidade_residual[(u, v)] -= caminho_residual
            capacidade_residual[(v, u)] += caminho_residual
            v = u
        
        # Busca um novo caminho de aumento
        existe_caminho, predecessores = bfs_caminho_aumento(g_nx, fonte, sumidouro, capacidade_residual)
    
    # Calcula o fluxo máximo
    fluxo_maximo = sum(fluxo.get((fonte, v), 0) for v in g_nx.neighbors(fonte))
    
    return fluxo, fluxo_maximo


def fluxo_maximo(grafo: Grafo, fonte: Any, sumidouro: Any) -> Tuple[Dict[Tuple[Any, Any], float], float]:
    """
    Encontra o fluxo máximo em uma rede usando o algoritmo de Ford-Fulkerson.
    
    Args:
        grafo: Grafo direcionado representando a rede de fluxo.
        fonte: Vértice fonte.
        sumidouro: Vértice sumidouro.
        
    Returns:
        Tuple[Dict[Tuple[Any, Any], float], float]: Tupla contendo:
            - Dicionário de fluxos nas arestas
            - Valor do fluxo máximo
            
    Raises:
        ValueError: Se algum dos vértices não existir no grafo.
        ValueError: Se o grafo não for direcionado.
        ValueError: Se houver arestas com capacidades negativas.
    """
    return ford_fulkerson(grafo, fonte, sumidouro)


def corte_minimo(grafo: Grafo, fonte: Any, sumidouro: Any) -> Tuple[Set[Any], Set[Any], float]:
    """
    Encontra o corte mínimo em uma rede usando o algoritmo de Ford-Fulkerson.
    
    Args:
        grafo: Grafo direcionado representando a rede de fluxo.
        fonte: Vértice fonte.
        sumidouro: Vértice sumidouro.
        
    Returns:
        Tuple[Set[Any], Set[Any], float]: Tupla contendo:
            - Conjunto de vértices do lado da fonte
            - Conjunto de vértices do lado do sumidouro
            - Capacidade do corte mínimo
            
    Raises:
        ValueError: Se algum dos vértices não existir no grafo.
        ValueError: Se o grafo não for direcionado.
        ValueError: Se houver arestas com capacidades negativas.
    """
    # Executa o algoritmo de Ford-Fulkerson
    fluxo, valor_fluxo = ford_fulkerson(grafo, fonte, sumidouro)
    
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Inicializa a capacidade residual
    capacidade_residual = {}
    for u, v, attrs in g_nx.edges(data=True):
        capacidade = attrs.get('capacity', attrs.get('weight', 1.0))
        capacidade_residual[(u, v)] = capacidade - fluxo.get((u, v), 0)
    
    # Encontra os vértices alcançáveis a partir da fonte na rede residual
    alcancaveis = set()
    fila = deque([fonte])
    alcancaveis.add(fonte)
    
    while fila:
        vertice_atual = fila.popleft()
        for adjacente in g_nx.neighbors(vertice_atual):
            if adjacente not in alcancaveis and capacidade_residual.get((vertice_atual, adjacente), 0) > 0:
                alcancaveis.add(adjacente)
                fila.append(adjacente)
    
    # O conjunto de vértices do lado do sumidouro é o complemento
    nao_alcancaveis = set(g_nx.nodes()) - alcancaveis
    
    # Calcula a capacidade do corte
    capacidade_corte = 0
    for u in alcancaveis:
        for v in nao_alcancaveis:
            if g_nx.has_edge(u, v):
                capacidade = g_nx.edges[u, v].get('capacity', g_nx.edges[u, v].get('weight', 1.0))
                capacidade_corte += capacidade
    
    return alcancaveis, nao_alcancaveis, capacidade_corte
