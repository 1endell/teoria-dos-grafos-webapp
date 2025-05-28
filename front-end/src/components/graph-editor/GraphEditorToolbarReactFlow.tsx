import React from 'react';
import { Button } from '@/components/ui/button';

interface GraphEditorToolbarReactFlowProps {
  onAddNode: () => void;
  onAddEdge: () => void;
  onLayout: () => void;
  onResetView: () => void;
  onSaveGraph: () => void;
}

const GraphEditorToolbarReactFlow: React.FC<GraphEditorToolbarReactFlowProps> = ({
  onAddNode,
  onAddEdge,
  onLayout,
  onResetView,
  onSaveGraph,
}) => {
  return (
    <div className="flex gap-2 p-2 bg-gray-100 border-b border-gray-300">
      <Button onClick={onAddNode} variant="default">Adicionar Vértice</Button>
      <Button onClick={onAddEdge} variant="outline">Adicionar Aresta</Button>
      <Button onClick={onLayout} variant="outline">Layout Automático</Button>
      <Button onClick={onResetView} variant="outline">Resetar Visão</Button>
      <Button onClick={onSaveGraph} variant="secondary">Salvar Grafo</Button>
    </div>
  );
};

export default GraphEditorToolbarReactFlow;
