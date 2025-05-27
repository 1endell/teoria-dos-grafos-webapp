export type EditorMode = 'select' | 'addNode' | 'addEdge' | 'pan';

export type NodeAttributes = Record<string, any>;

export type EdgeAttributes = Record<string, any>;

export interface NodeProperties {
  label: string;
  color: string;
}

export interface EdgeProperties {
  weight: number;
  color: string;
}

export interface GraphEditorState {
  mode: EditorMode;
  selectedNode: string | null;
  sourceNode: string | null;
  isDirected: boolean;
  isWeighted: boolean;
  nodeCounter: number;
  nodeProperties: NodeProperties;
  edgeProperties: EdgeProperties;
  isLoading: boolean;
  layoutType: string;
  grafoNome?: string; // Adicionado para permitir edição do nome do grafo
}

export interface GraphEditorProps {
  grafoId?: string;
  onSave?: (grafoId: string) => void;
}
