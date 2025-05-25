"""
Serviço para comparação entre grafos.
"""

import time
from typing import Dict, List, Any, Optional, Tuple

# Importações do backend de grafos
import sys
import os
sys.path.append('/home/ubuntu')  # Adiciona o diretório raiz ao path
from grafo_backend.core import Grafo
from grafo_backend.comparacao.isomorfismo import verificar_isomorfismo, encontrar_mapeamento_isomorfismo
from grafo_backend.comparacao.similaridade import calcular_similaridade_espectral, calcular_similaridade_estrutural
from grafo_backend.comparacao.subgrafos import verificar_subgrafo, encontrar_ocorrencias_subgrafo


class ComparacaoService:
    """
    Serviço para comparação entre grafos.
    """
    
    def __init__(self, grafo_service):
        """
        Inicializa o serviço de comparação.
        
        Args:
            grafo_service: Serviço de grafos para acesso aos grafos.
        """
        self.grafo_service = grafo_service
        self.metricas_disponiveis = {
            "isomorfismo": {
                "funcao": self.verificar_isomorfismo,
                "descricao": "Verifica se dois grafos são isomorfos"
            },
            "similaridade_espectral": {
                "funcao": self.calcular_similaridade_espectral,
                "descricao": "Calcula a similaridade espectral entre dois grafos"
            },
            "similaridade_estrutural": {
                "funcao": self.calcular_similaridade_estrutural,
                "descricao": "Calcula a similaridade estrutural entre dois grafos"
            },
            "subgrafo": {
                "funcao": self.verificar_subgrafo,
                "descricao": "Verifica se o primeiro grafo é subgrafo do segundo"
            }
        }
    
    def listar_metricas(self) -> List[Dict[str, str]]:
        """
        Lista as métricas de comparação disponíveis.
        
        Returns:
            List[Dict[str, str]]: Lista de métricas disponíveis.
        """
        return [
            {
                "id": metrica,
                "nome": metrica.replace("_", " ").title(),
                "descricao": info["descricao"]
            }
            for metrica, info in self.metricas_disponiveis.items()
        ]
    
    def comparar_grafos(self, grafo_id1: str, grafo_id2: str, metrica: str) -> Tuple[Any, float]:
        """
        Compara dois grafos usando uma métrica específica.
        
        Args:
            grafo_id1: ID do primeiro grafo.
            grafo_id2: ID do segundo grafo.
            metrica: Métrica de comparação.
            
        Returns:
            Tuple[Any, float]: Resultado da comparação e tempo de execução.
            
        Raises:
            ValueError: Se algum dos grafos não existir ou a métrica não for suportada.
        """
        # Verifica se a métrica é suportada
        if metrica not in self.metricas_disponiveis:
            raise ValueError(f"Métrica '{metrica}' não suportada.")
        
        # Obtém a função de comparação
        funcao_comparacao = self.metricas_disponiveis[metrica]["funcao"]
        
        # Executa a comparação
        return funcao_comparacao(grafo_id1, grafo_id2)
    
    def verificar_isomorfismo(self, grafo_id1: str, grafo_id2: str) -> Tuple[Dict[str, Any], float]:
        """
        Verifica se dois grafos são isomorfos.
        
        Args:
            grafo_id1: ID do primeiro grafo.
            grafo_id2: ID do segundo grafo.
            
        Returns:
            Tuple[Dict[str, Any], float]: Resultado da verificação e tempo de execução.
            
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
        
        # Mede o tempo de execução
        inicio = time.time()
        
        # Verifica o isomorfismo
        eh_isomorfo = verificar_isomorfismo(grafo1, grafo2)
        
        # Se for isomorfo, encontra o mapeamento
        mapeamento = None
        if eh_isomorfo:
            mapeamento = encontrar_mapeamento_isomorfismo(grafo1, grafo2)
        
        # Calcula o tempo de execução
        tempo_execucao = time.time() - inicio
        
        return {
            "eh_isomorfo": eh_isomorfo,
            "mapeamento": mapeamento
        }, tempo_execucao
    
    def calcular_similaridade_espectral(self, grafo_id1: str, grafo_id2: str) -> Tuple[Dict[str, Any], float]:
        """
        Calcula a similaridade espectral entre dois grafos.
        
        Args:
            grafo_id1: ID do primeiro grafo.
            grafo_id2: ID do segundo grafo.
            
        Returns:
            Tuple[Dict[str, Any], float]: Resultado do cálculo e tempo de execução.
            
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
        
        # Mede o tempo de execução
        inicio = time.time()
        
        # Calcula a similaridade espectral
        similaridade = calcular_similaridade_espectral(grafo1, grafo2)
        
        # Calcula o tempo de execução
        tempo_execucao = time.time() - inicio
        
        return {
            "similaridade": similaridade
        }, tempo_execucao
    
    def calcular_similaridade_estrutural(self, grafo_id1: str, grafo_id2: str) -> Tuple[Dict[str, Any], float]:
        """
        Calcula a similaridade estrutural entre dois grafos.
        
        Args:
            grafo_id1: ID do primeiro grafo.
            grafo_id2: ID do segundo grafo.
            
        Returns:
            Tuple[Dict[str, Any], float]: Resultado do cálculo e tempo de execução.
            
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
        
        # Mede o tempo de execução
        inicio = time.time()
        
        # Calcula a similaridade estrutural
        similaridade = calcular_similaridade_estrutural(grafo1, grafo2)
        
        # Calcula o tempo de execução
        tempo_execucao = time.time() - inicio
        
        return {
            "similaridade": similaridade
        }, tempo_execucao
    
    def verificar_subgrafo(self, grafo_id1: str, grafo_id2: str) -> Tuple[Dict[str, Any], float]:
        """
        Verifica se o primeiro grafo é subgrafo do segundo.
        
        Args:
            grafo_id1: ID do grafo a verificar como subgrafo.
            grafo_id2: ID do grafo maior.
            
        Returns:
            Tuple[Dict[str, Any], float]: Resultado da verificação e tempo de execução.
            
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
        
        # Mede o tempo de execução
        inicio = time.time()
        
        # Verifica se é subgrafo
        eh_subgrafo = verificar_subgrafo(grafo1, grafo2)
        
        # Se for subgrafo, encontra as ocorrências
        ocorrencias = None
        if eh_subgrafo:
            ocorrencias = encontrar_ocorrencias_subgrafo(grafo1, grafo2)
        
        # Calcula o tempo de execução
        tempo_execucao = time.time() - inicio
        
        return {
            "eh_subgrafo": eh_subgrafo,
            "ocorrencias": ocorrencias
        }, tempo_execucao
