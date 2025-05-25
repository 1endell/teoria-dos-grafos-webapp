# Análise de Algoritmos Implementados e Faltantes

## Algoritmos Solicitados pelo Usuário

Abaixo está a análise detalhada dos algoritmos solicitados pelo usuário, indicando quais já estão implementados e quais precisam ser adicionados.

| Algoritmo | Status | Localização | Observações |
|-----------|--------|-------------|-------------|
| Breadth-First Search (BFS) | ❌ Não implementado | - | Usado implicitamente em alguns algoritmos, mas não como função independente |
| Depth-First Search (DFS) | ❌ Não implementado | - | Usado implicitamente em alguns algoritmos, mas não como função independente |
| Iterative Deepening DFS (IDDFS) | ❌ Não implementado | - | - |
| Dijkstra | ✅ Implementado | `/algoritmos/caminhos/dijkstra.py` | Implementação completa com reconstrução de caminho |
| Bellman-Ford | ❌ Não implementado | - | Necessário para grafos com arestas de peso negativo |
| Floyd-Warshall | ❌ Não implementado | - | Algoritmo para todos os pares de caminhos mínimos |
| A* Algorithm | ❌ Não implementado | - | - |
| Prim | ❌ Não implementado | - | Algoritmo alternativo para árvore geradora mínima |
| Kruskal | ✅ Implementado | `/algoritmos/arvores/kruskal.py` | Implementação completa com Union-Find |
| Tarjan | ❌ Não implementado | - | Algoritmo para componentes fortemente conexos |
| Union-Find (Disjoint Set Union) | ✅ Implementado | `/algoritmos/arvores/kruskal.py` | Implementado como classe auxiliar no arquivo do Kruskal |
| Algoritmo para Pontes e Articulações | ❌ Não implementado | - | - |
| Ford-Fulkerson | ✅ Implementado | `/algoritmos/fluxo/ford_fulkerson.py` | Implementação completa com BFS para caminhos de aumento |
| Edmonds-Karp | ❌ Não implementado | - | Variante do Ford-Fulkerson que usa BFS |
| Dinic's Algorithm | ❌ Não implementado | - | Algoritmo avançado para fluxo máximo |
| Hopcroft-Karp | ❌ Não implementado | - | Algoritmo para emparelhamento máximo em grafos bipartidos |
| Hungarian Algorithm | ❌ Não implementado | - | Algoritmo para atribuição ótima |
| Kahn's Algorithm | ❌ Não implementado | - | Algoritmo para ordenação topológica |
| Hierholzer | ❌ Não implementado | - | Algoritmo para ciclo euleriano |
| Algoritmos para Hamiltonianos | ❌ Não implementado | - | - |
| Algoritmo Greedy | ✅ Implementado | `/algoritmos/coloracao/coloracao.py` | Implementado para coloração de grafos |
| Backtracking | ❌ Não implementado | - | - |
| Ullmann Algorithm | ❌ Não implementado | - | Algoritmo para isomorfismo de subgrafos |
| Hopcroft-Tarjan | ❌ Não implementado | - | Algoritmo para planaridade |
| PageRank | ✅ Implementado | `/algoritmos/centralidade/centralidade.py` | Implementação completa |
| Betweenness Centrality (Brandes) | ✅ Implementado | `/algoritmos/centralidade/centralidade.py` | Implementado como `centralidade_intermediacao` |
| Christofides | ❌ Não implementado | - | Algoritmo para o problema do caixeiro viajante |
| Algoritmos Genéticos | ❌ Não implementado | - | - |
| Algoritmos Incrementais/Decrementais | ✅ Implementado | `/algoritmos/dinamicos/dinamicos.py` | Implementado como parte do módulo de grafos dinâmicos |
| Maximal Clique (Bron–Kerbosch) | ❌ Não implementado | - | Algoritmo para encontrar cliques maximais |
| Girvan-Newman | ❌ Não implementado | - | Algoritmo para detecção de comunidades |
| Louvain Method | ❌ Não implementado | - | Algoritmo para detecção de comunidades |

## Resumo

- **Total de algoritmos solicitados**: 32
- **Algoritmos já implementados**: 8 (25%)
- **Algoritmos a implementar**: 24 (75%)

## Priorização para Implementação

Baseado na importância e utilidade dos algoritmos, sugere-se a seguinte ordem de implementação:

### Alta Prioridade
1. BFS e DFS (fundamentais e usados por muitos outros algoritmos)
2. Bellman-Ford (complementa Dijkstra para grafos com pesos negativos)
3. Floyd-Warshall (importante para problemas de todos os pares de caminhos mínimos)
4. Tarjan (fundamental para análise de componentes fortemente conexos)
5. Edmonds-Karp (melhoria do Ford-Fulkerson já implementado)

### Média Prioridade
6. Prim (alternativa ao Kruskal já implementado)
7. Algoritmo para Pontes e Articulações
8. A* Algorithm (importante para busca heurística)
9. Kahn's Algorithm (para ordenação topológica)
10. Hopcroft-Karp (para emparelhamento em grafos bipartidos)

### Baixa Prioridade
11. Algoritmos restantes, conforme necessidade e tempo disponível
