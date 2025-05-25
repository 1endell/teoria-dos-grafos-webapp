"""
Implementação do algoritmo de Edmonds-Karp para encontrar o fluxo máximo em redes.

O algoritmo de Edmonds-Karp é uma implementação específica do método de Ford-Fulkerson
que usa BFS para encontrar caminhos de aumento, garantindo complexidade polinomial.
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


def edmonds_karp(grafo: Grafo, fonte: Any, sumidouro: Any) -> Tuple[Dict[Tuple[Any, Any], float], float]:
    """
    Implementa o algoritmo de Edmonds-Karp para encontrar o fluxo máximo.
    
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
        raise ValueError("O algoritmo de Edmonds-Karp requer um grafo direcionado.")
    
    # Verifica se há arestas com capacidades negativas
    for u, v, attrs in g_nx.edges(data=True):
        capacidade = attrs.get('capacity', attrs.get('weight', 1.0))
        if capacidade < 0:
            raise ValueError("O algoritmo de Edmonds-Karp não suporta arestas com capacidades negativas.")
    
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
    
    # Contador de iterações para análise de desempenho
    iteracoes = 0
    
    # Enquanto existir um caminho de aumento
    existe_caminho, predecessores = bfs_caminho_aumento(g_nx, fonte, sumidouro, capacidade_residual)
    while existe_caminho:
        iteracoes += 1
        
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
    
    # Registra o número de iterações para análise
    edmonds_karp.iteracoes = iteracoes
    
    return fluxo, fluxo_maximo


def fluxo_maximo(grafo: Grafo, fonte: Any, sumidouro: Any) -> Tuple[Dict[Tuple[Any, Any], float], float]:
    """
    Encontra o fluxo máximo em uma rede usando o algoritmo de Edmonds-Karp.
    
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
    return edmonds_karp(grafo, fonte, sumidouro)


def corte_minimo(grafo: Grafo, fonte: Any, sumidouro: Any) -> Tuple[Set[Any], Set[Any], float]:
    """
    Encontra o corte mínimo em uma rede usando o algoritmo de Edmonds-Karp.
    
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
    # Executa o algoritmo de Edmonds-Karp
    fluxo, valor_fluxo = edmonds_karp(grafo, fonte, sumidouro)
    
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


def comparar_desempenho_ford_fulkerson_edmonds_karp(grafo: Grafo, fonte: Any, sumidouro: Any) -> Dict[str, Any]:
    """
    Compara o desempenho dos algoritmos de Ford-Fulkerson e Edmonds-Karp.
    
    Args:
        grafo: Grafo direcionado representando a rede de fluxo.
        fonte: Vértice fonte.
        sumidouro: Vértice sumidouro.
        
    Returns:
        Dict[str, Any]: Dicionário com métricas de comparação.
    """
    # Importa o algoritmo de Ford-Fulkerson
    from algoritmos.fluxo.ford_fulkerson import ford_fulkerson
    
    # Executa o algoritmo de Ford-Fulkerson
    fluxo_ff, valor_ff = ford_fulkerson(grafo, fonte, sumidouro)
    
    # Executa o algoritmo de Edmonds-Karp
    fluxo_ek, valor_ek = edmonds_karp(grafo, fonte, sumidouro)
    
    # Compara os resultados
    return {
        "valor_fluxo_ford_fulkerson": valor_ff,
        "valor_fluxo_edmonds_karp": valor_ek,
        "fluxos_iguais": valor_ff == valor_ek,
        "iteracoes_edmonds_karp": getattr(edmonds_karp, 'iteracoes', 0)
    }


def encontrar_emparelhamento_bipartido(grafo: Grafo, conjunto_a: Set[Any], conjunto_b: Set[Any]) -> Dict[Any, Any]:
    """
    Encontra um emparelhamento máximo em um grafo bipartido usando o algoritmo de Edmonds-Karp.
    
    Args:
        grafo: Grafo não direcionado bipartido.
        conjunto_a: Primeiro conjunto de vértices da bipartição.
        conjunto_b: Segundo conjunto de vértices da bipartição.
        
    Returns:
        Dict[Any, Any]: Dicionário mapeando vértices para seus pares no emparelhamento.
        
    Raises:
        ValueError: Se o grafo não for bipartido com a bipartição especificada.
    """
    # Verifica se a bipartição é válida
    for u, v in grafo.obter_arestas():
        if (u in conjunto_a and v in conjunto_a) or (u in conjunto_b and v in conjunto_b):
            raise ValueError("A bipartição especificada não é válida para o grafo.")
    
    # Cria um grafo de fluxo
    grafo_fluxo = Grafo("Grafo de Fluxo")
    
    # Adiciona vértices fonte e sumidouro
    fonte = "fonte"
    sumidouro = "sumidouro"
    grafo_fluxo.adicionar_vertice(fonte)
    grafo_fluxo.adicionar_vertice(sumidouro)
    
    # Adiciona todos os vértices do grafo original
    for vertice in grafo.obter_vertices():
        grafo_fluxo.adicionar_vertice(vertice)
    
    # Adiciona arestas da fonte para o conjunto A
    for vertice in conjunto_a:
        grafo_fluxo.adicionar_aresta(fonte, vertice, 1.0)
    
    # Adiciona arestas do conjunto B para o sumidouro
    for vertice in conjunto_b:
        grafo_fluxo.adicionar_aresta(vertice, sumidouro, 1.0)
    
    # Adiciona arestas entre os conjuntos A e B
    for u, v in grafo.obter_arestas():
        if u in conjunto_a and v in conjunto_b:
            grafo_fluxo.adicionar_aresta(u, v, 1.0)
        elif u in conjunto_b and v in conjunto_a:
            grafo_fluxo.adicionar_aresta(v, u, 1.0)
    
    # Executa o algoritmo de Edmonds-Karp
    fluxo, _ = edmonds_karp(grafo_fluxo, fonte, sumidouro)
    
    # Constrói o emparelhamento
    emparelhamento = {}
    for u in conjunto_a:
        for v in conjunto_b:
            if fluxo.get((u, v), 0) > 0:
                emparelhamento[u] = v
                emparelhamento[v] = u
    
    return emparelhamento
