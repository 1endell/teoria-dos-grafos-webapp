import React, { useState, useCallback, useRef } from 'react';
import { SidebarProvider } from '@/components/ui/sidebar';
import GraphPlatformSidebar from './graph-editor/GraphPlatformSidebar';
import { Input } from '@/components/ui/input';
import { useToast } from '@/hooks/use-toast';
import GraphEditorToolbarReactFlow from './graph-editor/GraphEditorToolbarReactFlow';
import ReactFlow, {
  MiniMap, Controls, Background,
  addEdge, useNodesState, useEdgesState, Connection, Edge, Node, ReactFlowProvider
} from 'reactflow';
import 'reactflow/dist/style.css';

const GraphMainEditor: React.FC = () => {
  const [isEditingTitle, setIsEditingTitle] = useState(false);
  const { toast } = useToast();
  const [graphName, setGraphName] = useState('Novo Grafo');

  // React Flow States
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const reactFlowWrapper = useRef<HTMLDivElement>(null);
  const [reactFlowInstance, setReactFlowInstance] = useState<any>(null);

  const onConnect = useCallback((params: Edge | Connection) => {
    setEdges((eds) => addEdge(params, eds));
  }, [setEdges]);

  const handleAddNode = () => {
    const newNode: Node = {
      id: `${+new Date()}`,
      position: { x: Math.random() * 400, y: Math.random() * 400 },
      data: { label: `Node ${nodes.length + 1}` },
      type: 'default',
    };
    setNodes((nds) => nds.concat(newNode));
  };

  const handleAddEdge = () => {
    toast({
      title: "Modo Aresta",
      description: "Conecte dois nós para criar uma aresta.",
      variant: "default",
    });
  };

  const handleLayout = () => {
    toast({
      title: "Layout Automático",
      description: "Layout automático ainda não implementado.",
      variant: "default",
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
          <ReactFlowProvider>
            {/* Header com título editável */}
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

            {/* Toolbar React Flow */}
            <GraphEditorToolbarReactFlow
              onAddNode={handleAddNode}
              onAddEdge={handleAddEdge}
              onLayout={handleLayout}
              onResetView={handleResetView}
              onSaveGraph={handleSaveGraph}
            />

            {/* React Flow Canvas */}
            <div className="flex-1 overflow-hidden" ref={reactFlowWrapper}>
              <ReactFlow
                nodes={nodes}
                edges={edges}
                onNodesChange={onNodesChange}
                onEdgesChange={onEdgesChange}
                onConnect={onConnect}
                onInit={setReactFlowInstance}
                fitView
              >
                <MiniMap />
                <Controls />
                <Background />
              </ReactFlow>
            </div>
          </ReactFlowProvider>
        </div>
      </div>
    </SidebarProvider>
  );
};

export default GraphMainEditor;
