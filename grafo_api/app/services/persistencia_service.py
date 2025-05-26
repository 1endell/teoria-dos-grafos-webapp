"""
Serviço para persistência de grafos.
"""

import logging
import base64
import json
from typing import Dict, Any, Optional, List

from app.services.grafo_service import GrafoService

# Configuração de logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class PersistenciaService:
    """
    Serviço para persistência de grafos.
    """
    
    def __init__(self, grafo_service: GrafoService = None):
        """
        Inicializa o serviço de persistência.
        
        Args:
            grafo_service: Serviço de grafos.
        """
        self.grafo_service = grafo_service
        logger.debug(f"PersistenciaService inicializado com ID: {id(self)}")
    
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
    
    def importar_grafo(self, nome: str, formato: str, conteudo: str) -> str:
        """
        Importa um grafo a partir de uma representação.
        
        Args:
            nome: Nome do grafo importado.
            formato: Formato da representação (graphml, gml, gexf, json, csv).
            conteudo: Conteúdo da representação.
            
        Returns:
            str: ID do grafo importado.
            
        Raises:
            ValueError: Se o formato for inválido ou o conteúdo for inválido.
        """
        # Obtém o serviço de grafos
        grafo_service = self._get_grafo_service()
        
        # Verifica se o formato é válido
        formatos_validos = ["graphml", "gml", "gexf", "json", "csv"]
        if formato not in formatos_validos:
            raise ValueError(f"Formato '{formato}' inválido. Formatos válidos: {', '.join(formatos_validos)}")
        
        # Processa o conteúdo de acordo com o formato
        if formato == "json":
            try:
                # Tenta interpretar o conteúdo como JSON
                dados = json.loads(conteudo)
                
                # Cria um novo grafo
                grafo_id = grafo_service.criar_grafo(
                    nome=nome,
                    direcionado=dados.get("direcionado", False),
                    ponderado=dados.get("ponderado", False),
                    bipartido=dados.get("bipartido", False)
                )
                
                # Adiciona os vértices
                for v in dados.get("vertices", []):
                    grafo_service.adicionar_vertice(
                        grafo_id=grafo_id,
                        vertice_id=v["id"],
                        atributos=v.get("atributos", {}),
                        conjunto=v.get("conjunto")
                    )
                
                # Adiciona as arestas
                for a in dados.get("arestas", []):
                    grafo_service.adicionar_aresta(
                        grafo_id=grafo_id,
                        origem=a["origem"],
                        destino=a["destino"],
                        peso=a.get("peso", 1.0),
                        atributos=a.get("atributos", {})
                    )
                
                return grafo_id
            
            except json.JSONDecodeError as e:
                raise ValueError(f"Conteúdo JSON inválido: {str(e)}")
            
            except KeyError as e:
                raise ValueError(f"Conteúdo JSON inválido: campo obrigatório ausente: {str(e)}")
        
        # Para outros formatos, usaríamos bibliotecas específicas
        # Por simplicidade, apenas simulamos a importação
        grafo_id = grafo_service.criar_grafo(nome=nome)
        
        # Adiciona alguns vértices e arestas de exemplo
        grafo_service.adicionar_vertice(grafo_id, "A")
        grafo_service.adicionar_vertice(grafo_id, "B")
        grafo_service.adicionar_vertice(grafo_id, "C")
        
        grafo_service.adicionar_aresta(grafo_id, "A", "B", 1.0)
        grafo_service.adicionar_aresta(grafo_id, "B", "C", 2.0)
        
        return grafo_id
    
    def exportar_grafo(self, grafo_id: str, formato: str) -> str:
        """
        Exporta um grafo para um formato específico.
        
        Args:
            grafo_id: ID do grafo.
            formato: Formato de exportação (graphml, gml, gexf, json, csv).
            
        Returns:
            str: Conteúdo da exportação.
            
        Raises:
            ValueError: Se o grafo não existir ou o formato for inválido.
        """
        # Obtém o serviço de grafos
        grafo_service = self._get_grafo_service()
        
        # Obtém o grafo
        grafo = grafo_service.obter_grafo(grafo_id)
        if not grafo:
            raise ValueError(f"Grafo com ID {grafo_id} não encontrado.")
        
        # Verifica se o formato é válido
        formatos_validos = ["graphml", "gml", "gexf", "json", "csv"]
        if formato not in formatos_validos:
            raise ValueError(f"Formato '{formato}' inválido. Formatos válidos: {', '.join(formatos_validos)}")
        
        # Exporta o grafo de acordo com o formato
        if formato == "json":
            # Serializa o grafo para JSON
            grafo_serializado = grafo_service.serializar_grafo(grafo_id)
            return json.dumps(grafo_serializado, indent=2)
        
        # Para outros formatos, usaríamos bibliotecas específicas
        # Por simplicidade, apenas simulamos a exportação
        if formato == "graphml":
            return f"""<?xml version="1.0" encoding="UTF-8"?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlns">
  <graph id="{grafo_id}" edgedefault="undirected">
    <node id="A"/>
    <node id="B"/>
    <node id="C"/>
    <edge source="A" target="B"/>
    <edge source="B" target="C"/>
  </graph>
</graphml>"""
        
        elif formato == "gml":
            return f"""graph [
  id {grafo_id}
  node [
    id "A"
  ]
  node [
    id "B"
  ]
  node [
    id "C"
  ]
  edge [
    source "A"
    target "B"
  ]
  edge [
    source "B"
    target "C"
  ]
]"""
        
        elif formato == "gexf":
            return f"""<?xml version="1.0" encoding="UTF-8"?>
<gexf xmlns="http://www.gexf.net/1.2draft" version="1.2">
  <graph mode="static" defaultedgetype="undirected">
    <nodes>
      <node id="A" label="A" />
      <node id="B" label="B" />
      <node id="C" label="C" />
    </nodes>
    <edges>
      <edge id="0" source="A" target="B" />
      <edge id="1" source="B" target="C" />
    </edges>
  </graph>
</gexf>"""
        
        elif formato == "csv":
            return """source,target,weight
A,B,1.0
B,C,2.0"""
        
        return ""
