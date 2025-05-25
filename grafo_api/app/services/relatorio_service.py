"""
Módulo para geração de relatórios didáticos em PDF para teoria dos grafos.

Este módulo utiliza WeasyPrint para gerar relatórios PDF detalhados e didáticos
sobre grafos, algoritmos e operações realizadas, com explicações passo a passo
e visualizações.
"""

import os
import time
import tempfile
import base64
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

import matplotlib.pyplot as plt
import networkx as nx
from weasyprint import HTML, CSS
from jinja2 import Environment, FileSystemLoader

# Importações do backend de grafos
import sys
sys.path.append('/home/ubuntu')  # Adiciona o diretório raiz ao path
from grafo_backend.core.grafo import Grafo
from grafo_backend.visualizacao import gerar_layout, visualizar_grafo


class RelatorioGrafoPDF:
    """
    Classe para geração de relatórios didáticos em PDF sobre teoria dos grafos.
    """
    
    def __init__(self, template_dir: str = None):
        """
        Inicializa o gerador de relatórios.
        
        Args:
            template_dir: Diretório contendo os templates HTML. Se None, usa o diretório padrão.
        """
        if template_dir is None:
            # Usa o diretório 'templates' dentro do diretório do módulo
            template_dir = os.path.join(os.path.dirname(__file__), 'templates')
            
            # Se o diretório não existir, cria-o
            if not os.path.exists(template_dir):
                os.makedirs(template_dir)
                
                # Cria os templates padrão
                self._criar_templates_padrao(template_dir)
        
        self.template_dir = template_dir
        self.env = Environment(loader=FileSystemLoader(template_dir))
        
        # Registra filtros personalizados
        self.env.filters['datetime_format'] = self._datetime_format
    
    def gerar_relatorio(self, 
                       titulo: str,
                       grafos: List[Dict[str, Any]],
                       operacoes: List[Dict[str, Any]] = None,
                       algoritmos: List[Dict[str, Any]] = None,
                       metadados: Dict[str, Any] = None,
                       config: Dict[str, Any] = None) -> bytes:
        """
        Gera um relatório PDF didático sobre grafos e operações.
        
        Args:
            titulo: Título do relatório
            grafos: Lista de dicionários contendo informações sobre os grafos
            operacoes: Lista de operações realizadas (opcional)
            algoritmos: Lista de algoritmos aplicados (opcional)
            metadados: Metadados adicionais para o relatório (opcional)
            config: Configurações de formatação (opcional)
            
        Returns:
            bytes: Conteúdo do PDF gerado
        """
        # Configura valores padrão
        if operacoes is None:
            operacoes = []
        if algoritmos is None:
            algoritmos = []
        if metadados is None:
            metadados = {}
        if config is None:
            config = {}
        
        # Valores padrão para metadados
        metadados.setdefault('autor', 'Usuário da Plataforma')
        metadados.setdefault('data', datetime.now())
        metadados.setdefault('descricao', 'Relatório didático de teoria dos grafos')
        
        # Valores padrão para configuração
        config.setdefault('incluir_teoria', True)
        config.setdefault('incluir_passos', True)
        config.setdefault('incluir_referencias', True)
        config.setdefault('estilo', 'padrao')
        
        # Gera imagens para os grafos
        for grafo_info in grafos:
            if 'grafo' in grafo_info:
                grafo = grafo_info['grafo']
                grafo_info['imagem_base64'] = self._gerar_imagem_grafo_base64(grafo)
        
        # Gera imagens para os resultados dos algoritmos, se necessário
        for algo_info in algoritmos:
            if 'resultado_visual' in algo_info and isinstance(algo_info['resultado_visual'], Grafo):
                grafo = algo_info['resultado_visual']
                algo_info['imagem_resultado_base64'] = self._gerar_imagem_grafo_base64(grafo)
        
        # Carrega o template
        template = self.env.get_template(f"relatorio_{config['estilo']}.html")
        
        # Renderiza o HTML
        html_content = template.render(
            titulo=titulo,
            grafos=grafos,
            operacoes=operacoes,
            algoritmos=algoritmos,
            metadados=metadados,
            config=config
        )
        
        # Carrega o CSS
        css_file = os.path.join(self.template_dir, f"estilo_{config['estilo']}.css")
        css = CSS(filename=css_file)
        
        # Gera o PDF
        html = HTML(string=html_content)
        pdf_bytes = html.write_pdf(stylesheets=[css])
        
        return pdf_bytes
    
    def gerar_relatorio_algoritmo(self,
                                 titulo: str,
                                 grafo: Grafo,
                                 algoritmo: str,
                                 parametros: Dict[str, Any],
                                 resultado: Any,
                                 passos: List[Dict[str, Any]] = None,
                                 teoria: str = None,
                                 referencias: List[str] = None,
                                 config: Dict[str, Any] = None) -> bytes:
        """
        Gera um relatório PDF didático focado em um algoritmo específico.
        
        Args:
            titulo: Título do relatório
            grafo: Grafo utilizado no algoritmo
            algoritmo: Nome do algoritmo
            parametros: Parâmetros utilizados no algoritmo
            resultado: Resultado do algoritmo
            passos: Lista de passos de execução do algoritmo (opcional)
            teoria: Explicação teórica do algoritmo (opcional)
            referencias: Referências bibliográficas (opcional)
            config: Configurações de formatação (opcional)
            
        Returns:
            bytes: Conteúdo do PDF gerado
        """
        # Configura valores padrão
        if passos is None:
            passos = []
        if teoria is None:
            teoria = self._obter_teoria_algoritmo(algoritmo)
        if referencias is None:
            referencias = self._obter_referencias_algoritmo(algoritmo)
        if config is None:
            config = {}
        
        # Prepara os dados do grafo
        grafo_info = {
            'id': 'grafo_principal',
            'nome': getattr(grafo, 'nome', 'Grafo'),
            'grafo': grafo,
            'num_vertices': grafo.numero_vertices(),
            'num_arestas': grafo.numero_arestas(),
            'direcionado': grafo.eh_direcionado() if hasattr(grafo, 'eh_direcionado') else False,
            'ponderado': grafo.eh_ponderado() if hasattr(grafo, 'eh_ponderado') else False
        }
        
        # Prepara os dados do algoritmo
        algoritmo_info = {
            'nome': algoritmo,
            'parametros': parametros,
            'resultado': resultado,
            'passos': passos,
            'teoria': teoria,
            'referencias': referencias
        }
        
        # Se o resultado for um grafo, adiciona visualização
        if isinstance(resultado, Grafo):
            algoritmo_info['resultado_visual'] = resultado
        
        # Gera o relatório
        return self.gerar_relatorio(
            titulo=titulo,
            grafos=[grafo_info],
            algoritmos=[algoritmo_info],
            config=config
        )
    
    def gerar_relatorio_comparacao(self,
                                  titulo: str,
                                  grafo1: Grafo,
                                  grafo2: Grafo,
                                  metrica: str,
                                  resultado: Any,
                                  explicacao: str = None,
                                  config: Dict[str, Any] = None) -> bytes:
        """
        Gera um relatório PDF didático comparando dois grafos.
        
        Args:
            titulo: Título do relatório
            grafo1: Primeiro grafo
            grafo2: Segundo grafo
            metrica: Métrica de comparação utilizada
            resultado: Resultado da comparação
            explicacao: Explicação didática da comparação (opcional)
            config: Configurações de formatação (opcional)
            
        Returns:
            bytes: Conteúdo do PDF gerado
        """
        # Configura valores padrão
        if explicacao is None:
            explicacao = self._obter_explicacao_metrica(metrica)
        if config is None:
            config = {}
        
        # Prepara os dados dos grafos
        grafo1_info = {
            'id': 'grafo1',
            'nome': getattr(grafo1, 'nome', 'Grafo 1'),
            'grafo': grafo1,
            'num_vertices': grafo1.numero_vertices(),
            'num_arestas': grafo1.numero_arestas(),
            'direcionado': grafo1.eh_direcionado() if hasattr(grafo1, 'eh_direcionado') else False,
            'ponderado': grafo1.eh_ponderado() if hasattr(grafo1, 'eh_ponderado') else False
        }
        
        grafo2_info = {
            'id': 'grafo2',
            'nome': getattr(grafo2, 'nome', 'Grafo 2'),
            'grafo': grafo2,
            'num_vertices': grafo2.numero_vertices(),
            'num_arestas': grafo2.numero_arestas(),
            'direcionado': grafo2.eh_direcionado() if hasattr(grafo2, 'eh_direcionado') else False,
            'ponderado': grafo2.eh_ponderado() if hasattr(grafo2, 'eh_ponderado') else False
        }
        
        # Prepara os metadados
        metadados = {
            'tipo_relatorio': 'comparacao',
            'metrica': metrica,
            'explicacao': explicacao
        }
        
        # Prepara os dados da operação
        operacao_info = {
            'tipo': 'comparacao',
            'nome': f"Comparação usando {metrica}",
            'descricao': f"Comparação entre {grafo1_info['nome']} e {grafo2_info['nome']} usando a métrica {metrica}",
            'resultado': resultado
        }
        
        # Gera o relatório
        return self.gerar_relatorio(
            titulo=titulo,
            grafos=[grafo1_info, grafo2_info],
            operacoes=[operacao_info],
            metadados=metadados,
            config=config
        )
    
    def gerar_relatorio_projeto(self,
                               projeto: Dict[str, Any],
                               config: Dict[str, Any] = None) -> bytes:
        """
        Gera um relatório PDF completo de um projeto de estudo.
        
        Args:
            projeto: Dicionário contendo informações do projeto
            config: Configurações de formatação (opcional)
            
        Returns:
            bytes: Conteúdo do PDF gerado
        """
        # Configura valores padrão
        if config is None:
            config = {}
        
        # Extrai informações do projeto
        titulo = projeto.get('titulo', 'Projeto de Estudo de Grafos')
        descricao = projeto.get('descricao', '')
        grafos = projeto.get('grafos', [])
        operacoes = projeto.get('operacoes', [])
        algoritmos = projeto.get('algoritmos', [])
        notas = projeto.get('notas', [])
        
        # Prepara os metadados
        metadados = {
            'tipo_relatorio': 'projeto',
            'autor': projeto.get('autor', 'Usuário da Plataforma'),
            'data_criacao': projeto.get('data_criacao', datetime.now()),
            'data_atualizacao': projeto.get('data_atualizacao', datetime.now()),
            'descricao': descricao,
            'notas': notas
        }
        
        # Gera o relatório
        return self.gerar_relatorio(
            titulo=titulo,
            grafos=grafos,
            operacoes=operacoes,
            algoritmos=algoritmos,
            metadados=metadados,
            config=config
        )
    
    def _gerar_imagem_grafo_base64(self, grafo: Grafo, layout: str = 'spring', 
                                  largura: int = 800, altura: int = 600) -> str:
        """
        Gera uma imagem de um grafo e retorna como string base64.
        
        Args:
            grafo: Grafo a ser visualizado
            layout: Layout de visualização
            largura: Largura da imagem em pixels
            altura: Altura da imagem em pixels
            
        Returns:
            str: Imagem em formato base64
        """
        # Obtém o grafo NetworkX subjacente
        g_nx = grafo.obter_grafo_networkx()
        
        # Configura a figura
        plt.figure(figsize=(largura/100, altura/100), dpi=100)
        
        # Gera o layout
        pos = None
        if layout == 'spring':
            pos = nx.spring_layout(g_nx)
        elif layout == 'circular':
            pos = nx.circular_layout(g_nx)
        elif layout == 'spectral':
            pos = nx.spectral_layout(g_nx)
        else:
            pos = nx.spring_layout(g_nx)  # Layout padrão
        
        # Desenha o grafo
        nx.draw(g_nx, pos, with_labels=True, node_color='skyblue', node_size=700, 
                edge_color='gray', width=1, font_size=10, font_weight='bold')
        
        # Se o grafo for ponderado, adiciona os pesos das arestas
        if hasattr(grafo, 'eh_ponderado') and grafo.eh_ponderado():
            edge_labels = {}
            for u, v in g_nx.edges():
                edge_labels[(u, v)] = grafo.obter_peso_aresta(u, v)
            nx.draw_networkx_edge_labels(g_nx, pos, edge_labels=edge_labels)
        
        # Salva a imagem em um buffer
        buf = tempfile.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close()
        
        # Converte para base64
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        
        return img_base64
    
    def _obter_teoria_algoritmo(self, algoritmo: str) -> str:
        """
        Obtém a explicação teórica de um algoritmo.
        
        Args:
            algoritmo: Nome do algoritmo
            
        Returns:
            str: Explicação teórica
        """
        # Dicionário de explicações teóricas para algoritmos comuns
        teorias = {
            'dijkstra': """
                <h3>Algoritmo de Dijkstra</h3>
                <p>O algoritmo de Dijkstra é um algoritmo para encontrar os caminhos mais curtos entre nós em um grafo, 
                que pode representar, por exemplo, redes rodoviárias. Foi concebido pelo cientista da computação holandês 
                Edsger W. Dijkstra em 1956 e publicado três anos depois.</p>
                
                <h4>Funcionamento</h4>
                <p>O algoritmo existe em muitas variantes. A variante original de Dijkstra encontra o caminho mais curto 
                entre dois nós específicos. Uma variante mais comum fixa um único nó como o nó "fonte" e encontra 
                caminhos mais curtos desse nó para todos os outros nós no grafo, produzindo uma árvore de caminhos mais curtos.</p>
                
                <h4>Passos do Algoritmo</h4>
                <ol>
                    <li>Atribua a cada nó um valor de distância tentativa: zero para o nó inicial e infinito para todos os outros nós.</li>
                    <li>Marque todos os nós como não visitados. Crie um conjunto de todos os nós não visitados chamado conjunto não visitado.</li>
                    <li>Para o nó atual, considere todos os seus vizinhos não visitados e calcule suas distâncias tentativas. 
                    Compare a distância tentativa recém-calculada com o valor atual atribuído e atribua o menor.</li>
                    <li>Quando terminar de considerar todos os vizinhos não visitados do nó atual, marque o nó atual como visitado 
                    e remova-o do conjunto não visitado.</li>
                    <li>Se o nó de destino foi marcado como visitado ou se a menor distância tentativa entre os nós no conjunto 
                    não visitado é infinito, então pare.</li>
                    <li>Caso contrário, selecione o nó não visitado com a menor distância tentativa, defina-o como o novo nó atual e volte ao passo 3.</li>
                </ol>
                
                <h4>Complexidade</h4>
                <p>A complexidade de tempo do algoritmo de Dijkstra depende da implementação. Usando uma fila de prioridade 
                (heap binário), a complexidade é O((V + E) log V), onde V é o número de vértices e E é o número de arestas.</p>
            """,
            
            'kruskal': """
                <h3>Algoritmo de Kruskal</h3>
                <p>O algoritmo de Kruskal é um algoritmo em teoria dos grafos que encontra uma árvore geradora mínima 
                para um grafo conexo com pesos. Isso significa que ele encontra um subconjunto das arestas que forma uma 
                árvore que inclui todos os vértices, onde o peso total das arestas na árvore é minimizado.</p>
                
                <h4>Funcionamento</h4>
                <p>O algoritmo de Kruskal é um algoritmo guloso que constrói a árvore geradora mínima adicionando arestas 
                em ordem crescente de peso, desde que não formem ciclos.</p>
                
                <h4>Passos do Algoritmo</h4>
                <ol>
                    <li>Ordene todas as arestas em ordem não decrescente de seus pesos.</li>
                    <li>Inicialize uma floresta vazia F (um conjunto de árvores).</li>
                    <li>Repita os seguintes passos até que a floresta se torne uma árvore geradora:
                        <ul>
                            <li>Escolha a aresta de menor peso que não forma um ciclo quando adicionada à floresta.</li>
                            <li>Adicione esta aresta à floresta.</li>
                        </ul>
                    </li>
                </ol>
                
                <h4>Complexidade</h4>
                <p>A complexidade de tempo do algoritmo de Kruskal é O(E log E) ou O(E log V), onde E é o número de arestas 
                e V é o número de vértices. Isso se deve principalmente à ordenação das arestas.</p>
            """,
            
            'ford_fulkerson': """
                <h3>Algoritmo de Ford-Fulkerson</h3>
                <p>O algoritmo de Ford-Fulkerson é um algoritmo que calcula o fluxo máximo em uma rede de fluxo. 
                Foi publicado em 1956 por L. R. Ford, Jr. e D. R. Fulkerson.</p>
                
                <h4>Funcionamento</h4>
                <p>O algoritmo funciona aumentando iterativamente o fluxo ao longo dos caminhos da fonte ao sumidouro, 
                até que nenhum caminho de aumento possa ser encontrado.</p>
                
                <h4>Passos do Algoritmo</h4>
                <ol>
                    <li>Inicialize o fluxo em todas as arestas como 0.</li>
                    <li>Enquanto existir um caminho de aumento da fonte ao sumidouro:
                        <ul>
                            <li>Encontre um caminho de aumento usando busca em largura ou busca em profundidade.</li>
                            <li>Calcule a capacidade residual do caminho (o mínimo das capacidades residuais das arestas no caminho).</li>
                            <li>Aumente o fluxo ao longo do caminho pela capacidade residual.</li>
                        </ul>
                    </li>
                </ol>
                
                <h4>Complexidade</h4>
                <p>A complexidade de tempo do algoritmo de Ford-Fulkerson depende do método usado para encontrar caminhos de aumento 
                e dos valores das capacidades. Se as capacidades são inteiras e o fluxo máximo é F, a complexidade é O(E * F), 
                onde E é o número de arestas.</p>
            """,
            
            'coloracao_welsh_powell': """
                <h3>Algoritmo de Coloração Welsh-Powell</h3>
                <p>O algoritmo de Welsh-Powell é um algoritmo guloso para coloração de vértices em um grafo. 
                Ele tenta minimizar o número de cores usadas, embora não garanta encontrar o número cromático exato.</p>
                
                <h4>Funcionamento</h4>
                <p>O algoritmo ordena os vértices por grau decrescente e então atribui cores sequencialmente, 
                garantindo que vértices adjacentes não recebam a mesma cor.</p>
                
                <h4>Passos do Algoritmo</h4>
                <ol>
                    <li>Ordene os vértices em ordem decrescente de grau.</li>
                    <li>Atribua a primeira cor ao primeiro vértice.</li>
                    <li>Percorra os vértices restantes em ordem e atribua a cor atual a cada vértice que não é adjacente 
                    a nenhum vértice já colorido com essa cor.</li>
                    <li>Repita o passo 3 com uma nova cor até que todos os vértices estejam coloridos.</li>
                </ol>
                
                <h4>Complexidade</h4>
                <p>A complexidade de tempo do algoritmo Welsh-Powell é O(V² + E), onde V é o número de vértices e E é o número de arestas.</p>
            """,
            
            # Adicione mais algoritmos conforme necessário
        }
        
        # Retorna a teoria do algoritmo ou uma mensagem padrão
        return teorias.get(algoritmo, f"<p>Teoria para o algoritmo {algoritmo} não disponível.</p>")
    
    def _obter_referencias_algoritmo(self, algoritmo: str) -> List[str]:
        """
        Obtém referências bibliográficas para um algoritmo.
        
        Args:
            algoritmo: Nome do algoritmo
            
        Returns:
            List[str]: Lista de referências
        """
        # Dicionário de referências para algoritmos comuns
        referencias = {
            'dijkstra': [
                "Dijkstra, E. W. (1959). \"A note on two problems in connexion with graphs\". Numerische Mathematik, 1, 269-271.",
                "Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). \"Introduction to Algorithms\" (3rd ed.). MIT Press.",
                "Sedgewick, R., & Wayne, K. (2011). \"Algorithms\" (4th ed.). Addison-Wesley Professional."
            ],
            'kruskal': [
                "Kruskal, J. B. (1956). \"On the shortest spanning subtree of a graph and the traveling salesman problem\". Proceedings of the American Mathematical Society, 7(1), 48-50.",
                "Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). \"Introduction to Algorithms\" (3rd ed.). MIT Press."
            ],
            'ford_fulkerson': [
                "Ford, L. R., & Fulkerson, D. R. (1956). \"Maximal flow through a network\". Canadian Journal of Mathematics, 8, 399-404.",
                "Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). \"Introduction to Algorithms\" (3rd ed.). MIT Press."
            ],
            'coloracao_welsh_powell': [
                "Welsh, D. J. A., & Powell, M. B. (1967). \"An upper bound for the chromatic number of a graph and its application to timetabling problems\". The Computer Journal, 10(1), 85-86.",
                "Diestel, R. (2017). \"Graph Theory\" (5th ed.). Springer."
            ],
            # Adicione mais algoritmos conforme necessário
        }
        
        # Retorna as referências do algoritmo ou uma lista vazia
        return referencias.get(algoritmo, [])
    
    def _obter_explicacao_metrica(self, metrica: str) -> str:
        """
        Obtém a explicação didática de uma métrica de comparação.
        
        Args:
            metrica: Nome da métrica
            
        Returns:
            str: Explicação didática
        """
        # Dicionário de explicações para métricas comuns
        explicacoes = {
            'isomorfismo': """
                <h3>Isomorfismo de Grafos</h3>
                <p>Dois grafos são isomorfos se existe uma correspondência biunívoca entre seus vértices e arestas 
                que preserva a estrutura de incidência. Em termos simples, grafos isomorfos são estruturalmente idênticos, 
                embora possam ser desenhados de maneiras diferentes.</p>
                
                <h4>Propriedades Preservadas</h4>
                <ul>
                    <li>Número de vértices</li>
                    <li>Número de arestas</li>
                    <li>Graus dos vértices</li>
                    <li>Ciclos e caminhos</li>
                    <li>Conectividade</li>
                </ul>
                
                <h4>Aplicações</h4>
                <p>O isomorfismo de grafos é utilizado em diversas áreas, como química (para identificar moléculas equivalentes), 
                redes sociais (para encontrar padrões de relacionamento) e segurança de computadores (para detectar padrões de ataque).</p>
            """,
            
            'similaridade_espectral': """
                <h3>Similaridade Espectral</h3>
                <p>A similaridade espectral é uma medida que compara os autovalores das matrizes de adjacência ou laplacianas 
                de dois grafos. Quanto mais próximos os espectros, mais similares são os grafos em termos de propriedades estruturais.</p>
                
                <h4>Cálculo</h4>
                <p>A similaridade espectral pode ser calculada de várias formas, como a distância euclidiana entre os autovalores 
                ordenados, a correlação entre os espectros, ou medidas mais sofisticadas que consideram também os autovetores.</p>
                
                <h4>Aplicações</h4>
                <p>A similaridade espectral é utilizada em reconhecimento de padrões, classificação de grafos, detecção de comunidades 
                em redes e comparação de estruturas moleculares.</p>
            """,
            
            'similaridade_estrutural': """
                <h3>Similaridade Estrutural</h3>
                <p>A similaridade estrutural mede o quanto dois grafos compartilham características estruturais comuns, 
                como distribuição de graus, coeficiente de agrupamento, diâmetro, etc.</p>
                
                <h4>Cálculo</h4>
                <p>Existem várias métricas para calcular a similaridade estrutural, como o coeficiente de Jaccard para conjuntos 
                de arestas, a distância de edição de grafos (número mínimo de operações para transformar um grafo em outro), 
                ou medidas baseadas em caminhadas aleatórias.</p>
                
                <h4>Aplicações</h4>
                <p>A similaridade estrutural é utilizada em bioinformática (comparação de redes de proteínas), análise de redes sociais 
                (identificação de comunidades similares) e aprendizado de máquina em grafos.</p>
            """,
            
            'subgrafo': """
                <h3>Verificação de Subgrafo</h3>
                <p>Um grafo H é subgrafo de um grafo G se todos os vértices e arestas de H estão presentes em G. 
                Em outras palavras, H pode ser obtido removendo-se alguns vértices e/ou arestas de G.</p>
                
                <h4>Tipos de Subgrafos</h4>
                <ul>
                    <li><strong>Subgrafo induzido</strong>: Obtido removendo-se apenas vértices (e todas as arestas incidentes a eles).</li>
                    <li><strong>Subgrafo gerador</strong>: Contém todos os vértices do grafo original, removendo-se apenas algumas arestas.</li>
                    <li><strong>Subgrafo isomorfo</strong>: Um subgrafo que é isomorfo a outro grafo dado.</li>
                </ul>
                
                <h4>Aplicações</h4>
                <p>A verificação de subgrafos é utilizada em mineração de dados em grafos, detecção de padrões em redes, 
                bioinformática (identificação de motivos em redes biológicas) e química (identificação de subestruturas moleculares).</p>
            """,
            
            # Adicione mais métricas conforme necessário
        }
        
        # Retorna a explicação da métrica ou uma mensagem padrão
        return explicacoes.get(metrica, f"<p>Explicação para a métrica {metrica} não disponível.</p>")
    
    def _datetime_format(self, value, format='%d/%m/%Y %H:%M'):
        """
        Formata um objeto datetime para string.
        
        Args:
            value: Valor datetime
            format: Formato de saída
            
        Returns:
            str: Data formatada
        """
        if isinstance(value, datetime):
            return value.strftime(format)
        return value
    
    def _criar_templates_padrao(self, template_dir: str):
        """
        Cria os templates HTML e CSS padrão no diretório especificado.
        
        Args:
            template_dir: Diretório onde os templates serão criados
        """
        # Template HTML padrão
        html_template = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ titulo }}</title>
</head>
<body>
    <header>
        <h1>{{ titulo }}</h1>
        <div class="metadados">
            <p>Autor: {{ metadados.autor }}</p>
            <p>Data: {{ metadados.data|datetime_format }}</p>
            {% if metadados.descricao %}
            <p>{{ metadados.descricao }}</p>
            {% endif %}
        </div>
    </header>
    
    <main>
        {% if grafos %}
        <section class="grafos">
            <h2>Grafos</h2>
            {% for grafo in grafos %}
            <div class="grafo">
                <h3>{{ grafo.nome }}</h3>
                <div class="grafo-info">
                    <p>Vértices: {{ grafo.num_vertices }}</p>
                    <p>Arestas: {{ grafo.num_arestas }}</p>
                    <p>Direcionado: {{ "Sim" if grafo.direcionado else "Não" }}</p>
                    <p>Ponderado: {{ "Sim" if grafo.ponderado else "Não" }}</p>
                </div>
                {% if grafo.imagem_base64 %}
                <div class="grafo-visualizacao">
                    <img src="data:image/png;base64,{{ grafo.imagem_base64 }}" alt="Visualização do grafo {{ grafo.nome }}">
                </div>
                {% endif %}
            </div>
            {% endfor %}
        </section>
        {% endif %}
        
        {% if algoritmos %}
        <section class="algoritmos">
            <h2>Algoritmos Aplicados</h2>
            {% for algoritmo in algoritmos %}
            <div class="algoritmo">
                <h3>{{ algoritmo.nome }}</h3>
                
                {% if config.incluir_teoria and algoritmo.teoria %}
                <div class="teoria">
                    {{ algoritmo.teoria|safe }}
                </div>
                {% endif %}
                
                <div class="parametros">
                    <h4>Parâmetros</h4>
                    <ul>
                    {% for param_nome, param_valor in algoritmo.parametros.items() %}
                        <li><strong>{{ param_nome }}</strong>: {{ param_valor }}</li>
                    {% endfor %}
                    </ul>
                </div>
                
                {% if config.incluir_passos and algoritmo.passos %}
                <div class="passos">
                    <h4>Passos de Execução</h4>
                    <ol>
                    {% for passo in algoritmo.passos %}
                        <li>
                            <p>{{ passo.descricao }}</p>
                            {% if passo.imagem_base64 %}
                            <img src="data:image/png;base64,{{ passo.imagem_base64 }}" alt="Passo {{ loop.index }}">
                            {% endif %}
                        </li>
                    {% endfor %}
                    </ol>
                </div>
                {% endif %}
                
                <div class="resultado">
                    <h4>Resultado</h4>
                    <div class="resultado-dados">
                        {{ algoritmo.resultado|pprint }}
                    </div>
                    {% if algoritmo.imagem_resultado_base64 %}
                    <div class="resultado-visualizacao">
                        <img src="data:image/png;base64,{{ algoritmo.imagem_resultado_base64 }}" alt="Resultado do algoritmo {{ algoritmo.nome }}">
                    </div>
                    {% endif %}
                </div>
                
                {% if config.incluir_referencias and algoritmo.referencias %}
                <div class="referencias">
                    <h4>Referências</h4>
                    <ul>
                    {% for referencia in algoritmo.referencias %}
                        <li>{{ referencia }}</li>
                    {% endfor %}
                    </ul>
                </div>
                {% endif %}
            </div>
            {% endfor %}
        </section>
        {% endif %}
        
        {% if operacoes %}
        <section class="operacoes">
            <h2>Operações Realizadas</h2>
            {% for operacao in operacoes %}
            <div class="operacao">
                <h3>{{ operacao.nome }}</h3>
                <p>{{ operacao.descricao }}</p>
                
                <div class="resultado">
                    <h4>Resultado</h4>
                    <div class="resultado-dados">
                        {{ operacao.resultado|pprint }}
                    </div>
                </div>
            </div>
            {% endfor %}
        </section>
        {% endif %}
        
        {% if metadados.tipo_relatorio == 'comparacao' %}
        <section class="comparacao">
            <h2>Comparação de Grafos</h2>
            <div class="metrica">
                <h3>Métrica: {{ metadados.metrica }}</h3>
                <div class="explicacao">
                    {{ metadados.explicacao|safe }}
                </div>
            </div>
        </section>
        {% endif %}
        
        {% if metadados.notas %}
        <section class="notas">
            <h2>Notas</h2>
            <ul>
            {% for nota in metadados.notas %}
                <li>{{ nota }}</li>
            {% endfor %}
            </ul>
        </section>
        {% endif %}
    </main>
    
    <footer>
        <p>Gerado automaticamente pela Plataforma de Estudo de Teoria dos Grafos</p>
        <p>{{ metadados.data|datetime_format('%d/%m/%Y %H:%M') }}</p>
    </footer>
</body>
</html>
"""
        
        # CSS padrão
        css_template = """/* Estilos gerais */
body {
    font-family: "Noto Sans CJK SC", "WenQuanYi Zen Hei", sans-serif;
    line-height: 1.6;
    color: #333;
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

h1, h2, h3, h4 {
    color: #2c3e50;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
}

h1 {
    text-align: center;
    font-size: 28px;
    border-bottom: 2px solid #3498db;
    padding-bottom: 10px;
}

h2 {
    font-size: 24px;
    border-bottom: 1px solid #bdc3c7;
    padding-bottom: 5px;
}

h3 {
    font-size: 20px;
    color: #2980b9;
}

h4 {
    font-size: 18px;
    color: #16a085;
}

p {
    margin: 0.8em 0;
}

/* Cabeçalho */
header {
    margin-bottom: 30px;
}

.metadados {
    background-color: #f8f9fa;
    padding: 10px 15px;
    border-radius: 5px;
    font-size: 14px;
    color: #555;
}

/* Seções */
section {
    margin-bottom: 40px;
}

/* Grafos */
.grafo {
    margin-bottom: 30px;
    padding: 15px;
    background-color: #f8f9fa;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.grafo-info {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 10px;
    margin: 15px 0;
}

.grafo-visualizacao {
    text-align: center;
    margin: 20px 0;
}

.grafo-visualizacao img {
    max-width: 100%;
    height: auto;
    border: 1px solid #ddd;
    border-radius: 5px;
}

/* Algoritmos */
.algoritmo {
    margin-bottom: 40px;
    padding: 20px;
    background-color: #f8f9fa;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.teoria {
    background-color: #e8f4f8;
    padding: 15px;
    border-radius: 5px;
    margin: 15px 0;
}

.parametros, .passos, .resultado, .referencias {
    margin: 20px 0;
}

.passos ol {
    padding-left: 20px;
}

.passos li {
    margin-bottom: 15px;
}

.passos img, .resultado-visualizacao img {
    max-width: 100%;
    height: auto;
    margin: 10px 0;
    border: 1px solid #ddd;
    border-radius: 5px;
}

.resultado-dados {
    background-color: #f0f0f0;
    padding: 15px;
    border-radius: 5px;
    font-family: monospace;
    white-space: pre-wrap;
    overflow-x: auto;
}

/* Operações */
.operacao {
    margin-bottom: 30px;
    padding: 15px;
    background-color: #f8f9fa;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

/* Comparação */
.comparacao .metrica {
    background-color: #e8f4f8;
    padding: 15px;
    border-radius: 5px;
    margin: 15px 0;
}

/* Notas */
.notas {
    background-color: #fffde7;
    padding: 15px;
    border-radius: 5px;
    margin: 20px 0;
}

/* Rodapé */
footer {
    margin-top: 50px;
    padding-top: 20px;
    border-top: 1px solid #eee;
    font-size: 14px;
    color: #777;
    text-align: center;
}

/* Responsividade */
@media (max-width: 768px) {
    body {
        padding: 10px;
    }
    
    .grafo-info {
        grid-template-columns: 1fr;
    }
}
"""
        
        # Cria os arquivos de template
        with open(os.path.join(template_dir, "relatorio_padrao.html"), "w") as f:
            f.write(html_template)
        
        with open(os.path.join(template_dir, "estilo_padrao.css"), "w") as f:
            f.write(css_template)
