import { BaseEdge, getStraightPath, useInternalNode } from '@xyflow/react';

function getNodeIntersection(intersectionNode, targetNode) {
  const { width: w, height: h } = intersectionNode.measured;
  const { x: x2, y: y2 } = intersectionNode.internals.positionAbsolute;
  const { x: x1, y: y1 } = targetNode.internals.positionAbsolute;
  return { x: x2 + w / 2, y: y2 + h / 2 };
}

function getEdgeParams(source, target) {
  const sourcePoint = getNodeIntersection(source, target);
  const targetPoint = getNodeIntersection(target, source);
  return { sx: sourcePoint.x, sy: sourcePoint.y, tx: targetPoint.x, ty: targetPoint.y };
}

function CustomFloatingEdge({ id, source, target }) {
  const sourceNode = useInternalNode(source);
  const targetNode = useInternalNode(target);

  if (!sourceNode || !targetNode) return null;

  const { sx, sy, tx, ty } = getEdgeParams(sourceNode, targetNode);
  const [path] = getStraightPath({ sourceX: sx, sourceY: sy, targetX: tx, targetY: ty });

  return <BaseEdge id={id} path={path} style={{ stroke: '#000', strokeWidth: 2 }} />;
}

export default CustomFloatingEdge;
