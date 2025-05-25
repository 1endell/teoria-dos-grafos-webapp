"""
Implementação de algoritmos de emparelhamento em grafos gerais.

Este módulo contém implementações de algoritmos para encontrar emparelhamentos
máximos em grafos gerais, incluindo o algoritmo de Edmonds (Blossom).
"""

import networkx as nx
from typing import Dict, List, Any, Set, Tuple, Optional
from grafo_backend.core.grafo import Grafo


def emparelhamento_maximo_geral(grafo: Grafo) -> Dict[Any, Any]:
    """
    Encontra um emparelhamento máximo em um grafo geral usando o algoritmo de Edmonds (Blossom).
    
    Um emparelhamento é um conjunto de arestas sem vértices em comum.
    Um emparelhamento máximo é um emparelhamento com o maior número possível de arestas.
    
    Args:
        grafo: Grafo a ser analisado.
        
    Returns:
        Dict[Any, Any]: Dicionário mapeando vértices para seus pares no emparelhamento.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Usa a implementação do NetworkX para encontrar o emparelhamento máximo
    emparelhamento = nx.algorithms.matching.max_weight_matching(g_nx, maxcardinality=True)
    
    # Converte o resultado para um dicionário
    resultado = {}
    for u, v in emparelhamento:
        resultado[u] = v
        resultado[v] = u
    
    return resultado


def emparelhamento_maximo_ponderado(grafo: Grafo) -> Dict[Any, Any]:
    """
    Encontra um emparelhamento máximo ponderado em um grafo.
    
    Um emparelhamento máximo ponderado é um emparelhamento cuja soma dos pesos
    das arestas é máxima.
    
    Args:
        grafo: Grafo ponderado a ser analisado.
        
    Returns:
        Dict[Any, Any]: Dicionário mapeando vértices para seus pares no emparelhamento.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Usa a implementação do NetworkX para encontrar o emparelhamento máximo ponderado
    emparelhamento = nx.algorithms.matching.max_weight_matching(g_nx)
    
    # Converte o resultado para um dicionário
    resultado = {}
    for u, v in emparelhamento:
        resultado[u] = v
        resultado[v] = u
    
    return resultado


def emparelhamento_perfeito_existe(grafo: Grafo) -> bool:
    """
    Verifica se existe um emparelhamento perfeito no grafo.
    
    Um emparelhamento perfeito é um emparelhamento que cobre todos os vértices do grafo.
    
    Args:
        grafo: Grafo a ser analisado.
        
    Returns:
        bool: True se existe um emparelhamento perfeito, False caso contrário.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Um emparelhamento perfeito só pode existir se o número de vértices for par
    if len(g_nx.nodes()) % 2 != 0:
        return False
    
    # Encontra um emparelhamento máximo
    emparelhamento = nx.algorithms.matching.max_weight_matching(g_nx, maxcardinality=True)
    
    # Verifica se o emparelhamento cobre todos os vértices
    return len(emparelhamento) * 2 == len(g_nx.nodes())


def encontrar_emparelhamento_perfeito(grafo: Grafo) -> Optional[Dict[Any, Any]]:
    """
    Encontra um emparelhamento perfeito no grafo, se existir.
    
    Args:
        grafo: Grafo a ser analisado.
        
    Returns:
        Optional[Dict[Any, Any]]: Dicionário mapeando vértices para seus pares no emparelhamento,
                                ou None se não existir um emparelhamento perfeito.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Um emparelhamento perfeito só pode existir se o número de vértices for par
    if len(g_nx.nodes()) % 2 != 0:
        return None
    
    # Encontra um emparelhamento máximo
    emparelhamento = nx.algorithms.matching.max_weight_matching(g_nx, maxcardinality=True)
    
    # Verifica se o emparelhamento cobre todos os vértices
    if len(emparelhamento) * 2 != len(g_nx.nodes()):
        return None
    
    # Converte o resultado para um dicionário
    resultado = {}
    for u, v in emparelhamento:
        resultado[u] = v
        resultado[v] = u
    
    return resultado


def calcular_cardinalidade_emparelhamento(emparelhamento: Dict[Any, Any]) -> int:
    """
    Calcula a cardinalidade de um emparelhamento.
    
    A cardinalidade é o número de arestas no emparelhamento.
    
    Args:
        emparelhamento: Dicionário mapeando vértices para seus pares.
        
    Returns:
        int: Número de arestas no emparelhamento.
    """
    # Cada aresta é contada duas vezes no dicionário (uma para cada extremidade)
    return len(emparelhamento) // 2


def verificar_emparelhamento_valido(grafo: Grafo, emparelhamento: Dict[Any, Any]) -> bool:
    """
    Verifica se um emparelhamento é válido para o grafo.
    
    Um emparelhamento é válido se:
    1. Cada vértice está emparelhado com no máximo um outro vértice
    2. Os vértices emparelhados são adjacentes no grafo
    
    Args:
        grafo: Grafo a ser analisado.
        emparelhamento: Dicionário mapeando vértices para seus pares.
        
    Returns:
        bool: True se o emparelhamento é válido, False caso contrário.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Verifica se cada par de vértices emparelhados é adjacente no grafo
    for u, v in emparelhamento.items():
        if not g_nx.has_edge(u, v):
            return False
    
    # Verifica se cada vértice está emparelhado com no máximo um outro vértice
    visitados = set()
    for u, v in emparelhamento.items():
        if u in visitados or v in visitados:
            return False
        visitados.add(u)
        visitados.add(v)
    
    return True


def encontrar_caminho_aumentante(grafo: Grafo, emparelhamento: Dict[Any, Any]) -> Optional[List[Any]]:
    """
    Encontra um caminho aumentante no grafo em relação ao emparelhamento.
    
    Um caminho aumentante é um caminho que alterna entre arestas não emparelhadas e emparelhadas,
    começando e terminando em vértices não emparelhados.
    
    Args:
        grafo: Grafo a ser analisado.
        emparelhamento: Dicionário mapeando vértices para seus pares.
        
    Returns:
        Optional[List[Any]]: Lista de vértices formando um caminho aumentante,
                           ou None se não existir um caminho aumentante.
    """
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Encontra vértices não emparelhados
    nao_emparelhados = set(g_nx.nodes()) - set(emparelhamento.keys())
    
    # Se não houver vértices não emparelhados, não há caminho aumentante
    if not nao_emparelhados:
        return None
    
    # Para cada vértice não emparelhado, tenta encontrar um caminho aumentante
    for inicio in nao_emparelhados:
        # Usa BFS para encontrar um caminho aumentante
        visitados = {inicio}
        fila = [(inicio, [])]
        
        while fila:
            vertice, caminho = fila.pop(0)
            caminho_atual = caminho + [vertice]
            
            # Para cada vizinho
            for vizinho in g_nx.neighbors(vertice):
                if vizinho in visitados:
                    continue
                
                # Se o vizinho não está emparelhado e não é o vértice inicial,
                # encontramos um caminho aumentante
                if vizinho not in emparelhamento and vizinho != inicio:
                    return caminho_atual + [vizinho]
                
                # Se o vizinho está emparelhado, adiciona o par do vizinho à fila
                if vizinho in emparelhamento:
                    par = emparelhamento[vizinho]
                    if par not in visitados:
                        visitados.add(vizinho)
                        visitados.add(par)
                        fila.append((par, caminho_atual + [vizinho]))
    
    # Se não encontrou um caminho aumentante
    return None


def aumentar_emparelhamento(emparelhamento: Dict[Any, Any], caminho: List[Any]) -> Dict[Any, Any]:
    """
    Aumenta um emparelhamento usando um caminho aumentante.
    
    Args:
        emparelhamento: Dicionário mapeando vértices para seus pares.
        caminho: Lista de vértices formando um caminho aumentante.
        
    Returns:
        Dict[Any, Any]: Novo emparelhamento aumentado.
    """
    # Cria uma cópia do emparelhamento
    novo_emparelhamento = emparelhamento.copy()
    
    # Percorre o caminho em pares
    for i in range(0, len(caminho) - 1, 2):
        u, v = caminho[i], caminho[i + 1]
        
        # Remove emparelhamentos existentes
        if u in novo_emparelhamento:
            del novo_emparelhamento[novo_emparelhamento[u]]
            del novo_emparelhamento[u]
        
        if v in novo_emparelhamento:
            del novo_emparelhamento[novo_emparelhamento[v]]
            del novo_emparelhamento[v]
        
        # Adiciona o novo emparelhamento
        novo_emparelhamento[u] = v
        novo_emparelhamento[v] = u
    
    return novo_emparelhamento
