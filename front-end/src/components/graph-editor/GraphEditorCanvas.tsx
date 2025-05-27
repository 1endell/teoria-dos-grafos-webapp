import React, { useRef, useEffect } from 'react';
import { EditorMode } from './types';

interface GraphEditorCanvasProps {
  mode: EditorMode;
  sourceNode: string | null;
  isLoading: boolean;
  onContainerRef: (ref: React.RefObject<HTMLDivElement>) => void;
}

const GraphEditorCanvas: React.FC<GraphEditorCanvasProps> = ({
  mode,
  sourceNode,
  isLoading,
  onContainerRef
}) => {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    onContainerRef(containerRef);
  }, [onContainerRef]);

  return (
    <div
      ref={containerRef}
      className="flex-1 bg-gray-50 relative"
      style={{
        height: '100%',
        position: 'relative',
        backgroundImage: `
          linear-gradient(rgba(0,0,0,0.1) 1px, transparent 1px),
          linear-gradient(90deg, rgba(0,0,0,0.1) 1px, transparent 1px)
        `,
        backgroundSize: '20px 20px'
      }}
    >
      {isLoading && (
        <div className="absolute inset-0 bg-white/70 flex items-center justify-center z-10">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
      )}

      {mode === 'addNode' && (
        <div className="absolute top-4 left-4 bg-white p-2 rounded shadow-md z-10">
          <p className="text-sm font-medium">Clique no canvas para adicionar um vértice</p>
          <p className="text-xs text-gray-500">Modo atual: {mode}</p>
        </div>
      )}

      {mode === 'addEdge' && (
        <div className="absolute top-4 left-4 bg-white p-2 rounded shadow-md z-10">
          <p className="text-sm font-medium">
            {sourceNode
              ? `Selecione o vértice de destino (origem: ${sourceNode})`
              : 'Selecione o vértice de origem'}
          </p>
        </div>
      )}
    </div>
  );
};

export default GraphEditorCanvas;
