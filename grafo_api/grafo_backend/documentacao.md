# Documentação do Backend para Estudo de Teoria dos Grafos

## Visão Geral

Este backend foi desenvolvido para estudo e aplicação da teoria dos grafos, permitindo criar, editar, comparar, aplicar funções e testar diversas possibilidades dos grafos. A implementação é baseada na biblioteca NetworkX e segue rigorosamente os princípios da teoria dos grafos.

## Estrutura do Backend

O backend está organizado em módulos que implementam diferentes aspectos da teoria dos grafos:

```
grafo_backend/
├── core/                  # Classes base para representação de grafos
├── tipos/                 # Implementações de tipos específicos de grafos
├── algoritmos/            # Algoritmos clássicos da teoria dos grafos
│   ├── caminhos/          # Algoritmos de caminhos mínimos (Dijkstra)
│   ├── arvores/           # Algoritmos de árvores geradoras (Kruskal)
│   └── fluxo/             # Algoritmos de fluxo em redes (Ford-Fulkerson)
├── operacoes/             # Operações entre grafos (união, interseção, etc.)
├── persistencia/          # Importação e exportação de grafos em formatos padrão
│   ├── exportador/        # Funções para exportar grafos
│   └── importador/        # Funções para importar grafos
├── comparacao/            # Funções para comparação e isomorfismo de grafos
├── analise/               # Funções para análise de propriedades de grafos
├── geradores/             # Funções para geração de grafos específicos
├── visualizacao/          # Funções para visualização de grafos
├── utils/                 # Funções utilitárias
└── exemplos/              # Exemplos de uso do backend
```

## Módulos Principais

### Core

O módulo `core` contém as classes fundamentais para representação de grafos:

- `Grafo`: Classe base para representação de grafos
- `Vertice`: Classe para representação de vértices
- `Aresta`: Classe para representação de arestas

### Tipos de Grafos

O módulo `tipos` implementa diferentes tipos de grafos:

- `GrafoDirecionado`: Implementação de grafos direcionados
- `GrafoPonderado`: Implementação de grafos ponderados
- `GrafoBipartido`: Implementação de grafos bipartidos

### Algoritmos Clássicos

O módulo `algoritmos` implementa algoritmos clássicos da teoria dos grafos:

#### Caminhos Mínimos (Dijkstra)

```python
from algoritmos.caminhos import dijkstra, caminho_minimo

# Calcular distâncias a partir de um vértice
distancias, predecessores = dijkstra(grafo, origem)

# Encontrar caminho mínimo entre dois vértices
caminho, distancia = caminho_minimo(grafo, origem, destino)
```

#### Árvores Geradoras Mínimas (Kruskal)

```python
from algoritmos.arvores import kruskal, arvore_geradora_minima

# Encontrar árvore geradora mínima
arestas_arvore, peso_total = arvore_geradora_minima(grafo)

# Criar subgrafo contendo apenas a árvore geradora mínima
from algoritmos.arvores import criar_subgrafo_arvore_geradora
subgrafo_arvore = criar_subgrafo_arvore_geradora(grafo, arestas_arvore)
```

#### Fluxo em Redes (Ford-Fulkerson)

```python
from algoritmos.fluxo import ford_fulkerson, fluxo_maximo

# Calcular fluxo máximo em uma rede
fluxos, valor_fluxo = fluxo_maximo(grafo, fonte, sumidouro)

# Encontrar corte mínimo
from algoritmos.fluxo import corte_minimo
conjunto_fonte, conjunto_sumidouro, capacidade_corte = corte_minimo(grafo, fonte, sumidouro)
```

### Operações entre Grafos

O módulo `operacoes` implementa operações entre grafos:

```python
from operacoes import uniao_grafos, intersecao_grafos, diferenca_grafos

# União de grafos
grafo_uniao = uniao_grafos(grafo1, grafo2)

# Interseção de grafos
grafo_intersecao = intersecao_grafos(grafo1, grafo2)

# Diferença de grafos
grafo_diferenca = diferenca_grafos(grafo1, grafo2)

# Diferença simétrica de grafos
from operacoes import diferenca_simetrica_grafos
grafo_dif_simetrica = diferenca_simetrica_grafos(grafo1, grafo2)

# Composição de grafos
from operacoes import composicao_grafos
grafo_composicao = composicao_grafos(grafo1, grafo2)
```

### Persistência de Grafos

O módulo `persistencia` implementa funções para importação e exportação de grafos em formatos padrão:

#### Exportação

```python
from persistencia import exportar_graphml, exportar_gml, exportar_gexf, exportar_json, exportar_csv

# Exportar para GraphML
exportar_graphml(grafo, "caminho/para/arquivo.graphml")

# Exportar para GML
exportar_gml(grafo, "caminho/para/arquivo.gml")

# Exportar para GEXF
exportar_gexf(grafo, "caminho/para/arquivo.gexf")

# Exportar para JSON
exportar_json(grafo, "caminho/para/arquivo.json")

# Exportar para CSV (lista de arestas)
exportar_csv(grafo, "caminho/para/arquivo.csv", formato="lista")

# Exportar para CSV (matriz de adjacência)
exportar_csv(grafo, "caminho/para/arquivo.csv", formato="matriz")
```

#### Importação

```python
from persistencia import importar_graphml, importar_gml, importar_gexf, importar_json, importar_csv

# Importar de GraphML
grafo = importar_graphml("caminho/para/arquivo.graphml")

# Importar de GML
grafo = importar_gml("caminho/para/arquivo.gml")

# Importar de GEXF
grafo = importar_gexf("caminho/para/arquivo.gexf")

# Importar de JSON
grafo = importar_json("caminho/para/arquivo.json")

# Importar de CSV (lista de arestas)
grafo = importar_csv("caminho/para/arquivo.csv", formato="lista")

# Importar de CSV (matriz de adjacência)
grafo = importar_csv("caminho/para/arquivo.csv", formato="matriz")
```

### Comparação e Isomorfismo de Grafos

O módulo `comparacao` implementa funções para comparação e isomorfismo de grafos:

#### Isomorfismo

```python
from comparacao import verificar_isomorfismo, encontrar_mapeamento_isomorfismo

# Verificar se dois grafos são isomorfos
resultado = verificar_isomorfismo(grafo1, grafo2)

# Encontrar mapeamento de isomorfismo
mapeamento = encontrar_mapeamento_isomorfismo(grafo1, grafo2)

# Verificar isomorfismo considerando atributos
from comparacao import verificar_isomorfismo_com_atributos
resultado = verificar_isomorfismo_com_atributos(grafo1, grafo2, 
                                              atributos_vertice=["cor", "peso"],
                                              atributos_aresta=["tipo"])

# Encontrar automorfismos
from comparacao import encontrar_automorfismos
automorfismos = encontrar_automorfismos(grafo)

# Calcular invariantes
from comparacao import calcular_invariantes
invariantes = calcular_invariantes(grafo)
```

#### Similaridade

```python
from comparacao import similaridade_estrutural, similaridade_espectral, distancia_edicao

# Calcular similaridade estrutural
sim = similaridade_estrutural(grafo1, grafo2)

# Calcular similaridade espectral
sim = similaridade_espectral(grafo1, grafo2)

# Calcular distância de edição
dist = distancia_edicao(grafo1, grafo2)

# Calcular matriz de similaridade
from comparacao import matriz_similaridade
matriz = matriz_similaridade([grafo1, grafo2, grafo3], metrica="estrutural")
```

#### Subgrafos

```python
from comparacao import verificar_subgrafo, verificar_subgrafo_induzido, criar_subgrafo_induzido

# Verificar se um grafo é subgrafo de outro
resultado = verificar_subgrafo(grafo, subgrafo)

# Verificar se um grafo é subgrafo induzido de outro
resultado = verificar_subgrafo_induzido(grafo, subgrafo)

# Criar subgrafo induzido
subgrafo = criar_subgrafo_induzido(grafo, [v1, v2, v3])

# Encontrar subgrafo isomorfo
from comparacao import encontrar_subgrafo_isomorfo
mapeamentos = encontrar_subgrafo_isomorfo(grafo, padrao)

# Encontrar cliques maximais
from comparacao import encontrar_cliques_maximais
cliques = encontrar_cliques_maximais(grafo, tamanho_minimo=3)

# Encontrar componentes conexos
from comparacao import encontrar_componentes_conexos
componentes = encontrar_componentes_conexos(grafo)
```

## Exemplos de Uso

### Criação de Grafos

```python
from core import Grafo
from tipos import GrafoPonderado, GrafoDirecionado, GrafoBipartido

# Criar grafo simples
g = Grafo("Meu Grafo")

# Adicionar vértices
g.adicionar_vertice("A", {"cor": "vermelho"})
g.adicionar_vertice("B", {"cor": "azul"})
g.adicionar_vertice("C", {"cor": "verde"})

# Adicionar arestas
g.adicionar_aresta("A", "B", 1.0, {"tipo": "forte"})
g.adicionar_aresta("B", "C", 2.0, {"tipo": "fraca"})
g.adicionar_aresta("C", "A", 3.0, {"tipo": "média"})

# Criar grafo ponderado
g_ponderado = GrafoPonderado("Grafo Ponderado")
g_ponderado.adicionar_vertice(1)
g_ponderado.adicionar_vertice(2)
g_ponderado.adicionar_aresta(1, 2, 5.5)  # Aresta com peso 5.5

# Criar grafo direcionado
g_direcionado = GrafoDirecionado("Grafo Direcionado")
g_direcionado.adicionar_vertice("X")
g_direcionado.adicionar_vertice("Y")
g_direcionado.adicionar_aresta("X", "Y")  # Aresta direcionada de X para Y

# Criar grafo bipartido
g_bipartido = GrafoBipartido("Grafo Bipartido")
g_bipartido.adicionar_vertice("A1", conjunto="A")
g_bipartido.adicionar_vertice("A2", conjunto="A")
g_bipartido.adicionar_vertice("B1", conjunto="B")
g_bipartido.adicionar_vertice("B2", conjunto="B")
g_bipartido.adicionar_aresta("A1", "B1")
g_bipartido.adicionar_aresta("A2", "B2")
```

### Análise de Grafos

```python
# Verificar propriedades básicas
print(f"Número de vértices: {g.numero_vertices()}")
print(f"Número de arestas: {g.numero_arestas()}")
print(f"É conexo: {g.eh_conexo()}")
print(f"É árvore: {g.eh_arvore()}")
print(f"É bipartido: {g.eh_bipartido()}")

# Obter vizinhos de um vértice
vizinhos = g.obter_vizinhos("A")
print(f"Vizinhos de A: {vizinhos}")

# Calcular grau de um vértice
grau = g.calcular_grau("A")
print(f"Grau de A: {grau}")

# Verificar adjacência
adjacente = g.sao_adjacentes("A", "B")
print(f"A e B são adjacentes: {adjacente}")
```

### Aplicação de Algoritmos

```python
# Criar grafo ponderado para teste
g = GrafoPonderado("Grafo de Teste")
for i in range(1, 7):
    g.adicionar_vertice(i)
g.adicionar_aresta(1, 2, 7)
g.adicionar_aresta(1, 3, 9)
g.adicionar_aresta(1, 6, 14)
g.adicionar_aresta(2, 3, 10)
g.adicionar_aresta(2, 4, 15)
g.adicionar_aresta(3, 4, 11)
g.adicionar_aresta(3, 6, 2)
g.adicionar_aresta(4, 5, 6)
g.adicionar_aresta(5, 6, 9)

# Aplicar algoritmo de Dijkstra
from algoritmos.caminhos import dijkstra, caminho_minimo
distancias, predecessores = dijkstra(g, 1)
print(f"Distâncias a partir do vértice 1: {distancias}")

# Encontrar caminho mínimo
caminho, dist = caminho_minimo(g, 1, 5)
print(f"Caminho mínimo de 1 para 5: {caminho}, distância: {dist}")

# Aplicar algoritmo de Kruskal
from algoritmos.arvores import arvore_geradora_minima
arvore, peso_total = arvore_geradora_minima(g)
print(f"Árvore geradora mínima: {arvore}")
print(f"Peso total da árvore: {peso_total}")
```

### Operações entre Grafos

```python
# Criar dois grafos para teste
g1 = Grafo("Grafo 1")
g2 = Grafo("Grafo 2")

# Adicionar vértices e arestas ao grafo 1
for i in range(1, 5):
    g1.adicionar_vertice(i)
g1.adicionar_aresta(1, 2)
g1.adicionar_aresta(2, 3)
g1.adicionar_aresta(3, 4)

# Adicionar vértices e arestas ao grafo 2
for i in range(3, 7):
    g2.adicionar_vertice(i)
g2.adicionar_aresta(3, 4)
g2.adicionar_aresta(4, 5)
g2.adicionar_aresta(5, 6)

# Realizar operações entre grafos
from operacoes import uniao_grafos, intersecao_grafos, diferenca_grafos
g_uniao = uniao_grafos(g1, g2)
g_intersecao = intersecao_grafos(g1, g2)
g_diferenca = diferenca_grafos(g1, g2)

print(f"União: {g_uniao}")
print(f"Interseção: {g_intersecao}")
print(f"Diferença (G1 - G2): {g_diferenca}")
```

### Persistência de Grafos

```python
# Criar grafo para teste
g = Grafo("Grafo para Persistência")
for i in range(1, 5):
    g.adicionar_vertice(i, {"label": f"Vértice {i}"})
g.adicionar_aresta(1, 2, 2.5, {"tipo": "forte"})
g.adicionar_aresta(2, 3, 1.5, {"tipo": "fraca"})
g.adicionar_aresta(3, 4, 3.0, {"tipo": "forte"})
g.adicionar_aresta(4, 1, 2.0, {"tipo": "média"})

# Exportar para diferentes formatos
from persistencia import exportar_graphml, exportar_json, exportar_csv
exportar_graphml(g, "grafo.graphml")
exportar_json(g, "grafo.json")
exportar_csv(g, "grafo_arestas.csv", formato="lista")
exportar_csv(g, "grafo_matriz.csv", formato="matriz")

# Importar de diferentes formatos
from persistencia import importar_graphml, importar_json, importar_csv
g1 = importar_graphml("grafo.graphml")
g2 = importar_json("grafo.json")
g3 = importar_csv("grafo_arestas.csv", formato="lista")
```

### Comparação e Isomorfismo de Grafos

```python
# Criar dois grafos isomorfos com rótulos diferentes
g1 = Grafo("Grafo 1")
g2 = Grafo("Grafo 2")

# Adicionar vértices e arestas ao grafo 1 (ciclo)
for i in range(1, 5):
    g1.adicionar_vertice(i)
g1.adicionar_aresta(1, 2)
g1.adicionar_aresta(2, 3)
g1.adicionar_aresta(3, 4)
g1.adicionar_aresta(4, 1)

# Adicionar vértices e arestas ao grafo 2 (ciclo com mesma estrutura)
for i in range(5, 9):
    g2.adicionar_vertice(i)
g2.adicionar_aresta(5, 6)
g2.adicionar_aresta(6, 7)
g2.adicionar_aresta(7, 8)
g2.adicionar_aresta(8, 5)

# Verificar isomorfismo
from comparacao import verificar_isomorfismo
resultado = verificar_isomorfismo(g1, g2)
print(f"Os grafos são isomorfos? {resultado}")

# Calcular similaridade
from comparacao import similaridade_estrutural
sim = similaridade_estrutural(g1, g2)
print(f"Similaridade estrutural: {sim:.4f}")

# Verificar subgrafo
g_sub = Grafo("Subgrafo")
for i in range(1, 4):
    g_sub.adicionar_vertice(i)
g_sub.adicionar_aresta(1, 2)
g_sub.adicionar_aresta(2, 3)

from comparacao import verificar_subgrafo
resultado = verificar_subgrafo(g1, g_sub)
print(f"g_sub é subgrafo de g1? {resultado}")
```

## Recursos Avançados

### Grafos Ponderados

```python
from tipos import GrafoPonderado

# Criar grafo ponderado
g = GrafoPonderado("Grafo Ponderado")

# Adicionar vértices
for i in range(1, 5):
    g.adicionar_vertice(i)

# Adicionar arestas com pesos
g.adicionar_aresta(1, 2, 3.5)
g.adicionar_aresta(2, 3, 2.0)
g.adicionar_aresta(3, 4, 1.5)
g.adicionar_aresta(4, 1, 4.0)

# Calcular peso total
peso_total = g.calcular_peso_total()
print(f"Peso total: {peso_total}")

# Obter arestas ordenadas por peso
arestas_ordenadas = g.obter_arestas_ordenadas_por_peso()
print(f"Arestas ordenadas por peso: {arestas_ordenadas}")

# Obter arestas com peso mínimo
arestas_min = g.obter_arestas_com_peso_minimo()
print(f"Arestas com peso mínimo: {arestas_min}")

# Obter arestas com peso máximo
arestas_max = g.obter_arestas_com_peso_maximo()
print(f"Arestas com peso máximo: {arestas_max}")
```

### Grafos Bipartidos

```python
from tipos import GrafoBipartido

# Criar grafo bipartido
g = GrafoBipartido("Grafo Bipartido")

# Adicionar vértices aos conjuntos A e B
g.adicionar_vertice('a1', {"tipo": "pessoa"}, 'A')
g.adicionar_vertice('a2', {"tipo": "pessoa"}, 'A')
g.adicionar_vertice('a3', {"tipo": "pessoa"}, 'A')
g.adicionar_vertice('b1', {"tipo": "projeto"}, 'B')
g.adicionar_vertice('b2', {"tipo": "projeto"}, 'B')

# Adicionar arestas entre os conjuntos
g.adicionar_aresta('a1', 'b1')
g.adicionar_aresta('a1', 'b2')
g.adicionar_aresta('a2', 'b1')
g.adicionar_aresta('a3', 'b2')

# Obter conjuntos
conjunto_a = g.obter_conjunto_a()
conjunto_b = g.obter_conjunto_b()
print(f"Conjunto A: {conjunto_a}")
print(f"Conjunto B: {conjunto_b}")

# Verificar conjunto de um vértice
conjunto = g.obter_conjunto_vertice('a1')
print(f"Vértice 'a1' pertence ao conjunto: {conjunto}")

# Encontrar emparelhamento máximo
emparelhamento = g.encontrar_emparelhamento_maximo()
print(f"Emparelhamento máximo: {emparelhamento}")

# Encontrar cobertura mínima
cobertura = g.encontrar_cobertura_minima()
print(f"Cobertura mínima: {cobertura}")
```

### Fluxo em Redes

```python
from tipos import GrafoDirecionado
from algoritmos.fluxo import fluxo_maximo, corte_minimo

# Criar grafo direcionado para teste de fluxo
g = GrafoDirecionado("Rede de Fluxo")

# Adicionar vértices
for v in ['s', 'a', 'b', 't']:
    g.adicionar_vertice(v)

# Adicionar arestas com capacidades
g.adicionar_aresta('s', 'a', 4)  # Capacidade 4
g.adicionar_aresta('s', 'b', 2)  # Capacidade 2
g.adicionar_aresta('a', 'b', 1)  # Capacidade 1
g.adicionar_aresta('a', 't', 3)  # Capacidade 3
g.adicionar_aresta('b', 't', 5)  # Capacidade 5

# Calcular fluxo máximo
fluxos, valor_fluxo = fluxo_maximo(g, 's', 't')
print(f"Fluxo máximo de s para t: {valor_fluxo}")
print(f"Fluxos nas arestas: {fluxos}")

# Encontrar corte mínimo
conjunto_s, conjunto_t, capacidade_corte = corte_minimo(g, 's', 't')
print(f"Conjunto S: {conjunto_s}")
print(f"Conjunto T: {conjunto_t}")
print(f"Capacidade do corte: {capacidade_corte}")
```

## Considerações Finais

Este backend foi desenvolvido para ser uma ferramenta completa para estudo e aplicação da teoria dos grafos, seguindo rigorosamente os princípios matemáticos e oferecendo uma ampla gama de funcionalidades. A implementação é modular e extensível, permitindo a adição de novos recursos e algoritmos conforme necessário.

Para mais informações e exemplos, consulte os arquivos na pasta `exemplos/`.
