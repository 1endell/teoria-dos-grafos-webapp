"""
Módulo para gerenciamento de projetos de estudo de teoria dos grafos.

Este módulo implementa funcionalidades para criar, gerenciar e persistir
projetos de estudo que agrupam múltiplos grafos, operações, algoritmos
e anotações relacionadas.
"""

import os
import json
import uuid
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Set

# Importações do backend de grafos
import sys
sys.path.append('/home/ubuntu')  # Adiciona o diretório raiz ao path
from grafo_backend.core.grafo import Grafo
from grafo_backend.persistencia.exportador import exportar_grafo
from grafo_backend.persistencia.importador import importar_grafo


class ProjetoEstudo:
    """
    Classe que representa um projeto de estudo de teoria dos grafos.
    
    Um projeto agrupa múltiplos grafos relacionados, operações realizadas,
    algoritmos aplicados, anotações e metadados para facilitar a continuidade
    de estudos e compartilhamento.
    """
    
    def __init__(self, titulo: str, descricao: str = "", autor: str = "Usuário"):
        """
        Inicializa um novo projeto de estudo.
        
        Args:
            titulo: Título do projeto
            descricao: Descrição do projeto (opcional)
            autor: Nome do autor do projeto (opcional)
        """
        self.id = str(uuid.uuid4())
        self.titulo = titulo
        self.descricao = descricao
        self.autor = autor
        self.data_criacao = datetime.now()
        self.data_atualizacao = self.data_criacao
        
        # Armazenamento de componentes do projeto
        self.grafos = {}  # id -> grafo
        self.operacoes = []  # Lista de operações realizadas
        self.algoritmos = []  # Lista de algoritmos aplicados
        self.notas = []  # Lista de anotações
        self.historico = []  # Histórico de ações no projeto
        self.tags = set()  # Tags para categorização
    
    def adicionar_grafo(self, grafo: Grafo, grafo_id: str = None) -> str:
        """
        Adiciona um grafo ao projeto.
        
        Args:
            grafo: Objeto Grafo a ser adicionado
            grafo_id: ID opcional para o grafo (se None, gera um novo ID)
            
        Returns:
            str: ID do grafo adicionado
        """
        if grafo_id is None:
            grafo_id = str(uuid.uuid4())
        
        self.grafos[grafo_id] = grafo
        self.data_atualizacao = datetime.now()
        
        # Registra no histórico
        self._registrar_acao(
            tipo="adicionar_grafo",
            descricao=f"Adicionado grafo '{grafo.nome}' ao projeto",
            detalhes={"grafo_id": grafo_id, "nome": grafo.nome}
        )
        
        return grafo_id
    
    def remover_grafo(self, grafo_id: str) -> bool:
        """
        Remove um grafo do projeto.
        
        Args:
            grafo_id: ID do grafo a ser removido
            
        Returns:
            bool: True se o grafo foi removido, False caso contrário
        """
        if grafo_id not in self.grafos:
            return False
        
        nome_grafo = self.grafos[grafo_id].nome
        del self.grafos[grafo_id]
        self.data_atualizacao = datetime.now()
        
        # Registra no histórico
        self._registrar_acao(
            tipo="remover_grafo",
            descricao=f"Removido grafo '{nome_grafo}' do projeto",
            detalhes={"grafo_id": grafo_id, "nome": nome_grafo}
        )
        
        return True
    
    def obter_grafo(self, grafo_id: str) -> Optional[Grafo]:
        """
        Obtém um grafo do projeto pelo ID.
        
        Args:
            grafo_id: ID do grafo
            
        Returns:
            Optional[Grafo]: O grafo correspondente ou None se não encontrado
        """
        return self.grafos.get(grafo_id)
    
    def listar_grafos(self) -> List[Dict[str, Any]]:
        """
        Lista todos os grafos do projeto com metadados.
        
        Returns:
            List[Dict[str, Any]]: Lista de metadados dos grafos
        """
        resultado = []
        for grafo_id, grafo in self.grafos.items():
            metadados = {
                "id": grafo_id,
                "nome": grafo.nome,
                "direcionado": grafo.eh_direcionado() if hasattr(grafo, 'eh_direcionado') else False,
                "ponderado": grafo.eh_ponderado() if hasattr(grafo, 'eh_ponderado') else False,
                "bipartido": grafo.eh_bipartido() if hasattr(grafo, 'eh_bipartido') else False,
                "num_vertices": grafo.numero_vertices(),
                "num_arestas": grafo.numero_arestas()
            }
            resultado.append(metadados)
        
        return resultado
    
    def registrar_operacao(self, tipo: str, descricao: str, 
                          grafos_entrada: List[str], grafo_saida: str,
                          parametros: Dict[str, Any] = None) -> int:
        """
        Registra uma operação realizada no projeto.
        
        Args:
            tipo: Tipo da operação (ex: "uniao", "intersecao")
            descricao: Descrição da operação
            grafos_entrada: Lista de IDs dos grafos de entrada
            grafo_saida: ID do grafo resultante
            parametros: Parâmetros adicionais da operação (opcional)
            
        Returns:
            int: Índice da operação registrada
        """
        if parametros is None:
            parametros = {}
        
        operacao = {
            "tipo": tipo,
            "descricao": descricao,
            "grafos_entrada": grafos_entrada,
            "grafo_saida": grafo_saida,
            "parametros": parametros,
            "timestamp": datetime.now()
        }
        
        self.operacoes.append(operacao)
        self.data_atualizacao = datetime.now()
        
        # Registra no histórico
        self._registrar_acao(
            tipo="operacao",
            descricao=descricao,
            detalhes={"tipo_operacao": tipo, "grafo_saida": grafo_saida}
        )
        
        return len(self.operacoes) - 1
    
    def registrar_algoritmo(self, nome: str, descricao: str, 
                           grafo_id: str, parametros: Dict[str, Any],
                           resultado: Any, passos: List[Dict[str, Any]] = None) -> int:
        """
        Registra a aplicação de um algoritmo no projeto.
        
        Args:
            nome: Nome do algoritmo
            descricao: Descrição da aplicação
            grafo_id: ID do grafo onde o algoritmo foi aplicado
            parametros: Parâmetros do algoritmo
            resultado: Resultado da execução
            passos: Lista de passos de execução (opcional)
            
        Returns:
            int: Índice do algoritmo registrado
        """
        if passos is None:
            passos = []
        
        algoritmo = {
            "nome": nome,
            "descricao": descricao,
            "grafo_id": grafo_id,
            "parametros": parametros,
            "resultado": resultado,
            "passos": passos,
            "timestamp": datetime.now()
        }
        
        self.algoritmos.append(algoritmo)
        self.data_atualizacao = datetime.now()
        
        # Registra no histórico
        self._registrar_acao(
            tipo="algoritmo",
            descricao=f"Aplicado algoritmo '{nome}' ao grafo",
            detalhes={"algoritmo": nome, "grafo_id": grafo_id}
        )
        
        return len(self.algoritmos) - 1
    
    def adicionar_nota(self, texto: str, grafo_id: str = None) -> int:
        """
        Adiciona uma nota ao projeto.
        
        Args:
            texto: Conteúdo da nota
            grafo_id: ID do grafo relacionado (opcional)
            
        Returns:
            int: Índice da nota adicionada
        """
        nota = {
            "texto": texto,
            "grafo_id": grafo_id,
            "timestamp": datetime.now()
        }
        
        self.notas.append(nota)
        self.data_atualizacao = datetime.now()
        
        # Registra no histórico
        self._registrar_acao(
            tipo="nota",
            descricao="Adicionada nota ao projeto",
            detalhes={"grafo_id": grafo_id} if grafo_id else {}
        )
        
        return len(self.notas) - 1
    
    def adicionar_tag(self, tag: str) -> bool:
        """
        Adiciona uma tag ao projeto.
        
        Args:
            tag: Tag a ser adicionada
            
        Returns:
            bool: True se a tag foi adicionada, False se já existia
        """
        if tag in self.tags:
            return False
        
        self.tags.add(tag)
        self.data_atualizacao = datetime.now()
        
        # Registra no histórico
        self._registrar_acao(
            tipo="tag",
            descricao=f"Adicionada tag '{tag}' ao projeto",
            detalhes={"tag": tag}
        )
        
        return True
    
    def remover_tag(self, tag: str) -> bool:
        """
        Remove uma tag do projeto.
        
        Args:
            tag: Tag a ser removida
            
        Returns:
            bool: True se a tag foi removida, False se não existia
        """
        if tag not in self.tags:
            return False
        
        self.tags.remove(tag)
        self.data_atualizacao = datetime.now()
        
        # Registra no histórico
        self._registrar_acao(
            tipo="tag",
            descricao=f"Removida tag '{tag}' do projeto",
            detalhes={"tag": tag}
        )
        
        return True
    
    def obter_historico(self) -> List[Dict[str, Any]]:
        """
        Obtém o histórico completo de ações no projeto.
        
        Returns:
            List[Dict[str, Any]]: Lista de ações no histórico
        """
        return self.historico
    
    def obter_metadados(self) -> Dict[str, Any]:
        """
        Obtém os metadados do projeto.
        
        Returns:
            Dict[str, Any]: Metadados do projeto
        """
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "autor": self.autor,
            "data_criacao": self.data_criacao,
            "data_atualizacao": self.data_atualizacao,
            "num_grafos": len(self.grafos),
            "num_operacoes": len(self.operacoes),
            "num_algoritmos": len(self.algoritmos),
            "num_notas": len(self.notas),
            "tags": list(self.tags)
        }
    
    def _registrar_acao(self, tipo: str, descricao: str, detalhes: Dict[str, Any] = None) -> None:
        """
        Registra uma ação no histórico do projeto.
        
        Args:
            tipo: Tipo da ação
            descricao: Descrição da ação
            detalhes: Detalhes adicionais (opcional)
        """
        if detalhes is None:
            detalhes = {}
        
        acao = {
            "tipo": tipo,
            "descricao": descricao,
            "detalhes": detalhes,
            "timestamp": datetime.now()
        }
        
        self.historico.append(acao)


class GerenciadorProjetos:
    """
    Classe para gerenciar projetos de estudo, incluindo persistência e importação/exportação.
    """
    
    def __init__(self, diretorio_armazenamento: str = None):
        """
        Inicializa o gerenciador de projetos.
        
        Args:
            diretorio_armazenamento: Diretório para armazenamento de projetos (opcional)
        """
        if diretorio_armazenamento is None:
            diretorio_armazenamento = os.path.join(os.path.dirname(__file__), '..', 'data', 'projetos')
            
        # Garante que o diretório existe
        os.makedirs(diretorio_armazenamento, exist_ok=True)
        
        self.diretorio_armazenamento = diretorio_armazenamento
        self.projetos_em_memoria = {}  # id -> projeto
    
    def criar_projeto(self, titulo: str, descricao: str = "", autor: str = "Usuário") -> str:
        """
        Cria um novo projeto de estudo.
        
        Args:
            titulo: Título do projeto
            descricao: Descrição do projeto (opcional)
            autor: Nome do autor do projeto (opcional)
            
        Returns:
            str: ID do projeto criado
        """
        projeto = ProjetoEstudo(titulo=titulo, descricao=descricao, autor=autor)
        self.projetos_em_memoria[projeto.id] = projeto
        return projeto.id
    
    def obter_projeto(self, projeto_id: str) -> Optional[ProjetoEstudo]:
        """
        Obtém um projeto pelo ID.
        
        Args:
            projeto_id: ID do projeto
            
        Returns:
            Optional[ProjetoEstudo]: O projeto correspondente ou None se não encontrado
        """
        # Verifica se o projeto está em memória
        if projeto_id in self.projetos_em_memoria:
            return self.projetos_em_memoria[projeto_id]
        
        # Tenta carregar do armazenamento
        try:
            return self.carregar_projeto(projeto_id)
        except:
            return None
    
    def listar_projetos(self, session_id: str = None) -> List[Dict[str, Any]]:
        """
        Lista todos os projetos disponíveis.
        
        Args:
            session_id: ID da sessão para filtrar projetos (opcional)
            
        Returns:
            List[Dict[str, Any]]: Lista de metadados dos projetos
        """
        # Implementação básica sem filtro por sessão
        # (será expandido quando implementarmos o sistema de sessões)
        resultado = []
        
        # Adiciona projetos em memória
        for projeto_id, projeto in self.projetos_em_memoria.items():
            resultado.append(projeto.obter_metadados())
        
        # Adiciona projetos armazenados em disco
        for arquivo in os.listdir(self.diretorio_armazenamento):
            if arquivo.endswith('.json'):
                projeto_id = arquivo[:-5]  # Remove a extensão .json
                
                # Pula se já está em memória
                if projeto_id in self.projetos_em_memoria:
                    continue
                
                try:
                    # Carrega apenas os metadados
                    with open(os.path.join(self.diretorio_armazenamento, arquivo), 'r') as f:
                        dados = json.load(f)
                        metadados = {
                            "id": dados.get("id", projeto_id),
                            "titulo": dados.get("titulo", "Sem título"),
                            "descricao": dados.get("descricao", ""),
                            "autor": dados.get("autor", "Desconhecido"),
                            "data_criacao": dados.get("data_criacao"),
                            "data_atualizacao": dados.get("data_atualizacao"),
                            "num_grafos": len(dados.get("grafos", {})),
                            "tags": dados.get("tags", [])
                        }
                        resultado.append(metadados)
                except:
                    # Ignora arquivos com erro
                    continue
        
        return resultado
    
    def salvar_projeto(self, projeto_id: str) -> bool:
        """
        Salva um projeto no armazenamento.
        
        Args:
            projeto_id: ID do projeto a ser salvo
            
        Returns:
            bool: True se o projeto foi salvo com sucesso, False caso contrário
        """
        projeto = self.obter_projeto(projeto_id)
        if not projeto:
            return False
        
        # Prepara o dicionário para serialização
        dados = {
            "id": projeto.id,
            "titulo": projeto.titulo,
            "descricao": projeto.descricao,
            "autor": projeto.autor,
            "data_criacao": projeto.data_criacao.isoformat(),
            "data_atualizacao": projeto.data_atualizacao.isoformat(),
            "tags": list(projeto.tags),
            "grafos": {},
            "operacoes": projeto.operacoes,
            "algoritmos": projeto.algoritmos,
            "notas": projeto.notas,
            "historico": projeto.historico
        }
        
        # Serializa os grafos
        for grafo_id, grafo in projeto.grafos.items():
            # Exporta o grafo para GraphML como representação padrão
            conteudo_graphml = exportar_grafo(grafo, "graphml")
            
            dados["grafos"][grafo_id] = {
                "nome": grafo.nome,
                "representacao": conteudo_graphml,
                "formato": "graphml"
            }
        
        # Salva o arquivo JSON
        try:
            caminho_arquivo = os.path.join(self.diretorio_armazenamento, f"{projeto_id}.json")
            with open(caminho_arquivo, 'w') as f:
                json.dump(dados, f, indent=2, default=str)
            return True
        except Exception as e:
            print(f"Erro ao salvar projeto: {e}")
            return False
    
    def carregar_projeto(self, projeto_id: str) -> Optional[ProjetoEstudo]:
        """
        Carrega um projeto do armazenamento.
        
        Args:
            projeto_id: ID do projeto a ser carregado
            
        Returns:
            Optional[ProjetoEstudo]: O projeto carregado ou None se não encontrado
        """
        caminho_arquivo = os.path.join(self.diretorio_armazenamento, f"{projeto_id}.json")
        if not os.path.exists(caminho_arquivo):
            return None
        
        try:
            with open(caminho_arquivo, 'r') as f:
                dados = json.load(f)
            
            # Cria o objeto de projeto
            projeto = ProjetoEstudo(
                titulo=dados.get("titulo", "Sem título"),
                descricao=dados.get("descricao", ""),
                autor=dados.get("autor", "Desconhecido")
            )
            
            # Atualiza os atributos
            projeto.id = dados.get("id", projeto_id)
            projeto.data_criacao = datetime.fromisoformat(dados.get("data_criacao", datetime.now().isoformat()))
            projeto.data_atualizacao = datetime.fromisoformat(dados.get("data_atualizacao", datetime.now().isoformat()))
            projeto.tags = set(dados.get("tags", []))
            projeto.operacoes = dados.get("operacoes", [])
            projeto.algoritmos = dados.get("algoritmos", [])
            projeto.notas = dados.get("notas", [])
            projeto.historico = dados.get("historico", [])
            
            # Carrega os grafos
            for grafo_id, grafo_dados in dados.get("grafos", {}).items():
                try:
                    representacao = grafo_dados.get("representacao", "")
                    formato = grafo_dados.get("formato", "graphml")
                    
                    # Importa o grafo da representação
                    grafo = importar_grafo(representacao, formato)
                    
                    # Atualiza o nome se necessário
                    if "nome" in grafo_dados:
                        grafo.nome = grafo_dados["nome"]
                    
                    # Adiciona ao projeto
                    projeto.grafos[grafo_id] = grafo
                except Exception as e:
                    print(f"Erro ao carregar grafo {grafo_id}: {e}")
            
            # Adiciona à memória e retorna
            self.projetos_em_memoria[projeto_id] = projeto
            return projeto
            
        except Exception as e:
            print(f"Erro ao carregar projeto: {e}")
            return None
    
    def excluir_projeto(self, projeto_id: str) -> bool:
        """
        Exclui um projeto.
        
        Args:
            projeto_id: ID do projeto a ser excluído
            
        Returns:
            bool: True se o projeto foi excluído com sucesso, False caso contrário
        """
        # Remove da memória
        if projeto_id in self.projetos_em_memoria:
            del self.projetos_em_memoria[projeto_id]
        
        # Remove do armazenamento
        caminho_arquivo = os.path.join(self.diretorio_armazenamento, f"{projeto_id}.json")
        if os.path.exists(caminho_arquivo):
            try:
                os.remove(caminho_arquivo)
                return True
            except:
                return False
        
        return True  # Considera sucesso se o projeto não existia
    
    def exportar_projeto(self, projeto_id: str, formato: str = "json") -> Optional[str]:
        """
        Exporta um projeto para um formato específico.
        
        Args:
            projeto_id: ID do projeto a ser exportado
            formato: Formato de exportação ("json", "zip")
            
        Returns:
            Optional[str]: Conteúdo do projeto exportado ou None em caso de erro
        """
        projeto = self.obter_projeto(projeto_id)
        if not projeto:
            return None
        
        if formato == "json":
            # Prepara o dicionário para serialização
            dados = {
                "id": projeto.id,
                "titulo": projeto.titulo,
                "descricao": projeto.descricao,
                "autor": projeto.autor,
                "data_criacao": projeto.data_criacao.isoformat(),
                "data_atualizacao": projeto.data_atualizacao.isoformat(),
                "tags": list(projeto.tags),
                "grafos": {},
                "operacoes": projeto.operacoes,
                "algoritmos": projeto.algoritmos,
                "notas": projeto.notas,
                "historico": projeto.historico
            }
            
            # Serializa os grafos
            for grafo_id, grafo in projeto.grafos.items():
                # Exporta o grafo para GraphML como representação padrão
                conteudo_graphml = exportar_grafo(grafo, "graphml")
                
                dados["grafos"][grafo_id] = {
                    "nome": grafo.nome,
                    "representacao": conteudo_graphml,
                    "formato": "graphml"
                }
            
            # Retorna o JSON como string
            return json.dumps(dados, indent=2, default=str)
        
        elif formato == "zip":
            # Implementação para formato ZIP seria aqui
            # (requer manipulação de arquivos temporários e compressão)
            return None
        
        else:
            return None
    
    def importar_projeto(self, conteudo: str, formato: str = "json") -> Optional[str]:
        """
        Importa um projeto a partir de uma representação.
        
        Args:
            conteudo: Conteúdo do projeto
            formato: Formato do conteúdo ("json", "zip")
            
        Returns:
            Optional[str]: ID do projeto importado ou None em caso de erro
        """
        if formato == "json":
            try:
                dados = json.loads(conteudo)
                
                # Cria o objeto de projeto
                projeto = ProjetoEstudo(
                    titulo=dados.get("titulo", "Projeto Importado"),
                    descricao=dados.get("descricao", ""),
                    autor=dados.get("autor", "Usuário")
                )
                
                # Atualiza os atributos
                if "id" in dados:
                    projeto.id = dados["id"]
                if "data_criacao" in dados:
                    projeto.data_criacao = datetime.fromisoformat(dados["data_criacao"])
                if "data_atualizacao" in dados:
                    projeto.data_atualizacao = datetime.fromisoformat(dados["data_atualizacao"])
                if "tags" in dados:
                    projeto.tags = set(dados["tags"])
                if "operacoes" in dados:
                    projeto.operacoes = dados["operacoes"]
                if "algoritmos" in dados:
                    projeto.algoritmos = dados["algoritmos"]
                if "notas" in dados:
                    projeto.notas = dados["notas"]
                if "historico" in dados:
                    projeto.historico = dados["historico"]
                
                # Importa os grafos
                for grafo_id, grafo_dados in dados.get("grafos", {}).items():
                    try:
                        representacao = grafo_dados.get("representacao", "")
                        formato_grafo = grafo_dados.get("formato", "graphml")
                        
                        # Importa o grafo da representação
                        grafo = importar_grafo(representacao, formato_grafo)
                        
                        # Atualiza o nome se necessário
                        if "nome" in grafo_dados:
                            grafo.nome = grafo_dados["nome"]
                        
                        # Adiciona ao projeto
                        projeto.grafos[grafo_id] = grafo
                    except Exception as e:
                        print(f"Erro ao importar grafo {grafo_id}: {e}")
                
                # Adiciona à memória
                self.projetos_em_memoria[projeto.id] = projeto
                
                return projeto.id
                
            except Exception as e:
                print(f"Erro ao importar projeto: {e}")
                return None
        
        elif formato == "zip":
            # Implementação para formato ZIP seria aqui
            return None
        
        else:
            return None
