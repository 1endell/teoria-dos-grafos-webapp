"""
Serviço para operações entre grafos.
"""

import logging
from typing import Dict, Any, Optional, List

from grafo_backend.operacoes.combinacao import (
    uniao_grafos, intersecao_grafos, diferenca_grafos, 
    diferenca_simetrica_grafos, composicao_grafos
)
from grafo_backend.tipos.grafo_ponderado import GrafoPonderado # Importa GrafoPonderado
from grafo_backend.core.grafo import Grafo # Importa Grafo base

# Configuração de logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class OperacaoService:
    """
    Serviço para operações entre grafos.
    """
    
    def __init__(self, grafo_service=None):
        """
        Inicializa o serviço de operações.
        
        Args:
            grafo_service: Serviço de grafos (opcional, pode ser obtido sob demanda)
        """
        self.grafo_service = grafo_service
        logger.debug(f"OperacaoService inicializado com ID: {id(self)}")
    
    def _get_grafo_service(self):
        """
        Obtém o serviço de grafos, seja o injetado no construtor ou via importação local.
        
        Returns:
            Serviço de grafos
        """
        if self.grafo_service is None:
            # Importação local para evitar ciclo de importação
            from app.core.session import get_grafo_service
            self.grafo_service = get_grafo_service()
        return self.grafo_service
    
    def _criar_grafo_resultado_no_servico(self, grafo_resultado: Grafo, nome_resultado: str) -> str:
        """
        Cria um novo grafo no serviço com base em um grafo backend.
        
        Args:
            grafo_resultado: O grafo backend resultante da operação.
            nome_resultado: O nome para o novo grafo no serviço.
            
        Returns:
            str: O ID do novo grafo criado no serviço.
        """
        grafo_service = self._get_grafo_service()
        
        # Verifica se o grafo resultante é ponderado
        eh_ponderado_resultado = isinstance(grafo_resultado, GrafoPonderado)
        
        # Cria um novo grafo no serviço
        grafo_id = grafo_service.criar_grafo(
            nome=nome_resultado,
            direcionado=grafo_resultado.eh_direcionado(),
            ponderado=eh_ponderado_resultado,
            bipartido=False # Operações não garantem preservação da bipartição
        )
        
        # Adiciona os vértices
        for v in grafo_resultado.obter_vertices():
            atributos = grafo_resultado.obter_atributos_vertice(v)
            grafo_service.adicionar_vertice(grafo_id, v, atributos)
        
        # Adiciona as arestas
        # Desempacota (u, v, atributos_aresta)
        for u, v, atributos_aresta in grafo_resultado.obter_arestas():
            peso = atributos_aresta.get("weight", 1.0)
            
            # Adiciona a aresta com ou sem peso, dependendo do tipo do grafo resultante
            if eh_ponderado_resultado:
                 grafo_service.adicionar_aresta(grafo_id, u, v, peso=peso, atributos=atributos_aresta)
            else:
                 # Remove o peso dos atributos se não for ponderado
                 atributos_aresta_sem_peso = atributos_aresta.copy()
                 atributos_aresta_sem_peso.pop("weight", None)
                 grafo_service.adicionar_aresta(grafo_id, u, v, atributos=atributos_aresta_sem_peso)
                 
        return grafo_id

    def uniao(self, grafo_id1: str, grafo_id2: str, nome_resultado: str) -> str:
        """
        Realiza a união de dois grafos.
        
        Args:
            grafo_id1: ID do primeiro grafo.
            grafo_id2: ID do segundo grafo.
            nome_resultado: Nome do grafo resultante.
            
        Returns:
            str: ID do grafo resultante.
        """
        # Obtém o serviço de grafos
        grafo_service = self._get_grafo_service()
        
        # Obtém os grafos
        grafo1 = grafo_service.obter_grafo(grafo_id1)
        grafo2 = grafo_service.obter_grafo(grafo_id2)
        
        if not grafo1 or not grafo2:
            raise ValueError("Grafos não encontrados.")
        
        # Realiza a união
        grafo_resultado = uniao_grafos(grafo1, grafo2, nome_resultado)
        
        # Cria o grafo resultante no serviço
        grafo_id = self._criar_grafo_resultado_no_servico(grafo_resultado, nome_resultado)
        
        logger.debug(f"União realizada: {grafo_id1} + {grafo_id2} = {grafo_id}")
        
        return grafo_id
    
    def intersecao(self, grafo_id1: str, grafo_id2: str, nome_resultado: str) -> str:
        """
        Realiza a interseção de dois grafos.
        
        Args:
            grafo_id1: ID do primeiro grafo.
            grafo_id2: ID do segundo grafo.
            nome_resultado: Nome do grafo resultante.
            
        Returns:
            str: ID do grafo resultante.
        """
        # Obtém o serviço de grafos
        grafo_service = self._get_grafo_service()
        
        # Obtém os grafos
        grafo1 = grafo_service.obter_grafo(grafo_id1)
        grafo2 = grafo_service.obter_grafo(grafo_id2)
        
        if not grafo1 or not grafo2:
            raise ValueError("Grafos não encontrados.")
        
        # Realiza a interseção
        grafo_resultado = intersecao_grafos(grafo1, grafo2, nome_resultado)
        
        # Cria o grafo resultante no serviço
        grafo_id = self._criar_grafo_resultado_no_servico(grafo_resultado, nome_resultado)
        
        logger.debug(f"Interseção realizada: {grafo_id1} ∩ {grafo_id2} = {grafo_id}")
        
        return grafo_id
    
    def diferenca(self, grafo_id1: str, grafo_id2: str, nome_resultado: str) -> str:
        """
        Realiza a diferença entre dois grafos.
        
        Args:
            grafo_id1: ID do primeiro grafo.
            grafo_id2: ID do segundo grafo.
            nome_resultado: Nome do grafo resultante.
            
        Returns:
            str: ID do grafo resultante.
        """
        # Obtém o serviço de grafos
        grafo_service = self._get_grafo_service()
        
        # Obtém os grafos
        grafo1 = grafo_service.obter_grafo(grafo_id1)
        grafo2 = grafo_service.obter_grafo(grafo_id2)
        
        if not grafo1 or not grafo2:
            raise ValueError("Grafos não encontrados.")
        
        # Realiza a diferença
        grafo_resultado = diferenca_grafos(grafo1, grafo2, nome_resultado)
        
        # Cria o grafo resultante no serviço
        grafo_id = self._criar_grafo_resultado_no_servico(grafo_resultado, nome_resultado)
        
        logger.debug(f"Diferença realizada: {grafo_id1} - {grafo_id2} = {grafo_id}")
        
        return grafo_id
    
    def diferenca_simetrica(self, grafo_id1: str, grafo_id2: str, nome_resultado: str) -> str:
        """
        Realiza a diferença simétrica entre dois grafos.
        
        Args:
            grafo_id1: ID do primeiro grafo.
            grafo_id2: ID do segundo grafo.
            nome_resultado: Nome do grafo resultante.
            
        Returns:
            str: ID do grafo resultante.
        """
        # Obtém o serviço de grafos
        grafo_service = self._get_grafo_service()
        
        # Obtém os grafos
        grafo1 = grafo_service.obter_grafo(grafo_id1)
        grafo2 = grafo_service.obter_grafo(grafo_id2)
        
        if not grafo1 or not grafo2:
            raise ValueError("Grafos não encontrados.")
        
        # Realiza a diferença simétrica
        grafo_resultado = diferenca_simetrica_grafos(grafo1, grafo2, nome_resultado)
        
        # Cria o grafo resultante no serviço
        grafo_id = self._criar_grafo_resultado_no_servico(grafo_resultado, nome_resultado)
        
        logger.debug(f"Diferença simétrica realizada: {grafo_id1} △ {grafo_id2} = {grafo_id}")
        
        return grafo_id
    
    def composicao(self, grafo_id1: str, grafo_id2: str, nome_resultado: str) -> str:
        """
        Realiza a composição de dois grafos.
        
        Args:
            grafo_id1: ID do primeiro grafo.
            grafo_id2: ID do segundo grafo.
            nome_resultado: Nome do grafo resultante.
            
        Returns:
            str: ID do grafo resultante.
        """
        # Obtém o serviço de grafos
        grafo_service = self._get_grafo_service()
        
        # Obtém os grafos
        grafo1 = grafo_service.obter_grafo(grafo_id1)
        grafo2 = grafo_service.obter_grafo(grafo_id2)
        
        if not grafo1 or not grafo2:
            raise ValueError("Grafos não encontrados.")
        
        # Realiza a composição
        grafo_resultado = composicao_grafos(grafo1, grafo2, nome_resultado)
        
        # Cria o grafo resultante no serviço
        grafo_id = self._criar_grafo_resultado_no_servico(grafo_resultado, nome_resultado)
        
        logger.debug(f"Composição realizada: {grafo_id1} ∘ {grafo_id2} = {grafo_id}")
        
        return grafo_id

