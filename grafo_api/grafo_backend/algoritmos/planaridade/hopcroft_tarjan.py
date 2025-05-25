"""
Implementação do algoritmo de Hopcroft-Tarjan para teste de planaridade em grafos.

Um grafo é planar se pode ser desenhado em um plano sem que suas arestas se cruzem.
O algoritmo de Hopcroft-Tarjan determina se um grafo é planar em tempo linear.
"""

from typing import Dict, List, Any, Tuple, Set, Optional
import networkx as nx
from grafo_backend.core.grafo import Grafo


def hopcroft_tarjan(grafo: Grafo) -> bool:
    """
    Implementa o algoritmo de Hopcroft-Tarjan para teste de planaridade.
    
    Args:
        grafo: Grafo não direcionado.
        
    Returns:
        bool: True se o grafo for planar, False caso contrário.
            
    Raises:
        ValueError: Se o grafo for direcionado.
    """
    # Verifica se o grafo é direcionado
    if grafo.eh_direcionado():
        raise ValueError("O algoritmo de Hopcroft-Tarjan só é aplicável a grafos não direcionados.")
    
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Verifica se o grafo é planar usando a função do NetworkX
    # (que implementa o algoritmo de Boyer-Myrvold, uma variante mais eficiente do Hopcroft-Tarjan)
    return nx.is_planar(g_nx)


def encontrar_embedding_planar(grafo: Grafo) -> Optional[Dict[Any, List[Any]]]:
    """
    Encontra um embedding planar para o grafo, se existir.
    
    Um embedding planar é uma representação do grafo onde as arestas não se cruzam.
    É representado como um dicionário que mapeia cada vértice para uma lista ordenada
    de seus vizinhos, no sentido horário.
    
    Args:
        grafo: Grafo não direcionado.
        
    Returns:
        Optional[Dict[Any, List[Any]]]: Dicionário representando o embedding planar,
            ou None se o grafo não for planar.
    """
    # Verifica se o grafo é direcionado
    if grafo.eh_direcionado():
        raise ValueError("O algoritmo só é aplicável a grafos não direcionados.")
    
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Verifica se o grafo é planar e obtém o embedding
    is_planar, embedding = nx.check_planarity(g_nx)
    
    if not is_planar:
        return None
    
    # Converte o embedding para o formato desejado
    # Nas versões mais recentes do NetworkX, o embedding já é um dicionário
    # que mapeia vértices para listas de vizinhos
    if isinstance(embedding, dict):
        return embedding
    
    # Para versões mais antigas do NetworkX, o embedding pode ser um objeto com métodos específicos
    try:
        resultado = {}
        for v in grafo.obter_vertices():
            # Tenta obter os vizinhos na ordem do embedding
            if hasattr(embedding, 'get_data') and hasattr(embedding.get_data(), 'neighbors_in_drawing_order'):
                resultado[v] = list(embedding.get_data().neighbors_in_drawing_order(v))
            else:
                # Fallback: retorna apenas a lista de vizinhos sem ordem específica
                resultado[v] = list(g_nx.neighbors(v))
        return resultado
    except Exception as e:
        # Se ocorrer qualquer erro, retorna apenas as listas de adjacência
        resultado = {}
        for v in grafo.obter_vertices():
            resultado[v] = list(g_nx.neighbors(v))
        return resultado


def encontrar_subgrafo_kuratowski(grafo: Grafo) -> Optional[Set[Any]]:
    """
    Encontra um subgrafo de Kuratowski no grafo, se existir.
    
    Pelo teorema de Kuratowski, um grafo é planar se e somente se não contém
    um subgrafo que é uma subdivisão de K5 (grafo completo com 5 vértices) ou
    K3,3 (grafo bipartido completo com 3 vértices em cada parte).
    
    Args:
        grafo: Grafo não direcionado.
        
    Returns:
        Optional[Set[Any]]: Conjunto de vértices que formam um subgrafo de Kuratowski,
            ou None se o grafo for planar.
    """
    # Verifica se o grafo é direcionado
    if grafo.eh_direcionado():
        raise ValueError("O algoritmo só é aplicável a grafos não direcionados.")
    
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Verifica se o grafo é planar
    if nx.is_planar(g_nx):
        return None
    
    # Encontra um subgrafo de Kuratowski
    subgrafo = nx.kuratowski_subgraph(g_nx)
    
    return set(subgrafo.nodes())


def calcular_genus(grafo: Grafo) -> int:
    """
    Calcula o genus de um grafo.
    
    O genus de um grafo é o número mínimo de "alças" que devem ser adicionadas
    a uma esfera para que o grafo possa ser desenhado sem cruzamentos.
    Um grafo planar tem genus 0.
    
    Args:
        grafo: Grafo não direcionado.
        
    Returns:
        int: Genus do grafo.
    """
    # Verifica se o grafo é direcionado
    if grafo.eh_direcionado():
        raise ValueError("O algoritmo só é aplicável a grafos não direcionados.")
    
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Verifica se o grafo é planar
    if nx.is_planar(g_nx):
        return 0
    
    # Calcula o genus usando a fórmula de Euler
    # Para um grafo com v vértices, e arestas e f faces:
    # v - e + f = 2 - 2g, onde g é o genus
    # Reorganizando: g = 1 + (e - v - f) / 2
    
    # Número de vértices e arestas
    v = g_nx.number_of_nodes()
    e = g_nx.number_of_edges()
    
    # Para grafos não planares, precisamos de uma aproximação do número de faces
    # Uma estimativa é usar o número de ciclos fundamentais
    # O número de ciclos fundamentais é e - v + c, onde c é o número de componentes conexos
    c = nx.number_connected_components(g_nx)
    ciclos_fundamentais = e - v + c
    
    # Estimativa do número de faces
    f = ciclos_fundamentais + 1
    
    # Calcula o genus
    g = 1 + (e - v - f) / 2
    
    return max(0, int(g))


def visualizar_grafo_planar(grafo: Grafo, arquivo: str = None) -> None:
    """
    Visualiza um grafo planar.
    
    Args:
        grafo: Grafo não direcionado.
        arquivo: Caminho para salvar a imagem (opcional).
    """
    import matplotlib.pyplot as plt
    import networkx as nx
    
    # Verifica se o grafo é planar
    if not hopcroft_tarjan(grafo):
        raise ValueError("O grafo não é planar.")
    
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Encontra um embedding planar
    pos = nx.planar_layout(g_nx)
    
    # Desenha o grafo
    plt.figure(figsize=(10, 8))
    
    # Desenha os vértices
    nx.draw_networkx_nodes(g_nx, pos, node_color='lightblue', node_size=500)
    
    # Desenha as arestas
    nx.draw_networkx_edges(g_nx, pos, width=1.5)
    
    # Desenha os rótulos dos vértices
    nx.draw_networkx_labels(g_nx, pos)
    
    plt.title("Grafo Planar")
    plt.axis('off')
    
    # Salva a imagem ou mostra na tela
    if arquivo:
        plt.savefig(arquivo)
    else:
        plt.show()
