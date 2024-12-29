import * as THREE from 'three'
import { CSS2DObject } from 'three/examples/jsm/renderers/CSS2DRenderer'
import { KnowledgeNode, NodeObject, NodePosition } from '../../types/NodeTypes'
import { NodeMaterial } from './NodeMaterial'

export class NodeManager {
  private nodes: Map<string, NodeObject>
  private radius: number
  private phi: number

  constructor(radius: number = 600) {
    this.nodes = new Map()
    this.radius = radius
    this.phi = Math.PI * (3 - Math.sqrt(5)) // 黄金角
  }

  public createNode(node: KnowledgeNode, index: number, total: number): NodeObject {
    // 创建几何体
    const geometry = new THREE.SphereGeometry(12, 32, 32)
    
    // 创建材质
    const color = this.getCategoryColor(node.category)
    const material = NodeMaterial.createMaterial(color)
    
    // 创建网格
    const sphere = new THREE.Mesh(geometry, material)
    
    // 计算位置
    const position = this.calculatePosition(index, total)
    sphere.position.set(
      position.x * this.radius,
      position.y * this.radius,
      position.z * this.radius
    )

    // 创建标签
    const label = this.createLabel(node.name)
    sphere.add(label)

    // 存储节点对象
    const nodeObject: NodeObject = {
      node,
      object: sphere,
      label,
      material,
      originalColor: color.clone()
    }
    this.nodes.set(node.id, nodeObject)

    return nodeObject
  }

  private calculatePosition(index: number, total: number): NodePosition {
    const y = 1 - (index / (total - 1)) * 2 // -1 到 1
    const radiusAtY = Math.sqrt(1 - y * y)
    const theta = this.phi * index

    return {
      x: Math.cos(theta) * radiusAtY,
      y: y,
      z: Math.sin(theta) * radiusAtY,
      radius: radiusAtY,
      angle: theta
    }
  }

  private createLabel(text: string): CSS2DObject {
    const labelDiv = document.createElement('div')
    labelDiv.className = 'node-label'
    labelDiv.textContent = text
    const label = new CSS2DObject(labelDiv)
    label.position.set(0, 20, 0)
    return label
  }

  private getCategoryColor(category: string): THREE.Color {
    // 这里可以根据实际需求设置不同类别的颜色
    const colors: { [key: string]: number } = {
      basic: 0x4CAF50,
      intermediate: 0x2196F3,
      advanced: 0x9C27B0,
      expert: 0xF44336
    }
    return new THREE.Color(colors[category] || 0xFFFFFF)
  }

  public getNode(id: string): NodeObject | undefined {
    return this.nodes.get(id)
  }

  public getAllNodes(): NodeObject[] {
    return Array.from(this.nodes.values())
  }

  public updateNodeColor(id: string, color: THREE.Color): void {
    const node = this.nodes.get(id)
    if (node && node.material instanceof THREE.ShaderMaterial) {
      NodeMaterial.updateColor(node.material, color)
    }
  }

  public resetNodeColor(id: string): void {
    const node = this.nodes.get(id)
    if (node && node.material instanceof THREE.ShaderMaterial) {
      NodeMaterial.updateColor(node.material, node.originalColor)
    }
  }

  public dispose(): void {
    this.nodes.forEach(node => {
      if (node.object instanceof THREE.Mesh) {
        node.object.geometry.dispose()
        if (node.material instanceof THREE.Material) {
          node.material.dispose()
        }
      }
    })
    this.nodes.clear()
  }
} 