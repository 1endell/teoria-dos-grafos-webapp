"""
Implementação de grafos bipartidos.

Esta classe estende a classe base Grafo para implementar
funcionalidades específicas de grafos bipartidos.
"""

import networkx as nx
from typing import Dict, List, Any, Optional, Set, Tuple, Union
from core.grafo import Grafo


class GrafoBipartido(Grafo):
    """
    Classe para representação de grafos bipartidos.
    
    Esta classe estende a classe base Grafo para implementar
    funcionalidades específicas de grafos bipartidos, onde os vértices
    podem ser divididos em dois conjuntos disjuntos de forma que
    não existam arestas entre vértices do mesmo conjunto.
    """
    
    def __init__(self, nome: str = "Grafo Bipartido"):
        """
        Inicializa um novo grafo bipartido.
        
        Args:
            nome: Nome do grafo para identificação.
        """
        super().__init__(nome)
        self._conjunto_a = set()  # Primeiro conjunto de vértices
        self._conjunto_b = set()  # Segundo conjunto de vértices
        
    def adicionar_vertice(self, id_vertice: Any, atributos: Optional[Dict[str, Any]] = None, 
                         conjunto: str = 'A') -> bool:
        """
        Adiciona um vértice ao grafo bipartido, especificando o conjunto.
        
        Args:
            id_vertice: Identificador único do vértice.
            atributos: Dicionário de atributos do vértice.
            conjunto: Conjunto ao qual o vértice pertence ('A' ou 'B').
            
        Returns:
            bool: True se o vértice foi adicionado, False se já existia.
            
        Raises:
            ValueError: Se o conjunto especificado não for 'A' ou 'B'.
        """
        if conjunto not in ['A', 'B']:
            raise ValueError("O conjunto deve ser 'A' ou 'B'.")
            
        if id_vertice in self._grafo.nodes:
            return False
            
        # Adiciona o vértice ao grafo
        attrs = atributos or {}
        attrs['conjunto'] = conjunto
        self._grafo.add_node(id_vertice, **attrs)
        
        # Adiciona o vértice ao conjunto correspondente
        if conjunto == 'A':
            self._conjunto_a.add(id_vertice)
        else:
            self._conjunto_b.add(id_vertice)
            
        return True
        
    def adicionar_aresta(self, origem: Any, destino: Any, peso: float = 1.0, 
                        atributos: Optional[Dict[str, Any]] = None) -> bool:
        """
        Adiciona uma aresta ao grafo bipartido.
        
        Args:
            origem: Identificador do vértice de origem.
            destino: Identificador do vértice de destino.
            peso: Peso da aresta.
            atributos: Dicionário de atributos da aresta.
            
        Returns:
            bool: True se a aresta foi adicionada, False se já existia ou se não for válida.
            
        Raises:
            ValueError: Se algum dos vértices não existir no grafo.
            ValueError: Se a aresta violar a propriedade bipartida.
        """
        if origem not in self._grafo.nodes:
            raise ValueError(f"Vértice de origem '{origem}' não existe no grafo.")
        if destino not in self._grafo.nodes:
            raise ValueError(f"Vértice de destino '{destino}' não existe no grafo.")
            
        # Verifica se a aresta viola a propriedade bipartida
        origem_conjunto = self._grafo.nodes[origem].get('conjunto')
        destino_conjunto = self._grafo.nodes[destino].get('conjunto')
        
        if origem_conjunto == destino_conjunto:
            raise ValueError(f"Não é possível adicionar aresta entre vértices do mesmo conjunto ({origem_conjunto}).")
            
        if self._grafo.has_edge(origem, destino):
            return False
            
        attr = atributos or {}
        attr['weight'] = peso
        self._grafo.add_edge(origem, destino, **attr)
        return True
        
    def obter_conjunto_a(self) -> Set[Any]:
        """
        Obtém o conjunto A de vértices.
        
        Returns:
            Set[Any]: Conjunto de identificadores dos vértices do conjunto A.
        """
        return self._conjunto_a.copy()
        
    def obter_conjunto_b(self) -> Set[Any]:
        """
        Obtém o conjunto B de vértices.
        
        Returns:
            Set[Any]: Conjunto de identificadores dos vértices do conjunto B.
        """
        return self._conjunto_b.copy()
        
    def obter_conjunto_vertice(self, id_vertice: Any) -> str:
        """
        Obtém o conjunto ao qual um vértice pertence.
        
        Args:
            id_vertice: Identificador do vértice.
            
        Returns:
            str: 'A' se o vértice pertence ao conjunto A, 'B' se pertence ao conjunto B.
            
        Raises:
            ValueError: Se o vértice não existir no grafo.
        """
        if id_vertice not in self._grafo.nodes:
            raise ValueError(f"Vértice '{id_vertice}' não existe no grafo.")
            
        return self._grafo.nodes[id_vertice].get('conjunto')
        
    def eh_bipartido(self) -> bool:
        """
        Verifica se o grafo é bipartido.
        
        Esta verificação é redundante para esta classe, pois a estrutura
        garante que o grafo seja bipartido, mas é mantida por consistência.
        
        Returns:
            bool: True, pois a estrutura garante que o grafo seja bipartido.
        """
        return True
        
    def verificar_biparticao(self) -> bool:
        """
        Verifica se a bipartição atual é válida.
        
        Returns:
            bool: True se a bipartição for válida, False caso contrário.
        """
        for origem, destino in self._grafo.edges():
            origem_conjunto = self._grafo.nodes[origem].get('conjunto')
            destino_conjunto = self._grafo.nodes[destino].get('conjunto')
            
            if origem_conjunto == destino_conjunto:
                return False
                
        return True
        
    def calcular_biparticao(self) -> Tuple[Set[Any], Set[Any]]:
        """
        Calcula uma bipartição válida para o grafo, se possível.
        
        Esta função é útil para verificar se um grafo genérico é bipartido
        e encontrar uma bipartição válida.
        
        Returns:
            Tuple[Set[Any], Set[Any]]: Tupla contendo os dois conjuntos da bipartição.
            
        Raises:
            ValueError: Se o grafo não for bipartido.
        """
        # Usa o algoritmo de coloração com duas cores para verificar bipartição
        try:
            bipartite_sets = nx.bipartite.sets(self._grafo)
            return bipartite_sets
        except:
            raise ValueError("O grafo não é bipartido.")
            
    def encontrar_emparelhamento_maximo(self) -> Dict[Any, Any]:
        """
        Encontra um emparelhamento máximo no grafo bipartido.
        
        Returns:
            Dict[Any, Any]: Dicionário mapeando vértices do conjunto A para vértices do conjunto B.
        """
        # Usa o algoritmo de emparelhamento máximo do NetworkX
        return nx.bipartite.maximum_matching(self._grafo, self._conjunto_a)
        
    def encontrar_cobertura_minima(self) -> Set[Any]:
        """
        Encontra uma cobertura mínima de vértices no grafo bipartido.
        
        Returns:
            Set[Any]: Conjunto de vértices que formam a cobertura mínima.
        """
        # Usa o algoritmo de cobertura mínima do NetworkX
        return nx.bipartite.minimum_vertex_cover(self._grafo, self._conjunto_a)
        
    def __str__(self) -> str:
        """
        Representação em string do grafo bipartido.
        
        Returns:
            str: Descrição do grafo bipartido.
        """
        return (f"{self.nome} (Bipartido): {self.numero_vertices()} vértices "
                f"({len(self._conjunto_a)} no conjunto A, {len(self._conjunto_b)} no conjunto B), "
                f"{self.numero_arestas()} arestas")
        
    def __repr__(self) -> str:
        """
        Representação oficial do grafo bipartido.
        
        Returns:
            str: Representação do grafo bipartido.
        """
        return f"GrafoBipartido(nome='{self.nome}')"
