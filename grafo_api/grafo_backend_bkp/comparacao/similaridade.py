"""
Implementação de métricas de similaridade entre grafos.

Este módulo contém funções para calcular métricas de similaridade entre grafos,
permitindo comparações mesmo quando os grafos não são isomorfos.
"""

import networkx as nx
import numpy as np
from typing import Dict, List, Any, Optional, Set, Tuple
from core.grafo import Grafo


def similaridade_estrutural(grafo1: Grafo, grafo2: Grafo) -> float:
    """
    Calcula uma métrica de similaridade estrutural entre dois grafos.
    
    Esta métrica é baseada na comparação de propriedades estruturais como
    número de vértices, arestas, distribuição de graus, etc.
    
    Args:
        grafo1: Primeiro grafo.
        grafo2: Segundo grafo.
        
    Returns:
        float: Valor entre 0 e 1, onde 1 indica grafos idênticos estruturalmente.
    """
    # Obtém os grafos NetworkX subjacentes
    g1_nx = grafo1.obter_grafo_networkx()
    g2_nx = grafo2.obter_grafo_networkx()
    
    # Calcula propriedades básicas
    n1 = g1_nx.number_of_nodes()
    n2 = g2_nx.number_of_nodes()
    e1 = g1_nx.number_of_edges()
    e2 = g2_nx.number_of_edges()
    
    # Similaridade baseada no número de vértices e arestas
    sim_vertices = 1.0 - abs(n1 - n2) / max(n1, n2, 1)
    sim_arestas = 1.0 - abs(e1 - e2) / max(e1, e2, 1)
    
    # Similaridade baseada na distribuição de graus
    graus1 = sorted([d for _, d in g1_nx.degree()])
    graus2 = sorted([d for _, d in g2_nx.degree()])
    
    # Normaliza as distribuições para comparação
    max_len = max(len(graus1), len(graus2))
    if max_len > 0:
        graus1_norm = graus1 + [0] * (max_len - len(graus1))
        graus2_norm = graus2 + [0] * (max_len - len(graus2))
        
        # Calcula a distância euclidiana normalizada
        dist_graus = np.linalg.norm(np.array(graus1_norm) - np.array(graus2_norm))
        max_dist = np.linalg.norm(np.array(graus1_norm))
        
        sim_graus = 1.0 - dist_graus / max(max_dist, 1.0)
    else:
        sim_graus = 1.0
    
    # Similaridade baseada na conectividade
    conexo1 = nx.is_connected(g1_nx)
    conexo2 = nx.is_connected(g2_nx)
    sim_conexo = 1.0 if conexo1 == conexo2 else 0.0
    
    # Similaridade baseada no número de componentes
    comp1 = nx.number_connected_components(g1_nx)
    comp2 = nx.number_connected_components(g2_nx)
    sim_comp = 1.0 - abs(comp1 - comp2) / max(comp1, comp2, 1)
    
    # Combina as métricas com pesos
    similaridade = (
        0.2 * sim_vertices +
        0.2 * sim_arestas +
        0.3 * sim_graus +
        0.15 * sim_conexo +
        0.15 * sim_comp
    )
    
    return similaridade


def similaridade_espectral(grafo1: Grafo, grafo2: Grafo) -> float:
    """
    Calcula a similaridade espectral entre dois grafos.
    
    Esta métrica é baseada na comparação dos autovalores da matriz laplaciana dos grafos.
    
    Args:
        grafo1: Primeiro grafo.
        grafo2: Segundo grafo.
        
    Returns:
        float: Valor entre 0 e 1, onde 1 indica grafos espectralmente idênticos.
    """
    try:
        # Obtém os grafos NetworkX subjacentes
        g1_nx = grafo1.obter_grafo_networkx()
        g2_nx = grafo2.obter_grafo_networkx()
        
        # Calcula os autovalores da matriz laplaciana
        autovalores1 = sorted(nx.laplacian_spectrum(g1_nx))
        autovalores2 = sorted(nx.laplacian_spectrum(g2_nx))
        
        # Normaliza os autovalores para comparação
        max_len = max(len(autovalores1), len(autovalores2))
        autovalores1_norm = list(autovalores1) + [0] * (max_len - len(autovalores1))
        autovalores2_norm = list(autovalores2) + [0] * (max_len - len(autovalores2))
        
        # Calcula a distância euclidiana normalizada
        dist = np.linalg.norm(np.array(autovalores1_norm) - np.array(autovalores2_norm))
        max_dist = np.linalg.norm(np.array(autovalores1_norm))
        
        # Calcula a similaridade
        similaridade = 1.0 - dist / max(max_dist, 1.0)
        
        return similaridade
    except:
        # Em caso de erro no cálculo dos autovalores, retorna uma estimativa baseada na estrutura
        return similaridade_estrutural(grafo1, grafo2)


def distancia_edicao(grafo1: Grafo, grafo2: Grafo) -> float:
    """
    Calcula uma aproximação da distância de edição entre dois grafos.
    
    A distância de edição é o número mínimo de operações (adição/remoção de vértices/arestas)
    necessárias para transformar um grafo em outro.
    
    Args:
        grafo1: Primeiro grafo.
        grafo2: Segundo grafo.
        
    Returns:
        float: Distância de edição aproximada.
    """
    # Obtém os grafos NetworkX subjacentes
    g1_nx = grafo1.obter_grafo_networkx()
    g2_nx = grafo2.obter_grafo_networkx()
    
    # Número de vértices e arestas
    n1 = g1_nx.number_of_nodes()
    n2 = g2_nx.number_of_nodes()
    e1 = g1_nx.number_of_edges()
    e2 = g2_nx.number_of_edges()
    
    # Diferença no número de vértices
    diff_vertices = abs(n1 - n2)
    
    # Diferença no número de arestas
    diff_arestas = abs(e1 - e2)
    
    # Estimativa da distância de edição
    distancia = diff_vertices + diff_arestas
    
    # Se os grafos têm o mesmo número de vértices, tenta uma estimativa melhor
    if n1 == n2:
        try:
            # Tenta encontrar um mapeamento entre os vértices
            from networkx.algorithms import isomorphism
            matcher = isomorphism.GraphMatcher(g1_nx, g2_nx)
            
            # Se os grafos são isomorfos, a distância é apenas a diferença de arestas
            if matcher.is_isomorphic():
                return diff_arestas
            
            # Caso contrário, estima com base nas diferenças estruturais
            distancia = diff_arestas + n1 * (1.0 - similaridade_estrutural(grafo1, grafo2))
        except:
            pass
    
    return distancia


def matriz_similaridade(grafos: List[Grafo], metrica: str = 'estrutural') -> np.ndarray:
    """
    Calcula a matriz de similaridade entre múltiplos grafos.
    
    Args:
        grafos: Lista de grafos a serem comparados.
        metrica: Métrica de similaridade a ser utilizada ('estrutural' ou 'espectral').
        
    Returns:
        np.ndarray: Matriz de similaridade, onde cada elemento [i,j] é a similaridade entre os grafos i e j.
    """
    n = len(grafos)
    matriz = np.zeros((n, n))
    
    for i in range(n):
        for j in range(i, n):
            if i == j:
                matriz[i, j] = 1.0
            else:
                if metrica == 'espectral':
                    sim = similaridade_espectral(grafos[i], grafos[j])
                else:
                    sim = similaridade_estrutural(grafos[i], grafos[j])
                matriz[i, j] = sim
                matriz[j, i] = sim
    
    return matriz
