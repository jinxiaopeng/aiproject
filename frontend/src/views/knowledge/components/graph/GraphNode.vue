<template>
  <node-interaction
    :node="node"
    :position="position"
    @position-change="handlePositionChange"
  >
    <div
      class="graph-node"
      :class="{ selected: isSelected }"
      @click="$emit('click', node)"
      @mouseenter="$emit('mouseenter', node)"
      @mouseleave="$emit('mouseleave', node)"
    >
      <div class="node-icon" :style="{ background: getCategoryColor(node.category) }">
        <i :class="getCategoryIcon(node.category)"></i>
      </div>
      <div class="node-label">{{ node.name }}</div>
      <div class="node-difficulty" :class="node.difficulty">
        {{ getDifficultyLabel(node.difficulty) }}
      </div>
    </div>
  </node-interaction>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { KnowledgeNode } from '@/api/knowledge'
import NodeInteraction from './NodeInteraction.vue'

// Props
const props = defineProps<{
  node: KnowledgeNode
  position: { x: number; y: number }
  isSelected: boolean
}>()

// Emits
const emit = defineEmits<{
  (e: 'click', node: KnowledgeNode): void
  (e: 'mouseenter', node: KnowledgeNode): void
  (e: 'mouseleave', node: KnowledgeNode): void
  (e: 'position-update', nodeId: string | number, position: { x: number; y: number }): void
}>()

// 处理位置更新
const handlePositionChange = (nodeId: string | number, position: { x: number; y: number }) => {
  emit('position-update', nodeId, position)
}

const nodeStyle = computed(() => {
  if (!props.position) {
    return {
      transform: 'translate(0px, 0px)',
      opacity: 0
    }
  }
  return {
    transform: `translate(${props.position.x}px, ${props.position.y}px)`,
    opacity: 1
  }
})

const getCategoryColor = (category: string) => {
  const colors: Record<string, string> = {
    concept: 'linear-gradient(135deg, #41b883, #42b8e7)',
    vulnerability: 'linear-gradient(135deg, #f56c6c, #ff9f7f)',
    tool: 'linear-gradient(135deg, #e6a23c, #f7ba2a)',
    technique: 'linear-gradient(135deg, #409eff, #36cfc9)',
    protocol: 'linear-gradient(135deg, #722ed1, #b37feb)',
    default: 'linear-gradient(135deg, #909399, #c0c4cc)'
  }
  return colors[category] || colors.default
}

const getCategoryIcon = (category: string) => {
  const icons: Record<string, string> = {
    concept: 'el-icon-connection',
    vulnerability: 'el-icon-warning',
    tool: 'el-icon-tools',
    technique: 'el-icon-magic-stick',
    protocol: 'el-icon-guide',
    default: 'el-icon-info'
  }
  return icons[category] || icons.default
}

const getDifficultyColor = (difficulty: string) => {
  const colors: Record<string, string> = {
    basic: '#67c23a',
    intermediate: '#e6a23c',
    advanced: '#f56c6c',
    expert: '#722ed1'
  }
  return colors[difficulty] || '#909399'
}
</script>

<style scoped>
.graph-node {
  position: absolute;
  display: flex;
  align-items: center;
  padding: 4px 8px;
  background: rgba(26, 29, 33, 0.95);
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  pointer-events: auto;
  transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1);
  transform-origin: center center;
  user-select: none;
  border: 1px solid rgba(65, 184, 131, 0.2);
  backdrop-filter: blur(4px);
  gap: 6px;
}

.graph-node:hover {
  transform: scale(1.1);
  z-index: 10;
  border-color: rgba(65, 184, 131, 0.5);
  box-shadow: 0 4px 16px rgba(65, 184, 131, 0.2);
}

.graph-node.selected {
  border-color: #41b883;
  box-shadow: 0 0 0 2px rgba(65, 184, 131, 0.2),
              0 4px 16px rgba(65, 184, 131, 0.3);
}

.node-icon {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.node-icon i {
  font-size: 12px;
}

.node-label {
  font-size: 12px;
  color: #e5eaf3;
  white-space: nowrap;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 0.8;
  }
  50% {
    transform: scale(1.1);
    opacity: 1;
  }
  100% {
    transform: scale(1);
    opacity: 0.8;
  }
}

.graph-node.selected .node-icon {
  animation: pulse 2s ease-in-out infinite;
}
</style> 