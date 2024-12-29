import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'
import { PerspectiveCamera } from 'three'
import { ControlsConfig } from '../../types/SceneTypes'

export class OrbitControlManager {
  private controls: OrbitControls

  constructor(camera: PerspectiveCamera, domElement: HTMLElement, config: ControlsConfig) {
    this.controls = new OrbitControls(camera, domElement)
    this.init(config)
  }

  private init(config: ControlsConfig): void {
    this.controls.enableDamping = config.enableDamping
    this.controls.dampingFactor = config.dampingFactor
    this.controls.screenSpacePanning = config.screenSpacePanning
    this.controls.minDistance = config.minDistance
    this.controls.maxDistance = config.maxDistance
    this.controls.autoRotateSpeed = config.autoRotateSpeed
  }

  public getControls(): OrbitControls {
    return this.controls
  }

  public update(): void {
    this.controls.update()
  }

  public enableAutoRotate(enable: boolean): void {
    this.controls.autoRotate = enable
  }

  public setRotateSpeed(speed: number): void {
    this.controls.autoRotateSpeed = speed
  }

  public setMinDistance(distance: number): void {
    this.controls.minDistance = distance
  }

  public setMaxDistance(distance: number): void {
    this.controls.maxDistance = distance
  }

  public dispose(): void {
    this.controls.dispose()
  }
} 