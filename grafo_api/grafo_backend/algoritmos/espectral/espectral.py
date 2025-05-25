"""
Implementação de algoritmos de teoria espectral de grafos.

Este módulo contém implementações de algoritmos para análise espectral de grafos,
incluindo cálculo de autovalores e autovetores da matriz laplaciana, clustering
espectral e detecção de comunidades.
"""

import networkx as nx
import numpy as np
from typing import Dict, List, Any, Set, Tuple, Optional
from core.grafo import Grafo
from scipy import sparse
from scipy.sparse.linalg import eigsh
from sklearn.cluster import KMeans


def calcular_matriz_adjacencia(grafo: Grafo) -> np.ndarray:
    """
    Calcula a matriz de adjacência do grafo.
    
    Args:
        grafo: Grafo a ser analisado.
        
    Returns:
        np.ndarray: Matriz de adjacência.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Calcula a matriz de adjacência
    return nx.to_numpy_array(g_nx)


def calcular_matriz_laplaciana(grafo: Grafo) -> np.ndarray:
    """
    Calcula a matriz laplaciana do grafo.
    
    A matriz laplaciana é definida como L = D - A, onde D é a matriz diagonal
    dos graus e A é a matriz de adjacência.
    
    Args:
        grafo: Grafo a ser analisado.
        
    Returns:
        np.ndarray: Matriz laplaciana.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Calcula a matriz laplaciana
    return nx.laplacian_matrix(g_nx).toarray()


def calcular_matriz_laplaciana_normalizada(grafo: Grafo) -> np.ndarray:
    """
    Calcula a matriz laplaciana normalizada do grafo.
    
    A matriz laplaciana normalizada é definida como L_norm = D^(-1/2) L D^(-1/2),
    onde L é a matriz laplaciana e D é a matriz diagonal dos graus.
    
    Args:
        grafo: Grafo a ser analisado.
        
    Returns:
        np.ndarray: Matriz laplaciana normalizada.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Calcula a matriz laplaciana normalizada
    return nx.normalized_laplacian_matrix(g_nx).toarray()


def calcular_autovalores_laplaciana(grafo: Grafo, k: int = None) -> np.ndarray:
    """
    Calcula os autovalores da matriz laplaciana do grafo.
    
    Args:
        grafo: Grafo a ser analisado.
        k: Número de autovalores a calcular. Se None, calcula todos.
        
    Returns:
        np.ndarray: Array de autovalores em ordem crescente.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Número de vértices
    n = g_nx.number_of_nodes()
    
    # Se k não for especificado, calcula todos os autovalores
    if k is None:
        k = n
    
    # Limita k ao número de vértices
    k = min(k, n)
    
    # Calcula a matriz laplaciana como matriz esparsa
    L = nx.laplacian_matrix(g_nx)
    
    # Para grafos pequenos, usa numpy
    if n < 500:
        # Converte para array denso
        L_dense = L.toarray()
        # Calcula todos os autovalores
        autovalores = np.linalg.eigvalsh(L_dense)
        # Retorna os k menores autovalores
        return np.sort(autovalores)[:k]
    
    # Para grafos grandes, usa eigsh para calcular apenas os k menores autovalores
    autovalores, _ = eigsh(L, k=k, which='SM')
    
    return np.sort(autovalores)


def calcular_autovetores_laplaciana(grafo: Grafo, k: int = None) -> Tuple[np.ndarray, np.ndarray]:
    """
    Calcula os autovalores e autovetores da matriz laplaciana do grafo.
    
    Args:
        grafo: Grafo a ser analisado.
        k: Número de autovalores/autovetores a calcular. Se None, calcula todos.
        
    Returns:
        Tuple[np.ndarray, np.ndarray]: Tupla contendo (autovalores, autovetores).
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Número de vértices
    n = g_nx.number_of_nodes()
    
    # Se k não for especificado, calcula todos os autovalores/autovetores
    if k is None:
        k = n
    
    # Limita k ao número de vértices
    k = min(k, n)
    
    # Calcula a matriz laplaciana como matriz esparsa
    L = nx.laplacian_matrix(g_nx)
    
    # Para grafos pequenos, usa numpy
    if n < 500:
        # Converte para array denso
        L_dense = L.toarray()
        # Calcula todos os autovalores e autovetores
        autovalores, autovetores = np.linalg.eigh(L_dense)
        # Ordena os autovalores e autovetores correspondentes
        idx = autovalores.argsort()
        autovalores = autovalores[idx]
        autovetores = autovetores[:, idx]
        # Retorna os k menores autovalores e seus autovetores
        return autovalores[:k], autovetores[:, :k]
    
    # Para grafos grandes, usa eigsh para calcular apenas os k menores autovalores/autovetores
    autovalores, autovetores = eigsh(L, k=k, which='SM')
    
    # Ordena os autovalores e autovetores correspondentes
    idx = autovalores.argsort()
    autovalores = autovalores[idx]
    autovetores = autovetores[:, idx]
    
    return autovalores, autovetores


def calcular_conectividade_algebrica(grafo: Grafo) -> float:
    """
    Calcula a conectividade algébrica do grafo.
    
    A conectividade algébrica é o segundo menor autovalor da matriz laplaciana.
    
    Args:
        grafo: Grafo a ser analisado.
        
    Returns:
        float: Conectividade algébrica.
    """
    # Calcula os dois menores autovalores
    autovalores = calcular_autovalores_laplaciana(grafo, k=2)
    
    # Retorna o segundo menor autovalor
    return autovalores[1]


def clustering_espectral(grafo: Grafo, n_clusters: int) -> Dict[Any, int]:
    """
    Realiza clustering espectral no grafo.
    
    Args:
        grafo: Grafo a ser analisado.
        n_clusters: Número de clusters.
        
    Returns:
        Dict[Any, int]: Dicionário mapeando vértices para seus clusters.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Lista de vértices na ordem usada pela matriz
    vertices = list(g_nx.nodes())
    
    # Calcula os autovetores da matriz laplaciana normalizada
    _, autovetores = calcular_autovetores_laplaciana(grafo, k=n_clusters)
    
    # Usa K-means para agrupar os vértices com base nos autovetores
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    clusters = kmeans.fit_predict(autovetores)
    
    # Mapeia vértices para clusters
    resultado = {}
    for i, vertice in enumerate(vertices):
        resultado[vertice] = int(clusters[i])
    
    return resultado


def detectar_comunidades_espectral(grafo: Grafo, max_comunidades: int = 10) -> Dict[Any, int]:
    """
    Detecta comunidades no grafo usando métodos espectrais.
    
    Args:
        grafo: Grafo a ser analisado.
        max_comunidades: Número máximo de comunidades a detectar.
        
    Returns:
        Dict[Any, int]: Dicionário mapeando vértices para suas comunidades.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Número de vértices
    n = g_nx.number_of_nodes()
    
    # Limita o número máximo de comunidades
    max_comunidades = min(max_comunidades, n // 2)
    
    # Calcula a conectividade algébrica para diferentes números de comunidades
    melhores_scores = []
    for k in range(2, max_comunidades + 1):
        # Realiza clustering espectral
        clusters = clustering_espectral(grafo, k)
        
        # Calcula a modularidade como medida de qualidade
        modularidade = calcular_modularidade(grafo, clusters)
        melhores_scores.append((k, modularidade))
    
    # Encontra o número de comunidades com maior modularidade
    k_otimo = max(melhores_scores, key=lambda x: x[1])[0]
    
    # Retorna o clustering com o número ótimo de comunidades
    return clustering_espectral(grafo, k_otimo)


def calcular_modularidade(grafo: Grafo, comunidades: Dict[Any, int]) -> float:
    """
    Calcula a modularidade de uma partição de comunidades.
    
    A modularidade mede a qualidade de uma divisão em comunidades.
    
    Args:
        grafo: Grafo a ser analisado.
        comunidades: Dicionário mapeando vértices para suas comunidades.
        
    Returns:
        float: Valor da modularidade.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Converte o dicionário para o formato esperado pelo NetworkX
    comunidades_nx = {}
    for vertice, comunidade in comunidades.items():
        if comunidade not in comunidades_nx:
            comunidades_nx[comunidade] = []
        comunidades_nx[comunidade].append(vertice)
    
    # Calcula a modularidade
    return nx.algorithms.community.modularity(g_nx, comunidades_nx.values())


def calcular_espectro_normalizado(grafo: Grafo) -> np.ndarray:
    """
    Calcula o espectro normalizado do grafo.
    
    O espectro normalizado é o conjunto de autovalores da matriz laplaciana normalizada.
    
    Args:
        grafo: Grafo a ser analisado.
        
    Returns:
        np.ndarray: Array de autovalores em ordem crescente.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Calcula a matriz laplaciana normalizada
    L_norm = nx.normalized_laplacian_matrix(g_nx).toarray()
    
    # Calcula os autovalores
    autovalores = np.linalg.eigvalsh(L_norm)
    
    return np.sort(autovalores)


def calcular_energia_espectral(grafo: Grafo) -> float:
    """
    Calcula a energia espectral do grafo.
    
    A energia espectral é a soma dos valores absolutos dos autovalores da matriz de adjacência.
    
    Args:
        grafo: Grafo a ser analisado.
        
    Returns:
        float: Energia espectral.
    """
    # Calcula a matriz de adjacência
    A = calcular_matriz_adjacencia(grafo)
    
    # Calcula os autovalores
    autovalores = np.linalg.eigvalsh(A)
    
    # Calcula a energia espectral
    return np.sum(np.abs(autovalores))


def calcular_distancia_espectral(grafo1: Grafo, grafo2: Grafo) -> float:
    """
    Calcula a distância espectral entre dois grafos.
    
    A distância espectral é a norma euclidiana da diferença entre os espectros dos grafos.
    
    Args:
        grafo1: Primeiro grafo.
        grafo2: Segundo grafo.
        
    Returns:
        float: Distância espectral.
        
    Raises:
        ValueError: Se os grafos têm números diferentes de vértices.
    """
    # Obtém os grafos NetworkX subjacentes
    g1_nx = grafo1.obter_grafo_networkx()
    g2_nx = grafo2.obter_grafo_networkx()
    
    # Verifica se os grafos têm o mesmo número de vértices
    if g1_nx.number_of_nodes() != g2_nx.number_of_nodes():
        raise ValueError("Os grafos devem ter o mesmo número de vértices.")
    
    # Calcula os espectros normalizados
    espectro1 = calcular_espectro_normalizado(grafo1)
    espectro2 = calcular_espectro_normalizado(grafo2)
    
    # Calcula a distância espectral
    return np.linalg.norm(espectro1 - espectro2)
