<template>
  <div class="graph-container">
    <div ref="chartRef" class="echarts-graph"></div>
    
    <!-- 控制面板 -->
    <div class="control-panel">
      <el-button-group>
        <el-tooltip content="重置视图" placement="top">
          <el-button @click="resetView">
            <el-icon><Refresh /></el-icon>
          </el-button>
        </el-tooltip>
        <el-tooltip content="切换布局" placement="top">
          <el-button @click="toggleLayout">
            <el-icon><SetUp /></el-icon>
          </el-button>
        </el-tooltip>
      </el-button-group>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { ElButton, ElButtonGroup, ElTooltip } from 'element-plus'
import { Refresh, SetUp } from '@element-plus/icons-vue'
import type { KnowledgeNode, KnowledgeLink } from '@/api/knowledge'

const props = defineProps<{
  nodes: KnowledgeNode[]
  edges: KnowledgeLink[]
}>()

const emit = defineEmits<{
  (e: 'nodeClick', node: KnowledgeNode): void
  (e: 'nodeHover', node: KnowledgeNode | null): void
}>()

const chartRef = ref<HTMLElement>()
let chart: echarts.ECharts | null = null
const layoutMode = ref<'force' | 'circular'>('force')

// 初始化图表
const initChart = () => {
  if (!chartRef.value) return
  
  chart = echarts.init(chartRef.value)
  
  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'item',
      formatter: (params: any) => {
        if (params.dataType === 'node') {
          const node = params.data.value
          return `
            <div class="tooltip-content">
              <h4>${node.name}</h4>
              <p>类型：${getCategoryLabel(node.category)}</p>
              <p>难度：${getDifficultyLabel(node.difficulty)}</p>
            </div>
          `
        }
        return params.name
      }
    },
    legend: {
      data: ['漏洞', '概念', '工具', '技术'],
      textStyle: {
        color: '#909399'
      },
      top: 20,
      right: 20
    },
    series: [{
      type: 'graph',
      layout: layoutMode.value,
      symbolSize: 50,
      roam: true,
      draggable: true,
      force: {
        repulsion: 1000,
        edgeLength: 200,
        gravity: 0.2
      },
      label: {
        show: true,
        position: 'right',
        formatter: '{b}',
        fontSize: 12,
        color: '#e5eaf3'
      },
      edgeSymbol: ['circle', 'arrow'],
      edgeSymbolSize: [4, 8],
      edgeLabel: {
        show: true,
        formatter: '{c}',
        fontSize: 10,
        color: '#909399'
      },
      categories: [
        { name: '漏洞', itemStyle: { color: '#f56c6c' } },
        { name: '概念', itemStyle: { color: '#409eff' } },
        { name: '工具', itemStyle: { color: '#e6a23c' } },
        { name: '技术', itemStyle: { color: '#67c23a' } }
      ],
      data: props.nodes.map(node => ({
        id: node.id,
        name: node.name,
        value: node,
        category: getCategoryLabel(node.category),
        symbolSize: 40,
        itemStyle: {
          color: getNodeColor(node.category),
          borderColor: getNodeColor(node.category),
          borderWidth: 2,
          shadowBlur: 10,
          shadowColor: getNodeColor(node.category)
        },
        label: {
          show: true,
          color: '#e5eaf3',
          fontSize: 12
        }
      })),
      links: props.edges.map(edge => ({
        source: edge.source,
        target: edge.target,
        name: edge.relation,
        value: edge.relation,
        lineStyle: {
          width: 2,
          curveness: 0.2,
          color: '#409eff',
          opacity: 0.6
        },
        label: {
          show: true,
          color: '#909399'
        }
      })),
      emphasis: {
        focus: 'adjacency',
        lineStyle: {
          width: 4,
          opacity: 1
        }
      }
    }]
  }
  
  chart.setOption(option)
  
  // 注册事件
  chart.on('click', (params) => {
    if (params.dataType === 'node') {
      const node = params.data.value
      emit('nodeClick', node)
    }
  })

  chart.on('mouseover', (params) => {
    if (params.dataType === 'node') {
      const node = params.data.value
      emit('nodeHover', node)
    }
  })

  chart.on('mouseout', () => {
    emit('nodeHover', null)
  })
}

// 切换布局
const toggleLayout = () => {
  layoutMode.value = layoutMode.value === 'force' ? 'circular' : 'force'
  if (chart) {
    chart.setOption({
      series: [{
        layout: layoutMode.value
      }]
    })
  }
}

// 重置视图
const resetView = () => {
  if (chart) {
    chart.dispatchAction({
      type: 'graphRoam',
      zoom: 1,
      dx: 0,
      dy: 0
    })
  }
}

// 获取节点颜色
const getNodeColor = (category: string) => {
  const colors: Record<string, string> = {
    'vulnerability': '#f56c6c',
    'concept': '#409eff',
    'tool': '#e6a23c',
    'technique': '#67c23a',
    'default': '#909399'
  }
  return colors[category] || colors.default
}

// 获取分类标签
const getCategoryLabel = (category: string) => {
  const labels: Record<string, string> = {
    'vulnerability': '漏洞',
    'concept': '概念',
    'tool': '工具',
    'technique': '技术',
    'default': '其他'
  }
  return labels[category] || category
}

// 获取难度标签
const getDifficultyLabel = (difficulty: string) => {
  const labels: Record<string, string> = {
    'basic': '入门',
    'intermediate': '进阶',
    'advanced': '高级',
    'expert': '专家',
    'default': '未知'
  }
  return labels[difficulty] || difficulty
}

// 监听窗口大小变化
const handleResize = () => {
  chart?.resize()
}

onMounted(() => {
  initChart()
  window.addEventListener('resize', handleResize)
})

// 监听数据变化
watch([() => props.nodes, () => props.edges], () => {
  if (chart) {
    initChart()
  }
}, { deep: true })

// 组件销毁时清理
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chart?.dispose()
})
</script>

<style scoped>
.graph-container {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 600px;
  background: transparent;
  border-radius: 4px;
  overflow: hidden;
}

.echarts-graph {
  width: 100%;
  height: 100%;
}

.control-panel {
  position: absolute;
  bottom: 20px;
  right: 20px;
  z-index: 10;
  background: rgba(28, 28, 35, 0.9);
  padding: 12px;
  border-radius: 8px;
  backdrop-filter: blur(10px);
  box-shadow: 
    0 4px 24px rgba(0, 0, 0, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

:deep(.el-button) {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #e5eaf3;
}

:deep(.el-button:hover) {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.3);
  color: #fff;
}

:deep(.el-tooltip__trigger) {
  display: inline-flex;
}

:deep(.tooltip-content) {
  padding: 8px;
}

:deep(.tooltip-content h4) {
  margin: 0 0 8px;
  color: #fff;
  font-size: 14px;
}

:deep(.tooltip-content p) {
  margin: 4px 0;
  color: #909399;
  font-size: 12px;
}
</style>