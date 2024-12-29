import { Object3D, Color, Material } from 'three'
import { CSS2DObject } from 'three/examples/jsm/renderers/CSS2DRenderer'

export interface KnowledgeNode {
  id: string
  name: string
  category: string
  level?: number
  description?: string
  progress?: number
  isRecommended?: boolean
}

export interface KnowledgeLink {
  source: string
  target: string
  type?: string
  strength?: number
}

export interface NodeObject {
  node: KnowledgeNode
  object: Object3D
  label: CSS2DObject
  material: Material
  originalColor: Color
}

export interface NodeMaterialUniforms {
  color: { value: Color }
  glowColor: { value: Color }
  time: { value: number }
}

export interface NodePosition {
  x: number
  y: number
  z: number
  radius: number
  angle: number
} 