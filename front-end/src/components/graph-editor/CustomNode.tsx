import { Handle } from '@xyflow/react';

export default function CustomNode({ id, data }) {
  const size = 60 * 0.4;
  const showHandles = data?.mode === 'addEdge';

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
        cursor: 'move',
        position: 'relative',
      }}
    >
      {id}
      {showHandles && (
        <>
          <Handle
            type="source"
            position="top"
            style={{
              width: size,
              height: size,
              position: 'absolute',
              top: '50%',
              left: '50%',
              transform: 'translate(-50%, -50%)',
              borderRadius: '50%',
              opacity: 0,
              cursor: 'crosshair',
            }}
          />
          <Handle
            type="target"
            position="top"
            style={{
              width: size,
              height: size,
              position: 'absolute',
              top: '50%',
              left: '50%',
              transform: 'translate(-50%, -50%)',
              borderRadius: '50%',
              opacity: 0,
            }}
          />
        </>
      )}
    </div>
  );
}
