"""
Script para validação da conformidade teórica das implementações.
Este script testa as implementações do backend para garantir que estão
de acordo com os princípios da teoria dos grafos.
"""

import sys
import os
import networkx as nx
import matplotlib.pyplot as plt

# Adiciona o diretório pai ao path para importação dos módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import Grafo, Vertice, Aresta
from tipos import GrafoDirecionado


def validar_grafo_basico():
    """
    Valida as operações básicas de um grafo não direcionado.
    """
    print("Validando operações básicas de um grafo não direcionado...")
    
    # Criação de grafo
    g = Grafo("Grafo de Teste")
    assert g.eh_vazio() == True, "Grafo recém-criado deve estar vazio"
    
    # Adição de vértices
    g.adicionar_vertice(1, {"cor": "vermelho"})
    g.adicionar_vertice(2, {"cor": "azul"})
    g.adicionar_vertice(3, {"cor": "verde"})
    
    assert g.numero_vertices() == 3, "Grafo deve ter 3 vértices"
    assert g.eh_vazio() == False, "Grafo não deve estar vazio após adição de vértices"
    assert g.eh_trivial() == False, "Grafo com 3 vértices não é trivial"
    
    # Adição de arestas
    g.adicionar_aresta(1, 2, 2.5, {"tipo": "amizade"})
    g.adicionar_aresta(2, 3, 1.5)
    
    assert g.numero_arestas() == 2, "Grafo deve ter 2 arestas"
    assert g.existe_aresta(1, 2) == True, "Deve existir aresta entre 1 e 2"
    assert g.existe_aresta(2, 1) == True, "Em grafo não direcionado, aresta (1,2) implica aresta (2,1)"
    assert g.obter_peso_aresta(1, 2) == 2.5, "Peso da aresta (1,2) deve ser 2.5"
    
    # Verificação de atributos
    assert g.obter_atributos_vertice(1)["cor"] == "vermelho", "Atributo 'cor' do vértice 1 deve ser 'vermelho'"
    assert g.obter_atributos_aresta(1, 2)["tipo"] == "amizade", "Atributo 'tipo' da aresta (1,2) deve ser 'amizade'"
    
    # Verificação de adjacência
    adjacentes_2 = g.obter_adjacentes(2)
    assert 1 in adjacentes_2 and 3 in adjacentes_2, "Vértice 2 deve ser adjacente a 1 e 3"
    assert g.obter_grau(2) == 2, "Grau do vértice 2 deve ser 2"
    
    # Remoção de aresta
    g.remover_aresta(1, 2)
    assert g.numero_arestas() == 1, "Grafo deve ter 1 aresta após remoção"
    assert g.existe_aresta(1, 2) == False, "Não deve existir aresta entre 1 e 2 após remoção"
    
    # Remoção de vértice
    g.remover_vertice(3)
    assert g.numero_vertices() == 2, "Grafo deve ter 2 vértices após remoção"
    assert g.numero_arestas() == 0, "Grafo não deve ter arestas após remoção do vértice 3"
    
    print("Validação de grafo básico concluída com sucesso!")


def validar_grafo_direcionado():
    """
    Valida as operações específicas de um grafo direcionado.
    """
    print("Validando operações específicas de um grafo direcionado...")
    
    # Criação de grafo direcionado
    g = GrafoDirecionado("Grafo Direcionado de Teste")
    
    # Adição de vértices
    g.adicionar_vertice(1)
    g.adicionar_vertice(2)
    g.adicionar_vertice(3)
    g.adicionar_vertice(4)
    
    # Adição de arestas direcionadas
    g.adicionar_aresta(1, 2)
    g.adicionar_aresta(2, 3)
    g.adicionar_aresta(3, 1)  # Ciclo 1->2->3->1
    g.adicionar_aresta(4, 1)
    
    assert g.numero_arestas() == 4, "Grafo direcionado deve ter 4 arestas"
    assert g.existe_aresta(1, 2) == True, "Deve existir aresta de 1 para 2"
    assert g.existe_aresta(2, 1) == False, "Não deve existir aresta de 2 para 1"
    
    # Verificação de graus de entrada e saída
    assert g.obter_grau_entrada(1) == 2, "Grau de entrada do vértice 1 deve ser 2"
    assert g.obter_grau_saida(1) == 1, "Grau de saída do vértice 1 deve ser 1"
    
    # Verificação de predecessores e sucessores
    assert set(g.obter_predecessores(1)) == {3, 4}, "Predecessores de 1 devem ser 3 e 4"
    assert set(g.obter_sucessores(1)) == {2}, "Sucessor de 1 deve ser 2"
    
    # Verificação de conectividade
    assert g.eh_fortemente_conexo() == False, "Grafo não deve ser fortemente conexo"
    
    # Adicionando aresta para tornar fortemente conexo
    g.adicionar_aresta(1, 4)
    assert g.eh_fortemente_conexo() == True, "Grafo deve ser fortemente conexo após adição da aresta"
    
    # Componentes fortemente conexos
    g.remover_aresta(1, 4)
    componentes = g.obter_componentes_fortemente_conexos()
    assert len(componentes) == 2, "Grafo deve ter 2 componentes fortemente conexos"
    
    print("Validação de grafo direcionado concluída com sucesso!")


def validar_propriedades_teoricas():
    """
    Valida propriedades teóricas dos grafos implementados.
    """
    print("Validando propriedades teóricas dos grafos...")
    
    # Grafo completo K4
    g = Grafo("K4")
    for i in range(1, 5):
        g.adicionar_vertice(i)
    
    for i in range(1, 5):
        for j in range(i+1, 5):
            g.adicionar_aresta(i, j)
    
    # Verificações teóricas para K4
    assert g.numero_vertices() == 4, "K4 deve ter 4 vértices"
    assert g.numero_arestas() == 6, "K4 deve ter 6 arestas (n*(n-1)/2 = 4*3/2 = 6)"
    assert g.eh_conexo() == True, "K4 deve ser conexo"
    
    for i in range(1, 5):
        assert g.obter_grau(i) == 3, f"Cada vértice em K4 deve ter grau 3, vértice {i} tem grau {g.obter_grau(i)}"
    
    # Grafo bipartido completo K2,3
    g = Grafo("K2,3")
    # Conjunto X: {1, 2}
    g.adicionar_vertice(1, {"conjunto": "X"})
    g.adicionar_vertice(2, {"conjunto": "X"})
    # Conjunto Y: {3, 4, 5}
    g.adicionar_vertice(3, {"conjunto": "Y"})
    g.adicionar_vertice(4, {"conjunto": "Y"})
    g.adicionar_vertice(5, {"conjunto": "Y"})
    
    # Adiciona arestas entre todos os vértices de X e Y
    for i in range(1, 3):
        for j in range(3, 6):
            g.adicionar_aresta(i, j)
    
    # Verificações teóricas para K2,3
    assert g.numero_vertices() == 5, "K2,3 deve ter 5 vértices"
    assert g.numero_arestas() == 6, "K2,3 deve ter 6 arestas (2*3 = 6)"
    assert g.eh_conexo() == True, "K2,3 deve ser conexo"
    
    assert g.obter_grau(1) == 3, "Vértice 1 deve ter grau 3"
    assert g.obter_grau(2) == 3, "Vértice 2 deve ter grau 3"
    assert g.obter_grau(3) == 2, "Vértice 3 deve ter grau 2"
    assert g.obter_grau(4) == 2, "Vértice 4 deve ter grau 2"
    assert g.obter_grau(5) == 2, "Vértice 5 deve ter grau 2"
    
    # Grafo ciclo C5
    g = Grafo("C5")
    for i in range(1, 6):
        g.adicionar_vertice(i)
    
    g.adicionar_aresta(1, 2)
    g.adicionar_aresta(2, 3)
    g.adicionar_aresta(3, 4)
    g.adicionar_aresta(4, 5)
    g.adicionar_aresta(5, 1)
    
    # Verificações teóricas para C5
    assert g.numero_vertices() == 5, "C5 deve ter 5 vértices"
    assert g.numero_arestas() == 5, "C5 deve ter 5 arestas"
    assert g.eh_conexo() == True, "C5 deve ser conexo"
    
    for i in range(1, 6):
        assert g.obter_grau(i) == 2, f"Cada vértice em C5 deve ter grau 2, vértice {i} tem grau {g.obter_grau(i)}"
    
    print("Validação de propriedades teóricas concluída com sucesso!")


def validar_visualizacao():
    """
    Valida a funcionalidade de visualização de grafos.
    """
    print("Validando visualização de grafos...")
    
    # Cria um grafo para visualização
    g = Grafo("Grafo para Visualização")
    
    # Adiciona vértices
    for i in range(1, 6):
        g.adicionar_vertice(i)
    
    # Adiciona arestas com pesos diferentes
    g.adicionar_aresta(1, 2, 2.5)
    g.adicionar_aresta(1, 3, 1.8)
    g.adicionar_aresta(2, 4, 3.1)
    g.adicionar_aresta(3, 4, 2.0)
    g.adicionar_aresta(3, 5, 1.5)
    g.adicionar_aresta(4, 5, 2.2)
    
    # Testa diferentes layouts
    layouts = ["spring", "circular", "random", "shell", "kamada_kawai", "spectral"]
    
    for layout in layouts:
        print(f"Testando layout: {layout}")
        g.visualizar(titulo=f"Grafo com layout {layout}", layout=layout, mostrar=False, 
                    salvar_como=f"/home/ubuntu/grafo_backend/grafo_{layout}.png")
    
    print("Validação de visualização concluída com sucesso!")


def validar_conformidade_teorica():
    """
    Função principal para validação da conformidade teórica.
    """
    print("Iniciando validação de conformidade teórica...")
    
    try:
        validar_grafo_basico()
        validar_grafo_direcionado()
        validar_propriedades_teoricas()
        validar_visualizacao()
        
        print("\nTodos os testes de conformidade teórica foram concluídos com sucesso!")
        print("O backend está em conformidade com os princípios da teoria dos grafos.")
        return True
    except AssertionError as e:
        print(f"\nFalha na validação: {e}")
        return False


if __name__ == "__main__":
    validar_conformidade_teorica()
