"""
Implementação de algoritmos para grafos dinâmicos e temporais.

Este módulo contém implementações de estruturas e algoritmos para representar
e analisar grafos que evoluem no tempo, incluindo métricas temporais e
detecção de padrões.
"""

import networkx as nx
import numpy as np
from typing import Dict, List, Any, Set, Tuple, Optional, Callable
from core.grafo import Grafo
import datetime


class GrafoDinamico:
    """
    Classe para representação de grafos dinâmicos/temporais.
    
    Um grafo dinâmico é uma sequência de snapshots de grafos ao longo do tempo.
    """
    
    def __init__(self, nome: str):
        """
        Inicializa um grafo dinâmico.
        
        Args:
            nome: Nome do grafo dinâmico.
        """
        self.nome = nome
        self.snapshots = {}  # Dicionário mapeando timestamps para grafos
        self.timestamps = []  # Lista ordenada de timestamps
    
    def adicionar_snapshot(self, timestamp: Any, grafo: Grafo):
        """
        Adiciona um snapshot do grafo em um determinado momento.
        
        Args:
            timestamp: Identificador temporal do snapshot.
            grafo: Grafo representando o estado no momento timestamp.
        """
        self.snapshots[timestamp] = grafo
        
        # Mantém a lista de timestamps ordenada
        self.timestamps = sorted(self.snapshots.keys())
    
    def obter_snapshot(self, timestamp: Any) -> Optional[Grafo]:
        """
        Obtém o snapshot do grafo em um determinado momento.
        
        Args:
            timestamp: Identificador temporal do snapshot.
            
        Returns:
            Optional[Grafo]: Grafo no momento timestamp, ou None se não existir.
        """
        return self.snapshots.get(timestamp)
    
    def obter_timestamps(self) -> List[Any]:
        """
        Obtém a lista ordenada de timestamps.
        
        Returns:
            List[Any]: Lista ordenada de timestamps.
        """
        return self.timestamps
    
    def numero_snapshots(self) -> int:
        """
        Obtém o número de snapshots.
        
        Returns:
            int: Número de snapshots.
        """
        return len(self.snapshots)
    
    def interpolar_snapshot(self, timestamp: Any) -> Optional[Grafo]:
        """
        Interpola um snapshot para um timestamp que não existe explicitamente.
        
        Args:
            timestamp: Identificador temporal para interpolação.
            
        Returns:
            Optional[Grafo]: Grafo interpolado, ou None se não for possível interpolar.
        """
        # Se o timestamp existe, retorna o snapshot diretamente
        if timestamp in self.snapshots:
            return self.snapshots[timestamp]
        
        # Se não há snapshots suficientes para interpolar
        if len(self.timestamps) < 2:
            return None
        
        # Encontra os timestamps anterior e posterior
        anterior = None
        posterior = None
        
        for t in self.timestamps:
            if t < timestamp:
                anterior = t
            elif t > timestamp:
                posterior = t
                break
        
        # Se não encontrou anterior ou posterior, não é possível interpolar
        if anterior is None or posterior is None:
            return None
        
        # Obtém os snapshots anterior e posterior
        grafo_anterior = self.snapshots[anterior]
        grafo_posterior = self.snapshots[posterior]
        
        # Cria um novo grafo para o resultado da interpolação
        from core.grafo import Grafo
        grafo_interpolado = Grafo(f"Interpolação em {timestamp}")
        
        # Obtém os grafos NetworkX subjacentes
        g_anterior = grafo_anterior.obter_grafo_networkx()
        g_posterior = grafo_posterior.obter_grafo_networkx()
        
        # Adiciona todos os vértices que existem em pelo menos um dos grafos
        todos_vertices = set(g_anterior.nodes()) | set(g_posterior.nodes())
        for v in todos_vertices:
            grafo_interpolado.adicionar_vertice(v)
        
        # Adiciona arestas que existem em ambos os grafos
        for u, v in set(g_anterior.edges()) & set(g_posterior.edges()):
            grafo_interpolado.adicionar_aresta(u, v)
        
        return grafo_interpolado
    
    def calcular_metricas_temporais(self) -> Dict[str, float]:
        """
        Calcula métricas temporais para o grafo dinâmico.
        
        Returns:
            Dict[str, float]: Dicionário com métricas temporais.
        """
        if len(self.timestamps) < 2:
            return {"taxa_mudanca": 0.0, "estabilidade": 1.0}
        
        # Calcula a taxa média de mudança de arestas entre snapshots consecutivos
        taxa_mudanca_total = 0.0
        estabilidade_total = 0.0
        
        for i in range(1, len(self.timestamps)):
            t_anterior = self.timestamps[i-1]
            t_atual = self.timestamps[i]
            
            grafo_anterior = self.snapshots[t_anterior]
            grafo_atual = self.snapshots[t_atual]
            
            g_anterior = grafo_anterior.obter_grafo_networkx()
            g_atual = grafo_atual.obter_grafo_networkx()
            
            # Calcula o número de arestas adicionadas e removidas
            arestas_anteriores = set(g_anterior.edges())
            arestas_atuais = set(g_atual.edges())
            
            arestas_adicionadas = len(arestas_atuais - arestas_anteriores)
            arestas_removidas = len(arestas_anteriores - arestas_atuais)
            
            # Taxa de mudança: proporção de arestas que mudaram
            total_arestas = max(1, len(arestas_anteriores | arestas_atuais))
            taxa_mudanca = (arestas_adicionadas + arestas_removidas) / total_arestas
            
            # Estabilidade: proporção de arestas que permaneceram iguais
            arestas_mantidas = len(arestas_anteriores & arestas_atuais)
            estabilidade = arestas_mantidas / total_arestas if total_arestas > 0 else 1.0
            
            taxa_mudanca_total += taxa_mudanca
            estabilidade_total += estabilidade
        
        # Calcula as médias
        taxa_mudanca_media = taxa_mudanca_total / (len(self.timestamps) - 1)
        estabilidade_media = estabilidade_total / (len(self.timestamps) - 1)
        
        return {
            "taxa_mudanca": taxa_mudanca_media,
            "estabilidade": estabilidade_media
        }
    
    def detectar_comunidades_temporais(self, algoritmo_comunidade: Callable[[Grafo], Dict[Any, int]]) -> Dict[Any, Dict[Any, int]]:
        """
        Detecta comunidades ao longo do tempo.
        
        Args:
            algoritmo_comunidade: Função que recebe um grafo e retorna um dicionário
                                 mapeando vértices para suas comunidades.
            
        Returns:
            Dict[Any, Dict[Any, int]]: Dicionário mapeando timestamps para dicionários
                                     de comunidades.
        """
        comunidades_temporais = {}
        
        for timestamp in self.timestamps:
            grafo = self.snapshots[timestamp]
            comunidades = algoritmo_comunidade(grafo)
            comunidades_temporais[timestamp] = comunidades
        
        return comunidades_temporais
    
    def calcular_fluxo_temporal(self, origem: Any, destino: Any) -> Dict[Any, float]:
        """
        Calcula o fluxo entre dois vértices ao longo do tempo.
        
        Args:
            origem: Vértice de origem.
            destino: Vértice de destino.
            
        Returns:
            Dict[Any, float]: Dicionário mapeando timestamps para valores de fluxo.
        """
        fluxos = {}
        
        for timestamp in self.timestamps:
            grafo = self.snapshots[timestamp]
            g_nx = grafo.obter_grafo_networkx()
            
            # Verifica se os vértices existem no grafo
            if origem not in g_nx.nodes() or destino not in g_nx.nodes():
                fluxos[timestamp] = 0.0
                continue
            
            # Tenta calcular o fluxo máximo
            try:
                valor_fluxo = nx.maximum_flow_value(g_nx, origem, destino)
                fluxos[timestamp] = valor_fluxo
            except nx.NetworkXError:
                # Se não for possível calcular o fluxo (por exemplo, se não houver caminho)
                fluxos[timestamp] = 0.0
        
        return fluxos
    
    def calcular_centralidade_temporal(self, metrica_centralidade: Callable[[Grafo, Any], float]) -> Dict[Any, Dict[Any, float]]:
        """
        Calcula a centralidade dos vértices ao longo do tempo.
        
        Args:
            metrica_centralidade: Função que recebe um grafo e um vértice e retorna
                                 sua centralidade.
            
        Returns:
            Dict[Any, Dict[Any, float]]: Dicionário mapeando timestamps para dicionários
                                       de centralidades.
        """
        centralidades_temporais = {}
        
        for timestamp in self.timestamps:
            grafo = self.snapshots[timestamp]
            g_nx = grafo.obter_grafo_networkx()
            
            centralidades = {}
            for vertice in g_nx.nodes():
                centralidades[vertice] = metrica_centralidade(grafo, vertice)
            
            centralidades_temporais[timestamp] = centralidades
        
        return centralidades_temporais
    
    def detectar_eventos(self) -> Dict[str, List[Tuple[Any, Any, Any]]]:
        """
        Detecta eventos significativos na evolução do grafo.
        
        Returns:
            Dict[str, List[Tuple[Any, Any, Any]]]: Dicionário mapeando tipos de eventos
                                                para listas de eventos (timestamp, entidade, valor).
        """
        eventos = {
            "novo_vertice": [],
            "remocao_vertice": [],
            "nova_aresta": [],
            "remocao_aresta": [],
            "aumento_grau": [],
            "diminuicao_grau": []
        }
        
        if len(self.timestamps) < 2:
            return eventos
        
        for i in range(1, len(self.timestamps)):
            t_anterior = self.timestamps[i-1]
            t_atual = self.timestamps[i]
            
            grafo_anterior = self.snapshots[t_anterior]
            grafo_atual = self.snapshots[t_atual]
            
            g_anterior = grafo_anterior.obter_grafo_networkx()
            g_atual = grafo_atual.obter_grafo_networkx()
            
            # Detecta novos vértices e remoções
            vertices_anteriores = set(g_anterior.nodes())
            vertices_atuais = set(g_atual.nodes())
            
            for v in vertices_atuais - vertices_anteriores:
                eventos["novo_vertice"].append((t_atual, v, None))
            
            for v in vertices_anteriores - vertices_atuais:
                eventos["remocao_vertice"].append((t_atual, v, None))
            
            # Detecta novas arestas e remoções
            arestas_anteriores = set(g_anterior.edges())
            arestas_atuais = set(g_atual.edges())
            
            for u, v in arestas_atuais - arestas_anteriores:
                eventos["nova_aresta"].append((t_atual, (u, v), None))
            
            for u, v in arestas_anteriores - arestas_atuais:
                eventos["remocao_aresta"].append((t_atual, (u, v), None))
            
            # Detecta mudanças de grau
            vertices_comuns = vertices_anteriores & vertices_atuais
            for v in vertices_comuns:
                grau_anterior = g_anterior.degree(v)
                grau_atual = g_atual.degree(v)
                
                if grau_atual > grau_anterior:
                    eventos["aumento_grau"].append((t_atual, v, grau_atual - grau_anterior))
                elif grau_atual < grau_anterior:
                    eventos["diminuicao_grau"].append((t_atual, v, grau_anterior - grau_atual))
        
        return eventos


def criar_grafo_dinamico_de_snapshots(nome: str, snapshots: Dict[Any, Grafo]) -> GrafoDinamico:
    """
    Cria um grafo dinâmico a partir de snapshots.
    
    Args:
        nome: Nome do grafo dinâmico.
        snapshots: Dicionário mapeando timestamps para grafos.
        
    Returns:
        GrafoDinamico: Grafo dinâmico criado.
    """
    grafo_dinamico = GrafoDinamico(nome)
    
    for timestamp, grafo in snapshots.items():
        grafo_dinamico.adicionar_snapshot(timestamp, grafo)
    
    return grafo_dinamico


def calcular_latencia_temporal(grafo_dinamico: GrafoDinamico, origem: Any, destino: Any) -> Dict[Any, float]:
    """
    Calcula a latência temporal entre dois vértices ao longo do tempo.
    
    A latência temporal é o tempo necessário para uma informação se propagar
    de um vértice a outro.
    
    Args:
        grafo_dinamico: Grafo dinâmico a ser analisado.
        origem: Vértice de origem.
        destino: Vértice de destino.
        
    Returns:
        Dict[Any, float]: Dicionário mapeando timestamps para latências.
    """
    latencias = {}
    timestamps = grafo_dinamico.obter_timestamps()
    
    for i, timestamp in enumerate(timestamps):
        grafo = grafo_dinamico.obter_snapshot(timestamp)
        g_nx = grafo.obter_grafo_networkx()
        
        # Verifica se os vértices existem no grafo
        if origem not in g_nx.nodes() or destino not in g_nx.nodes():
            latencias[timestamp] = float('inf')
            continue
        
        # Tenta calcular o caminho mais curto
        try:
            caminho = nx.shortest_path(g_nx, origem, destino)
            latencias[timestamp] = len(caminho) - 1  # Número de arestas no caminho
        except nx.NetworkXNoPath:
            # Se não houver caminho
            latencias[timestamp] = float('inf')
    
    return latencias


def calcular_duracao_aresta(grafo_dinamico: GrafoDinamico, u: Any, v: Any) -> float:
    """
    Calcula a duração total de uma aresta no grafo dinâmico.
    
    Args:
        grafo_dinamico: Grafo dinâmico a ser analisado.
        u: Primeiro vértice da aresta.
        v: Segundo vértice da aresta.
        
    Returns:
        float: Duração total da aresta (proporção de snapshots em que a aresta existe).
    """
    timestamps = grafo_dinamico.obter_timestamps()
    
    if not timestamps:
        return 0.0
    
    # Conta em quantos snapshots a aresta existe
    count = 0
    for timestamp in timestamps:
        grafo = grafo_dinamico.obter_snapshot(timestamp)
        g_nx = grafo.obter_grafo_networkx()
        
        if g_nx.has_edge(u, v):
            count += 1
    
    # Retorna a proporção
    return count / len(timestamps)


def calcular_estabilidade_vertice(grafo_dinamico: GrafoDinamico, vertice: Any) -> float:
    """
    Calcula a estabilidade de um vértice no grafo dinâmico.
    
    A estabilidade é medida pela variação do grau do vértice ao longo do tempo.
    
    Args:
        grafo_dinamico: Grafo dinâmico a ser analisado.
        vertice: Vértice a ser analisado.
        
    Returns:
        float: Estabilidade do vértice (1.0 = completamente estável, 0.0 = completamente instável).
    """
    timestamps = grafo_dinamico.obter_timestamps()
    
    if len(timestamps) < 2:
        return 1.0
    
    # Coleta os graus do vértice em cada snapshot
    graus = []
    for timestamp in timestamps:
        grafo = grafo_dinamico.obter_snapshot(timestamp)
        g_nx = grafo.obter_grafo_networkx()
        
        if vertice in g_nx.nodes():
            graus.append(g_nx.degree(vertice))
        else:
            graus.append(0)
    
    # Calcula a variação média do grau
    variacao_total = 0
    for i in range(1, len(graus)):
        variacao_total += abs(graus[i] - graus[i-1])
    
    variacao_media = variacao_total / (len(graus) - 1)
    
    # Calcula o grau médio
    grau_medio = sum(graus) / len(graus)
    
    # Normaliza a variação em relação ao grau médio
    if grau_medio > 0:
        estabilidade = 1.0 - min(1.0, variacao_media / grau_medio)
    else:
        estabilidade = 1.0 if variacao_media == 0 else 0.0
    
    return estabilidade
