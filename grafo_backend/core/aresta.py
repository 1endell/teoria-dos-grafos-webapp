"""
Classe para representação de arestas em grafos.
"""

from typing import Dict, Any, Optional, Tuple


class Aresta:
    """
    Classe para representação de arestas em grafos.
    
    Esta classe encapsula a funcionalidade de arestas para garantir
    fidelidade à teoria dos grafos e fornecer uma API consistente.
    """
    
    def __init__(self, origem: Any, destino: Any, peso: float = 1.0, 
                atributos: Optional[Dict[str, Any]] = None, direcionada: bool = False):
        """
        Inicializa uma nova aresta.
        
        Args:
            origem: Identificador do vértice de origem.
            destino: Identificador do vértice de destino.
            peso: Peso da aresta.
            atributos: Dicionário de atributos da aresta.
            direcionada: Indica se a aresta é direcionada.
        """
        self.origem = origem
        self.destino = destino
        self.peso = peso
        self.atributos = atributos or {}
        self.direcionada = direcionada
        
        # Garante que o peso esteja nos atributos
        self.atributos['weight'] = peso
        
    def definir_atributo(self, chave: str, valor: Any) -> None:
        """
        Define um atributo da aresta.
        
        Args:
            chave: Nome do atributo.
            valor: Valor do atributo.
        """
        self.atributos[chave] = valor
        
        # Atualiza o peso se o atributo for 'weight'
        if chave == 'weight':
            self.peso = float(valor)
        
    def obter_atributo(self, chave: str, padrao: Any = None) -> Any:
        """
        Obtém um atributo da aresta.
        
        Args:
            chave: Nome do atributo.
            padrao: Valor padrão caso o atributo não exista.
            
        Returns:
            Any: Valor do atributo ou valor padrão.
        """
        return self.atributos.get(chave, padrao)
        
    def remover_atributo(self, chave: str) -> bool:
        """
        Remove um atributo da aresta.
        
        Args:
            chave: Nome do atributo.
            
        Returns:
            bool: True se o atributo foi removido, False se não existia.
            
        Raises:
            ValueError: Se tentar remover o atributo 'weight'.
        """
        if chave == 'weight':
            raise ValueError("Não é possível remover o atributo 'weight' de uma aresta.")
            
        if chave in self.atributos:
            del self.atributos[chave]
            return True
        return False
        
    def definir_peso(self, peso: float) -> None:
        """
        Define o peso da aresta.
        
        Args:
            peso: Novo peso da aresta.
        """
        self.peso = peso
        self.atributos['weight'] = peso
        
    def obter_peso(self) -> float:
        """
        Obtém o peso da aresta.
        
        Returns:
            float: Peso da aresta.
        """
        return self.peso
        
    def listar_atributos(self) -> Dict[str, Any]:
        """
        Lista todos os atributos da aresta.
        
        Returns:
            Dict[str, Any]: Dicionário de atributos.
        """
        return self.atributos.copy()
        
    def obter_vertices(self) -> Tuple[Any, Any]:
        """
        Obtém os vértices da aresta.
        
        Returns:
            Tuple[Any, Any]: Tupla (origem, destino).
        """
        return (self.origem, self.destino)
        
    def inverter(self) -> None:
        """
        Inverte a direção da aresta.
        
        Raises:
            ValueError: Se a aresta não for direcionada.
        """
        if not self.direcionada:
            raise ValueError("Não é possível inverter uma aresta não direcionada.")
            
        self.origem, self.destino = self.destino, self.origem
        
    def __eq__(self, outro: object) -> bool:
        """
        Verifica se duas arestas são iguais.
        
        Args:
            outro: Outra aresta para comparação.
            
        Returns:
            bool: True se as arestas forem iguais, False caso contrário.
        """
        if not isinstance(outro, Aresta):
            return False
            
        if self.direcionada:
            return (self.origem == outro.origem and 
                    self.destino == outro.destino and 
                    self.direcionada == outro.direcionada)
        else:
            # Para arestas não direcionadas, a ordem dos vértices não importa
            return ((self.origem == outro.origem and self.destino == outro.destino) or
                    (self.origem == outro.destino and self.destino == outro.origem)) and \
                   self.direcionada == outro.direcionada
        
    def __hash__(self) -> int:
        """
        Calcula o hash da aresta.
        
        Returns:
            int: Hash da aresta.
        """
        if self.direcionada:
            return hash((self.origem, self.destino, self.direcionada))
        else:
            # Para arestas não direcionadas, a ordem dos vértices não importa
            return hash(frozenset([self.origem, self.destino]))
        
    def __str__(self) -> str:
        """
        Representação em string da aresta.
        
        Returns:
            str: Descrição da aresta.
        """
        if self.direcionada:
            return f"Aresta direcionada ({self.origem} -> {self.destino}, peso={self.peso})"
        else:
            return f"Aresta ({self.origem} -- {self.destino}, peso={self.peso})"
        
    def __repr__(self) -> str:
        """
        Representação oficial da aresta.
        
        Returns:
            str: Representação da aresta.
        """
        return (f"Aresta(origem={repr(self.origem)}, destino={repr(self.destino)}, "
                f"peso={self.peso}, direcionada={self.direcionada})")
