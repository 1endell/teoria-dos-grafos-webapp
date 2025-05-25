"""
Implementação do algoritmo de Dinic para encontrar o fluxo máximo em redes.

O algoritmo de Dinic é uma implementação mais eficiente do método de Ford-Fulkerson
para encontrar o fluxo máximo em uma rede, com complexidade de tempo O(V²E).
"""

from typing import Dict, List, Any, Tuple, Set, Optional, Deque
from collections import deque
import networkx as nx
from ...core.grafo import Grafo


def dinic(grafo: Grafo, fonte: Any, sumidouro: Any) -> Tuple[Dict[Tuple[Any, Any], float], float]:
    """
    Implementa o algoritmo de Dinic para encontrar o fluxo máximo em uma rede.
    
    Args:
        grafo: Grafo ponderado direcionado representando a rede.
        fonte: Vértice fonte.
        sumidouro: Vértice sumidouro.
        
    Returns:
        Tuple[Dict[Tuple[Any, Any], float], float]: Tupla contendo:
            - Dicionário mapeando arestas (u, v) para seus fluxos
            - Valor do fluxo máximo
            
    Raises:
        ValueError: Se algum dos vértices não existir no grafo.
        ValueError: Se o grafo não for direcionado.
    """
    # Verifica se os vértices existem no grafo
    if not grafo.existe_vertice(fonte):
        raise ValueError(f"Vértice fonte '{fonte}' não existe no grafo.")
    if not grafo.existe_vertice(sumidouro):
        raise ValueError(f"Vértice sumidouro '{sumidouro}' não existe no grafo.")
    
    # Verifica se o grafo é direcionado
    if not grafo.eh_direcionado():
        raise ValueError("O algoritmo de Dinic só é aplicável a grafos direcionados.")
    
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Cria a rede residual
    rede_residual = nx.DiGraph()
    
    # Adiciona os vértices
    for v in grafo.obter_vertices():
        rede_residual.add_node(v)
    
    # Adiciona as arestas com capacidades
    for u, v, attrs in g_nx.edges(data=True):
        capacidade = attrs.get('weight', 1.0)
        rede_residual.add_edge(u, v, capacity=capacidade, flow=0)
        # Adiciona a aresta reversa com capacidade zero
        if not rede_residual.has_edge(v, u):
            rede_residual.add_edge(v, u, capacity=0, flow=0)
    
    # Função para construir a rede de nível usando BFS
    def construir_rede_nivel() -> bool:
        global nivel
        nivel = {}
        
        # Inicializa a fila para BFS
        fila = deque([fonte])
        nivel[fonte] = 0
        
        # Enquanto houver vértices na fila
        while fila:
            u = fila.popleft()
            
            # Para cada vizinho
            for v in rede_residual.neighbors(u):
                # Se o vizinho ainda não tem nível e a capacidade residual é positiva
                if v not in nivel and rede_residual[u][v]['capacity'] > rede_residual[u][v]['flow']:
                    nivel[v] = nivel[u] + 1
                    fila.append(v)
        
        # Retorna True se o sumidouro foi alcançado
        return sumidouro in nivel
    
    # Função para encontrar um caminho de aumento usando DFS
    def encontrar_caminho_aumento(u: Any, fluxo_min: float) -> float:
        # Se chegou ao sumidouro ou o fluxo mínimo é zero
        if u == sumidouro or fluxo_min == 0:
            return fluxo_min
        
        # Para cada vizinho
        for v in rede_residual.neighbors(u):
            # Se o vizinho está no próximo nível e a capacidade residual é positiva
            if nivel.get(v, -1) == nivel[u] + 1 and rede_residual[u][v]['capacity'] > rede_residual[u][v]['flow']:
                # Calcula o fluxo residual
                capacidade_residual = rede_residual[u][v]['capacity'] - rede_residual[u][v]['flow']
                # Encontra o fluxo de aumento
                fluxo_aumento = encontrar_caminho_aumento(v, min(fluxo_min, capacidade_residual))
                
                # Se encontrou um caminho de aumento
                if fluxo_aumento > 0:
                    # Atualiza o fluxo na aresta
                    rede_residual[u][v]['flow'] += fluxo_aumento
                    # Atualiza o fluxo na aresta reversa
                    rede_residual[v][u]['flow'] -= fluxo_aumento
                    
                    return fluxo_aumento
        
        # Se não encontrou caminho de aumento
        return 0
    
    # Algoritmo principal de Dinic
    fluxo_maximo = 0
    
    # Enquanto houver um caminho da fonte ao sumidouro na rede residual
    while construir_rede_nivel():
        # Enquanto houver um caminho de aumento
        while True:
            fluxo_aumento = encontrar_caminho_aumento(fonte, float('infinity'))
            
            if fluxo_aumento == 0:
                break
            
            fluxo_maximo += fluxo_aumento
    
    # Constrói o dicionário de fluxos
    fluxos = {}
    
    for u, v, attrs in rede_residual.edges(data=True):
        if attrs['capacity'] > 0:  # Apenas arestas originais, não as reversas
            fluxos[(u, v)] = attrs['flow']
    
    return fluxos, fluxo_maximo


def comparar_dinic_edmonds_karp(grafo: Grafo, fonte: Any, sumidouro: Any) -> Dict[str, Any]:
    """
    Compara os algoritmos de Dinic e Edmonds-Karp para o mesmo grafo.
    
    Args:
        grafo: Grafo ponderado direcionado representando a rede.
        fonte: Vértice fonte.
        sumidouro: Vértice sumidouro.
        
    Returns:
        Dict[str, Any]: Dicionário contendo:
            - 'dinic_fluxo': Valor do fluxo máximo encontrado pelo Dinic
            - 'edmonds_karp_fluxo': Valor do fluxo máximo encontrado pelo Edmonds-Karp
            - 'iguais': Booleano indicando se os fluxos são iguais
            - 'dinic_tempo': Tempo de execução do Dinic
            - 'edmonds_karp_tempo': Tempo de execução do Edmonds-Karp
    """
    import time
    from algoritmos.fluxo.edmonds_karp import edmonds_karp
    
    # Mede o tempo de execução do Dinic
    inicio = time.time()
    _, dinic_fluxo = dinic(grafo, fonte, sumidouro)
    fim = time.time()
    dinic_tempo = fim - inicio
    
    # Mede o tempo de execução do Edmonds-Karp
    inicio = time.time()
    _, edmonds_karp_fluxo = edmonds_karp(grafo, fonte, sumidouro)
    fim = time.time()
    edmonds_karp_tempo = fim - inicio
    
    # Compara os resultados
    return {
        'dinic_fluxo': dinic_fluxo,
        'edmonds_karp_fluxo': edmonds_karp_fluxo,
        'iguais': abs(dinic_fluxo - edmonds_karp_fluxo) < 1e-9,  # Compara com tolerância para erros de ponto flutuante
        'dinic_tempo': dinic_tempo,
        'edmonds_karp_tempo': edmonds_karp_tempo
    }


def visualizar_fluxo(grafo: Grafo, fluxos: Dict[Tuple[Any, Any], float], fonte: Any, sumidouro: Any, arquivo: str = None) -> None:
    """
    Visualiza o fluxo em uma rede.
    
    Args:
        grafo: Grafo ponderado direcionado representando a rede.
        fluxos: Dicionário mapeando arestas (u, v) para seus fluxos.
        fonte: Vértice fonte.
        sumidouro: Vértice sumidouro.
        arquivo: Caminho para salvar a imagem (opcional).
    """
    import matplotlib.pyplot as plt
    import networkx as nx
    
    # Cria um grafo NetworkX para visualização
    g_nx = grafo.obter_grafo_networkx()
    
    # Define as posições dos vértices
    pos = nx.spring_layout(g_nx)
    
    # Desenha o grafo
    plt.figure(figsize=(12, 8))
    
    # Desenha os vértices
    nx.draw_networkx_nodes(g_nx, pos, node_color='lightblue', node_size=500)
    
    # Destaca a fonte e o sumidouro
    nx.draw_networkx_nodes(g_nx, pos, nodelist=[fonte], node_color='green', node_size=700)
    nx.draw_networkx_nodes(g_nx, pos, nodelist=[sumidouro], node_color='red', node_size=700)
    
    # Desenha as arestas com rótulos de fluxo/capacidade
    for u, v, attrs in g_nx.edges(data=True):
        capacidade = attrs.get('weight', 1.0)
        fluxo = fluxos.get((u, v), 0)
        
        # Calcula a largura da aresta baseada no fluxo
        largura = 1 + 3 * (fluxo / capacidade) if capacidade > 0 else 1
        
        # Desenha a aresta
        nx.draw_networkx_edges(g_nx, pos, edgelist=[(u, v)], width=largura, alpha=0.7,
                              edge_color='blue' if fluxo > 0 else 'gray')
        
        # Adiciona o rótulo de fluxo/capacidade
        label = f"{fluxo}/{capacidade}"
        edge_labels = {(u, v): label}
        nx.draw_networkx_edge_labels(g_nx, pos, edge_labels=edge_labels, font_size=10)
    
    # Desenha os rótulos dos vértices
    nx.draw_networkx_labels(g_nx, pos)
    
    plt.title(f"Fluxo Máximo: {sum(fluxos.get((fonte, v), 0) for v in g_nx.neighbors(fonte))}")
    plt.axis('off')
    
    # Salva a imagem ou mostra na tela
    if arquivo:
        plt.savefig(arquivo)
    else:
        plt.show()
