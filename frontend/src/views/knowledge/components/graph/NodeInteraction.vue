<template>
  <div 
    class="node-interaction"
    :style="nodeStyle"
    @mousedown="startDrag"
    @dblclick="handleDoubleClick"
  >
    <slot></slot>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import type { KnowledgeNode } from '@/api/knowledge'

const props = defineProps<{
  node: KnowledgeNode
  position: { x: number; y: number }
}>()

const emit = defineEmits<{
  (e: 'position-change', nodeId: string | number, position: { x: number; y: number }): void
}>()

const router = useRouter()
const isDragging = ref(false)
const dragOffset = ref({ x: 0, y: 0 })
const currentPosition = ref({ x: 0, y: 0 })

// 计算节点样式
const nodeStyle = computed(() => {
  const x = isDragging.value ? currentPosition.value.x : props.position.x
  const y = isDragging.value ? currentPosition.value.y : props.position.y
  
  return {
    transform: `translate(${x}px, ${y}px)`,
    cursor: isDragging.value ? 'grabbing' : 'grab',
    transition: isDragging.value ? 'none' : 'transform 0.3s cubic-bezier(0.4, 0, 0.2, 1)'
  }
})

// 开始拖拽
const startDrag = (event: MouseEvent) => {
  isDragging.value = true
  dragOffset.value = {
    x: event.clientX - props.position.x,
    y: event.clientY - props.position.y
  }
  currentPosition.value = props.position
  
  // 添加全局事件监听
  document.addEventListener('mousemove', handleDrag)
  document.addEventListener('mouseup', stopDrag)
}

// 处理拖拽
const handleDrag = (event: MouseEvent) => {
  if (!isDragging.value) return
  
  currentPosition.value = {
    x: event.clientX - dragOffset.value.x,
    y: event.clientY - dragOffset.value.y
  }
  
  emit('position-change', props.node.id, currentPosition.value)
}

// 停止拖拽
const stopDrag = () => {
  isDragging.value = false
  document.removeEventListener('mousemove', handleDrag)
  document.removeEventListener('mouseup', stopDrag)
}

// 处理双击
const handleDoubleClick = () => {
  // 如果节点有关联的课程，跳转到课程页面
  if (props.node.courseId) {
    router.push(`/learning-path/courses/${props.node.courseId}`)
  }
}

// 组件卸载时清理事件监听
onBeforeUnmount(() => {
  document.removeEventListener('mousemove', handleDrag)
  document.removeEventListener('mouseup', stopDrag)
})
</script>

<style scoped>
.node-interaction {
  position: absolute;
  user-select: none;
  will-change: transform;
}

.node-interaction:hover {
  z-index: 10;
}

.node-interaction:active {
  z-index: 11;
}
</style> 