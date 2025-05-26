"""
Implementação de operações de combinação entre grafos.
"""

from typing import Dict, List, Any, Optional, Set, Tuple, Union
import logging

from grafo_backend.core.grafo import Grafo
from grafo_backend.tipos.grafo_ponderado import GrafoPonderado

# Configuração de logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def uniao_grafos(grafo1: Grafo, grafo2: Grafo, nome_resultado: str = "União") -> Grafo:
    """
    Realiza a união de dois grafos.
    
    Args:
        grafo1: Primeiro grafo.
        grafo2: Segundo grafo.
        nome_resultado: Nome do grafo resultante.
        
    Returns:
        Grafo: Grafo resultante da união.
    """
    # Determina o tipo do grafo resultante
    eh_ponderado = isinstance(grafo1, GrafoPonderado) or isinstance(grafo2, GrafoPonderado)
    eh_direcionado = grafo1.eh_direcionado() or grafo2.eh_direcionado()
    
    # Cria o grafo resultante
    if eh_ponderado:
        resultado = GrafoPonderado(nome_resultado, direcionado=eh_direcionado)
    else:
        resultado = Grafo(nome_resultado, direcionado=eh_direcionado)
    
    # Adiciona os vértices do primeiro grafo
    for v in grafo1.obter_vertices():
        atributos = grafo1.obter_atributos_vertice(v)
        resultado.adicionar_vertice(v, atributos)
    
    # Adiciona os vértices do segundo grafo
    for v in grafo2.obter_vertices():
        if not resultado.existe_vertice(v):
            atributos = grafo2.obter_atributos_vertice(v)
            resultado.adicionar_vertice(v, atributos)
    
    # Adiciona as arestas do primeiro grafo
    # Corrigido: Desempacota (u, v, atributos_aresta)
    for u, v, atributos_aresta in grafo1.obter_arestas():
        peso = atributos_aresta.get("weight", 1.0)
        
        if eh_ponderado:
            resultado.adicionar_aresta(u, v, peso, atributos_aresta)
        else:
            # Remove o peso se não for ponderado
            atributos_sem_peso = atributos_aresta.copy()
            atributos_sem_peso.pop("weight", None)
            resultado.adicionar_aresta(u, v, atributos=atributos_sem_peso)
    
    # Adiciona as arestas do segundo grafo
    # Corrigido: Desempacota (u, v, atributos_aresta)
    for u, v, atributos_aresta in grafo2.obter_arestas():
        if not resultado.existe_aresta(u, v):
            peso = atributos_aresta.get("weight", 1.0)
            
            if eh_ponderado:
                resultado.adicionar_aresta(u, v, peso, atributos_aresta)
            else:
                # Remove o peso se não for ponderado
                atributos_sem_peso = atributos_aresta.copy()
                atributos_sem_peso.pop("weight", None)
                resultado.adicionar_aresta(u, v, atributos=atributos_sem_peso)
    
    logger.debug(f"União realizada: {grafo1.nome} + {grafo2.nome} = {resultado.nome}")
    logger.debug(f"Resultado: {resultado.numero_vertices()} vértices, {resultado.numero_arestas()} arestas")
    
    return resultado


def intersecao_grafos(grafo1: Grafo, grafo2: Grafo, nome_resultado: str = "Interseção") -> Grafo:
    """
    Realiza a interseção de dois grafos.
    
    Args:
        grafo1: Primeiro grafo.
        grafo2: Segundo grafo.
        nome_resultado: Nome do grafo resultante.
        
    Returns:
        Grafo: Grafo resultante da interseção.
    """
    # Determina o tipo do grafo resultante
    eh_ponderado = isinstance(grafo1, GrafoPonderado) or isinstance(grafo2, GrafoPonderado)
    eh_direcionado = grafo1.eh_direcionado() or grafo2.eh_direcionado()
    
    # Cria o grafo resultante
    if eh_ponderado:
        resultado = GrafoPonderado(nome_resultado, direcionado=eh_direcionado)
    else:
        resultado = Grafo(nome_resultado, direcionado=eh_direcionado)
    
    # Adiciona os vértices que estão em ambos os grafos
    for v in grafo1.obter_vertices():
        if grafo2.existe_vertice(v):
            # Combina os atributos dos vértices
            atributos1 = grafo1.obter_atributos_vertice(v)
            atributos2 = grafo2.obter_atributos_vertice(v)
            atributos = {**atributos1, **atributos2}
            
            resultado.adicionar_vertice(v, atributos)
    
    # Adiciona as arestas que estão em ambos os grafos
    # Corrigido: Desempacota (u, v, atributos1)
    for u, v, atributos1 in grafo1.obter_arestas():
        if grafo2.existe_aresta(u, v):
            # Combina os atributos das arestas
            atributos2 = grafo2.obter_atributos_aresta(u, v)
            atributos = {**atributos1, **atributos2}
            
            # Determina o peso da aresta
            peso1 = atributos1.get("weight", 1.0)
            peso2 = atributos2.get("weight", 1.0)
            peso = (peso1 + peso2) / 2  # Média dos pesos
            
            if eh_ponderado:
                resultado.adicionar_aresta(u, v, peso, atributos)
            else:
                # Remove o peso se não for ponderado
                atributos_sem_peso = atributos.copy()
                atributos_sem_peso.pop("weight", None)
                resultado.adicionar_aresta(u, v, atributos=atributos_sem_peso)
    
    logger.debug(f"Interseção realizada: {grafo1.nome} ∩ {grafo2.nome} = {resultado.nome}")
    logger.debug(f"Resultado: {resultado.numero_vertices()} vértices, {resultado.numero_arestas()} arestas")
    
    return resultado


def diferenca_grafos(grafo1: Grafo, grafo2: Grafo, nome_resultado: str = "Diferença") -> Grafo:
    """
    Realiza a diferença entre dois grafos (grafo1 - grafo2).
    
    Args:
        grafo1: Primeiro grafo.
        grafo2: Segundo grafo.
        nome_resultado: Nome do grafo resultante.
        
    Returns:
        Grafo: Grafo resultante da diferença.
    """
    # Determina o tipo do grafo resultante
    eh_ponderado = isinstance(grafo1, GrafoPonderado)
    eh_direcionado = grafo1.eh_direcionado()
    
    # Cria o grafo resultante
    if eh_ponderado:
        resultado = GrafoPonderado(nome_resultado, direcionado=eh_direcionado)
    else:
        resultado = Grafo(nome_resultado, direcionado=eh_direcionado)
    
    # Adiciona os vértices do primeiro grafo que não estão no segundo
    for v in grafo1.obter_vertices():
        if not grafo2.existe_vertice(v):
            atributos = grafo1.obter_atributos_vertice(v)
            resultado.adicionar_vertice(v, atributos)
    
    # Adiciona os vértices do primeiro grafo que estão em ambos
    for v in grafo1.obter_vertices():
        if grafo2.existe_vertice(v) and not resultado.existe_vertice(v):
            atributos = grafo1.obter_atributos_vertice(v)
            resultado.adicionar_vertice(v, atributos)
    
    # Adiciona as arestas do primeiro grafo que não estão no segundo
    # Corrigido: Desempacota (u, v, atributos_aresta)
    for u, v, atributos_aresta in grafo1.obter_arestas():
        if not grafo2.existe_aresta(u, v) and resultado.existe_vertice(u) and resultado.existe_vertice(v):
            peso = atributos_aresta.get("weight", 1.0)
            
            if eh_ponderado:
                resultado.adicionar_aresta(u, v, peso, atributos_aresta)
            else:
                # Remove o peso se não for ponderado
                atributos_sem_peso = atributos_aresta.copy()
                atributos_sem_peso.pop("weight", None)
                resultado.adicionar_aresta(u, v, atributos=atributos_sem_peso)
    
    logger.debug(f"Diferença realizada: {grafo1.nome} - {grafo2.nome} = {resultado.nome}")
    logger.debug(f"Resultado: {resultado.numero_vertices()} vértices, {resultado.numero_arestas()} arestas")
    
    return resultado


def diferenca_simetrica_grafos(grafo1: Grafo, grafo2: Grafo, nome_resultado: str = "Diferença Simétrica") -> Grafo:
    """
    Realiza a diferença simétrica entre dois grafos.
    
    Args:
        grafo1: Primeiro grafo.
        grafo2: Segundo grafo.
        nome_resultado: Nome do grafo resultante.
        
    Returns:
        Grafo: Grafo resultante da diferença simétrica.
    """
    # Calcula a união dos grafos
    uniao = uniao_grafos(grafo1, grafo2, "União Temporária")
    
    # Calcula a interseção dos grafos
    intersecao = intersecao_grafos(grafo1, grafo2, "Interseção Temporária")
    
    # Calcula a diferença simétrica como união - interseção
    resultado = diferenca_grafos(uniao, intersecao, nome_resultado)
    
    logger.debug(f"Diferença simétrica realizada: {grafo1.nome} △ {grafo2.nome} = {resultado.nome}")
    logger.debug(f"Resultado: {resultado.numero_vertices()} vértices, {resultado.numero_arestas()} arestas")
    
    return resultado


def composicao_grafos(grafo1: Grafo, grafo2: Grafo, nome_resultado: str = "Composição") -> Grafo:
    """
    Realiza a composição de dois grafos.
    
    Args:
        grafo1: Primeiro grafo.
        grafo2: Segundo grafo.
        nome_resultado: Nome do grafo resultante.
        
    Returns:
        Grafo: Grafo resultante da composição.
    """
    # Determina o tipo do grafo resultante
    eh_ponderado = isinstance(grafo1, GrafoPonderado) or isinstance(grafo2, GrafoPonderado)
    eh_direcionado = grafo1.eh_direcionado() or grafo2.eh_direcionado()
    
    # Cria o grafo resultante
    if eh_ponderado:
        resultado = GrafoPonderado(nome_resultado, direcionado=eh_direcionado)
    else:
        resultado = Grafo(nome_resultado, direcionado=eh_direcionado)
    
    # Adiciona os vértices do primeiro grafo
    for v in grafo1.obter_vertices():
        atributos = grafo1.obter_atributos_vertice(v)
        resultado.adicionar_vertice(v, atributos)
    
    # Adiciona os vértices do segundo grafo
    for v in grafo2.obter_vertices():
        if not resultado.existe_vertice(v):
            atributos = grafo2.obter_atributos_vertice(v)
            resultado.adicionar_vertice(v, atributos)
    
    # Adiciona as arestas da composição
    for u in grafo1.obter_vertices():
        for v in grafo1.obter_vertices():
            # Verifica se existe um caminho de comprimento 2 de u para v
            # passando por algum vértice do segundo grafo
            for w in grafo2.obter_vertices():
                if grafo1.existe_aresta(u, w) and grafo2.existe_aresta(w, v):
                    # Calcula o peso da aresta composta
                    peso = 1.0
                    if eh_ponderado:
                        peso1 = grafo1.obter_atributos_aresta(u, w).get("weight", 1.0)
                        peso2 = grafo2.obter_atributos_aresta(w, v).get("weight", 1.0)
                        peso = peso1 * peso2  # Produto dos pesos
                    
                    # Adiciona a aresta ao resultado
                    if not resultado.existe_aresta(u, v):
                        atributos = {"composicao": f"via {w}"}
                        if eh_ponderado:
                            resultado.adicionar_aresta(u, v, peso, atributos)
                        else:
                            # Remove o peso se não for ponderado
                            atributos_sem_peso = atributos.copy()
                            atributos_sem_peso.pop("weight", None)
                            resultado.adicionar_aresta(u, v, atributos=atributos_sem_peso)
                    break
    
    logger.debug(f"Composição realizada: {grafo1.nome} ∘ {grafo2.nome} = {resultado.nome}")
    logger.debug(f"Resultado: {resultado.numero_vertices()} vértices, {resultado.numero_arestas()} arestas")
    
    return resultado

