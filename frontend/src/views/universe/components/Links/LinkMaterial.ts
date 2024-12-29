import * as THREE from 'three'

export class LinkMaterial {
  private static vertexShader = `
    varying float vDistance;
    void main() {
      vDistance = position.y;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `

  private static fragmentShader = `
    uniform vec3 color;
    uniform float opacity;
    varying float vDistance;
    void main() {
      float alpha = opacity * (1.0 - vDistance);
      gl_FragColor = vec4(color, alpha);
    }
  `

  public static createMaterial(color: THREE.Color = new THREE.Color(0x888888)): THREE.ShaderMaterial {
    return new THREE.ShaderMaterial({
      uniforms: {
        color: { value: color },
        opacity: { value: 0.6 }
      },
      vertexShader: LinkMaterial.vertexShader,
      fragmentShader: LinkMaterial.fragmentShader,
      transparent: true,
      depthWrite: false
    })
  }

  public static updateOpacity(material: THREE.ShaderMaterial, opacity: number): void {
    material.uniforms.opacity.value = opacity
  }

  public static updateColor(material: THREE.ShaderMaterial, color: THREE.Color): void {
    material.uniforms.color.value = color
  }
} 