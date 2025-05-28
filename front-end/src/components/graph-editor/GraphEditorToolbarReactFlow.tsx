import React from 'react';
import { Button } from '@/components/ui/button';

interface GraphEditorToolbarReactFlowProps {
  onAddNode: () => void;
  onAddEdge: () => void;
  onResetView: () => void;
  onLayout: () => void;
  onSaveGraph: () => void;
}

const GraphEditorToolbarReactFlow: React.FC<GraphEditorToolbarReactFlowProps> = ({
  onAddNode,
  onAddEdge,
  onResetView,
  onLayout,
  onSaveGraph
}) => {
  return (
    <div className="flex space-x-2 p-2 bg-gray-100 border-b">
      <Button variant="default" onClick={onAddNode}>
        Adicionar Vértice
      </Button>
      <Button variant="default" onClick={onAddEdge}>
        Adicionar Aresta
      </Button>
      <Button variant="default" onClick={onLayout}>
        Layout Automático
      </Button>
      <Button variant="default" onClick={onResetView}>
        Resetar Visão
      </Button>
      <Button variant="default" onClick={onSaveGraph}>
        Salvar Grafo
      </Button>
    </div>
  );
};

export default GraphEditorToolbarReactFlow;
