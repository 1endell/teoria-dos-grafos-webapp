import React from 'react';
import { BaseEdge, getBezierPath } from 'reactflow';

const CustomFloatingEdge = ({ id, sourceX, sourceY, targetX, targetY }) => {
  const [edgePath] = getBezierPath({ sourceX, sourceY, targetX, targetY });
  return (
    <BaseEdge
      id={id}
      path={edgePath}
      style={{ stroke: '#000', strokeWidth: 2 }}
    />
  );
};

export default CustomFloatingEdge;
