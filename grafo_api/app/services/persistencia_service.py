"""
Serviço para persistência de grafos em diferentes formatos.
"""

import time
import io
from typing import Dict, List, Any, Optional, Tuple

# Importações do backend de grafos
import sys
import os
sys.path.append('/home/ubuntu')  # Adiciona o diretório raiz ao path
from grafo_backend.core.grafo import Grafo
from grafo_backend.persistencia.exportador import (
    exportar_graphml, exportar_gml, exportar_gexf, exportar_json, exportar_csv
)
from grafo_backend.persistencia.importador import (
    importar_graphml, importar_gml, importar_gexf, importar_json, importar_csv
)


class PersistenciaService:
    """
    Serviço para persistência de grafos em diferentes formatos.
    """
    
    def __init__(self, grafo_service):
        """
        Inicializa o serviço de persistência.
        
        Args:
            grafo_service: Serviço de grafos para acesso aos grafos.
        """
        self.grafo_service = grafo_service
        self.formatos_suportados = {
            "graphml": {
                "exportar": exportar_graphml,
                "importar": importar_graphml,
                "descricao": "GraphML (XML para grafos)",
                "mime_type": "application/xml"
            },
            "gml": {
                "exportar": exportar_gml,
                "importar": importar_gml,
                "descricao": "Graph Modeling Language",
                "mime_type": "text/plain"
            },
            "gexf": {
                "exportar": exportar_gexf,
                "importar": importar_gexf,
                "descricao": "Graph Exchange XML Format",
                "mime_type": "application/xml"
            },
            "json": {
                "exportar": exportar_json,
                "importar": importar_json,
                "descricao": "JavaScript Object Notation",
                "mime_type": "application/json"
            },
            "csv": {
                "exportar": exportar_csv,
                "importar": importar_csv,
                "descricao": "Comma-Separated Values",
                "mime_type": "text/csv"
            }
        }
    
    def listar_formatos(self) -> List[Dict[str, str]]:
        """
        Lista os formatos de persistência suportados.
        
        Returns:
            List[Dict[str, str]]: Lista de formatos suportados.
        """
        return [
            {
                "id": formato,
                "nome": formato.upper(),
                "descricao": info["descricao"],
                "mime_type": info["mime_type"]
            }
            for formato, info in self.formatos_suportados.items()
        ]
    
    def exportar_grafo(self, grafo_id: str, formato: str) -> str:
        """
        Exporta um grafo para um formato específico.
        
        Args:
            grafo_id: ID do grafo.
            formato: Formato de exportação.
            
        Returns:
            str: Conteúdo do grafo no formato especificado.
            
        Raises:
            ValueError: Se o grafo não existir ou o formato não for suportado.
        """
        # Verifica se o formato é suportado
        if formato not in self.formatos_suportados:
            raise ValueError(f"Formato '{formato}' não suportado.")
        
        # Obtém o grafo
        grafo = self.grafo_service.obter_grafo(grafo_id)
        if not grafo:
            raise ValueError(f"Grafo com ID {grafo_id} não encontrado.")
        
        # Obtém a função de exportação
        exportar = self.formatos_suportados[formato]["exportar"]
        
        # Exporta o grafo
        conteudo = exportar(grafo)
        
        return conteudo
    
    def importar_grafo(self, nome: str, formato: str, conteudo: str) -> str:
        """
        Importa um grafo a partir de uma representação em um formato específico.
        
        Args:
            nome: Nome do grafo a ser criado.
            formato: Formato do grafo.
            conteudo: Conteúdo do grafo no formato especificado.
            
        Returns:
            str: ID do grafo importado.
            
        Raises:
            ValueError: Se o formato não for suportado ou o conteúdo for inválido.
        """
        # Verifica se o formato é suportado
        if formato not in self.formatos_suportados:
            raise ValueError(f"Formato '{formato}' não suportado.")
        
        # Obtém a função de importação
        importar = self.formatos_suportados[formato]["importar"]
        
        try:
            # Importa o grafo
            grafo = importar(conteudo, nome)
            
            # Determina se o grafo é direcionado e ponderado
            direcionado = grafo.eh_direcionado() if hasattr(grafo, 'eh_direcionado') else False
            ponderado = grafo.eh_ponderado() if hasattr(grafo, 'eh_ponderado') else False
            bipartido = grafo.eh_bipartido() if hasattr(grafo, 'eh_bipartido') else False
            
            # Cria um novo grafo no serviço
            grafo_id = self.grafo_service.criar_grafo(
                nome=nome,
                direcionado=direcionado,
                ponderado=ponderado,
                bipartido=bipartido
            )
            
            # Adiciona os vértices
            for v in grafo.obter_vertices():
                atributos = grafo.obter_atributos_vertice(v)
                conjunto = None
                if bipartido and hasattr(grafo, 'obter_conjunto_vertice'):
                    conjunto = grafo.obter_conjunto_vertice(v)
                self.grafo_service.adicionar_vertice(grafo_id, v, atributos, conjunto)
            
            # Adiciona as arestas
            for u, v in grafo.obter_arestas():
                atributos = grafo.obter_atributos_aresta(u, v)
                peso = 1.0
                if ponderado and hasattr(grafo, 'obter_peso_aresta'):
                    peso = grafo.obter_peso_aresta(u, v)
                self.grafo_service.adicionar_aresta(grafo_id, u, v, peso, atributos)
            
            return grafo_id
        except Exception as e:
            raise ValueError(f"Erro ao importar grafo: {str(e)}")
    
    def obter_mime_type(self, formato: str) -> str:
        """
        Obtém o MIME type para um formato específico.
        
        Args:
            formato: Formato do grafo.
            
        Returns:
            str: MIME type correspondente.
            
        Raises:
            ValueError: Se o formato não for suportado.
        """
        # Verifica se o formato é suportado
        if formato not in self.formatos_suportados:
            raise ValueError(f"Formato '{formato}' não suportado.")
        
        return self.formatos_suportados[formato]["mime_type"]
