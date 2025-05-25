"""
Implementação de grafos ponderados.

Esta classe estende a classe base Grafo para implementar
funcionalidades específicas de grafos ponderados.
"""

import networkx as nx
from typing import Dict, List, Any, Optional, Set, Tuple, Union
from ..core.grafo import Grafo


class GrafoPonderado(Grafo):
    """
    Classe para representação de grafos ponderados.
    
    Esta classe estende a classe base Grafo para implementar
    funcionalidades específicas de grafos ponderados, onde as arestas
    possuem pesos associados.
    """
    
    def __init__(self, nome: str = "Grafo Ponderado", direcionado: bool = False):
        """
        Inicializa um novo grafo ponderado.
        
        Args:
            nome: Nome do grafo para identificação.
            direcionado: Indica se o grafo é direcionado.
        """
        super().__init__(nome)
        if direcionado:
            self._grafo = nx.DiGraph()
        else:
            self._grafo = nx.Graph()
        self.direcionado = direcionado
        
    def adicionar_aresta(self, origem: Any, destino: Any, peso: float = 1.0, 
                        atributos: Optional[Dict[str, Any]] = None) -> bool:
        """
        Adiciona uma aresta ponderada ao grafo.
        
        Args:
            origem: Identificador do vértice de origem.
            destino: Identificador do vértice de destino.
            peso: Peso da aresta.
            atributos: Dicionário de atributos da aresta.
            
        Returns:
            bool: True se a aresta foi adicionada, False se já existia.
            
        Raises:
            ValueError: Se algum dos vértices não existir no grafo.
            ValueError: Se o peso for negativo e não for permitido.
        """
        if origem not in self._grafo.nodes:
            raise ValueError(f"Vértice de origem '{origem}' não existe no grafo.")
        if destino not in self._grafo.nodes:
            raise ValueError(f"Vértice de destino '{destino}' não existe no grafo.")
            
        if self._grafo.has_edge(origem, destino):
            return False
            
        attr = atributos or {}
        attr['weight'] = peso
        self._grafo.add_edge(origem, destino, **attr)
        return True
        
    def definir_peso_aresta(self, origem: Any, destino: Any, peso: float) -> bool:
        """
        Define o peso de uma aresta existente.
        
        Args:
            origem: Identificador do vértice de origem.
            destino: Identificador do vértice de destino.
            peso: Novo peso da aresta.
            
        Returns:
            bool: True se o peso foi definido, False se a aresta não existir.
            
        Raises:
            ValueError: Se o peso for negativo e não for permitido.
        """
        if not self._grafo.has_edge(origem, destino):
            return False
            
        self._grafo[origem][destino]['weight'] = peso
        return True
        
    def obter_peso_aresta(self, origem: Any, destino: Any) -> float:
        """
        Obtém o peso de uma aresta.
        
        Args:
            origem: Identificador do vértice de origem.
            destino: Identificador do vértice de destino.
            
        Returns:
            float: Peso da aresta.
            
        Raises:
            ValueError: Se a aresta não existir no grafo.
        """
        if not self._grafo.has_edge(origem, destino):
            raise ValueError(f"Aresta ({origem}, {destino}) não existe no grafo.")
            
        return self._grafo[origem][destino].get('weight', 1.0)
        
    def obter_arestas_ordenadas_por_peso(self, crescente: bool = True) -> List[Tuple[Any, Any, float]]:
        """
        Obtém a lista de arestas ordenadas por peso.
        
        Args:
            crescente: Se True, ordena em ordem crescente de peso, caso contrário, em ordem decrescente.
            
        Returns:
            List[Tuple[Any, Any, float]]: Lista de tuplas (origem, destino, peso) ordenadas por peso.
        """
        arestas = []
        for origem, destino, atributos in self._grafo.edges(data=True):
            peso = atributos.get('weight', 1.0)
            arestas.append((origem, destino, peso))
            
        return sorted(arestas, key=lambda x: x[2], reverse=not crescente)
        
    def calcular_peso_total(self) -> float:
        """
        Calcula a soma dos pesos de todas as arestas do grafo.
        
        Returns:
            float: Soma dos pesos de todas as arestas.
        """
        return sum(atributos.get('weight', 1.0) for _, _, atributos in self._grafo.edges(data=True))
        
    def obter_arestas_com_peso_minimo(self) -> List[Tuple[Any, Any, float]]:
        """
        Obtém a lista de arestas com peso mínimo.
        
        Returns:
            List[Tuple[Any, Any, float]]: Lista de tuplas (origem, destino, peso) com peso mínimo.
        """
        if self.numero_arestas() == 0:
            return []
            
        arestas = self.obter_arestas_ordenadas_por_peso(crescente=True)
        peso_minimo = arestas[0][2]
        
        return [(origem, destino, peso) for origem, destino, peso in arestas if peso == peso_minimo]
        
    def obter_arestas_com_peso_maximo(self) -> List[Tuple[Any, Any, float]]:
        """
        Obtém a lista de arestas com peso máximo.
        
        Returns:
            List[Tuple[Any, Any, float]]: Lista de tuplas (origem, destino, peso) com peso máximo.
        """
        if self.numero_arestas() == 0:
            return []
            
        arestas = self.obter_arestas_ordenadas_por_peso(crescente=False)
        peso_maximo = arestas[0][2]
        
        return [(origem, destino, peso) for origem, destino, peso in arestas if peso == peso_maximo]
        
    def eh_direcionado(self) -> bool:
        """
        Verifica se o grafo é direcionado.
        
        Returns:
            bool: True se o grafo for direcionado, False caso contrário.
        """
        return self.direcionado
        
    def __str__(self) -> str:
        """
        Representação em string do grafo ponderado.
        
        Returns:
            str: Descrição do grafo ponderado.
        """
        tipo = "Direcionado" if self.direcionado else "Não Direcionado"
        return f"{self.nome} (Ponderado, {tipo}): {self.numero_vertices()} vértices, {self.numero_arestas()} arestas"
        
    def __repr__(self) -> str:
        """
        Representação oficial do grafo ponderado.
        
        Returns:
            str: Representação do grafo ponderado.
        """
        return f"GrafoPonderado(nome='{self.nome}', direcionado={self.direcionado})"
