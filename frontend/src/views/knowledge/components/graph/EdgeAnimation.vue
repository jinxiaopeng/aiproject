<template>
  <g class="edge-animation" :class="{ 'is-highlighted': isHighlighted }">
    <!-- 主路径 -->
    <path
      :d="pathData"
      class="edge-path"
      fill="none"
      :stroke="getEdgeColor"
      stroke-width="1.5"
      :marker-end="isHighlighted ? 'url(#arrow-highlighted)' : 'url(#arrow)'"
    />

    <!-- 动画效果 -->
    <path
      v-if="isHighlighted"
      :d="pathData"
      class="edge-animation-path"
      fill="none"
      :stroke="getEdgeColor"
      stroke-width="2"
    >
      <animate
        attributeName="stroke-dashoffset"
        :from="pathLength"
        :to="0"
        dur="1.5s"
        repeatCount="indefinite"
      />
    </path>

    <!-- 关系标签 -->
    <g v-if="isHighlighted" :transform="getLabelPosition">
      <rect
        :width="getLabelWidth"
        height="22"
        rx="4"
        ry="4"
        fill="rgba(28, 28, 35, 0.95)"
        :stroke="getEdgeColor"
        stroke-width="1"
        transform="translate(-50%, -50%)"
      />
      <text
        class="edge-label"
        :fill="getEdgeColor"
        text-anchor="middle"
        dominant-baseline="middle"
        font-size="12"
      >
        {{ edge.relation }}
      </text>
    </g>
  </g>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { KnowledgeLink } from '@/api/knowledge'

const props = defineProps<{
  edge: KnowledgeLink
  sourcePos: { x: number; y: number }
  targetPos: { x: number; y: number }
  isHighlighted: boolean
}>()

// 计算路径数据
const pathData = computed(() => {
  const { sourcePos, targetPos } = props
  const dx = targetPos.x - sourcePos.x
  const dy = targetPos.y - sourcePos.y
  const dr = Math.sqrt(dx * dx + dy * dy)
  
  // 使用二次贝塞尔曲线创建平滑的曲线
  const midX = (sourcePos.x + targetPos.x) / 2
  const midY = (sourcePos.y + targetPos.y) / 2
  const offset = dr * 0.2 // 控制曲线的弯曲程度
  
  // 计算垂直于连线的控制点
  const angle = Math.atan2(dy, dx)
  const perpAngle = angle + Math.PI / 2
  const controlX = midX + Math.cos(perpAngle) * offset
  const controlY = midY + Math.sin(perpAngle) * offset
  
  return `M ${sourcePos.x} ${sourcePos.y} Q ${controlX} ${controlY} ${targetPos.x} ${targetPos.y}`
})

// 计算路径长度（用于动画）
const pathLength = computed(() => {
  const path = document.createElementNS('http://www.w3.org/2000/svg', 'path')
  path.setAttribute('d', pathData.value)
  return path.getTotalLength()
})

// 获取边的颜色
const getEdgeColor = computed(() => {
  const colors: Record<string, string> = {
    'includes': 'var(--el-color-primary)',
    'depends_on': 'var(--el-color-warning)',
    'related_to': 'var(--el-color-info)',
    'causes': 'var(--el-color-danger)',
    'default': 'var(--el-color-info)'
  }
  return colors[props.edge.relation] || colors.default
})

// 获取标签位置
const getLabelPosition = computed(() => {
  const { sourcePos, targetPos } = props
  const midX = (sourcePos.x + targetPos.x) / 2
  const midY = (sourcePos.y + targetPos.y) / 2
  return `translate(${midX}, ${midY})`
})

// 获取标签宽度
const getLabelWidth = computed(() => {
  return props.edge.relation.length * 8 + 16 // 根据文本长度动态计算宽度
})
</script>

<style scoped>
.edge-animation {
  pointer-events: none;
}

.edge-path {
  transition: all 0.3s ease;
}

.edge-animation-path {
  stroke-dasharray: 10, 5;
  opacity: 0.6;
}

.edge-label {
  font-size: 12px;
  font-weight: 500;
  pointer-events: none;
  user-select: none;
}

.is-highlighted .edge-path {
  stroke-width: 2;
  filter: url(#glow);
}

/* 动画效果 */
@keyframes dash {
  to {
    stroke-dashoffset: 0;
  }
}
</style> 