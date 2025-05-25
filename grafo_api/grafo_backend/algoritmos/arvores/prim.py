"""
Implementação do algoritmo de Prim para encontrar árvores geradoras mínimas.

O algoritmo de Prim constrói uma árvore geradora mínima iniciando de um vértice
arbitrário e adicionando iterativamente a aresta de menor peso que conecta a árvore
parcial a um novo vértice.
"""

from typing import Dict, List, Any, Tuple, Set
import heapq
import networkx as nx
from ...core.grafo import Grafo


def prim(grafo: Grafo, raiz: Any = None) -> Tuple[Grafo, float]:
    """
    Implementa o algoritmo de Prim para encontrar uma árvore geradora mínima.
    
    Args:
        grafo: Grafo ponderado não direcionado.
        raiz: Vértice inicial (opcional). Se não for especificado, um vértice arbitrário será escolhido.
        
    Returns:
        Tuple[Grafo, float]: Tupla contendo:
            - Grafo representando a árvore geradora mínima
            - Peso total da árvore geradora mínima
            
    Raises:
        ValueError: Se o grafo for direcionado.
        ValueError: Se o grafo não for conexo.
        ValueError: Se o grafo não tiver vértices.
    """
    # Verifica se o grafo é direcionado
    if grafo.eh_direcionado():
        raise ValueError("O algoritmo de Prim só é aplicável a grafos não direcionados.")
    
    # Verifica se o grafo tem vértices
    vertices = list(grafo.obter_vertices())
    if not vertices:
        raise ValueError("O grafo não possui vértices.")
    
    # Se a raiz não for especificada, escolhe o primeiro vértice
    if raiz is None:
        raiz = vertices[0]
    elif not grafo.existe_vertice(raiz):
        raise ValueError(f"Vértice raiz '{raiz}' não existe no grafo.")
    
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Inicializa as estruturas de dados
    arvore = Grafo("Árvore Geradora Mínima")
    for vertice in vertices:
        arvore.adicionar_vertice(vertice)
    
    visitados = {raiz}
    arestas = []
    peso_total = 0.0
    
    # Fila de prioridade para as arestas
    fila_prioridade = []
    
    # Adiciona todas as arestas adjacentes à raiz na fila de prioridade
    for vizinho in grafo.obter_adjacentes(raiz):
        peso = g_nx[raiz][vizinho].get('weight', 1.0)
        heapq.heappush(fila_prioridade, (peso, raiz, vizinho))
    
    # Enquanto não visitou todos os vértices e há arestas na fila
    while fila_prioridade and len(visitados) < len(vertices):
        # Remove a aresta de menor peso
        peso, u, v = heapq.heappop(fila_prioridade)
        
        # Se o vértice de destino já foi visitado, continua
        if v in visitados:
            continue
        
        # Adiciona o vértice de destino ao conjunto de visitados
        visitados.add(v)
        
        # Adiciona a aresta à árvore
        arvore.adicionar_aresta(u, v, peso)
        arestas.append((u, v, peso))
        peso_total += peso
        
        # Adiciona todas as arestas adjacentes ao novo vértice na fila de prioridade
        for vizinho in grafo.obter_adjacentes(v):
            if vizinho not in visitados:
                peso = g_nx[v][vizinho].get('weight', 1.0)
                heapq.heappush(fila_prioridade, (peso, v, vizinho))
    
    # Verifica se a árvore contém todos os vértices
    if len(visitados) < len(vertices):
        raise ValueError("O grafo não é conexo.")
    
    return arvore, peso_total


def comparar_prim_kruskal(grafo: Grafo) -> Dict[str, Any]:
    """
    Compara os algoritmos de Prim e Kruskal para o mesmo grafo.
    
    Args:
        grafo: Grafo ponderado não direcionado.
        
    Returns:
        Dict[str, Any]: Dicionário contendo:
            - 'prim_arvore': Árvore geradora mínima encontrada pelo algoritmo de Prim
            - 'prim_peso': Peso total da árvore encontrada pelo Prim
            - 'kruskal_arvore': Árvore geradora mínima encontrada pelo algoritmo de Kruskal
            - 'kruskal_peso': Peso total da árvore encontrada pelo Kruskal
            - 'iguais': Booleano indicando se as árvores têm o mesmo peso
            
    Raises:
        ValueError: Se o grafo for direcionado.
        ValueError: Se o grafo não for conexo.
    """
    from algoritmos.arvores.kruskal import kruskal
    
    # Executa o algoritmo de Prim
    prim_arvore, prim_peso = prim(grafo)
    
    # Executa o algoritmo de Kruskal
    kruskal_arvore, kruskal_peso = kruskal(grafo)
    
    # Compara os resultados
    return {
        'prim_arvore': prim_arvore,
        'prim_peso': prim_peso,
        'kruskal_arvore': kruskal_arvore,
        'kruskal_peso': kruskal_peso,
        'iguais': abs(prim_peso - kruskal_peso) < 1e-9  # Compara com tolerância para erros de ponto flutuante
    }


def verificar_otimalidade(grafo: Grafo, arvore: Grafo) -> bool:
    """
    Verifica se uma árvore geradora é mínima usando o teorema do corte.
    
    O teorema do corte afirma que uma aresta pertence a uma árvore geradora mínima
    se e somente se é a aresta de menor peso que cruza algum corte do grafo.
    
    Args:
        grafo: Grafo ponderado não direcionado original.
        arvore: Árvore geradora a ser verificada.
        
    Returns:
        bool: True se a árvore for mínima, False caso contrário.
    """
    # Obtém os grafos NetworkX subjacentes
    g_nx = grafo.obter_grafo_networkx()
    arvore_nx = arvore.obter_grafo_networkx()
    
    # Verifica se é uma árvore geradora
    if not nx.is_tree(arvore_nx) or set(arvore_nx.nodes()) != set(g_nx.nodes()):
        return False
    
    # Para cada aresta da árvore
    for u, v, attrs in arvore_nx.edges(data=True):
        # Remove a aresta da árvore para criar um corte
        arvore_nx.remove_edge(u, v)
        
        # Encontra os componentes conexos após a remoção
        componentes = list(nx.connected_components(arvore_nx))
        
        # Encontra a aresta de menor peso que cruza o corte
        menor_peso = float('infinity')
        aresta_menor_peso = None
        
        for comp in componentes:
            for vertice in comp:
                for vizinho in g_nx.neighbors(vertice):
                    if vizinho not in comp:
                        peso = g_nx[vertice][vizinho].get('weight', 1.0)
                        if peso < menor_peso:
                            menor_peso = peso
                            aresta_menor_peso = (vertice, vizinho)
        
        # Restaura a aresta removida
        arvore_nx.add_edge(u, v, **attrs)
        
        # Verifica se a aresta original é a de menor peso
        peso_original = g_nx[u][v].get('weight', 1.0)
        if aresta_menor_peso != (u, v) and aresta_menor_peso != (v, u) and menor_peso < peso_original:
            return False
    
    return True
