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
  useReactFlow
} from 'reactflow';
import 'reactflow/dist/style.css';

const initialNodes: Node[] = [];
const initialEdges: Edge[] = [];

const GraphEditorReactFlow: React.FC = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
  const [nodeCounter, setNodeCounter] = useState(0);

  const onConnect = useCallback(
    (params: Edge | Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  const { fitView, getNodes, getEdges, setViewport } = useReactFlow();

  const generateLabel = (counter: number) => {
    let label = '';
    while (counter >= 0) {
      label = String.fromCharCode(97 + (counter % 26)) + label;
      counter = Math.floor(counter / 26) - 1;
    }
    return label;
  };

  const handleAddNode = () => {
    const id = `node-${+new Date()}`;
    const label = generateLabel(nodeCounter);
    const newNode: Node = {
      id,
      data: { label },
      position: { x: viewport.x + window.innerWidth / 2 - 25, y: viewport.y + window.innerHeight / 2 - 25 },
      type: 'default',
      style: {
        borderRadius: '50%',
        width: 50,
        height: 50,
        textAlign: 'center',
        lineHeight: '50px',
        background: '#4f46e5',
        color: 'white',
        border: '2px solid #1e40af'
      }
    };
    setNodes((nds) => [...nds, newNode]);
    setNodeCounter((prev) => prev + 1);
  };

  const handleAddEdge = () => {
    if (selectedNodeId) {
      const targetNode = nodes.find((n) => n.id !== selectedNodeId);
      if (targetNode) {
        const newEdge: Edge = {
          id: `e${selectedNodeId}-${targetNode.id}`,
          source: selectedNodeId,
          target: targetNode.id,
          type: 'default'
        };
        setEdges((eds) => [...eds, newEdge]);
      }
    }
  };

  const handleLayout = () => {
    setNodes((nds) =>
      nds.map((node) => ({
        ...node,
        position: { x: viewport.x + window.innerWidth / 2 - 25, y: viewport.y + window.innerHeight / 2 - 25 }
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
    <ReactFlowProvider connectionLineType="straight" connectionLineStyle={{ stroke: "#000", strokeWidth: 2 }} defaultEdgeOptions={{ type: "default", markerEnd: { type: "arrowclosed" } }} panOnDrag zoomOnScroll nodeDraggable fitView>
      <div style={{ width: '100%', height: '600px' }}>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          onNodeClick={(_, node) = connectionLineType="straight" connectionLineStyle={{ stroke: "#000", strokeWidth: 2 }} defaultEdgeOptions={{ type: "default", markerEnd: { type: "arrowclosed" } }} panOnDrag zoomOnScroll nodeDraggable fitView> setSelectedNodeId(node.id)}
          fitView
        >
          <Background />
          <Controls />
          <MiniMap />
        </ReactFlow>
      </div>

      {/* Barra de ferramentas personalizada */}
      <div className="mt-4 flex gap-2 justify-center">
        <button
          onClick={handleAddNode}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Adicionar Vértice
        </button>
        <button
          onClick={handleAddEdge}
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
        >
          Adicionar Aresta
        </button>
        <button
          onClick={handleLayout}
          className="bg-yellow-500 text-white px-4 py-2 rounded hover:bg-yellow-600"
        >
          Layout Aleatório
        </button>
        <button
          onClick={handleResetView}
          className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700"
        >
          Resetar Visão
        </button>
        <button
          onClick={handleSaveGraph}
          className="bg-teal-600 text-white px-4 py-2 rounded hover:bg-teal-700"
        >
          Salvar Grafo
        </button>
      </div>
    </ReactFlowProvider>
  );
};

export default GraphEditorReactFlow;
