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
        zIndex: 10,
        cursor: 'grab', // Consistente para todo o nó
        userSelect: 'none', // Evita seleção de texto
      }}
    >
      {data.label}

      {/* Ocultando Handles visuais e liberando a conexão */}
      <Handle
        type="source"
        position={Position.Top}
        style={{ opacity: 0 }}
      />
      <Handle
        type="target"
        position={Position.Bottom}
        style={{ opacity: 0 }}
      />
    </div>
  );
};

export default CustomNode;
