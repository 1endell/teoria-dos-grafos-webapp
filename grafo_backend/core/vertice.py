"""
Classe para representação de vértices em grafos.
"""

from typing import Dict, Any, Optional


class Vertice:
    """
    Classe para representação de vértices em grafos.
    
    Esta classe encapsula a funcionalidade de vértices para garantir
    fidelidade à teoria dos grafos e fornecer uma API consistente.
    """
    
    def __init__(self, id_vertice: Any, atributos: Optional[Dict[str, Any]] = None):
        """
        Inicializa um novo vértice.
        
        Args:
            id_vertice: Identificador único do vértice.
            atributos: Dicionário de atributos do vértice.
        """
        self.id = id_vertice
        self.atributos = atributos or {}
        
    def definir_atributo(self, chave: str, valor: Any) -> None:
        """
        Define um atributo do vértice.
        
        Args:
            chave: Nome do atributo.
            valor: Valor do atributo.
        """
        self.atributos[chave] = valor
        
    def obter_atributo(self, chave: str, padrao: Any = None) -> Any:
        """
        Obtém um atributo do vértice.
        
        Args:
            chave: Nome do atributo.
            padrao: Valor padrão caso o atributo não exista.
            
        Returns:
            Any: Valor do atributo ou valor padrão.
        """
        return self.atributos.get(chave, padrao)
        
    def remover_atributo(self, chave: str) -> bool:
        """
        Remove um atributo do vértice.
        
        Args:
            chave: Nome do atributo.
            
        Returns:
            bool: True se o atributo foi removido, False se não existia.
        """
        if chave in self.atributos:
            del self.atributos[chave]
            return True
        return False
        
    def listar_atributos(self) -> Dict[str, Any]:
        """
        Lista todos os atributos do vértice.
        
        Returns:
            Dict[str, Any]: Dicionário de atributos.
        """
        return self.atributos.copy()
        
    def __eq__(self, outro: object) -> bool:
        """
        Verifica se dois vértices são iguais.
        
        Args:
            outro: Outro vértice para comparação.
            
        Returns:
            bool: True se os vértices forem iguais, False caso contrário.
        """
        if not isinstance(outro, Vertice):
            return False
        return self.id == outro.id
        
    def __hash__(self) -> int:
        """
        Calcula o hash do vértice.
        
        Returns:
            int: Hash do vértice.
        """
        return hash(self.id)
        
    def __str__(self) -> str:
        """
        Representação em string do vértice.
        
        Returns:
            str: Descrição do vértice.
        """
        return f"Vértice {self.id}"
        
    def __repr__(self) -> str:
        """
        Representação oficial do vértice.
        
        Returns:
            str: Representação do vértice.
        """
        return f"Vertice(id={repr(self.id)}, atributos={repr(self.atributos)})"
