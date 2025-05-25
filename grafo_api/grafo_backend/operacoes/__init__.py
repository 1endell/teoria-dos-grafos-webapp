"""
Módulo de inicialização para operações entre grafos.
"""

from .combinacao import (
    uniao_grafos, 
    intersecao_grafos, 
    diferenca_grafos, 
    diferenca_simetrica_grafos,
    composicao_grafos
)

__all__ = [
    'uniao_grafos', 
    'intersecao_grafos', 
    'diferenca_grafos', 
    'diferenca_simetrica_grafos',
    'composicao_grafos'
]
