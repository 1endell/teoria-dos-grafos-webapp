import React from 'react';
import { BaseEdge, EdgeLabelRenderer, getStraightPath } from 'reactflow';

const CustomFloatingEdge = ({ id, sourceX, sourceY, targetX, targetY, sourcePosition, targetPosition, style, markerEnd }) => {
  const [edgePath] = getStraightPath({ sourceX, sourceY, targetX, targetY });

  return (
    <>
      <BaseEdge path={edgePath} style={{ strokeWidth: 2, stroke: '#333', ...style }} markerEnd={undefined} />
      <EdgeLabelRenderer>
        <div
          style={{
            position: 'absolute',
            transform: `translate(-50%, -50%) translate(${(sourceX + targetX) / 2}px, ${(sourceY + targetY) / 2}px)`,
            fontSize: 12,
            background: 'white',
            padding: '2px 4px',
            borderRadius: 4,
          }}
          className="nodrag nopan"
        >
          {/* Se quiser colocar um label opcional, insira aqui */}
        </div>
      </EdgeLabelRenderer>
    </>
  );
};

export default CustomFloatingEdge;
