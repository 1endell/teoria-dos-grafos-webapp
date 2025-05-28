import React, { useCallback, useState, useRef } from 'react';
import ReactFlow, {
  Background,
  Controls,
  addEdge,
  MiniMap,
  useNodesState,
  useEdgesState,
  Connection,
  Edge,
  Node,
  ReactFlowProvider,
  useReactFlow
} from 'reactflow';
import 'reactflow/dist/style.css';
import { Button } from '@/components/ui/button';
import { useToast } from '@/hooks/use-toast';

const GraphEditorReactFlow: React.FC = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState<Node[]>([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState<Edge[]>([]);
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
  const { toast } = useToast();

  const { fitView, getNodes, getEdges, setViewport } = useReactFlow();
  const reactFlowWrapper = useRef<HTMLDivElement>(null);

  const onConnect = useCallback(
    (params: Edge | Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  const handleAddNode = () => {
    const id = `node-${Date.now()}`;
    const newNode: Node = {
      id,
      data: { label: `Vértice ${nodes.length + 1}` },
      position: { x: Math.random() * 600, y: Math.random() * 400 },
      type: 'default',
    };
    setNodes((nds) => [...nds, newNode]);
  };

  const handleAddEdge = () => {
    if (selectedNodeId) {
      const targetNode = nodes.find((n) => n.id !== selectedNodeId);
      if (targetNode) {
        const newEdge: Edge = {
          id: `e${selectedNodeId}-${targetNode.id}`,
          source: selectedNodeId,
          target: targetNode.id,
          type: 'default',
        };
        setEdges((eds) => [...eds, newEdge]);
        setSelectedNodeId(null);
      } else {
        toast({ title: "Erro", description: "Nenhum outro vértice disponível para conectar.", variant: "destructive" });
      }
    } else {
      toast({ title: "Aviso", description: "Selecione um vértice primeiro.", variant: "default" });
    }
  };

  const handleLayout = () => {
    setNodes((nds) =>
      nds.map((node) => ({
        ...node,
        position: { x: Math.random() * 600, y: Math.random() * 400 },
      }))
    );
    setEdges((eds) => [...eds]); // Forçar refresh
  };

  const handleResetView = () => {
    fitView();
  };

  const handleSaveGraph = () => {
    const data = { nodes: getNodes(), edges: getEdges() };
    console.log('Grafo salvo:', data);
    toast({ title: "Sucesso", description: "Grafo salvo no console!", variant: "success" });
  };

  return (
    <ReactFlowProvider>
      <div className="w-full h-full flex flex-col">
        {/* Canvas React Flow */}
        <div className="flex-1" ref={reactFlowWrapper}>
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            onNodeClick={(_, node) => setSelectedNodeId(node.id)}
            fitView
          >
            <Background />
            <MiniMap />
            <Controls />
          </ReactFlow>
        </div>

        {/* Toolbar Interna */}
        <div className="flex gap-2 p-2 border-t bg-white shadow-sm">
          <Button onClick={handleAddNode}>Adicionar Vértice</Button>
          <Button onClick={handleAddEdge} disabled={!selectedNodeId}>Criar Aresta</Button>
          <Button onClick={handleLayout}>Aplicar Layout</Button>
          <Button onClick={handleResetView}>Resetar Visão</Button>
          <Button onClick={handleSaveGraph}>Salvar Grafo</Button>
        </div>
      </div>
    </ReactFlowProvider>
  );
};

export default GraphEditorReactFlow;
