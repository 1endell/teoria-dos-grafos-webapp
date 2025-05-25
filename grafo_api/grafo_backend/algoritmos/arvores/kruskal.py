"""
Implementação do algoritmo de Kruskal para encontrar árvores geradoras mínimas em grafos ponderados.

O algoritmo de Kruskal encontra uma árvore geradora mínima para um grafo conexo ponderado,
selecionando arestas em ordem crescente de peso e adicionando-as à árvore se não formarem ciclos.
"""

from typing import Dict, List, Any, Optional, Tuple, Set
import networkx as nx
from core.grafo import Grafo


class UnionFind:
    """
    Implementação da estrutura de dados Union-Find para o algoritmo de Kruskal.
    """
    
    def __init__(self, elementos):
        """
        Inicializa a estrutura Union-Find.
        
        Args:
            elementos: Conjunto de elementos.
        """
        self.pai = {elemento: elemento for elemento in elementos}
        self.rank = {elemento: 0 for elemento in elementos}
    
    def encontrar(self, elemento):
        """
        Encontra o representante do conjunto que contém o elemento.
        
        Args:
            elemento: Elemento a ser buscado.
            
        Returns:
            O representante do conjunto.
        """
        if self.pai[elemento] != elemento:
            self.pai[elemento] = self.encontrar(self.pai[elemento])
        return self.pai[elemento]
    
    def unir(self, elemento1, elemento2):
        """
        Une os conjuntos que contêm os elementos.
        
        Args:
            elemento1: Primeiro elemento.
            elemento2: Segundo elemento.
        """
        raiz1 = self.encontrar(elemento1)
        raiz2 = self.encontrar(elemento2)
        
        if raiz1 == raiz2:
            return
        
        if self.rank[raiz1] < self.rank[raiz2]:
            self.pai[raiz1] = raiz2
        else:
            self.pai[raiz2] = raiz1
            if self.rank[raiz1] == self.rank[raiz2]:
                self.rank[raiz1] += 1


def kruskal(grafo: Grafo) -> List[Tuple[Any, Any, float]]:
    """
    Implementa o algoritmo de Kruskal para encontrar uma árvore geradora mínima.
    
    Args:
        grafo: Grafo ponderado.
        
    Returns:
        List[Tuple[Any, Any, float]]: Lista de arestas (origem, destino, peso) que formam a árvore geradora mínima.
        
    Raises:
        ValueError: Se o grafo não for conexo.
    """
    # Verifica se o grafo é conexo
    if not grafo.eh_conexo():
        raise ValueError("O algoritmo de Kruskal requer um grafo conexo.")
    
    # Obtém todas as arestas do grafo
    arestas = []
    for origem, destino, atributos in grafo.obter_arestas():
        peso = atributos.get('weight', 1.0)
        arestas.append((origem, destino, peso))
    
    # Ordena as arestas por peso
    arestas.sort(key=lambda x: x[2])
    
    # Inicializa a estrutura Union-Find
    union_find = UnionFind(grafo.obter_vertices())
    
    # Inicializa a árvore geradora mínima
    arvore_geradora = []
    
    # Para cada aresta em ordem crescente de peso
    for origem, destino, peso in arestas:
        # Se a adição da aresta não forma ciclo
        if union_find.encontrar(origem) != union_find.encontrar(destino):
            # Adiciona a aresta à árvore geradora
            arvore_geradora.append((origem, destino, peso))
            # Une os conjuntos
            union_find.unir(origem, destino)
    
    return arvore_geradora


def arvore_geradora_minima(grafo: Grafo) -> Tuple[List[Tuple[Any, Any, float]], float]:
    """
    Encontra uma árvore geradora mínima usando o algoritmo de Kruskal.
    
    Args:
        grafo: Grafo ponderado.
        
    Returns:
        Tuple[List[Tuple[Any, Any, float]], float]: Tupla contendo:
            - Lista de arestas (origem, destino, peso) que formam a árvore geradora mínima
            - Peso total da árvore geradora mínima
            
    Raises:
        ValueError: Se o grafo não for conexo.
    """
    # Executa o algoritmo de Kruskal
    arvore = kruskal(grafo)
    
    # Calcula o peso total da árvore geradora
    peso_total = sum(peso for _, _, peso in arvore)
    
    return arvore, peso_total


def criar_subgrafo_arvore_geradora(grafo: Grafo, arestas_arvore: List[Tuple[Any, Any, float]]) -> Grafo:
    """
    Cria um subgrafo contendo apenas as arestas da árvore geradora mínima.
    
    Args:
        grafo: Grafo original.
        arestas_arvore: Lista de arestas (origem, destino, peso) da árvore geradora mínima.
        
    Returns:
        Grafo: Subgrafo contendo apenas as arestas da árvore geradora mínima.
    """
    # Cria um novo grafo com os mesmos vértices
    subgrafo = Grafo(f"Árvore Geradora Mínima de {grafo.nome}")
    
    # Adiciona todos os vértices do grafo original
    for vertice in grafo.obter_vertices():
        atributos = grafo.obter_atributos_vertice(vertice)
        subgrafo.adicionar_vertice(vertice, atributos)
    
    # Adiciona apenas as arestas da árvore geradora
    for origem, destino, peso in arestas_arvore:
        atributos = grafo.obter_atributos_aresta(origem, destino).copy()
        atributos['weight'] = peso
        subgrafo.adicionar_aresta(origem, destino, peso, atributos)
    
    return subgrafo
