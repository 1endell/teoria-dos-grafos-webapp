import { Handle } from '@xyflow/react';

export default function CustomNode({ id }) {
  const size = 60 * 0.4;

  return (
    <div
      style={{
        background: '#4f46e5',
        color: 'white',
        borderRadius: '50%',
        width: size,
        height: size,
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        fontWeight: 'bold',
        cursor: 'move', // Cursor para indicar arrastar
      }}
    >
      {id}
    </div>
  );
}
