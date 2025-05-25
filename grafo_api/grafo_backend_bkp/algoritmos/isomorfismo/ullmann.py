"""
Implementação do algoritmo de Ullmann para isomorfismo de subgrafos.

O algoritmo de Ullmann determina se um grafo é isomorfo a um subgrafo de outro grafo,
ou seja, se existe uma correspondência um-para-um entre os vértices de um grafo e
um subconjunto de vértices do outro grafo que preserva as adjacências.
"""

from typing import Dict, List, Any, Tuple, Set, Optional
import numpy as np
import networkx as nx
from core.grafo import Grafo


def ullmann(grafo_pequeno: Grafo, grafo_grande: Grafo) -> Optional[Dict[Any, Any]]:
    """
    Implementa o algoritmo de Ullmann para isomorfismo de subgrafos.
    
    Args:
        grafo_pequeno: Grafo menor que será procurado como subgrafo.
        grafo_grande: Grafo maior onde será procurado o subgrafo.
        
    Returns:
        Optional[Dict[Any, Any]]: Dicionário mapeando vértices do grafo pequeno para
            vértices correspondentes no grafo grande, ou None se não existir isomorfismo.
    """
    # Obtém os grafos NetworkX subjacentes
    g_pequeno = grafo_pequeno.obter_grafo_networkx()
    g_grande = grafo_grande.obter_grafo_networkx()
    
    # Obtém os vértices dos grafos
    vertices_pequeno = list(grafo_pequeno.obter_vertices())
    vertices_grande = list(grafo_grande.obter_vertices())
    
    # Verifica se o grafo pequeno tem mais vértices que o grande
    if len(vertices_pequeno) > len(vertices_grande):
        return None
    
    # Cria as matrizes de adjacência
    matriz_pequeno = nx.to_numpy_array(g_pequeno, nodelist=vertices_pequeno)
    matriz_grande = nx.to_numpy_array(g_grande, nodelist=vertices_grande)
    
    # Inicializa a matriz de mapeamento M
    # M[i, j] = 1 se o vértice i do grafo pequeno pode ser mapeado para o vértice j do grafo grande
    M = np.zeros((len(vertices_pequeno), len(vertices_grande)), dtype=int)
    
    # Inicializa M com base nos graus dos vértices
    for i, v_pequeno in enumerate(vertices_pequeno):
        grau_v = g_pequeno.degree(v_pequeno)
        
        for j, v_grande in enumerate(vertices_grande):
            grau_u = g_grande.degree(v_grande)
            
            # Um vértice do grafo pequeno só pode ser mapeado para um vértice do grafo grande
            # se o grau do vértice no grafo grande for maior ou igual ao grau no grafo pequeno
            if grau_u >= grau_v:
                M[i, j] = 1
    
    # Função para refinar a matriz M
    def refinar_M(M: np.ndarray) -> np.ndarray:
        M_refinada = M.copy()
        
        for i in range(len(vertices_pequeno)):
            for j in range(len(vertices_grande)):
                if M[i, j] == 1:
                    # Verifica se a adjacência é preservada
                    for k in range(len(vertices_pequeno)):
                        if matriz_pequeno[i, k] == 1:
                            # Se o vértice k do grafo pequeno é adjacente ao vértice i,
                            # então deve existir pelo menos um vértice l do grafo grande
                            # que é adjacente ao vértice j e que pode ser mapeado para k
                            adjacencia_preservada = False
                            
                            for l in range(len(vertices_grande)):
                                if matriz_grande[j, l] == 1 and M[k, l] == 1:
                                    adjacencia_preservada = True
                                    break
                            
                            if not adjacencia_preservada:
                                M_refinada[i, j] = 0
                                break
        
        return M_refinada
    
    # Refina a matriz M até convergir
    while True:
        M_nova = refinar_M(M)
        
        if np.array_equal(M, M_nova):
            break
        
        M = M_nova
    
    # Verifica se ainda existe possibilidade de isomorfismo
    if not np.any(M):
        return None
    
    # Função para verificar se uma matriz de mapeamento é válida
    def verificar_mapeamento(F: np.ndarray) -> bool:
        # Verifica se F é uma matriz de permutação (uma linha, uma coluna)
        if not (np.sum(F, axis=0) <= 1).all() or not (np.sum(F, axis=1) == 1).all():
            return False
        
        # Verifica se o mapeamento preserva as adjacências
        S = F @ matriz_grande @ F.T
        
        # S[i, j] > 0 se existe uma aresta entre os vértices mapeados para i e j
        # matriz_pequeno[i, j] == 1 se existe uma aresta entre i e j no grafo pequeno
        # Para ser um isomorfismo, se matriz_pequeno[i, j] == 1, então S[i, j] > 0
        for i in range(len(vertices_pequeno)):
            for j in range(len(vertices_pequeno)):
                if matriz_pequeno[i, j] == 1 and S[i, j] == 0:
                    return False
        
        return True
    
    # Função recursiva para encontrar um mapeamento válido
    def backtrack(F: np.ndarray, nivel: int) -> Optional[np.ndarray]:
        if nivel == len(vertices_pequeno):
            # Verifica se o mapeamento é válido
            if verificar_mapeamento(F):
                return F
            return None
        
        # Tenta mapear o vértice 'nivel' do grafo pequeno para cada vértice do grafo grande
        for j in range(len(vertices_grande)):
            if M[nivel, j] == 1:
                # Verifica se o vértice j do grafo grande já foi mapeado
                if np.sum(F[:nivel, j]) == 0:
                    # Cria uma cópia da matriz F
                    F_nova = F.copy()
                    F_nova[nivel, j] = 1
                    
                    # Continua a busca
                    resultado = backtrack(F_nova, nivel + 1)
                    
                    if resultado is not None:
                        return resultado
        
        return None
    
    # Inicializa a matriz F (mapeamento final)
    F = np.zeros((len(vertices_pequeno), len(vertices_grande)), dtype=int)
    
    # Encontra um mapeamento válido
    F_final = backtrack(F, 0)
    
    if F_final is None:
        return None
    
    # Converte a matriz F para um dicionário de mapeamento
    mapeamento = {}
    
    for i in range(len(vertices_pequeno)):
        for j in range(len(vertices_grande)):
            if F_final[i, j] == 1:
                mapeamento[vertices_pequeno[i]] = vertices_grande[j]
                break
    
    return mapeamento


def encontrar_todos_subgrafos_isomorfos(grafo_padrao: Grafo, grafo_alvo: Grafo) -> List[Dict[Any, Any]]:
    """
    Encontra todos os subgrafos do grafo alvo que são isomorfos ao grafo padrão.
    
    Args:
        grafo_padrao: Grafo padrão a ser procurado.
        grafo_alvo: Grafo onde serão procurados os subgrafos.
        
    Returns:
        List[Dict[Any, Any]]: Lista de dicionários, onde cada dicionário mapeia vértices
            do grafo padrão para vértices correspondentes no grafo alvo.
    """
    # Obtém os grafos NetworkX subjacentes
    g_padrao = grafo_padrao.obter_grafo_networkx()
    g_alvo = grafo_alvo.obter_grafo_networkx()
    
    # Obtém os vértices dos grafos
    vertices_padrao = list(grafo_padrao.obter_vertices())
    vertices_alvo = list(grafo_alvo.obter_vertices())
    
    # Verifica se o grafo padrão tem mais vértices que o alvo
    if len(vertices_padrao) > len(vertices_alvo):
        return []
    
    # Lista para armazenar os mapeamentos encontrados
    mapeamentos = []
    
    # Função para verificar se um mapeamento já foi encontrado
    def mapeamento_ja_encontrado(mapeamento: Dict[Any, Any]) -> bool:
        for m in mapeamentos:
            if set(m.items()) == set(mapeamento.items()):
                return True
        return False
    
    # Para cada subconjunto de vértices do grafo alvo com o mesmo tamanho do grafo padrão
    for vertices_subgrafo in nx.utils.powerlaw_sequence(len(vertices_alvo), len(vertices_padrao)):
        # Cria um subgrafo induzido pelos vértices selecionados
        subgrafo = grafo_alvo.obter_subgrafo([vertices_alvo[i] for i in vertices_subgrafo])
        
        # Verifica se o subgrafo é isomorfo ao grafo padrão
        mapeamento = ullmann(grafo_padrao, subgrafo)
        
        if mapeamento is not None and not mapeamento_ja_encontrado(mapeamento):
            # Converte o mapeamento para o grafo alvo original
            mapeamento_original = {v: vertices_alvo[vertices_subgrafo.index(mapeamento[v])] for v in mapeamento}
            mapeamentos.append(mapeamento_original)
    
    return mapeamentos


def verificar_isomorfismo_subgrafo(grafo_pequeno: Grafo, grafo_grande: Grafo, mapeamento: Dict[Any, Any]) -> bool:
    """
    Verifica se um mapeamento representa um isomorfismo de subgrafo válido.
    
    Args:
        grafo_pequeno: Grafo menor que será verificado como subgrafo.
        grafo_grande: Grafo maior onde será verificado o subgrafo.
        mapeamento: Dicionário mapeando vértices do grafo pequeno para vértices do grafo grande.
        
    Returns:
        bool: True se o mapeamento representa um isomorfismo de subgrafo válido, False caso contrário.
    """
    # Verifica se todos os vértices do grafo pequeno estão no mapeamento
    if set(grafo_pequeno.obter_vertices()) != set(mapeamento.keys()):
        return False
    
    # Verifica se o mapeamento preserva as adjacências
    for u, v in grafo_pequeno.obter_grafo_networkx().edges():
        u_mapeado = mapeamento[u]
        v_mapeado = mapeamento[v]
        
        if not grafo_grande.existe_aresta(u_mapeado, v_mapeado):
            return False
    
    return True


def visualizar_isomorfismo_subgrafo(grafo_pequeno: Grafo, grafo_grande: Grafo, mapeamento: Dict[Any, Any], arquivo: str = None) -> None:
    """
    Visualiza um isomorfismo de subgrafo.
    
    Args:
        grafo_pequeno: Grafo menor que é isomorfo a um subgrafo do grafo grande.
        grafo_grande: Grafo maior que contém um subgrafo isomorfo ao grafo pequeno.
        mapeamento: Dicionário mapeando vértices do grafo pequeno para vértices do grafo grande.
        arquivo: Caminho para salvar a imagem (opcional).
    """
    import matplotlib.pyplot as plt
    import networkx as nx
    
    # Cria grafos NetworkX para visualização
    g_pequeno = grafo_pequeno.obter_grafo_networkx()
    g_grande = grafo_grande.obter_grafo_networkx()
    
    # Define as posições dos vértices
    pos_pequeno = nx.spring_layout(g_pequeno)
    pos_grande = nx.spring_layout(g_grande)
    
    # Cria a figura com dois subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
    
    # Desenha o grafo pequeno
    nx.draw_networkx_nodes(g_pequeno, pos_pequeno, ax=ax1, node_color='lightblue', node_size=500)
    nx.draw_networkx_edges(g_pequeno, pos_pequeno, ax=ax1, width=1.5)
    nx.draw_networkx_labels(g_pequeno, pos_pequeno, ax=ax1)
    
    ax1.set_title("Grafo Padrão")
    ax1.axis('off')
    
    # Desenha o grafo grande
    nx.draw_networkx_nodes(g_grande, pos_grande, ax=ax2, node_color='lightgray', node_size=500)
    nx.draw_networkx_edges(g_grande, pos_grande, ax=ax2, width=1, alpha=0.5)
    
    # Destaca o subgrafo isomorfo
    vertices_mapeados = list(mapeamento.values())
    nx.draw_networkx_nodes(g_grande, pos_grande, ax=ax2, nodelist=vertices_mapeados, node_color='lightblue', node_size=700)
    
    # Destaca as arestas do subgrafo isomorfo
    arestas_mapeadas = []
    for u, v in g_pequeno.obter_grafo_networkx().edges():
        u_mapeado = mapeamento[u]
        v_mapeado = mapeamento[v]
        arestas_mapeadas.append((u_mapeado, v_mapeado))
    
    nx.draw_networkx_edges(g_grande, pos_grande, ax=ax2, edgelist=arestas_mapeadas, width=2, edge_color='blue')
    
    # Adiciona rótulos aos vértices
    nx.draw_networkx_labels(g_grande, pos_grande, ax=ax2)
    
    # Adiciona o mapeamento como texto
    mapeamento_texto = "\n".join([f"{u} → {v}" for u, v in mapeamento.items()])
    ax2.text(0.05, 0.05, f"Mapeamento:\n{mapeamento_texto}", transform=ax2.transAxes, fontsize=10,
             verticalalignment='bottom', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    ax2.set_title("Grafo Alvo com Subgrafo Isomorfo Destacado")
    ax2.axis('off')
    
    plt.tight_layout()
    
    # Salva a imagem ou mostra na tela
    if arquivo:
        plt.savefig(arquivo)
    else:
        plt.show()
