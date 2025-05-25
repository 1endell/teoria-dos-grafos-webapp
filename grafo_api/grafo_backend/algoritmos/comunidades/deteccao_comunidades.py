"""
Implementação do algoritmo de Girvan-Newman para detecção de comunidades em grafos.

O algoritmo de Girvan-Newman detecta comunidades em grafos removendo iterativamente
as arestas com maior centralidade de intermediação (betweenness centrality).
"""

from typing import Dict, List, Any, Tuple, Set, Optional
import networkx as nx
import numpy as np
from collections import deque
from core.grafo import Grafo


def girvan_newman(grafo: Grafo, num_comunidades: int = None) -> List[Set[Any]]:
    """
    Implementa o algoritmo de Girvan-Newman para detecção de comunidades.
    
    Args:
        grafo: Grafo não direcionado.
        num_comunidades: Número desejado de comunidades (opcional).
            Se não for especificado, o algoritmo encontrará a melhor partição.
        
    Returns:
        List[Set[Any]]: Lista de conjuntos, onde cada conjunto contém os vértices de uma comunidade.
            
    Raises:
        ValueError: Se o grafo for direcionado.
    """
    # Verifica se o grafo é direcionado
    if grafo.eh_direcionado():
        raise ValueError("O algoritmo de Girvan-Newman só é aplicável a grafos não direcionados.")
    
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Cria uma cópia do grafo para manipulação
    g_copia = g_nx.copy()
    
    # Lista para armazenar as comunidades em cada iteração
    todas_comunidades = []
    
    # Função para calcular a centralidade de intermediação das arestas
    def calcular_centralidade_intermediacao() -> Dict[Tuple[Any, Any], float]:
        # Inicializa a centralidade de cada aresta (garantindo que ambas as direções estejam presentes)
        centralidade = {}
        for u, v in g_copia.edges():
            centralidade[(u, v)] = 0.0
            centralidade[(v, u)] = 0.0  # Garante que ambas as direções estejam presentes
        
        # Para cada par de vértices
        vertices = list(g_copia.nodes())
        
        for s in vertices:
            # Inicializa as estruturas para BFS
            distancias = {v: float('infinity') for v in vertices}
            distancias[s] = 0
            
            # Número de caminhos mais curtos
            num_caminhos = {v: 0 for v in vertices}
            num_caminhos[s] = 1
            
            # Predecessores de cada vértice
            predecessores = {v: [] for v in vertices}
            
            # Fila para BFS
            fila = deque([s])
            
            # Executa BFS
            while fila:
                v = fila.popleft()
                
                for w in g_copia.neighbors(v):
                    # Se w ainda não foi descoberto
                    if distancias[w] == float('infinity'):
                        distancias[w] = distancias[v] + 1
                        fila.append(w)
                    
                    # Se w está no próximo nível da BFS
                    if distancias[w] == distancias[v] + 1:
                        num_caminhos[w] += num_caminhos[v]
                        predecessores[w].append(v)
            
            # Inicializa a contribuição de cada vértice
            contribuicao = {v: 0.0 for v in vertices}
            
            # Processa os vértices em ordem decrescente de distância
            for w in sorted(vertices, key=lambda x: -distancias[x]):
                for v in predecessores[w]:
                    # Contribuição de v para os caminhos até w
                    if num_caminhos[w] > 0:  # Evita divisão por zero
                        contribuicao[v] += (num_caminhos[v] / num_caminhos[w]) * (1 + contribuicao[w])
                    
                    # Atualiza a centralidade da aresta
                    if v != s:  # Evita contar duas vezes
                        if num_caminhos[w] > 0:  # Evita divisão por zero
                            valor = (num_caminhos[v] / num_caminhos[w]) * (1 + contribuicao[w])
                            # Garante que a aresta existe no dicionário de centralidade
                            if (v, w) in centralidade:
                                centralidade[(v, w)] += valor
                            elif (w, v) in centralidade:
                                centralidade[(w, v)] += valor
        
        # Divide por 2 para evitar contar cada aresta duas vezes
        for k in centralidade:
            centralidade[k] /= 2.0
        
        # Filtra apenas as arestas reais do grafo para retornar
        arestas_reais = {}
        for u, v in g_copia.edges():
            if (u, v) in centralidade:
                arestas_reais[(u, v)] = centralidade[(u, v)]
            elif (v, u) in centralidade:
                arestas_reais[(u, v)] = centralidade[(v, u)]
        
        return arestas_reais
    
    # Função para encontrar as comunidades atuais
    def encontrar_comunidades() -> List[Set[Any]]:
        return [set(c) for c in nx.connected_components(g_copia)]
    
    # Função para calcular a modularidade de uma partição
    def calcular_modularidade(comunidades: List[Set[Any]]) -> float:
        m = g_nx.number_of_edges()
        if m == 0:
            return 0.0
        
        modularidade = 0.0
        
        for comunidade in comunidades:
            for i in comunidade:
                for j in comunidade:
                    # Verifica se existe aresta entre i e j no grafo original
                    a_ij = 1.0 if g_nx.has_edge(i, j) else 0.0
                    
                    # Graus dos vértices no grafo original
                    k_i = g_nx.degree(i)
                    k_j = g_nx.degree(j)
                    
                    # Contribuição para a modularidade
                    modularidade += a_ij - (k_i * k_j) / (2.0 * m)
        
        return modularidade / (2.0 * m)
    
    # Inicializa as melhores comunidades e sua modularidade
    melhores_comunidades = encontrar_comunidades()
    melhor_modularidade = calcular_modularidade(melhores_comunidades)
    
    # Adiciona as comunidades iniciais
    todas_comunidades.append(melhores_comunidades)
    
    # Enquanto houver arestas para remover
    while g_copia.number_of_edges() > 0:
        # Calcula a centralidade de intermediação
        centralidade = calcular_centralidade_intermediacao()
        
        # Encontra a aresta com maior centralidade
        aresta_max = max(centralidade.items(), key=lambda x: x[1])[0]
        
        # Remove a aresta
        g_copia.remove_edge(*aresta_max)
        
        # Encontra as novas comunidades
        comunidades = encontrar_comunidades()
        
        # Adiciona as novas comunidades
        todas_comunidades.append(comunidades)
        
        # Calcula a modularidade
        modularidade = calcular_modularidade(comunidades)
        
        # Atualiza as melhores comunidades se necessário
        if modularidade > melhor_modularidade:
            melhor_modularidade = modularidade
            melhores_comunidades = comunidades
        
        # Se atingiu o número desejado de comunidades, para
        if num_comunidades is not None and len(comunidades) >= num_comunidades:
            break
    
    # Retorna as melhores comunidades ou as comunidades com o número desejado
    if num_comunidades is not None:
        for comunidades in todas_comunidades:
            if len(comunidades) == num_comunidades:
                return comunidades
    
    return melhores_comunidades


def louvain_method(grafo: Grafo) -> List[Set[Any]]:
    """
    Implementa o método de Louvain para detecção de comunidades.
    
    O método de Louvain é um algoritmo hierárquico que otimiza a modularidade
    em duas fases: primeiro atribui cada vértice a uma comunidade, depois
    agrega as comunidades em um novo grafo.
    
    Args:
        grafo: Grafo não direcionado.
        
    Returns:
        List[Set[Any]]: Lista de conjuntos, onde cada conjunto contém os vértices de uma comunidade.
            
    Raises:
        ValueError: Se o grafo for direcionado.
    """
    # Verifica se o grafo é direcionado
    if grafo.eh_direcionado():
        raise ValueError("O método de Louvain só é aplicável a grafos não direcionados.")
    
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Função para calcular a modularidade
    def calcular_modularidade(comunidades: Dict[Any, int]) -> float:
        m = g_nx.number_of_edges()
        if m == 0:
            return 0.0
        
        modularidade = 0.0
        
        # Calcula a soma dos pesos dentro de cada comunidade
        soma_dentro = {}
        soma_total = {}
        
        for i, j, peso in g_nx.edges(data='weight', default=1.0):
            if comunidades[i] == comunidades[j]:
                if comunidades[i] not in soma_dentro:
                    soma_dentro[comunidades[i]] = 0.0
                soma_dentro[comunidades[i]] += peso
            
            if comunidades[i] not in soma_total:
                soma_total[comunidades[i]] = 0.0
            soma_total[comunidades[i]] += peso
            
            if comunidades[j] not in soma_total:
                soma_total[comunidades[j]] = 0.0
            soma_total[comunidades[j]] += peso
        
        # Calcula a modularidade
        for c in soma_dentro:
            modularidade += (soma_dentro[c] / (2.0 * m)) - ((soma_total[c] / (2.0 * m)) ** 2)
        
        return modularidade
    
    # Função para a primeira fase do algoritmo
    def primeira_fase(g: nx.Graph) -> Dict[Any, int]:
        # Inicializa cada vértice em sua própria comunidade
        comunidades = {v: i for i, v in enumerate(g.nodes())}
        
        # Calcula o ganho de modularidade ao mover um vértice para uma comunidade
        def calcular_ganho(v: Any, comunidade: int) -> float:
            k_i = sum(peso for _, _, peso in g.edges(v, data='weight', default=1.0))
            k_i_in = sum(peso for u, _, peso in g.edges(v, data='weight', default=1.0) if comunidades[u] == comunidade)
            m = g.size(weight='weight')
            
            # Soma dos pesos das arestas na comunidade
            soma_tot = sum(peso for u, _, peso in g.edges(data='weight', default=1.0) if comunidades[u] == comunidade)
            
            return (k_i_in - soma_tot * k_i / (2.0 * m)) / (2.0 * m)
        
        # Enquanto houver melhorias
        melhorou = True
        
        while melhorou:
            melhorou = False
            
            # Para cada vértice
            for v in g.nodes():
                # Comunidade atual do vértice
                comunidade_atual = comunidades[v]
                
                # Comunidades vizinhas
                comunidades_vizinhas = set(comunidades[u] for u in g.neighbors(v))
                
                # Melhor comunidade e ganho
                melhor_comunidade = comunidade_atual
                melhor_ganho = 0.0
                
                # Verifica o ganho para cada comunidade vizinha
                for comunidade in comunidades_vizinhas:
                    if comunidade != comunidade_atual:
                        ganho = calcular_ganho(v, comunidade)
                        
                        if ganho > melhor_ganho:
                            melhor_ganho = ganho
                            melhor_comunidade = comunidade
                
                # Se encontrou uma comunidade melhor
                if melhor_comunidade != comunidade_atual:
                    comunidades[v] = melhor_comunidade
                    melhorou = True
        
        return comunidades
    
    # Função para a segunda fase do algoritmo
    def segunda_fase(g: nx.Graph, comunidades: Dict[Any, int]) -> nx.Graph:
        # Cria um novo grafo onde cada nó é uma comunidade
        g_novo = nx.Graph()
        
        # Adiciona os nós (comunidades)
        for c in set(comunidades.values()):
            g_novo.add_node(c)
        
        # Adiciona as arestas entre comunidades
        for u, v, peso in g.edges(data='weight', default=1.0):
            c_u = comunidades[u]
            c_v = comunidades[v]
            
            if g_novo.has_edge(c_u, c_v):
                g_novo[c_u][c_v]['weight'] += peso
            else:
                g_novo.add_edge(c_u, c_v, weight=peso)
        
        return g_novo
    
    # Inicializa o grafo atual
    g_atual = g_nx.copy()
    
    # Mapeamento de vértices para comunidades
    mapeamento = {v: v for v in g_nx.nodes()}
    
    # Enquanto houver melhorias
    while True:
        # Primeira fase
        comunidades = primeira_fase(g_atual)
        
        # Atualiza o mapeamento
        mapeamento = {v: comunidades[mapeamento[v]] for v in g_nx.nodes()}
        
        # Segunda fase
        g_novo = segunda_fase(g_atual, comunidades)
        
        # Se não houve agregação, termina
        if g_novo.number_of_nodes() == g_atual.number_of_nodes():
            break
        
        # Atualiza o grafo atual
        g_atual = g_novo
    
    # Constrói as comunidades finais
    comunidades_finais = {}
    
    for v in g_nx.nodes():
        c = mapeamento[v]
        
        if c not in comunidades_finais:
            comunidades_finais[c] = set()
        
        comunidades_finais[c].add(v)
    
    return list(comunidades_finais.values())


def calcular_modularidade(grafo: Grafo, comunidades: List[Set[Any]]) -> float:
    """
    Calcula a modularidade de uma partição em comunidades.
    
    A modularidade é uma medida da qualidade de uma partição em comunidades,
    que compara a densidade de conexões dentro das comunidades com a densidade
    esperada em um grafo aleatório com a mesma distribuição de graus.
    
    Args:
        grafo: Grafo não direcionado.
        comunidades: Lista de conjuntos, onde cada conjunto contém os vértices de uma comunidade.
        
    Returns:
        float: Valor da modularidade, entre -0.5 e 1.0.
            Valores próximos de 1.0 indicam uma boa partição.
    """
    # Verifica se o grafo é direcionado
    if grafo.eh_direcionado():
        raise ValueError("O cálculo de modularidade só é aplicável a grafos não direcionados.")
    
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Número de arestas
    m = g_nx.number_of_edges()
    if m == 0:
        return 0.0
    
    # Calcula a modularidade
    modularidade = 0.0
    
    for comunidade in comunidades:
        for i in comunidade:
            for j in comunidade:
                # Verifica se existe aresta entre i e j
                a_ij = 1.0 if g_nx.has_edge(i, j) else 0.0
                
                # Graus dos vértices
                k_i = g_nx.degree(i)
                k_j = g_nx.degree(j)
                
                # Contribuição para a modularidade
                modularidade += a_ij - (k_i * k_j) / (2.0 * m)
    
    return modularidade / (2.0 * m)


def visualizar_comunidades(grafo: Grafo, comunidades: List[Set[Any]], arquivo: str = None) -> None:
    """
    Visualiza as comunidades em um grafo.
    
    Args:
        grafo: Grafo não direcionado.
        comunidades: Lista de conjuntos, onde cada conjunto contém os vértices de uma comunidade.
        arquivo: Caminho para salvar a imagem (opcional).
    """
    import matplotlib.pyplot as plt
    import networkx as nx
    import matplotlib.cm as cm
    
    # Cria um grafo NetworkX para visualização
    g_nx = grafo.obter_grafo_networkx()
    
    # Define as posições dos vértices
    pos = nx.spring_layout(g_nx)
    
    # Desenha o grafo
    plt.figure(figsize=(12, 8))
    
    # Desenha as arestas
    nx.draw_networkx_edges(g_nx, pos, alpha=0.3)
    
    # Desenha os vértices e as comunidades
    cores = cm.rainbow(np.linspace(0, 1, len(comunidades)))
    
    for i, comunidade in enumerate(comunidades):
        nx.draw_networkx_nodes(g_nx, pos, nodelist=list(comunidade), node_color=[cores[i]], node_size=500)
    
    # Desenha os rótulos dos vértices
    nx.draw_networkx_labels(g_nx, pos)
    
    # Calcula a modularidade
    modularidade = calcular_modularidade(grafo, comunidades)
    
    plt.title(f"Comunidades (total: {len(comunidades)}, modularidade: {modularidade:.4f})")
    plt.axis('off')
    
    # Salva a imagem ou mostra na tela
    if arquivo:
        plt.savefig(arquivo)
    else:
        plt.show()
