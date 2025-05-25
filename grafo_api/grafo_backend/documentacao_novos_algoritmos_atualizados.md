# Documentação dos Algoritmos de Teoria dos Grafos

Esta documentação apresenta os algoritmos implementados no backend de teoria dos grafos, incluindo descrições, exemplos de uso, complexidade computacional e limitações.

## Sumário

1. [Algoritmos de Busca](#algoritmos-de-busca)
2. [Algoritmos de Caminhos Mínimos](#algoritmos-de-caminhos-mínimos)
3. [Algoritmos de Componentes Conexos](#algoritmos-de-componentes-conexos)
4. [Algoritmos de Árvores Geradoras Mínimas](#algoritmos-de-árvores-geradoras-mínimas)
5. [Algoritmos de Fluxo Máximo](#algoritmos-de-fluxo-máximo)
6. [Algoritmos de Emparelhamento](#algoritmos-de-emparelhamento)
7. [Algoritmos de Ordenação Topológica](#algoritmos-de-ordenação-topológica)
8. [Algoritmos de Ciclos](#algoritmos-de-ciclos)
9. [Algoritmos de Cliques](#algoritmos-de-cliques)
10. [Algoritmos de Isomorfismo](#algoritmos-de-isomorfismo)
11. [Algoritmos de Planaridade](#algoritmos-de-planaridade)
12. [Algoritmos de Detecção de Comunidades](#algoritmos-de-detecção-de-comunidades)
13. [Algoritmos para o Problema do Caixeiro Viajante](#algoritmos-para-o-problema-do-caixeiro-viajante)

## Algoritmos de Busca

### Breadth-First Search (BFS)

**Descrição**: Algoritmo de busca em largura que explora todos os vértices de um grafo em níveis, visitando primeiro todos os vizinhos de um vértice antes de avançar para os próximos níveis.

**Implementação**: `algoritmos/caminhos/busca/busca.py`

**Complexidade**: O(V + E), onde V é o número de vértices e E é o número de arestas.

**Exemplo de uso**:
```python
from core.grafo import Grafo
from algoritmos.caminhos.busca.busca import bfs

# Cria um grafo
grafo = Grafo("Grafo de Exemplo")
grafo.adicionar_vertice(1)
grafo.adicionar_vertice(2)
grafo.adicionar_vertice(3)
grafo.adicionar_aresta(1, 2)
grafo.adicionar_aresta(1, 3)
grafo.adicionar_aresta(2, 3)

# Executa BFS a partir do vértice 1
predecessores, distancias = bfs(grafo, 1)
print(f"Predecessores: {predecessores}")
print(f"Distâncias: {distancias}")
```

**Limitações**: Não considera pesos nas arestas e não é adequado para encontrar caminhos mínimos em grafos ponderados.

### Depth-First Search (DFS)

**Descrição**: Algoritmo de busca em profundidade que explora o grafo seguindo um caminho até o fim antes de retroceder.

**Implementação**: `algoritmos/caminhos/busca/busca.py`

**Complexidade**: O(V + E), onde V é o número de vértices e E é o número de arestas.

**Exemplo de uso**:
```python
from core.grafo import Grafo
from algoritmos.caminhos.busca.busca import dfs

# Cria um grafo
grafo = Grafo("Grafo de Exemplo")
grafo.adicionar_vertice(1)
grafo.adicionar_vertice(2)
grafo.adicionar_vertice(3)
grafo.adicionar_aresta(1, 2)
grafo.adicionar_aresta(1, 3)
grafo.adicionar_aresta(2, 3)

# Executa DFS a partir do vértice 1
predecessores, tempos = dfs(grafo, 1)
print(f"Predecessores: {predecessores}")
print(f"Tempos de descoberta e finalização: {tempos}")
```

**Limitações**: Não garante encontrar o caminho mais curto entre dois vértices.

### Iterative Deepening DFS (IDDFS)

**Descrição**: Combina as vantagens de BFS e DFS, realizando múltiplas buscas em profundidade com profundidade limitada crescente.

**Implementação**: `algoritmos/caminhos/busca/busca.py`

**Complexidade**: O(b^d), onde b é o fator de ramificação e d é a profundidade da solução.

**Exemplo de uso**:
```python
from core.grafo import Grafo
from algoritmos.caminhos.busca.busca import iddfs

# Cria um grafo
grafo = Grafo("Grafo de Exemplo")
grafo.adicionar_vertice(1)
grafo.adicionar_vertice(2)
grafo.adicionar_vertice(3)
grafo.adicionar_vertice(4)
grafo.adicionar_aresta(1, 2)
grafo.adicionar_aresta(1, 3)
grafo.adicionar_aresta(2, 4)
grafo.adicionar_aresta(3, 4)

# Executa IDDFS a partir do vértice 1 com profundidade máxima 2
predecessores, visitados = iddfs(grafo, 1, 2)
print(f"Predecessores: {predecessores}")
print(f"Vértices visitados: {visitados}")
```

**Limitações**: Pode ser mais lento que BFS para encontrar soluções em níveis rasos.

## Algoritmos de Caminhos Mínimos

### Dijkstra

**Descrição**: Algoritmo para encontrar o caminho mais curto entre um vértice e todos os outros em um grafo ponderado com pesos não negativos.

**Implementação**: `algoritmos/caminhos/dijkstra.py`

**Complexidade**: O(V^2) com matriz de adjacência, O((V+E)log V) com fila de prioridade.

**Exemplo de uso**:
```python
from core.grafo import Grafo
from algoritmos.caminhos.dijkstra import dijkstra

# Cria um grafo ponderado
grafo = Grafo("Grafo Ponderado")
grafo.adicionar_vertice(1)
grafo.adicionar_vertice(2)
grafo.adicionar_vertice(3)
grafo.adicionar_aresta(1, 2, peso=5)
grafo.adicionar_aresta(1, 3, peso=10)
grafo.adicionar_aresta(2, 3, peso=2)

# Encontra os caminhos mínimos a partir do vértice 1
distancias, predecessores = dijkstra(grafo, 1)
print(f"Distâncias: {distancias}")
print(f"Predecessores: {predecessores}")
```

**Limitações**: Não funciona corretamente em grafos com arestas de peso negativo.

### Bellman-Ford

**Descrição**: Algoritmo para encontrar o caminho mais curto entre um vértice e todos os outros em um grafo ponderado, mesmo com pesos negativos.

**Implementação**: `algoritmos/caminhos/bellman_ford.py`

**Complexidade**: O(V*E), onde V é o número de vértices e E é o número de arestas.

**Exemplo de uso**:
```python
from core.grafo import Grafo
from algoritmos.caminhos.bellman_ford import bellman_ford

# Cria um grafo ponderado com arestas de peso negativo
grafo = Grafo("Grafo com Pesos Negativos", direcionado=True)
grafo.adicionar_vertice(1)
grafo.adicionar_vertice(2)
grafo.adicionar_vertice(3)
grafo.adicionar_aresta(1, 2, peso=5)
grafo.adicionar_aresta(1, 3, peso=10)
grafo.adicionar_aresta(2, 3, peso=-2)

# Encontra os caminhos mínimos a partir do vértice 1
distancias, predecessores, ciclo_negativo = bellman_ford(grafo, 1)
print(f"Distâncias: {distancias}")
print(f"Predecessores: {predecessores}")
print(f"Ciclo negativo detectado: {ciclo_negativo}")
```

**Limitações**: Mais lento que Dijkstra para grafos sem arestas de peso negativo.

### Floyd-Warshall

**Descrição**: Algoritmo para encontrar os caminhos mais curtos entre todos os pares de vértices em um grafo ponderado.

**Implementação**: `algoritmos/caminhos/floyd_warshall.py`

**Complexidade**: O(V^3), onde V é o número de vértices.

**Exemplo de uso**:
```python
from core.grafo import Grafo
from algoritmos.caminhos.floyd_warshall import floyd_warshall

# Cria um grafo ponderado
grafo = Grafo("Grafo Ponderado")
grafo.adicionar_vertice(1)
grafo.adicionar_vertice(2)
grafo.adicionar_vertice(3)
grafo.adicionar_aresta(1, 2, peso=5)
grafo.adicionar_aresta(1, 3, peso=10)
grafo.adicionar_aresta(2, 3, peso=2)

# Encontra os caminhos mínimos entre todos os pares de vértices
distancias = floyd_warshall(grafo)
print(f"Matriz de distâncias: {distancias}")
```

**Limitações**: Não é eficiente para grafos grandes devido à complexidade cúbica.

### A* Algorithm

**Descrição**: Algoritmo de busca informada que encontra o caminho mais curto entre dois vértices usando uma heurística para guiar a busca.

**Implementação**: `algoritmos/caminhos/a_star.py`

**Complexidade**: O(E), onde E é o número de arestas, mas depende da heurística.

**Exemplo de uso**:
```python
from core.grafo import Grafo
from algoritmos.caminhos.a_star import a_star

# Cria um grafo ponderado
grafo = Grafo("Grafo Ponderado")
grafo.adicionar_vertice(1)
grafo.adicionar_vertice(2)
grafo.adicionar_vertice(3)
grafo.adicionar_aresta(1, 2, peso=5)
grafo.adicionar_aresta(1, 3, peso=10)
grafo.adicionar_aresta(2, 3, peso=2)

# Encontra o caminho mais curto entre os vértices 1 e 3
caminho, custo = a_star(grafo, 1, 3)
print(f"Caminho: {caminho}")
print(f"Custo: {custo}")
```

**Limitações**: A eficiência depende da qualidade da heurística utilizada.

## Algoritmos de Componentes Conexos

### Tarjan

**Descrição**: Algoritmo para encontrar componentes fortemente conexos em grafos direcionados.

**Implementação**: `algoritmos/caminhos/tarjan.py`

**Complexidade**: O(V + E), onde V é o número de vértices e E é o número de arestas.

**Exemplo de uso**:
```python
from core.grafo import Grafo
from algoritmos.caminhos.tarjan import tarjan

# Cria um grafo direcionado
grafo = Grafo("Grafo Direcionado", direcionado=True)
grafo.adicionar_vertice(1)
grafo.adicionar_vertice(2)
grafo.adicionar_vertice(3)
grafo.adicionar_aresta(1, 2)
grafo.adicionar_aresta(2, 3)
grafo.adicionar_aresta(3, 1)

# Encontra os componentes fortemente conexos
componentes = tarjan(grafo)
print(f"Componentes fortemente conexos: {componentes}")
```

**Limitações**: Aplicável apenas a grafos direcionados.

### Algoritmos para Pontes e Articulações

**Descrição**: Algoritmos para encontrar pontes (arestas cuja remoção aumenta o número de componentes conexos) e articulações (vértices cuja remoção aumenta o número de componentes conexos) em grafos não direcionados.

**Implementação**: `algoritmos/caminhos/tarjan.py`

**Complexidade**: O(V + E), onde V é o número de vértices e E é o número de arestas.

**Exemplo de uso**:
```python
from core.grafo import Grafo
from algoritmos.caminhos.tarjan import encontrar_pontes, encontrar_pontos_articulacao

# Cria um grafo não direcionado
grafo = Grafo("Grafo Não Direcionado")
grafo.adicionar_vertice(1)
grafo.adicionar_vertice(2)
grafo.adicionar_vertice(3)
grafo.adicionar_vertice(4)
grafo.adicionar_aresta(1, 2)
grafo.adicionar_aresta(2, 3)
grafo.adicionar_aresta(3, 4)

# Encontra as pontes
pontes = encontrar_pontes(grafo)
print(f"Pontes: {pontes}")

# Encontra as articulações
articulacoes = encontrar_pontos_articulacao(grafo)
print(f"Articulações: {articulacoes}")
```

**Limitações**: Aplicável apenas a grafos não direcionados.

## Algoritmos de Árvores Geradoras Mínimas

### Kruskal

**Descrição**: Algoritmo para encontrar uma árvore geradora mínima em um grafo ponderado não direcionado.

**Implementação**: `algoritmos/arvores/kruskal.py`

**Complexidade**: O(E log E), onde E é o número de arestas.

**Exemplo de uso**:
```python
from core.grafo import Grafo
from algoritmos.arvores.kruskal import arvore_geradora_minima

# Cria um grafo ponderado não direcionado
grafo = Grafo("Grafo Ponderado")
grafo.adicionar_vertice(1)
grafo.adicionar_vertice(2)
grafo.adicionar_vertice(3)
grafo.adicionar_aresta(1, 2, peso=5)
grafo.adicionar_aresta(1, 3, peso=10)
grafo.adicionar_aresta(2, 3, peso=2)

# Encontra a árvore geradora mínima
arestas, custo_total = arvore_geradora_minima(grafo)
print(f"Arestas da árvore geradora mínima: {arestas}")
print(f"Custo total: {custo_total}")
```

**Limitações**: Requer que o grafo seja conexo para encontrar uma árvore geradora.

### Prim

**Descrição**: Algoritmo para encontrar uma árvore geradora mínima em um grafo ponderado não direcionado.

**Implementação**: `algoritmos/arvores/prim.py`

**Complexidade**: O(V^2) com matriz de adjacência, O(E log V) com fila de prioridade.

**Exemplo de uso**:
```python
from core.grafo import Grafo
from algoritmos.arvores.prim import prim

# Cria um grafo ponderado não direcionado
grafo = Grafo("Grafo Ponderado")
grafo.adicionar_vertice(1)
grafo.adicionar_vertice(2)
grafo.adicionar_vertice(3)
grafo.adicionar_aresta(1, 2, peso=5)
grafo.adicionar_aresta(1, 3, peso=10)
grafo.adicionar_aresta(2, 3, peso=2)

# Encontra a árvore geradora mínima
arestas, custo_total = prim(grafo)
print(f"Arestas da árvore geradora mínima: {arestas}")
print(f"Custo total: {custo_total}")
```

**Limitações**: Requer que o grafo seja conexo para encontrar uma árvore geradora.

## Algoritmos de Fluxo Máximo

### Ford-Fulkerson

**Descrição**: Algoritmo para encontrar o fluxo máximo em uma rede de fluxo.

**Implementação**: `algoritmos/fluxo/ford_fulkerson.py`

**Complexidade**: O(E * max_flow), onde E é o número de arestas e max_flow é o valor do fluxo máximo.

**Exemplo de uso**:
```python
from core.grafo import Grafo
from algoritmos.fluxo.ford_fulkerson import ford_fulkerson

# Cria um grafo direcionado com capacidades
grafo = Grafo("Rede de Fluxo", direcionado=True)
grafo.adicionar_vertice('s')  # fonte
grafo.adicionar_vertice('t')  # sumidouro
grafo.adicionar_vertice('a')
grafo.adicionar_vertice('b')
grafo.adicionar_aresta('s', 'a', peso=10)  # peso = capacidade
grafo.adicionar_aresta('s', 'b', peso=5)
grafo.adicionar_aresta('a', 't', peso=8)
grafo.adicionar_aresta('b', 't', peso=7)

# Encontra o fluxo máximo
fluxos, fluxo_maximo = ford_fulkerson(grafo, 's', 't')
print(f"Fluxos nas arestas: {fluxos}")
print(f"Fluxo máximo: {fluxo_maximo}")
```

**Limitações**: Pode ser ineficiente para grafos com capacidades grandes.

### Edmonds-Karp

**Descrição**: Implementação do algoritmo de Ford-Fulkerson que usa BFS para encontrar caminhos aumentantes.

**Implementação**: `algoritmos/fluxo/edmonds_karp.py`

**Complexidade**: O(V * E^2), onde V é o número de vértices e E é o número de arestas.

**Exemplo de uso**:
```python
from core.grafo import Grafo
from algoritmos.fluxo.edmonds_karp import edmonds_karp

# Cria um grafo direcionado com capacidades
grafo = Grafo("Rede de Fluxo", direcionado=True)
grafo.adicionar_vertice('s')  # fonte
grafo.adicionar_vertice('t')  # sumidouro
grafo.adicionar_vertice('a')
grafo.adicionar_vertice('b')
grafo.adicionar_aresta('s', 'a', peso=10)  # peso = capacidade
grafo.adicionar_aresta('s', 'b', peso=5)
grafo.adicionar_aresta('a', 't', peso=8)
grafo.adicionar_aresta('b', 't', peso=7)

# Encontra o fluxo máximo
fluxos, fluxo_maximo = edmonds_karp(grafo, 's', 't')
print(f"Fluxos nas arestas: {fluxos}")
print(f"Fluxo máximo: {fluxo_maximo}")
```

**Limitações**: Pode ser mais lento que Dinic para redes de fluxo complexas.

### Dinic

**Descrição**: Algoritmo para encontrar o fluxo máximo em uma rede de fluxo, mais eficiente que Ford-Fulkerson e Edmonds-Karp.

**Implementação**: `algoritmos/fluxo/dinic.py`

**Complexidade**: O(V^2 * E), onde V é o número de vértices e E é o número de arestas.

**Exemplo de uso**:
```python
from core.grafo import Grafo
from algoritmos.fluxo.dinic import dinic

# Cria um grafo direcionado com capacidades
grafo = Grafo("Rede de Fluxo", direcionado=True)
grafo.adicionar_vertice('s')  # fonte
grafo.adicionar_vertice('t')  # sumidouro
grafo.adicionar_vertice('a')
grafo.adicionar_vertice('b')
grafo.adicionar_aresta('s', 'a', peso=10)  # peso = capacidade
grafo.adicionar_aresta('s', 'b', peso=5)
grafo.adicionar_aresta('a', 't', peso=8)
grafo.adicionar_aresta('b', 't', peso=7)

# Encontra o fluxo máximo
fluxos, fluxo_maximo = dinic(grafo, 's', 't')
print(f"Fluxos nas arestas: {fluxos}")
print(f"Fluxo máximo: {fluxo_maximo}")
```

**Limitações**: Implementação mais complexa que os outros algoritmos de fluxo.

## Algoritmos de Emparelhamento

### Hopcroft-Karp

**Descrição**: Algoritmo para encontrar um emparelhamento máximo em um grafo bipartido.

**Implementação**: `algoritmos/emparelhamento/hopcroft_karp.py`

**Complexidade**: O(E * sqrt(V)), onde E é o número de arestas e V é o número de vértices.

**Exemplo de uso**:
```python
from core.grafo import Grafo
from algoritmos.emparelhamento.hopcroft_karp import hopcroft_karp

# Cria um grafo bipartido
grafo = Grafo("Grafo Bipartido")
grafo.adicionar_vertice('u1')
grafo.adicionar_vertice('u2')
grafo.adicionar_vertice('v1')
grafo.adicionar_vertice('v2')
grafo.adicionar_aresta('u1', 'v1')
grafo.adicionar_aresta('u1', 'v2')
grafo.adicionar_aresta('u2', 'v1')

# Encontra o emparelhamento máximo
emparelhamento = hopcroft_karp(grafo)
print(f"Emparelhamento: {emparelhamento}")
print(f"Tamanho do emparelhamento: {len(emparelhamento)}")
```

**Limitações**: Aplicável apenas a grafos bipartidos.

### Hungarian Algorithm

**Descrição**: Algoritmo para resolver o problema de atribuição ótima, encontrando um emparelhamento de custo mínimo em um grafo bipartido ponderado.

**Implementação**: `algoritmos/emparelhamento/hungarian.py`

**Complexidade**: O(n^3), onde n é o número de vértices em cada parte do grafo bipartido.

**Exemplo de uso**:
```python
import numpy as np
from algoritmos.emparelhamento.hungarian import hungarian_algorithm

# Cria uma matriz de custos
matriz_custos = np.array([
    [10, 20, 30],
    [15, 25, 35],
    [20, 30, 40]
])

# Encontra a atribuição ótima
atribuicao, custo_total = hungarian_algorithm(matriz_custos)
print(f"Atribuição: {atribuicao}")
print(f"Custo total: {custo_total}")
```

**Limitações**: Requer uma matriz de custos quadrada.

## Algoritmos de Ordenação Topológica

### Kahn's Algorithm

**Descrição**: Algoritmo para encontrar uma ordenação topológica em um grafo acíclico direcionado (DAG).

**Implementação**: `algoritmos/ordenacao/kahn.py`

**Complexidade**: O(V + E), onde V é o número de vértices e E é o número de arestas.

**Exemplo de uso**:
```python
from core.grafo import Grafo
from algoritmos.ordenacao.kahn import kahn

# Cria um grafo acíclico direcionado
grafo = Grafo("DAG", direcionado=True)
grafo.adicionar_vertice(1)
grafo.adicionar_vertice(2)
grafo.adicionar_vertice(3)
grafo.adicionar_aresta(1, 2)
grafo.adicionar_aresta(1, 3)
grafo.adicionar_aresta(2, 3)

# Encontra uma ordenação topológica
ordenacao = kahn(grafo)
print(f"Ordenação topológica: {ordenacao}")
```

**Limitações**: Aplicável apenas a grafos acíclicos direcionados.

## Algoritmos de Ciclos

### Hierholzer

**Descrição**: Algoritmo para encontrar um ciclo euleriano em um grafo.

**Implementação**: `algoritmos/ciclos/hierholzer.py`

**Complexidade**: O(E), onde E é o número de arestas.

**Exemplo de uso**:
```python
from core.grafo import Grafo
from algoritmos.ciclos.hierholzer import hierholzer, verificar_grafo_euleriano

# Cria um grafo euleriano
grafo = Grafo("Grafo Euleriano")
grafo.adicionar_vertice(1)
grafo.adicionar_vertice(2)
grafo.adicionar_vertice(3)
grafo.adicionar_aresta(1, 2)
grafo.adicionar_aresta(2, 3)
grafo.adicionar_aresta(3, 1)

# Verifica se o grafo é euleriano
eh_euleriano = verificar_grafo_euleriano(grafo)
print(f"É euleriano: {eh_euleriano}")

# Encontra um ciclo euleriano
ciclo = hierholzer(grafo)
print(f"Ciclo euleriano: {ciclo}")
```

**Limitações**: O grafo deve ser euleriano (todos os vértices têm grau par e o grafo é conexo).

### Algoritmos para Hamiltonianos

**Descrição**: Algoritmos para encontrar ciclos hamiltonianos em um grafo.

**Implementação**: `algoritmos/ciclos/hamiltoniano.py`

**Complexidade**: O(n!), onde n é o número de vértices.

**Exemplo de uso**:
```python
from core.grafo import Grafo
from algoritmos.ciclos.hamiltoniano import encontrar_ciclo_hamiltoniano_backtracking, verificar_ciclo_hamiltoniano

# Cria um grafo hamiltoniano
grafo = Grafo("Grafo Hamiltoniano")
grafo.adicionar_vertice(1)
grafo.adicionar_vertice(2)
grafo.adicionar_vertice(3)
grafo.adicionar_aresta(1, 2)
grafo.adicionar_aresta(2, 3)
grafo.adicionar_aresta(3, 1)

# Encontra um ciclo hamiltoniano
ciclo = encontrar_ciclo_hamiltoniano_backtracking(grafo)
print(f"Ciclo hamiltoniano: {ciclo}")

# Verifica se o ciclo é válido
valido = verificar_ciclo_hamiltoniano(grafo, ciclo)
print(f"Ciclo válido: {valido}")
```

**Limitações**: Algoritmo exponencial, não eficiente para grafos grandes.

## Algoritmos de Cliques

### Bron-Kerbosch

**Descrição**: Algoritmo para encontrar todos os cliques maximais em um grafo não direcionado.

**Implementação**: `algoritmos/cliques/bron_kerbosch.py`

**Complexidade**: O(3^(n/3)), onde n é o número de vértices.

**Exemplo de uso**:
```python
from core.grafo import Grafo
from algoritmos.cliques.bron_kerbosch import bron_kerbosch, encontrar_clique_maximo

# Cria um grafo não direcionado
grafo = Grafo("Grafo com Cliques")
grafo.adicionar_vertice(1)
grafo.adicionar_vertice(2)
grafo.adicionar_vertice(3)
grafo.adicionar_vertice(4)
grafo.adicionar_aresta(1, 2)
grafo.adicionar_aresta(1, 3)
grafo.adicionar_aresta(2, 3)
grafo.adicionar_aresta(3, 4)

# Encontra todos os cliques maximais
cliques = bron_kerbosch(grafo)
print(f"Cliques maximais: {cliques}")

# Encontra o clique máximo
clique_maximo, tamanho = encontrar_clique_maximo(grafo)
print(f"Clique máximo: {clique_maximo}")
print(f"Tamanho: {tamanho}")
```

**Limitações**: Algoritmo exponencial, não eficiente para grafos grandes.

## Algoritmos de Isomorfismo

### Ullmann Algorithm

**Descrição**: Algoritmo para verificar se um grafo é isomorfo a um subgrafo de outro grafo.

**Implementação**: `algoritmos/isomorfismo/ullmann.py`

**Complexidade**: O(n!), onde n é o número de vértices.

**Exemplo de uso**:
```python
from core.grafo import Grafo
from algoritmos.isomorfismo.ullmann import ullmann, verificar_isomorfismo_subgrafo

# Cria dois grafos
grafo_pequeno = Grafo("Grafo Pequeno")
grafo_pequeno.adicionar_vertice(1)
grafo_pequeno.adicionar_vertice(2)
grafo_pequeno.adicionar_aresta(1, 2)

grafo_grande = Grafo("Grafo Grande")
grafo_grande.adicionar_vertice(1)
grafo_grande.adicionar_vertice(2)
grafo_grande.adicionar_vertice(3)
grafo_grande.adicionar_aresta(1, 2)
grafo_grande.adicionar_aresta(2, 3)

# Verifica se o grafo pequeno é isomorfo a um subgrafo do grafo grande
mapeamento = ullmann(grafo_pequeno, grafo_grande)
print(f"Mapeamento: {mapeamento}")

# Verifica se o mapeamento é válido
valido = verificar_isomorfismo_subgrafo(grafo_pequeno, grafo_grande, mapeamento)
print(f"Isomorfismo válido: {valido}")
```

**Limitações**: Algoritmo exponencial, não eficiente para grafos grandes.

## Algoritmos de Planaridade

### Hopcroft-Tarjan

**Descrição**: Algoritmo para verificar se um grafo é planar.

**Implementação**: `algoritmos/planaridade/hopcroft_tarjan.py`

**Complexidade**: O(V), onde V é o número de vértices.

**Exemplo de uso**:
```python
from core.grafo import Grafo
from algoritmos.planaridade.hopcroft_tarjan import hopcroft_tarjan, encontrar_embedding_planar

# Cria um grafo planar
grafo = Grafo("Grafo Planar")
grafo.adicionar_vertice(1)
grafo.adicionar_vertice(2)
grafo.adicionar_vertice(3)
grafo.adicionar_vertice(4)
grafo.adicionar_aresta(1, 2)
grafo.adicionar_aresta(2, 3)
grafo.adicionar_aresta(3, 4)
grafo.adicionar_aresta(4, 1)

# Verifica se o grafo é planar
eh_planar = hopcroft_tarjan(grafo)
print(f"É planar: {eh_planar}")

# Encontra um embedding planar
embedding = encontrar_embedding_planar(grafo)
print(f"Embedding: {embedding}")
```

**Limitações**: A implementação atual usa o algoritmo de Boyer-Myrvold do NetworkX, que é uma variante mais eficiente do Hopcroft-Tarjan.

## Algoritmos de Detecção de Comunidades

### Girvan-Newman

**Descrição**: Algoritmo para detectar comunidades em grafos, removendo iterativamente as arestas com maior centralidade de intermediação.

**Implementação**: `algoritmos/comunidades/deteccao_comunidades.py`

**Complexidade**: O(V * E^2), onde V é o número de vértices e E é o número de arestas.

**Exemplo de uso**:
```python
from core.grafo import Grafo
from algoritmos.comunidades.deteccao_comunidades import girvan_newman

# Cria um grafo com comunidades
grafo = Grafo("Grafo com Comunidades")
grafo.adicionar_vertice(1)
grafo.adicionar_vertice(2)
grafo.adicionar_vertice(3)
grafo.adicionar_vertice(4)
grafo.adicionar_vertice(5)
grafo.adicionar_aresta(1, 2)
grafo.adicionar_aresta(1, 3)
grafo.adicionar_aresta(2, 3)
grafo.adicionar_aresta(4, 5)
grafo.adicionar_aresta(3, 4)

# Detecta comunidades
comunidades = girvan_newman(grafo, num_comunidades=2)
print(f"Comunidades: {comunidades}")
```

**Limitações**: Pode ser lento para grafos grandes devido ao cálculo repetido da centralidade de intermediação.

### Louvain Method

**Descrição**: Algoritmo hierárquico para detectar comunidades em grafos, otimizando a modularidade.

**Implementação**: `algoritmos/comunidades/deteccao_comunidades.py`

**Complexidade**: O(n * log n), onde n é o número de vértices.

**Exemplo de uso**:
```python
from core.grafo import Grafo
from algoritmos.comunidades.deteccao_comunidades import louvain_method, calcular_modularidade

# Cria um grafo com comunidades
grafo = Grafo("Grafo com Comunidades")
grafo.adicionar_vertice(1)
grafo.adicionar_vertice(2)
grafo.adicionar_vertice(3)
grafo.adicionar_vertice(4)
grafo.adicionar_vertice(5)
grafo.adicionar_aresta(1, 2)
grafo.adicionar_aresta(1, 3)
grafo.adicionar_aresta(2, 3)
grafo.adicionar_aresta(4, 5)
grafo.adicionar_aresta(3, 4)

# Detecta comunidades
comunidades = louvain_method(grafo)
print(f"Comunidades: {comunidades}")

# Calcula a modularidade
modularidade = calcular_modularidade(grafo, comunidades)
print(f"Modularidade: {modularidade}")
```

**Limitações**: A qualidade das comunidades detectadas depende da estrutura do grafo.

## Algoritmos para o Problema do Caixeiro Viajante

### Christofides

**Descrição**: Algoritmo de aproximação para o problema do caixeiro viajante em grafos completos que satisfazem a desigualdade triangular.

**Implementação**: `algoritmos/tsp/christofides.py`

**Complexidade**: O(n^3), onde n é o número de vértices.

**Exemplo de uso**:
```python
from core.grafo import Grafo
from algoritmos.tsp.christofides import christofides

# Cria um grafo completo
grafo = Grafo("Grafo Completo")
grafo.adicionar_vertice(1)
grafo.adicionar_vertice(2)
grafo.adicionar_vertice(3)
grafo.adicionar_vertice(4)
grafo.adicionar_aresta(1, 2, peso=10)
grafo.adicionar_aresta(1, 3, peso=15)
grafo.adicionar_aresta(1, 4, peso=20)
grafo.adicionar_aresta(2, 3, peso=35)
grafo.adicionar_aresta(2, 4, peso=25)
grafo.adicionar_aresta(3, 4, peso=30)

# Encontra uma aproximação para o TSP
ciclo, custo = christofides(grafo)
print(f"Ciclo: {ciclo}")
print(f"Custo: {custo}")
```

**Limitações**: Garante uma solução com custo no máximo 1.5 vezes o custo ótimo, mas apenas para grafos que satisfazem a desigualdade triangular.

### Algoritmos Genéticos

**Descrição**: Algoritmo evolutivo para encontrar uma aproximação para o problema do caixeiro viajante.

**Implementação**: `algoritmos/tsp/christofides.py`

**Complexidade**: Depende do número de gerações e do tamanho da população.

**Exemplo de uso**:
```python
from core.grafo import Grafo
from algoritmos.tsp.christofides import algoritmo_genetico_tsp

# Cria um grafo completo
grafo = Grafo("Grafo Completo")
grafo.adicionar_vertice(1)
grafo.adicionar_vertice(2)
grafo.adicionar_vertice(3)
grafo.adicionar_vertice(4)
grafo.adicionar_aresta(1, 2, peso=10)
grafo.adicionar_aresta(1, 3, peso=15)
grafo.adicionar_aresta(1, 4, peso=20)
grafo.adicionar_aresta(2, 3, peso=35)
grafo.adicionar_aresta(2, 4, peso=25)
grafo.adicionar_aresta(3, 4, peso=30)

# Encontra uma aproximação para o TSP usando algoritmo genético
ciclo, custo = algoritmo_genetico_tsp(grafo, tamanho_populacao=50, num_geracoes=100)
print(f"Ciclo: {ciclo}")
print(f"Custo: {custo}")
```

**Limitações**: Não garante encontrar a solução ótima, e a qualidade da solução depende dos parâmetros do algoritmo.

## Conclusão

Este backend de teoria dos grafos fornece uma ampla gama de algoritmos para análise e manipulação de grafos, implementados de forma modular e bem documentada. Os algoritmos são fiéis aos princípios da teoria dos grafos e podem ser usados para resolver diversos problemas em diferentes domínios.

Para mais informações sobre cada algoritmo, consulte a documentação específica nos arquivos de implementação.
