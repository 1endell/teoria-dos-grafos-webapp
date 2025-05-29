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
import CustomNode from './CustomNode';
import CustomEdge from './CustomEdge';
import CustomConnectionLine from './CustomConnectionLine';

const initialNodes: Node[] = [];
const initialEdges: Edge[] = [];

const GraphEditorReactFlow: React.FC = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
  const [nodeCounter, setNodeCounter] = useState(0);

  const onConnect = useCallback(
    (params: Edge | Connection) => setEdges((eds) => addEdge({ ...params, type: 'custom' }, eds)),
    [setEdges]
  );

  const { getViewport } = useReactFlow();

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
    const viewport = getViewport();
    const newNode: Node = {
      id,
      data: { label },
      position: {
        x: viewport.x + window.innerWidth / 2 - 25,
        y: viewport.y + window.innerHeight / 2 - 25
      },
      type: 'custom'
    };
    setNodes((nds) => [...nds, newNode]);
    setNodeCounter((prev) => prev + 1);
  };

  return (
    <>
      <button onClick={handleAddNode} style={{ marginBottom: 10 }}>Adicionar Nó</button>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        fitView
        nodeTypes={{ custom: CustomNode }}
        edgeTypes={{ custom: CustomEdge }}
        defaultEdgeOptions={{ type: 'custom' }}
        connectionLineComponent={CustomConnectionLine}
        connectionLineStyle={{ stroke: '#000', strokeWidth: 2 }}
        connectionLineType="straight"
        panOnDrag
        zoomOnScroll
        nodeDraggable
      >
        <Background gap={16} size={1} color="#ccc" variant="dots" />
        <Controls />
      </ReactFlow>
    </>
  );
};

export default GraphEditorReactFlow;
