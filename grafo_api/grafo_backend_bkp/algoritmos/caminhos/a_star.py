"""
Implementação do algoritmo A* (A-Star) para encontrar caminhos mínimos em grafos.

O algoritmo A* é uma extensão do algoritmo de Dijkstra que usa uma heurística
para guiar a busca em direção ao destino, tornando-o mais eficiente para
encontrar caminhos mínimos entre dois vértices específicos.
"""

from typing import Dict, List, Any, Tuple, Callable, Optional
import heapq
import networkx as nx
from ...core.grafo import Grafo


def a_star(grafo: Grafo, origem: Any, destino: Any, 
           heuristica: Callable[[Any, Any], float] = None) -> Tuple[List[Any], float]:
    """
    Implementa o algoritmo A* para encontrar o caminho mínimo entre dois vértices.
    
    Args:
        grafo: Grafo ponderado.
        origem: Vértice de origem.
        destino: Vértice de destino.
        heuristica: Função que estima a distância entre dois vértices.
                   Se não for fornecida, será usada uma heurística nula (equivalente a Dijkstra).
        
    Returns:
        Tuple[List[Any], float]: Tupla contendo:
            - Lista de vértices que formam o caminho mínimo
            - Custo total do caminho
            
    Raises:
        ValueError: Se algum dos vértices não existir no grafo.
        ValueError: Se não existir caminho entre origem e destino.
    """
    # Verifica se os vértices existem no grafo
    if not grafo.existe_vertice(origem):
        raise ValueError(f"Vértice de origem '{origem}' não existe no grafo.")
    if not grafo.existe_vertice(destino):
        raise ValueError(f"Vértice de destino '{destino}' não existe no grafo.")
    
    # Se a heurística não for fornecida, usa uma heurística nula
    if heuristica is None:
        heuristica = lambda u, v: 0
    
    # Obtém o grafo NetworkX subjacente
    g_nx = grafo.obter_grafo_networkx()
    
    # Inicializa as estruturas de dados
    abertos = []  # Fila de prioridade (heap) para os vértices a serem explorados
    fechados = set()  # Conjunto de vértices já explorados
    
    # Dicionário de custos g: custo do caminho da origem até o vértice
    g_custo = {vertice: float('infinity') for vertice in grafo.obter_vertices()}
    g_custo[origem] = 0
    
    # Dicionário de custos f: g(n) + h(n)
    f_custo = {vertice: float('infinity') for vertice in grafo.obter_vertices()}
    f_custo[origem] = heuristica(origem, destino)
    
    # Dicionário de predecessores para reconstrução do caminho
    predecessores = {vertice: None for vertice in grafo.obter_vertices()}
    
    # Adiciona o vértice de origem à fila de prioridade
    heapq.heappush(abertos, (f_custo[origem], origem))
    
    # Enquanto houver vértices na fila de prioridade
    while abertos:
        # Remove o vértice com menor custo f
        _, vertice_atual = heapq.heappop(abertos)
        
        # Se chegou ao destino, reconstrói o caminho e retorna
        if vertice_atual == destino:
            caminho = []
            atual = destino
            while atual is not None:
                caminho.append(atual)
                atual = predecessores[atual]
            caminho.reverse()
            return caminho, g_custo[destino]
        
        # Adiciona o vértice atual ao conjunto de fechados
        fechados.add(vertice_atual)
        
        # Para cada vizinho do vértice atual
        for vizinho in grafo.obter_adjacentes(vertice_atual):
            # Se o vizinho já foi explorado, continua
            if vizinho in fechados:
                continue
            
            # Calcula o custo g tentativo
            peso = g_nx[vertice_atual][vizinho].get('weight', 1.0)
            g_tentativo = g_custo[vertice_atual] + peso
            
            # Se o vizinho não está na fila ou o novo caminho é melhor
            if g_tentativo < g_custo[vizinho]:
                # Atualiza o predecessor
                predecessores[vizinho] = vertice_atual
                # Atualiza o custo g
                g_custo[vizinho] = g_tentativo
                # Atualiza o custo f
                f_custo[vizinho] = g_tentativo + heuristica(vizinho, destino)
                
                # Adiciona o vizinho à fila de prioridade se ainda não estiver
                if not any(vizinho == v for _, v in abertos):
                    heapq.heappush(abertos, (f_custo[vizinho], vizinho))
    
    # Se chegou aqui, não existe caminho entre origem e destino
    raise ValueError(f"Não existe caminho de '{origem}' para '{destino}'.")


def heuristica_distancia_euclidiana(grafo: Grafo, pos: Dict[Any, Tuple[float, float]]) -> Callable[[Any, Any], float]:
    """
    Cria uma função de heurística baseada na distância euclidiana entre vértices.
    
    Args:
        grafo: Grafo ponderado.
        pos: Dicionário mapeando vértices para suas coordenadas (x, y).
        
    Returns:
        Callable[[Any, Any], float]: Função de heurística que estima a distância entre dois vértices.
    """
    def heuristica(u: Any, v: Any) -> float:
        """
        Calcula a distância euclidiana entre dois vértices.
        
        Args:
            u: Primeiro vértice.
            v: Segundo vértice.
            
        Returns:
            float: Distância euclidiana entre os vértices.
        """
        if u not in pos or v not in pos:
            return 0
        
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    
    return heuristica


def heuristica_manhattan(grafo: Grafo, pos: Dict[Any, Tuple[float, float]]) -> Callable[[Any, Any], float]:
    """
    Cria uma função de heurística baseada na distância de Manhattan entre vértices.
    
    Args:
        grafo: Grafo ponderado.
        pos: Dicionário mapeando vértices para suas coordenadas (x, y).
        
    Returns:
        Callable[[Any, Any], float]: Função de heurística que estima a distância entre dois vértices.
    """
    def heuristica(u: Any, v: Any) -> float:
        """
        Calcula a distância de Manhattan entre dois vértices.
        
        Args:
            u: Primeiro vértice.
            v: Segundo vértice.
            
        Returns:
            float: Distância de Manhattan entre os vértices.
        """
        if u not in pos or v not in pos:
            return 0
        
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        return abs(x1 - x2) + abs(y1 - y2)
    
    return heuristica


def comparar_a_star_dijkstra(grafo: Grafo, origem: Any, destino: Any, 
                             heuristica: Callable[[Any, Any], float] = None) -> Dict[str, Any]:
    """
    Compara os algoritmos A* e Dijkstra para o mesmo grafo.
    
    Args:
        grafo: Grafo ponderado.
        origem: Vértice de origem.
        destino: Vértice de destino.
        heuristica: Função de heurística para o A*.
        
    Returns:
        Dict[str, Any]: Dicionário contendo:
            - 'a_star_caminho': Caminho encontrado pelo A*
            - 'a_star_custo': Custo do caminho encontrado pelo A*
            - 'dijkstra_caminho': Caminho encontrado pelo Dijkstra
            - 'dijkstra_custo': Custo do caminho encontrado pelo Dijkstra
            - 'iguais': Booleano indicando se os caminhos têm o mesmo custo
            - 'nos_explorados_a_star': Número de nós explorados pelo A*
            - 'nos_explorados_dijkstra': Número de nós explorados pelo Dijkstra
    """
    from algoritmos.caminhos.dijkstra import dijkstra, reconstruir_caminho
    
    # Contador de nós explorados para A*
    nos_explorados_a_star = [0]
    
    def a_star_contador(grafo: Grafo, origem: Any, destino: Any, heuristica: Callable[[Any, Any], float] = None):
        # Verifica se os vértices existem no grafo
        if not grafo.existe_vertice(origem):
            raise ValueError(f"Vértice de origem '{origem}' não existe no grafo.")
        if not grafo.existe_vertice(destino):
            raise ValueError(f"Vértice de destino '{destino}' não existe no grafo.")
        
        # Se a heurística não for fornecida, usa uma heurística nula
        if heuristica is None:
            heuristica = lambda u, v: 0
        
        # Obtém o grafo NetworkX subjacente
        g_nx = grafo.obter_grafo_networkx()
        
        # Inicializa as estruturas de dados
        abertos = []  # Fila de prioridade (heap) para os vértices a serem explorados
        fechados = set()  # Conjunto de vértices já explorados
        
        # Dicionário de custos g: custo do caminho da origem até o vértice
        g_custo = {vertice: float('infinity') for vertice in grafo.obter_vertices()}
        g_custo[origem] = 0
        
        # Dicionário de custos f: g(n) + h(n)
        f_custo = {vertice: float('infinity') for vertice in grafo.obter_vertices()}
        f_custo[origem] = heuristica(origem, destino)
        
        # Dicionário de predecessores para reconstrução do caminho
        predecessores = {vertice: None for vertice in grafo.obter_vertices()}
        
        # Adiciona o vértice de origem à fila de prioridade
        heapq.heappush(abertos, (f_custo[origem], origem))
        
        # Enquanto houver vértices na fila de prioridade
        while abertos:
            # Remove o vértice com menor custo f
            _, vertice_atual = heapq.heappop(abertos)
            nos_explorados_a_star[0] += 1
            
            # Se chegou ao destino, reconstrói o caminho e retorna
            if vertice_atual == destino:
                caminho = []
                atual = destino
                while atual is not None:
                    caminho.append(atual)
                    atual = predecessores[atual]
                caminho.reverse()
                return caminho, g_custo[destino]
            
            # Adiciona o vértice atual ao conjunto de fechados
            fechados.add(vertice_atual)
            
            # Para cada vizinho do vértice atual
            for vizinho in grafo.obter_adjacentes(vertice_atual):
                # Se o vizinho já foi explorado, continua
                if vizinho in fechados:
                    continue
                
                # Calcula o custo g tentativo
                peso = g_nx[vertice_atual][vizinho].get('weight', 1.0)
                g_tentativo = g_custo[vertice_atual] + peso
                
                # Se o vizinho não está na fila ou o novo caminho é melhor
                if g_tentativo < g_custo[vizinho]:
                    # Atualiza o predecessor
                    predecessores[vizinho] = vertice_atual
                    # Atualiza o custo g
                    g_custo[vizinho] = g_tentativo
                    # Atualiza o custo f
                    f_custo[vizinho] = g_tentativo + heuristica(vizinho, destino)
                    
                    # Adiciona o vizinho à fila de prioridade se ainda não estiver
                    if not any(vizinho == v for _, v in abertos):
                        heapq.heappush(abertos, (f_custo[vizinho], vizinho))
        
        # Se chegou aqui, não existe caminho entre origem e destino
        raise ValueError(f"Não existe caminho de '{origem}' para '{destino}'.")
    
    # Contador de nós explorados para Dijkstra
    nos_explorados_dijkstra = [0]
    
    def dijkstra_contador(grafo: Grafo, origem: Any):
        # Verifica se o vértice de origem existe no grafo
        if not grafo.existe_vertice(origem):
            raise ValueError(f"Vértice de origem '{origem}' não existe no grafo.")
        
        # Obtém o grafo NetworkX subjacente
        g_nx = grafo.obter_grafo_networkx()
        
        # Inicializa as estruturas de dados
        distancias = {vertice: float('infinity') for vertice in grafo.obter_vertices()}
        distancias[origem] = 0
        predecessores = {vertice: None for vertice in grafo.obter_vertices()}
        visitados = set()
        
        # Fila de prioridade para os vértices
        fila_prioridade = [(0, origem)]
        
        # Enquanto houver vértices na fila
        while fila_prioridade:
            # Remove o vértice com menor distância
            dist_atual, vertice_atual = heapq.heappop(fila_prioridade)
            nos_explorados_dijkstra[0] += 1
            
            # Se o vértice já foi visitado, continua
            if vertice_atual in visitados:
                continue
            
            # Marca o vértice como visitado
            visitados.add(vertice_atual)
            
            # Se a distância atual é maior que a registrada, continua
            if dist_atual > distancias[vertice_atual]:
                continue
            
            # Para cada vizinho do vértice atual
            for vizinho in grafo.obter_adjacentes(vertice_atual):
                # Se o vizinho já foi visitado, continua
                if vizinho in visitados:
                    continue
                
                # Calcula a nova distância
                peso = g_nx[vertice_atual][vizinho].get('weight', 1.0)
                nova_distancia = distancias[vertice_atual] + peso
                
                # Se a nova distância é menor que a registrada
                if nova_distancia < distancias[vizinho]:
                    # Atualiza a distância
                    distancias[vizinho] = nova_distancia
                    # Atualiza o predecessor
                    predecessores[vizinho] = vertice_atual
                    # Adiciona o vizinho à fila de prioridade
                    heapq.heappush(fila_prioridade, (nova_distancia, vizinho))
        
        return distancias, predecessores
    
    # Executa o A* com contador
    a_star_caminho, a_star_custo = a_star_contador(grafo, origem, destino, heuristica)
    
    # Executa o Dijkstra com contador
    distancias, predecessores = dijkstra_contador(grafo, origem)
    
    # Verifica se existe caminho para o destino
    if distancias[destino] == float('infinity'):
        raise ValueError(f"Não existe caminho de '{origem}' para '{destino}'.")
    
    # Reconstrói o caminho do Dijkstra
    dijkstra_caminho = reconstruir_caminho(predecessores, origem, destino)
    dijkstra_custo = distancias[destino]
    
    # Compara os resultados
    return {
        'a_star_caminho': a_star_caminho,
        'a_star_custo': a_star_custo,
        'dijkstra_caminho': dijkstra_caminho,
        'dijkstra_custo': dijkstra_custo,
        'iguais': abs(a_star_custo - dijkstra_custo) < 1e-9,  # Compara com tolerância para erros de ponto flutuante
        'nos_explorados_a_star': nos_explorados_a_star[0],
        'nos_explorados_dijkstra': nos_explorados_dijkstra[0]
    }
