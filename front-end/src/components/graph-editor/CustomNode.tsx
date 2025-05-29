import React from 'react';
import { Handle, Position } from 'reactflow';

const CustomNode = ({ data, selected }) => {
  const { label, color = '#ffcc00', icon = '⚙️', size = 60 } = data;
  
  return (
    <div
      style={{
        background: color,
        border: selected ? '3px solid #333' : '2px solid #333',
        borderRadius: '50%',
        width: size,
        height: size,
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        fontWeight: 'bold',
        fontSize: size / 3,
        position: 'relative',
        zIndex: 10,
        cursor: 'pointer',
        userSelect: 'none',
      }}
    >
      {/* Ícone central */}
      <span style={{ position: 'absolute', top: '5%', left: '50%', transform: 'translate(-50%, 0)' }}>{icon}</span>
      {/* Label */}
      <span style={{ position: 'absolute', bottom: '10%', left: '50%', transform: 'translate(-50%, 0)', fontSize: size / 4 }}>
        {label}
      </span>
      {/* Oculta Handles visuais, mas permite conexão em qualquer ponto */}
      <Handle type="source" position={Position.Right} style={{ opacity: 0 }} />
      <Handle type="target" position={Position.Left} style={{ opacity: 0 }} />
    </div>
  );
};

export default CustomNode;
