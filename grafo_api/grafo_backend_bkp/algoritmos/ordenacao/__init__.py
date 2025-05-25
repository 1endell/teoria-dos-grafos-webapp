"""
Módulo de algoritmos de ordenação topológica em grafos.

Este módulo contém implementações de algoritmos para encontrar ordenações
topológicas em grafos direcionados acíclicos (DAGs), como o algoritmo de Kahn.
"""

from algoritmos.ordenacao.kahn import kahn, verificar_ordenacao_topologica, encontrar_caminho_critico
