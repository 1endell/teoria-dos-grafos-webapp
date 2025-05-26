"""
Classe base para representação de grafos.
Implementa a interface comum para todos os tipos de grafos.
"""

import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, List, Any, Optional, Set, Tuple, Union


class Grafo:
    """
    Classe base para representação de grafos.
    
    Esta classe encapsula a funcionalidade do NetworkX para garantir
    fidelidade à teoria dos grafos e fornecer uma API consistente.
    """
    
    def __init__(self, nome: str = "Grafo", direcionado: bool = False):
        """
        Inicializa um novo grafo.
        
        Args:
            nome: Nome do grafo para identificação.
            direcionado: Se True, cria um grafo direcionado. Se False, cria um grafo não direcionado.
        """
        self.nome = nome
        if direcionado:
            self._grafo = nx.DiGraph()  # Grafo direcionado
        else:
            self._grafo = nx.Graph()  # Grafo não direcionado
        
    def adicionar_vertice(self, id_vertice: Any, atributos: Optional[Dict[str, Any]] = None) -> bool:
        """
        Adiciona um vértice ao grafo.
        
        Args:
            id_vertice: Identificador único do vértice.
            atributos: Dicionário de atributos do vértice.
            
        Returns:
            bool: True se o vértice foi adicionado, False se já existia.
        """
        if id_vertice in self._grafo.nodes:
            return False
            
        self._grafo.add_node(id_vertice, **(atributos or {}))
        return True
        
    def adicionar_aresta(self, origem: Any, destino: Any, peso: float = 1.0, 
                        atributos: Optional[Dict[str, Any]] = None) -> bool:
        """
        Adiciona uma aresta ao grafo.
        
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
        if origem not in self._grafo.nodes:
            raise ValueError(f"Vértice de origem \'{origem}\' não existe no grafo.")
        if destino not in self._grafo.nodes:
            raise ValueError(f"Vértice de destino \'{destino}\' não existe no grafo.")
            
        if self._grafo.has_edge(origem, destino):
            return False
            
        attr = atributos or {}
        attr["weight"] = peso
        self._grafo.add_edge(origem, destino, **attr)
        return True
        
    def remover_vertice(self, id_vertice: Any) -> bool:
        """
        Remove um vértice do grafo.
        
        Args:
            id_vertice: Identificador do vértice a ser removido.
            
        Returns:
            bool: True se o vértice foi removido, False se não existia.
        """
        if id_vertice not in self._grafo.nodes:
            return False
            
        self._grafo.remove_node(id_vertice)
        return True
        
    def remover_aresta(self, origem: Any, destino: Any) -> bool:
        """
        Remove uma aresta do grafo.
        
        Args:
            origem: Identificador do vértice de origem.
            destino: Identificador do vértice de destino.
            
        Returns:
            bool: True se a aresta foi removida, False se não existia.
        """
        if not self._grafo.has_edge(origem, destino):
            return False
            
        self._grafo.remove_edge(origem, destino)
        return True
        
    def obter_vertices(self) -> List[Any]:
        """
        Obtém a lista de vértices do grafo.
        
        Returns:
            List[Any]: Lista de identificadores dos vértices.
        """
        return list(self._grafo.nodes)
        
    def obter_arestas(self) -> List[Tuple[Any, Any, Dict[str, Any]]]:
        """
        Obtém a lista de arestas do grafo.
        
        Returns:
            List[Tuple[Any, Any, Dict[str, Any]]]: Lista de tuplas (origem, destino, atributos).
        """
        return [(u, v, self._grafo.edges[u, v]) for u, v in self._grafo.edges]
        
    def obter_atributos_vertice(self, id_vertice: Any) -> Dict[str, Any]:
        """
        Obtém os atributos de um vértice.
        
        Args:
            id_vertice: Identificador do vértice.
            
        Returns:
            Dict[str, Any]: Dicionário de atributos do vértice.
            
        Raises:
            ValueError: Se o vértice não existir no grafo.
        """
        if id_vertice not in self._grafo.nodes:
            raise ValueError(f"Vértice \'{id_vertice}\' não existe no grafo.")
            
        return dict(self._grafo.nodes[id_vertice])

    def definir_atributos_vertice(self, id_vertice: Any, atributos: Dict[str, Any]) -> None:
        """
        Define os atributos de um vértice.

        Args:
            id_vertice: Identificador do vértice.
            atributos: Dicionário de atributos a serem definidos.

        Raises:
            ValueError: Se o vértice não existir no grafo.
        """
        if id_vertice not in self._grafo.nodes:
            raise ValueError(f"Vértice \'{id_vertice}\' não existe no grafo.")

        # Atualiza os atributos existentes com os novos
        self._grafo.nodes[id_vertice].update(atributos)
        
    def obter_atributos_aresta(self, origem: Any, destino: Any) -> Dict[str, Any]:
        """
        Obtém os atributos de uma aresta.
        
        Args:
            origem: Identificador do vértice de origem.
            destino: Identificador do vértice de destino.
            
        Returns:
            Dict[str, Any]: Dicionário de atributos da aresta.
            
        Raises:
            ValueError: Se a aresta não existir no grafo.
        """
        if not self._grafo.has_edge(origem, destino):
            raise ValueError(f"Aresta ({origem}, {destino}) não existe no grafo.")
            
        return dict(self._grafo.edges[origem, destino])

    def definir_atributos_aresta(self, origem: Any, destino: Any, atributos: Dict[str, Any]) -> None:
        """
        Define os atributos de uma aresta.

        Args:
            origem: Identificador do vértice de origem.
            destino: Identificador do vértice de destino.
            atributos: Dicionário de atributos a serem definidos.

        Raises:
            ValueError: Se a aresta não existir no grafo.
        """
        if not self._grafo.has_edge(origem, destino):
            raise ValueError(f"Aresta ({origem}, {destino}) não existe no grafo.")

        # Atualiza os atributos existentes com os novos
        self._grafo.edges[origem, destino].update(atributos)
        
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
            
        return self._grafo.edges[origem, destino].get("weight", 1.0)

    def definir_peso_aresta(self, origem: Any, destino: Any, peso: float) -> None:
        """
        Define o peso de uma aresta.

        Args:
            origem: Identificador do vértice de origem.
            destino: Identificador do vértice de destino.
            peso: Novo peso da aresta.

        Raises:
            ValueError: Se a aresta não existir no grafo.
        """
        if not self._grafo.has_edge(origem, destino):
            raise ValueError(f"Aresta ({origem}, {destino}) não existe no grafo.")

        self._grafo.edges[origem, destino]["weight"] = peso
        
    def obter_adjacentes(self, id_vertice: Any) -> List[Any]:
        """
        Obtém a lista de vértices adjacentes a um vértice.
        
        Args:
            id_vertice: Identificador do vértice.
            
        Returns:
            List[Any]: Lista de identificadores dos vértices adjacentes.
            
        Raises:
            ValueError: Se o vértice não existir no grafo.
        """
        if id_vertice not in self._grafo.nodes:
            raise ValueError(f"Vértice \'{id_vertice}\' não existe no grafo.")
            
        return list(self._grafo.neighbors(id_vertice))
    
    def obter_vizinhos(self, id_vertice: Any) -> List[Any]:
        """
        Obtém a lista de vértices vizinhos a um vértice (alias para obter_adjacentes).
        Método necessário para compatibilidade com algoritmos de caminhos.
        
        Args:
            id_vertice: Identificador do vértice.
            
        Returns:
            List[Any]: Lista de identificadores dos vértices vizinhos.
            
        Raises:
            ValueError: Se o vértice não existir no grafo.
        """
        return self.obter_adjacentes(id_vertice)
        
    def obter_grau(self, id_vertice: Any) -> int:
        """
        Obtém o grau de um vértice.
        
        Args:
            id_vertice: Identificador do vértice.
            
        Returns:
            int: Grau do vértice.
            
        Raises:
            ValueError: Se o vértice não existir no grafo.
        """
        if id_vertice not in self._grafo.nodes:
            raise ValueError(f"Vértice \'{id_vertice}\' não existe no grafo.")
            
        return self._grafo.degree(id_vertice)

    def calcular_grau(self, id_vertice: Any) -> int:
        """
        Calcula o grau de um vértice (alias para obter_grau).

        Args:
            id_vertice: Identificador do vértice.

        Returns:
            int: Grau do vértice.

        Raises:
            ValueError: Se o vértice não existir no grafo.
        """
        return self.obter_grau(id_vertice)
        
    def existe_vertice(self, id_vertice: Any) -> bool:
        """
        Verifica se um vértice existe no grafo.
        
        Args:
            id_vertice: Identificador do vértice.
            
        Returns:
            bool: True se o vértice existir, False caso contrário.
        """
        return id_vertice in self._grafo.nodes
        
    def existe_aresta(self, origem: Any, destino: Any) -> bool:
        """
        Verifica se uma aresta existe no grafo.
        
        Args:
            origem: Identificador do vértice de origem.
            destino: Identificador do vértice de destino.
            
        Returns:
            bool: True se a aresta existir, False caso contrário.
        """
        return self._grafo.has_edge(origem, destino)
        
    def numero_vertices(self) -> int:
        """
        Obtém o número de vértices do grafo.
        
        Returns:
            int: Número de vértices.
        """
        return self._grafo.number_of_nodes()
        
    def numero_arestas(self) -> int:
        """
        Obtém o número de arestas do grafo.
        
        Returns:
            int: Número de arestas.
        """
        return self._grafo.number_of_edges()
        
    def eh_vazio(self) -> bool:
        """
        Verifica se o grafo é vazio (sem vértices).
        
        Returns:
            bool: True se o grafo for vazio, False caso contrário.
        """
        return self.numero_vertices() == 0
        
    def eh_trivial(self) -> bool:
        """
        Verifica se o grafo é trivial (apenas um vértice).
        
        Returns:
            bool: True se o grafo for trivial, False caso contrário.
        """
        return self.numero_vertices() == 1
        
    def eh_conexo(self) -> bool:
        """
        Verifica se o grafo é conexo.
        
        Returns:
            bool: True se o grafo for conexo, False caso contrário.
        """
        if self.eh_vazio():
            return True
        # Para grafos direcionados, verifica conectividade forte ou fraca
        if self.eh_direcionado():
            return nx.is_weakly_connected(self._grafo)
        return nx.is_connected(self._grafo)
        
    def eh_direcionado(self) -> bool:
        """
        Verifica se o grafo é direcionado.
        
        Returns:
            bool: True se o grafo for direcionado, False caso contrário.
        """
        return isinstance(self._grafo, nx.DiGraph)
        
    def visualizar(self, titulo: Optional[str] = None, 
                  layout: str = "spring", 
                  tamanho_figura: Tuple[int, int] = (10, 8),
                  mostrar: bool = True,
                  salvar_como: Optional[str] = None) -> None:
        """
        Visualiza o grafo utilizando matplotlib.
        
        Args:
            titulo: Título do gráfico.
            layout: Tipo de layout para visualização ("spring", "circular", "random", "shell", "kamada_kawai", "spectral").
            tamanho_figura: Tamanho da figura (largura, altura).
            mostrar: Se True, exibe a figura. Se False, apenas cria a figura sem exibir.
            salvar_como: Caminho para salvar a figura. Se None, não salva.
        """
        plt.figure(figsize=tamanho_figura)
        
        # Seleciona o layout
        if layout == "spring":
            pos = nx.spring_layout(self._grafo)
        elif layout == "circular":
            pos = nx.circular_layout(self._grafo)
        elif layout == "random":
            pos = nx.random_layout(self._grafo)
        elif layout == "shell":
            pos = nx.shell_layout(self._grafo)
        elif layout == "kamada_kawai":
            pos = nx.kamada_kawai_layout(self._grafo)
        elif layout == "spectral":
            pos = nx.spectral_layout(self._grafo)
        else:
            pos = nx.spring_layout(self._grafo)
            
        # Obtém pesos das arestas para visualização
        edge_weights = [self._grafo[u][v].get("weight", 1.0) for u, v in self._grafo.edges()]
        
        # Desenha o grafo
        nx.draw_networkx_nodes(self._grafo, pos, node_size=500, node_color="lightblue")
        
        # Desenha as arestas com setas se for direcionado
        if self.eh_direcionado():
            nx.draw_networkx_edges(self._grafo, pos, width=edge_weights, alpha=0.7, 
                                  arrowstyle="->", arrowsize=15)
        else:
            nx.draw_networkx_edges(self._grafo, pos, width=edge_weights, alpha=0.7)
            
        nx.draw_networkx_labels(self._grafo, pos, font_size=12)
        
        # Adiciona rótulos de peso nas arestas
        # Corrigido: Usar aspas simples dentro da f-string
        edge_labels = {(u, v): f"{self._grafo[u][v].get('weight', 1.0):.1f}" 
                      for u, v in self._grafo.edges()}
        nx.draw_networkx_edge_labels(self._grafo, pos, edge_labels=edge_labels)
        
        # Configura o título
        if titulo:
            plt.title(titulo)
        else:
            plt.title(self.nome)
            
        plt.axis("off")
        
        # Salva a figura se solicitado
        if salvar_como:
            plt.savefig(salvar_como, bbox_inches="tight")
            
        # Exibe a figura se solicitado
        if mostrar:
            plt.show()
        else:
            plt.close()
            
    def obter_grafo_networkx(self) -> Union[nx.Graph, nx.DiGraph]:
        """
        Obtém o objeto NetworkX subjacente.
        
        Returns:
            Union[nx.Graph, nx.DiGraph]: Objeto NetworkX representando o grafo.
        """
        return self._grafo
        
    def definir_grafo_networkx(self, grafo: Union[nx.Graph, nx.DiGraph]) -> None:
        """
        Define o objeto NetworkX subjacente.
        
        Args:
            grafo: Objeto NetworkX a ser utilizado.
        """
        self._grafo = grafo
        
    def __str__(self) -> str:
        """
        Representação em string do grafo.
        
        Returns:
            str: Descrição do grafo.
        """
        tipo = "direcionado" if self.eh_direcionado() else "não direcionado"
        return f"{self.nome}: {self.numero_vertices()} vértices, {self.numero_arestas()} arestas, {tipo}"
        
    def __repr__(self) -> str:
        """
        Representação oficial do grafo.
        
        Returns:
            str: Representação do grafo.
        """
        return f"Grafo(nome='{self.nome}', direcionado={self.eh_direcionado()})"
