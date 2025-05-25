"""
Implementação do algoritmo Húngaro (Hungarian Algorithm) para o problema de atribuição ótima.

O algoritmo Húngaro resolve o problema de atribuição ótima em tempo O(n³),
encontrando a atribuição de custo mínimo em uma matriz de custos.
"""

from typing import Dict, List, Any, Tuple, Set, Optional
import numpy as np
import networkx as nx
from grafo_backend.core.grafo import Grafo


def hungarian_algorithm(matriz_custos: np.ndarray) -> Tuple[List[Tuple[int, int]], float]:
    """
    Implementa o algoritmo Húngaro para resolver o problema de atribuição ótima.
    
    Args:
        matriz_custos: Matriz de custos n x n, onde matriz_custos[i, j] é o custo de atribuir i a j.
        
    Returns:
        Tuple[List[Tuple[int, int]], float]: Tupla contendo:
            - Lista de tuplas (i, j) representando a atribuição ótima
            - Custo total da atribuição
    """
    # Verifica se a matriz é quadrada
    n, m = matriz_custos.shape
    if n != m:
        raise ValueError("A matriz de custos deve ser quadrada.")
    
    # Cria uma cópia da matriz de custos
    matriz = matriz_custos.copy()
    
    # Passo 1: Subtrai o menor valor de cada linha
    for i in range(n):
        matriz[i, :] -= np.min(matriz[i, :])
    
    # Passo 2: Subtrai o menor valor de cada coluna
    for j in range(n):
        matriz[:, j] -= np.min(matriz[:, j])
    
    # Inicializa a atribuição
    linha_para_coluna = {}  # Mapeamento de linhas para colunas
    coluna_para_linha = {}  # Mapeamento de colunas para linhas
    
    # Função para encontrar um caminho aumentante usando DFS
    def encontrar_caminho_aumentante(i: int, visitados_linha: Set[int], visitados_coluna: Set[int]) -> bool:
        visitados_linha.add(i)
        
        for j in range(n):
            if matriz[i, j] == 0 and j not in visitados_coluna:
                visitados_coluna.add(j)
                
                if j not in coluna_para_linha or encontrar_caminho_aumentante(coluna_para_linha[j], visitados_linha, visitados_coluna):
                    linha_para_coluna[i] = j
                    coluna_para_linha[j] = i
                    return True
        
        return False
    
    # Enquanto não encontrar uma atribuição completa
    while len(linha_para_coluna) < n:
        # Encontra um caminho aumentante para cada linha não atribuída
        for i in range(n):
            if i not in linha_para_coluna:
                visitados_linha = set()
                visitados_coluna = set()
                
                if not encontrar_caminho_aumentante(i, visitados_linha, visitados_coluna):
                    # Se não encontrou um caminho aumentante, ajusta a matriz
                    # Encontra o menor valor não coberto
                    min_valor = float('infinity')
                    for i in range(n):
                        if i not in visitados_linha:
                            for j in range(n):
                                if j not in visitados_coluna:
                                    min_valor = min(min_valor, matriz[i, j])
                    
                    # Subtrai o menor valor das linhas não visitadas
                    for i in range(n):
                        if i not in visitados_linha:
                            matriz[i, :] -= min_valor
                    
                    # Adiciona o menor valor às colunas visitadas
                    for j in range(n):
                        if j in visitados_coluna:
                            matriz[:, j] += min_valor
                    
                    # Tenta novamente
                    break
    
    # Calcula o custo total da atribuição
    custo_total = 0
    atribuicao = []
    
    for i, j in linha_para_coluna.items():
        custo_total += matriz_custos[i, j]
        atribuicao.append((i, j))
    
    return atribuicao, custo_total


def atribuicao_otima_grafo(grafo: Grafo, conjunto_a: Set[Any], conjunto_b: Set[Any], 
                          funcao_custo: callable = None) -> Dict[Any, Any]:
    """
    Resolve o problema de atribuição ótima em um grafo bipartido.
    
    Args:
        grafo: Grafo bipartido.
        conjunto_a: Conjunto de vértices do lado A.
        conjunto_b: Conjunto de vértices do lado B.
        funcao_custo: Função que retorna o custo de atribuir um vértice de A a um vértice de B.
                     Se não for fornecida, usa o peso da aresta.
        
    Returns:
        Dict[Any, Any]: Dicionário mapeando vértices do conjunto A para seus pares no conjunto B.
            
    Raises:
        ValueError: Se o grafo não for bipartido.
        ValueError: Se os conjuntos A e B não formarem uma partição do grafo.
    """
    # Verifica se os conjuntos A e B são disjuntos
    if conjunto_a & conjunto_b:
        raise ValueError("Os conjuntos A e B devem ser disjuntos.")
    
    # Verifica se os conjuntos A e B contêm todos os vértices do grafo
    if conjunto_a | conjunto_b != set(grafo.obter_vertices()):
        raise ValueError("Os conjuntos A e B devem conter todos os vértices do grafo.")
    
    # Verifica se o grafo é bipartido
    g_nx = grafo.obter_grafo_networkx()
    for u, v in g_nx.edges():
        if (u in conjunto_a and v in conjunto_a) or (u in conjunto_b and v in conjunto_b):
            raise ValueError("O grafo não é bipartido com a partição fornecida.")
    
    # Se os conjuntos têm tamanhos diferentes, adiciona vértices fictícios
    n = max(len(conjunto_a), len(conjunto_b))
    
    # Cria listas ordenadas dos vértices
    vertices_a = list(conjunto_a)
    vertices_b = list(conjunto_b)
    
    # Adiciona vértices fictícios se necessário
    vertices_a_ficticios = vertices_a + [f"ficticio_a_{i}" for i in range(len(vertices_a), n)]
    vertices_b_ficticios = vertices_b + [f"ficticio_b_{i}" for i in range(len(vertices_b), n)]
    
    # Cria a matriz de custos
    matriz_custos = np.full((n, n), float('infinity'))
    
    # Preenche a matriz de custos
    for i, u in enumerate(vertices_a_ficticios):
        for j, v in enumerate(vertices_b_ficticios):
            if u in conjunto_a and v in conjunto_b:
                if grafo.existe_aresta(u, v):
                    if funcao_custo:
                        matriz_custos[i, j] = funcao_custo(u, v)
                    else:
                        matriz_custos[i, j] = g_nx[u][v].get('weight', 1.0)
                else:
                    matriz_custos[i, j] = float('infinity')
            else:
                # Custo alto para vértices fictícios
                matriz_custos[i, j] = 0
    
    # Resolve o problema de atribuição
    atribuicao, _ = hungarian_algorithm(matriz_custos)
    
    # Converte a atribuição de volta para os vértices originais
    resultado = {}
    
    for i, j in atribuicao:
        u = vertices_a_ficticios[i]
        v = vertices_b_ficticios[j]
        
        if u in conjunto_a and v in conjunto_b:
            resultado[u] = v
    
    return resultado


def verificar_atribuicao_otima(matriz_custos: np.ndarray, atribuicao: List[Tuple[int, int]]) -> bool:
    """
    Verifica se uma atribuição é ótima usando o teorema da dualidade.
    
    Args:
        matriz_custos: Matriz de custos n x n.
        atribuicao: Lista de tuplas (i, j) representando a atribuição.
        
    Returns:
        bool: True se a atribuição for ótima, False caso contrário.
    """
    n = matriz_custos.shape[0]
    
    # Calcula o custo da atribuição
    custo_atribuicao = sum(matriz_custos[i, j] for i, j in atribuicao)
    
    # Resolve o problema dual
    u = np.zeros(n)
    v = np.zeros(n)
    
    # Inicializa u e v
    for i, j in atribuicao:
        u[i] = matriz_custos[i, j]
    
    # Ajusta u e v para satisfazer as restrições de dualidade
    for i in range(n):
        for j in range(n):
            v[j] = max(v[j], matriz_custos[i, j] - u[i])
    
    # Calcula o valor da solução dual
    valor_dual = sum(u) + sum(v)
    
    # Pelo teorema da dualidade, a atribuição é ótima se o custo for igual ao valor dual
    return abs(custo_atribuicao - valor_dual) < 1e-9


def visualizar_atribuicao(grafo: Grafo, conjunto_a: Set[Any], conjunto_b: Set[Any], 
                         atribuicao: Dict[Any, Any], arquivo: str = None) -> None:
    """
    Visualiza a atribuição ótima em um grafo bipartido.
    
    Args:
        grafo: Grafo bipartido.
        conjunto_a: Conjunto de vértices do lado A.
        conjunto_b: Conjunto de vértices do lado B.
        atribuicao: Dicionário mapeando vértices do conjunto A para seus pares no conjunto B.
        arquivo: Caminho para salvar a imagem (opcional).
    """
    import matplotlib.pyplot as plt
    import networkx as nx
    
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
    
    # Desenha as arestas não atribuídas
    arestas_nao_atribuidas = [(u, v) for u, v in g_nx.edges() if u not in atribuicao or atribuicao[u] != v]
    nx.draw_networkx_edges(g_nx, pos, edgelist=arestas_nao_atribuidas, width=1, alpha=0.5)
    
    # Desenha as arestas atribuídas
    arestas_atribuidas = [(u, atribuicao[u]) for u in atribuicao]
    nx.draw_networkx_edges(g_nx, pos, edgelist=arestas_atribuidas, width=3, edge_color='red')
    
    # Desenha os rótulos dos vértices
    nx.draw_networkx_labels(g_nx, pos)
    
    plt.title(f"Atribuição Ótima (tamanho: {len(atribuicao)})")
    plt.axis('off')
    
    # Salva a imagem ou mostra na tela
    if arquivo:
        plt.savefig(arquivo)
    else:
        plt.show()
