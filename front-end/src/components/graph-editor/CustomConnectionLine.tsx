import React from 'react';
import { getStraightPath } from '@xyflow/react';

function CustomConnectionLine({ fromX, fromY, toX, toY, connectionLineStyle }) {
  const [edgePath] = getStraightPath({ sourceX: fromX, sourceY: fromY, targetX: toX, targetY: toY });
  return <path style={connectionLineStyle} fill="none" d={edgePath} />;
}

export default CustomConnectionLine;
