import React, { useState } from 'react';
import { SidebarProvider } from '@/components/ui/sidebar';
import GraphPlatformSidebar from './graph-editor/GraphPlatformSidebar';
import { Input } from '@/components/ui/input';
import { useToast } from '@/hooks/use-toast';
import GraphEditorReactFlow from './graph-editor/GraphEditorReactFlow';

const GraphMainEditor: React.FC = () => {
  const [isEditingTitle, setIsEditingTitle] = useState(false);
  const [graphName, setGraphName] = useState('Novo Grafo');
  const { toast } = useToast();

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
        <GraphPlatformSidebar onLoadGrafo={() => {}} /> {/* Carregar grafos futuro */}

        <div className="flex flex-col flex-1">
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
            </div>
          </div>

          {/* React Flow Editor completo */}
          <div className="flex-1 overflow-hidden">
            <GraphEditorReactFlow />
          </div>
        </div>
      </div>
    </SidebarProvider>
  );
};

export default GraphMainEditor;
