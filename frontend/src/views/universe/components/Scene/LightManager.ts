import * as THREE from 'three'
import { LightConfig } from '../../types/SceneTypes'

export class LightManager {
  private ambientLight: THREE.AmbientLight
  private directionalLight: THREE.DirectionalLight

  constructor(config: LightConfig) {
    this.ambientLight = new THREE.AmbientLight(
      config.ambient.color,
      config.ambient.intensity
    )

    this.directionalLight = new THREE.DirectionalLight(
      config.directional.color,
      config.directional.intensity
    )

    this.init(config)
  }

  private init(config: LightConfig): void {
    const { x, y, z } = config.directional.position
    this.directionalLight.position.set(x, y, z)
  }

  public getAmbientLight(): THREE.AmbientLight {
    return this.ambientLight
  }

  public getDirectionalLight(): THREE.DirectionalLight {
    return this.directionalLight
  }

  public updateAmbientIntensity(intensity: number): void {
    this.ambientLight.intensity = intensity
  }

  public updateDirectionalIntensity(intensity: number): void {
    this.directionalLight.intensity = intensity
  }

  public setDirectionalPosition(x: number, y: number, z: number): void {
    this.directionalLight.position.set(x, y, z)
  }

  public dispose(): void {
    // Dispose of any resources if needed
  }
} 