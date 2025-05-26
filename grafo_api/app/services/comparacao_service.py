"""
Serviço para comparação entre grafos.
"""

import logging
import time
from typing import Dict, Any, Optional, List

from app.schemas.grafo import ResultadoComparacao
from app.services.grafo_service import GrafoService

# Configuração de logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ComparacaoService:
    """
    Serviço para comparação entre grafos.
    """
    
    def __init__(self, grafo_service: GrafoService = None):
        """
        Inicializa o serviço de comparação.
        
        Args:
            grafo_service: Serviço de grafos.
        """
        self.grafo_service = grafo_service
        logger.debug(f"ComparacaoService inicializado com ID: {id(self)}")
    
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
    
    def comparar(self, grafo_id1: str, grafo_id2: str, metrica: str) -> ResultadoComparacao:
        """
        Compara dois grafos usando a métrica especificada.
        
        Args:
            grafo_id1: ID do primeiro grafo.
            grafo_id2: ID do segundo grafo.
            metrica: Métrica de comparação (isomorfismo, similaridade, subgrafo).
            
        Returns:
            ResultadoComparacao: Resultado da comparação.
            
        Raises:
            ValueError: Se os grafos não existirem ou a métrica não for suportada.
        """
        # Obtém o serviço de grafos
        grafo_service = self._get_grafo_service()
        
        # Obtém os grafos
        grafo1 = grafo_service.obter_grafo(grafo_id1)
        grafo2 = grafo_service.obter_grafo(grafo_id2)
        
        if not grafo1 or not grafo2:
            raise ValueError("Grafos não encontrados.")
        
        # Verifica a métrica
        if metrica not in ["isomorfismo", "similaridade_espectral", "subgrafo"]:
            raise ValueError(f"Métrica '{metrica}' não suportada.")
        
        # Executa a comparação
        inicio = time.time()
        
        if metrica == "isomorfismo":
            resultado = self._verificar_isomorfismo(grafo1, grafo2)
        elif metrica == "similaridade_espectral":
            resultado = self._calcular_similaridade_espectral(grafo1, grafo2)
        elif metrica == "subgrafo":
            resultado = self._verificar_subgrafo(grafo1, grafo2)
        
        fim = time.time()
        tempo_execucao = fim - inicio
        
        # Retorna o resultado
        return ResultadoComparacao(
            grafo_id1=grafo_id1,
            grafo_id2=grafo_id2,
            metrica=metrica,
            resultado=resultado,
            tempo_execucao=tempo_execucao
        )
    
    def _verificar_isomorfismo(self, grafo1, grafo2) -> Dict[str, Any]:
        """
        Verifica se dois grafos são isomorfos.
        
        Args:
            grafo1: Primeiro grafo.
            grafo2: Segundo grafo.
            
        Returns:
            Dict[str, Any]: Resultado da verificação.
        """
        # Implementação simplificada para demonstração
        # Em um caso real, usaria um algoritmo de isomorfismo como VF2
        
        # Verifica se os grafos têm o mesmo número de vértices e arestas
        eh_isomorfo = (
            grafo1.numero_vertices() == grafo2.numero_vertices() and
            grafo1.numero_arestas() == grafo2.numero_arestas()
        )
        
        return {"eh_isomorfo": eh_isomorfo}
    
    def _calcular_similaridade_espectral(self, grafo1, grafo2) -> Dict[str, Any]:
        """
        Calcula a similaridade espectral entre dois grafos.
        
        Args:
            grafo1: Primeiro grafo.
            grafo2: Segundo grafo.
            
        Returns:
            Dict[str, Any]: Resultado do cálculo.
        """
        # Implementação simplificada para demonstração
        # Em um caso real, calcularia os autovalores da matriz laplaciana
        
        # Calcula uma similaridade baseada no número de vértices e arestas
        max_vertices = max(grafo1.numero_vertices(), grafo2.numero_vertices())
        min_vertices = min(grafo1.numero_vertices(), grafo2.numero_vertices())
        
        max_arestas = max(grafo1.numero_arestas(), grafo2.numero_arestas())
        min_arestas = min(grafo1.numero_arestas(), grafo2.numero_arestas())
        
        similaridade_vertices = min_vertices / max_vertices if max_vertices > 0 else 1.0
        similaridade_arestas = min_arestas / max_arestas if max_arestas > 0 else 1.0
        
        similaridade = (similaridade_vertices + similaridade_arestas) / 2
        
        return {"similaridade": similaridade}
    
    def _verificar_subgrafo(self, grafo1, grafo2) -> Dict[str, Any]:
        """
        Verifica se o primeiro grafo é subgrafo do segundo.
        
        Args:
            grafo1: Primeiro grafo (potencial subgrafo).
            grafo2: Segundo grafo (grafo maior).
            
        Returns:
            Dict[str, Any]: Resultado da verificação.
        """
        # Implementação simplificada para demonstração
        # Em um caso real, usaria um algoritmo de isomorfismo de subgrafo
        
        # Verifica se o número de vértices e arestas do primeiro grafo é menor ou igual ao do segundo
        eh_subgrafo = (
            grafo1.numero_vertices() <= grafo2.numero_vertices() and
            grafo1.numero_arestas() <= grafo2.numero_arestas()
        )
        
        return {"eh_subgrafo": eh_subgrafo}
