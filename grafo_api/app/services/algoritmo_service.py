"""
Serviço para execução de algoritmos em grafos.
"""

import time
from typing import Dict, List, Any, Optional, Tuple, Callable
import importlib

# Importações do backend de grafos
import sys
import os
sys.path.append('/home/ubuntu')  # Adiciona o diretório raiz ao path
from grafo_backend.core import Grafo


class AlgoritmoService:
    """
    Serviço para execução de algoritmos em grafos.
    """
    
    def __init__(self, grafo_service):
        """
        Inicializa o serviço de algoritmos.
        
        Args:
            grafo_service: Serviço de grafos para acesso aos grafos.
        """
        self.grafo_service = grafo_service
        self.algoritmos_disponiveis = self._mapear_algoritmos_disponiveis()
    
    def _mapear_algoritmos_disponiveis(self) -> Dict[str, Dict[str, Any]]:
        """
        Mapeia os algoritmos disponíveis no backend.
        
        Returns:
            Dict[str, Dict[str, Any]]: Dicionário mapeando nomes de algoritmos para suas informações.
        """
        algoritmos = {}
        
        # Algoritmos de caminhos
        algoritmos["dijkstra"] = {
            "nome": "Dijkstra",
            "categoria": "caminhos",
            "descricao": "Algoritmo para encontrar caminhos mínimos em grafos ponderados",
            "modulo": "grafo_backend.algoritmos.caminhos.dijkstra",
            "funcao": "dijkstra",
            "parametros_obrigatorios": ["origem"],
            "parametros_opcionais": []
        }
        
        algoritmos["caminho_minimo"] = {
            "nome": "Caminho Mínimo",
            "categoria": "caminhos",
            "descricao": "Encontra o caminho mínimo entre dois vértices",
            "modulo": "grafo_backend.algoritmos.caminhos.dijkstra",
            "funcao": "caminho_minimo",
            "parametros_obrigatorios": ["origem", "destino"],
            "parametros_opcionais": []
        }
        
        # Algoritmos de árvores
        algoritmos["kruskal"] = {
            "nome": "Kruskal",
            "categoria": "arvores",
            "descricao": "Algoritmo para encontrar árvore geradora mínima",
            "modulo": "grafo_backend.algoritmos.arvores.kruskal",
            "funcao": "kruskal",
            "parametros_obrigatorios": [],
            "parametros_opcionais": []
        }
        
        algoritmos["arvore_geradora_minima"] = {
            "nome": "Árvore Geradora Mínima",
            "categoria": "arvores",
            "descricao": "Encontra uma árvore geradora mínima usando o algoritmo de Kruskal",
            "modulo": "grafo_backend.algoritmos.arvores.kruskal",
            "funcao": "arvore_geradora_minima",
            "parametros_obrigatorios": [],
            "parametros_opcionais": []
        }
        
        # Algoritmos de fluxo
        algoritmos["ford_fulkerson"] = {
            "nome": "Ford-Fulkerson",
            "categoria": "fluxo",
            "descricao": "Algoritmo para encontrar fluxo máximo em redes",
            "modulo": "grafo_backend.algoritmos.fluxo.ford_fulkerson",
            "funcao": "ford_fulkerson",
            "parametros_obrigatorios": ["fonte", "sumidouro"],
            "parametros_opcionais": []
        }
        
        algoritmos["fluxo_maximo"] = {
            "nome": "Fluxo Máximo",
            "categoria": "fluxo",
            "descricao": "Calcula o fluxo máximo em uma rede",
            "modulo": "grafo_backend.algoritmos.fluxo.ford_fulkerson",
            "funcao": "fluxo_maximo",
            "parametros_obrigatorios": ["fonte", "sumidouro"],
            "parametros_opcionais": []
        }
        
        # Algoritmos de coloração
        algoritmos["coloracao_gulosa"] = {
            "nome": "Coloração Gulosa",
            "categoria": "coloracao",
            "descricao": "Algoritmo guloso para coloração de vértices",
            "modulo": "grafo_backend.algoritmos.coloracao.coloracao",
            "funcao": "coloracao_gulosa",
            "parametros_obrigatorios": [],
            "parametros_opcionais": ["ordem_vertices"]
        }
        
        algoritmos["coloracao_welsh_powell"] = {
            "nome": "Coloração Welsh-Powell",
            "categoria": "coloracao",
            "descricao": "Algoritmo de Welsh-Powell para coloração de vértices",
            "modulo": "grafo_backend.algoritmos.coloracao.coloracao",
            "funcao": "coloracao_welsh_powell",
            "parametros_obrigatorios": [],
            "parametros_opcionais": []
        }
        
        algoritmos["coloracao_dsatur"] = {
            "nome": "Coloração DSatur",
            "categoria": "coloracao",
            "descricao": "Algoritmo DSatur para coloração de vértices",
            "modulo": "grafo_backend.algoritmos.coloracao.coloracao",
            "funcao": "coloracao_dsatur",
            "parametros_obrigatorios": [],
            "parametros_opcionais": []
        }
        
        algoritmos["coloracao_arestas"] = {
            "nome": "Coloração de Arestas",
            "categoria": "coloracao",
            "descricao": "Algoritmo para coloração de arestas",
            "modulo": "grafo_backend.algoritmos.coloracao.coloracao",
            "funcao": "coloracao_arestas",
            "parametros_obrigatorios": [],
            "parametros_opcionais": []
        }
        
        algoritmos["numero_cromatico"] = {
            "nome": "Número Cromático",
            "categoria": "coloracao",
            "descricao": "Calcula uma aproximação do número cromático do grafo",
            "modulo": "grafo_backend.algoritmos.coloracao.coloracao",
            "funcao": "calcular_numero_cromatico_aproximado",
            "parametros_obrigatorios": [],
            "parametros_opcionais": []
        }
        
        # Algoritmos de emparelhamento
        algoritmos["emparelhamento_maximo"] = {
            "nome": "Emparelhamento Máximo",
            "categoria": "emparelhamento",
            "descricao": "Encontra um emparelhamento máximo em um grafo geral",
            "modulo": "grafo_backend.algoritmos.emparelhamento.emparelhamento",
            "funcao": "emparelhamento_maximo_geral",
            "parametros_obrigatorios": [],
            "parametros_opcionais": []
        }
        
        algoritmos["emparelhamento_maximo_ponderado"] = {
            "nome": "Emparelhamento Máximo Ponderado",
            "categoria": "emparelhamento",
            "descricao": "Encontra um emparelhamento máximo ponderado em um grafo",
            "modulo": "grafo_backend.algoritmos.emparelhamento.emparelhamento",
            "funcao": "emparelhamento_maximo_ponderado",
            "parametros_obrigatorios": [],
            "parametros_opcionais": []
        }
        
        # Algoritmos de planaridade
        algoritmos["verificar_planaridade"] = {
            "nome": "Verificar Planaridade",
            "categoria": "planaridade",
            "descricao": "Verifica se um grafo é planar",
            "modulo": "grafo_backend.algoritmos.planaridade.planaridade",
            "funcao": "verificar_planaridade",
            "parametros_obrigatorios": [],
            "parametros_opcionais": []
        }
        
        algoritmos["detectar_subgrafo_kuratowski"] = {
            "nome": "Detectar Subgrafo de Kuratowski",
            "categoria": "planaridade",
            "descricao": "Detecta um subgrafo de Kuratowski (K5 ou K3,3) no grafo",
            "modulo": "grafo_backend.algoritmos.planaridade.planaridade",
            "funcao": "detectar_subgrafo_kuratowski",
            "parametros_obrigatorios": [],
            "parametros_opcionais": []
        }
        
        algoritmos["calcular_faces"] = {
            "nome": "Calcular Faces",
            "categoria": "planaridade",
            "descricao": "Calcula as faces de um grafo planar",
            "modulo": "grafo_backend.algoritmos.planaridade.planaridade",
            "funcao": "calcular_faces",
            "parametros_obrigatorios": [],
            "parametros_opcionais": []
        }
        
        # Algoritmos espectrais
        algoritmos["autovalores_laplaciana"] = {
            "nome": "Autovalores da Laplaciana",
            "categoria": "espectral",
            "descricao": "Calcula os autovalores da matriz laplaciana do grafo",
            "modulo": "grafo_backend.algoritmos.espectral.espectral",
            "funcao": "calcular_autovalores_laplaciana",
            "parametros_obrigatorios": [],
            "parametros_opcionais": ["k"]
        }
        
        algoritmos["conectividade_algebrica"] = {
            "nome": "Conectividade Algébrica",
            "categoria": "espectral",
            "descricao": "Calcula a conectividade algébrica do grafo",
            "modulo": "grafo_backend.algoritmos.espectral.espectral",
            "funcao": "calcular_conectividade_algebrica",
            "parametros_obrigatorios": [],
            "parametros_opcionais": []
        }
        
        algoritmos["clustering_espectral"] = {
            "nome": "Clustering Espectral",
            "categoria": "espectral",
            "descricao": "Realiza clustering espectral no grafo",
            "modulo": "grafo_backend.algoritmos.espectral.espectral",
            "funcao": "clustering_espectral",
            "parametros_obrigatorios": ["n_clusters"],
            "parametros_opcionais": []
        }
        
        algoritmos["detectar_comunidades"] = {
            "nome": "Detectar Comunidades",
            "categoria": "espectral",
            "descricao": "Detecta comunidades no grafo usando métodos espectrais",
            "modulo": "grafo_backend.algoritmos.espectral.espectral",
            "funcao": "detectar_comunidades_espectral",
            "parametros_obrigatorios": [],
            "parametros_opcionais": ["max_comunidades"]
        }
        
        # Algoritmos de centralidade
        algoritmos["centralidade_grau"] = {
            "nome": "Centralidade de Grau",
            "categoria": "centralidade",
            "descricao": "Calcula a centralidade de grau para todos os vértices do grafo",
            "modulo": "grafo_backend.algoritmos.centralidade.centralidade",
            "funcao": "centralidade_grau",
            "parametros_obrigatorios": [],
            "parametros_opcionais": []
        }
        
        algoritmos["centralidade_intermediacao"] = {
            "nome": "Centralidade de Intermediação",
            "categoria": "centralidade",
            "descricao": "Calcula a centralidade de intermediação para todos os vértices do grafo",
            "modulo": "grafo_backend.algoritmos.centralidade.centralidade",
            "funcao": "centralidade_intermediacao",
            "parametros_obrigatorios": [],
            "parametros_opcionais": ["normalizado"]
        }
        
        algoritmos["centralidade_proximidade"] = {
            "nome": "Centralidade de Proximidade",
            "categoria": "centralidade",
            "descricao": "Calcula a centralidade de proximidade para todos os vértices do grafo",
            "modulo": "grafo_backend.algoritmos.centralidade.centralidade",
            "funcao": "centralidade_proximidade",
            "parametros_obrigatorios": [],
            "parametros_opcionais": []
        }
        
        algoritmos["centralidade_autovetor"] = {
            "nome": "Centralidade de Autovetor",
            "categoria": "centralidade",
            "descricao": "Calcula a centralidade de autovetor para todos os vértices do grafo",
            "modulo": "grafo_backend.algoritmos.centralidade.centralidade",
            "funcao": "centralidade_autovetor",
            "parametros_obrigatorios": [],
            "parametros_opcionais": ["max_iter", "tol"]
        }
        
        algoritmos["pagerank"] = {
            "nome": "PageRank",
            "categoria": "centralidade",
            "descricao": "Calcula o PageRank para todos os vértices do grafo",
            "modulo": "grafo_backend.algoritmos.centralidade.centralidade",
            "funcao": "pagerank",
            "parametros_obrigatorios": [],
            "parametros_opcionais": ["alpha", "max_iter", "tol"]
        }
        
        algoritmos["centralidade_katz"] = {
            "nome": "Centralidade de Katz",
            "categoria": "centralidade",
            "descricao": "Calcula a centralidade de Katz para todos os vértices do grafo",
            "modulo": "grafo_backend.algoritmos.centralidade.centralidade",
            "funcao": "centralidade_katz",
            "parametros_obrigatorios": [],
            "parametros_opcionais": ["alpha", "beta", "max_iter", "tol"]
        }
        
        return algoritmos
    
    def listar_algoritmos(self, categoria: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Lista os algoritmos disponíveis.
        
        Args:
            categoria: Categoria de algoritmos a listar. Se None, lista todos.
            
        Returns:
            List[Dict[str, Any]]: Lista de informações dos algoritmos.
        """
        algoritmos = []
        
        for nome, info in self.algoritmos_disponiveis.items():
            if categoria is None or info["categoria"] == categoria:
                algoritmos.append({
                    "id": nome,
                    "nome": info["nome"],
                    "categoria": info["categoria"],
                    "descricao": info["descricao"],
                    "parametros_obrigatorios": info["parametros_obrigatorios"],
                    "parametros_opcionais": info["parametros_opcionais"]
                })
        
        return algoritmos
    
    def executar_algoritmo(self, algoritmo_id: str, grafo_id: str, parametros: Dict[str, Any] = None) -> Tuple[Dict[str, Any], float]:
        """
        Executa um algoritmo em um grafo.
        
        Args:
            algoritmo_id: ID do algoritmo a executar.
            grafo_id: ID do grafo.
            parametros: Parâmetros para o algoritmo.
            
        Returns:
            Tuple[Dict[str, Any], float]: Tupla contendo o resultado do algoritmo e o tempo de execução.
            
        Raises:
            ValueError: Se o algoritmo ou o grafo não existirem, ou se parâmetros obrigatórios estiverem faltando.
        """
        # Verifica se o algoritmo existe
        if algoritmo_id not in self.algoritmos_disponiveis:
            raise ValueError(f"Algoritmo '{algoritmo_id}' não encontrado.")
        
        # Obtém o grafo
        grafo = self.grafo_service.obter_grafo(grafo_id)
        if not grafo:
            raise ValueError(f"Grafo com ID {grafo_id} não encontrado.")
        
        # Obtém informações do algoritmo
        info_algoritmo = self.algoritmos_disponiveis[algoritmo_id]
        
        # Inicializa parâmetros se não fornecidos
        if parametros is None:
            parametros = {}
        
        # Verifica se todos os parâmetros obrigatórios foram fornecidos
        for param in info_algoritmo["parametros_obrigatorios"]:
            if param not in parametros:
                raise ValueError(f"Parâmetro obrigatório '{param}' não fornecido para o algoritmo '{algoritmo_id}'.")
        
        # Importa o módulo e a função do algoritmo
        modulo = importlib.import_module(info_algoritmo["modulo"])
        funcao = getattr(modulo, info_algoritmo["funcao"])
        
        # Executa o algoritmo e mede o tempo
        inicio = time.time()
        
        # Prepara os argumentos para a função
        args = [grafo]
        kwargs = {}
        
        # Adiciona os parâmetros
        for param, valor in parametros.items():
            kwargs[param] = valor
        
        # Executa a função
        resultado = funcao(*args, **kwargs)
        
        # Calcula o tempo de execução
        tempo_execucao = time.time() - inicio
        
        # Converte o resultado para um formato serializável
        resultado_serializavel = self._converter_resultado_para_serializavel(resultado)
        
        return resultado_serializavel, tempo_execucao
    
    def _converter_resultado_para_serializavel(self, resultado: Any) -> Dict[str, Any]:
        """
        Converte o resultado de um algoritmo para um formato serializável.
        
        Args:
            resultado: Resultado do algoritmo.
            
        Returns:
            Dict[str, Any]: Resultado em formato serializável.
        """
        # Se o resultado for uma tupla, converte para um dicionário
        if isinstance(resultado, tuple):
            # Tenta inferir nomes para os elementos da tupla
            if len(resultado) == 2:
                # Casos comuns de tuplas de dois elementos
                if isinstance(resultado[0], dict) and isinstance(resultado[1], (int, float)):
                    return {"mapeamento": resultado[0], "valor": resultado[1]}
                elif isinstance(resultado[0], list) and isinstance(resultado[1], (int, float)):
                    return {"lista": resultado[0], "valor": resultado[1]}
                else:
                    return {"item1": resultado[0], "item2": resultado[1]}
            else:
                # Para tuplas de outros tamanhos
                return {f"item{i+1}": item for i, item in enumerate(resultado)}
        
        # Se o resultado for um dicionário, verifica se os valores são serializáveis
        elif isinstance(resultado, dict):
            resultado_serializavel = {}
            for chave, valor in resultado.items():
                # Converte chaves não serializáveis para strings
                chave_str = str(chave)
                
                # Converte valores não serializáveis
                if isinstance(valor, (int, float, str, bool, type(None))):
                    resultado_serializavel[chave_str] = valor
                elif isinstance(valor, (list, tuple)):
                    resultado_serializavel[chave_str] = [str(item) if not isinstance(item, (int, float, str, bool, type(None))) else item for item in valor]
                elif isinstance(valor, dict):
                    resultado_serializavel[chave_str] = {str(k): str(v) if not isinstance(v, (int, float, str, bool, type(None))) else v for k, v in valor.items()}
                else:
                    resultado_serializavel[chave_str] = str(valor)
            
            return resultado_serializavel
        
        # Se o resultado for uma lista, converte para um dicionário
        elif isinstance(resultado, list):
            return {"resultado": resultado}
        
        # Para outros tipos, converte para string
        else:
            return {"resultado": str(resultado)}
