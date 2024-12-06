<template>
  <div class="graph-edge" :class="{ selected: isSelected }">
    <svg :width="width" :height="height" :style="svgStyle">
      <defs>
        <marker
          id="arrow"
          viewBox="0 0 10 10"
          refX="5"
          refY="5"
          markerWidth="6"
          markerHeight="6"
          orient="auto-start-reverse"
        >
          <path d="M 0 0 L 10 5 L 0 10 z" />
        </marker>
        <filter id="glow">
          <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
          <feMerge>
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
      </defs>
      <path
        :d="pathD"
        fill="none"
        stroke="currentColor"
        stroke-width="1.5"
        marker-end="url(#arrow)"
        filter="url(#glow)"
      />
      <text
        :x="labelX"
        :y="labelY"
        text-anchor="middle"
        alignment-baseline="middle"
        class="edge-label"
        filter="url(#glow)"
      >
        {{ relation }}
      </text>
    </svg>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

// Props
const props = defineProps<{
  source: { x: number; y: number }
  target: { x: number; y: number }
  relation: string
  isSelected: boolean
}>()

const width = computed(() => {
  const dx = props.target.x - props.source.x
  const dy = props.target.y - props.source.y
  return Math.abs(dx) + 40
})

const height = computed(() => {
  const dx = props.target.x - props.source.x
  const dy = props.target.y - props.source.y
  return Math.abs(dy) + 40
})

const svgStyle = computed(() => {
  const left = Math.min(props.source.x, props.target.x) - 20
  const top = Math.min(props.source.y, props.target.y) - 20
  return {
    position: 'absolute',
    left: `${left}px`,
    top: `${top}px`
  }
})

const pathD = computed(() => {
  const sourceX = props.source.x < props.target.x
    ? 20
    : width.value - 20
  const sourceY = props.source.y < props.target.y
    ? 20
    : height.value - 20
  const targetX = props.target.x < props.source.x
    ? 20
    : width.value - 20
  const targetY = props.target.y < props.source.y
    ? 20
    : height.value - 20

  const dx = targetX - sourceX
  const dy = targetY - sourceY
  const controlX = sourceX + dx * 0.5
  const controlY = sourceY + dy * 0.5

  return `M ${sourceX} ${sourceY} Q ${controlX} ${controlY} ${targetX} ${targetY}`
})

const labelX = computed(() => width.value / 2)
const labelY = computed(() => height.value / 2)
</script>

<style scoped>
.graph-edge {
  position: absolute;
  pointer-events: none;
  color: rgba(65, 184, 131, 0.4);
}

.graph-edge.selected {
  color: #41b883;
  z-index: 1;
}

.graph-edge marker {
  fill: currentColor;
}

.graph-edge path {
  stroke-dasharray: 10, 5;
  animation: dash 20s linear infinite;
}

@keyframes dash {
  to {
    stroke-dashoffset: -1000;
  }
}

.edge-label {
  font-size: 12px;
  fill: #e5eaf3;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
  font-weight: 500;
}

:deep(#arrow) {
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.3));
}
</style> 