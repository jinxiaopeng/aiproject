<template>
  <div ref="graphRef" class="graph-container">
    <canvas ref="canvasRef"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'
import type { NodeMesh, EdgeLine } from '@/types/three'
import type { KnowledgeNode } from '@/api/knowledge'
import gsap from 'gsap'

// Props
const props = defineProps<{
  nodes: KnowledgeNode[]
  links: { source: string; target: string; relation: string }[]
}>()

// Emits
const emit = defineEmits<{
  (e: 'nodeClick', node: KnowledgeNode): void
  (e: 'nodeHover', node: KnowledgeNode | null): void
}>()

// Refs
const graphRef = ref<HTMLElement | null>(null)
const canvasRef = ref<HTMLCanvasElement | null>(null)

// Scene variables
let scene: THREE.Scene
let camera: THREE.PerspectiveCamera
let renderer: THREE.WebGLRenderer
let controls: OrbitControls
let nodeMeshes: NodeMesh[] = []
let edgeLines: EdgeLine[] = []
let selectedObject: NodeMesh | null = null
let animationFrameId: number | null = null

// Initialize Three.js scene
const initScene = () => {
  if (!graphRef.value || !canvasRef.value) return

  scene = new THREE.Scene()
  camera = new THREE.PerspectiveCamera(
    75,
    graphRef.value.clientWidth / graphRef.value.clientHeight,
    0.1,
    2000
  )
  
  renderer = new THREE.WebGLRenderer({
    canvas: canvasRef.value,
    antialias: true,
    alpha: true
  })
  
  renderer.setSize(graphRef.value.clientWidth, graphRef.value.clientHeight)
  renderer.setPixelRatio(window.devicePixelRatio)
  
  camera.position.z = 1000
  
  controls = new OrbitControls(camera, renderer.domElement)
  controls.enableDamping = true
  controls.dampingFactor = 0.05
}

// Clean up
onBeforeUnmount(() => {
  if (animationFrameId !== null) {
    cancelAnimationFrame(animationFrameId)
  }
  
  if (renderer) {
    renderer.dispose()
  }
  
  // Clean up meshes and materials
  nodeMeshes.forEach(node => {
    if (node.geometry) node.geometry.dispose()
    if (node.material instanceof THREE.Material) {
      node.material.dispose()
    }
  })
  
  edgeLines.forEach(edge => {
    if (edge.geometry) edge.geometry.dispose()
    if (edge.material instanceof THREE.Material) {
      edge.material.dispose()
    }
  })
})

// Initialize
onMounted(() => {
  initScene()
})
</script>

<style scoped>
.graph-container {
  width: 100%;
  height: 100%;
  position: relative;
}

canvas {
  width: 100% !important;
  height: 100% !important;
}
</style> 