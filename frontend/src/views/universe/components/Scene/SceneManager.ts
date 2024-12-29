import * as THREE from 'three'
import { SceneConfig } from '../../types/SceneTypes'

export class SceneManager {
  private scene: THREE.Scene

  constructor(config: SceneConfig) {
    this.scene = new THREE.Scene()
    this.init(config)
  }

  private init(config: SceneConfig): void {
    this.scene.background = new THREE.Color(config.backgroundColor)
  }

  public getScene(): THREE.Scene {
    return this.scene
  }

  public add(object: THREE.Object3D): void {
    this.scene.add(object)
  }

  public remove(object: THREE.Object3D): void {
    this.scene.remove(object)
  }

  public clear(): void {
    while(this.scene.children.length > 0) {
      this.scene.remove(this.scene.children[0])
    }
  }

  public dispose(): void {
    this.clear()
    // Dispose of any other resources if needed
  }
} 