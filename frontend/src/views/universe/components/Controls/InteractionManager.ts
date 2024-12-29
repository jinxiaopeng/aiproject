import * as THREE from 'three'
import { NodeObject } from '../../types/NodeTypes'

export class InteractionManager {
  private raycaster: THREE.Raycaster
  private mouse: THREE.Vector2
  private camera: THREE.Camera
  private domElement: HTMLElement
  private nodeObjects: NodeObject[]
  private hoveredNode: NodeObject | null
  private selectedNode: NodeObject | null
  private onNodeClick: (node: any) => void
  private onNodeHover: (node: any) => void

  constructor(
    camera: THREE.Camera,
    domElement: HTMLElement,
    onNodeClick: (node: any) => void,
    onNodeHover: (node: any) => void
  ) {
    this.raycaster = new THREE.Raycaster()
    this.mouse = new THREE.Vector2()
    this.camera = camera
    this.domElement = domElement
    this.nodeObjects = []
    this.hoveredNode = null
    this.selectedNode = null
    this.onNodeClick = onNodeClick
    this.onNodeHover = onNodeHover

    this.init()
  }

  private init(): void {
    this.domElement.addEventListener('mousemove', this.onMouseMove.bind(this))
    this.domElement.addEventListener('click', this.onClick.bind(this))
  }

  public setNodeObjects(nodes: NodeObject[]): void {
    this.nodeObjects = nodes
  }

  private onMouseMove(event: MouseEvent): void {
    const rect = this.domElement.getBoundingClientRect()
    this.mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1
    this.mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1

    this.checkIntersection()
  }

  private onClick(event: MouseEvent): void {
    const rect = this.domElement.getBoundingClientRect()
    this.mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1
    this.mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1

    this.checkIntersection(true)
  }

  private checkIntersection(isClick: boolean = false): void {
    this.raycaster.setFromCamera(this.mouse, this.camera)

    const intersects = this.raycaster.intersectObjects(
      this.nodeObjects.map(no => no.object),
      true
    )

    if (intersects.length > 0) {
      const intersectedObject = intersects[0].object
      const nodeObject = this.nodeObjects.find(
        no => no.object === intersectedObject || no.object.children.includes(intersectedObject)
      )

      if (nodeObject) {
        if (isClick) {
          this.selectedNode = nodeObject
          this.onNodeClick(nodeObject.node)
        } else if (this.hoveredNode !== nodeObject) {
          this.hoveredNode = nodeObject
          this.onNodeHover(nodeObject.node)
        }
      }
    } else {
      if (!isClick && this.hoveredNode) {
        this.hoveredNode = null
        this.onNodeHover(null)
      }
    }
  }

  public dispose(): void {
    this.domElement.removeEventListener('mousemove', this.onMouseMove.bind(this))
    this.domElement.removeEventListener('click', this.onClick.bind(this))
  }
} 