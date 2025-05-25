"""
Implementação de algoritmos para encontrar ciclos hamiltonianos em grafos.

Um ciclo hamiltoniano é um ciclo que visita cada vértice exatamente uma vez,
exceto pelo vértice inicial que também é o final.
"""

from typing import Dict, List, Any, Tuple, Set, Optional
import networkx as nx
from grafo_backend.core.grafo import Grafo


def encontrar_ciclo_hamiltoniano_backtracking(grafo: Grafo) -> Optional[List[Any]]:
    """
    Encontra um ciclo hamiltoniano usando backtracking.
    
    Args:
        grafo: Grafo não direcionado ou direcionado.
        
    Returns:
        Optional[List[Any]]: Lista de vértices que formam um ciclo hamiltoniano,
            ou None se o grafo não for hamiltoniano.
    """
    # Verifica se o grafo tem vértices suficientes
    vertices = list(grafo.obter_vertices())
    n = len(vertices)
    
    if n < 3:
        return None if n > 0 else []
    
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Inicializa o caminho com o primeiro vértice
    caminho = [vertices[0]]
    visitados = {vertices[0]}
    
    # Função recursiva para encontrar o ciclo hamiltoniano
    def backtrack() -> bool:
        # Se todos os vértices foram visitados
        if len(caminho) == n:
            # Verifica se o último vértice está conectado ao primeiro
            ultimo = caminho[-1]
            primeiro = caminho[0]
            
            if grafo.eh_direcionado():
                return g_nx.has_edge(ultimo, primeiro)
            else:
                return g_nx.has_edge(ultimo, primeiro) or g_nx.has_edge(primeiro, ultimo)
        
        # Tenta adicionar cada vértice adjacente ao último vértice do caminho
        ultimo = caminho[-1]
        
        for vizinho in grafo.obter_adjacentes(ultimo):
            if vizinho not in visitados:
                # Adiciona o vizinho ao caminho
                caminho.append(vizinho)
                visitados.add(vizinho)
                
                # Continua a busca
                if backtrack():
                    return True
                
                # Se não encontrou um ciclo, remove o vizinho
                caminho.pop()
                visitados.remove(vizinho)
        
        return False
    
    # Inicia a busca
    if backtrack():
        # Adiciona o primeiro vértice ao final para formar um ciclo
        return caminho + [vertices[0]]
    
    return None


def encontrar_ciclo_hamiltoniano_branch_and_bound(grafo: Grafo) -> Optional[List[Any]]:
    """
    Encontra um ciclo hamiltoniano usando branch and bound.
    
    Esta implementação usa uma heurística de custo mínimo para podar ramos
    que não podem levar a uma solução ótima.
    
    Args:
        grafo: Grafo ponderado não direcionado ou direcionado.
        
    Returns:
        Optional[List[Any]]: Lista de vértices que formam um ciclo hamiltoniano,
            ou None se o grafo não for hamiltoniano.
    """
    # Verifica se o grafo tem vértices suficientes
    vertices = list(grafo.obter_vertices())
    n = len(vertices)
    
    if n < 3:
        return None if n > 0 else []
    
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Inicializa o melhor caminho e seu custo
    melhor_caminho = None
    melhor_custo = float('infinity')
    
    # Inicializa o caminho atual com o primeiro vértice
    caminho = [vertices[0]]
    visitados = {vertices[0]}
    custo_atual = 0
    
    # Função recursiva para encontrar o ciclo hamiltoniano
    def branch_and_bound() -> None:
        nonlocal melhor_caminho, melhor_custo
        
        # Se todos os vértices foram visitados
        if len(caminho) == n:
            # Verifica se o último vértice está conectado ao primeiro
            ultimo = caminho[-1]
            primeiro = caminho[0]
            
            if grafo.existe_aresta(ultimo, primeiro):
                # Calcula o custo total do ciclo
                peso_final = g_nx[ultimo][primeiro].get('weight', 1.0)
                custo_total = custo_atual + peso_final
                
                # Atualiza o melhor caminho se necessário
                if custo_total < melhor_custo:
                    melhor_custo = custo_total
                    melhor_caminho = caminho.copy() + [primeiro]
            
            return
        
        # Tenta adicionar cada vértice adjacente ao último vértice do caminho
        ultimo = caminho[-1]
        
        # Ordena os vizinhos por peso da aresta
        vizinhos = []
        for vizinho in grafo.obter_adjacentes(ultimo):
            if vizinho not in visitados:
                peso = g_nx[ultimo][vizinho].get('weight', 1.0)
                vizinhos.append((vizinho, peso))
        
        # Ordena por peso crescente
        vizinhos.sort(key=lambda x: x[1])
        
        for vizinho, peso in vizinhos:
            # Calcula o novo custo
            novo_custo = custo_atual + peso
            
            # Poda: se o novo custo já é maior que o melhor encontrado, não continua
            if novo_custo >= melhor_custo:
                continue
            
            # Adiciona o vizinho ao caminho
            caminho.append(vizinho)
            visitados.add(vizinho)
            custo_atual += peso
            
            # Continua a busca
            branch_and_bound()
            
            # Remove o vizinho
            caminho.pop()
            visitados.remove(vizinho)
            custo_atual -= peso
    
    # Inicia a busca
    branch_and_bound()
    
    return melhor_caminho


def verificar_ciclo_hamiltoniano(grafo: Grafo, ciclo: List[Any]) -> bool:
    """
    Verifica se uma lista de vértices forma um ciclo hamiltoniano válido.
    
    Args:
        grafo: Grafo não direcionado ou direcionado.
        ciclo: Lista de vértices a ser verificada.
        
    Returns:
        bool: True se a lista formar um ciclo hamiltoniano válido, False caso contrário.
    """
    # Verifica se o ciclo contém todos os vértices
    if set(ciclo[:-1]) != set(grafo.obter_vertices()):
        return False
    
    # Verifica se o primeiro e o último vértices são iguais
    if ciclo[0] != ciclo[-1]:
        return False
    
    # Verifica se cada par consecutivo de vértices forma uma aresta
    for i in range(len(ciclo) - 1):
        if not grafo.existe_aresta(ciclo[i], ciclo[i+1]):
            return False
    
    return True


def aproximacao_ciclo_hamiltoniano(grafo: Grafo) -> Tuple[List[Any], float]:
    """
    Encontra uma aproximação de um ciclo hamiltoniano usando o algoritmo do vizinho mais próximo.
    
    Args:
        grafo: Grafo ponderado não direcionado.
        
    Returns:
        Tuple[List[Any], float]: Tupla contendo:
            - Lista de vértices que formam um ciclo hamiltoniano aproximado
            - Custo total do ciclo
            
    Raises:
        ValueError: Se o grafo for direcionado.
    """
    # Verifica se o grafo é direcionado
    if grafo.eh_direcionado():
        raise ValueError("O algoritmo de aproximação só é aplicável a grafos não direcionados.")
    
    # Verifica se o grafo tem vértices suficientes
    vertices = list(grafo.obter_vertices())
    n = len(vertices)
    
    if n < 3:
        return vertices + vertices[:1], 0
    
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Inicializa o caminho com o primeiro vértice
    caminho = [vertices[0]]
    visitados = {vertices[0]}
    custo_total = 0
    
    # Enquanto não visitou todos os vértices
    while len(visitados) < n:
        ultimo = caminho[-1]
        proximo = None
        menor_peso = float('infinity')
        
        # Encontra o vizinho não visitado mais próximo
        for vizinho in grafo.obter_adjacentes(ultimo):
            if vizinho not in visitados:
                peso = g_nx[ultimo][vizinho].get('weight', 1.0)
                if peso < menor_peso:
                    menor_peso = peso
                    proximo = vizinho
        
        # Se não encontrou um próximo vértice, o grafo não é completo
        if proximo is None:
            # Tenta encontrar qualquer vértice não visitado
            for v in vertices:
                if v not in visitados:
                    proximo = v
                    # Usa um peso grande para penalizar a falta de aresta
                    menor_peso = 1000
                    break
        
        # Adiciona o próximo vértice ao caminho
        caminho.append(proximo)
        visitados.add(proximo)
        custo_total += menor_peso
    
    # Adiciona a aresta de volta ao início
    if grafo.existe_aresta(caminho[-1], caminho[0]):
        peso_final = g_nx[caminho[-1]][caminho[0]].get('weight', 1.0)
    else:
        # Penaliza a falta de aresta
        peso_final = 1000
    
    custo_total += peso_final
    
    # Fecha o ciclo
    caminho.append(caminho[0])
    
    return caminho, custo_total


def visualizar_ciclo_hamiltoniano(grafo: Grafo, ciclo: List[Any], arquivo: str = None) -> None:
    """
    Visualiza um ciclo hamiltoniano em um grafo.
    
    Args:
        grafo: Grafo não direcionado ou direcionado.
        ciclo: Lista de vértices que formam um ciclo hamiltoniano.
        arquivo: Caminho para salvar a imagem (opcional).
    """
    import matplotlib.pyplot as plt
    import networkx as nx
    
    # Cria um grafo NetworkX para visualização
    g_nx = grafo.obter_grafo_networkx()
    
    # Define as posições dos vértices
    pos = nx.spring_layout(g_nx)
    
    # Cria as arestas do ciclo na ordem
    arestas_ciclo = [(ciclo[i], ciclo[i+1]) for i in range(len(ciclo)-1)]
    
    # Desenha o grafo
    plt.figure(figsize=(12, 8))
    
    # Desenha os vértices
    nx.draw_networkx_nodes(g_nx, pos, node_color='lightblue', node_size=500)
    
    # Desenha as arestas não pertencentes ao ciclo
    arestas_nao_ciclo = [(u, v) for u, v in g_nx.edges() if (u, v) not in arestas_ciclo and (v, u) not in arestas_ciclo]
    nx.draw_networkx_edges(g_nx, pos, edgelist=arestas_nao_ciclo, width=1, alpha=0.5)
    
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
    
    plt.title("Ciclo Hamiltoniano")
    plt.axis('off')
    
    # Salva a imagem ou mostra na tela
    if arquivo:
        plt.savefig(arquivo)
    else:
        plt.show()
