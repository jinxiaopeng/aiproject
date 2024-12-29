<template>
  <div ref="container" class="universe-scene"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as THREE from 'three'
import { CSS2DRenderer } from 'three/examples/jsm/renderers/CSS2DRenderer'
import { SceneManager } from './Scene/SceneManager'
import { CameraManager } from './Scene/CameraManager'
import { LightManager } from './Scene/LightManager'
import { NodeManager } from './Nodes/NodeManager'
import { LinkManager } from './Links/LinkManager'
import { ParticleSystem } from './Effects/ParticleSystem'
import { OrbitControlManager } from './Controls/OrbitControlManager'
import { InteractionManager } from './Controls/InteractionManager'
import { KnowledgeNode, KnowledgeLink } from '../types/NodeTypes'
import type { SceneConfig, CameraConfig, LightConfig, ControlsConfig } from '../types/SceneTypes'

// Props
const props = defineProps<{
  nodes: KnowledgeNode[]
  links: KnowledgeLink[]
}>()

// Emits
const emit = defineEmits<{
  (e: 'node-click', node: any): void
  (e: 'node-hover', node: any): void
}>()

// Refs
const container = ref<HTMLElement>()

// Managers
let sceneManager: SceneManager
let cameraManager: CameraManager
let lightManager: LightManager
let nodeManager: NodeManager
let linkManager: LinkManager
let particleSystem: ParticleSystem
let controlManager: OrbitControlManager
let interactionManager: InteractionManager

// Renderers
let renderer: THREE.WebGLRenderer
let labelRenderer: CSS2DRenderer

// Animation
let animationFrameId: number

// 初始化场景
const initScene = () => {
  if (!container.value) return

  try {
    const width = container.value.clientWidth
    const height = container.value.clientHeight

    // 初始化场景管理器
    const sceneConfig: SceneConfig = {
      width,
      height,
      backgroundColor: 0x000000
    }
    sceneManager = new SceneManager(sceneConfig)

    // 初始化相机管理器
    const cameraConfig: CameraConfig = {
      fov: 60,
      near: 1,
      far: 10000,
      position: { x: 1000, y: 500, z: 1000 }
    }
    cameraManager = new CameraManager(cameraConfig, width / height)

    // 初始化光照管理器
    const lightConfig: LightConfig = {
      ambient: {
        color: 0xffffff,
        intensity: 0.5
      },
      directional: {
        color: 0xffffff,
        intensity: 0.8,
        position: { x: 200, y: 200, z: 200 }
      }
    }
    lightManager = new LightManager(lightConfig)

    // 添加光照到场景
    sceneManager.add(lightManager.getAmbientLight())
    sceneManager.add(lightManager.getDirectionalLight())

    // 初始化渲染器
    renderer = new THREE.WebGLRenderer({
      antialias: true,
      alpha: true,
      powerPreference: 'high-performance'
    })
    renderer.setPixelRatio(window.devicePixelRatio)
    renderer.setSize(width, height)
    renderer.setClearColor(0x000000, 1)
    container.value.appendChild(renderer.domElement)

    // 初始化标签渲染器
    labelRenderer = new CSS2DRenderer()
    labelRenderer.setSize(width, height)
    labelRenderer.domElement.style.position = 'absolute'
    labelRenderer.domElement.style.top = '0'
    labelRenderer.domElement.style.left = '0'
    labelRenderer.domElement.style.pointerEvents = 'none'
    container.value.appendChild(labelRenderer.domElement)

    // 初始化控制器管理器
    const controlsConfig: ControlsConfig = {
      enableDamping: true,
      dampingFactor: 0.05,
      screenSpacePanning: true,
      minDistance: 500,
      maxDistance: 3000,
      autoRotateSpeed: 0.5
    }
    controlManager = new OrbitControlManager(
      cameraManager.getCamera(),
      renderer.domElement,
      controlsConfig
    )

    // 初始化节点管理器
    nodeManager = new NodeManager()

    // 初始化连接管理器
    linkManager = new LinkManager()

    // 初始化粒子系统
    particleSystem = new ParticleSystem()
    sceneManager.add(particleSystem.getObject())

    // 初始化交互管理器
    interactionManager = new InteractionManager(
      cameraManager.getCamera(),
      renderer.domElement,
      (node) => emit('node-click', node),
      (node) => emit('node-hover', node)
    )

    // 添加事件监听
    window.addEventListener('resize', onWindowResize)

    // 创建节点和连接
    createNodesAndLinks()

    // 开始动画循环
    animate()
  } catch (error) {
    console.error('Error initializing scene:', error)
  }
}

// 创建节点和连接
const createNodesAndLinks = () => {
  // 创建所有节点
  props.nodes.forEach((node, index) => {
    const nodeObject = nodeManager.createNode(node, index, props.nodes.length)
    sceneManager.add(nodeObject.object)
  })

  // 创建所有连接
  props.links.forEach(link => {
    const sourceNode = nodeManager.getNode(link.source)
    const targetNode = nodeManager.getNode(link.target)
    
    if (sourceNode && targetNode) {
      const linkObject = linkManager.createLink(
        link,
        sourceNode.object.position,
        targetNode.object.position
      )
      sceneManager.add(linkObject.object)
    }
  })

  // 更新交互管理器的节点列表
  interactionManager.setNodeObjects(nodeManager.getAllNodes())
}

// 窗口大小改变处理
const onWindowResize = () => {
  if (!container.value) return

  const width = container.value.clientWidth
  const height = container.value.clientHeight

  cameraManager.updateAspect(width / height)
  renderer.setSize(width, height)
  labelRenderer.setSize(width, height)
}

// 动画循环
const animate = () => {
  animationFrameId = requestAnimationFrame(animate)

  // 更新控制器
  controlManager.update()

  // 更新粒子系统
  particleSystem.update()

  // 渲染场景
  renderer.render(sceneManager.getScene(), cameraManager.getCamera())
  labelRenderer.render(sceneManager.getScene(), cameraManager.getCamera())
}

// 生命周期钩子
onMounted(() => {
  initScene()
})

onUnmounted(() => {
  // 清理资源
  window.removeEventListener('resize', onWindowResize)
  cancelAnimationFrame(animationFrameId)

  sceneManager.dispose()
  nodeManager.dispose()
  linkManager.dispose()
  particleSystem.dispose()
  controlManager.dispose()
  interactionManager.dispose()
  
  renderer.dispose()
})

// 监听属性变化
watch(
  () => props.nodes,
  () => {
    if (sceneManager) {
      sceneManager.clear()
      createNodesAndLinks()
    }
  },
  { deep: true }
)

watch(
  () => props.links,
  () => {
    if (sceneManager) {
      sceneManager.clear()
      createNodesAndLinks()
    }
  },
  { deep: true }
)
</script>

<style scoped>
.universe-scene {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
  background-color: #000;
}

:deep(.node-label) {
  color: #fff;
  font-family: Arial, sans-serif;
  font-size: 12px;
  padding: 2px 4px;
  background: rgba(0, 0, 0, 0.6);
  border-radius: 4px;
  pointer-events: none;
  white-space: nowrap;
}
</style> 