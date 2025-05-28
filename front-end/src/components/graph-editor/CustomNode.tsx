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
        pointerEvents: 'auto',
      }}
    >
      {data.label}

      {/* Handles invisíveis para permitir conexão a qualquer ponto */}
      <Handle
        type="source"
        position={Position.Top}
        style={{ opacity: 0 }}
        isConnectable
      />
      <Handle
        type="source"
        position={Position.Right}
        style={{ opacity: 0 }}
        isConnectable
      />
      <Handle
        type="source"
        position={Position.Bottom}
        style={{ opacity: 0 }}
        isConnectable
      />
      <Handle
        type="source"
        position={Position.Left}
        style={{ opacity: 0 }}
        isConnectable
      />
      <Handle
        type="target"
        position={Position.Top}
        style={{ opacity: 0 }}
        isConnectable
      />
      <Handle
        type="target"
        position={Position.Right}
        style={{ opacity: 0 }}
        isConnectable
      />
      <Handle
        type="target"
        position={Position.Bottom}
        style={{ opacity: 0 }}
        isConnectable
      />
      <Handle
        type="target"
        position={Position.Left}
        style={{ opacity: 0 }}
        isConnectable
      />
    </div>
  );
};

export default CustomNode;
