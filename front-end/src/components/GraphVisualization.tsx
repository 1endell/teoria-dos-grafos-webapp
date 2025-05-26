
import React, { useEffect, useState, useCallback } from 'react';
import {
  ReactFlow,
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  Node,
  Edge,
  Position,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { graphService } from '@/services/graphService';
import { DadosVisualizacao } from '@/types/graph';
import { Button } from '@/components/ui/button';
import { ArrowLeft, RefreshCw } from 'lucide-react';

interface GraphVisualizationProps {
  grafoId: string;
  onBack: () => void;
}

const GraphVisualization: React.FC<GraphVisualizationProps> = ({ grafoId, onBack }) => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadVisualization = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      const visualizationData: DadosVisualizacao = await graphService.obterVisualizacao(grafoId);
      
      // Convert API data to React Flow nodes
      const flowNodes: Node[] = visualizationData.vertices.map((vertex) => ({
        id: vertex.id,
        type: 'default',
        position: { x: vertex.x * 200, y: vertex.y * 200 },
        data: { label: vertex.id },
        style: {
          background: '#6366f1',
          color: 'white',
          border: '2px solid #4f46e5',
          borderRadius: '8px',
          fontSize: '12px',
          fontWeight: 'bold',
        },
        sourcePosition: Position.Right,
        targetPosition: Position.Left,
      }));

      // Convert API data to React Flow edges
      const flowEdges: Edge[] = visualizationData.arestas.map((aresta, index) => ({
        id: `edge-${index}`,
        source: aresta.origem,
        target: aresta.destino,
        type: 'smoothstep',
        style: { stroke: '#6366f1', strokeWidth: 2 },
        animated: false,
      }));

      setNodes(flowNodes);
      setEdges(flowEdges);
    } catch (err) {
      console.error('Error loading visualization:', err);
      setError('Erro ao carregar a visualização do grafo');
    } finally {
      setLoading(false);
    }
  }, [grafoId, setNodes, setEdges]);

  useEffect(() => {
    loadVisualization();
  }, [loadVisualization]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center h-96 space-y-4">
        <p className="text-red-600">{error}</p>
        <Button onClick={loadVisualization} variant="outline">
          <RefreshCw className="mr-2 h-4 w-4" />
          Tentar novamente
        </Button>
      </div>
    );
  }

  return (
    <div className="h-full w-full">
      <div className="mb-4 flex items-center gap-4">
        <Button onClick={onBack} variant="outline">
          <ArrowLeft className="mr-2 h-4 w-4" />
          Voltar
        </Button>
        <Button onClick={loadVisualization} variant="outline">
          <RefreshCw className="mr-2 h-4 w-4" />
          Atualizar
        </Button>
      </div>
      
      <div className="h-96 w-full border border-gray-300 rounded-lg overflow-hidden">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          fitView
          attributionPosition="bottom-right"
          className="bg-gray-50"
        >
          <MiniMap />
          <Controls />
          <Background gap={12} size={1} />
        </ReactFlow>
      </div>
    </div>
  );
};

export default GraphVisualization;
