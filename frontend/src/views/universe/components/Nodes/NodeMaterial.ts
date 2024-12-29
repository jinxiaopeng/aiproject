import * as THREE from 'three'
import { NodeMaterialUniforms } from '../../types/NodeTypes'

export class NodeMaterial {
  private static vertexShader = `
    varying vec3 vNormal;
    varying vec3 vPosition;
    void main() {
      vNormal = normalize(normalMatrix * normal);
      vPosition = (modelViewMatrix * vec4(position, 1.0)).xyz;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `

  private static fragmentShader = `
    uniform vec3 color;
    uniform vec3 glowColor;
    uniform float time;
    varying vec3 vNormal;
    varying vec3 vPosition;
    void main() {
      float intensity = pow(0.7 - dot(vNormal, vec3(0, 0, 1.0)), 2.0);
      float glow = sin(time * 2.0) * 0.5 + 0.5;
      vec3 finalColor = mix(color, glowColor, intensity * glow);
      gl_FragColor = vec4(finalColor, 1.0);
    }
  `

  public static createMaterial(color: THREE.Color): THREE.ShaderMaterial {
    const uniforms: NodeMaterialUniforms = {
      color: { value: color },
      glowColor: { value: color.clone().multiplyScalar(1.5) },
      time: { value: 0 }
    }

    return new THREE.ShaderMaterial({
      uniforms,
      vertexShader: NodeMaterial.vertexShader,
      fragmentShader: NodeMaterial.fragmentShader,
      transparent: true,
      side: THREE.FrontSide
    })
  }

  public static updateTime(material: THREE.ShaderMaterial, time: number): void {
    material.uniforms.time.value = time
  }

  public static updateColor(material: THREE.ShaderMaterial, color: THREE.Color): void {
    material.uniforms.color.value = color
    material.uniforms.glowColor.value = color.clone().multiplyScalar(1.5)
  }
} 