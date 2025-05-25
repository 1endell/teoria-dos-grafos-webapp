"""
Implementação de exportação de grafos para o formato CSV.

Este módulo contém funções para exportar grafos para o formato CSV,
representando a matriz de adjacência ou a lista de arestas do grafo.
"""

import networkx as nx
import csv
import os
from typing import Dict, List, Any, Optional, Literal
from grafo_backend.core.grafo import Grafo


def exportar_csv_matriz_adjacencia(grafo: Grafo, caminho: str) -> bool:
    """
    Exporta um grafo para o formato CSV como matriz de adjacência.
    
    Args:
        grafo: Grafo a ser exportado.
        caminho: Caminho do arquivo de saída.
        
    Returns:
        bool: True se a exportação foi bem-sucedida, False caso contrário.
    """
    try:
        # Obtém o grafo NetworkX subjacente
        g_nx = grafo.obter_grafo_networkx()
        
        # Obtém a lista de vértices
        vertices = list(g_nx.nodes())
        
        # Cria a matriz de adjacência
        matriz = []
        
        # Adiciona a linha de cabeçalho com os vértices
        cabecalho = [''] + [str(v) for v in vertices]
        matriz.append(cabecalho)
        
        # Para cada vértice, adiciona uma linha com os pesos das arestas
        for v1 in vertices:
            linha = [str(v1)]
            for v2 in vertices:
                if g_nx.has_edge(v1, v2):
                    peso = g_nx[v1][v2].get('weight', 1.0)
                    linha.append(str(peso))
                else:
                    linha.append('0')
            matriz.append(linha)
        
        # Exporta para CSV
        with open(caminho, 'w', newline='', encoding='utf-8') as arquivo:
            escritor = csv.writer(arquivo)
            for linha in matriz:
                escritor.writerow(linha)
        
        return True
    except Exception as e:
        print(f"Erro ao exportar grafo para CSV (matriz de adjacência): {e}")
        return False


def exportar_csv_lista_arestas(grafo: Grafo, caminho: str) -> bool:
    """
    Exporta um grafo para o formato CSV como lista de arestas.
    
    Args:
        grafo: Grafo a ser exportado.
        caminho: Caminho do arquivo de saída.
        
    Returns:
        bool: True se a exportação foi bem-sucedida, False caso contrário.
    """
    try:
        # Obtém o grafo NetworkX subjacente
        g_nx = grafo.obter_grafo_networkx()
        
        # Cria a lista de arestas
        arestas = []
        
        # Adiciona a linha de cabeçalho
        cabecalho = ['origem', 'destino', 'peso']
        arestas.append(cabecalho)
        
        # Para cada aresta, adiciona uma linha com origem, destino e peso
        for origem, destino, atributos in g_nx.edges(data=True):
            peso = atributos.get('weight', 1.0)
            arestas.append([str(origem), str(destino), str(peso)])
        
        # Exporta para CSV
        with open(caminho, 'w', newline='', encoding='utf-8') as arquivo:
            escritor = csv.writer(arquivo)
            for linha in arestas:
                escritor.writerow(linha)
        
        return True
    except Exception as e:
        print(f"Erro ao exportar grafo para CSV (lista de arestas): {e}")
        return False


def exportar_csv(grafo: Grafo, caminho: str, formato: Literal['matriz', 'lista'] = 'lista') -> bool:
    """
    Exporta um grafo para o formato CSV.
    
    Args:
        grafo: Grafo a ser exportado.
        caminho: Caminho do arquivo de saída.
        formato: Formato de exportação ('matriz' para matriz de adjacência, 'lista' para lista de arestas).
        
    Returns:
        bool: True se a exportação foi bem-sucedida, False caso contrário.
    """
    if formato == 'matriz':
        return exportar_csv_matriz_adjacencia(grafo, caminho)
    else:
        return exportar_csv_lista_arestas(grafo, caminho)
