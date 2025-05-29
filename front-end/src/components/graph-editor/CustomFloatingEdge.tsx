import { BaseEdge, getStraightPath, useInternalNode } from '@xyflow/react';
import { getEdgeParams } from './utils.js';

function FloatingEdge({ id, source, target }) {
  const sourceNode = useInternalNode(source);
  const targetNode = useInternalNode(target);

  if (!sourceNode || !targetNode) return null;

  const { sx, sy, tx, ty } = getEdgeParams(sourceNode, targetNode);
  const [path] = getStraightPath({ sourceX: sx, sourceY: sy, targetX: tx, targetY: ty });

  return <BaseEdge id={id} path={path} style={{ stroke: '#000', strokeWidth: 2 }} />;
}

export default FloatingEdge;
