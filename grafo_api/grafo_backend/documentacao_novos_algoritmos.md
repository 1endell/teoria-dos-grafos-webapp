# Documentação dos Novos Algoritmos de Teoria dos Grafos

Este documento descreve os novos algoritmos implementados no backend de teoria dos grafos, incluindo suas funcionalidades, parâmetros, valores de retorno e exemplos de uso.

## Algoritmos de Busca

### Breadth-First Search (BFS)

**Descrição**: Algoritmo de busca em largura que visita todos os vértices alcançáveis a partir da origem em ordem crescente de distância.

**Localização**: `algoritmos/caminhos/busca/busca.py`

**Funções**:
- `bfs(grafo, origem)`: Executa BFS a partir de um vértice de origem.
- `reconstruir_caminho_bfs(predecessores, origem, destino)`: Reconstrói o caminho mais curto encontrado pela BFS.

**Exemplo de uso**:
```python
from algoritmos.caminhos.busca.busca import bfs, reconstruir_caminho_bfs

# Executa BFS a partir do vértice 1
predecessores, distancias = bfs(grafo, 1)

# Reconstrói o caminho mais curto de 1 a 5
caminho = reconstruir_caminho_bfs(predecessores, 1, 5)
print(f"Caminho mais curto: {caminho}")
print(f"Distância: {distancias[5]}")
```

### Depth-First Search (DFS)

**Descrição**: Algoritmo de busca em profundidade que explora o grafo seguindo um caminho até o fim antes de retroceder.

**Localização**: `algoritmos/caminhos/busca/busca.py`

**Funções**:
- `dfs(grafo, origem)`: Executa DFS recursiva a partir de um vértice de origem.
- `dfs_iterativo(grafo, origem)`: Executa DFS de forma iterativa usando uma pilha explícita.

**Exemplo de uso**:
```python
from algoritmos.caminhos.busca.busca import dfs

# Executa DFS a partir do vértice 1
predecessores, tempos = dfs(grafo, 1)

# Analisa os tempos de descoberta e finalização
for vertice, (descoberta, finalizacao) in tempos.items():
    print(f"Vértice {vertice}: descoberto em {descoberta}, finalizado em {finalizacao}")
```

### Iterative Deepening DFS (IDDFS)

**Descrição**: Algoritmo que combina as vantagens da BFS e da DFS, realizando DFS com profundidade limitada e aumentando gradualmente essa profundidade.

**Localização**: `algoritmos/caminhos/busca/busca.py`

**Funções**:
- `iddfs(grafo, origem, profundidade_maxima)`: Executa IDDFS a partir de um vértice de origem até uma profundidade máxima.

**Exemplo de uso**:
```python
from algoritmos.caminhos.busca.busca import iddfs

# Executa IDDFS a partir do vértice 1 com profundidade máxima 3
predecessores, visitados = iddfs(grafo, 1, 3)
print(f"Vértices visitados: {visitados}")
```

### Funções Auxiliares de Busca

**Localização**: `algoritmos/caminhos/busca/busca.py`

**Funções**:
- `encontrar_componentes_conexos(grafo)`: Encontra todos os componentes conexos do grafo.
- `verificar_bipartido(grafo)`: Verifica se um grafo é bipartido.
- `encontrar_ciclo(grafo)`: Encontra um ciclo no grafo, se existir.
- `ordenacao_topologica(grafo)`: Realiza uma ordenação topológica do grafo direcionado acíclico.

## Algoritmos de Caminhos Mínimos

### Bellman-Ford

**Descrição**: Algoritmo para encontrar caminhos mínimos em grafos ponderados, mesmo com arestas de peso negativo.

**Localização**: `algoritmos/caminhos/bellman_ford.py`

**Funções**:
- `bellman_ford(grafo, origem)`: Executa o algoritmo de Bellman-Ford.
- `caminho_minimo(grafo, origem, destino)`: Encontra o caminho mínimo entre dois vértices.
- `detectar_ciclo_negativo(grafo)`: Detecta um ciclo de peso negativo no grafo, se existir.

**Exemplo de uso**:
```python
from algoritmos.caminhos.bellman_ford import bellman_ford, caminho_minimo

# Executa Bellman-Ford a partir do vértice 1
distancias, predecessores, ciclo_negativo = bellman_ford(grafo, 1)

# Encontra o caminho mínimo de 1 a 5
caminho, distancia = caminho_minimo(grafo, 1, 5)
print(f"Caminho mínimo: {caminho}")
print(f"Distância: {distancia}")
```

### Floyd-Warshall

**Descrição**: Algoritmo para encontrar caminhos mínimos entre todos os pares de vértices em um grafo ponderado.

**Localização**: `algoritmos/caminhos/floyd_warshall.py`

**Funções**:
- `floyd_warshall(grafo)`: Executa o algoritmo de Floyd-Warshall.
- `calcular_diametro(grafo)`: Calcula o diâmetro do grafo.
- `calcular_centro(grafo)`: Calcula o centro do grafo.
- `calcular_matriz_distancias(grafo)`: Calcula a matriz de distâncias entre todos os pares de vértices.

**Exemplo de uso**:
```python
from algoritmos.caminhos.floyd_warshall import floyd_warshall, calcular_diametro

# Executa Floyd-Warshall
distancias, proximos = floyd_warshall(grafo)

# Calcula o diâmetro do grafo
diametro, par = calcular_diametro(grafo)
print(f"Diâmetro do grafo: {diametro}")
print(f"Par de vértices que realiza o diâmetro: {par}")
```

## Algoritmos de Componentes Conexos

### Tarjan

**Descrição**: Algoritmo para encontrar componentes fortemente conexos em grafos direcionados.

**Localização**: `algoritmos/caminhos/tarjan.py`

**Funções**:
- `tarjan(grafo)`: Executa o algoritmo de Tarjan.
- `encontrar_componentes_fortemente_conexos(grafo)`: Encontra todos os componentes fortemente conexos do grafo.
- `condensar_grafo(grafo)`: Condensa um grafo direcionado em um grafo acíclico direcionado (DAG) de componentes fortemente conexos.

**Exemplo de uso**:
```python
from algoritmos.caminhos.tarjan import tarjan, condensar_grafo

# Encontra componentes fortemente conexos
componentes = tarjan(grafo)
print(f"Componentes fortemente conexos: {componentes}")

# Condensa o grafo
grafo_condensado, mapeamento = condensar_grafo(grafo)
print(f"Grafo condensado: {grafo_condensado}")
```

### Pontes e Articulações

**Descrição**: Algoritmos para encontrar pontes e pontos de articulação em grafos não direcionados.

**Localização**: `algoritmos/caminhos/tarjan.py`

**Funções**:
- `encontrar_pontes(grafo)`: Encontra todas as pontes no grafo.
- `encontrar_pontos_articulacao(grafo)`: Encontra todos os pontos de articulação no grafo.
- `verificar_grafo_biconexo(grafo)`: Verifica se um grafo é biconexo.

**Exemplo de uso**:
```python
from algoritmos.caminhos.tarjan import encontrar_pontes, encontrar_pontos_articulacao

# Encontra pontes
pontes = encontrar_pontes(grafo)
print(f"Pontes encontradas: {pontes}")

# Encontra pontos de articulação
articulacoes = encontrar_pontos_articulacao(grafo)
print(f"Pontos de articulação encontrados: {articulacoes}")
```

## Algoritmos de Fluxo

### Edmonds-Karp

**Descrição**: Algoritmo para encontrar o fluxo máximo em redes, implementação específica do método de Ford-Fulkerson que usa BFS para encontrar caminhos de aumento.

**Localização**: `algoritmos/fluxo/edmonds_karp.py`

**Funções**:
- `edmonds_karp(grafo, fonte, sumidouro)`: Executa o algoritmo de Edmonds-Karp.
- `fluxo_maximo(grafo, fonte, sumidouro)`: Encontra o fluxo máximo em uma rede.
- `corte_minimo(grafo, fonte, sumidouro)`: Encontra o corte mínimo em uma rede.
- `comparar_desempenho_ford_fulkerson_edmonds_karp(grafo, fonte, sumidouro)`: Compara o desempenho dos algoritmos de Ford-Fulkerson e Edmonds-Karp.

**Exemplo de uso**:
```python
from algoritmos.fluxo.edmonds_karp import edmonds_karp, corte_minimo

# Encontra o fluxo máximo
fluxo, valor_fluxo = edmonds_karp(grafo, 1, 6)
print(f"Valor do fluxo máximo: {valor_fluxo}")

# Encontra o corte mínimo
lado_fonte, lado_sumidouro, capacidade = corte_minimo(grafo, 1, 6)
print(f"Corte mínimo: {capacidade}")
```

## Criação de Grafos Direcionados

Com a atualização da classe `Grafo`, agora é possível criar grafos direcionados de forma nativa:

```python
# Cria um grafo não direcionado (padrão)
grafo = Grafo("Meu Grafo")

# Cria um grafo direcionado
grafo_dir = Grafo("Meu Grafo Direcionado", direcionado=True)

# Verifica se um grafo é direcionado
eh_direcionado = grafo.eh_direcionado()
```

## Próximos Passos

Os seguintes algoritmos ainda estão pendentes de implementação:

1. A* Algorithm
2. Prim
3. Hopcroft-Karp
4. Hungarian Algorithm
5. Kahn's Algorithm
6. Hierholzer
7. Algoritmos para Hamiltonianos
8. Backtracking
9. Ullmann Algorithm
10. Hopcroft-Tarjan
11. Christofides
12. Algoritmos Genéticos
13. Maximal Clique (Bron–Kerbosch)
14. Girvan-Newman
15. Louvain Method

Estes algoritmos serão implementados em futuras atualizações do backend.
