import React, { useState, useCallback } from 'react';
import {
  Background,
  ReactFlow,
  useNodesState,
  useEdgesState,
  addEdge,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';

import CustomNode from './components/graph-editor/CustomNode';
import CustomFloatingEdge from './components/graph-editor/CustomFloatingEdge';
import CustomConnectionLine from './components/graph-editor/CustomConnectionLine';

const initialNodes = [
  { id: '1', type: 'custom', position: { x: 100, y: 100 } },
  { id: '2', type: 'custom', position: { x: 300, y: 200 } },
];
const initialEdges = [];

const nodeTypes = { custom: CustomNode };
const edgeTypes = { floating: CustomFloatingEdge };
const connectionLineStyle = { stroke: '#000', strokeWidth: 2 };

const App = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [mode, setMode] = useState('move'); // 'move', 'addNode', 'addEdge'
  const [selectedSource, setSelectedSource] = useState(null);

  const onPaneClick = useCallback(
    (event) => {
      if (mode === 'addNode') {
        const newNode = {
          id: `${+new Date()}`,
          type: 'custom',
          position: { x: event.clientX - 100, y: event.clientY - 40 },
          data: { mode },
        };
        setNodes((nds) => [...nds, newNode]);
      }
      setSelectedSource(null); // Reset ao clicar fora
    },
    [mode, setNodes]
  );

  const onNodeClick = useCallback(
    (event, node) => {
      if (mode === 'addEdge') {
        if (!selectedSource) {
          setSelectedSource(node.id); // Definir como origem
        } else if (selectedSource !== node.id) {
          setEdges((eds) =>
            addEdge({ source: selectedSource, target: node.id, type: 'floating' }, eds)
          );
          setSelectedSource(null); // Reset após conexão
        }
      }
    },
    [mode, selectedSource, setEdges]
  );

  const displayedNodes = nodes.map((node) => ({
    ...node,
    data: { ...node.data, mode },
  }));

  return (
    <div style={{ display: 'flex', width: '100vw', height: '100vh' }}>
      <div style={{ flexGrow: 1, position: 'relative' }}>
        <ReactFlow
          nodes={displayedNodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onNodeClick={onNodeClick}
          fitView
          nodeTypes={nodeTypes}
          edgeTypes={edgeTypes}
          connectionLineComponent={CustomConnectionLine}
          connectionLineStyle={connectionLineStyle}
          style={{ width: '100%', height: '100%' }}
          connectionMode="invalid" // Desativa conexões automáticas
          onPaneClick={onPaneClick}
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
          <button onClick={() => setMode('move')} style={{ display: 'block', marginBottom: 10 }}>
            Mover Vértice
          </button>
          <button onClick={() => setMode('addNode')} style={{ display: 'block', marginBottom: 10 }}>
            Adicionar Vértice
          </button>
          <button onClick={() => setMode('addEdge')} style={{ display: 'block' }}>
            Adicionar Aresta
          </button>
          <p style={{ marginTop: 10 }}>Modo atual: {mode}</p>
        </div>
      )}
    </div>
  );
};

export default App;
