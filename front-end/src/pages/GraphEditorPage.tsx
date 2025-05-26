import React from 'react';
import GraphVisualEditor from '@/components/GraphVisualEditor';

const GraphEditorPage: React.FC = () => {
  return (
    <div className="h-screen flex flex-col">
      <GraphVisualEditor />
    </div>
  );
};

export default GraphEditorPage;
