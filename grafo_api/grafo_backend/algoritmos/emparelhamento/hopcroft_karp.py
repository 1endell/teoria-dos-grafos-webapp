"""
Implementação do algoritmo de Hopcroft-Karp para emparelhamento máximo em grafos bipartidos.

O algoritmo de Hopcroft-Karp encontra um emparelhamento máximo em um grafo bipartido
com complexidade de tempo O(E * sqrt(V)), onde E é o número de arestas e V é o número de vértices.
"""

from typing import Dict, List, Any, Tuple, Set, Optional
from collections import deque
import networkx as nx
from grafo_backend.core.grafo import Grafo


def hopcroft_karp(grafo: Grafo) -> Dict[Any, Any]:
    """
    Implementa o algoritmo de Hopcroft-Karp para encontrar um emparelhamento máximo em um grafo bipartido.
    
    Args:
        grafo: Grafo bipartido não direcionado.
        
    Returns:
        Dict[Any, Any]: Dicionário mapeando vértices do conjunto A para seus pares no conjunto B.
            
    Raises:
        ValueError: Se o grafo for direcionado.
        ValueError: Se o grafo não for bipartido.
    """
    # Verifica se o grafo é direcionado
    if grafo.eh_direcionado():
        raise ValueError("O algoritmo de Hopcroft-Karp só é aplicável a grafos não direcionados.")
    
    # Verifica se o grafo é bipartido
    from algoritmos.caminhos.busca.busca import verificar_bipartido
    eh_bipartido, cores = verificar_bipartido(grafo)
    
    if not eh_bipartido:
        raise ValueError("O algoritmo de Hopcroft-Karp só é aplicável a grafos bipartidos.")
    
    # Divide os vértices em dois conjuntos: A (cor 0) e B (cor 1)
    conjunto_a = {v for v, cor in cores.items() if cor == 0}
    conjunto_b = {v for v, cor in cores.items() if cor == 1}
    
    # Inicializa o emparelhamento
    emparelhamento = {}  # Mapeamento de vértices do conjunto A para seus pares no conjunto B
    emparelhamento_reverso = {}  # Mapeamento de vértices do conjunto B para seus pares no conjunto A
    
    # Função para encontrar um caminho aumentante usando BFS
    def bfs() -> bool:
        fila = deque()
        
        # Adiciona todos os vértices não emparelhados do conjunto A à fila
        for v in conjunto_a:
            if v not in emparelhamento:
                distancias[v] = 0
                fila.append(v)
            else:
                distancias[v] = float('infinity')
        
        distancias[None] = float('infinity')
        
        # BFS para encontrar caminhos aumentantes
        while fila:
            v = fila.popleft()
            
            if distancias[v] < distancias[None]:
                for u in grafo.obter_adjacentes(v):
                    if distancias[emparelhamento_reverso.get(u, None)] == float('infinity'):
                        distancias[emparelhamento_reverso.get(u, None)] = distancias[v] + 1
                        fila.append(emparelhamento_reverso.get(u, None))
        
        return distancias[None] != float('infinity')
    
    # Função para encontrar um caminho aumentante usando DFS
    def dfs(v: Any) -> bool:
        if v is None:
            return True
        
        for u in grafo.obter_adjacentes(v):
            if distancias[emparelhamento_reverso.get(u, None)] == distancias[v] + 1:
                if dfs(emparelhamento_reverso.get(u, None)):
                    emparelhamento[v] = u
                    emparelhamento_reverso[u] = v
                    return True
        
        distancias[v] = float('infinity')
        return False
    
    # Algoritmo principal de Hopcroft-Karp
    while True:
        # Inicializa as distâncias para a BFS
        distancias = {}
        
        # Se não há mais caminhos aumentantes, termina
        if not bfs():
            break
        
        # Para cada vértice não emparelhado do conjunto A, tenta encontrar um caminho aumentante
        for v in conjunto_a:
            if v not in emparelhamento:
                dfs(v)
    
    return emparelhamento


def verificar_emparelhamento_maximo(grafo: Grafo, emparelhamento: Dict[Any, Any]) -> bool:
    """
    Verifica se um emparelhamento é máximo usando o teorema de König.
    
    O teorema de König afirma que em um grafo bipartido, o tamanho do emparelhamento máximo
    é igual ao tamanho da cobertura mínima por vértices.
    
    Args:
        grafo: Grafo bipartido não direcionado.
        emparelhamento: Dicionário mapeando vértices do conjunto A para seus pares no conjunto B.
        
    Returns:
        bool: True se o emparelhamento for máximo, False caso contrário.
    """
    # Verifica se o grafo é bipartido
    from algoritmos.caminhos.busca.busca import verificar_bipartido
    eh_bipartido, cores = verificar_bipartido(grafo)
    
    if not eh_bipartido:
        raise ValueError("O grafo não é bipartido.")
    
    # Divide os vértices em dois conjuntos: A (cor 0) e B (cor 1)
    conjunto_a = {v for v, cor in cores.items() if cor == 0}
    conjunto_b = {v for v, cor in cores.items() if cor == 1}
    
    # Cria um grafo direcionado para encontrar a cobertura mínima
    g_dir = nx.DiGraph()
    
    # Adiciona os vértices
    for v in grafo.obter_vertices():
        g_dir.add_node(v)
    
    # Adiciona um vértice fonte e um vértice sumidouro
    fonte = 'fonte'
    sumidouro = 'sumidouro'
    g_dir.add_node(fonte)
    g_dir.add_node(sumidouro)
    
    # Adiciona arestas da fonte para os vértices do conjunto A
    for v in conjunto_a:
        g_dir.add_edge(fonte, v, capacity=1)
    
    # Adiciona arestas dos vértices do conjunto B para o sumidouro
    for v in conjunto_b:
        g_dir.add_edge(v, sumidouro, capacity=1)
    
    # Adiciona arestas entre os conjuntos A e B
    for u, v in grafo.obter_grafo_networkx().edges():
        if u in conjunto_a and v in conjunto_b:
            g_dir.add_edge(u, v, capacity=1)
        elif u in conjunto_b and v in conjunto_a:
            g_dir.add_edge(v, u, capacity=1)
    
    # Encontra o corte mínimo
    _, corte_particao = nx.minimum_cut(g_dir, fonte, sumidouro)
    lado_fonte, lado_sumidouro = corte_particao
    
    # Remove a fonte e o sumidouro das partições
    lado_fonte = lado_fonte - {fonte}
    lado_sumidouro = lado_sumidouro - {sumidouro}
    
    # A cobertura mínima é formada pelos vértices do conjunto A no lado do sumidouro
    # e pelos vértices do conjunto B no lado da fonte
    cobertura_minima = (lado_sumidouro & conjunto_a) | (lado_fonte & conjunto_b)
    
    # Pelo teorema de König, o tamanho do emparelhamento máximo é igual ao tamanho da cobertura mínima
    return len(emparelhamento) == len(cobertura_minima)


def encontrar_caminho_aumentante(grafo: Grafo, emparelhamento: Dict[Any, Any]) -> Optional[List[Any]]:
    """
    Encontra um caminho aumentante no grafo em relação ao emparelhamento atual.
    
    Um caminho aumentante é um caminho alternante que começa e termina em vértices não emparelhados.
    
    Args:
        grafo: Grafo bipartido não direcionado.
        emparelhamento: Dicionário mapeando vértices do conjunto A para seus pares no conjunto B.
        
    Returns:
        Optional[List[Any]]: Lista de vértices que formam um caminho aumentante, ou None se não existir.
    """
    # Verifica se o grafo é bipartido
    from algoritmos.caminhos.busca.busca import verificar_bipartido
    eh_bipartido, cores = verificar_bipartido(grafo)
    
    if not eh_bipartido:
        raise ValueError("O grafo não é bipartido.")
    
    # Divide os vértices em dois conjuntos: A (cor 0) e B (cor 1)
    conjunto_a = {v for v, cor in cores.items() if cor == 0}
    conjunto_b = {v for v, cor in cores.items() if cor == 1}
    
    # Cria o emparelhamento reverso
    emparelhamento_reverso = {v: u for u, v in emparelhamento.items()}
    
    # Encontra vértices não emparelhados do conjunto A
    nao_emparelhados_a = conjunto_a - set(emparelhamento.keys())
    
    # Se não há vértices não emparelhados no conjunto A, o emparelhamento é máximo
    if not nao_emparelhados_a:
        return None
    
    # BFS para encontrar um caminho aumentante
    for origem in nao_emparelhados_a:
        visitados = {origem}
        fila = deque([(origem, [])])  # (vértice, caminho)
        
        while fila:
            v, caminho = fila.popleft()
            caminho_atual = caminho + [v]
            
            # Se v está no conjunto A, procura por arestas não emparelhadas
            if v in conjunto_a:
                for u in grafo.obter_adjacentes(v):
                    if u not in visitados and v not in emparelhamento:
                        # Se u não está emparelhado, encontramos um caminho aumentante
                        if u not in emparelhamento_reverso:
                            return caminho_atual + [u]
                        
                        visitados.add(u)
                        fila.append((u, caminho_atual))
            
            # Se v está no conjunto B, procura por arestas emparelhadas
            else:
                if v in emparelhamento_reverso:
                    u = emparelhamento_reverso[v]
                    if u not in visitados:
                        visitados.add(u)
                        fila.append((u, caminho_atual))
    
    return None


def visualizar_emparelhamento(grafo: Grafo, emparelhamento: Dict[Any, Any], arquivo: str = None) -> None:
    """
    Visualiza o emparelhamento em um grafo bipartido.
    
    Args:
        grafo: Grafo bipartido não direcionado.
        emparelhamento: Dicionário mapeando vértices do conjunto A para seus pares no conjunto B.
        arquivo: Caminho para salvar a imagem (opcional).
    """
    import matplotlib.pyplot as plt
    import networkx as nx
    
    # Verifica se o grafo é bipartido
    from algoritmos.caminhos.busca.busca import verificar_bipartido
    eh_bipartido, cores = verificar_bipartido(grafo)
    
    if not eh_bipartido:
        raise ValueError("O grafo não é bipartido.")
    
    # Divide os vértices em dois conjuntos: A (cor 0) e B (cor 1)
    conjunto_a = {v for v, cor in cores.items() if cor == 0}
    conjunto_b = {v for v, cor in cores.items() if cor == 1}
    
    # Cria um grafo NetworkX para visualização
    g_nx = nx.Graph()
    
    # Adiciona os vértices
    for v in grafo.obter_vertices():
        g_nx.add_node(v)
    
    # Adiciona as arestas
    for u, v in grafo.obter_grafo_networkx().edges():
        g_nx.add_edge(u, v)
    
    # Define as posições dos vértices
    pos = {}
    
    # Posiciona os vértices do conjunto A à esquerda
    for i, v in enumerate(conjunto_a):
        pos[v] = (-1, i - len(conjunto_a) / 2)
    
    # Posiciona os vértices do conjunto B à direita
    for i, v in enumerate(conjunto_b):
        pos[v] = (1, i - len(conjunto_b) / 2)
    
    # Desenha o grafo
    plt.figure(figsize=(10, 8))
    
    # Desenha os vértices
    nx.draw_networkx_nodes(g_nx, pos, nodelist=conjunto_a, node_color='lightblue', node_size=500)
    nx.draw_networkx_nodes(g_nx, pos, nodelist=conjunto_b, node_color='lightgreen', node_size=500)
    
    # Desenha as arestas não emparelhadas
    arestas_nao_emparelhadas = [(u, v) for u, v in g_nx.edges() if u not in emparelhamento or emparelhamento[u] != v]
    nx.draw_networkx_edges(g_nx, pos, edgelist=arestas_nao_emparelhadas, width=1, alpha=0.5)
    
    # Desenha as arestas emparelhadas
    arestas_emparelhadas = [(u, emparelhamento[u]) for u in emparelhamento]
    nx.draw_networkx_edges(g_nx, pos, edgelist=arestas_emparelhadas, width=3, edge_color='red')
    
    # Desenha os rótulos dos vértices
    nx.draw_networkx_labels(g_nx, pos)
    
    plt.title(f"Emparelhamento Máximo (tamanho: {len(emparelhamento)})")
    plt.axis('off')
    
    # Salva a imagem ou mostra na tela
    if arquivo:
        plt.savefig(arquivo)
    else:
        plt.show()
