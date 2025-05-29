import React, { useCallback, useState, useEffect } from 'react';
import {
  Background,
  ReactFlow,
  addEdge,
  useNodesState,
  useEdgesState,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';

import CustomNode from './components/graph-editor/CustomNode';
import CustomFloatingEdge from './components/graph-editor/CustomFloatingEdge';
import CustomConnectionLine from './components/graph-editor/CustomConnectionLine';

const initialNodes = [
  { id: '1', type: 'custom', position: { x: 100, y: 100 } },
  { id: '2', type: 'custom', position: { x: 300, y: 200 } },
  { id: '3', type: 'custom', position: { x: 200, y: 400 } },
  { id: '4', type: 'custom', position: { x: 500, y: 300 } },
];

const initialEdges = [];

const nodeTypes = { custom: CustomNode };
const edgeTypes = { floating: CustomFloatingEdge };

const connectionLineStyle = { stroke: '#000', strokeWidth: 2 };

const App = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [isCtrlPressed, setIsCtrlPressed] = useState(false);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Control') setIsCtrlPressed(true);
    };
    const handleKeyUp = (e) => {
      if (e.key === 'Control') setIsCtrlPressed(false);
    };
    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
    };
  }, []);

  const onConnect = useCallback(
    (params) => {
      if (isCtrlPressed) {
        setEdges((eds) => addEdge({ ...params, type: 'floating' }, eds));
      }
    },
    [setEdges, isCtrlPressed]
  );

  return (
    <div style={{ display: 'flex', width: '100vw', height: '100vh' }}>
      <div style={{ flexGrow: 1, position: 'relative' }}>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          fitView
          nodeTypes={nodeTypes}
          edgeTypes={edgeTypes}
          connectionLineComponent={CustomConnectionLine}
          connectionLineStyle={connectionLineStyle}
          style={{ width: '100%', height: '100%' }}
        >
          <Background />
        </ReactFlow>

        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          style={{
            position: 'absolute',
            top: 10,
            right: sidebarOpen ? 210 : 10,
            zIndex: 10,
            padding: '5px 10px',
            cursor: 'pointer',
          }}
        >
          {sidebarOpen ? 'Fechar' : 'Abrir'}
        </button>
      </div>

      {sidebarOpen && (
        <div
          style={{
            width: 200,
            background: '#f5f5f5',
            borderLeft: '1px solid #ccc',
            padding: 10,
            boxSizing: 'border-box',
          }}
        >
          <h3>Ferramentas</h3>
          <button style={{ display: 'block', marginBottom: 10 }}>Adicionar Vértice</button>
          <button style={{ display: 'block', marginBottom: 10 }}>Adicionar Aresta</button>
          <button style={{ display: 'block' }}>Remover Seleção</button>
        </div>
      )}
    </div>
  );
};

export default App;
