"""
Script para validação dos novos algoritmos implementados.

Este script testa os algoritmos implementados para garantir que estão funcionando corretamente.
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from grafo_backend.core.grafo import Grafo

# Importa os algoritmos implementados
from algoritmos.caminhos.busca.busca import bfs, dfs, iddfs
from algoritmos.caminhos.bellman_ford import bellman_ford
from algoritmos.caminhos.floyd_warshall import floyd_warshall
from algoritmos.caminhos.tarjan import tarjan, encontrar_pontes, encontrar_pontos_articulacao as encontrar_articulacoes
from algoritmos.caminhos.a_star import a_star
from algoritmos.caminhos.dijkstra import dijkstra

from algoritmos.arvores.kruskal import kruskal, arvore_geradora_minima
from algoritmos.arvores.prim import prim

from algoritmos.fluxo.ford_fulkerson import ford_fulkerson
from algoritmos.fluxo.edmonds_karp import edmonds_karp
from algoritmos.fluxo.dinic import dinic, comparar_dinic_edmonds_karp

from algoritmos.emparelhamento.hopcroft_karp import hopcroft_karp
from algoritmos.emparelhamento.hungarian import hungarian_algorithm as hungarian

from algoritmos.ordenacao.kahn import kahn, verificar_ordenacao_topologica

from algoritmos.ciclos.hierholzer import hierholzer, verificar_grafo_euleriano
from algoritmos.ciclos.hamiltoniano import encontrar_ciclo_hamiltoniano_backtracking, verificar_ciclo_hamiltoniano

from algoritmos.cliques.bron_kerbosch import bron_kerbosch, encontrar_clique_maximo

from algoritmos.isomorfismo.ullmann import ullmann, verificar_isomorfismo_subgrafo

from algoritmos.planaridade.hopcroft_tarjan import hopcroft_tarjan, encontrar_embedding_planar

from algoritmos.comunidades.deteccao_comunidades import girvan_newman, louvain_method, calcular_modularidade

from algoritmos.tsp.christofides import christofides, algoritmo_genetico_tsp, comparar_algoritmos_tsp


def criar_grafo_teste():
    """Cria um grafo de teste para validação dos algoritmos."""
    grafo = Grafo("Grafo de Teste")
    
    # Adiciona vértices
    for i in range(1, 7):
        grafo.adicionar_vertice(i)
    
    # Adiciona arestas com pesos
    grafo.adicionar_aresta(1, 2, peso=2)
    grafo.adicionar_aresta(1, 3, peso=4)
    grafo.adicionar_aresta(2, 3, peso=1)
    grafo.adicionar_aresta(2, 4, peso=7)
    grafo.adicionar_aresta(3, 4, peso=3)
    grafo.adicionar_aresta(3, 5, peso=5)
    grafo.adicionar_aresta(4, 5, peso=2)
    grafo.adicionar_aresta(4, 6, peso=6)
    grafo.adicionar_aresta(5, 6, peso=1)
    
    return grafo


def criar_grafo_direcionado_teste():
    """Cria um grafo direcionado de teste para validação dos algoritmos."""
    grafo = Grafo("Grafo Direcionado de Teste", direcionado=True)
    
    # Adiciona vértices
    for i in range(1, 7):
        grafo.adicionar_vertice(i)
    
    # Adiciona arestas com pesos
    grafo.adicionar_aresta(1, 2, peso=2)
    grafo.adicionar_aresta(1, 3, peso=4)
    grafo.adicionar_aresta(2, 3, peso=1)
    grafo.adicionar_aresta(2, 4, peso=7)
    grafo.adicionar_aresta(3, 4, peso=3)
    grafo.adicionar_aresta(3, 5, peso=5)
    grafo.adicionar_aresta(4, 5, peso=2)
    grafo.adicionar_aresta(4, 6, peso=6)
    grafo.adicionar_aresta(5, 6, peso=1)
    
    return grafo


def criar_grafo_fluxo_teste():
    """Cria um grafo de teste para algoritmos de fluxo."""
    grafo = Grafo("Grafo de Fluxo", direcionado=True)
    
    # Adiciona vértices
    grafo.adicionar_vertice('s')  # fonte
    grafo.adicionar_vertice('t')  # sumidouro
    grafo.adicionar_vertice('a')
    grafo.adicionar_vertice('b')
    grafo.adicionar_vertice('c')
    grafo.adicionar_vertice('d')
    
    # Adiciona arestas com capacidades (pesos)
    grafo.adicionar_aresta('s', 'a', peso=10)
    grafo.adicionar_aresta('s', 'c', peso=8)
    grafo.adicionar_aresta('a', 'b', peso=6)
    grafo.adicionar_aresta('a', 'c', peso=5)
    grafo.adicionar_aresta('b', 't', peso=10)
    grafo.adicionar_aresta('c', 'd', peso=7)
    grafo.adicionar_aresta('d', 'b', peso=4)
    grafo.adicionar_aresta('d', 't', peso=10)
    
    return grafo


def criar_grafo_bipartido_teste():
    """Cria um grafo bipartido de teste para algoritmos de emparelhamento."""
    grafo = Grafo("Grafo Bipartido")
    
    # Adiciona vértices do conjunto U
    for i in range(1, 5):
        grafo.adicionar_vertice(f'u{i}')
    
    # Adiciona vértices do conjunto V
    for i in range(1, 5):
        grafo.adicionar_vertice(f'v{i}')
    
    # Adiciona arestas entre os conjuntos
    grafo.adicionar_aresta('u1', 'v1')
    grafo.adicionar_aresta('u1', 'v2')
    grafo.adicionar_aresta('u2', 'v1')
    grafo.adicionar_aresta('u2', 'v3')
    grafo.adicionar_aresta('u3', 'v2')
    grafo.adicionar_aresta('u3', 'v3')
    grafo.adicionar_aresta('u3', 'v4')
    grafo.adicionar_aresta('u4', 'v3')
    grafo.adicionar_aresta('u4', 'v4')
    
    return grafo


def criar_grafo_dag_teste():
    """Cria um grafo acíclico direcionado (DAG) de teste para ordenação topológica."""
    grafo = Grafo("Grafo DAG", direcionado=True)
    
    # Adiciona vértices
    for i in range(1, 7):
        grafo.adicionar_vertice(i)
    
    # Adiciona arestas (sem ciclos)
    grafo.adicionar_aresta(1, 2)
    grafo.adicionar_aresta(1, 3)
    grafo.adicionar_aresta(2, 4)
    grafo.adicionar_aresta(3, 4)
    grafo.adicionar_aresta(3, 5)
    grafo.adicionar_aresta(4, 6)
    grafo.adicionar_aresta(5, 6)
    
    return grafo


def criar_grafo_euleriano_teste():
    """Cria um grafo euleriano de teste."""
    grafo = Grafo("Grafo Euleriano")
    
    # Adiciona vértices
    for i in range(1, 7):
        grafo.adicionar_vertice(i)
    
    # Adiciona arestas (todos os vértices têm grau par)
    grafo.adicionar_aresta(1, 2)
    grafo.adicionar_aresta(1, 3)
    grafo.adicionar_aresta(2, 3)
    grafo.adicionar_aresta(2, 4)
    grafo.adicionar_aresta(3, 4)
    grafo.adicionar_aresta(3, 5)
    grafo.adicionar_aresta(4, 5)
    grafo.adicionar_aresta(4, 6)
    grafo.adicionar_aresta(5, 6)
    grafo.adicionar_aresta(5, 1)
    
    return grafo


def criar_grafo_hamiltoniano_teste():
    """Cria um grafo hamiltoniano de teste."""
    grafo = Grafo("Grafo Hamiltoniano")
    
    # Adiciona vértices
    for i in range(1, 6):
        grafo.adicionar_vertice(i)
    
    # Adiciona arestas (forma um ciclo hamiltoniano)
    grafo.adicionar_aresta(1, 2)
    grafo.adicionar_aresta(2, 3)
    grafo.adicionar_aresta(3, 4)
    grafo.adicionar_aresta(4, 5)
    grafo.adicionar_aresta(5, 1)
    
    # Adiciona algumas arestas extras
    grafo.adicionar_aresta(1, 3)
    grafo.adicionar_aresta(2, 4)
    
    return grafo


def criar_grafo_clique_teste():
    """Cria um grafo com múltiplos cliques para teste."""
    grafo = Grafo("Grafo com Cliques")
    
    # Adiciona vértices
    for i in range(1, 10):
        grafo.adicionar_vertice(i)
    
    # Clique 1: vértices 1, 2, 3, 4
    grafo.adicionar_aresta(1, 2)
    grafo.adicionar_aresta(1, 3)
    grafo.adicionar_aresta(1, 4)
    grafo.adicionar_aresta(2, 3)
    grafo.adicionar_aresta(2, 4)
    grafo.adicionar_aresta(3, 4)
    
    # Clique 2: vértices 5, 6, 7
    grafo.adicionar_aresta(5, 6)
    grafo.adicionar_aresta(5, 7)
    grafo.adicionar_aresta(6, 7)
    
    # Clique 3: vértices 8, 9
    grafo.adicionar_aresta(8, 9)
    
    # Algumas arestas entre cliques
    grafo.adicionar_aresta(4, 5)
    grafo.adicionar_aresta(7, 8)
    
    return grafo


def criar_grafo_isomorfismo_teste():
    """Cria dois grafos para teste de isomorfismo de subgrafos."""
    # Grafo pequeno (padrão)
    grafo_pequeno = Grafo("Grafo Padrão")
    for i in range(1, 4):
        grafo_pequeno.adicionar_vertice(i)
    
    grafo_pequeno.adicionar_aresta(1, 2)
    grafo_pequeno.adicionar_aresta(2, 3)
    grafo_pequeno.adicionar_aresta(3, 1)
    
    # Grafo grande (alvo)
    grafo_grande = Grafo("Grafo Alvo")
    for i in range(1, 7):
        grafo_grande.adicionar_vertice(i)
    
    grafo_grande.adicionar_aresta(1, 2)
    grafo_grande.adicionar_aresta(2, 3)
    grafo_grande.adicionar_aresta(3, 1)
    grafo_grande.adicionar_aresta(3, 4)
    grafo_grande.adicionar_aresta(4, 5)
    grafo_grande.adicionar_aresta(5, 6)
    grafo_grande.adicionar_aresta(6, 4)
    
    return grafo_pequeno, grafo_grande


def criar_grafo_planar_teste():
    """Cria um grafo planar de teste."""
    grafo = Grafo("Grafo Planar")
    
    # Adiciona vértices
    for i in range(1, 7):
        grafo.adicionar_vertice(i)
    
    # Adiciona arestas (forma um grafo planar)
    grafo.adicionar_aresta(1, 2)
    grafo.adicionar_aresta(1, 3)
    grafo.adicionar_aresta(2, 3)
    grafo.adicionar_aresta(2, 4)
    grafo.adicionar_aresta(3, 5)
    grafo.adicionar_aresta(4, 5)
    grafo.adicionar_aresta(4, 6)
    grafo.adicionar_aresta(5, 6)
    
    return grafo


def criar_grafo_nao_planar_teste():
    """Cria um grafo não planar de teste (K5)."""
    grafo = Grafo("Grafo Não Planar (K5)")
    
    # Adiciona vértices
    for i in range(1, 6):
        grafo.adicionar_vertice(i)
    
    # Adiciona arestas (forma um K5, que não é planar)
    for i in range(1, 6):
        for j in range(i+1, 6):
            grafo.adicionar_aresta(i, j)
    
    return grafo


def criar_grafo_comunidades_teste():
    """Cria um grafo com comunidades para teste."""
    grafo = Grafo("Grafo com Comunidades")
    
    # Adiciona vértices
    for i in range(1, 13):
        grafo.adicionar_vertice(i)
    
    # Comunidade 1: vértices 1-4
    grafo.adicionar_aresta(1, 2)
    grafo.adicionar_aresta(1, 3)
    grafo.adicionar_aresta(1, 4)
    grafo.adicionar_aresta(2, 3)
    grafo.adicionar_aresta(3, 4)
    
    # Comunidade 2: vértices 5-8
    grafo.adicionar_aresta(5, 6)
    grafo.adicionar_aresta(5, 7)
    grafo.adicionar_aresta(5, 8)
    grafo.adicionar_aresta(6, 7)
    grafo.adicionar_aresta(7, 8)
    
    # Comunidade 3: vértices 9-12
    grafo.adicionar_aresta(9, 10)
    grafo.adicionar_aresta(9, 11)
    grafo.adicionar_aresta(9, 12)
    grafo.adicionar_aresta(10, 11)
    grafo.adicionar_aresta(11, 12)
    
    # Arestas entre comunidades (poucas)
    grafo.adicionar_aresta(4, 5)
    grafo.adicionar_aresta(8, 9)
    
    return grafo


def criar_grafo_tsp_teste():
    """Cria um grafo completo para teste do problema do caixeiro viajante."""
    grafo = Grafo("Grafo TSP")
    
    # Adiciona vértices
    for i in range(1, 6):
        grafo.adicionar_vertice(i)
    
    # Adiciona arestas com pesos (grafo completo)
    grafo.adicionar_aresta(1, 2, peso=10)
    grafo.adicionar_aresta(1, 3, peso=15)
    grafo.adicionar_aresta(1, 4, peso=20)
    grafo.adicionar_aresta(1, 5, peso=25)
    grafo.adicionar_aresta(2, 3, peso=35)
    grafo.adicionar_aresta(2, 4, peso=30)
    grafo.adicionar_aresta(2, 5, peso=15)
    grafo.adicionar_aresta(3, 4, peso=25)
    grafo.adicionar_aresta(3, 5, peso=20)
    grafo.adicionar_aresta(4, 5, peso=10)
    
    return grafo


def testar_algoritmos_busca():
    """Testa os algoritmos de busca."""
    print("\n=== Testando Algoritmos de Busca ===")
    grafo = criar_grafo_teste()
    
    # Testa BFS
    print("\nBFS a partir do vértice 1:")
    resultado_bfs = bfs(grafo, 1)
    print(f"Ordem de visita: {resultado_bfs}")
    
    # Testa DFS
    print("\nDFS a partir do vértice 1:")
    resultado_dfs = dfs(grafo, 1)
    print(f"Ordem de visita: {resultado_dfs}")
    
    # Testa IDDFS
    print("\nIDDFS a partir do vértice 1 (profundidade máxima 3):")
    resultado_iddfs = iddfs(grafo, 1, 3)
    print(f"Ordem de visita: {resultado_iddfs}")


def testar_algoritmos_caminhos_minimos():
    """Testa os algoritmos de caminhos mínimos."""
    print("\n=== Testando Algoritmos de Caminhos Mínimos ===")
    grafo = criar_grafo_teste()
    
    # Testa Dijkstra
    print("\nDijkstra a partir do vértice 1:")
    distancias, predecessores = dijkstra(grafo, 1)
    print(f"Distâncias: {distancias}")
    print(f"Predecessores: {predecessores}")
    
    # Testa Bellman-Ford
    print("\nBellman-Ford a partir do vértice 1:")
    distancias, predecessores, ciclo_negativo = bellman_ford(grafo, 1)
    print(f"Distâncias: {distancias}")
    print(f"Predecessores: {predecessores}")
    print(f"Ciclo negativo detectado: {ciclo_negativo}")
    
    # Testa Floyd-Warshall
    print("\nFloyd-Warshall:")
    distancias = floyd_warshall(grafo)
    print(f"Matriz de distâncias: {distancias}")
    
    # Testa A*
    print("\nA* do vértice 1 ao vértice 6:")
    caminho, custo = a_star(grafo, 1, 6)
    print(f"Caminho: {caminho}")
    print(f"Custo: {custo}")


def testar_algoritmos_componentes():
    """Testa os algoritmos de componentes conexos."""
    print("\n=== Testando Algoritmos de Componentes Conexos ===")
    grafo = criar_grafo_teste()
    grafo_dir = criar_grafo_direcionado_teste()
    
    # Testa Tarjan para componentes fortemente conexos (requer grafo direcionado)
    print("\nComponentes fortemente conexos (Tarjan):")
    componentes = tarjan(grafo_dir)
    print(f"Componentes: {componentes}")
    
    # Testa algoritmo para encontrar pontes (requer grafo não direcionado)
    print("\nPontes no grafo:")
    pontes = encontrar_pontes(grafo)
    print(f"Pontes: {pontes}")
    
    # Testa algoritmo para encontrar articulações (requer grafo não direcionado)
    print("\nArticulações no grafo:")
    articulacoes = encontrar_articulacoes(grafo)
    print(f"Articulações: {articulacoes}")


def testar_algoritmos_arvores():
    """Testa os algoritmos de árvores geradoras mínimas."""
    print("\n=== Testando Algoritmos de Árvores Geradoras Mínimas ===")
    grafo = criar_grafo_teste()
    
    # Testa Kruskal
    print("\nÁrvore geradora mínima (Kruskal):")
    arestas, custo = arvore_geradora_minima(grafo)
    print(f"Arestas: {arestas}")
    print(f"Custo total: {custo}")
    
    # Testa Prim
    print("\nÁrvore geradora mínima (Prim):")
    arestas, custo = prim(grafo)
    print(f"Arestas: {arestas}")
    print(f"Custo total: {custo}")


def testar_algoritmos_fluxo():
    """Testa os algoritmos de fluxo máximo."""
    print("\n=== Testando Algoritmos de Fluxo Máximo ===")
    grafo = criar_grafo_fluxo_teste()
    
    # Testa Ford-Fulkerson
    print("\nFluxo máximo (Ford-Fulkerson) de 's' para 't':")
    fluxos, fluxo_maximo = ford_fulkerson(grafo, 's', 't')
    print(f"Fluxos nas arestas: {fluxos}")
    print(f"Fluxo máximo: {fluxo_maximo}")
    
    # Testa Edmonds-Karp
    print("\nFluxo máximo (Edmonds-Karp) de 's' para 't':")
    fluxos, fluxo_maximo = edmonds_karp(grafo, 's', 't')
    print(f"Fluxos nas arestas: {fluxos}")
    print(f"Fluxo máximo: {fluxo_maximo}")
    
    # Testa Dinic
    print("\nFluxo máximo (Dinic) de 's' para 't':")
    fluxos, fluxo_maximo = dinic(grafo, 's', 't')
    print(f"Fluxos nas arestas: {fluxos}")
    print(f"Fluxo máximo: {fluxo_maximo}")
    
    # Compara os algoritmos
    print("\nComparação entre Dinic e Edmonds-Karp:")
    comparacao = comparar_dinic_edmonds_karp(grafo, 's', 't')
    print(f"Resultados: {comparacao}")


def testar_algoritmos_emparelhamento():
    """Testa os algoritmos de emparelhamento."""
    print("\n=== Testando Algoritmos de Emparelhamento ===")
    grafo = criar_grafo_bipartido_teste()
    
    # Testa Hopcroft-Karp
    print("\nEmparelhamento máximo (Hopcroft-Karp):")
    emparelhamento = hopcroft_karp(grafo)
    print(f"Emparelhamento: {emparelhamento}")
    print(f"Tamanho do emparelhamento: {len(emparelhamento)}")
    
    # Cria uma matriz de custo para o algoritmo húngaro
    print("\nAtribuição ótima (Hungarian Algorithm):")
    matriz_custo = np.array([
        [10, 20, 30, 40],
        [15, 25, 35, 45],
        [20, 30, 40, 50],
        [25, 35, 45, 55]
    ])
    atribuicao, custo_total = hungarian(matriz_custo)
    print(f"Atribuição: {atribuicao}")
    print(f"Custo total: {custo_total}")


def testar_algoritmos_ordenacao():
    """Testa os algoritmos de ordenação topológica."""
    print("\n=== Testando Algoritmos de Ordenação Topológica ===")
    grafo = criar_grafo_dag_teste()
    
    # Testa Kahn
    print("\nOrdenação topológica (Kahn):")
    ordenacao = kahn(grafo)
    print(f"Ordenação: {ordenacao}")
    
    # Verifica se a ordenação é válida
    print("\nVerificação da ordenação:")
    valida = verificar_ordenacao_topologica(grafo, ordenacao)
    print(f"Ordenação válida: {valida}")


def testar_algoritmos_ciclos():
    """Testa os algoritmos de ciclos eulerianos e hamiltonianos."""
    print("\n=== Testando Algoritmos de Ciclos ===")
    
    # Testa Hierholzer para ciclos eulerianos
    grafo_euleriano = criar_grafo_euleriano_teste()
    print("\nVerificação de grafo euleriano:")
    eh_euleriano = verificar_grafo_euleriano(grafo_euleriano)
    print(f"É euleriano: {eh_euleriano}")
    
    print("\nCiclo euleriano (Hierholzer):")
    ciclo = hierholzer(grafo_euleriano)
    print(f"Ciclo: {ciclo}")
    
    # Testa algoritmos para ciclos hamiltonianos
    grafo_hamiltoniano = criar_grafo_hamiltoniano_teste()
    print("\nCiclo hamiltoniano (Backtracking):")
    ciclo = encontrar_ciclo_hamiltoniano_backtracking(grafo_hamiltoniano)
    print(f"Ciclo: {ciclo}")
    
    print("\nVerificação de ciclo hamiltoniano:")
    valido = verificar_ciclo_hamiltoniano(grafo_hamiltoniano, ciclo)
    print(f"Ciclo válido: {valido}")


def testar_algoritmos_cliques():
    """Testa os algoritmos de cliques."""
    print("\n=== Testando Algoritmos de Cliques ===")
    grafo = criar_grafo_clique_teste()
    
    # Testa Bron-Kerbosch
    print("\nCliques maximais (Bron-Kerbosch):")
    cliques = bron_kerbosch(grafo)
    print(f"Cliques: {cliques}")
    
    # Testa algoritmo para encontrar o clique máximo
    print("\nClique máximo:")
    clique_maximo, tamanho = encontrar_clique_maximo(grafo)
    print(f"Clique máximo: {clique_maximo}")
    print(f"Tamanho: {tamanho}")


def testar_algoritmos_isomorfismo():
    """Testa os algoritmos de isomorfismo de subgrafos."""
    print("\n=== Testando Algoritmos de Isomorfismo ===")
    grafo_pequeno, grafo_grande = criar_grafo_isomorfismo_teste()
    
    # Testa Ullmann
    print("\nIsomorfismo de subgrafos (Ullmann):")
    mapeamento = ullmann(grafo_pequeno, grafo_grande)
    print(f"Mapeamento: {mapeamento}")
    
    # Verifica se o mapeamento é válido
    print("\nVerificação do isomorfismo:")
    valido = verificar_isomorfismo_subgrafo(grafo_pequeno, grafo_grande, mapeamento)
    print(f"Isomorfismo válido: {valido}")


def testar_algoritmos_planaridade():
    """Testa os algoritmos de planaridade."""
    print("\n=== Testando Algoritmos de Planaridade ===")
    grafo_planar = criar_grafo_planar_teste()
    grafo_nao_planar = criar_grafo_nao_planar_teste()
    
    # Testa Hopcroft-Tarjan para grafo planar
    print("\nVerificação de grafo planar:")
    eh_planar = hopcroft_tarjan(grafo_planar)
    print(f"É planar: {eh_planar}")
    
    # Testa Hopcroft-Tarjan para grafo não planar
    print("\nVerificação de grafo não planar (K5):")
    eh_planar = hopcroft_tarjan(grafo_nao_planar)
    print(f"É planar: {eh_planar}")
    
    # Testa algoritmo para encontrar um embedding planar
    print("\nEmbedding planar:")
    embedding = encontrar_embedding_planar(grafo_planar)
    print(f"Embedding: {embedding}")


def testar_algoritmos_comunidades():
    """Testa os algoritmos de detecção de comunidades."""
    print("\n=== Testando Algoritmos de Detecção de Comunidades ===")
    grafo = criar_grafo_comunidades_teste()
    
    # Testa Girvan-Newman
    print("\nDetecção de comunidades (Girvan-Newman):")
    comunidades = girvan_newman(grafo, num_comunidades=3)
    print(f"Comunidades: {comunidades}")
    
    # Testa Louvain Method
    print("\nDetecção de comunidades (Louvain Method):")
    comunidades = louvain_method(grafo)
    print(f"Comunidades: {comunidades}")
    
    # Calcula a modularidade
    print("\nModularidade das comunidades:")
    modularidade = calcular_modularidade(grafo, comunidades)
    print(f"Modularidade: {modularidade}")


def testar_algoritmos_tsp():
    """Testa os algoritmos para o problema do caixeiro viajante."""
    print("\n=== Testando Algoritmos para o Problema do Caixeiro Viajante ===")
    grafo = criar_grafo_tsp_teste()
    
    # Testa Christofides
    print("\nAproximação do TSP (Christofides):")
    ciclo, custo = christofides(grafo)
    print(f"Ciclo: {ciclo}")
    print(f"Custo: {custo}")
    
    # Testa Algoritmo Genético
    print("\nAproximação do TSP (Algoritmo Genético):")
    ciclo, custo = algoritmo_genetico_tsp(grafo, tamanho_populacao=20, num_geracoes=100)
    print(f"Ciclo: {ciclo}")
    print(f"Custo: {custo}")
    
    # Compara os algoritmos
    print("\nComparação entre algoritmos para o TSP:")
    comparacao = comparar_algoritmos_tsp(grafo)
    print(f"Resultados: {comparacao}")


def main():
    """Função principal para testar todos os algoritmos."""
    print("=== Validação dos Novos Algoritmos Implementados ===")
    
    # Testa os algoritmos de busca
    testar_algoritmos_busca()
    
    # Testa os algoritmos de caminhos mínimos
    testar_algoritmos_caminhos_minimos()
    
    # Testa os algoritmos de componentes conexos
    testar_algoritmos_componentes()
    
    # Testa os algoritmos de árvores geradoras mínimas
    testar_algoritmos_arvores()
    
    # Testa os algoritmos de fluxo máximo
    testar_algoritmos_fluxo()
    
    # Testa os algoritmos de emparelhamento
    testar_algoritmos_emparelhamento()
    
    # Testa os algoritmos de ordenação topológica
    testar_algoritmos_ordenacao()
    
    # Testa os algoritmos de ciclos
    testar_algoritmos_ciclos()
    
    # Testa os algoritmos de cliques
    testar_algoritmos_cliques()
    
    # Testa os algoritmos de isomorfismo
    testar_algoritmos_isomorfismo()
    
    # Testa os algoritmos de planaridade
    testar_algoritmos_planaridade()
    
    # Testa os algoritmos de detecção de comunidades
    testar_algoritmos_comunidades()
    
    # Testa os algoritmos para o problema do caixeiro viajante
    testar_algoritmos_tsp()
    
    print("\n=== Validação Concluída com Sucesso! ===")


if __name__ == "__main__":
    main()
