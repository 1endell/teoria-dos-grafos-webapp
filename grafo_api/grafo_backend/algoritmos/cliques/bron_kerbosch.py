"""
Implementação do algoritmo de Bron-Kerbosch para encontrar cliques maximais em grafos.

Um clique é um subgrafo completo, ou seja, um conjunto de vértices onde todos
estão conectados entre si. Um clique maximal é um clique que não pode ser
estendido adicionando mais vértices.
"""

from typing import Dict, List, Any, Tuple, Set, Optional
import networkx as nx
from core.grafo import Grafo


def bron_kerbosch(grafo: Grafo, com_pivoteamento: bool = True) -> List[Set[Any]]:
    """
    Implementa o algoritmo de Bron-Kerbosch para encontrar todos os cliques maximais.
    
    Args:
        grafo: Grafo não direcionado.
        com_pivoteamento: Se True, usa a versão com pivoteamento para melhor desempenho.
        
    Returns:
        List[Set[Any]]: Lista de conjuntos, onde cada conjunto contém os vértices de um clique maximal.
            
    Raises:
        ValueError: Se o grafo for direcionado.
    """
    # Verifica se o grafo é direcionado
    if grafo.eh_direcionado():
        raise ValueError("O algoritmo de Bron-Kerbosch só é aplicável a grafos não direcionados.")
    
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Lista para armazenar os cliques maximais encontrados
    cliques_maximais = []
    
    # Função recursiva para o algoritmo de Bron-Kerbosch sem pivoteamento
    def bron_kerbosch_sem_pivoteamento(R: Set[Any], P: Set[Any], X: Set[Any]) -> None:
        if not P and not X:
            # R é um clique maximal
            cliques_maximais.append(R.copy())
            return
        
        # Para cada vértice em P
        for v in list(P):
            # Vizinhos de v
            vizinhos = set(g_nx.neighbors(v))
            
            # Chamada recursiva
            bron_kerbosch_sem_pivoteamento(
                R | {v},           # Adiciona v ao clique atual
                P & vizinhos,      # Vértices em P que são vizinhos de v
                X & vizinhos       # Vértices em X que são vizinhos de v
            )
            
            # Move v de P para X
            P.remove(v)
            X.add(v)
    
    # Função recursiva para o algoritmo de Bron-Kerbosch com pivoteamento
    def bron_kerbosch_com_pivoteamento(R: Set[Any], P: Set[Any], X: Set[Any]) -> None:
        if not P and not X:
            # R é um clique maximal
            cliques_maximais.append(R.copy())
            return
        
        # Escolhe um pivô de P ∪ X que maximize |P ∩ N(u)|
        pivo = None
        max_vizinhos = -1
        
        for u in P | X:
            vizinhos = set(g_nx.neighbors(u))
            num_vizinhos = len(P & vizinhos)
            
            if num_vizinhos > max_vizinhos:
                max_vizinhos = num_vizinhos
                pivo = u
        
        # Vizinhos do pivô
        vizinhos_pivo = set(g_nx.neighbors(pivo))
        
        # Para cada vértice em P que não é vizinho do pivô
        for v in list(P - vizinhos_pivo):
            # Vizinhos de v
            vizinhos = set(g_nx.neighbors(v))
            
            # Chamada recursiva
            bron_kerbosch_com_pivoteamento(
                R | {v},           # Adiciona v ao clique atual
                P & vizinhos,      # Vértices em P que são vizinhos de v
                X & vizinhos       # Vértices em X que são vizinhos de v
            )
            
            # Move v de P para X
            P.remove(v)
            X.add(v)
    
    # Inicializa os conjuntos
    R = set()  # Clique atual
    P = set(grafo.obter_vertices())  # Vértices candidatos
    X = set()  # Vértices já processados
    
    # Executa o algoritmo
    if com_pivoteamento:
        bron_kerbosch_com_pivoteamento(R, P, X)
    else:
        bron_kerbosch_sem_pivoteamento(R, P, X)
    
    return cliques_maximais


def encontrar_clique_maximo(grafo: Grafo) -> Tuple[Set[Any], int]:
    """
    Encontra o clique máximo (de maior tamanho) em um grafo.
    
    Args:
        grafo: Grafo não direcionado.
        
    Returns:
        Tuple[Set[Any], int]: Tupla contendo:
            - Conjunto de vértices que formam o clique máximo
            - Tamanho do clique máximo
    """
    # Encontra todos os cliques maximais
    cliques_maximais = bron_kerbosch(grafo)
    
    # Encontra o clique de maior tamanho
    clique_maximo = max(cliques_maximais, key=len) if cliques_maximais else set()
    
    return clique_maximo, len(clique_maximo)


def calcular_numero_clique(grafo: Grafo) -> int:
    """
    Calcula o número de clique de um grafo.
    
    O número de clique é o tamanho do maior clique no grafo.
    
    Args:
        grafo: Grafo não direcionado.
        
    Returns:
        int: Número de clique do grafo.
    """
    _, tamanho = encontrar_clique_maximo(grafo)
    return tamanho


def verificar_clique(grafo: Grafo, vertices: Set[Any]) -> bool:
    """
    Verifica se um conjunto de vértices forma um clique.
    
    Args:
        grafo: Grafo não direcionado.
        vertices: Conjunto de vértices a ser verificado.
        
    Returns:
        bool: True se o conjunto formar um clique, False caso contrário.
    """
    # Verifica se todos os vértices existem no grafo
    for v in vertices:
        if not grafo.existe_vertice(v):
            return False
    
    # Verifica se todos os pares de vértices estão conectados
    for u in vertices:
        for v in vertices:
            if u != v and not grafo.existe_aresta(u, v):
                return False
    
    return True


def visualizar_cliques(grafo: Grafo, cliques: List[Set[Any]], arquivo: str = None) -> None:
    """
    Visualiza os cliques em um grafo.
    
    Args:
        grafo: Grafo não direcionado.
        cliques: Lista de conjuntos, onde cada conjunto contém os vértices de um clique.
        arquivo: Caminho para salvar a imagem (opcional).
    """
    import matplotlib.pyplot as plt
    import networkx as nx
    import matplotlib.cm as cm
    
    # Cria um grafo NetworkX para visualização
    g_nx = grafo.obter_grafo_networkx()
    
    # Define as posições dos vértices
    pos = nx.spring_layout(g_nx)
    
    # Desenha o grafo
    plt.figure(figsize=(12, 8))
    
    # Desenha as arestas
    nx.draw_networkx_edges(g_nx, pos, alpha=0.3)
    
    # Desenha os vértices e os cliques
    cores = cm.rainbow(np.linspace(0, 1, len(cliques)))
    
    # Primeiro, desenha todos os vértices em cinza
    nx.draw_networkx_nodes(g_nx, pos, node_color='lightgray', node_size=300)
    
    # Depois, desenha cada clique com uma cor diferente
    for i, clique in enumerate(cliques):
        nx.draw_networkx_nodes(g_nx, pos, nodelist=list(clique), node_color=[cores[i]], node_size=500)
    
    # Desenha os rótulos dos vértices
    nx.draw_networkx_labels(g_nx, pos)
    
    plt.title(f"Cliques Maximais (total: {len(cliques)})")
    plt.axis('off')
    
    # Salva a imagem ou mostra na tela
    if arquivo:
        plt.savefig(arquivo)
    else:
        plt.show()
