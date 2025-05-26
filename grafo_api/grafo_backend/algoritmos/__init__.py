"""
Módulo de algoritmos.

Este módulo contém implementações de diversos algoritmos para grafos,
organizados por categorias.
"""

# Importações de algoritmos de caminhos
from grafo_backend.algoritmos.caminhos.dijkstra import dijkstra

# Importações de algoritmos de coloração
from grafo_backend.algoritmos.coloracao.coloracao import (
    coloracao_gulosa,
    coloracao_welsh_powell,
    coloracao_dsatur,
    coloracao_arestas,
    calcular_numero_cromatico_aproximado
)

# Importações de algoritmos de centralidade
from grafo_backend.algoritmos.centralidade.centralidade import (
    centralidade_grau,
    centralidade_intermediacao,
    centralidade_proximidade,
    centralidade_autovetor,
    pagerank,
    centralidade_katz
)

# Exporta todas as funções para o namespace do pacote
__all__ = [
    # Algoritmos de caminhos
    'dijkstra',
    
    # Algoritmos de coloração
    'coloracao_gulosa',
    'coloracao_welsh_powell',
    'coloracao_dsatur',
    'coloracao_arestas',
    'calcular_numero_cromatico_aproximado',
    
    # Algoritmos de centralidade
    'centralidade_grau',
    'centralidade_intermediacao',
    'centralidade_proximidade',
    'centralidade_autovetor',
    'pagerank',
    'centralidade_katz'
]
