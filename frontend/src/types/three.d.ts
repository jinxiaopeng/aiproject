import * as THREE from 'three'
import { KnowledgeNode } from '@/api/knowledge'

export interface NodeUserData extends KnowledgeNode {
  material: THREE.ShaderMaterial
  glowMaterial: THREE.ShaderMaterial
  originalPosition: THREE.Vector3
  velocity: THREE.Vector3
  connections: THREE.Line[]
}

export interface NodeMesh extends THREE.Mesh {
  userData: NodeUserData
}

export interface EdgeUserData {
  source: NodeMesh
  target: NodeMesh
  relation: string
  curve: THREE.QuadraticBezierCurve3
  material: THREE.ShaderMaterial
}

export interface EdgeLine extends THREE.Line {
  userData: EdgeUserData
} 