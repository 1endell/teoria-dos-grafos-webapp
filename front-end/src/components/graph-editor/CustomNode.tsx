import { Handle, Position } from '@xyflow/react';

export default function CustomNode({ id }) {
  return (
    <div
      style={{
        background: '#4f46e5',
        color: 'white',
        borderRadius: '50%',
        width: 60,
        height: 60,
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        fontWeight: 'bold',
        cursor: 'pointer',
        userSelect: 'none',
      }}
    >
      {id}
    </div>
  );
}
