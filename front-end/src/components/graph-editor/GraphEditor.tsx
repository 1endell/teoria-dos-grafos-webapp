import React from 'react';
import GraphEditorReactFlow from './GraphEditorReactFlow';

interface GraphEditorProps {
  grafoId?: string;
  onSave?: (grafoId: string) => void;
}

const GraphEditor: React.FC<GraphEditorProps> = ({ grafoId, onSave }) => {
  return (
    <GraphEditorReactFlow grafoId={grafoId} onSave={onSave} />
  );
};

export default GraphEditor;
