import React from 'react';
import { BaseEdge, EdgeLabelRenderer, getBezierPath, EdgeProps } from 'reactflow';

const CustomEdge: React.FC<EdgeProps> = ({ id, sourceX, sourceY, targetX, targetY, sourcePosition, targetPosition, label }) => {
  const [path, labelX, labelY] = getBezierPath({
    sourceX,
    sourceY,
    sourcePosition,
    targetX,
    targetY,
    targetPosition,
  });

  return (
    <>
      <BaseEdge
        id={id}
        path={path}
        style={{ stroke: 'red', strokeWidth: 3, fill: 'none' }}
      />
      <EdgeLabelRenderer>
        <div
          style={{
            position: 'absolute',
            transform: `translate(-50%, -50%) translate(${labelX}px,${labelY}px)`,
            background: 'white',
            padding: 4,
            borderRadius: 4,
            border: '1px solid #ddd',
            fontSize: 12,
          }}
          className="nodrag nopan"
        >
          {label || 'Aresta'}
        </div>
      </EdgeLabelRenderer>
    </>
  );
};

export default CustomEdge;
