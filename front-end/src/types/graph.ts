
export interface Vertice {
  id: string;
  atributos?: Record<string, any>;
  grau?: number;
}

export interface VerticeCreate {
  id: string;
  atributos?: Record<string, any>;
  conjunto?: string | null;
}

export interface Aresta {
  origem: string;
  destino: string;
  peso?: number;
  atributos?: Record<string, any>;
}

export interface ArestaCreate {
  origem: string;
  destino: string;
  peso?: number;
  atributos?: Record<string, any>;
}

export interface GrafoInfo {
  id: string;
  nome: string;
  direcionado: boolean;
  ponderado: boolean;
  bipartido: boolean;
  num_vertices: number;
  num_arestas: number;
  data_criacao: string;
  data_atualizacao?: string | null;
}

export interface Grafo extends GrafoInfo {
  vertices: Vertice[];
  arestas: Aresta[];
}

export interface GrafoCreate {
  nome: string;
  direcionado?: boolean;
  ponderado?: boolean;
  bipartido?: boolean;
  vertices?: VerticeCreate[];
  arestas?: ArestaCreate[];
}

export interface DadosVisualizacao {
  vertices: Array<{
    id: string;
    x: number;
    y: number;
    [key: string]: any;
  }>;
  arestas: Array<{
    origem: string;
    destino: string;
    [key: string]: any;
  }>;
  layout: string;
}

export interface ResultadoAlgoritmo {
  algoritmo: string;
  grafo_id: string;
  resultado: Record<string, any>;
  tempo_execucao: number;
}
