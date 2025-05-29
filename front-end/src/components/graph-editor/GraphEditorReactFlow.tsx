import React, { useCallback, useState } from 'react';
import ReactFlow, {
  Background,
  Controls,
  addEdge,
  useNodesState,
  useEdgesState,
  Node,
  Edge,
  useReactFlow,
  ReactFlowProvider // Importar o Provider
} from '@xyflow/react';
import 'reactflow/dist/style.css';

import CustomNode from './CustomNode';
import CustomEdge from './CustomEdge';
import CustomConnectionLine from './CustomConnectionLine';

const initialNodes: Node[] = [];
const initialEdges: Edge[] = [];

const GraphEditorReactFlow: React.FC = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [nodeCounter, setNodeCounter] = useState(0);

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

  const onConnect = useCallback(
    (params: Edge) => setEdges((eds) => addEdge({ ...params, type: 'custom' }, eds)),
    [setEdges]
  );

  return (
    <ReactFlowProvider>
      <div style={{ marginBottom: 10 }}>
        <button onClick={handleAddNode}>Adicionar Nó</button>
      </div>
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
      >
        <Background gap={16} size={1} color="#ccc" variant="dots" />
        <Controls />
      </ReactFlow>
    </ReactFlowProvider>
  );
};

export default GraphEditorReactFlow;
