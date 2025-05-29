import React from 'react';
import { Handle, Position, NodeProps } from '@xyflow/react';

const CustomCircleNode: React.FC<NodeProps> = ({ data, selected }) => {
  return (
    <div
      style={{
        background: selected ? '#2563eb' : '#4f46e5',
        color: 'white',
        border: '2px solid #1e40af',
        borderRadius: '50%',
        width: 60,
        height: 60,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontWeight: 'bold',
        fontSize: '16px',
        position: 'relative'
      }}
    >
      {data.label}

      {/* Conexão livre: Handles invisíveis cobrindo toda a circunferência */}
      <Handle
        type="target"
        position={Position.Left}
        style={{ opacity: 0, width: '100%', height: '100%', borderRadius: '50%', top: 0, left: 0 }}
        isConnectable={true}
      />
      <Handle
        type="source"
        position={Position.Right}
        style={{ opacity: 0, width: '100%', height: '100%', borderRadius: '50%', top: 0, left: 0 }}
        isConnectable={true}
      />
    </div>
  );
};

export default CustomCircleNode;
