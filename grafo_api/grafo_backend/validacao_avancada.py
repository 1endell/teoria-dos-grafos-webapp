"""
Script para validação teórica das funcionalidades avançadas do backend.
Este script testa as implementações avançadas do backend para garantir que estão
de acordo com os princípios da teoria dos grafos.
"""

import sys
import os
import networkx as nx
import matplotlib.pyplot as plt
import tempfile

# Adiciona o diretório pai ao path para importação dos módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .core import Grafo, Vertice, Aresta
from .tipos import GrafoDirecionado, GrafoPonderado, GrafoBipartido
from .algoritmos.caminhos import dijkstra, caminho_minimo
from .algoritmos.arvores import kruskal, arvore_geradora_minima
from .algoritmos.fluxo import ford_fulkerson, fluxo_maximo
from .operacoes import uniao_grafos, intersecao_grafos, diferenca_grafos
from .persistencia import (
    exportar_graphml, importar_graphml,
    exportar_json, importar_json,
    exportar_csv, importar_csv
)
from .comparacao import (
    verificar_isomorfismo,
    similaridade_estrutural,
    verificar_subgrafo,
    criar_subgrafo_induzido
)


def validar_algoritmos_classicos():
    """
    Valida os algoritmos clássicos implementados.
    """
    print("\n=== Validando Algoritmos Clássicos ===")
    
    # Criação de grafo ponderado para testes
    g = GrafoPonderado("Grafo de Teste para Algoritmos")
    
    # Adiciona vértices
    for i in range(1, 7):
        g.adicionar_vertice(i)
    
    # Adiciona arestas com pesos
    g.adicionar_aresta(1, 2, 7)
    g.adicionar_aresta(1, 3, 9)
    g.adicionar_aresta(1, 6, 14)
    g.adicionar_aresta(2, 3, 10)
    g.adicionar_aresta(2, 4, 15)
    g.adicionar_aresta(3, 4, 11)
    g.adicionar_aresta(3, 6, 2)
    g.adicionar_aresta(4, 5, 6)
    g.adicionar_aresta(5, 6, 9)
    
    print(f"Grafo criado: {g}")
    
    # Teste do algoritmo de Dijkstra
    print("\nTestando algoritmo de Dijkstra:")
    distancias, predecessores = dijkstra(g, 1)
    print(f"Distâncias a partir do vértice 1: {distancias}")
    
    # Verifica se as distâncias estão corretas
    assert distancias[1] == 0, f"Distância de 1 para 1 deve ser 0, obtido {distancias[1]}"
    assert distancias[2] == 7, f"Distância de 1 para 2 deve ser 7, obtido {distancias[2]}"
    assert distancias[3] == 9, f"Distância de 1 para 3 deve ser 9, obtido {distancias[3]}"
    assert distancias[6] == 11, f"Distância de 1 para 6 deve ser 11, obtido {distancias[6]}"
    
    # Teste do caminho mínimo
    caminho, dist = caminho_minimo(g, 1, 5)
    print(f"Caminho mínimo de 1 para 5: {caminho}, distância: {dist}")
    assert dist == 20, f"Distância do caminho mínimo de 1 para 5 deve ser 20, obtido {dist}"
    
    # Teste do algoritmo de Kruskal
    print("\nTestando algoritmo de Kruskal:")
    arvore, peso_total = arvore_geradora_minima(g)
    print(f"Árvore geradora mínima: {arvore}")
    print(f"Peso total da árvore: {peso_total}")
    
    # Verifica se o peso total está correto
    assert peso_total == 33, f"Peso total da árvore geradora mínima deve ser 33, obtido {peso_total}"
    
    # Teste do algoritmo de Ford-Fulkerson
    print("\nTestando algoritmo de Ford-Fulkerson:")
    
    # Cria um grafo direcionado para teste de fluxo
    g_fluxo = GrafoDirecionado("Grafo de Teste para Fluxo")
    
    # Adiciona vértices
    for v in ['s', 'a', 'b', 't']:
        g_fluxo.adicionar_vertice(v)
    
    # Adiciona arestas com capacidades
    g_fluxo.adicionar_aresta('s', 'a', 4)
    g_fluxo.adicionar_aresta('s', 'b', 2)
    g_fluxo.adicionar_aresta('a', 'b', 1)
    g_fluxo.adicionar_aresta('a', 't', 3)
    g_fluxo.adicionar_aresta('b', 't', 5)
    
    # Calcula o fluxo máximo
    fluxos, valor_fluxo = fluxo_maximo(g_fluxo, 's', 't')
    print(f"Fluxo máximo de s para t: {valor_fluxo}")
    print(f"Fluxos nas arestas: {fluxos}")
    
    # Verifica se o fluxo máximo está correto
    assert valor_fluxo == 6, f"Fluxo máximo deve ser 6, obtido {valor_fluxo}"
    
    print("Validação de algoritmos clássicos concluída com sucesso!")
    return True


def validar_tipos_grafos():
    """
    Valida os tipos de grafos implementados.
    """
    print("\n=== Validando Tipos de Grafos ===")
    
    # Teste de grafo ponderado
    print("\nTestando grafo ponderado:")
    g_ponderado = GrafoPonderado("Grafo Ponderado de Teste")
    
    # Adiciona vértices
    for i in range(1, 5):
        g_ponderado.adicionar_vertice(i)
    
    # Adiciona arestas com pesos
    g_ponderado.adicionar_aresta(1, 2, 3.5)
    g_ponderado.adicionar_aresta(2, 3, 2.0)
    g_ponderado.adicionar_aresta(3, 4, 1.5)
    g_ponderado.adicionar_aresta(4, 1, 4.0)
    
    print(f"Grafo ponderado: {g_ponderado}")
    print(f"Peso total: {g_ponderado.calcular_peso_total()}")
    
    # Verifica se o peso total está correto
    assert g_ponderado.calcular_peso_total() == 11.0, f"Peso total deve ser 11.0, obtido {g_ponderado.calcular_peso_total()}"
    
    # Obtém arestas ordenadas por peso
    arestas_ordenadas = g_ponderado.obter_arestas_ordenadas_por_peso()
    print(f"Arestas ordenadas por peso: {arestas_ordenadas}")
    
    # Verifica se a ordenação está correta
    assert arestas_ordenadas[0][2] == 1.5, f"Aresta com menor peso deve ter peso 1.5, obtido {arestas_ordenadas[0][2]}"
    
    # Teste de grafo bipartido
    print("\nTestando grafo bipartido:")
    g_bipartido = GrafoBipartido("Grafo Bipartido de Teste")
    
    # Adiciona vértices aos conjuntos A e B
    g_bipartido.adicionar_vertice('a1', {"tipo": "pessoa"}, 'A')
    g_bipartido.adicionar_vertice('a2', {"tipo": "pessoa"}, 'A')
    g_bipartido.adicionar_vertice('a3', {"tipo": "pessoa"}, 'A')
    g_bipartido.adicionar_vertice('b1', {"tipo": "projeto"}, 'B')
    g_bipartido.adicionar_vertice('b2', {"tipo": "projeto"}, 'B')
    
    # Adiciona arestas entre os conjuntos
    g_bipartido.adicionar_aresta('a1', 'b1')
    g_bipartido.adicionar_aresta('a1', 'b2')
    g_bipartido.adicionar_aresta('a2', 'b1')
    g_bipartido.adicionar_aresta('a3', 'b2')
    
    print(f"Grafo bipartido: {g_bipartido}")
    print(f"Conjunto A: {g_bipartido.obter_conjunto_a()}")
    print(f"Conjunto B: {g_bipartido.obter_conjunto_b()}")
    
    # Verifica se os conjuntos estão corretos
    assert len(g_bipartido.obter_conjunto_a()) == 3, f"Conjunto A deve ter 3 vértices, obtido {len(g_bipartido.obter_conjunto_a())}"
    assert len(g_bipartido.obter_conjunto_b()) == 2, f"Conjunto B deve ter 2 vértices, obtido {len(g_bipartido.obter_conjunto_b())}"
    
    # Testa emparelhamento máximo
    emparelhamento = g_bipartido.encontrar_emparelhamento_maximo()
    print(f"Emparelhamento máximo: {emparelhamento}")
    
    # Verifica se o emparelhamento tem o tamanho correto
    assert len(emparelhamento) // 2 == 2, f"Emparelhamento máximo deve ter 2 arestas, obtido {len(emparelhamento) // 2}"
    
    # Tenta adicionar uma aresta inválida (entre vértices do mesmo conjunto)
    try:
        g_bipartido.adicionar_aresta('a1', 'a2')
        assert False, "Deveria ter lançado uma exceção ao adicionar aresta entre vértices do mesmo conjunto"
    except ValueError:
        pass  # Exceção esperada
    
    print("Validação de tipos de grafos concluída com sucesso!")
    return True


def validar_operacoes_grafos():
    """
    Valida as operações entre grafos.
    """
    print("\n=== Validando Operações entre Grafos ===")
    
    # Cria dois grafos para teste
    g1 = Grafo("Grafo 1")
    g2 = Grafo("Grafo 2")
    
    # Adiciona vértices ao grafo 1
    for i in range(1, 5):
        g1.adicionar_vertice(i)
    
    # Adiciona arestas ao grafo 1
    g1.adicionar_aresta(1, 2)
    g1.adicionar_aresta(2, 3)
    g1.adicionar_aresta(3, 4)
    
    # Adiciona vértices ao grafo 2
    for i in range(3, 7):
        g2.adicionar_vertice(i)
    
    # Adiciona arestas ao grafo 2
    g2.adicionar_aresta(3, 4)
    g2.adicionar_aresta(4, 5)
    g2.adicionar_aresta(5, 6)
    
    print(f"Grafo 1: {g1}")
    print(f"Grafo 2: {g2}")
    
    # Teste de união de grafos
    g_uniao = uniao_grafos(g1, g2)
    print(f"\nUnião: {g_uniao}")
    
    # Verifica se a união tem o número correto de vértices e arestas
    assert g_uniao.numero_vertices() == 6, f"União deve ter 6 vértices, obtido {g_uniao.numero_vertices()}"
    assert g_uniao.numero_arestas() == 5, f"União deve ter 5 arestas, obtido {g_uniao.numero_arestas()}"
    
    # Teste de interseção de grafos
    g_intersecao = intersecao_grafos(g1, g2)
    print(f"Interseção: {g_intersecao}")
    
    # Verifica se a interseção tem o número correto de vértices e arestas
    assert g_intersecao.numero_vertices() == 2, f"Interseção deve ter 2 vértices, obtido {g_intersecao.numero_vertices()}"
    assert g_intersecao.numero_arestas() == 1, f"Interseção deve ter 1 aresta, obtido {g_intersecao.numero_arestas()}"
    
    # Teste de diferença de grafos
    g_diferenca = diferenca_grafos(g1, g2)
    print(f"Diferença (G1 - G2): {g_diferenca}")
    
    # Verifica se a diferença tem o número correto de vértices e arestas
    assert g_diferenca.numero_vertices() == 4, f"Diferença deve ter 4 vértices, obtido {g_diferenca.numero_vertices()}"
    assert g_diferenca.numero_arestas() == 2, f"Diferença deve ter 2 arestas, obtido {g_diferenca.numero_arestas()}"
    
    print("Validação de operações entre grafos concluída com sucesso!")
    return True


def validar_persistencia():
    """
    Valida a persistência de grafos em diferentes formatos.
    """
    print("\n=== Validando Persistência de Grafos ===")
    
    # Cria um grafo para teste
    g = Grafo("Grafo para Persistência")
    
    # Adiciona vértices
    for i in range(1, 5):
        g.adicionar_vertice(i, {"label": f"Vértice {i}"})
    
    # Adiciona arestas
    g.adicionar_aresta(1, 2, 2.5, {"tipo": "forte"})
    g.adicionar_aresta(2, 3, 1.5, {"tipo": "fraca"})
    g.adicionar_aresta(3, 4, 3.0, {"tipo": "forte"})
    g.adicionar_aresta(4, 1, 2.0, {"tipo": "média"})
    
    print(f"Grafo original: {g}")
    
    # Cria diretório temporário para os arquivos
    with tempfile.TemporaryDirectory() as temp_dir:
        # Teste de exportação/importação GraphML
        graphml_path = os.path.join(temp_dir, "grafo.graphml")
        print(f"\nTestando persistência em GraphML: {graphml_path}")
        
        # Exporta para GraphML
        exportar_graphml(g, graphml_path)
        assert os.path.exists(graphml_path), f"Arquivo GraphML não foi criado: {graphml_path}"
        
        # Importa de GraphML
        g_importado = importar_graphml(graphml_path)
        print(f"Grafo importado de GraphML: {g_importado}")
        
        # Verifica se o grafo importado tem o mesmo número de vértices e arestas
        assert g_importado.numero_vertices() == g.numero_vertices(), "Número de vértices diferente após importação de GraphML"
        assert g_importado.numero_arestas() == g.numero_arestas(), "Número de arestas diferente após importação de GraphML"
        
        # Teste de exportação/importação JSON
        json_path = os.path.join(temp_dir, "grafo.json")
        print(f"\nTestando persistência em JSON: {json_path}")
        
        # Exporta para JSON
        exportar_json(g, json_path)
        assert os.path.exists(json_path), f"Arquivo JSON não foi criado: {json_path}"
        
        # Importa de JSON
        g_importado = importar_json(json_path)
        print(f"Grafo importado de JSON: {g_importado}")
        
        # Verifica se o grafo importado tem o mesmo número de vértices e arestas
        assert g_importado.numero_vertices() == g.numero_vertices(), "Número de vértices diferente após importação de JSON"
        assert g_importado.numero_arestas() == g.numero_arestas(), "Número de arestas diferente após importação de JSON"
        
        # Teste de exportação/importação CSV
        csv_path = os.path.join(temp_dir, "grafo.csv")
        print(f"\nTestando persistência em CSV: {csv_path}")
        
        # Exporta para CSV (lista de arestas)
        exportar_csv(g, csv_path, formato='lista')
        assert os.path.exists(csv_path), f"Arquivo CSV não foi criado: {csv_path}"
        
        # Importa de CSV
        g_importado = importar_csv(csv_path, formato='lista')
        print(f"Grafo importado de CSV: {g_importado}")
        
        # Verifica se o grafo importado tem o mesmo número de vértices e arestas
        assert g_importado.numero_vertices() == g.numero_vertices(), "Número de vértices diferente após importação de CSV"
        assert g_importado.numero_arestas() == g.numero_arestas(), "Número de arestas diferente após importação de CSV"
    
    print("Validação de persistência concluída com sucesso!")
    return True


def validar_comparacao():
    """
    Valida as funcionalidades de comparação e isomorfismo de grafos.
    """
    print("\n=== Validando Comparação e Isomorfismo de Grafos ===")
    
    # Cria dois grafos isomorfos com rótulos diferentes
    g1 = Grafo("Grafo 1")
    g2 = Grafo("Grafo 2")
    
    # Adiciona vértices ao grafo 1
    for i in range(1, 5):
        g1.adicionar_vertice(i)
    
    # Adiciona arestas ao grafo 1 (ciclo)
    g1.adicionar_aresta(1, 2)
    g1.adicionar_aresta(2, 3)
    g1.adicionar_aresta(3, 4)
    g1.adicionar_aresta(4, 1)
    
    # Adiciona vértices ao grafo 2 com rótulos diferentes
    for i in range(5, 9):
        g2.adicionar_vertice(i)
    
    # Adiciona arestas ao grafo 2 (ciclo com mesma estrutura)
    g2.adicionar_aresta(5, 6)
    g2.adicionar_aresta(6, 7)
    g2.adicionar_aresta(7, 8)
    g2.adicionar_aresta(8, 5)
    
    print(f"Grafo 1: {g1}")
    print(f"Grafo 2: {g2}")
    
    # Teste de isomorfismo
    resultado = verificar_isomorfismo(g1, g2)
    print(f"\nOs grafos são isomorfos? {resultado}")
    
    # Verifica se os grafos são isomorfos
    assert resultado == True, "Os grafos deveriam ser isomorfos"
    
    # Cria um terceiro grafo não isomorfo
    g3 = Grafo("Grafo 3")
    
    # Adiciona vértices ao grafo 3
    for i in range(1, 5):
        g3.adicionar_vertice(i)
    
    # Adiciona arestas ao grafo 3 (estrutura diferente)
    g3.adicionar_aresta(1, 2)
    g3.adicionar_aresta(1, 3)
    g3.adicionar_aresta(1, 4)
    g3.adicionar_aresta(2, 3)
    
    print(f"Grafo 3: {g3}")
    
    # Teste de isomorfismo com grafo não isomorfo
    resultado = verificar_isomorfismo(g1, g3)
    print(f"Grafo 1 e Grafo 3 são isomorfos? {resultado}")
    
    # Verifica se os grafos não são isomorfos
    assert resultado == False, "Os grafos não deveriam ser isomorfos"
    
    # Teste de similaridade estrutural
    sim = similaridade_estrutural(g1, g3)
    print(f"\nSimilaridade estrutural entre Grafo 1 e Grafo 3: {sim:.4f}")
    
    # Verifica se a similaridade está no intervalo [0, 1]
    assert 0 <= sim <= 1, f"Similaridade deve estar entre 0 e 1, obtido {sim}"
    
    # Teste de subgrafo
    g_sub = Grafo("Subgrafo")
    
    # Adiciona vértices ao subgrafo
    for i in range(1, 4):
        g_sub.adicionar_vertice(i)
    
    # Adiciona arestas ao subgrafo
    g_sub.adicionar_aresta(1, 2)
    g_sub.adicionar_aresta(2, 3)
    
    print(f"\nSubgrafo: {g_sub}")
    
    # Teste de verificação de subgrafo
    resultado = verificar_subgrafo(g1, g_sub)
    print(f"g_sub é subgrafo de g1? {resultado}")
    
    # Verifica se é subgrafo
    assert resultado == True, "g_sub deveria ser subgrafo de g1"
    
    # Teste de criação de subgrafo induzido
    subgrafo_induzido = criar_subgrafo_induzido(g1, [1, 2, 3])
    print(f"\nSubgrafo induzido de g1: {subgrafo_induzido}")
    
    # Verifica se o subgrafo induzido tem o número correto de vértices e arestas
    assert subgrafo_induzido.numero_vertices() == 3, f"Subgrafo induzido deve ter 3 vértices, obtido {subgrafo_induzido.numero_vertices()}"
    assert subgrafo_induzido.numero_arestas() == 2, f"Subgrafo induzido deve ter 2 arestas, obtido {subgrafo_induzido.numero_arestas()}"
    
    print("Validação de comparação e isomorfismo concluída com sucesso!")
    return True


def validar_funcionalidades_avancadas():
    """
    Função principal para validação das funcionalidades avançadas.
    """
    print("Iniciando validação das funcionalidades avançadas...")
    
    try:
        validar_algoritmos_classicos()
        validar_tipos_grafos()
        validar_operacoes_grafos()
        validar_persistencia()
        validar_comparacao()
        
        print("\nTodos os testes de funcionalidades avançadas foram concluídos com sucesso!")
        print("O backend expandido está em conformidade com os princípios da teoria dos grafos.")
        return True
    except AssertionError as e:
        print(f"\nFalha na validação: {e}")
        return False


if __name__ == "__main__":
    validar_funcionalidades_avancadas()
