
import React from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Button } from '@/components/ui/button';
import { Trash2 } from 'lucide-react';
import Graph from 'graphology';
import { NodeProperties, EdgeProperties } from './types';

interface GraphEditorSidebarProps {
  graph: Graph;
  selectedNode: string | null;
  isWeighted: boolean;
  nodeProperties: NodeProperties;
  edgeProperties: EdgeProperties;
  onNodePropertiesChange: (properties: NodeProperties) => void;
  onEdgePropertiesChange: (properties: EdgeProperties) => void;
  onRemoveSelectedNode: () => void;
}

const GraphEditorSidebar: React.FC<GraphEditorSidebarProps> = ({
  graph,
  selectedNode,
  isWeighted,
  nodeProperties,
  edgeProperties,
  onNodePropertiesChange,
  onEdgePropertiesChange,
  onRemoveSelectedNode
}) => {
  return (
    <div className="w-64 border-l bg-white p-4 overflow-y-auto">
      <Tabs defaultValue="node">
        <TabsList className="w-full">
          <TabsTrigger value="node" className="flex-1">Vértice</TabsTrigger>
          <TabsTrigger value="edge" className="flex-1">Aresta</TabsTrigger>
        </TabsList>
        
        <TabsContent value="node" className="space-y-4 mt-4">
          <div>
            <Label htmlFor="nodeLabel">Rótulo</Label>
            <Input
              id="nodeLabel"
              value={nodeProperties.label}
              onChange={(e) => onNodePropertiesChange({...nodeProperties, label: e.target.value})}
              placeholder="Auto (a, b, c...)"
            />
            <p className="text-xs text-gray-500 mt-1">
              Deixe vazio para gerar automaticamente (a, b, c, ..., z, aa, ab...)
            </p>
          </div>
          
          <div>
            <Label htmlFor="nodeColor">Cor</Label>
            <div className="flex items-center space-x-2">
              <Input
                id="nodeColor"
                type="color"
                value={nodeProperties.color}
                onChange={(e) => onNodePropertiesChange({...nodeProperties, color: e.target.value})}
                className="w-12 h-8 p-0"
              />
              <Input
                value={nodeProperties.color}
                onChange={(e) => onNodePropertiesChange({...nodeProperties, color: e.target.value})}
                className="flex-1"
              />
            </div>
          </div>
          
          {selectedNode && (
            <div className="mt-4 p-2 bg-gray-50 rounded">
              <h4 className="text-sm font-medium mb-2">Vértice Selecionado: {selectedNode}</h4>
              <Button 
                size="sm" 
                variant="destructive"
                onClick={onRemoveSelectedNode}
                className="w-full"
              >
                <Trash2 className="h-4 w-4 mr-1" />
                Remover
              </Button>
            </div>
          )}
        </TabsContent>
        
        <TabsContent value="edge" className="space-y-4 mt-4">
          {isWeighted && (
            <div>
              <Label htmlFor="edgeWeight">Peso</Label>
              <div className="flex items-center space-x-2">
                <Input
                  type="number"
                  step="0.1"
                  min="0"
                  value={edgeProperties.weight}
                  onChange={(e) => onEdgePropertiesChange({...edgeProperties, weight: parseFloat(e.target.value) || 0})}
                  className="flex-1"
                />
              </div>
            </div>
          )}
          
          <div>
            <Label htmlFor="edgeColor">Cor</Label>
            <div className="flex items-center space-x-2">
              <Input
                id="edgeColor"
                type="color"
                value={edgeProperties.color}
                onChange={(e) => onEdgePropertiesChange({...edgeProperties, color: e.target.value})}
                className="w-12 h-8 p-0"
              />
              <Input
                value={edgeProperties.color}
                onChange={(e) => onEdgePropertiesChange({...edgeProperties, color: e.target.value})}
                className="flex-1"
              />
            </div>
          </div>
          
          <div className="mt-4">
            <p className="text-sm text-gray-500">
              Para adicionar uma aresta, selecione o modo de aresta e clique em dois vértices consecutivamente.
            </p>
          </div>
        </TabsContent>
      </Tabs>
      
      <div className="mt-6">
        <h3 className="text-sm font-medium mb-2">Informações do Grafo</h3>
        <div className="text-xs space-y-1">
          <p>Vértices: {graph?.order || 0}</p>
          <p>Arestas: {graph?.size || 0}</p>
        </div>
      </div>
    </div>
  );
};

export default GraphEditorSidebar;
