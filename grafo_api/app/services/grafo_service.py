"""
Serviço para gerenciamento de grafos na API.
"""

import uuid
import time
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

# Configuração de logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Importações do backend de grafos
import sys
import os
sys.path.append("/home/ubuntu")  # Adiciona o diretório raiz ao path
from grafo_backend.core import Grafo
from grafo_backend.tipos import GrafoDirecionado, GrafoPonderado, GrafoBipartido


class GrafoService:
    """
    Serviço para gerenciamento de grafos.
    """

    def __init__(self):
        """Inicializa o serviço de grafos."""
        self.grafos: Dict[str, Grafo] = {}
        self.metadados: Dict[str, Dict[str, Any]] = {}
        logger.debug(f"GrafoService inicializado com ID: {id(self)}")

    def criar_grafo(self, nome: str, direcionado: bool = False,
                   ponderado: bool = False, bipartido: bool = False) -> str:
        """
        Cria um novo grafo e retorna seu ID.

        Args:
            nome: Nome do grafo.
            direcionado: Se True, cria um grafo direcionado.
            ponderado: Se True, cria um grafo ponderado.
            bipartido: Se True, cria um grafo bipartido.

        Returns:
            str: ID do grafo criado.
        """
        # Cria o tipo apropriado de grafo
        if bipartido:
            grafo = GrafoBipartido(nome)
        elif ponderado and direcionado:
            grafo = GrafoPonderado(nome, direcionado=True)
        elif ponderado:
            grafo = GrafoPonderado(nome)
        elif direcionado:
            grafo = GrafoDirecionado(nome)
        else:
            grafo = Grafo(nome)

        # Gera ID único
        grafo_id = str(uuid.uuid4())

        # Armazena grafo e metadados
        self.grafos[grafo_id] = grafo
        self.metadados[grafo_id] = {
            "id": grafo_id,
            "nome": nome,
            "direcionado": direcionado,
            "ponderado": ponderado,
            "bipartido": bipartido,
            "data_criacao": datetime.now(),
            "data_atualizacao": None
        }

        logger.debug(f"Grafo criado: ID={grafo_id}, Nome={nome}, Tipo={type(grafo).__name__}")
        logger.debug(f"Total de grafos armazenados: {len(self.grafos)}")
        logger.debug(f"IDs dos grafos armazenados: {list(self.grafos.keys())}")

        return grafo_id

    def obter_grafo(self, grafo_id: str) -> Optional[Grafo]:
        """
        Obtém um grafo pelo ID.

        Args:
            grafo_id: ID do grafo.

        Returns:
            Optional[Grafo]: Grafo correspondente ao ID, ou None se não existir.
        """
        grafo = self.grafos.get(grafo_id)
        if grafo:
            logger.debug(f"Grafo encontrado: ID={grafo_id}, Nome={grafo.nome}")
        else:
            logger.debug(f"Grafo não encontrado: ID={grafo_id}")
            logger.debug(f"IDs disponíveis: {list(self.grafos.keys())}")

        return grafo

    def obter_metadados(self, grafo_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtém os metadados de um grafo pelo ID.

        Args:
            grafo_id: ID do grafo.

        Returns:
            Optional[Dict[str, Any]]: Metadados do grafo, ou None se não existir.
        """
        metadados = self.metadados.get(grafo_id)
        if metadados:
            # Corrigido: Usar aspas simples dentro da f-string
            logger.debug(f"Metadados encontrados: ID={grafo_id}, Nome={metadados['nome']}")
        else:
            logger.debug(f"Metadados não encontrados: ID={grafo_id}")

        return metadados

    def listar_metadados(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Lista os metadados dos grafos disponíveis.

        Args:
            skip: Número de grafos a pular.
            limit: Número máximo de grafos a retornar.

        Returns:
            List[Dict[str, Any]]: Lista de metadados dos grafos.
        """
        metadados_list = list(self.metadados.values())

        # Ordena por data de criação (mais recente primeiro)
        metadados_list.sort(key=lambda x: x["data_criacao"], reverse=True)

        # Aplica paginação
        metadados_list = metadados_list[skip:skip + limit]

        # Adiciona informações de número de vértices e arestas
        for meta in metadados_list:
            grafo_id = meta["id"]
            grafo = self.grafos.get(grafo_id)
            if grafo:
                meta["num_vertices"] = grafo.numero_vertices()
                meta["num_arestas"] = grafo.numero_arestas()
            else:
                meta["num_vertices"] = 0
                meta["num_arestas"] = 0

        logger.debug(f"Listando metadados: total={len(self.metadados)}, retornados={len(metadados_list)}")

        return metadados_list

    def listar_grafos(self, skip: int = 0, limit: int = 100) -> Tuple[int, List[Dict[str, Any]]]:
        """
        Lista os grafos disponíveis.

        Args:
            skip: Número de grafos a pular.
            limit: Número máximo de grafos a retornar.

        Returns:
            Tuple[int, List[Dict[str, Any]]]: Tupla contendo o número total de grafos
                                            e a lista de metadados dos grafos.
        """
        total = len(self.metadados)
        metadados_list = self.listar_metadados(skip, limit)

        logger.debug(f"Listando grafos: total={total}, retornados={len(metadados_list)}")

        return total, metadados_list

    def atualizar_grafo(self, grafo_id: str, nome: Optional[str] = None,
                       direcionado: Optional[bool] = None, ponderado: Optional[bool] = None,
                       bipartido: Optional[bool] = None) -> bool:
        """
        Atualiza os metadados de um grafo.

        Args:
            grafo_id: ID do grafo.
            nome: Novo nome do grafo.
            direcionado: Se o grafo é direcionado.
            ponderado: Se o grafo é ponderado.
            bipartido: Se o grafo é bipartido.

        Returns:
            bool: True se o grafo foi atualizado, False se não existir.
        """
        if grafo_id not in self.metadados:
            logger.debug(f"Tentativa de atualizar grafo inexistente: ID={grafo_id}")
            return False

        # Atualiza os metadados
        if nome is not None:
            self.metadados[grafo_id]["nome"] = nome
            self.grafos[grafo_id].nome = nome

        if direcionado is not None:
            self.metadados[grafo_id]["direcionado"] = direcionado
            # Nota: Mudar o tipo de grafo requer recriar o grafo

        if ponderado is not None:
            self.metadados[grafo_id]["ponderado"] = ponderado
            # Nota: Mudar o tipo de grafo requer recriar o grafo

        if bipartido is not None:
            self.metadados[grafo_id]["bipartido"] = bipartido
            # Nota: Mudar o tipo de grafo requer recriar o grafo

        # Atualiza a data de atualização
        self.metadados[grafo_id]["data_atualizacao"] = datetime.now()

        logger.debug(f"Grafo atualizado: ID={grafo_id}, Nome={self.metadados[grafo_id]['nome']}")

        return True

    def excluir_grafo(self, grafo_id: str) -> bool:
        """
        Exclui um grafo.

        Args:
            grafo_id: ID do grafo.

        Returns:
            bool: True se o grafo foi excluído, False se não existir.
        """
        if grafo_id not in self.grafos:
            logger.debug(f"Tentativa de excluir grafo inexistente: ID={grafo_id}")
            return False

        # Remove o grafo e seus metadados
        nome = self.metadados[grafo_id]["nome"]
        del self.grafos[grafo_id]
        del self.metadados[grafo_id]

        logger.debug(f"Grafo excluído: ID={grafo_id}, Nome={nome}")
        logger.debug(f"Total de grafos restantes: {len(self.grafos)}")

        return True

    def remover_grafo(self, grafo_id: str) -> bool:
        """
        Remove um grafo (alias para excluir_grafo).

        Args:
            grafo_id: ID do grafo.

        Returns:
            bool: True se o grafo foi removido, False se não existir.
        """
        return self.excluir_grafo(grafo_id)

    def adicionar_vertice(self, grafo_id: str, vertice_id: Any,
                         atributos: Dict[str, Any] = None, conjunto: Optional[str] = None) -> bool:
        """
        Adiciona um vértice a um grafo.

        Args:
            grafo_id: ID do grafo.
            vertice_id: ID do vértice.
            atributos: Atributos do vértice.
            conjunto: Conjunto do vértice (para grafos bipartidos).

        Returns:
            bool: True se o vértice foi adicionado, False se o grafo não existir.
        """
        grafo = self.obter_grafo(grafo_id)
        if not grafo:
            logger.debug(f"Tentativa de adicionar vértice a grafo inexistente: ID={grafo_id}")
            return False

        # Inicializa atributos se não fornecidos
        if atributos is None:
            atributos = {}

        # Adiciona o vértice
        if isinstance(grafo, GrafoBipartido) and conjunto:
            grafo.adicionar_vertice(vertice_id, atributos, conjunto)
        else:
            grafo.adicionar_vertice(vertice_id, atributos)

        # Atualiza a data de atualização
        self.metadados[grafo_id]["data_atualizacao"] = datetime.now()

        logger.debug(f"Vértice adicionado: Grafo={grafo_id}, Vértice={vertice_id}")

        return True

    def obter_vertice(self, grafo_id: str, vertice_id: Any) -> Optional[Dict[str, Any]]:
        """
        Obtém informações de um vértice.

        Args:
            grafo_id: ID do grafo.
            vertice_id: ID do vértice.

        Returns:
            Optional[Dict[str, Any]]: Informações do vértice, ou None se não existir.
        """
        grafo = self.obter_grafo(grafo_id)
        if not grafo or not grafo.existe_vertice(vertice_id):
            logger.debug(f"Vértice não encontrado: Grafo={grafo_id}, Vértice={vertice_id}")
            return None

        # Obtém atributos do vértice
        atributos = grafo.obter_atributos_vertice(vertice_id)

        # Calcula o grau do vértice
        grau = 0
        if hasattr(grafo, "calcular_grau"):
            grau = grafo.calcular_grau(vertice_id)
        else:
            grau = grafo.obter_grau(vertice_id)

        # Obtém o conjunto do vértice (para grafos bipartidos)
        conjunto = None
        if isinstance(grafo, GrafoBipartido):
            conjunto = grafo.obter_conjunto_vertice(vertice_id)

        logger.debug(f"Vértice encontrado: Grafo={grafo_id}, Vértice={vertice_id}, Grau={grau}")

        return {
            "id": vertice_id,
            "atributos": atributos,
            "grau": grau,
            "conjunto": conjunto
        }

    def atualizar_vertice(self, grafo_id: str, vertice_id: Any,
                         atributos: Dict[str, Any]) -> bool:
        """
        Atualiza os atributos de um vértice.

        Args:
            grafo_id: ID do grafo.
            vertice_id: ID do vértice.
            atributos: Novos atributos do vértice.

        Returns:
            bool: True se o vértice foi atualizado, False se não existir.
        """
        grafo = self.obter_grafo(grafo_id)
        if not grafo or not grafo.existe_vertice(vertice_id):
            logger.debug(f"Tentativa de atualizar vértice inexistente: Grafo={grafo_id}, Vértice={vertice_id}")
            return False

        # Atualiza os atributos do vértice
        grafo.definir_atributos_vertice(vertice_id, atributos)

        # Atualiza a data de atualização
        self.metadados[grafo_id]["data_atualizacao"] = datetime.now()

        logger.debug(f"Vértice atualizado: Grafo={grafo_id}, Vértice={vertice_id}")

        return True

    def remover_vertice(self, grafo_id: str, vertice_id: Any) -> bool:
        """
        Remove um vértice de um grafo.

        Args:
            grafo_id: ID do grafo.
            vertice_id: ID do vértice.

        Returns:
            bool: True se o vértice foi removido, False se não existir.
        """
        grafo = self.obter_grafo(grafo_id)
        if not grafo or not grafo.existe_vertice(vertice_id):
            logger.debug(f"Tentativa de remover vértice inexistente: Grafo={grafo_id}, Vértice={vertice_id}")
            return False

        # Remove o vértice
        grafo.remover_vertice(vertice_id)

        # Atualiza a data de atualização
        self.metadados[grafo_id]["data_atualizacao"] = datetime.now()

        logger.debug(f"Vértice removido: Grafo={grafo_id}, Vértice={vertice_id}")

        return True

    def adicionar_aresta(self, grafo_id: str, origem: Any, destino: Any,
                        peso: float = 1.0, atributos: Dict[str, Any] = None) -> bool:
        """
        Adiciona uma aresta a um grafo.

        Args:
            grafo_id: ID do grafo.
            origem: Vértice de origem.
            destino: Vértice de destino.
            peso: Peso da aresta.
            atributos: Atributos da aresta.

        Returns:
            bool: True se a aresta foi adicionada, False se o grafo não existir
                 ou os vértices não existirem.
        """
        grafo = self.obter_grafo(grafo_id)
        if not grafo:
            logger.debug(f"Tentativa de adicionar aresta a grafo inexistente: ID={grafo_id}")
            return False

        # Verifica se os vértices existem
        if not grafo.existe_vertice(origem) or not grafo.existe_vertice(destino):
            logger.debug(f"Tentativa de adicionar aresta com vértices inexistentes: Grafo={grafo_id}, Origem={origem}, Destino={destino}")
            return False

        # Inicializa atributos se não fornecidos
        if atributos is None:
            atributos = {}

        # Adiciona a aresta
        if isinstance(grafo, GrafoPonderado):
            grafo.adicionar_aresta(origem, destino, peso, atributos)
        else:
            grafo.adicionar_aresta(origem, destino, atributos=atributos)

        # Atualiza a data de atualização
        self.metadados[grafo_id]["data_atualizacao"] = datetime.now()

        logger.debug(f"Aresta adicionada: Grafo={grafo_id}, Origem={origem}, Destino={destino}, Peso={peso}")

        return True

    def obter_aresta(self, grafo_id: str, origem: Any, destino: Any) -> Optional[Dict[str, Any]]:
        """
        Obtém informações de uma aresta.

        Args:
            grafo_id: ID do grafo.
            origem: Vértice de origem.
            destino: Vértice de destino.

        Returns:
            Optional[Dict[str, Any]]: Informações da aresta, ou None se não existir.
        """
        grafo = self.obter_grafo(grafo_id)
        if not grafo or not grafo.existe_aresta(origem, destino):
            logger.debug(f"Aresta não encontrada: Grafo={grafo_id}, Origem={origem}, Destino={destino}")
            return None

        # Obtém atributos da aresta
        atributos = grafo.obter_atributos_aresta(origem, destino)

        # Obtém o peso da aresta (para grafos ponderados)
        peso = 1.0
        if isinstance(grafo, GrafoPonderado):
            peso = grafo.obter_peso_aresta(origem, destino)

        logger.debug(f"Aresta encontrada: Grafo={grafo_id}, Origem={origem}, Destino={destino}, Peso={peso}")

        return {
            "origem": origem,
            "destino": destino,
            "peso": peso,
            "atributos": atributos
        }

    def atualizar_aresta(self, grafo_id: str, origem: Any, destino: Any,
                        peso: Optional[float] = None, atributos: Optional[Dict[str, Any]] = None) -> bool:
        """
        Atualiza uma aresta.

        Args:
            grafo_id: ID do grafo.
            origem: Vértice de origem.
            destino: Vértice de destino.
            peso: Novo peso da aresta.
            atributos: Novos atributos da aresta.

        Returns:
            bool: True se a aresta foi atualizada, False se não existir.
        """
        grafo = self.obter_grafo(grafo_id)
        if not grafo or not grafo.existe_aresta(origem, destino):
            logger.debug(f"Tentativa de atualizar aresta inexistente: Grafo={grafo_id}, Origem={origem}, Destino={destino}")
            return False

        # Atualiza o peso da aresta (para grafos ponderados)
        if peso is not None and isinstance(grafo, GrafoPonderado):
            grafo.definir_peso_aresta(origem, destino, peso)

        # Atualiza os atributos da aresta
        if atributos is not None:
            grafo.definir_atributos_aresta(origem, destino, atributos)

        # Atualiza a data de atualização
        self.metadados[grafo_id]["data_atualizacao"] = datetime.now()

        logger.debug(f"Aresta atualizada: Grafo={grafo_id}, Origem={origem}, Destino={destino}")

        return True

    def remover_aresta(self, grafo_id: str, origem: Any, destino: Any) -> bool:
        """
        Remove uma aresta de um grafo.

        Args:
            grafo_id: ID do grafo.
            origem: Vértice de origem.
            destino: Vértice de destino.

        Returns:
            bool: True se a aresta foi removida, False se não existir.
        """
        grafo = self.obter_grafo(grafo_id)
        if not grafo or not grafo.existe_aresta(origem, destino):
            logger.debug(f"Tentativa de remover aresta inexistente: Grafo={grafo_id}, Origem={origem}, Destino={destino}")
            return False

        # Remove a aresta
        grafo.remover_aresta(origem, destino)

        # Atualiza a data de atualização
        self.metadados[grafo_id]["data_atualizacao"] = datetime.now()

        logger.debug(f"Aresta removida: Grafo={grafo_id}, Origem={origem}, Destino={destino}")

        return True

    def serializar_grafo(self, grafo_id: str) -> Dict[str, Any]:
        """
        Serializa um grafo para formato JSON.

        Args:
            grafo_id: ID do grafo.

        Returns:
            Dict[str, Any]: Representação serializada do grafo.

        Raises:
            ValueError: Se o grafo não existir.
        """
        grafo = self.obter_grafo(grafo_id)
        if not grafo:
            raise ValueError(f"Grafo com ID {grafo_id} não encontrado.")

        # Obtém os metadados do grafo
        metadados = self.obter_metadados(grafo_id)

        # Serializa os vértices
        vertices = []
        for v in grafo.obter_vertices():
            atributos = grafo.obter_atributos_vertice(v)
            grau = 0
            if hasattr(grafo, "calcular_grau"):
                grau = grafo.calcular_grau(v)
            else:
                grau = grafo.obter_grau(v)

            vertices.append({
                "id": v,
                "atributos": atributos,
                "grau": grau
            })

        # Serializa as arestas
        arestas = []
        # Corrige o desempacotamento para lidar com (u, v, attrs)
        for u, v, _ in grafo.obter_arestas():
            atributos = grafo.obter_atributos_aresta(u, v)
            peso = 1.0
            if isinstance(grafo, GrafoPonderado):
                peso = grafo.obter_peso_aresta(u, v)

            arestas.append({
                "origem": u,
                "destino": v,
                "peso": peso,
                "atributos": atributos
            })

        # Converte objetos datetime para strings ISO para garantir serialização JSON
        data_criacao_str = metadados["data_criacao"].isoformat() if metadados["data_criacao"] else None
        data_atualizacao_str = metadados["data_atualizacao"].isoformat() if metadados["data_atualizacao"] else None

        # Constrói a representação serializada
        serializado = {
            "id": grafo_id,
            "nome": metadados["nome"],
            "direcionado": metadados["direcionado"],
            "ponderado": metadados["ponderado"],
            "bipartido": metadados["bipartido"],
            "num_vertices": grafo.numero_vertices(),
            "num_arestas": grafo.numero_arestas(),
            "data_criacao": data_criacao_str,
            "data_atualizacao": data_atualizacao_str,
            "vertices": vertices,
            "arestas": arestas
        }

        return serializado

    def obter_vertices(self, grafo_id: str) -> List[Dict[str, Any]]:
        """
        Obtém a lista de vértices de um grafo.

        Args:
            grafo_id: ID do grafo.

        Returns:
            List[Dict[str, Any]]: Lista de informações dos vértices.

        Raises:
            ValueError: Se o grafo não existir.
        """
        grafo = self.obter_grafo(grafo_id)
        if not grafo:
            raise ValueError(f"Grafo com ID {grafo_id} não encontrado.")

        # Obtém informações de cada vértice
        vertices = []
        for v in grafo.obter_vertices():
            vertice_info = self.obter_vertice(grafo_id, v)
            if vertice_info:
                vertices.append(vertice_info)

        return vertices

    def obter_arestas(self, grafo_id: str) -> List[Dict[str, Any]]:
        """
        Obtém a lista de arestas de um grafo.

        Args:
            grafo_id: ID do grafo.

        Returns:
            List[Dict[str, Any]]: Lista de informações das arestas.

        Raises:
            ValueError: Se o grafo não existir.
        """
        grafo = self.obter_grafo(grafo_id)
        if not grafo:
            raise ValueError(f"Grafo com ID {grafo_id} não encontrado.")

        # Obtém informações de cada aresta
        arestas = []
        for u, v, _ in grafo.obter_arestas():
            aresta_info = self.obter_aresta(grafo_id, u, v)
            if aresta_info:
                arestas.append(aresta_info)

        return arestas
