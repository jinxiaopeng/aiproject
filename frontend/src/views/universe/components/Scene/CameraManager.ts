import * as THREE from 'three'
import { CameraConfig } from '../../types/SceneTypes'

export class CameraManager {
  private camera: THREE.PerspectiveCamera

  constructor(config: CameraConfig, aspect: number) {
    this.camera = new THREE.PerspectiveCamera(
      config.fov,
      aspect,
      config.near,
      config.far
    )
    this.init(config)
  }

  private init(config: CameraConfig): void {
    const { x, y, z } = config.position
    this.camera.position.set(x, y, z)
    this.camera.lookAt(0, 0, 0)
  }

  public getCamera(): THREE.PerspectiveCamera {
    return this.camera
  }

  public updateAspect(aspect: number): void {
    this.camera.aspect = aspect
    this.camera.updateProjectionMatrix()
  }

  public setPosition(x: number, y: number, z: number): void {
    this.camera.position.set(x, y, z)
  }

  public lookAt(x: number, y: number, z: number): void {
    this.camera.lookAt(x, y, z)
  }

  public dispose(): void {
    // Dispose of any resources if needed
  }
} 