import React, { useState, useCallback, useRef } from 'react';
import { SidebarProvider } from '@/components/ui/sidebar';
import GraphPlatformSidebar from './graph-editor/GraphPlatformSidebar';
import { Input } from '@/components/ui/input';
import { useToast } from '@/hooks/use-toast';
import ReactFlow, {
  MiniMap, Controls, Background,
  addEdge, useNodesState, useEdgesState, Connection, Edge, Node
} from 'reactflow';
import 'reactflow/dist/style.css';
import dagre from 'dagre';
import CustomCircleNode from './graph-editor/CustomCircleNode';
import CustomEdge from './graph-editor/CustomEdge';

const edgeTypes = {
  custom: CustomEdge
};

const nodeTypes = {
  customCircle: CustomCircleNode
};

const onConnect = useCallback((params: Edge | Connection) => {
  setEdges((eds) => addEdge({ ...params, type: 'custom', data: { color: '#f43f5e', width: 3, dashed: false, label: 'Ligação' } }, eds));
}, [setEdges]);

const GraphMainEditor: React.FC = () => {
  const [isEditingTitle, setIsEditingTitle] = useState(false);
  const { toast } = useToast();
  const [graphName, setGraphName] = useState('Novo Grafo');
  const [nodeCounter, setNodeCounter] = useState(0);

  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const reactFlowWrapper = useRef<HTMLDivElement>(null);
  const [reactFlowInstance, setReactFlowInstance] = useState<any>(null);
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);

  const onConnect = useCallback(
    (params: Edge | Connection) =>
      setEdges((eds) =>
        addEdge(
          { ...params, type: 'custom', data: { color: '#f43f5e', width: 3, dashed: false, label: 'Aresta' } },
          eds
        )
      ),
    [setEdges]
  );

  const generateLabel = (counter: number) => {
    let label = '';
    while (counter >= 0) {
      label = String.fromCharCode(97 + (counter % 26)) + label;
      counter = Math.floor(counter / 26) - 1;
    }
    return label;
  };

  const handleAddNode = () => {
    const id = `${+new Date()}`;
    const label = generateLabel(nodeCounter);
    const newNode: Node = {
      id,
      position: { x: Math.random() * 400, y: Math.random() * 400 },
      data: { label },
      type: 'customCircle',
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
    setNodes((nds) => nds.concat(newNode));
    setNodeCounter((prev) => prev + 1);
  };

  const handleAddEdge = () => {
    toast({
      title: "Modo Aresta",
      description: "Conecte dois nós para criar uma aresta.",
      variant: "default",
    });
  };

  const handleLayout = () => {
    const g = new dagre.graphlib.Graph();
    g.setGraph({ rankdir: 'LR' });
    g.setDefaultEdgeLabel(() => ({}));

    nodes.forEach(node => {
      g.setNode(node.id, { width: 100, height: 100 });
    });

    edges.forEach(edge => {
      g.setEdge(edge.source, edge.target);
    });

    dagre.layout(g);

    const updatedNodes = nodes.map(node => {
      const pos = g.node(node.id);
      return {
        ...node,
        position: { x: pos.x - 50, y: pos.y - 50 } // Ajuste para centralizar
      };
    });

    setNodes(updatedNodes);
    toast({
      title: "Layout automático aplicado",
      description: "Os nós foram organizados automaticamente.",
      variant: "success",
    });
  };

  const handleResetView = () => {
    reactFlowInstance?.fitView();
  };

  const handleSaveGraph = () => {
    const graphData = {
      nodes,
      edges,
      name: graphName
    };
    console.log("Graph Saved:", graphData);
    toast({
      title: "Grafo salvo",
      description: "Os dados do grafo foram salvos no console.",
      variant: "success",
    });
  };

  const handleTitleEdit = () => setIsEditingTitle(true);
  const handleTitleSave = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      const newName = (e.target as HTMLInputElement).value.trim();
      if (newName) {
        setGraphName(newName);
        setIsEditingTitle(false);
      } else {
        toast({
          title: "Erro",
          description: "O nome do grafo não pode estar vazio.",
          variant: "destructive",
        });
      }
    } else if (e.key === 'Escape') {
      setIsEditingTitle(false);
    }
  };

  return (
    <SidebarProvider>
      <div className="min-h-screen flex w-full">
        <GraphPlatformSidebar onLoadGrafo={() => {}} />

        <div className="flex flex-col flex-1">
          <div className="bg-white border-b p-4 flex items-center justify-between">
            <div className="flex items-center space-x-4">
              {isEditingTitle ? (
                <Input
                  defaultValue={graphName}
                  className="text-xl font-semibold"
                  onKeyDown={handleTitleSave}
                  onBlur={() => setIsEditingTitle(false)}
                  autoFocus
                />
              ) : (
                <h1
                  className="text-xl font-semibold cursor-pointer hover:text-blue-600"
                  onClick={handleTitleEdit}
                  title="Clique para editar o nome do grafo"
                >
                  {graphName}
                </h1>
              )}
              <span className="text-sm text-gray-500">
                Vértices: {nodes.length} | Arestas: {edges.length}
              </span>
            </div>
          </div>

          <div className="mt-4 flex gap-2 justify-center">
            <button onClick={handleAddNode} className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Adicionar Vértice</button>
            <button onClick={handleAddEdge} className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">Adicionar Aresta</button>
            <button onClick={handleLayout} className="bg-yellow-500 text-white px-4 py-2 rounded hover:bg-yellow-600">Layout Automático</button>
            <button onClick={handleResetView} className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700">Resetar Visão</button>
            <button onClick={handleSaveGraph} className="bg-teal-600 text-white px-4 py-2 rounded hover:bg-teal-700">Salvar Grafo</button>
          </div>

          <div className="flex-1 overflow-hidden" ref={reactFlowWrapper}>
            <ReactFlow
              nodes={nodes}
              edges={edges}
              onNodesChange={onNodesChange}
              onEdgesChange={onEdgesChange}
              onConnect={onConnect}
              onInit={setReactFlowInstance}
              fitView
              nodeTypes={nodeTypes}
              edgeTypes={edgeTypes}
              onNodeClick={(_, node) => setSelectedNodeId(node.id)}
            >
              <MiniMap />
              <Controls />
              <Background />
            </ReactFlow>
          </div>
        </div>
      </div>
    </SidebarProvider>
  );
};

export default GraphMainEditor;
