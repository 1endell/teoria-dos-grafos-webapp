"""
Módulo de exemplos básicos de uso do backend para estudo de teoria dos grafos.
"""

import sys
import os
import matplotlib.pyplot as plt

# Adiciona o diretório pai ao path para importação dos módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ..core import Grafo
from ..tipos import GrafoDirecionado


def exemplo_grafo_simples():
    """
    Exemplo de criação e manipulação de um grafo simples não direcionado.
    """
    print("\n=== Exemplo: Grafo Simples Não Direcionado ===")
    
    # Criação do grafo
    g = Grafo("Grafo de Amizades")
    
    # Adição de vértices (pessoas)
    g.adicionar_vertice("Alice", {"idade": 25, "cidade": "São Paulo"})
    g.adicionar_vertice("Bob", {"idade": 30, "cidade": "Rio de Janeiro"})
    g.adicionar_vertice("Carlos", {"idade": 28, "cidade": "Belo Horizonte"})
    g.adicionar_vertice("Diana", {"idade": 22, "cidade": "Brasília"})
    g.adicionar_vertice("Eduardo", {"idade": 35, "cidade": "São Paulo"})
    
    print(f"Grafo criado: {g}")
    print(f"Número de vértices: {g.numero_vertices()}")
    
    # Adição de arestas (amizades) com pesos representando a "força" da amizade
    g.adicionar_aresta("Alice", "Bob", 0.8, {"tipo": "trabalho"})
    g.adicionar_aresta("Alice", "Carlos", 0.6, {"tipo": "escola"})
    g.adicionar_aresta("Bob", "Diana", 0.9, {"tipo": "família"})
    g.adicionar_aresta("Carlos", "Diana", 0.7, {"tipo": "trabalho"})
    g.adicionar_aresta("Diana", "Eduardo", 0.5, {"tipo": "online"})
    
    print(f"Número de arestas: {g.numero_arestas()}")
    
    # Verificação de propriedades
    print(f"O grafo é conexo? {g.eh_conexo()}")
    
    # Informações sobre vértices
    for pessoa in g.obter_vertices():
        atributos = g.obter_atributos_vertice(pessoa)
        adjacentes = g.obter_adjacentes(pessoa)
        print(f"{pessoa}: {atributos['idade']} anos, {atributos['cidade']}, "
              f"Amigos: {adjacentes}, Grau: {g.obter_grau(pessoa)}")
    
    # Informações sobre arestas
    print("\nRelações de amizade:")
    for origem, destino, atributos in g.obter_arestas():
        peso = atributos.get('weight', 1.0)
        tipo = atributos.get('tipo', 'desconhecido')
        print(f"{origem} -- {destino}: força {peso:.1f}, tipo: {tipo}")
    
    # Visualização do grafo
    g.visualizar(titulo="Grafo de Amizades", layout="spring", 
                salvar_como="/home/ubuntu/grafo_backend/exemplos/grafo_amizades.png")
    
    print(f"Visualização salva em: /home/ubuntu/grafo_backend/exemplos/grafo_amizades.png")
    
    return g


def exemplo_grafo_direcionado():
    """
    Exemplo de criação e manipulação de um grafo direcionado.
    """
    print("\n=== Exemplo: Grafo Direcionado de Dependências ===")
    
    # Criação do grafo direcionado
    g = GrafoDirecionado("Grafo de Dependências de Disciplinas")
    
    # Adição de vértices (disciplinas)
    g.adicionar_vertice("Cálculo I", {"semestre": 1, "creditos": 4})
    g.adicionar_vertice("Álgebra Linear", {"semestre": 1, "creditos": 4})
    g.adicionar_vertice("Programação I", {"semestre": 1, "creditos": 4})
    g.adicionar_vertice("Cálculo II", {"semestre": 2, "creditos": 4})
    g.adicionar_vertice("Estruturas de Dados", {"semestre": 2, "creditos": 4})
    g.adicionar_vertice("Teoria dos Grafos", {"semestre": 3, "creditos": 4})
    g.adicionar_vertice("Algoritmos", {"semestre": 3, "creditos": 4})
    
    print(f"Grafo criado: {g}")
    print(f"Número de vértices: {g.numero_vertices()}")
    
    # Adição de arestas direcionadas (pré-requisitos)
    g.adicionar_aresta("Cálculo I", "Cálculo II", 1.0, {"tipo": "obrigatório"})
    g.adicionar_aresta("Programação I", "Estruturas de Dados", 1.0, {"tipo": "obrigatório"})
    g.adicionar_aresta("Estruturas de Dados", "Algoritmos", 1.0, {"tipo": "obrigatório"})
    g.adicionar_aresta("Álgebra Linear", "Teoria dos Grafos", 1.0, {"tipo": "obrigatório"})
    g.adicionar_aresta("Estruturas de Dados", "Teoria dos Grafos", 1.0, {"tipo": "obrigatório"})
    
    print(f"Número de arestas: {g.numero_arestas()}")
    
    # Verificação de propriedades específicas de grafos direcionados
    print(f"O grafo é fortemente conexo? {g.eh_fortemente_conexo()}")
    print(f"O grafo é fracamente conexo? {g.eh_fracamente_conexo()}")
    
    # Informações sobre vértices
    print("\nInformações sobre as disciplinas:")
    for disciplina in g.obter_vertices():
        atributos = g.obter_atributos_vertice(disciplina)
        predecessores = g.obter_predecessores(disciplina)
        sucessores = g.obter_sucessores(disciplina)
        
        print(f"{disciplina} (Semestre {atributos['semestre']}, {atributos['creditos']} créditos):")
        print(f"  Pré-requisitos: {predecessores}")
        print(f"  É pré-requisito para: {sucessores}")
        print(f"  Grau de entrada: {g.obter_grau_entrada(disciplina)}")
        print(f"  Grau de saída: {g.obter_grau_saida(disciplina)}")
    
    # Componentes fortemente conexos
    componentes = g.obter_componentes_fortemente_conexos()
    print(f"\nComponentes fortemente conexos: {len(componentes)}")
    for i, componente in enumerate(componentes):
        print(f"  Componente {i+1}: {componente}")
    
    # Visualização do grafo
    g.visualizar(titulo="Grafo de Dependências de Disciplinas", layout="dot", 
                salvar_como="/home/ubuntu/grafo_backend/exemplos/grafo_dependencias.png")
    
    print(f"Visualização salva em: /home/ubuntu/grafo_backend/exemplos/grafo_dependencias.png")
    
    return g


def exemplo_operacoes_grafos():
    """
    Exemplo de operações com grafos.
    """
    print("\n=== Exemplo: Operações com Grafos ===")
    
    # Este exemplo será implementado quando o módulo de operações estiver completo
    print("Este exemplo será implementado em uma versão futura.")


if __name__ == "__main__":
    # Executa os exemplos
    exemplo_grafo_simples()
    exemplo_grafo_direcionado()
    # exemplo_operacoes_grafos()  # Será implementado futuramente
