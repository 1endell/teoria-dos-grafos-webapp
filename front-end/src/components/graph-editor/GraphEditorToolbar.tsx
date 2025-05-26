
import React from 'react';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { Label } from '@/components/ui/label';
import { 
  MousePointer, Circle, ArrowRight, Move, 
  Save, Trash2, Maximize 
} from 'lucide-react';
import { EditorMode } from './types';

interface GraphEditorToolbarProps {
  mode: EditorMode;
  isDirected: boolean;
  isWeighted: boolean;
  selectedNode: string | null;
  isLoading: boolean;
  onModeChange: (mode: EditorMode) => void;
  onToggleDirected: () => void;
  onToggleWeighted: () => void;
  onApplyLayout: (type: string) => void;
  onResetZoom: () => void;
  onRemoveSelectedNode: () => void;
  onSaveGraph: () => void;
}

const GraphEditorToolbar: React.FC<GraphEditorToolbarProps> = ({
  mode,
  isDirected,
  isWeighted,
  selectedNode,
  isLoading,
  onModeChange,
  onToggleDirected,
  onToggleWeighted,
  onApplyLayout,
  onResetZoom,
  onRemoveSelectedNode,
  onSaveGraph
}) => {
  return (
    <div className="bg-white border-b p-2 flex items-center justify-between">
      <div className="flex items-center space-x-2">
        <Button
          size="sm"
          variant={mode === 'select' ? 'default' : 'outline'}
          onClick={() => onModeChange('select')}
          title="Selecionar"
        >
          <MousePointer className="h-4 w-4" />
        </Button>
        <Button
          size="sm"
          variant={mode === 'addNode' ? 'default' : 'outline'}
          onClick={() => onModeChange('addNode')}
          title="Adicionar Vértice"
        >
          <Circle className="h-4 w-4" />
        </Button>
        <Button
          size="sm"
          variant={mode === 'addEdge' ? 'default' : 'outline'}
          onClick={() => onModeChange('addEdge')}
          title="Adicionar Aresta"
        >
          <ArrowRight className="h-4 w-4" />
        </Button>
        <Button
          size="sm"
          variant={mode === 'pan' ? 'default' : 'outline'}
          onClick={() => onModeChange('pan')}
          title="Mover Canvas"
        >
          <Move className="h-4 w-4" />
        </Button>
        
        <div className="h-6 border-r mx-2"></div>
        
        <Button
          size="sm"
          variant="outline"
          onClick={() => onApplyLayout('circular')}
          title="Layout Circular"
          disabled={isLoading}
        >
          <span className="text-xs">Circular</span>
        </Button>
        <Button
          size="sm"
          variant="outline"
          onClick={() => onApplyLayout('forceatlas2')}
          title="Layout Force Atlas 2"
          disabled={isLoading}
        >
          <span className="text-xs">Force</span>
        </Button>
        
        <div className="h-6 border-r mx-2"></div>
        
        <Button
          size="sm"
          variant="outline"
          onClick={onResetZoom}
          title="Resetar Zoom"
        >
          <Maximize className="h-4 w-4" />
        </Button>
      </div>
      
      <div className="flex items-center space-x-2">
        <div className="flex items-center space-x-2">
          <div className="flex items-center space-x-1">
            <Checkbox 
              id="directed"
              checked={isDirected}
              onCheckedChange={onToggleDirected}
            />
            <Label htmlFor="directed" className="text-xs">Direcionado</Label>
          </div>
          <div className="flex items-center space-x-1">
            <Checkbox 
              id="weighted"
              checked={isWeighted}
              onCheckedChange={onToggleWeighted}
            />
            <Label htmlFor="weighted" className="text-xs">Ponderado</Label>
          </div>
        </div>
        
        <div className="h-6 border-r mx-2"></div>
        
        <Button
          size="sm"
          variant="outline"
          onClick={onRemoveSelectedNode}
          disabled={!selectedNode}
          title="Remover Selecionado"
        >
          <Trash2 className="h-4 w-4" />
        </Button>
        
        <Button
          size="sm"
          variant="default"
          onClick={onSaveGraph}
          disabled={isLoading}
          title="Salvar Grafo"
        >
          <Save className="h-4 w-4 mr-1" />
          <span>Salvar</span>
        </Button>
      </div>
    </div>
  );
};

export default GraphEditorToolbar;
