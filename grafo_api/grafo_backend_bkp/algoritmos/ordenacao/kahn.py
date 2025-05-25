"""
Implementação do algoritmo de Kahn para ordenação topológica em grafos direcionados acíclicos.

O algoritmo de Kahn encontra uma ordenação topológica em um grafo direcionado acíclico (DAG),
que é uma ordenação linear dos vértices tal que para toda aresta (u, v), u vem antes de v.
"""

from typing import Dict, List, Any, Tuple, Set, Optional, Deque
from collections import deque
import networkx as nx
from core.grafo import Grafo


def kahn(grafo: Grafo) -> List[Any]:
    """
    Implementa o algoritmo de Kahn para ordenação topológica.
    
    Args:
        grafo: Grafo direcionado acíclico.
        
    Returns:
        List[Any]: Lista de vértices em ordem topológica.
            
    Raises:
        ValueError: Se o grafo não for direcionado.
        ValueError: Se o grafo contiver ciclos.
    """
    # Verifica se o grafo é direcionado
    if not grafo.eh_direcionado():
        raise ValueError("O algoritmo de Kahn só é aplicável a grafos direcionados.")
    
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Calcula o grau de entrada de cada vértice
    grau_entrada = {v: 0 for v in grafo.obter_vertices()}
    
    for u, v in g_nx.edges():
        grau_entrada[v] += 1
    
    # Inicializa a fila com vértices de grau de entrada zero
    fila = deque([v for v, grau in grau_entrada.items() if grau == 0])
    
    # Inicializa a ordenação topológica
    ordenacao = []
    
    # Enquanto houver vértices na fila
    while fila:
        # Remove um vértice da fila
        v = fila.popleft()
        
        # Adiciona o vértice à ordenação
        ordenacao.append(v)
        
        # Para cada vizinho do vértice
        for u in list(g_nx.successors(v)):
            # Reduz o grau de entrada do vizinho
            grau_entrada[u] -= 1
            
            # Se o grau de entrada do vizinho for zero, adiciona à fila
            if grau_entrada[u] == 0:
                fila.append(u)
    
    # Verifica se todos os vértices foram incluídos na ordenação
    if len(ordenacao) != len(grafo.obter_vertices()):
        raise ValueError("O grafo contém ciclos.")
    
    return ordenacao


def verificar_ordenacao_topologica(grafo: Grafo, ordenacao: List[Any]) -> bool:
    """
    Verifica se uma ordenação é topológica.
    
    Uma ordenação é topológica se para toda aresta (u, v), u vem antes de v na ordenação.
    
    Args:
        grafo: Grafo direcionado acíclico.
        ordenacao: Lista de vértices a ser verificada.
        
    Returns:
        bool: True se a ordenação for topológica, False caso contrário.
    """
    # Verifica se o grafo é direcionado
    if not grafo.eh_direcionado():
        raise ValueError("A ordenação topológica só é definida para grafos direcionados.")
    
    # Verifica se a ordenação contém todos os vértices
    if set(ordenacao) != set(grafo.obter_vertices()):
        return False
    
    # Cria um mapeamento de vértices para suas posições na ordenação
    posicao = {v: i for i, v in enumerate(ordenacao)}
    
    # Verifica se para toda aresta (u, v), u vem antes de v na ordenação
    for u, v in grafo.obter_grafo_networkx().edges():
        if posicao[u] >= posicao[v]:
            return False
    
    return True


def encontrar_caminho_critico(grafo: Grafo, pesos: Dict[Any, float]) -> Tuple[List[Any], float]:
    """
    Encontra o caminho crítico em um grafo direcionado acíclico.
    
    O caminho crítico é o caminho mais longo em um DAG, considerando os pesos dos vértices.
    É útil em problemas de escalonamento de tarefas, onde os vértices representam tarefas
    e os pesos representam suas durações.
    
    Args:
        grafo: Grafo direcionado acíclico.
        pesos: Dicionário mapeando vértices para seus pesos (durações).
        
    Returns:
        Tuple[List[Any], float]: Tupla contendo:
            - Lista de vértices que formam o caminho crítico
            - Duração total do caminho crítico
    """
    # Verifica se o grafo é direcionado
    if not grafo.eh_direcionado():
        raise ValueError("O caminho crítico só é definido para grafos direcionados.")
    
    # Obtém uma ordenação topológica
    ordenacao = kahn(grafo)
    
    # Inicializa as distâncias e predecessores
    distancias = {v: 0 for v in grafo.obter_vertices()}
    predecessores = {v: None for v in grafo.obter_vertices()}
    
    # Para cada vértice na ordenação topológica
    for v in ordenacao:
        # Para cada sucessor do vértice
        for u in grafo.obter_adjacentes(v):
            # Calcula a nova distância
            nova_distancia = distancias[v] + pesos[u]
            
            # Se a nova distância for maior que a registrada
            if nova_distancia > distancias[u]:
                # Atualiza a distância
                distancias[u] = nova_distancia
                # Atualiza o predecessor
                predecessores[u] = v
    
    # Encontra o vértice com a maior distância
    v_final = max(distancias.items(), key=lambda x: x[1])[0]
    
    # Reconstrói o caminho crítico
    caminho = []
    v = v_final
    
    while v is not None:
        caminho.append(v)
        v = predecessores[v]
    
    # Inverte o caminho para que comece no início
    caminho.reverse()
    
    return caminho, distancias[v_final]


def visualizar_ordenacao_topologica(grafo: Grafo, ordenacao: List[Any], arquivo: str = None) -> None:
    """
    Visualiza uma ordenação topológica em um grafo direcionado acíclico.
    
    Args:
        grafo: Grafo direcionado acíclico.
        ordenacao: Lista de vértices em ordem topológica.
        arquivo: Caminho para salvar a imagem (opcional).
    """
    import matplotlib.pyplot as plt
    import networkx as nx
    
    # Cria um grafo NetworkX para visualização
    g_nx = grafo.obter_grafo_networkx()
    
    # Define as posições dos vértices
    pos = {}
    
    # Posiciona os vértices da esquerda para a direita de acordo com a ordenação
    for i, v in enumerate(ordenacao):
        pos[v] = (i, 0)
    
    # Desenha o grafo
    plt.figure(figsize=(12, 6))
    
    # Desenha os vértices
    nx.draw_networkx_nodes(g_nx, pos, node_color='lightblue', node_size=500)
    
    # Desenha as arestas
    nx.draw_networkx_edges(g_nx, pos, width=1.5, arrowsize=20)
    
    # Desenha os rótulos dos vértices
    nx.draw_networkx_labels(g_nx, pos)
    
    # Adiciona rótulos de posição na ordenação
    for i, v in enumerate(ordenacao):
        plt.text(i, -0.3, f"Posição {i+1}", ha='center')
    
    plt.title("Ordenação Topológica")
    plt.axis('off')
    
    # Salva a imagem ou mostra na tela
    if arquivo:
        plt.savefig(arquivo)
    else:
        plt.show()
