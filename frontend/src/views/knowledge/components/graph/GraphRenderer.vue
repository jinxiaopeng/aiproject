<template>
  <div ref="container" class="graph-renderer">
    <canvas ref="canvas"></canvas>
    <div class="node-layer">
      <graph-node
        v-for="node in visibleNodes"
        :key="node.id"
        :node="node"
        :position="nodePositions[node.id]"
        :is-selected="selectedNodeId === node.id"
        @click="handleNodeClick"
        @mouseenter="handleNodeHover"
        @mouseleave="handleNodeLeave"
      />
    </div>
    <div class="edge-layer">
      <graph-edge
        v-for="edge in visibleEdges"
        :key="edge.source + '-' + edge.target"
        :source="nodePositions[edge.source]"
        :target="nodePositions[edge.target]"
        :relation="edge.type"
        :is-selected="isEdgeSelected(edge)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import { useElementSize } from '@vueuse/core'
import { ForceGraph } from '@/utils/force-graph'
import GraphNode from './GraphNode.vue'
import GraphEdge from './GraphEdge.vue'
import type { KnowledgeNode, KnowledgeLink } from '@/api/knowledge'

// Props
const props = defineProps<{
  nodes: KnowledgeNode[]
  edges: KnowledgeLink[]
}>()

// Emits
const emit = defineEmits<{
  (e: 'node-click', node: KnowledgeNode): void
  (e: 'node-hover', node: KnowledgeNode | null): void
}>()

// Refs
const container = ref<HTMLElement | null>(null)
const { width, height } = useElementSize(container)

// 状态
const selectedNodeId = ref<string | null>(null)
const nodePositions = ref<Record<string, { x: number, y: number }>>({})
const forceGraph = ref<ForceGraph | null>(null)

// 计算属性
const visibleNodes = computed(() => {
  return props.nodes.filter(node => {
    const position = nodePositions.value[node.id]
    return position !== undefined
  })
})

const visibleEdges = computed(() => {
  return props.edges.filter(edge => {
    const sourcePos = nodePositions.value[edge.source]
    const targetPos = nodePositions.value[edge.target]
    return sourcePos !== undefined && targetPos !== undefined
  })
})

// 监听尺寸变化
watch([width, height], ([newWidth, newHeight]) => {
  console.log('Container size:', newWidth, newHeight)
  if (forceGraph.value) {
    forceGraph.value.updateSize(newWidth, newHeight)
  }
})

// 方法
const initForceGraph = () => {
  if (!container.value) return
  
  console.log('Initializing force graph with size:', width.value, height.value)
  forceGraph.value = new ForceGraph({
    nodes: props.nodes,
    edges: props.edges,
    width: width.value,
    height: height.value,
    onTick: (positions) => {
      nodePositions.value = positions
    }
  })
}

const handleNodeClick = (node: KnowledgeNode) => {
  selectedNodeId.value = node.id
  emit('node-click', node)
}

const handleNodeHover = (node: KnowledgeNode) => {
  emit('node-hover', node)
}

const handleNodeLeave = () => {
  emit('node-hover', null)
}

const isEdgeSelected = (edge: KnowledgeLink) => {
  return selectedNodeId.value === edge.source || selectedNodeId.value === edge.target
}

// 监听属性变化
watch([() => props.nodes, () => props.edges], ([newNodes, newEdges]) => {
  console.log('Data updated:', { nodes: newNodes.length, edges: newEdges.length })
  if (forceGraph.value) {
    forceGraph.value.updateData(newNodes, newEdges)
  }
})

// 生命周期钩子
onMounted(() => {
  console.log('GraphRenderer mounted')
  initForceGraph()
})

onBeforeUnmount(() => {
  forceGraph.value?.destroy()
})
</script>

<style scoped>
.graph-renderer {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 500px;
  background: #1a1d21;
  background-image: 
    radial-gradient(circle at 25px 25px, rgba(65, 184, 131, 0.05) 2%, transparent 0%),
    radial-gradient(circle at 75px 75px, rgba(66, 184, 231, 0.05) 2%, transparent 0%);
  background-size: 100px 100px;
  border-radius: 4px;
  overflow: hidden;
  border: 1px solid rgba(65, 184, 131, 0.1);
  box-shadow: inset 0 0 100px rgba(0, 0, 0, 0.2);
}

canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: transparent;
}

.node-layer,
.edge-layer {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.node-layer {
  z-index: 2;
  pointer-events: auto;
}

.edge-layer {
  z-index: 1;
  pointer-events: none;
}

/* 添加网格线效果 */
.graph-renderer::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    linear-gradient(rgba(65, 184, 131, 0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(65, 184, 131, 0.05) 1px, transparent 1px);
  background-size: 50px 50px;
  pointer-events: none;
}

/* 添加辉光效果 */
.graph-renderer::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 50% 50%, rgba(65, 184, 131, 0.1), transparent 70%);
  pointer-events: none;
  opacity: 0.5;
}
</style> 