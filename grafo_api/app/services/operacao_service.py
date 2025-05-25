"""
Serviço para operações entre grafos.
"""

import time
from typing import Dict, List, Any, Optional, Tuple

# Importações do backend de grafos
import sys
import os
sys.path.append('/home/ubuntu')  # Adiciona o diretório raiz ao path
from grafo_backend.core.grafo import Grafo
from grafo_backend.operacoes.combinacao import (
    uniao, intersecao, diferenca, diferenca_simetrica, composicao
)


class OperacaoService:
    """
    Serviço para operações entre grafos.
    """
    
    def __init__(self, grafo_service):
        """
        Inicializa o serviço de operações.
        
        Args:
            grafo_service: Serviço de grafos para acesso aos grafos.
        """
        self.grafo_service = grafo_service
    
    def uniao_grafos(self, grafo_id1: str, grafo_id2: str, nome_resultado: Optional[str] = None) -> str:
        """
        Realiza a união de dois grafos.
        
        Args:
            grafo_id1: ID do primeiro grafo.
            grafo_id2: ID do segundo grafo.
            nome_resultado: Nome do grafo resultante.
            
        Returns:
            str: ID do grafo resultante.
            
        Raises:
            ValueError: Se algum dos grafos não existir.
        """
        # Obtém os grafos
        grafo1 = self.grafo_service.obter_grafo(grafo_id1)
        grafo2 = self.grafo_service.obter_grafo(grafo_id2)
        
        if not grafo1:
            raise ValueError(f"Grafo com ID {grafo_id1} não encontrado.")
        
        if not grafo2:
            raise ValueError(f"Grafo com ID {grafo_id2} não encontrado.")
        
        # Define o nome do grafo resultante
        if nome_resultado is None:
            nome_resultado = f"União de {grafo1.nome} e {grafo2.nome}"
        
        # Obtém os metadados dos grafos
        meta1 = self.grafo_service.obter_metadados(grafo_id1)
        meta2 = self.grafo_service.obter_metadados(grafo_id2)
        
        # Determina se o grafo resultante será direcionado e ponderado
        direcionado = meta1["direcionado"] or meta2["direcionado"]
        ponderado = meta1["ponderado"] or meta2["ponderado"]
        
        # Realiza a união
        grafo_uniao = uniao(grafo1, grafo2)
        
        # Cria um novo grafo para o resultado
        grafo_id = self.grafo_service.criar_grafo(
            nome=nome_resultado,
            direcionado=direcionado,
            ponderado=ponderado,
            bipartido=False  # A união pode não preservar a bipartição
        )
        
        # Obtém o grafo resultante
        grafo_resultado = self.grafo_service.obter_grafo(grafo_id)
        
        # Copia os vértices e arestas do grafo união para o grafo resultado
        for v in grafo_uniao.obter_vertices():
            atributos = grafo_uniao.obter_atributos_vertice(v)
            self.grafo_service.adicionar_vertice(grafo_id, v, atributos)
        
        for u, v in grafo_uniao.obter_arestas():
            atributos = grafo_uniao.obter_atributos_aresta(u, v)
            peso = 1.0
            if ponderado:
                peso = grafo_uniao.obter_peso_aresta(u, v) if hasattr(grafo_uniao, 'obter_peso_aresta') else 1.0
            self.grafo_service.adicionar_aresta(grafo_id, u, v, peso, atributos)
        
        return grafo_id
    
    def intersecao_grafos(self, grafo_id1: str, grafo_id2: str, nome_resultado: Optional[str] = None) -> str:
        """
        Realiza a interseção de dois grafos.
        
        Args:
            grafo_id1: ID do primeiro grafo.
            grafo_id2: ID do segundo grafo.
            nome_resultado: Nome do grafo resultante.
            
        Returns:
            str: ID do grafo resultante.
            
        Raises:
            ValueError: Se algum dos grafos não existir.
        """
        # Obtém os grafos
        grafo1 = self.grafo_service.obter_grafo(grafo_id1)
        grafo2 = self.grafo_service.obter_grafo(grafo_id2)
        
        if not grafo1:
            raise ValueError(f"Grafo com ID {grafo_id1} não encontrado.")
        
        if not grafo2:
            raise ValueError(f"Grafo com ID {grafo_id2} não encontrado.")
        
        # Define o nome do grafo resultante
        if nome_resultado is None:
            nome_resultado = f"Interseção de {grafo1.nome} e {grafo2.nome}"
        
        # Obtém os metadados dos grafos
        meta1 = self.grafo_service.obter_metadados(grafo_id1)
        meta2 = self.grafo_service.obter_metadados(grafo_id2)
        
        # Determina se o grafo resultante será direcionado e ponderado
        direcionado = meta1["direcionado"] or meta2["direcionado"]
        ponderado = meta1["ponderado"] or meta2["ponderado"]
        
        # Realiza a interseção
        grafo_intersecao = intersecao(grafo1, grafo2)
        
        # Cria um novo grafo para o resultado
        grafo_id = self.grafo_service.criar_grafo(
            nome=nome_resultado,
            direcionado=direcionado,
            ponderado=ponderado,
            bipartido=False  # A interseção pode não preservar a bipartição
        )
        
        # Obtém o grafo resultante
        grafo_resultado = self.grafo_service.obter_grafo(grafo_id)
        
        # Copia os vértices e arestas do grafo interseção para o grafo resultado
        for v in grafo_intersecao.obter_vertices():
            atributos = grafo_intersecao.obter_atributos_vertice(v)
            self.grafo_service.adicionar_vertice(grafo_id, v, atributos)
        
        for u, v in grafo_intersecao.obter_arestas():
            atributos = grafo_intersecao.obter_atributos_aresta(u, v)
            peso = 1.0
            if ponderado:
                peso = grafo_intersecao.obter_peso_aresta(u, v) if hasattr(grafo_intersecao, 'obter_peso_aresta') else 1.0
            self.grafo_service.adicionar_aresta(grafo_id, u, v, peso, atributos)
        
        return grafo_id
    
    def diferenca_grafos(self, grafo_id1: str, grafo_id2: str, nome_resultado: Optional[str] = None) -> str:
        """
        Realiza a diferença entre dois grafos.
        
        Args:
            grafo_id1: ID do primeiro grafo.
            grafo_id2: ID do segundo grafo.
            nome_resultado: Nome do grafo resultante.
            
        Returns:
            str: ID do grafo resultante.
            
        Raises:
            ValueError: Se algum dos grafos não existir.
        """
        # Obtém os grafos
        grafo1 = self.grafo_service.obter_grafo(grafo_id1)
        grafo2 = self.grafo_service.obter_grafo(grafo_id2)
        
        if not grafo1:
            raise ValueError(f"Grafo com ID {grafo_id1} não encontrado.")
        
        if not grafo2:
            raise ValueError(f"Grafo com ID {grafo_id2} não encontrado.")
        
        # Define o nome do grafo resultante
        if nome_resultado is None:
            nome_resultado = f"Diferença de {grafo1.nome} e {grafo2.nome}"
        
        # Obtém os metadados dos grafos
        meta1 = self.grafo_service.obter_metadados(grafo_id1)
        
        # O grafo resultante herda as propriedades do primeiro grafo
        direcionado = meta1["direcionado"]
        ponderado = meta1["ponderado"]
        
        # Realiza a diferença
        grafo_diferenca = diferenca(grafo1, grafo2)
        
        # Cria um novo grafo para o resultado
        grafo_id = self.grafo_service.criar_grafo(
            nome=nome_resultado,
            direcionado=direcionado,
            ponderado=ponderado,
            bipartido=False  # A diferença pode não preservar a bipartição
        )
        
        # Obtém o grafo resultante
        grafo_resultado = self.grafo_service.obter_grafo(grafo_id)
        
        # Copia os vértices e arestas do grafo diferença para o grafo resultado
        for v in grafo_diferenca.obter_vertices():
            atributos = grafo_diferenca.obter_atributos_vertice(v)
            self.grafo_service.adicionar_vertice(grafo_id, v, atributos)
        
        for u, v in grafo_diferenca.obter_arestas():
            atributos = grafo_diferenca.obter_atributos_aresta(u, v)
            peso = 1.0
            if ponderado:
                peso = grafo_diferenca.obter_peso_aresta(u, v) if hasattr(grafo_diferenca, 'obter_peso_aresta') else 1.0
            self.grafo_service.adicionar_aresta(grafo_id, u, v, peso, atributos)
        
        return grafo_id
    
    def diferenca_simetrica_grafos(self, grafo_id1: str, grafo_id2: str, nome_resultado: Optional[str] = None) -> str:
        """
        Realiza a diferença simétrica entre dois grafos.
        
        Args:
            grafo_id1: ID do primeiro grafo.
            grafo_id2: ID do segundo grafo.
            nome_resultado: Nome do grafo resultante.
            
        Returns:
            str: ID do grafo resultante.
            
        Raises:
            ValueError: Se algum dos grafos não existir.
        """
        # Obtém os grafos
        grafo1 = self.grafo_service.obter_grafo(grafo_id1)
        grafo2 = self.grafo_service.obter_grafo(grafo_id2)
        
        if not grafo1:
            raise ValueError(f"Grafo com ID {grafo_id1} não encontrado.")
        
        if not grafo2:
            raise ValueError(f"Grafo com ID {grafo_id2} não encontrado.")
        
        # Define o nome do grafo resultante
        if nome_resultado is None:
            nome_resultado = f"Diferença simétrica de {grafo1.nome} e {grafo2.nome}"
        
        # Obtém os metadados dos grafos
        meta1 = self.grafo_service.obter_metadados(grafo_id1)
        meta2 = self.grafo_service.obter_metadados(grafo_id2)
        
        # Determina se o grafo resultante será direcionado e ponderado
        direcionado = meta1["direcionado"] or meta2["direcionado"]
        ponderado = meta1["ponderado"] or meta2["ponderado"]
        
        # Realiza a diferença simétrica
        grafo_diferenca_simetrica = diferenca_simetrica(grafo1, grafo2)
        
        # Cria um novo grafo para o resultado
        grafo_id = self.grafo_service.criar_grafo(
            nome=nome_resultado,
            direcionado=direcionado,
            ponderado=ponderado,
            bipartido=False  # A diferença simétrica pode não preservar a bipartição
        )
        
        # Obtém o grafo resultante
        grafo_resultado = self.grafo_service.obter_grafo(grafo_id)
        
        # Copia os vértices e arestas do grafo diferença simétrica para o grafo resultado
        for v in grafo_diferenca_simetrica.obter_vertices():
            atributos = grafo_diferenca_simetrica.obter_atributos_vertice(v)
            self.grafo_service.adicionar_vertice(grafo_id, v, atributos)
        
        for u, v in grafo_diferenca_simetrica.obter_arestas():
            atributos = grafo_diferenca_simetrica.obter_atributos_aresta(u, v)
            peso = 1.0
            if ponderado:
                peso = grafo_diferenca_simetrica.obter_peso_aresta(u, v) if hasattr(grafo_diferenca_simetrica, 'obter_peso_aresta') else 1.0
            self.grafo_service.adicionar_aresta(grafo_id, u, v, peso, atributos)
        
        return grafo_id
    
    def composicao_grafos(self, grafo_id1: str, grafo_id2: str, nome_resultado: Optional[str] = None) -> str:
        """
        Realiza a composição de dois grafos.
        
        Args:
            grafo_id1: ID do primeiro grafo.
            grafo_id2: ID do segundo grafo.
            nome_resultado: Nome do grafo resultante.
            
        Returns:
            str: ID do grafo resultante.
            
        Raises:
            ValueError: Se algum dos grafos não existir.
        """
        # Obtém os grafos
        grafo1 = self.grafo_service.obter_grafo(grafo_id1)
        grafo2 = self.grafo_service.obter_grafo(grafo_id2)
        
        if not grafo1:
            raise ValueError(f"Grafo com ID {grafo_id1} não encontrado.")
        
        if not grafo2:
            raise ValueError(f"Grafo com ID {grafo_id2} não encontrado.")
        
        # Define o nome do grafo resultante
        if nome_resultado is None:
            nome_resultado = f"Composição de {grafo1.nome} e {grafo2.nome}"
        
        # Obtém os metadados dos grafos
        meta1 = self.grafo_service.obter_metadados(grafo_id1)
        meta2 = self.grafo_service.obter_metadados(grafo_id2)
        
        # Determina se o grafo resultante será direcionado e ponderado
        direcionado = meta1["direcionado"] or meta2["direcionado"]
        ponderado = meta1["ponderado"] or meta2["ponderado"]
        
        # Realiza a composição
        grafo_composicao = composicao(grafo1, grafo2)
        
        # Cria um novo grafo para o resultado
        grafo_id = self.grafo_service.criar_grafo(
            nome=nome_resultado,
            direcionado=direcionado,
            ponderado=ponderado,
            bipartido=False  # A composição pode não preservar a bipartição
        )
        
        # Obtém o grafo resultante
        grafo_resultado = self.grafo_service.obter_grafo(grafo_id)
        
        # Copia os vértices e arestas do grafo composição para o grafo resultado
        for v in grafo_composicao.obter_vertices():
            atributos = grafo_composicao.obter_atributos_vertice(v)
            self.grafo_service.adicionar_vertice(grafo_id, v, atributos)
        
        for u, v in grafo_composicao.obter_arestas():
            atributos = grafo_composicao.obter_atributos_aresta(u, v)
            peso = 1.0
            if ponderado:
                peso = grafo_composicao.obter_peso_aresta(u, v) if hasattr(grafo_composicao, 'obter_peso_aresta') else 1.0
            self.grafo_service.adicionar_aresta(grafo_id, u, v, peso, atributos)
        
        return grafo_id
