import React from 'react';
import { Handle, NodeProps, Position } from 'reactflow';

const CustomNode: React.FC<NodeProps> = ({ data }) => {
  return (
    <div
      style={{
        position: 'relative',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        border: '2px solid #000',
        borderRadius: '50%',
        width: 60,
        height: 60,
        backgroundColor: 'white',
        fontWeight: 'bold',
        color: '#000',
      }}
    >
      {data.label}
      {/* Handles invisíveis cobrindo a borda */}
      <Handle type="source" position={Position.Top} style={{ width: 20, height: 20, opacity: 0 }} />
      <Handle type="source" position={Position.Right} style={{ width: 20, height: 20, opacity: 0 }} />
      <Handle type="source" position={Position.Bottom} style={{ width: 20, height: 20, opacity: 0 }} />
      <Handle type="source" position={Position.Left} style={{ width: 20, height: 20, opacity: 0 }} />
      <Handle type="target" position={Position.Top} style={{ width: 20, height: 20, opacity: 0 }} />
      <Handle type="target" position={Position.Right} style={{ width: 20, height: 20, opacity: 0 }} />
      <Handle type="target" position={Position.Bottom} style={{ width: 20, height: 20, opacity: 0 }} />
      <Handle type="target" position={Position.Left} style={{ width: 20, height: 20, opacity: 0 }} />
    </div>
  );
};

export default CustomNode;
