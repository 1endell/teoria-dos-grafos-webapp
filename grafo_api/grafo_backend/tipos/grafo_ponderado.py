"""
Implementação da classe GrafoPonderado para grafos ponderados.
"""

from typing import Dict, List, Any, Optional, Set, Tuple, Union
import networkx as nx
import logging

from grafo_backend.core.grafo import Grafo

# Configuração de logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class GrafoPonderado(Grafo):
    """
    Classe para representação de grafos ponderados.
    """
    
    def __init__(self, nome: str, direcionado: bool = False):
        """
        Inicializa um grafo ponderado.
        
        Args:
            nome: Nome do grafo.
            direcionado: Se True, cria um grafo direcionado.
        """
        super().__init__(nome, direcionado)
        logger.debug(f"GrafoPonderado inicializado: Nome={nome}, Direcionado={direcionado}")
    
    def adicionar_aresta(self, origem: Any, destino: Any, peso: float = 1.0, atributos: Dict[str, Any] = None) -> bool:
        """
        Adiciona uma aresta ponderada ao grafo.
        
        Args:
            origem: Vértice de origem.
            destino: Vértice de destino.
            peso: Peso da aresta.
            atributos: Atributos da aresta.
            
        Returns:
            bool: True se a aresta foi adicionada, False caso contrário.
        """
        # Inicializa atributos se não fornecidos
        if atributos is None:
            atributos = {}
        
        # Adiciona o peso aos atributos
        atributos["peso"] = peso
        
        # Chama o método da classe base para adicionar a aresta
        return super().adicionar_aresta(origem, destino, atributos)
    
    def obter_peso_aresta(self, origem: Any, destino: Any) -> float:
        """
        Obtém o peso de uma aresta.
        
        Args:
            origem: Vértice de origem.
            destino: Vértice de destino.
            
        Returns:
            float: Peso da aresta.
            
        Raises:
            ValueError: Se a aresta não existir.
        """
        if not self.existe_aresta(origem, destino):
            raise ValueError(f"Aresta ({origem}, {destino}) não existe no grafo.")
        
        # Obtém os atributos da aresta
        atributos = self.obter_atributos_aresta(origem, destino)
        
        # Retorna o peso da aresta
        return atributos.get("peso", 1.0)
    
    def definir_peso_aresta(self, origem: Any, destino: Any, peso: float) -> bool:
        """
        Define o peso de uma aresta.
        
        Args:
            origem: Vértice de origem.
            destino: Vértice de destino.
            peso: Novo peso da aresta.
            
        Returns:
            bool: True se o peso foi definido, False caso contrário.
        """
        if not self.existe_aresta(origem, destino):
            return False
        
        # Obtém os atributos da aresta
        atributos = self.obter_atributos_aresta(origem, destino)
        
        # Atualiza o peso
        atributos["peso"] = peso
        
        # Define os atributos atualizados
        self.definir_atributos_aresta(origem, destino, atributos)
        
        return True
    
    def calcular_grau(self, vertice: Any) -> int:
        """
        Calcula o grau de um vértice.
        
        Args:
            vertice: Vértice para calcular o grau.
            
        Returns:
            int: Grau do vértice.
            
        Raises:
            ValueError: Se o vértice não existir.
        """
        return self.obter_grau(vertice)
    
    def eh_isomorfo(self, outro_grafo: 'Grafo') -> bool:
        """
        Verifica se este grafo é isomorfo a outro grafo.
        
        Args:
            outro_grafo: Outro grafo para comparação.
            
        Returns:
            bool: True se os grafos são isomorfos, False caso contrário.
        """
        # Verifica se os grafos têm o mesmo número de vértices e arestas
        if self.numero_vertices() != outro_grafo.numero_vertices() or self.numero_arestas() != outro_grafo.numero_arestas():
            return False
        
        # Converte para NetworkX para usar o algoritmo de isomorfismo
        G1 = self.para_networkx()
        G2 = outro_grafo.para_networkx()
        
        # Verifica isomorfismo
        return nx.is_isomorphic(G1, G2)
    
    def calcular_similaridade(self, outro_grafo: 'Grafo', metrica: str = "espectral") -> float:
        """
        Calcula a similaridade entre este grafo e outro grafo.
        
        Args:
            outro_grafo: Outro grafo para comparação.
            metrica: Métrica de similaridade (espectral, jaccard, edit_distance).
            
        Returns:
            float: Valor de similaridade entre 0 e 1.
        """
        # Converte para NetworkX
        G1 = self.para_networkx()
        G2 = outro_grafo.para_networkx()
        
        if metrica == "espectral":
            # Similaridade espectral (baseada em autovalores)
            try:
                import numpy as np
                from scipy import linalg
                
                # Calcula os autovalores das matrizes de adjacência
                A1 = nx.adjacency_matrix(G1).todense()
                A2 = nx.adjacency_matrix(G2).todense()
                
                # Calcula os autovalores
                eig1 = linalg.eigvals(A1)
                eig2 = linalg.eigvals(A2)
                
                # Ordena os autovalores
                eig1 = sorted(abs(eig1))
                eig2 = sorted(abs(eig2))
                
                # Normaliza os vetores para o mesmo tamanho
                max_len = max(len(eig1), len(eig2))
                eig1 = eig1 + [0] * (max_len - len(eig1))
                eig2 = eig2 + [0] * (max_len - len(eig2))
                
                # Calcula a distância euclidiana normalizada
                dist = np.linalg.norm(np.array(eig1) - np.array(eig2))
                max_dist = np.linalg.norm(np.array(eig1)) + np.linalg.norm(np.array(eig2))
                
                # Converte distância para similaridade
                if max_dist == 0:
                    return 1.0
                return 1.0 - (dist / max_dist)
            
            except ImportError:
                logger.warning("Bibliotecas numpy ou scipy não disponíveis. Usando similaridade Jaccard.")
                metrica = "jaccard"
        
        if metrica == "jaccard":
            # Similaridade de Jaccard (baseada em conjuntos de arestas)
            arestas1 = set(G1.edges())
            arestas2 = set(G2.edges())
            
            # Calcula a similaridade de Jaccard
            intersecao = len(arestas1.intersection(arestas2))
            uniao = len(arestas1.union(arestas2))
            
            if uniao == 0:
                return 1.0
            return intersecao / uniao
        
        if metrica == "edit_distance":
            # Distância de edição de grafos
            try:
                # Calcula a distância de edição
                dist = nx.graph_edit_distance(G1, G2)
                max_dist = self.numero_vertices() + outro_grafo.numero_vertices() + self.numero_arestas() + outro_grafo.numero_arestas()
                
                # Converte distância para similaridade
                if max_dist == 0:
                    return 1.0
                return 1.0 - (dist / max_dist)
            
            except nx.NetworkXError:
                logger.warning("Erro ao calcular distância de edição. Usando similaridade Jaccard.")
                # Recorre à similaridade de Jaccard
                return self.calcular_similaridade(outro_grafo, metrica="jaccard")
        
        # Métrica desconhecida
        logger.warning(f"Métrica de similaridade desconhecida: {metrica}. Usando similaridade Jaccard.")
        return self.calcular_similaridade(outro_grafo, metrica="jaccard")
    
    def eh_subgrafo(self, outro_grafo: 'Grafo') -> bool:
        """
        Verifica se este grafo é subgrafo de outro grafo.
        
        Args:
            outro_grafo: Outro grafo para comparação.
            
        Returns:
            bool: True se este grafo é subgrafo do outro, False caso contrário.
        """
        # Verifica se todos os vértices deste grafo estão no outro grafo
        for v in self.obter_vertices():
            if not outro_grafo.existe_vertice(v):
                return False
        
        # Verifica se todas as arestas deste grafo estão no outro grafo
        for u, v in self.obter_arestas():
            if not outro_grafo.existe_aresta(u, v):
                return False
        
        return True
    
    def para_networkx(self) -> Union[nx.Graph, nx.DiGraph]:
        """
        Converte o grafo para um objeto NetworkX.
        
        Returns:
            Union[nx.Graph, nx.DiGraph]: Grafo NetworkX correspondente.
        """
        # Cria um grafo NetworkX direcionado ou não direcionado
        if self.eh_direcionado():
            G = nx.DiGraph(name=self.nome)
        else:
            G = nx.Graph(name=self.nome)
        
        # Adiciona os vértices com seus atributos
        for v in self.obter_vertices():
            atributos = self.obter_atributos_vertice(v)
            G.add_node(v, **atributos)
        
        # Adiciona as arestas com seus atributos
        for u, v in self.obter_arestas():
            atributos = self.obter_atributos_aresta(u, v)
            peso = atributos.get("peso", 1.0)
            G.add_edge(u, v, weight=peso, **atributos)
        
        return G
