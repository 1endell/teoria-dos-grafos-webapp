"""
Implementação do algoritmo de Christofides para o problema do caixeiro viajante.

O algoritmo de Christofides é uma heurística para o problema do caixeiro viajante
que garante uma solução com custo no máximo 1.5 vezes o custo ótimo para grafos
com pesos que satisfazem a desigualdade triangular.
"""

from typing import Dict, List, Any, Tuple, Set, Optional
import networkx as nx
import numpy as np
from core.grafo import Grafo


def christofides(grafo: Grafo) -> Tuple[List[Any], float]:
    """
    Implementa o algoritmo de Christofides para o problema do caixeiro viajante.
    
    Args:
        grafo: Grafo completo não direcionado com pesos nas arestas.
        
    Returns:
        Tuple[List[Any], float]: Tupla contendo:
            - Lista de vértices que formam um ciclo hamiltoniano aproximado
            - Custo total do ciclo
            
    Raises:
        ValueError: Se o grafo for direcionado.
        ValueError: Se o grafo não for completo.
    """
    # Verifica se o grafo é direcionado
    if grafo.eh_direcionado():
        raise ValueError("O algoritmo de Christofides só é aplicável a grafos não direcionados.")
    
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Verifica se o grafo é completo
    n = len(grafo.obter_vertices())
    if g_nx.number_of_edges() < (n * (n - 1)) // 2:
        raise ValueError("O algoritmo de Christofides só é aplicável a grafos completos.")
    
    # 1. Encontra uma árvore geradora mínima (MST)
    mst = nx.minimum_spanning_tree(g_nx, weight='weight')
    
    # 2. Encontra os vértices de grau ímpar na MST
    vertices_impares = [v for v, d in mst.degree() if d % 2 == 1]
    
    # 3. Encontra um emparelhamento perfeito de custo mínimo entre os vértices de grau ímpar
    # Cria um subgrafo completo induzido pelos vértices de grau ímpar
    subgrafo = nx.Graph()
    for i, u in enumerate(vertices_impares):
        for j, v in enumerate(vertices_impares):
            if i < j:  # Evita adicionar arestas duplicadas
                # Usa o peso negativo para encontrar o emparelhamento de custo máximo
                # (que é equivalente ao emparelhamento de custo mínimo no grafo original)
                subgrafo.add_edge(u, v, weight=-g_nx[u][v]['weight'])
    
    # Encontra o emparelhamento perfeito de custo máximo
    emparelhamento = nx.algorithms.matching.max_weight_matching(subgrafo, maxcardinality=True)
    
    # 4. Combina a MST com o emparelhamento para formar um multigrafo euleriano
    multigrafo = nx.MultiGraph(mst)
    for u, v in emparelhamento:
        multigrafo.add_edge(u, v, weight=g_nx[u][v]['weight'])
    
    # 5. Encontra um ciclo euleriano no multigrafo
    ciclo_euleriano = list(nx.eulerian_circuit(multigrafo))
    
    # 6. Converte o ciclo euleriano em um ciclo hamiltoniano usando atalhos
    ciclo_hamiltoniano = []
    visitados = set()
    
    for u, v in ciclo_euleriano:
        if u not in visitados:
            ciclo_hamiltoniano.append(u)
            visitados.add(u)
    
    # Fecha o ciclo
    ciclo_hamiltoniano.append(ciclo_hamiltoniano[0])
    
    # Calcula o custo total do ciclo
    custo_total = 0
    for i in range(len(ciclo_hamiltoniano) - 1):
        u = ciclo_hamiltoniano[i]
        v = ciclo_hamiltoniano[i + 1]
        custo_total += g_nx[u][v]['weight']
    
    return ciclo_hamiltoniano, custo_total


def algoritmo_genetico_tsp(grafo: Grafo, tamanho_populacao: int = 100, num_geracoes: int = 1000,
                          taxa_mutacao: float = 0.01, taxa_cruzamento: float = 0.8) -> Tuple[List[Any], float]:
    """
    Implementa um algoritmo genético para o problema do caixeiro viajante.
    
    Args:
        grafo: Grafo completo não direcionado com pesos nas arestas.
        tamanho_populacao: Tamanho da população de soluções.
        num_geracoes: Número de gerações a serem executadas.
        taxa_mutacao: Probabilidade de mutação de um gene.
        taxa_cruzamento: Probabilidade de cruzamento entre dois indivíduos.
        
    Returns:
        Tuple[List[Any], float]: Tupla contendo:
            - Lista de vértices que formam um ciclo hamiltoniano aproximado
            - Custo total do ciclo
            
    Raises:
        ValueError: Se o grafo for direcionado.
        ValueError: Se o grafo não for completo.
    """
    # Verifica se o grafo é direcionado
    if grafo.eh_direcionado():
        raise ValueError("O algoritmo genético só é aplicável a grafos não direcionados.")
    
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Verifica se o grafo é completo
    n = len(grafo.obter_vertices())
    if g_nx.number_of_edges() < (n * (n - 1)) // 2:
        raise ValueError("O algoritmo genético só é aplicável a grafos completos.")
    
    # Obtém os vértices do grafo
    vertices = list(grafo.obter_vertices())
    
    # Função para calcular o custo de um ciclo
    def calcular_custo(ciclo: List[Any]) -> float:
        custo = 0
        for i in range(len(ciclo) - 1):
            u = ciclo[i]
            v = ciclo[i + 1]
            custo += g_nx[u][v]['weight']
        return custo
    
    # Função para gerar um indivíduo aleatório
    def gerar_individuo() -> List[Any]:
        individuo = vertices.copy()
        np.random.shuffle(individuo)
        # Fecha o ciclo
        return individuo + [individuo[0]]
    
    # Função para gerar a população inicial
    def gerar_populacao() -> List[List[Any]]:
        return [gerar_individuo() for _ in range(tamanho_populacao)]
    
    # Função para selecionar indivíduos para reprodução usando seleção por torneio
    def selecionar(populacao: List[List[Any]], custos: List[float]) -> List[Any]:
        # Seleciona 3 indivíduos aleatoriamente
        indices = np.random.choice(len(populacao), 3, replace=False)
        # Retorna o indivíduo com menor custo
        return populacao[min(indices, key=lambda i: custos[i])]
    
    # Função para realizar cruzamento entre dois indivíduos usando PMX (Partially Mapped Crossover)
    def cruzar(pai1: List[Any], pai2: List[Any]) -> List[Any]:
        # Remove o último vértice (que é igual ao primeiro)
        p1 = pai1[:-1]
        p2 = pai2[:-1]
        
        # Escolhe dois pontos de corte
        ponto1 = np.random.randint(0, len(p1))
        ponto2 = np.random.randint(ponto1, len(p1))
        
        # Cria o filho com valores indefinidos
        filho = [None] * len(p1)
        
        # Copia o segmento entre os pontos de corte do pai1 para o filho
        for i in range(ponto1, ponto2 + 1):
            filho[i] = p1[i]
        
        # Cria um mapeamento entre os valores do segmento do pai1 e do pai2
        mapeamento = {}
        for i in range(ponto1, ponto2 + 1):
            if p2[i] not in filho:
                mapeamento[p2[i]] = p1[i]
        
        # Preenche o resto do filho com valores do pai2, respeitando o mapeamento
        for i in range(len(p1)):
            if i < ponto1 or i > ponto2:
                valor = p2[i]
                while valor in filho:
                    valor = mapeamento.get(valor, valor)
                filho[i] = valor
        
        # Fecha o ciclo
        return filho + [filho[0]]
    
    # Função para realizar mutação em um indivíduo usando troca de dois genes
    def mutar(individuo: List[Any]) -> List[Any]:
        # Remove o último vértice (que é igual ao primeiro)
        ind = individuo[:-1]
        
        # Escolhe dois pontos para trocar
        ponto1 = np.random.randint(0, len(ind))
        ponto2 = np.random.randint(0, len(ind))
        
        # Troca os valores
        ind[ponto1], ind[ponto2] = ind[ponto2], ind[ponto1]
        
        # Fecha o ciclo
        return ind + [ind[0]]
    
    # Gera a população inicial
    populacao = gerar_populacao()
    
    # Executa o algoritmo genético
    for geracao in range(num_geracoes):
        # Calcula o custo de cada indivíduo
        custos = [calcular_custo(ind) for ind in populacao]
        
        # Encontra o melhor indivíduo
        melhor_indice = np.argmin(custos)
        melhor_individuo = populacao[melhor_indice]
        melhor_custo = custos[melhor_indice]
        
        # Cria a nova população
        nova_populacao = [melhor_individuo]  # Elitismo
        
        while len(nova_populacao) < tamanho_populacao:
            # Seleciona dois pais
            pai1 = selecionar(populacao, custos)
            pai2 = selecionar(populacao, custos)
            
            # Realiza cruzamento com probabilidade taxa_cruzamento
            if np.random.random() < taxa_cruzamento:
                filho = cruzar(pai1, pai2)
            else:
                filho = pai1.copy()
            
            # Realiza mutação com probabilidade taxa_mutacao
            if np.random.random() < taxa_mutacao:
                filho = mutar(filho)
            
            # Adiciona o filho à nova população
            nova_populacao.append(filho)
        
        # Atualiza a população
        populacao = nova_populacao
    
    # Calcula o custo de cada indivíduo na população final
    custos = [calcular_custo(ind) for ind in populacao]
    
    # Encontra o melhor indivíduo
    melhor_indice = np.argmin(custos)
    melhor_individuo = populacao[melhor_indice]
    melhor_custo = custos[melhor_indice]
    
    return melhor_individuo, melhor_custo


def comparar_algoritmos_tsp(grafo: Grafo) -> Dict[str, Any]:
    """
    Compara diferentes algoritmos para o problema do caixeiro viajante.
    
    Args:
        grafo: Grafo completo não direcionado com pesos nas arestas.
        
    Returns:
        Dict[str, Any]: Dicionário contendo os resultados de cada algoritmo.
    """
    import time
    
    resultados = {}
    
    # Christofides
    inicio = time.time()
    ciclo_christofides, custo_christofides = christofides(grafo)
    fim = time.time()
    resultados['christofides'] = {
        'ciclo': ciclo_christofides,
        'custo': custo_christofides,
        'tempo': fim - inicio
    }
    
    # Algoritmo genético
    inicio = time.time()
    ciclo_genetico, custo_genetico = algoritmo_genetico_tsp(grafo)
    fim = time.time()
    resultados['genetico'] = {
        'ciclo': ciclo_genetico,
        'custo': custo_genetico,
        'tempo': fim - inicio
    }
    
    # Vizinho mais próximo (implementado anteriormente em hamiltoniano.py)
    from algoritmos.ciclos.hamiltoniano import aproximacao_ciclo_hamiltoniano
    inicio = time.time()
    ciclo_vizinho, custo_vizinho = aproximacao_ciclo_hamiltoniano(grafo)
    fim = time.time()
    resultados['vizinho_mais_proximo'] = {
        'ciclo': ciclo_vizinho,
        'custo': custo_vizinho,
        'tempo': fim - inicio
    }
    
    return resultados


def visualizar_ciclo_tsp(grafo: Grafo, ciclo: List[Any], algoritmo: str = "TSP", arquivo: str = None) -> None:
    """
    Visualiza um ciclo hamiltoniano para o problema do caixeiro viajante.
    
    Args:
        grafo: Grafo não direcionado.
        ciclo: Lista de vértices que formam um ciclo hamiltoniano.
        algoritmo: Nome do algoritmo usado para encontrar o ciclo.
        arquivo: Caminho para salvar a imagem (opcional).
    """
    import matplotlib.pyplot as plt
    import networkx as nx
    
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Define as posições dos vértices
    pos = nx.spring_layout(g_nx)
    
    # Cria as arestas do ciclo na ordem
    arestas_ciclo = [(ciclo[i], ciclo[i+1]) for i in range(len(ciclo)-1)]
    
    # Calcula o custo total do ciclo
    custo_total = sum(g_nx[u][v]['weight'] for u, v in arestas_ciclo)
    
    # Desenha o grafo
    plt.figure(figsize=(12, 8))
    
    # Desenha os vértices
    nx.draw_networkx_nodes(g_nx, pos, node_color='lightblue', node_size=500)
    
    # Desenha as arestas não pertencentes ao ciclo
    arestas_nao_ciclo = [(u, v) for u, v in g_nx.edges() if (u, v) not in arestas_ciclo and (v, u) not in arestas_ciclo]
    nx.draw_networkx_edges(g_nx, pos, edgelist=arestas_nao_ciclo, width=1, alpha=0.2)
    
    # Desenha as arestas do ciclo com cores diferentes para indicar a ordem
    for i, (u, v) in enumerate(arestas_ciclo):
        # Calcula a cor baseada na posição da aresta no ciclo
        cor = plt.cm.viridis(i / len(arestas_ciclo))
        
        # Desenha a aresta
        nx.draw_networkx_edges(g_nx, pos, edgelist=[(u, v)], width=2, edge_color=[cor])
        
        # Adiciona o número da aresta no ciclo
        edge_labels = {(u, v): str(i+1)}
        nx.draw_networkx_edge_labels(g_nx, pos, edge_labels=edge_labels, font_size=8)
    
    # Desenha os rótulos dos vértices
    nx.draw_networkx_labels(g_nx, pos)
    
    plt.title(f"Ciclo TSP ({algoritmo}) - Custo: {custo_total:.2f}")
    plt.axis('off')
    
    # Salva a imagem ou mostra na tela
    if arquivo:
        plt.savefig(arquivo)
    else:
        plt.show()
