import * as THREE from 'three'
import { KnowledgeLink } from '../../types/NodeTypes'
import { LinkMaterial } from './LinkMaterial'

interface LinkObject {
  link: KnowledgeLink
  object: THREE.Line
  material: THREE.ShaderMaterial
}

export class LinkManager {
  private links: Map<string, LinkObject>

  constructor() {
    this.links = new Map()
  }

  public createLink(
    link: KnowledgeLink,
    sourcePosition: THREE.Vector3,
    targetPosition: THREE.Vector3
  ): LinkObject {
    const geometry = this.createLinkGeometry(sourcePosition, targetPosition)
    const material = LinkMaterial.createMaterial()
    const line = new THREE.Line(geometry, material)

    const linkObject: LinkObject = {
      link,
      object: line,
      material
    }

    const linkId = this.getLinkId(link.source, link.target)
    this.links.set(linkId, linkObject)

    return linkObject
  }

  private createLinkGeometry(
    source: THREE.Vector3,
    target: THREE.Vector3
  ): THREE.BufferGeometry {
    const points = this.calculateCurve(source, target)
    return new THREE.BufferGeometry().setFromPoints(points)
  }

  private calculateCurve(
    source: THREE.Vector3,
    target: THREE.Vector3
  ): THREE.Vector3[] {
    const points: THREE.Vector3[] = []
    const segments = 50

    for (let i = 0; i <= segments; i++) {
      const t = i / segments
      const point = new THREE.Vector3()
      point.lerpVectors(source, target, t)
      
      // Add a slight curve
      const mid = source.clone().lerp(target, 0.5)
      const height = source.distanceTo(target) * 0.1
      const curve = Math.sin(t * Math.PI) * height
      point.y += curve
      
      points.push(point)
    }

    return points
  }

  public updateLinkPosition(
    linkId: string,
    sourcePosition: THREE.Vector3,
    targetPosition: THREE.Vector3
  ): void {
    const linkObject = this.links.get(linkId)
    if (!linkObject) return

    const geometry = this.createLinkGeometry(sourcePosition, targetPosition)
    linkObject.object.geometry.dispose()
    linkObject.object.geometry = geometry
  }

  private getLinkId(source: string, target: string): string {
    return `${source}-${target}`
  }

  public getLink(source: string, target: string): LinkObject | undefined {
    return this.links.get(this.getLinkId(source, target))
  }

  public getAllLinks(): LinkObject[] {
    return Array.from(this.links.values())
  }

  public dispose(): void {
    this.links.forEach(link => {
      link.object.geometry.dispose()
      if (link.material instanceof THREE.Material) {
        link.material.dispose()
      }
    })
    this.links.clear()
  }
} 