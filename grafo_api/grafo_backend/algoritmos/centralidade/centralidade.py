"""
Módulo de algoritmos de centralidade em grafos.

Este módulo contém implementações de algoritmos para calcular diferentes medidas de centralidade
em grafos, incluindo centralidade de grau, intermediação, proximidade, autovetor, PageRank e Katz.
"""

from typing import Dict, Any, Optional
import networkx as nx
from grafo_backend.core.grafo import Grafo


def centralidade_grau(grafo: Grafo) -> Dict[Any, float]:
    """
    Calcula a centralidade de grau para todos os vértices do grafo.
    
    Args:
        grafo: Grafo a ser analisado.
        
    Returns:
        Dict[Any, float]: Dicionário mapeando vértices para seus valores de centralidade de grau.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Calcula a centralidade de grau
    centralidade = nx.degree_centrality(g_nx)
    
    return centralidade


def centralidade_intermediacao(grafo: Grafo, normalizado: bool = True) -> Dict[Any, float]:
    """
    Calcula a centralidade de intermediação para todos os vértices do grafo.
    
    Args:
        grafo: Grafo a ser analisado.
        normalizado: Se True, normaliza os valores de centralidade.
        
    Returns:
        Dict[Any, float]: Dicionário mapeando vértices para seus valores de centralidade de intermediação.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Calcula a centralidade de intermediação
    centralidade = nx.betweenness_centrality(g_nx, normalized=normalizado)
    
    return centralidade


def centralidade_proximidade(grafo: Grafo) -> Dict[Any, float]:
    """
    Calcula a centralidade de proximidade para todos os vértices do grafo.
    
    Args:
        grafo: Grafo a ser analisado.
        
    Returns:
        Dict[Any, float]: Dicionário mapeando vértices para seus valores de centralidade de proximidade.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Calcula a centralidade de proximidade
    centralidade = nx.closeness_centrality(g_nx)
    
    return centralidade


def centralidade_autovetor(grafo: Grafo, max_iter: int = 100, tol: float = 1e-6) -> Dict[Any, float]:
    """
    Calcula a centralidade de autovetor para todos os vértices do grafo.
    
    Args:
        grafo: Grafo a ser analisado.
        max_iter: Número máximo de iterações.
        tol: Tolerância para convergência.
        
    Returns:
        Dict[Any, float]: Dicionário mapeando vértices para seus valores de centralidade de autovetor.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Calcula a centralidade de autovetor
    centralidade = nx.eigenvector_centrality(g_nx, max_iter=max_iter, tol=tol)
    
    return centralidade


def pagerank(grafo: Grafo, alpha: float = 0.85, max_iter: int = 100, tol: float = 1e-6) -> Dict[Any, float]:
    """
    Calcula o PageRank para todos os vértices do grafo.
    
    Args:
        grafo: Grafo a ser analisado.
        alpha: Fator de amortecimento.
        max_iter: Número máximo de iterações.
        tol: Tolerância para convergência.
        
    Returns:
        Dict[Any, float]: Dicionário mapeando vértices para seus valores de PageRank.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Calcula o PageRank
    centralidade = nx.pagerank(g_nx, alpha=alpha, max_iter=max_iter, tol=tol)
    
    return centralidade


def centralidade_katz(grafo: Grafo, alpha: Optional[float] = None, beta: float = 1.0, max_iter: int = 100, tol: float = 1e-6) -> Dict[Any, float]:
    """
    Calcula a centralidade de Katz para todos os vértices do grafo.
    
    Args:
        grafo: Grafo a ser analisado.
        alpha: Fator de atenuação. Se None, usa 1/lambda_max.
        beta: Peso do vetor de excentricidade.
        max_iter: Número máximo de iterações.
        tol: Tolerância para convergência.
        
    Returns:
        Dict[Any, float]: Dicionário mapeando vértices para seus valores de centralidade de Katz.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Calcula a centralidade de Katz
    centralidade = nx.katz_centrality(g_nx, alpha=alpha, beta=beta, max_iter=max_iter, tol=tol)
    
    return centralidade
