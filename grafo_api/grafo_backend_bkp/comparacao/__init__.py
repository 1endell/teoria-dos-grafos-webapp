"""
Módulo de inicialização para comparação de grafos.
"""

from .isomorfismo import (
    verificar_isomorfismo,
    encontrar_mapeamento_isomorfismo,
    verificar_isomorfismo_com_atributos,
    encontrar_automorfismos,
    calcular_invariantes
)

from .similaridade import (
    similaridade_estrutural,
    similaridade_espectral,
    distancia_edicao,
    matriz_similaridade
)

from .subgrafos import (
    verificar_subgrafo,
    verificar_subgrafo_induzido,
    criar_subgrafo_induzido,
    encontrar_subgrafo_isomorfo,
    encontrar_cliques_maximais,
    encontrar_componentes_conexos
)

__all__ = [
    'verificar_isomorfismo',
    'encontrar_mapeamento_isomorfismo',
    'verificar_isomorfismo_com_atributos',
    'encontrar_automorfismos',
    'calcular_invariantes',
    'similaridade_estrutural',
    'similaridade_espectral',
    'distancia_edicao',
    'matriz_similaridade',
    'verificar_subgrafo',
    'verificar_subgrafo_induzido',
    'criar_subgrafo_induzido',
    'encontrar_subgrafo_isomorfo',
    'encontrar_cliques_maximais',
    'encontrar_componentes_conexos'
]
