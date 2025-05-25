"""
Implementação de métricas de centralidade avançadas para grafos.

Este módulo contém implementações de algoritmos para calcular diferentes métricas
de centralidade em grafos, incluindo centralidade de intermediação (betweenness),
centralidade de autovetor (eigenvector), PageRank e outras.
"""

import networkx as nx
import numpy as np
from typing import Dict, List, Any, Set, Tuple, Optional
from core.grafo import Grafo


def centralidade_grau(grafo: Grafo) -> Dict[Any, float]:
    """
    Calcula a centralidade de grau para todos os vértices do grafo.
    
    A centralidade de grau de um vértice é simplesmente seu grau normalizado
    pelo número máximo possível de vizinhos.
    
    Args:
        grafo: Grafo a ser analisado.
        
    Returns:
        Dict[Any, float]: Dicionário mapeando vértices para suas centralidades de grau.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Número de vértices
    n = g_nx.number_of_nodes()
    
    # Fator de normalização (n-1 é o grau máximo possível)
    normalizacao = 1.0 / max(1, n - 1)
    
    # Calcula a centralidade de grau para cada vértice
    centralidades = {}
    for v in g_nx.nodes():
        centralidades[v] = g_nx.degree(v) * normalizacao
    
    return centralidades


def centralidade_intermediacao(grafo: Grafo, normalizado: bool = True) -> Dict[Any, float]:
    """
    Calcula a centralidade de intermediação (betweenness) para todos os vértices do grafo.
    
    A centralidade de intermediação de um vértice v é a soma das frações de
    caminhos mais curtos entre todos os pares de vértices que passam por v.
    
    Args:
        grafo: Grafo a ser analisado.
        normalizado: Se True, normaliza os valores para o intervalo [0, 1].
        
    Returns:
        Dict[Any, float]: Dicionário mapeando vértices para suas centralidades de intermediação.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Calcula a centralidade de intermediação
    return nx.betweenness_centrality(g_nx, normalized=normalizado)


def centralidade_proximidade(grafo: Grafo) -> Dict[Any, float]:
    """
    Calcula a centralidade de proximidade (closeness) para todos os vértices do grafo.
    
    A centralidade de proximidade de um vértice v é o inverso da soma das
    distâncias de v para todos os outros vértices.
    
    Args:
        grafo: Grafo a ser analisado.
        
    Returns:
        Dict[Any, float]: Dicionário mapeando vértices para suas centralidades de proximidade.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Calcula a centralidade de proximidade
    return nx.closeness_centrality(g_nx)


def centralidade_autovetor(grafo: Grafo, max_iter: int = 100, tol: float = 1e-6) -> Dict[Any, float]:
    """
    Calcula a centralidade de autovetor (eigenvector) para todos os vértices do grafo.
    
    A centralidade de autovetor atribui a cada vértice um valor proporcional à soma
    das centralidades de seus vizinhos.
    
    Args:
        grafo: Grafo a ser analisado.
        max_iter: Número máximo de iterações para o algoritmo de potência.
        tol: Tolerância para convergência.
        
    Returns:
        Dict[Any, float]: Dicionário mapeando vértices para suas centralidades de autovetor.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Calcula a centralidade de autovetor
    return nx.eigenvector_centrality(g_nx, max_iter=max_iter, tol=tol)


def pagerank(grafo: Grafo, alpha: float = 0.85, max_iter: int = 100, tol: float = 1e-6) -> Dict[Any, float]:
    """
    Calcula o PageRank para todos os vértices do grafo.
    
    O PageRank é uma variante da centralidade de autovetor que inclui um fator
    de amortecimento para lidar com sumidouros.
    
    Args:
        grafo: Grafo a ser analisado.
        alpha: Fator de amortecimento (probabilidade de seguir um link).
        max_iter: Número máximo de iterações.
        tol: Tolerância para convergência.
        
    Returns:
        Dict[Any, float]: Dicionário mapeando vértices para seus valores de PageRank.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Calcula o PageRank
    return nx.pagerank(g_nx, alpha=alpha, max_iter=max_iter, tol=tol)


def centralidade_katz(grafo: Grafo, alpha: float = 0.1, beta: float = 1.0, max_iter: int = 1000, tol: float = 1e-6) -> Dict[Any, float]:
    """
    Calcula a centralidade de Katz para todos os vértices do grafo.
    
    A centralidade de Katz é uma variante da centralidade de autovetor que atribui
    uma pequena quantidade de centralidade a cada vértice independentemente de sua conectividade.
    
    Args:
        grafo: Grafo a ser analisado.
        alpha: Fator de atenuação para caminhos de comprimento k.
        beta: Centralidade base atribuída a cada vértice.
        max_iter: Número máximo de iterações.
        tol: Tolerância para convergência.
        
    Returns:
        Dict[Any, float]: Dicionário mapeando vértices para suas centralidades de Katz.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Calcula a centralidade de Katz
    return nx.katz_centrality(g_nx, alpha=alpha, beta=beta, max_iter=max_iter, tol=tol)


def centralidade_intermediacao_arestas(grafo: Grafo, normalizado: bool = True) -> Dict[Tuple[Any, Any], float]:
    """
    Calcula a centralidade de intermediação para todas as arestas do grafo.
    
    A centralidade de intermediação de uma aresta e é a soma das frações de
    caminhos mais curtos entre todos os pares de vértices que passam por e.
    
    Args:
        grafo: Grafo a ser analisado.
        normalizado: Se True, normaliza os valores para o intervalo [0, 1].
        
    Returns:
        Dict[Tuple[Any, Any], float]: Dicionário mapeando arestas para suas centralidades de intermediação.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Calcula a centralidade de intermediação de arestas
    return nx.edge_betweenness_centrality(g_nx, normalized=normalizado)


def centralidade_informacao(grafo: Grafo) -> Dict[Any, float]:
    """
    Calcula a centralidade de informação para todos os vértices do grafo.
    
    A centralidade de informação mede a redução na eficiência da rede quando
    um vértice é removido.
    
    Args:
        grafo: Grafo a ser analisado.
        
    Returns:
        Dict[Any, float]: Dicionário mapeando vértices para suas centralidades de informação.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Calcula a centralidade de informação
    return nx.information_centrality(g_nx)


def centralidade_harmonica(grafo: Grafo) -> Dict[Any, float]:
    """
    Calcula a centralidade harmônica para todos os vértices do grafo.
    
    A centralidade harmônica de um vértice v é a soma dos inversos das
    distâncias de v para todos os outros vértices.
    
    Args:
        grafo: Grafo a ser analisado.
        
    Returns:
        Dict[Any, float]: Dicionário mapeando vértices para suas centralidades harmônicas.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Calcula a centralidade harmônica
    return nx.harmonic_centrality(g_nx)


def centralidade_percolacao(grafo: Grafo, k: int = None) -> Dict[Any, float]:
    """
    Calcula a centralidade de percolação para todos os vértices do grafo.
    
    A centralidade de percolação mede a importância de um vértice na
    disseminação de informações através da rede.
    
    Args:
        grafo: Grafo a ser analisado.
        k: Número de caminhos aleatórios a considerar. Se None, usa um valor padrão.
        
    Returns:
        Dict[Any, float]: Dicionário mapeando vértices para suas centralidades de percolação.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Calcula a centralidade de percolação
    return nx.percolation_centrality(g_nx, k=k)


def calcular_todas_centralidades(grafo: Grafo) -> Dict[str, Dict[Any, float]]:
    """
    Calcula todas as métricas de centralidade para o grafo.
    
    Args:
        grafo: Grafo a ser analisado.
        
    Returns:
        Dict[str, Dict[Any, float]]: Dicionário mapeando nomes de métricas para
                                   dicionários de centralidades.
    """
    centralidades = {}
    
    # Calcula todas as métricas de centralidade
    centralidades["grau"] = centralidade_grau(grafo)
    centralidades["intermediacao"] = centralidade_intermediacao(grafo)
    centralidades["proximidade"] = centralidade_proximidade(grafo)
    
    # Algumas métricas podem falhar em certos grafos, então usamos try-except
    try:
        centralidades["autovetor"] = centralidade_autovetor(grafo)
    except:
        centralidades["autovetor"] = {v: 0.0 for v in grafo.obter_vertices()}
    
    try:
        centralidades["pagerank"] = pagerank(grafo)
    except:
        centralidades["pagerank"] = {v: 0.0 for v in grafo.obter_vertices()}
    
    try:
        centralidades["katz"] = centralidade_katz(grafo)
    except:
        centralidades["katz"] = {v: 0.0 for v in grafo.obter_vertices()}
    
    try:
        centralidades["harmonica"] = centralidade_harmonica(grafo)
    except:
        centralidades["harmonica"] = {v: 0.0 for v in grafo.obter_vertices()}
    
    return centralidades


def identificar_vertices_mais_centrais(grafo: Grafo, metrica: str = "pagerank", k: int = 5) -> List[Tuple[Any, float]]:
    """
    Identifica os k vértices mais centrais segundo uma métrica específica.
    
    Args:
        grafo: Grafo a ser analisado.
        metrica: Nome da métrica de centralidade a usar.
        k: Número de vértices a retornar.
        
    Returns:
        List[Tuple[Any, float]]: Lista de tuplas (vértice, centralidade) ordenada por centralidade.
        
    Raises:
        ValueError: Se a métrica não for reconhecida.
    """
    # Dicionário de funções de centralidade
    metricas = {
        "grau": centralidade_grau,
        "intermediacao": centralidade_intermediacao,
        "proximidade": centralidade_proximidade,
        "autovetor": centralidade_autovetor,
        "pagerank": pagerank,
        "katz": centralidade_katz,
        "harmonica": centralidade_harmonica
    }
    
    # Verifica se a métrica é válida
    if metrica not in metricas:
        raise ValueError(f"Métrica de centralidade '{metrica}' não reconhecida.")
    
    # Calcula a centralidade
    centralidades = metricas[metrica](grafo)
    
    # Ordena os vértices por centralidade e retorna os k mais centrais
    vertices_ordenados = sorted(centralidades.items(), key=lambda x: x[1], reverse=True)
    
    return vertices_ordenados[:k]


def calcular_distribuicao_centralidade(grafo: Grafo, metrica: str = "grau") -> Dict[float, int]:
    """
    Calcula a distribuição de uma métrica de centralidade no grafo.
    
    Args:
        grafo: Grafo a ser analisado.
        metrica: Nome da métrica de centralidade a usar.
        
    Returns:
        Dict[float, int]: Dicionário mapeando valores de centralidade para frequências.
        
    Raises:
        ValueError: Se a métrica não for reconhecida.
    """
    # Dicionário de funções de centralidade
    metricas = {
        "grau": centralidade_grau,
        "intermediacao": centralidade_intermediacao,
        "proximidade": centralidade_proximidade,
        "autovetor": centralidade_autovetor,
        "pagerank": pagerank,
        "katz": centralidade_katz,
        "harmonica": centralidade_harmonica
    }
    
    # Verifica se a métrica é válida
    if metrica not in metricas:
        raise ValueError(f"Métrica de centralidade '{metrica}' não reconhecida.")
    
    # Calcula a centralidade
    centralidades = metricas[metrica](grafo)
    
    # Calcula a distribuição
    distribuicao = {}
    for valor in centralidades.values():
        # Arredonda para evitar problemas de precisão
        valor_arredondado = round(valor, 4)
        if valor_arredondado not in distribuicao:
            distribuicao[valor_arredondado] = 0
        distribuicao[valor_arredondado] += 1
    
    return distribuicao
