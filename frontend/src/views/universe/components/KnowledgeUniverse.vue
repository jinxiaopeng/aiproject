<template>
  <div ref="container" class="universe-scene"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'
import { CSS2DRenderer, CSS2DObject } from 'three/examples/jsm/renderers/CSS2DRenderer'
import { Points, PointsMaterial } from 'three'

// Props
const props = defineProps<{
  nodes: any[]
  links: any[]
}>()

// Emits
const emit = defineEmits<{
  (e: 'node-click', node: any): void
  (e: 'node-hover', node: any): void
}>()

// Refs
const container = ref<HTMLElement>()

// Three.js variables
let scene: THREE.Scene
let camera: THREE.PerspectiveCamera
let renderer: THREE.WebGLRenderer
let labelRenderer: CSS2DRenderer
let controls: OrbitControls
let nodeObjects = new Map()
let linkObjects = new Map()
let raycaster = new THREE.Raycaster()
let mouse = new THREE.Vector2()

// 初始化场景
const initScene = () => {
  if (!container.value) {
    console.error('Container element not found')
    return
  }

  try {
    // 创建场景
    scene = new THREE.Scene()
    scene.background = new THREE.Color(0x000000)

    // 获取容器尺寸
    const width = container.value.clientWidth
    const height = container.value.clientHeight
    
    console.log('Container dimensions:', width, height)
    
    // 创建相机
    camera = new THREE.PerspectiveCamera(60, width / height, 1, 10000)
    camera.position.set(1000, 500, 1000)
    camera.lookAt(0, 0, 0)

    // 创建渲染器
    renderer = new THREE.WebGLRenderer({ 
      antialias: true,
      alpha: true,
      powerPreference: 'high-performance'
    })
    renderer.setPixelRatio(window.devicePixelRatio)
    renderer.setSize(width, height)
    renderer.setClearColor(0x000000, 1)
    container.value.appendChild(renderer.domElement)

    // 创建标签渲染器
    labelRenderer = new CSS2DRenderer()
    labelRenderer.setSize(width, height)
    labelRenderer.domElement.style.position = 'absolute'
    labelRenderer.domElement.style.top = '0'
    labelRenderer.domElement.style.left = '0'
    labelRenderer.domElement.style.pointerEvents = 'none'
    container.value.appendChild(labelRenderer.domElement)

    // 创建控制器
    controls = new OrbitControls(camera, renderer.domElement)
    controls.enableDamping = true
    controls.dampingFactor = 0.05
    controls.screenSpacePanning = true
    controls.minDistance = 500
    controls.maxDistance = 3000
    controls.autoRotateSpeed = 0.5

    // 添加光照
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5)
    scene.add(ambientLight)

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8)
    directionalLight.position.set(200, 200, 200)
    scene.add(directionalLight)

    // 添加事件监听
    window.addEventListener('resize', onWindowResize)
    container.value.addEventListener('mousemove', onMouseMove)
    container.value.addEventListener('click', onMouseClick)

    // 添加粒子效果
    addParticles()

    // 开始动画循环
    animate()
    
    console.log('Scene initialized successfully')
  } catch (error) {
    console.error('Error initializing scene:', error)
  }
}

// 添加节点材质的shader代码
const vertexShader = `
  varying vec2 vUv;
  void main() {
    vUv = uv;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
  }
`

const fragmentShader = `
  uniform vec3 glowColor;
  uniform float time;
  varying vec2 vUv;
  
  void main() {
    float dist = length(vUv - vec2(0.5));
    float alpha = smoothstep(0.5, 0.2, dist);
    float pulse = sin(time * 3.0) * 0.5 + 0.5;
    vec3 color = mix(glowColor, glowColor * 1.5, pulse);
    gl_FragColor = vec4(color, alpha);
  }
`

// 修改createNodeMaterial函数
const createNodeMaterial = (color: THREE.Color) => {
  return new THREE.ShaderMaterial({
    uniforms: {
      glowColor: { value: color },
      time: { value: 0 }
    },
    vertexShader,
    fragmentShader,
    transparent: true,
    depthWrite: false
  })
}

// 修改createNode函数
const createNode = (node: any) => {
  const geometry = new THREE.SphereGeometry(5, 32, 32)
  const color = getCategoryColor(node.category)
  const material = createNodeMaterial(color)
  const mesh = new THREE.Mesh(geometry, material)
  
  // 存储节点信息
  nodeObjects.set(node.id, {
    node,
    object: mesh,
    material,
    originalColor: color.clone()
  })
  
  return mesh
}

// 创建节点
const createNodes = () => {
  if (!scene) {
    console.error('Scene not initialized')
    return
  }

  try {
    // 计算球形分布的参数
    const radius = 600 // 球体半径
    const phi = Math.PI * (3 - Math.sqrt(5)) // 黄金角
    const totalNodes = props.nodes.length

    props.nodes.forEach((node, index) => {
      // 创建节点球体
      const geometry = new THREE.SphereGeometry(12, 32, 32)
      
      // 创建发光材质
      const glowMaterial = new THREE.ShaderMaterial({
        uniforms: {
          color: { value: new THREE.Color(getCategoryColor(node.category)) },
          glowColor: { value: new THREE.Color(getCategoryColor(node.category)) },
          time: { value: 0 }
        },
        vertexShader: `
          varying vec3 vNormal;
          varying vec3 vPosition;
          void main() {
            vNormal = normalize(normalMatrix * normal);
            vPosition = (modelViewMatrix * vec4(position, 1.0)).xyz;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
          }
        `,
        fragmentShader: `
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
        `,
        transparent: true,
        side: THREE.FrontSide
      })

      const sphere = new THREE.Mesh(geometry, glowMaterial)

      // 计算球面分布坐标
      const y = 1 - (index / (totalNodes - 1)) * 2 // -1 到 1
      const radiusAtY = Math.sqrt(1 - y * y) // 当前y坐标下的圆半径
      const theta = phi * index // 当前点的角度

      // 设置节点位置
      const x = Math.cos(theta) * radiusAtY
      const z = Math.sin(theta) * radiusAtY
      
      // 根据节点类别调整半径
      const categoryMultiplier = getCategoryRadiusMultiplier(node.category)
      sphere.position.set(
        x * radius * categoryMultiplier,
        y * radius,
        z * radius * categoryMultiplier
      )

      // 创建标签
      const labelDiv = document.createElement('div')
      labelDiv.className = 'node-label'
      labelDiv.textContent = node.name
      const label = new CSS2DObject(labelDiv)
      label.position.set(0, 20, 0)
      sphere.add(label)

      // 存储节点对象
      nodeObjects.set(node.id, {
        node,
        object: sphere,
        label,
        material: glowMaterial,
        originalColor: new THREE.Color(getCategoryColor(node.category))
      })

      scene.add(sphere)
    })
    
    console.log('Nodes created successfully:', props.nodes.length)
  } catch (error) {
    console.error('Error creating nodes:', error)
  }
}

// 根据类别获取半径乘数
const getCategoryRadiusMultiplier = (category: string) => {
  const multipliers: { [key: string]: number } = {
    'security': 1.2,  // 安全节点分布在外层
    'web': 1.0,       // Web节点在中层
    'network': 0.9,   // 网络节点稍内
    'system': 0.8,    // 系统节点更
    'database': 0.7   // 数据库节点最内
  }
  return multipliers[category] || 1.0
}

// 创建连接
const createLinks = () => {
  if (!scene) {
    console.error('Scene not initialized')
    return
  }

  try {
    console.log('Creating links:', props.links.length)
    
    props.links.forEach(link => {
      const sourceObj = nodeObjects.get(link.source)
      const targetObj = nodeObjects.get(link.target)
      
      if (sourceObj && targetObj) {
        // 创建管道几何体代替线条
        const direction = new THREE.Vector3().subVectors(
          targetObj.object.position,
          sourceObj.object.position
        )
        const length = direction.length()
        
        // 创建流光材质
        const material = new THREE.ShaderMaterial({
          uniforms: {
            time: { value: Math.random() * 10 },
            color: { value: new THREE.Color(0x4a90e2) },
            dashSize: { value: 5 },
            totalSize: { value: 15 },
            opacity: { value: 0.8 }
          },
          vertexShader: `
            uniform float time;
            varying vec2 vUv;
            void main() {
              vUv = uv;
              gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
            }
          `,
          fragmentShader: `
            uniform vec3 color;
            uniform float time;
            uniform float dashSize;
            uniform float totalSize;
            uniform float opacity;
            varying vec2 vUv;
            void main() {
              float t = mod(vUv.x - time * 0.5, totalSize) / totalSize;
              float dash = step(t, dashSize / totalSize);
              float alpha = dash * (1.0 - t * 1.5) * opacity;
              vec3 glowColor = mix(color, vec3(1.0), 0.5);
              gl_FragColor = vec4(glowColor, alpha);
            }
          `,
          transparent: true,
          depthWrite: false,
          side: THREE.DoubleSide
        })

        // 创建几何体
        const curve = new THREE.LineCurve3(
          sourceObj.object.position,
          targetObj.object.position
        )
        
        const tubeGeometry = new THREE.TubeGeometry(
          curve,
          20,  // 分段数
          3,   // 管道半径
          8,   // 管道截面分段数
          false // 是否闭合
        )
        
        // 创建管道
        const tube = new THREE.Mesh(tubeGeometry, material)
        scene.add(tube)
        
        // 存储连接对象
        linkObjects.set(link.id, {
          link,
          object: tube,
          source: sourceObj,
          target: targetObj,
          material,
          curve
        })
      }
    })
    
    console.log('Links created successfully')
  } catch (error) {
    console.error('Error creating links:', error)
  }
}

// 更新连接位置
const updateLinkPosition = (tube: THREE.Mesh, source: THREE.Mesh, target: THREE.Mesh) => {
  const curve = new THREE.LineCurve3(source.position, target.position)
  const geometry = new THREE.TubeGeometry(
    curve,
    20,  // 分段数
    3,   // 管道半径
    8,   // 管道截面分段数
    false // 是否闭合
  )
  tube.geometry.dispose()
  tube.geometry = geometry
}

// 动画循环
const animate = () => {
  if (!scene || !camera || !renderer || !labelRenderer) {
    console.error('Required objects not initialized')
    return
  }

  requestAnimationFrame(animate)
  
  try {
    controls.update()
    
    // 更新节点动画
    nodeObjects.forEach(({ object, material }) => {
      if (material.uniforms) {
        material.uniforms.time.value += 0.016
      }
    })
    
    // 更新连接位置和动画
    linkObjects.forEach(({ object, source, target, material }) => {
      if (source && target) {
        updateLinkPosition(object, source.object, target.object)
        if (material.uniforms) {
          material.uniforms.time.value += 0.016
        }
      }
    })
    
    // 渲染场景
    renderer.render(scene, camera)
    labelRenderer.render(scene, camera)
  } catch (error) {
    console.error('Error in animation loop:', error)
  }
}

// 事件处理
const onWindowResize = () => {
  if (!container.value) return
  
  const width = container.value.clientWidth
  const height = container.value.clientHeight
  
  camera.aspect = width / height
  camera.updateProjectionMatrix()
  
  renderer.setSize(width, height)
  labelRenderer.setSize(width, height)
}

const onMouseMove = (event: MouseEvent) => {
  if (!container.value) return
  
  const rect = container.value.getBoundingClientRect()
  mouse.x = ((event.clientX - rect.left) / container.value.clientWidth) * 2 - 1
  mouse.y = -((event.clientY - rect.top) / container.value.clientHeight) * 2 + 1
  
  raycaster.setFromCamera(mouse, camera)
  
  const intersects = raycaster.intersectObjects(scene.children)
  let hoveredNode = null
  
  nodeObjects.forEach(({ node, object, originalColor }) => {
    const material = object.material as THREE.MeshPhongMaterial
    material.color.copy(originalColor)
    material.opacity = 0.8
  })
  
  if (intersects.length > 0) {
    const intersected = intersects[0].object as THREE.Mesh
    nodeObjects.forEach(({ node, object }) => {
      if (object === intersected) {
        const material = object.material as THREE.MeshPhongMaterial
        material.color.setHex(0xff0000)
        material.opacity = 1
        hoveredNode = node
      }
    })
  }
  
  emit('node-hover', hoveredNode)
}

const onMouseClick = (event: MouseEvent) => {
  if (!container.value) return
  
  const rect = container.value.getBoundingClientRect()
  mouse.x = ((event.clientX - rect.left) / container.value.clientWidth) * 2 - 1
  mouse.y = -((event.clientY - rect.top) / container.value.clientHeight) * 2 + 1
  
  raycaster.setFromCamera(mouse, camera)
  
  const intersects = raycaster.intersectObjects(scene.children)
  if (intersects.length > 0) {
    const intersected = intersects[0].object as THREE.Mesh
    nodeObjects.forEach(({ node, object }) => {
      if (object === intersected) {
        highlightNode(node)
        // 注释掉发送点击事件，这样就不会触发弹出框
        // emit('node-click', node)
      }
    })
  } else {
    // 点击空白处重置效果
    highlightNode(null)
  }
}

// 公开方法
const resetCamera = () => {
  camera.position.set(0, 0, 500)
  camera.lookAt(0, 0, 0)
  controls.reset()
}

const toggleAutoRotate = (enabled: boolean) => {
  controls.autoRotate = enabled
}

const highlightNode = (node: any) => {
  if (!node) {
    // 重置所有节点效果
    nodeObjects.forEach(({ material, originalColor }) => {
      if (material.uniforms) {
        material.uniforms.glowColor.value = originalColor
        material.uniforms.time.value = 0
      }
    })
    
    // 重置所有连接效果
    linkObjects.forEach(({ material }) => {
      if (material.uniforms) {
        material.uniforms.opacity.value = 0.3
        material.uniforms.color.value = new THREE.Color(0x4a90e2)
      }
    })
    return
  }
  
  // 获取相关节点
  const relatedLinks = Array.from(linkObjects.values()).filter(({ link }) => 
    link.source === node.id || link.target === node.id
  )
  
  const relatedNodeIds = new Set([
    ...relatedLinks.map(({ link }) => link.source),
    ...relatedLinks.map(({ link }) => link.target)
  ])
  
  // 更新所有节点效果
  nodeObjects.forEach(({ node: currentNode, material, originalColor }) => {
    if (material.uniforms) {
      if (currentNode.id === node.id) {
        // 高亮选中节点
        material.uniforms.glowColor.value = new THREE.Color(0xff0000)
        material.uniforms.time.value = Date.now() * 0.001
      } else if (relatedNodeIds.has(currentNode.id)) {
        // 高亮相关节点
        material.uniforms.glowColor.value = new THREE.Color(0x00ff00)
        material.uniforms.time.value = Date.now() * 0.001
      } else {
        // 淡化其他节点
        material.uniforms.glowColor.value = originalColor
        material.uniforms.time.value = 0
      }
    }
  })
  
  // 更新连接效果
  linkObjects.forEach(({ link, material }) => {
    if (material.uniforms) {
      if (link.source === node.id || link.target === node.id) {
        // 高亮相关连接
        material.uniforms.opacity.value = 0.8
        material.uniforms.color.value = new THREE.Color(0x00ff00)
      } else {
        // 淡化其他连接
        material.uniforms.opacity.value = 0.1
        material.uniforms.color.value = new THREE.Color(0x4a90e2)
      }
    }
  })
}

const focusNode = (node: any) => {
  if (!node) return
  
  const nodeObj = nodeObjects.get(node.id)
  if (nodeObj) {
    const position = nodeObj.object.position
    const target = new THREE.Vector3(position.x, position.y, position.z)
    
    // 高亮相关节点
    highlightNode(node)
    
    // 相机动画
    gsap.to(camera.position, {
      duration: 1,
      x: target.x + 100,
      y: target.y + 50,
      z: target.z + 200,
      onUpdate: () => {
        camera.lookAt(target)
      },
      onComplete: () => {
        // 添加相机轻微晃动效果
        gsap.to(camera.position, {
          duration: 2,
          x: target.x + 110,
          y: target.y + 55,
          z: target.z + 210,
          yoyo: true,
          repeat: -1,
          ease: "sine.inOut"
        })
      }
    })
  }
}

defineExpose({
  resetCamera,
  toggleAutoRotate,
  highlightNode,
  focusNode
})

// 工具函数
const getCategoryColor = (category: string): THREE.Color => {
  const colorMap: { [key: string]: THREE.Color } = {
    'security': new THREE.Color(0xff0000),
    'web': new THREE.Color(0x4a90e2),
    'network': new THREE.Color(0x00ff00),
    'system': new THREE.Color(0xffff00),
    'database': new THREE.Color(0xff00ff)
  }
  return colorMap[category] || new THREE.Color(0x808080)
}

// 生命周期
onMounted(() => {
  console.log('Component mounted')
  initScene()
  
  // 延迟创建节点和连接，确保场景已经准备好
  nextTick(() => {
    console.log('Creating nodes and links')
    createNodes()
    createLinks()
  })
})

onUnmounted(() => {
  if (container.value) {
    window.removeEventListener('resize', onWindowResize)
    container.value.removeEventListener('mousemove', onMouseMove)
    container.value.removeEventListener('click', onMouseClick)
  }
})

// 监听数据变化
watch(() => props.nodes, () => {
  // 清除现有节点
  nodeObjects.forEach(({ object }) => {
    scene.remove(object)
  })
  nodeObjects.clear()
  
  // 创建新节点
  createNodes()
}, { deep: true })

watch(() => props.links, () => {
  // 清除现有连接
  linkObjects.forEach(({ object }) => {
    scene.remove(object)
  })
  linkObjects.clear()
  
  // 创建新连接
  createLinks()
}, { deep: true })

// 在initScene函数中添加粒子效果
const addParticles = () => {
  const particleGeometry = new THREE.BufferGeometry()
  const particleCount = 1000
  const positions = new Float32Array(particleCount * 3)
  
  for(let i = 0; i < particleCount * 3; i += 3) {
    positions[i] = (Math.random() - 0.5) * 1000
    positions[i + 1] = (Math.random() - 0.5) * 1000
    positions[i + 2] = (Math.random() - 0.5) * 1000
  }
  
  particleGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))
  
  const particleMaterial = new THREE.PointsMaterial({
    color: 0x666666,
    size: 1,
    transparent: true,
    opacity: 0.5,
    sizeAttenuation: true
  })
  
  const particles = new THREE.Points(particleGeometry, particleMaterial)
  scene.add(particles)
  
  // 添加粒子动画
  const animateParticles = () => {
    particles.rotation.x += 0.0001
    particles.rotation.y += 0.0001
  }
  
  return animateParticles
}
</script>

<style lang="scss" scoped>
.universe-scene {
  width: 100%;
  height: 100%;
}

:deep(.node-label) {
  color: #ffffff;
  font-size: 12px;
  padding: 2px 4px;
  background: rgba(0, 0, 0, 0.6);
  border-radius: 4px;
  pointer-events: none;
  white-space: nowrap;
}
</style> 