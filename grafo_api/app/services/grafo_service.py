"""
Serviço para gerenciamento de grafos na API.
"""

import uuid
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

# Importações do backend de grafos
import sys
import os
sys.path.append('/home/ubuntu')  # Adiciona o diretório raiz ao path
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
        
        return grafo_id
    
    def obter_grafo(self, grafo_id: str) -> Optional[Grafo]:
        """
        Obtém um grafo pelo ID.
        
        Args:
            grafo_id: ID do grafo.
            
        Returns:
            Optional[Grafo]: Grafo correspondente ao ID, ou None se não existir.
        """
        return self.grafos.get(grafo_id)
    
    def obter_metadados(self, grafo_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtém os metadados de um grafo pelo ID.
        
        Args:
            grafo_id: ID do grafo.
            
        Returns:
            Optional[Dict[str, Any]]: Metadados do grafo, ou None se não existir.
        """
        return self.metadados.get(grafo_id)
    
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
            return False
        
        # Remove o grafo e seus metadados
        del self.grafos[grafo_id]
        del self.metadados[grafo_id]
        
        return True
    
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
            return None
        
        # Obtém atributos do vértice
        atributos = grafo.obter_atributos_vertice(vertice_id)
        
        # Calcula o grau do vértice
        grau = grafo.calcular_grau(vertice_id)
        
        # Obtém o conjunto do vértice (para grafos bipartidos)
        conjunto = None
        if isinstance(grafo, GrafoBipartido):
            conjunto = grafo.obter_conjunto_vertice(vertice_id)
        
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
            return False
        
        # Atualiza os atributos do vértice
        grafo.definir_atributos_vertice(vertice_id, atributos)
        
        # Atualiza a data de atualização
        self.metadados[grafo_id]["data_atualizacao"] = datetime.now()
        
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
            return False
        
        # Remove o vértice
        grafo.remover_vertice(vertice_id)
        
        # Atualiza a data de atualização
        self.metadados[grafo_id]["data_atualizacao"] = datetime.now()
        
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
            return False
        
        # Verifica se os vértices existem
        if not grafo.existe_vertice(origem) or not grafo.existe_vertice(destino):
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
            return None
        
        # Obtém atributos da aresta
        atributos = grafo.obter_atributos_aresta(origem, destino)
        
        # Obtém o peso da aresta (para grafos ponderados)
        peso = 1.0
        if isinstance(grafo, GrafoPonderado):
            peso = grafo.obter_peso_aresta(origem, destino)
        
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
            return False
        
        # Atualiza o peso da aresta (para grafos ponderados)
        if peso is not None and isinstance(grafo, GrafoPonderado):
            grafo.definir_peso_aresta(origem, destino, peso)
        
        # Atualiza os atributos da aresta
        if atributos is not None:
            grafo.definir_atributos_aresta(origem, destino, atributos)
        
        # Atualiza a data de atualização
        self.metadados[grafo_id]["data_atualizacao"] = datetime.now()
        
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
            return False
        
        # Remove a aresta
        grafo.remover_aresta(origem, destino)
        
        # Atualiza a data de atualização
        self.metadados[grafo_id]["data_atualizacao"] = datetime.now()
        
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
        
        metadados = self.obter_metadados(grafo_id)
        
        # Obtém vértices e arestas
        vertices = []
        for v in grafo.obter_vertices():
            vertice_info = self.obter_vertice(grafo_id, v)
            vertices.append(vertice_info)
        
        arestas = []
        for u, v in grafo.obter_arestas():
            aresta_info = self.obter_aresta(grafo_id, u, v)
            arestas.append(aresta_info)
        
        # Constrói a representação serializada
        return {
            "id": grafo_id,
            "nome": metadados["nome"],
            "direcionado": metadados["direcionado"],
            "ponderado": metadados["ponderado"],
            "bipartido": metadados["bipartido"],
            "num_vertices": grafo.numero_vertices(),
            "num_arestas": grafo.numero_arestas(),
            "data_criacao": metadados["data_criacao"],
            "data_atualizacao": metadados["data_atualizacao"],
            "vertices": vertices,
            "arestas": arestas
        }
    
    def desserializar_grafo(self, dados: Dict[str, Any]) -> str:
        """
        Cria um grafo a partir de uma representação serializada.
        
        Args:
            dados: Representação serializada do grafo.
            
        Returns:
            str: ID do grafo criado.
        """
        # Cria o grafo
        grafo_id = self.criar_grafo(
            nome=dados["nome"],
            direcionado=dados.get("direcionado", False),
            ponderado=dados.get("ponderado", False),
            bipartido=dados.get("bipartido", False)
        )
        
        # Adiciona os vértices
        for v in dados.get("vertices", []):
            self.adicionar_vertice(
                grafo_id=grafo_id,
                vertice_id=v["id"],
                atributos=v.get("atributos", {}),
                conjunto=v.get("conjunto")
            )
        
        # Adiciona as arestas
        for a in dados.get("arestas", []):
            self.adicionar_aresta(
                grafo_id=grafo_id,
                origem=a["origem"],
                destino=a["destino"],
                peso=a.get("peso", 1.0),
                atributos=a.get("atributos", {})
            )
        
        return grafo_id
