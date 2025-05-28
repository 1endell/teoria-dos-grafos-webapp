import React, { useCallback, useState } from 'react';
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
  useReactFlow,
} from 'reactflow';
import 'reactflow/dist/style.css';
import GraphEditorToolbarReactFlow from './GraphEditorToolbarReactFlow';

const initialNodes: Node[] = [];

const initialEdges: Edge[] = [];

const GraphEditorReactFlow: React.FC = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
  const { fitView, getNodes, getEdges } = useReactFlow();

  const onConnect = useCallback(
    (params: Edge | Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  const handleAddNode = () => {
    const id = `node-${Date.now()}`;
    const newNode: Node = {
      id,
      data: { label: `Vértice ${nodes.length + 1}` },
      position: { x: Math.random() * 400, y: Math.random() * 400 },
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
      }
    }
  };

  const handleLayout = () => {
    setNodes((nds) =>
      nds.map((node) => ({
        ...node,
        position: { x: Math.random() * 400, y: Math.random() * 400 },
      }))
    );
    setEdges((eds) => [...eds]);
  };

  const handleResetView = () => {
    fitView();
  };

  const handleSaveGraph = () => {
    const data = { nodes: getNodes(), edges: getEdges() };
    console.log('Grafo salvo:', data);
    alert('Grafo salvo no console!');
  };

  return (
    <ReactFlowProvider>
      <div style={{ width: '100%', height: '600px' }}>
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
          <Controls />
          <MiniMap />
        </ReactFlow>
      </div>

      <div className="mt-2">
        <GraphEditorToolbarReactFlow
          onAddNode={handleAddNode}
          onAddEdge={handleAddEdge}
          onLayout={handleLayout}
          onResetView={handleResetView}
          onSaveGraph={handleSaveGraph}
        />
      </div>
    </ReactFlowProvider>
  );
};

export default GraphEditorReactFlow;
