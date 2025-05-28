import React from 'react';
import { Handle, Position } from 'reactflow';

const CustomNode = ({ data }) => {
  return (
    <div
      style={{
        background: 'white',
        border: '2px solid #333',
        borderRadius: '50%',
        width: 60,
        height: 60,
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        fontWeight: 'bold',
        position: 'relative',
        zIndex: 10, // Deixa o vértice acima das arestas
      }}
    >
      {data.label}

      {/* Handle para conexões */}
      <Handle
        type="source"
        position={Position.Right}
        style={{ opacity: 0 }} // Ocultar o handle (já usamos a circunferência toda)
      />
      <Handle
        type="target"
        position={Position.Left}
        style={{ opacity: 0 }} // Ocultar o handle (já usamos a circunferência toda)
      />
    </div>
  );
};

export default CustomNode;
