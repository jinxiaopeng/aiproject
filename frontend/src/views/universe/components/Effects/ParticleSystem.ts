import * as THREE from 'three'

export class ParticleSystem {
  private particles: THREE.Points
  private particleCount: number
  private particleGeometry: THREE.BufferGeometry
  private particleMaterial: THREE.PointsMaterial

  constructor(count: number = 1000) {
    this.particleCount = count
    this.particleGeometry = new THREE.BufferGeometry()
    this.particleMaterial = new THREE.PointsMaterial({
      size: 2,
      sizeAttenuation: true,
      color: 0xFFFFFF,
      transparent: true,
      opacity: 0.8,
      blending: THREE.AdditiveBlending,
      depthWrite: false
    })
    
    this.particles = this.createParticles()
  }

  private createParticles(): THREE.Points {
    const positions = new Float32Array(this.particleCount * 3)
    const velocities = new Float32Array(this.particleCount * 3)
    
    for (let i = 0; i < this.particleCount; i++) {
      const i3 = i * 3
      
      // Random positions in a sphere
      const radius = Math.random() * 1000
      const theta = Math.random() * Math.PI * 2
      const phi = Math.acos(2 * Math.random() - 1)
      
      positions[i3] = radius * Math.sin(phi) * Math.cos(theta)
      positions[i3 + 1] = radius * Math.sin(phi) * Math.sin(theta)
      positions[i3 + 2] = radius * Math.cos(phi)
      
      // Random velocities
      velocities[i3] = (Math.random() - 0.5) * 0.2
      velocities[i3 + 1] = (Math.random() - 0.5) * 0.2
      velocities[i3 + 2] = (Math.random() - 0.5) * 0.2
    }
    
    this.particleGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))
    this.particleGeometry.setAttribute('velocity', new THREE.BufferAttribute(velocities, 3))
    
    return new THREE.Points(this.particleGeometry, this.particleMaterial)
  }

  public update(): void {
    const positions = this.particleGeometry.attributes.position.array as Float32Array
    const velocities = this.particleGeometry.attributes.velocity.array as Float32Array
    
    for (let i = 0; i < this.particleCount; i++) {
      const i3 = i * 3
      
      // Update positions based on velocities
      positions[i3] += velocities[i3]
      positions[i3 + 1] += velocities[i3 + 1]
      positions[i3 + 2] += velocities[i3 + 2]
      
      // Check boundaries and reset particles if they go too far
      const distance = Math.sqrt(
        positions[i3] ** 2 +
        positions[i3 + 1] ** 2 +
        positions[i3 + 2] ** 2
      )
      
      if (distance > 1000) {
        const scale = 1000 / distance
        positions[i3] *= scale
        positions[i3 + 1] *= scale
        positions[i3 + 2] *= scale
      }
    }
    
    this.particleGeometry.attributes.position.needsUpdate = true
  }

  public getObject(): THREE.Points {
    return this.particles
  }

  public dispose(): void {
    this.particleGeometry.dispose()
    this.particleMaterial.dispose()
  }
} 