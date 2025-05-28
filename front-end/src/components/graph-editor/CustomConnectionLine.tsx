import React from 'react';
import { ConnectionLineComponentProps, getStraightPath } from 'reactflow';

const CustomConnectionLine = ({ fromX, fromY, toX, toY, connectionLineStyle }: ConnectionLineComponentProps) => {
  const [edgePath] = getStraightPath({ sourceX: fromX, sourceY: fromY, targetX: toX, targetY: toY });

  return (
    <path
      fill="none"
      stroke="#333"
      strokeWidth={2}
      d={edgePath}
      style={connectionLineStyle}
    />
  );
};

export default CustomConnectionLine;
