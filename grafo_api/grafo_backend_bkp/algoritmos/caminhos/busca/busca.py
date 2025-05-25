"""
Implementação de algoritmos de busca em grafos: BFS e DFS.

Este módulo contém implementações dos algoritmos de busca em largura (BFS)
e busca em profundidade (DFS), fundamentais para diversos outros algoritmos
em teoria dos grafos.
"""

from typing import Dict, List, Any, Set, Tuple, Optional, Callable
from collections import deque
import networkx as nx
from ....core.grafo import Grafo


def bfs(grafo: Grafo, origem: Any) -> Tuple[Dict[Any, Any], Dict[Any, int]]:
    """
    Implementa o algoritmo de Busca em Largura (BFS).
    
    A BFS visita todos os vértices alcançáveis a partir da origem em ordem
    crescente de distância, explorando todos os vizinhos de um vértice antes
    de passar para os próximos níveis.
    
    Args:
        grafo: Grafo a ser percorrido.
        origem: Vértice de origem.
        
    Returns:
        Tuple[Dict[Any, Any], Dict[Any, int]]: Tupla contendo:
            - Dicionário de predecessores para reconstrução de caminhos
            - Dicionário de distâncias (em número de arestas) da origem a cada vértice
            
    Raises:
        ValueError: Se o vértice de origem não existir no grafo.
    """
    # Verifica se o vértice de origem existe no grafo
    if not grafo.existe_vertice(origem):
        raise ValueError(f"Vértice de origem '{origem}' não existe no grafo.")
    
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Inicializa as estruturas de dados
    visitados = {origem}
    fila = deque([origem])
    predecessores = {vertice: None for vertice in grafo.obter_vertices()}
    distancias = {vertice: float('infinity') for vertice in grafo.obter_vertices()}
    distancias[origem] = 0
    
    # Enquanto houver vértices na fila
    while fila:
        # Remove o primeiro vértice da fila
        vertice_atual = fila.popleft()
        
        # Para cada vizinho não visitado
        for vizinho in grafo.obter_adjacentes(vertice_atual):
            if vizinho not in visitados:
                # Marca como visitado
                visitados.add(vizinho)
                # Adiciona à fila
                fila.append(vizinho)
                # Registra o predecessor
                predecessores[vizinho] = vertice_atual
                # Registra a distância
                distancias[vizinho] = distancias[vertice_atual] + 1
    
    return predecessores, distancias


def dfs(grafo: Grafo, origem: Any) -> Tuple[Dict[Any, Any], Dict[Any, Tuple[int, int]]]:
    """
    Implementa o algoritmo de Busca em Profundidade (DFS).
    
    A DFS explora o grafo seguindo um caminho até o fim antes de retroceder,
    o que permite identificar propriedades como tempos de descoberta e finalização.
    
    Args:
        grafo: Grafo a ser percorrido.
        origem: Vértice de origem.
        
    Returns:
        Tuple[Dict[Any, Any], Dict[Any, Tuple[int, int]]]: Tupla contendo:
            - Dicionário de predecessores para reconstrução de caminhos
            - Dicionário mapeando vértices para tuplas (tempo_descoberta, tempo_finalização)
            
    Raises:
        ValueError: Se o vértice de origem não existir no grafo.
    """
    # Verifica se o vértice de origem existe no grafo
    if not grafo.existe_vertice(origem):
        raise ValueError(f"Vértice de origem '{origem}' não existe no grafo.")
    
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Inicializa as estruturas de dados
    predecessores = {vertice: None for vertice in grafo.obter_vertices()}
    tempos = {}  # Mapeamento de vértices para tuplas (tempo_descoberta, tempo_finalização)
    visitados = set()
    tempo_atual = [0]  # Lista com um elemento para permitir modificação na função interna
    
    def dfs_visita(vertice):
        # Marca o vértice como visitado
        visitados.add(vertice)
        # Registra o tempo de descoberta
        tempo_atual[0] += 1
        tempo_descoberta = tempo_atual[0]
        
        # Para cada vizinho não visitado
        for vizinho in grafo.obter_adjacentes(vertice):
            if vizinho not in visitados:
                # Registra o predecessor
                predecessores[vizinho] = vertice
                # Visita o vizinho recursivamente
                dfs_visita(vizinho)
        
        # Registra o tempo de finalização
        tempo_atual[0] += 1
        tempo_finalizacao = tempo_atual[0]
        # Armazena os tempos de descoberta e finalização
        tempos[vertice] = (tempo_descoberta, tempo_finalizacao)
    
    # Inicia a DFS a partir da origem
    dfs_visita(origem)
    
    # Para vértices não alcançáveis a partir da origem
    for vertice in grafo.obter_vertices():
        if vertice not in visitados:
            tempos[vertice] = (0, 0)  # Tempos zero para vértices não visitados
    
    return predecessores, tempos


def dfs_iterativo(grafo: Grafo, origem: Any) -> Tuple[Dict[Any, Any], Set[Any]]:
    """
    Implementa o algoritmo de Busca em Profundidade (DFS) de forma iterativa.
    
    Esta versão usa uma pilha explícita em vez de recursão, o que pode ser
    mais eficiente para grafos muito grandes.
    
    Args:
        grafo: Grafo a ser percorrido.
        origem: Vértice de origem.
        
    Returns:
        Tuple[Dict[Any, Any], Set[Any]]: Tupla contendo:
            - Dicionário de predecessores para reconstrução de caminhos
            - Conjunto de vértices visitados
            
    Raises:
        ValueError: Se o vértice de origem não existir no grafo.
    """
    # Verifica se o vértice de origem existe no grafo
    if not grafo.existe_vertice(origem):
        raise ValueError(f"Vértice de origem '{origem}' não existe no grafo.")
    
    # Inicializa as estruturas de dados
    predecessores = {vertice: None for vertice in grafo.obter_vertices()}
    visitados = set()
    pilha = [origem]
    
    # Enquanto houver vértices na pilha
    while pilha:
        # Remove o último vértice da pilha
        vertice_atual = pilha.pop()
        
        # Se o vértice já foi visitado, continua
        if vertice_atual in visitados:
            continue
        
        # Marca como visitado
        visitados.add(vertice_atual)
        
        # Para cada vizinho não visitado
        for vizinho in grafo.obter_adjacentes(vertice_atual):
            if vizinho not in visitados:
                # Adiciona à pilha
                pilha.append(vizinho)
                # Registra o predecessor se ainda não tiver um
                if predecessores[vizinho] is None:
                    predecessores[vizinho] = vertice_atual
    
    return predecessores, visitados


def iddfs(grafo: Grafo, origem: Any, profundidade_maxima: int) -> Tuple[Dict[Any, Any], Set[Any]]:
    """
    Implementa o algoritmo de Busca em Profundidade Iterativa (IDDFS).
    
    O IDDFS combina as vantagens da BFS (encontrar caminhos mais curtos) e da DFS
    (uso eficiente de memória) realizando DFS com profundidade limitada e
    aumentando gradualmente essa profundidade.
    
    Args:
        grafo: Grafo a ser percorrido.
        origem: Vértice de origem.
        profundidade_maxima: Profundidade máxima a ser explorada.
        
    Returns:
        Tuple[Dict[Any, Any], Set[Any]]: Tupla contendo:
            - Dicionário de predecessores para reconstrução de caminhos
            - Conjunto de vértices visitados
            
    Raises:
        ValueError: Se o vértice de origem não existir no grafo.
    """
    # Verifica se o vértice de origem existe no grafo
    if not grafo.existe_vertice(origem):
        raise ValueError(f"Vértice de origem '{origem}' não existe no grafo.")
    
    # Inicializa as estruturas de dados
    predecessores = {vertice: None for vertice in grafo.obter_vertices()}
    todos_visitados = set()
    
    # Para cada profundidade de 0 até profundidade_maxima
    for profundidade in range(profundidade_maxima + 1):
        visitados = set()
        
        def dfs_limitada(vertice, profundidade_atual):
            # Marca o vértice como visitado
            visitados.add(vertice)
            todos_visitados.add(vertice)
            
            # Se atingiu a profundidade limite, retorna
            if profundidade_atual == profundidade:
                return
            
            # Para cada vizinho não visitado nesta iteração
            for vizinho in grafo.obter_adjacentes(vertice):
                if vizinho not in visitados:
                    # Registra o predecessor se ainda não tiver um
                    if predecessores[vizinho] is None:
                        predecessores[vizinho] = vertice
                    # Visita o vizinho recursivamente
                    dfs_limitada(vizinho, profundidade_atual + 1)
        
        # Inicia a DFS limitada a partir da origem
        dfs_limitada(origem, 0)
    
    return predecessores, todos_visitados


def reconstruir_caminho_bfs(predecessores: Dict[Any, Any], origem: Any, destino: Any) -> List[Any]:
    """
    Reconstrói o caminho mais curto encontrado pela BFS.
    
    Args:
        predecessores: Dicionário de predecessores retornado pela BFS.
        origem: Vértice de origem.
        destino: Vértice de destino.
        
    Returns:
        List[Any]: Lista de vértices que formam o caminho mais curto.
        
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


def encontrar_componentes_conexos(grafo: Grafo) -> List[Set[Any]]:
    """
    Encontra todos os componentes conexos do grafo usando BFS.
    
    Args:
        grafo: Grafo a ser analisado.
        
    Returns:
        List[Set[Any]]: Lista de conjuntos, onde cada conjunto contém os vértices de um componente conexo.
    """
    # Obtém todos os vértices do grafo
    vertices = set(grafo.obter_vertices())
    componentes = []
    
    # Enquanto houver vértices não visitados
    while vertices:
        # Escolhe um vértice arbitrário
        origem = next(iter(vertices))
        
        # Executa BFS a partir desse vértice
        _, visitados = dfs_iterativo(grafo, origem)
        
        # Adiciona o componente conexo à lista
        componentes.append(visitados)
        
        # Remove os vértices visitados do conjunto de vértices restantes
        vertices -= visitados
    
    return componentes


def verificar_bipartido(grafo: Grafo) -> Tuple[bool, Dict[Any, int]]:
    """
    Verifica se um grafo é bipartido usando BFS.
    
    Um grafo é bipartido se seus vértices podem ser divididos em dois conjuntos
    disjuntos de modo que toda aresta conecte vértices de conjuntos diferentes.
    
    Args:
        grafo: Grafo a ser analisado.
        
    Returns:
        Tuple[bool, Dict[Any, int]]: Tupla contendo:
            - Booleano indicando se o grafo é bipartido
            - Dicionário mapeando vértices para suas cores (0 ou 1) se for bipartido,
              ou um dicionário vazio se não for bipartido
    """
    # Inicializa as cores dos vértices
    cores = {}
    
    # Para cada componente conexo
    for componente in encontrar_componentes_conexos(grafo):
        # Escolhe um vértice arbitrário do componente
        origem = next(iter(componente))
        
        # Inicializa a fila para BFS
        fila = deque([origem])
        cores[origem] = 0  # Atribui a cor 0 à origem
        
        # Enquanto houver vértices na fila
        while fila:
            # Remove o primeiro vértice da fila
            vertice_atual = fila.popleft()
            
            # Para cada vizinho
            for vizinho in grafo.obter_adjacentes(vertice_atual):
                # Se o vizinho ainda não tem cor
                if vizinho not in cores:
                    # Atribui a cor oposta
                    cores[vizinho] = 1 - cores[vertice_atual]
                    # Adiciona à fila
                    fila.append(vizinho)
                # Se o vizinho já tem cor e é a mesma do vértice atual
                elif cores[vizinho] == cores[vertice_atual]:
                    # O grafo não é bipartido
                    return False, {}
    
    # Se chegou até aqui, o grafo é bipartido
    return True, cores


def encontrar_ciclo(grafo: Grafo) -> Optional[List[Any]]:
    """
    Encontra um ciclo no grafo usando DFS, se existir.
    
    Args:
        grafo: Grafo a ser analisado.
        
    Returns:
        Optional[List[Any]]: Lista de vértices que formam um ciclo, ou None se não existir ciclo.
    """
    # Inicializa as estruturas de dados
    visitados = set()
    em_pilha = set()  # Vértices na pilha de recursão atual
    predecessores = {}
    
    def dfs_ciclo(vertice):
        # Marca o vértice como visitado e adiciona à pilha
        visitados.add(vertice)
        em_pilha.add(vertice)
        
        # Para cada vizinho
        for vizinho in grafo.obter_adjacentes(vertice):
            # Se o vizinho ainda não foi visitado
            if vizinho not in visitados:
                # Registra o predecessor
                predecessores[vizinho] = vertice
                # Se encontrou um ciclo na recursão
                if dfs_ciclo(vizinho):
                    return True
            # Se o vizinho está na pilha atual, encontrou um ciclo
            elif vizinho in em_pilha:
                # Reconstrói o ciclo
                ciclo = [vizinho]
                atual = vertice
                while atual != vizinho:
                    ciclo.append(atual)
                    atual = predecessores[atual]
                ciclo.append(vizinho)  # Fecha o ciclo
                ciclo.reverse()  # Inverte para ordem natural
                
                # Armazena o ciclo encontrado
                encontrar_ciclo.resultado = ciclo
                return True
        
        # Remove o vértice da pilha ao retornar
        em_pilha.remove(vertice)
        return False
    
    # Inicializa o resultado
    encontrar_ciclo.resultado = None
    
    # Para cada vértice não visitado
    for vertice in grafo.obter_vertices():
        if vertice not in visitados:
            predecessores = {vertice: None}
            if dfs_ciclo(vertice):
                return encontrar_ciclo.resultado
    
    # Se não encontrou ciclo
    return None


def ordenacao_topologica(grafo: Grafo) -> Optional[List[Any]]:
    """
    Realiza uma ordenação topológica do grafo usando DFS, se possível.
    
    Uma ordenação topológica é uma ordenação linear dos vértices de um grafo
    direcionado acíclico (DAG) tal que para toda aresta (u, v), u vem antes de v.
    
    Args:
        grafo: Grafo direcionado a ser analisado.
        
    Returns:
        Optional[List[Any]]: Lista de vértices em ordem topológica, ou None se o grafo contiver ciclos.
    """
    # Verifica se o grafo é direcionado
    g_nx = grafo.obter_grafo_networkx()
    if not isinstance(g_nx, nx.DiGraph):
        raise ValueError("A ordenação topológica só é definida para grafos direcionados.")
    
    # Verifica se o grafo contém ciclos
    if encontrar_ciclo(grafo) is not None:
        return None  # Não é possível realizar ordenação topológica em grafos com ciclos
    
    # Inicializa as estruturas de dados
    visitados = set()
    ordem_topologica = []
    
    def dfs_topologica(vertice):
        # Marca o vértice como visitado
        visitados.add(vertice)
        
        # Para cada vizinho não visitado
        for vizinho in grafo.obter_adjacentes(vertice):
            if vizinho not in visitados:
                dfs_topologica(vizinho)
        
        # Adiciona o vértice à ordem topológica
        ordem_topologica.append(vertice)
    
    # Para cada vértice não visitado
    for vertice in grafo.obter_vertices():
        if vertice not in visitados:
            dfs_topologica(vertice)
    
    # Inverte a ordem para obter a ordenação topológica correta
    return list(reversed(ordem_topologica))
