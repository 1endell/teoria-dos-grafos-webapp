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
  const [nodeCounter, setNodeCounter] = useState(0);
  const [mode, setMode] = useState<'move' | 'addEdge'>('move');
  const [selectedSource, setSelectedSource] = useState<string | null>(null);

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

  const onNodeClick = useCallback((_, node) => {
    if (mode === 'addEdge') {
      if (!selectedSource) {
        setSelectedSource(node.id); // Primeiro clique define origem
      } else if (selectedSource !== node.id) {
        // Segundo clique cria a aresta
        setEdges((eds) =>
          addEdge({ source: selectedSource, target: node.id, type: 'custom' }, eds)
        );
        setSelectedSource(null);
      }
    }
  }, [mode, selectedSource, setEdges]);

  return (
    <>
      <div style={{ marginBottom: 10 }}>
        <button onClick={handleAddNode} style={{ marginRight: 10 }}>Adicionar Nó</button>
        <button onClick={() => setMode('move')} style={{ marginRight: 10 }}>Modo Mover</button>
        <button onClick={() => setMode('addEdge')}>Modo Adicionar Aresta</button>
        <span style={{ marginLeft: 10 }}>Modo Atual: {mode}</span>
      </div>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={() => {}} // Desativar onConnect padrão
        fitView
        nodeTypes={{ custom: CustomNode }}
        edgeTypes={{ custom: CustomEdge }}
        defaultEdgeOptions={{ type: 'custom' }}
        connectionLineComponent={CustomConnectionLine}
        connectionLineStyle={{ stroke: '#000', strokeWidth: 2 }}
        connectionLineType="straight"
        panOnDrag
        zoomOnScroll
        nodeDraggable={mode === 'move'} // Só permite mover no modo "move"
        onNodeClick={onNodeClick} // Clique para criar aresta
      >
        <Background gap={16} size={1} color="#ccc" variant="dots" />
        <Controls />
      </ReactFlow>
    </>
  );
};

export default GraphEditorReactFlow;
