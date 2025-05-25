"""
Implementação do algoritmo de Tarjan para encontrar componentes fortemente conexos em grafos direcionados.

O algoritmo de Tarjan encontra todos os componentes fortemente conexos de um grafo direcionado
em tempo linear, usando uma única passagem de busca em profundidade.
"""

from typing import Dict, List, Any, Set, Tuple
import networkx as nx
from ...core.grafo import Grafo


def tarjan(grafo: Grafo) -> List[List[Any]]:
    """
    Implementa o algoritmo de Tarjan para encontrar componentes fortemente conexos.
    
    Um componente fortemente conexo é um subgrafo maximal onde existe um caminho
    entre qualquer par de vértices.
    
    Args:
        grafo: Grafo direcionado.
        
    Returns:
        List[List[Any]]: Lista de componentes fortemente conexos, onde cada componente
                       é uma lista de vértices.
                       
    Raises:
        ValueError: Se o grafo não for direcionado.
    """
    # Verifica se o grafo é direcionado
    g_nx = grafo.obter_grafo_networkx()
    if not isinstance(g_nx, nx.DiGraph):
        raise ValueError("O algoritmo de Tarjan requer um grafo direcionado.")
    
    # Inicializa as estruturas de dados
    indice = {}  # Mapeamento de vértices para seus índices de descoberta
    lowlink = {}  # Mapeamento de vértices para seus valores de lowlink
    na_pilha = set()  # Conjunto de vértices na pilha
    pilha = []  # Pilha de vértices
    
    # Índice atual para atribuição
    proximo_indice = [0]  # Lista com um elemento para permitir modificação na função interna
    
    # Lista de componentes fortemente conexos
    componentes = []
    
    def strongconnect(v):
        # Atribui o mesmo índice e lowlink inicialmente
        indice[v] = proximo_indice[0]
        lowlink[v] = proximo_indice[0]
        proximo_indice[0] += 1
        pilha.append(v)
        na_pilha.add(v)
        
        # Considera os sucessores de v
        for w in grafo.obter_adjacentes(v):
            if w not in indice:
                # Sucessor w ainda não foi visitado, visita recursivamente
                strongconnect(w)
                # Atualiza o lowlink de v com o de w
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif w in na_pilha:
                # Sucessor w está na pilha, portanto está no componente atual
                # Atualiza o lowlink de v com o índice de w
                lowlink[v] = min(lowlink[v], indice[w])
        
        # Se v é um nó raiz de um componente fortemente conexo
        if lowlink[v] == indice[v]:
            # Inicia um novo componente fortemente conexo
            componente = []
            while True:
                w = pilha.pop()
                na_pilha.remove(w)
                componente.append(w)
                if w == v:
                    break
            componentes.append(componente)
    
    # Executa o algoritmo para cada vértice não visitado
    for v in grafo.obter_vertices():
        if v not in indice:
            strongconnect(v)
    
    return componentes


def encontrar_componentes_fortemente_conexos(grafo: Grafo) -> List[List[Any]]:
    """
    Encontra todos os componentes fortemente conexos do grafo.
    
    Args:
        grafo: Grafo direcionado.
        
    Returns:
        List[List[Any]]: Lista de componentes fortemente conexos, onde cada componente
                       é uma lista de vértices.
                       
    Raises:
        ValueError: Se o grafo não for direcionado.
    """
    return tarjan(grafo)


def condensar_grafo(grafo: Grafo) -> Tuple[Grafo, Dict[Any, List[Any]]]:
    """
    Condensa um grafo direcionado em um grafo acíclico direcionado (DAG) de componentes fortemente conexos.
    
    Args:
        grafo: Grafo direcionado.
        
    Returns:
        Tuple[Grafo, Dict[Any, List[Any]]]: Tupla contendo:
            - Grafo condensado, onde cada vértice representa um componente fortemente conexo
            - Dicionário mapeando vértices do grafo condensado para listas de vértices originais
            
    Raises:
        ValueError: Se o grafo não for direcionado.
    """
    # Encontra os componentes fortemente conexos
    componentes = tarjan(grafo)
    
    # Cria um novo grafo para o grafo condensado
    grafo_condensado = Grafo("Grafo Condensado")
    
    # Mapeamento de vértices originais para seus componentes
    vertice_para_componente = {}
    for i, componente in enumerate(componentes):
        for v in componente:
            vertice_para_componente[v] = i
    
    # Mapeamento de componentes para seus vértices
    componente_para_vertices = {i: componente for i, componente in enumerate(componentes)}
    
    # Adiciona vértices ao grafo condensado
    for i in range(len(componentes)):
        grafo_condensado.adicionar_vertice(i)
    
    # Adiciona arestas entre componentes
    arestas_adicionadas = set()
    for u in grafo.obter_vertices():
        comp_u = vertice_para_componente[u]
        for v in grafo.obter_adjacentes(u):
            comp_v = vertice_para_componente[v]
            if comp_u != comp_v and (comp_u, comp_v) not in arestas_adicionadas:
                grafo_condensado.adicionar_aresta(comp_u, comp_v)
                arestas_adicionadas.add((comp_u, comp_v))
    
    return grafo_condensado, componente_para_vertices


def encontrar_pontes(grafo: Grafo) -> List[Tuple[Any, Any]]:
    """
    Encontra todas as pontes no grafo.
    
    Uma ponte é uma aresta cuja remoção aumenta o número de componentes conexos.
    
    Args:
        grafo: Grafo não direcionado.
        
    Returns:
        List[Tuple[Any, Any]]: Lista de arestas que são pontes.
        
    Raises:
        ValueError: Se o grafo for direcionado.
    """
    # Verifica se o grafo é não direcionado
    g_nx = grafo.obter_grafo_networkx()
    if isinstance(g_nx, nx.DiGraph):
        raise ValueError("O algoritmo de encontrar pontes requer um grafo não direcionado.")
    
    # Inicializa as estruturas de dados
    descoberta = {}  # Tempo de descoberta de cada vértice
    low = {}  # Valor low de cada vértice
    pai = {}  # Pai de cada vértice na árvore DFS
    pontes = []  # Lista de pontes encontradas
    
    # Tempo atual para atribuição
    tempo = [0]  # Lista com um elemento para permitir modificação na função interna
    
    def dfs(u):
        # Marca o vértice como visitado
        descoberta[u] = tempo[0]
        low[u] = tempo[0]
        tempo[0] += 1
        
        # Visita todos os vizinhos
        for v in grafo.obter_adjacentes(u):
            # Se o vizinho não foi visitado
            if v not in descoberta:
                pai[v] = u
                dfs(v)
                
                # Atualiza o valor low de u
                low[u] = min(low[u], low[v])
                
                # Se o valor low de v é maior que o tempo de descoberta de u,
                # então u-v é uma ponte
                if low[v] > descoberta[u]:
                    pontes.append((u, v))
            
            # Se o vizinho já foi visitado e não é o pai de u
            elif v != pai.get(u):
                # Atualiza o valor low de u
                low[u] = min(low[u], descoberta[v])
    
    # Executa DFS para cada vértice não visitado
    for u in grafo.obter_vertices():
        if u not in descoberta:
            pai[u] = None
            dfs(u)
    
    return pontes


def encontrar_pontos_articulacao(grafo: Grafo) -> Set[Any]:
    """
    Encontra todos os pontos de articulação no grafo.
    
    Um ponto de articulação é um vértice cuja remoção aumenta o número de componentes conexos.
    
    Args:
        grafo: Grafo não direcionado.
        
    Returns:
        Set[Any]: Conjunto de vértices que são pontos de articulação.
        
    Raises:
        ValueError: Se o grafo for direcionado.
    """
    # Verifica se o grafo é não direcionado
    g_nx = grafo.obter_grafo_networkx()
    if isinstance(g_nx, nx.DiGraph):
        raise ValueError("O algoritmo de encontrar pontos de articulação requer um grafo não direcionado.")
    
    # Inicializa as estruturas de dados
    descoberta = {}  # Tempo de descoberta de cada vértice
    low = {}  # Valor low de cada vértice
    pai = {}  # Pai de cada vértice na árvore DFS
    articulacoes = set()  # Conjunto de pontos de articulação
    
    # Tempo atual para atribuição
    tempo = [0]  # Lista com um elemento para permitir modificação na função interna
    
    def dfs(u):
        # Marca o vértice como visitado
        descoberta[u] = tempo[0]
        low[u] = tempo[0]
        tempo[0] += 1
        
        # Contador de filhos na árvore DFS
        filhos = 0
        
        # Visita todos os vizinhos
        for v in grafo.obter_adjacentes(u):
            # Se o vizinho não foi visitado
            if v not in descoberta:
                pai[v] = u
                filhos += 1
                dfs(v)
                
                # Atualiza o valor low de u
                low[u] = min(low[u], low[v])
                
                # Caso 1: u é raiz da árvore DFS e tem mais de um filho
                if pai[u] is None and filhos > 1:
                    articulacoes.add(u)
                
                # Caso 2: u não é raiz e o valor low de algum filho v é maior ou igual
                # ao tempo de descoberta de u
                if pai[u] is not None and low[v] >= descoberta[u]:
                    articulacoes.add(u)
            
            # Se o vizinho já foi visitado e não é o pai de u
            elif v != pai.get(u):
                # Atualiza o valor low de u
                low[u] = min(low[u], descoberta[v])
    
    # Executa DFS para cada vértice não visitado
    for u in grafo.obter_vertices():
        if u not in descoberta:
            pai[u] = None
            dfs(u)
    
    return articulacoes


def verificar_grafo_biconexo(grafo: Grafo) -> bool:
    """
    Verifica se um grafo é biconexo.
    
    Um grafo é biconexo se é conexo e não possui pontos de articulação.
    
    Args:
        grafo: Grafo não direcionado.
        
    Returns:
        bool: True se o grafo é biconexo, False caso contrário.
        
    Raises:
        ValueError: Se o grafo for direcionado.
    """
    # Verifica se o grafo é conexo
    g_nx = grafo.obter_grafo_networkx()
    if not nx.is_connected(g_nx):
        return False
    
    # Verifica se o grafo tem pontos de articulação
    articulacoes = encontrar_pontos_articulacao(grafo)
    
    # Um grafo é biconexo se não tem pontos de articulação
    return len(articulacoes) == 0
