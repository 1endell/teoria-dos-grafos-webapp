"""
Implementação do algoritmo de Hierholzer para encontrar ciclos eulerianos em grafos.

O algoritmo de Hierholzer encontra um ciclo euleriano em um grafo, ou seja,
um ciclo que percorre cada aresta exatamente uma vez.
"""

from typing import Dict, List, Any, Tuple, Set, Optional
import networkx as nx
from grafo_backend.core.grafo import Grafo


def hierholzer(grafo: Grafo, vertice_inicial: Any = None) -> Optional[List[Any]]:
    """
    Implementa o algoritmo de Hierholzer para encontrar um ciclo euleriano.
    
    Args:
        grafo: Grafo não direcionado ou direcionado.
        vertice_inicial: Vértice inicial para o ciclo (opcional).
            Se não for especificado, um vértice arbitrário será escolhido.
        
    Returns:
        Optional[List[Any]]: Lista de vértices que formam um ciclo euleriano,
            ou None se o grafo não for euleriano.
            
    Raises:
        ValueError: Se o vértice inicial não existir no grafo.
    """
    # Verifica se o grafo tem vértices
    vertices = list(grafo.obter_vertices())
    if not vertices:
        return []
    
    # Se o vértice inicial não for especificado, escolhe o primeiro vértice
    if vertice_inicial is None:
        vertice_inicial = vertices[0]
    elif not grafo.existe_vertice(vertice_inicial):
        raise ValueError(f"Vértice inicial '{vertice_inicial}' não existe no grafo.")
    
    # Verifica se o grafo é euleriano
    if not verificar_grafo_euleriano(grafo):
        return None
    
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Cria uma cópia do grafo para manipulação
    g_copia = g_nx.copy()
    
    # Função para encontrar um subciclo a partir de um vértice
    def encontrar_subciclo(vertice: Any) -> List[Any]:
        subciclo = [vertice]
        v_atual = vertice
        
        while True:
            # Obtém os vizinhos do vértice atual
            vizinhos = list(g_copia.neighbors(v_atual))
            
            # Se não há mais vizinhos, termina o subciclo
            if not vizinhos:
                break
            
            # Escolhe o próximo vértice
            proximo = vizinhos[0]
            
            # Remove a aresta percorrida
            g_copia.remove_edge(v_atual, proximo)
            
            # Atualiza o vértice atual
            v_atual = proximo
            
            # Adiciona o vértice ao subciclo
            subciclo.append(v_atual)
        
        return subciclo
    
    # Inicializa o ciclo euleriano com um subciclo a partir do vértice inicial
    ciclo = encontrar_subciclo(vertice_inicial)
    
    # Enquanto houver arestas não percorridas
    i = 0
    while i < len(ciclo):
        # Verifica se o vértice atual tem arestas não percorridas
        if list(g_copia.neighbors(ciclo[i])):
            # Encontra um novo subciclo a partir deste vértice
            subciclo = encontrar_subciclo(ciclo[i])
            
            # Insere o subciclo no ciclo principal
            ciclo = ciclo[:i+1] + subciclo[1:] + ciclo[i+1:]
        else:
            # Avança para o próximo vértice
            i += 1
    
    return ciclo


def verificar_grafo_euleriano(grafo: Grafo) -> bool:
    """
    Verifica se um grafo é euleriano.
    
    Um grafo não direcionado é euleriano se todos os vértices têm grau par.
    Um grafo direcionado é euleriano se todos os vértices têm grau de entrada igual ao grau de saída.
    
    Args:
        grafo: Grafo não direcionado ou direcionado.
        
    Returns:
        bool: True se o grafo for euleriano, False caso contrário.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Verifica se o grafo é conexo (ou fortemente conexo, se for direcionado)
    if grafo.eh_direcionado():
        if not nx.is_strongly_connected(g_nx):
            return False
        
        # Verifica se todos os vértices têm grau de entrada igual ao grau de saída
        for v in grafo.obter_vertices():
            if g_nx.in_degree(v) != g_nx.out_degree(v):
                return False
    else:
        if not nx.is_connected(g_nx):
            return False
        
        # Verifica se todos os vértices têm grau par
        for v in grafo.obter_vertices():
            if g_nx.degree(v) % 2 != 0:
                return False
    
    return True


def verificar_grafo_semi_euleriano(grafo: Grafo) -> Tuple[bool, Optional[Tuple[Any, Any]]]:
    """
    Verifica se um grafo é semi-euleriano.
    
    Um grafo não direcionado é semi-euleriano se exatamente dois vértices têm grau ímpar.
    Um grafo direcionado é semi-euleriano se exatamente um vértice tem grau de saída = grau de entrada + 1
    e exatamente um vértice tem grau de entrada = grau de saída + 1.
    
    Args:
        grafo: Grafo não direcionado ou direcionado.
        
    Returns:
        Tuple[bool, Optional[Tuple[Any, Any]]]: Tupla contendo:
            - Booleano indicando se o grafo é semi-euleriano
            - Tupla com os vértices inicial e final do caminho euleriano, ou None se não for semi-euleriano
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Verifica se o grafo é conexo (ou fracamente conexo, se for direcionado)
    if grafo.eh_direcionado():
        if not nx.is_weakly_connected(g_nx):
            return False, None
        
        # Encontra vértices com diferença entre grau de entrada e saída
        inicio = None
        fim = None
        
        for v in grafo.obter_vertices():
            in_degree = g_nx.in_degree(v)
            out_degree = g_nx.out_degree(v)
            
            if out_degree == in_degree + 1:
                if inicio is not None:
                    return False, None  # Mais de um vértice inicial
                inicio = v
            elif in_degree == out_degree + 1:
                if fim is not None:
                    return False, None  # Mais de um vértice final
                fim = v
            elif in_degree != out_degree:
                return False, None  # Vértice com diferença maior que 1
        
        # Verifica se encontrou exatamente um vértice inicial e um final
        if inicio is not None and fim is not None:
            return True, (inicio, fim)
        
        return False, None
    else:
        if not nx.is_connected(g_nx):
            return False, None
        
        # Encontra vértices com grau ímpar
        impares = [v for v in grafo.obter_vertices() if g_nx.degree(v) % 2 == 1]
        
        # Verifica se há exatamente dois vértices com grau ímpar
        if len(impares) == 2:
            return True, (impares[0], impares[1])
        
        return False, None


def encontrar_caminho_euleriano(grafo: Grafo) -> Optional[List[Any]]:
    """
    Encontra um caminho euleriano em um grafo semi-euleriano.
    
    Args:
        grafo: Grafo não direcionado ou direcionado.
        
    Returns:
        Optional[List[Any]]: Lista de vértices que formam um caminho euleriano,
            ou None se o grafo não for semi-euleriano.
    """
    # Verifica se o grafo é semi-euleriano
    eh_semi_euleriano, vertices = verificar_grafo_semi_euleriano(grafo)
    
    if not eh_semi_euleriano:
        return None
    
    # Obtém os vértices inicial e final
    inicio, fim = vertices
    
    # Cria um grafo auxiliar adicionando uma aresta entre os vértices inicial e final
    grafo_auxiliar = grafo.copiar()
    grafo_auxiliar.adicionar_aresta(fim, inicio)
    
    # Encontra um ciclo euleriano no grafo auxiliar
    ciclo = hierholzer(grafo_auxiliar, inicio)
    
    if ciclo is None:
        return None
    
    # Encontra a posição da aresta adicionada no ciclo
    for i in range(len(ciclo) - 1):
        if ciclo[i] == fim and ciclo[i+1] == inicio:
            # Remove a aresta adicionada e reorganiza o ciclo
            return ciclo[i+1:] + ciclo[:i+1]
    
    # Se a aresta adicionada estiver no final do ciclo
    if ciclo[-1] == fim and ciclo[0] == inicio:
        return ciclo
    
    return None


def visualizar_ciclo_euleriano(grafo: Grafo, ciclo: List[Any], arquivo: str = None) -> None:
    """
    Visualiza um ciclo euleriano em um grafo.
    
    Args:
        grafo: Grafo não direcionado ou direcionado.
        ciclo: Lista de vértices que formam um ciclo euleriano.
        arquivo: Caminho para salvar a imagem (opcional).
    """
    import matplotlib.pyplot as plt
    import networkx as nx
    
    # Cria um grafo NetworkX para visualização
    g_nx = grafo.obter_grafo_networkx()
    
    # Define as posições dos vértices
    pos = nx.spring_layout(g_nx)
    
    # Cria as arestas do ciclo na ordem
    arestas_ciclo = [(ciclo[i], ciclo[i+1]) for i in range(len(ciclo)-1)]
    
    # Desenha o grafo
    plt.figure(figsize=(12, 8))
    
    # Desenha os vértices
    nx.draw_networkx_nodes(g_nx, pos, node_color='lightblue', node_size=500)
    
    # Desenha as arestas não pertencentes ao ciclo
    arestas_nao_ciclo = [(u, v) for u, v in g_nx.edges() if (u, v) not in arestas_ciclo and (v, u) not in arestas_ciclo]
    nx.draw_networkx_edges(g_nx, pos, edgelist=arestas_nao_ciclo, width=1, alpha=0.5)
    
    # Desenha as arestas do ciclo com cores diferentes para indicar a ordem
    for i, (u, v) in enumerate(arestas_ciclo):
        # Calcula a cor baseada na posição da aresta no ciclo
        cor = plt.cm.viridis(i / len(arestas_ciclo))
        
        # Desenha a aresta
        nx.draw_networkx_edges(g_nx, pos, edgelist=[(u, v)], width=2, edge_color=[cor])
        
        # Adiciona o número da aresta no ciclo
        edge_labels = {(u, v): str(i+1)}
        nx.draw_networkx_edge_labels(g_nx, pos, edge_labels=edge_labels, font_size=8)
    
    # Desenha os rótulos dos vértices
    nx.draw_networkx_labels(g_nx, pos)
    
    plt.title("Ciclo Euleriano")
    plt.axis('off')
    
    # Salva a imagem ou mostra na tela
    if arquivo:
        plt.savefig(arquivo)
    else:
        plt.show()
