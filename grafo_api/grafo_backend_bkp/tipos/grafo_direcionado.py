"""
Implementação de tipos específicos de grafos.
"""

from ..core import Grafo
import networkx as nx
from typing import Dict, List, Any, Optional, Set, Tuple, Union


class GrafoDirecionado(Grafo):
    """
    Classe para representação de grafos direcionados.
    
    Esta classe estende a classe base Grafo para implementar
    funcionalidades específicas de grafos direcionados.
    """
    
    def __init__(self, nome: str = "Grafo Direcionado"):
        """
        Inicializa um novo grafo direcionado.
        
        Args:
            nome: Nome do grafo para identificação.
        """
        super().__init__(nome)
        self._grafo = nx.DiGraph()  # Grafo direcionado
        
    def adicionar_aresta(self, origem: Any, destino: Any, peso: float = 1.0, 
                        atributos: Optional[Dict[str, Any]] = None) -> bool:
        """
        Adiciona uma aresta direcionada ao grafo.
        
        Args:
            origem: Identificador do vértice de origem.
            destino: Identificador do vértice de destino.
            peso: Peso da aresta.
            atributos: Dicionário de atributos da aresta.
            
        Returns:
            bool: True se a aresta foi adicionada, False se já existia.
            
        Raises:
            ValueError: Se algum dos vértices não existir no grafo.
        """
        return super().adicionar_aresta(origem, destino, peso, atributos)
        
    def obter_grau_entrada(self, id_vertice: Any) -> int:
        """
        Obtém o grau de entrada de um vértice.
        
        Args:
            id_vertice: Identificador do vértice.
            
        Returns:
            int: Grau de entrada do vértice.
            
        Raises:
            ValueError: Se o vértice não existir no grafo.
        """
        if id_vertice not in self._grafo.nodes:
            raise ValueError(f"Vértice '{id_vertice}' não existe no grafo.")
            
        return self._grafo.in_degree(id_vertice)
        
    def obter_grau_saida(self, id_vertice: Any) -> int:
        """
        Obtém o grau de saída de um vértice.
        
        Args:
            id_vertice: Identificador do vértice.
            
        Returns:
            int: Grau de saída do vértice.
            
        Raises:
            ValueError: Se o vértice não existir no grafo.
        """
        if id_vertice not in self._grafo.nodes:
            raise ValueError(f"Vértice '{id_vertice}' não existe no grafo.")
            
        return self._grafo.out_degree(id_vertice)
        
    def obter_predecessores(self, id_vertice: Any) -> List[Any]:
        """
        Obtém a lista de vértices predecessores de um vértice.
        
        Args:
            id_vertice: Identificador do vértice.
            
        Returns:
            List[Any]: Lista de identificadores dos vértices predecessores.
            
        Raises:
            ValueError: Se o vértice não existir no grafo.
        """
        if id_vertice not in self._grafo.nodes:
            raise ValueError(f"Vértice '{id_vertice}' não existe no grafo.")
            
        return list(self._grafo.predecessors(id_vertice))
        
    def obter_sucessores(self, id_vertice: Any) -> List[Any]:
        """
        Obtém a lista de vértices sucessores de um vértice.
        
        Args:
            id_vertice: Identificador do vértice.
            
        Returns:
            List[Any]: Lista de identificadores dos vértices sucessores.
            
        Raises:
            ValueError: Se o vértice não existir no grafo.
        """
        if id_vertice not in self._grafo.nodes:
            raise ValueError(f"Vértice '{id_vertice}' não existe no grafo.")
            
        return list(self._grafo.successors(id_vertice))
        
    def eh_fortemente_conexo(self) -> bool:
        """
        Verifica se o grafo é fortemente conexo.
        
        Returns:
            bool: True se o grafo for fortemente conexo, False caso contrário.
        """
        if self.eh_vazio():
            return True
        return nx.is_strongly_connected(self._grafo)
        
    def eh_fracamente_conexo(self) -> bool:
        """
        Verifica se o grafo é fracamente conexo.
        
        Returns:
            bool: True se o grafo for fracamente conexo, False caso contrário.
        """
        if self.eh_vazio():
            return True
        return nx.is_weakly_connected(self._grafo)
        
    def obter_componentes_fortemente_conexos(self) -> List[Set[Any]]:
        """
        Obtém os componentes fortemente conexos do grafo.
        
        Returns:
            List[Set[Any]]: Lista de conjuntos de vértices, onde cada conjunto
                           representa um componente fortemente conexo.
        """
        return list(nx.strongly_connected_components(self._grafo))
        
    def obter_componentes_fracamente_conexos(self) -> List[Set[Any]]:
        """
        Obtém os componentes fracamente conexos do grafo.
        
        Returns:
            List[Set[Any]]: Lista de conjuntos de vértices, onde cada conjunto
                           representa um componente fracamente conexo.
        """
        return list(nx.weakly_connected_components(self._grafo))
        
    def __str__(self) -> str:
        """
        Representação em string do grafo direcionado.
        
        Returns:
            str: Descrição do grafo direcionado.
        """
        return f"{self.nome} (Direcionado): {self.numero_vertices()} vértices, {self.numero_arestas()} arestas"
        
    def __repr__(self) -> str:
        """
        Representação oficial do grafo direcionado.
        
        Returns:
            str: Representação do grafo direcionado.
        """
        return f"GrafoDirecionado(nome='{self.nome}')"
