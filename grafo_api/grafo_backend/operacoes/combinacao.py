"""
Implementação de operações de combinação entre grafos.

Este módulo contém funções para realizar operações de união, interseção e diferença entre grafos.
"""

import networkx as nx
from typing import Dict, List, Any, Optional, Set, Tuple, Union
from core.grafo import Grafo


def uniao_grafos(grafo1: Grafo, grafo2: Grafo, nome_resultado: str = None) -> Grafo:
    """
    Realiza a união de dois grafos.
    
    A união de dois grafos G1 = (V1, E1) e G2 = (V2, E2) é um grafo G = (V, E) onde:
    V = V1 ∪ V2 e E = E1 ∪ E2
    
    Args:
        grafo1: Primeiro grafo.
        grafo2: Segundo grafo.
        nome_resultado: Nome do grafo resultante. Se None, usa "União de {grafo1.nome} e {grafo2.nome}".
        
    Returns:
        Grafo: Grafo resultante da união.
    """
    # Define o nome do grafo resultante
    if nome_resultado is None:
        nome_resultado = f"União de {grafo1.nome} e {grafo2.nome}"
    
    # Cria um novo grafo
    resultado = Grafo(nome_resultado)
    
    # Obtém os grafos NetworkX subjacentes
    g1_nx = grafo1.obter_grafo_networkx()
    g2_nx = grafo2.obter_grafo_networkx()
    
    # Realiza a união dos grafos NetworkX usando compose (que permite nós comuns)
    g_uniao = nx.compose(g1_nx, g2_nx)
    
    # Define o grafo resultante
    resultado.definir_grafo_networkx(g_uniao)
    
    return resultado


def intersecao_grafos(grafo1: Grafo, grafo2: Grafo, nome_resultado: str = None) -> Grafo:
    """
    Realiza a interseção de dois grafos.
    
    A interseção de dois grafos G1 = (V1, E1) e G2 = (V2, E2) é um grafo G = (V, E) onde:
    V = V1 ∩ V2 e E = E1 ∩ E2
    
    Args:
        grafo1: Primeiro grafo.
        grafo2: Segundo grafo.
        nome_resultado: Nome do grafo resultante. Se None, usa "Interseção de {grafo1.nome} e {grafo2.nome}".
        
    Returns:
        Grafo: Grafo resultante da interseção.
    """
    # Define o nome do grafo resultante
    if nome_resultado is None:
        nome_resultado = f"Interseção de {grafo1.nome} e {grafo2.nome}"
    
    # Cria um novo grafo
    resultado = Grafo(nome_resultado)
    
    # Obtém os grafos NetworkX subjacentes
    g1_nx = grafo1.obter_grafo_networkx()
    g2_nx = grafo2.obter_grafo_networkx()
    
    # Realiza a interseção dos grafos NetworkX
    g_intersecao = nx.intersection(g1_nx, g2_nx)
    
    # Define o grafo resultante
    resultado.definir_grafo_networkx(g_intersecao)
    
    return resultado


def diferenca_grafos(grafo1: Grafo, grafo2: Grafo, nome_resultado: str = None) -> Grafo:
    """
    Realiza a diferença entre dois grafos.
    
    A diferença entre dois grafos G1 = (V1, E1) e G2 = (V2, E2) é um grafo G = (V, E) onde:
    V = V1 e E = E1 - E2
    
    Args:
        grafo1: Primeiro grafo (minuendo).
        grafo2: Segundo grafo (subtraendo).
        nome_resultado: Nome do grafo resultante. Se None, usa "Diferença de {grafo1.nome} e {grafo2.nome}".
        
    Returns:
        Grafo: Grafo resultante da diferença.
    """
    # Define o nome do grafo resultante
    if nome_resultado is None:
        nome_resultado = f"Diferença de {grafo1.nome} e {grafo2.nome}"
    
    # Cria um novo grafo
    resultado = Grafo(nome_resultado)
    
    # Obtém os grafos NetworkX subjacentes
    g1_nx = grafo1.obter_grafo_networkx()
    g2_nx = grafo2.obter_grafo_networkx()
    
    # Cria um novo grafo com os mesmos vértices e atributos do grafo1
    g_diferenca = g1_nx.copy()
    
    # Remove as arestas que estão em g2_nx
    for u, v in g2_nx.edges():
        if g_diferenca.has_edge(u, v):
            g_diferenca.remove_edge(u, v)
    
    # Define o grafo resultante
    resultado.definir_grafo_networkx(g_diferenca)
    
    return resultado


def diferenca_simetrica_grafos(grafo1: Grafo, grafo2: Grafo, nome_resultado: str = None) -> Grafo:
    """
    Realiza a diferença simétrica entre dois grafos.
    
    A diferença simétrica entre dois grafos G1 = (V1, E1) e G2 = (V2, E2) é um grafo G = (V, E) onde:
    V = V1 ∪ V2 e E = (E1 ∪ E2) - (E1 ∩ E2)
    
    Args:
        grafo1: Primeiro grafo.
        grafo2: Segundo grafo.
        nome_resultado: Nome do grafo resultante. Se None, usa "Diferença simétrica de {grafo1.nome} e {grafo2.nome}".
        
    Returns:
        Grafo: Grafo resultante da diferença simétrica.
    """
    # Define o nome do grafo resultante
    if nome_resultado is None:
        nome_resultado = f"Diferença simétrica de {grafo1.nome} e {grafo2.nome}"
    
    # Cria um novo grafo
    resultado = Grafo(nome_resultado)
    
    # Obtém os grafos NetworkX subjacentes
    g1_nx = grafo1.obter_grafo_networkx()
    g2_nx = grafo2.obter_grafo_networkx()
    
    # Implementação personalizada da diferença simétrica
    # Primeiro, cria a união dos grafos
    g_uniao = nx.compose(g1_nx, g2_nx)
    
    # Depois, remove as arestas que estão em ambos os grafos
    g_dif_simetrica = g_uniao.copy()
    
    for u, v in g1_nx.edges():
        if g2_nx.has_edge(u, v):
            g_dif_simetrica.remove_edge(u, v)
    
    # Define o grafo resultante
    resultado.definir_grafo_networkx(g_dif_simetrica)
    
    return resultado


def composicao_grafos(grafo1: Grafo, grafo2: Grafo, nome_resultado: str = None) -> Grafo:
    """
    Realiza a composição de dois grafos.
    
    A composição de dois grafos G1 = (V1, E1) e G2 = (V2, E2) é um grafo G = (V, E) onde:
    V = V1 × V2 e E = {((u1, u2), (v1, v2)) | (u1, v1) ∈ E1 ou (u2, v2) ∈ E2}
    
    Args:
        grafo1: Primeiro grafo.
        grafo2: Segundo grafo.
        nome_resultado: Nome do grafo resultante. Se None, usa "Composição de {grafo1.nome} e {grafo2.nome}".
        
    Returns:
        Grafo: Grafo resultante da composição.
    """
    # Define o nome do grafo resultante
    if nome_resultado is None:
        nome_resultado = f"Composição de {grafo1.nome} e {grafo2.nome}"
    
    # Cria um novo grafo
    resultado = Grafo(nome_resultado)
    
    # Obtém os grafos NetworkX subjacentes
    g1_nx = grafo1.obter_grafo_networkx()
    g2_nx = grafo2.obter_grafo_networkx()
    
    # Realiza a composição dos grafos NetworkX
    g_composicao = nx.compose(g1_nx, g2_nx)
    
    # Define o grafo resultante
    resultado.definir_grafo_networkx(g_composicao)
    
    return resultado
