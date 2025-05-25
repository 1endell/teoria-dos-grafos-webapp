"""
Implementação de importação de grafos a partir do formato CSV.

Este módulo contém funções para importar grafos a partir do formato CSV,
representando a matriz de adjacência ou a lista de arestas do grafo.
"""

import networkx as nx
import csv
import os
from typing import Dict, List, Any, Optional, Literal
from core.grafo import Grafo


def importar_csv_matriz_adjacencia(caminho: str, nome: str = None) -> Optional[Grafo]:
    """
    Importa um grafo a partir de um arquivo CSV contendo uma matriz de adjacência.
    
    Args:
        caminho: Caminho do arquivo de entrada.
        nome: Nome a ser atribuído ao grafo. Se None, usa o nome do arquivo sem extensão.
        
    Returns:
        Optional[Grafo]: Grafo importado ou None se a importação falhar.
    """
    try:
        # Define o nome do grafo
        if nome is None:
            nome = os.path.splitext(os.path.basename(caminho))[0]
        
        # Cria um novo grafo
        grafo = Grafo(nome)
        g_nx = nx.Graph()
        
        # Lê o arquivo CSV
        with open(caminho, 'r', newline='', encoding='utf-8') as arquivo:
            leitor = csv.reader(arquivo)
            linhas = list(leitor)
        
        if not linhas:
            raise ValueError("Arquivo CSV vazio")
        
        # Obtém os vértices da primeira linha (cabeçalho)
        vertices = [v for v in linhas[0][1:] if v]
        
        # Adiciona os vértices ao grafo
        for vertice in vertices:
            g_nx.add_node(vertice)
        
        # Para cada linha após o cabeçalho
        for i, linha in enumerate(linhas[1:], 1):
            if not linha:
                continue
                
            origem = linha[0]
            
            # Para cada coluna após a primeira
            for j, valor in enumerate(linha[1:], 1):
                if j <= len(vertices):
                    destino = vertices[j-1]
                    try:
                        peso = float(valor)
                        if peso > 0:  # Adiciona aresta apenas se o peso for positivo
                            g_nx.add_edge(origem, destino, weight=peso)
                    except ValueError:
                        # Ignora valores não numéricos
                        pass
        
        # Define o grafo NetworkX importado
        grafo.definir_grafo_networkx(g_nx)
        
        return grafo
    except Exception as e:
        print(f"Erro ao importar grafo de CSV (matriz de adjacência): {e}")
        return None


def importar_csv_lista_arestas(caminho: str, nome: str = None) -> Optional[Grafo]:
    """
    Importa um grafo a partir de um arquivo CSV contendo uma lista de arestas.
    
    Args:
        caminho: Caminho do arquivo de entrada.
        nome: Nome a ser atribuído ao grafo. Se None, usa o nome do arquivo sem extensão.
        
    Returns:
        Optional[Grafo]: Grafo importado ou None se a importação falhar.
    """
    try:
        # Define o nome do grafo
        if nome is None:
            nome = os.path.splitext(os.path.basename(caminho))[0]
        
        # Cria um novo grafo
        grafo = Grafo(nome)
        g_nx = nx.Graph()
        
        # Lê o arquivo CSV
        with open(caminho, 'r', newline='', encoding='utf-8') as arquivo:
            leitor = csv.reader(arquivo)
            linhas = list(leitor)
        
        if not linhas:
            raise ValueError("Arquivo CSV vazio")
        
        # Verifica se a primeira linha é um cabeçalho
        cabecalho = linhas[0]
        tem_cabecalho = cabecalho[0].lower() == 'origem' and cabecalho[1].lower() == 'destino'
        
        # Define o índice inicial para processar as linhas
        indice_inicial = 1 if tem_cabecalho else 0
        
        # Para cada linha após o cabeçalho (se houver)
        for linha in linhas[indice_inicial:]:
            if len(linha) < 2:
                continue
                
            origem = linha[0]
            destino = linha[1]
            
            # Adiciona os vértices se não existirem
            if origem not in g_nx:
                g_nx.add_node(origem)
            if destino not in g_nx:
                g_nx.add_node(destino)
            
            # Obtém o peso, se disponível
            peso = 1.0
            if len(linha) > 2:
                try:
                    peso = float(linha[2])
                except ValueError:
                    # Usa o peso padrão se não for possível converter
                    pass
            
            # Adiciona a aresta
            g_nx.add_edge(origem, destino, weight=peso)
        
        # Define o grafo NetworkX importado
        grafo.definir_grafo_networkx(g_nx)
        
        return grafo
    except Exception as e:
        print(f"Erro ao importar grafo de CSV (lista de arestas): {e}")
        return None


def importar_csv(caminho: str, nome: str = None, formato: Literal['matriz', 'lista'] = 'lista') -> Optional[Grafo]:
    """
    Importa um grafo a partir de um arquivo CSV.
    
    Args:
        caminho: Caminho do arquivo de entrada.
        nome: Nome a ser atribuído ao grafo. Se None, usa o nome do arquivo sem extensão.
        formato: Formato de importação ('matriz' para matriz de adjacência, 'lista' para lista de arestas).
        
    Returns:
        Optional[Grafo]: Grafo importado ou None se a importação falhar.
    """
    if formato == 'matriz':
        return importar_csv_matriz_adjacencia(caminho, nome)
    else:
        return importar_csv_lista_arestas(caminho, nome)
