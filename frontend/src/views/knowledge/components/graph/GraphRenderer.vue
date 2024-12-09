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
            <el-icon><Setting /></el-icon>
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
import { Refresh, Setting } from '@element-plus/icons-vue'
import type { KnowledgeNode, KnowledgeLink } from '@/api/knowledge'

const props = defineProps<{
  nodes: KnowledgeNode[]
  links: KnowledgeLink[]
}>()

const emit = defineEmits<{
  (e: 'nodeClick', node: KnowledgeNode): void
  (e: 'nodeHover', node: KnowledgeNode | null): void
}>()

const chartRef = ref<HTMLElement>()
let chart: echarts.ECharts | null = null
const layoutMode = ref<'force' | 'circular'>('force')

// 添加节点散开动画相关的状态
const expandedNodeId = ref<string | number | null>(null)
const nodePositions = ref<Map<string | number, { x: number, y: number }>>(new Map())

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
              <p>类型：${node.category}</p>
              <p>难度：${node.difficulty}</p>
              <p>${node.description}</p>
            </div>
          `
        }
        return params.name
      }
    },
    legend: {
      data: ['领域', '漏洞', '技能', '技术', '工具', '基础', '管理', '架构', '研究'],
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
        gravity: 0.2,
        friction: 0.1,
        layoutAnimation: true
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
        { name: '领域', itemStyle: { color: '#409eff' } },
        { name: '漏洞', itemStyle: { color: '#f56c6c' } },
        { name: '技能', itemStyle: { color: '#67c23a' } },
        { name: '技术', itemStyle: { color: '#e6a23c' } },
        { name: '工具', itemStyle: { color: '#e6a23c' } },
        { name: '基础', itemStyle: { color: '#409eff' } },
        { name: '管理', itemStyle: { color: '#67c23a' } },
        { name: '架构', itemStyle: { color: '#409eff' } },
        { name: '研究', itemStyle: { color: '#e6a23c' } }
      ],
      data: props.nodes.map(node => {
        const isExpanded = expandedNodeId.value === node.id
        const baseSize = node.value * 5
        
        // 如果节点已展开或与展开节点相关，调整其位置
        let position = undefined
        if (expandedNodeId.value !== null) {
          const savedPosition = nodePositions.value.get(node.id)
          if (savedPosition) {
            position = [savedPosition.x, savedPosition.y]
          }
        }
        
        return {
          id: node.id,
          name: node.name,
          value: node,
          category: node.category,
          symbolSize: isExpanded ? baseSize * 1.5 : baseSize,
          itemStyle: {
            color: getNodeColor(node.category),
            borderColor: getNodeColor(node.category),
            borderWidth: isExpanded ? 4 : 2,
            shadowBlur: isExpanded ? 20 : 10,
            shadowColor: getNodeColor(node.category)
          },
          label: {
            show: true,
            color: '#e5eaf3',
            fontSize: isExpanded ? 14 : 12,
            fontWeight: isExpanded ? 'bold' : 'normal'
          },
          x: position ? position[0] : undefined,
          y: position ? position[1] : undefined,
          fixed: position !== undefined
        }
      }),
      links: props.links.map(link => {
        const isRelated = expandedNodeId.value === link.source || expandedNodeId.value === link.target
        return {
          source: link.source,
          target: link.target,
          name: link.type,
          value: link.type,
          lineStyle: {
            width: isRelated ? Math.max(2, link.value) : Math.max(1, link.value),
            curveness: 0.2,
            color: isRelated ? '#67c23a' : '#409eff',
            opacity: isRelated ? 0.8 : 0.6,
            shadowBlur: isRelated ? 10 : 0,
            shadowColor: '#67c23a'
          },
          label: {
            show: true,
            color: isRelated ? '#67c23a' : '#909399',
            fontSize: isRelated ? 12 : 10,
            fontWeight: isRelated ? 'bold' : 'normal'
          }
        }
      }),
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
      handleNodeClick(node)
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

// 处理节点点击
const handleNodeClick = (node: KnowledgeNode) => {
  // 保存当前所有节点的位置
  if (chart) {
    const graphicOption = chart.getOption()
    const nodes = graphicOption.series[0].data
    nodes.forEach((node: any) => {
      if (node.x !== undefined && node.y !== undefined) {
        nodePositions.value.set(node.id, { x: node.x, y: node.y })
      }
    })
  }

  // 如果点击的是已展开的节点，则收起
  if (expandedNodeId.value === node.id) {
    expandedNodeId.value = null
    nodePositions.value.clear()
  } else {
    // 否则展开新节点
    expandedNodeId.value = node.id
    
    // 调整力导向图的参数以产生散开效果
    if (chart) {
      chart.setOption({
        series: [{
          force: {
            repulsion: 2000,
            edgeLength: 300,
            gravity: 0.1,
            friction: 0.2,
            layoutAnimation: true
          }
        }]
      })
    }
  }

  // 更新图表
  initChart()
  
  // 触发节点点击事件
  emit('nodeClick', node)
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
    '领域': '#409eff',
    '漏洞': '#f56c6c',
    '技能': '#67c23a',
    '技术': '#e6a23c',
    '工具': '#e6a23c',
    '基础': '#409eff',
    '管理': '#67c23a',
    '架构': '#409eff',
    '研究': '#e6a23c',
    'default': '#909399'
  }
  return colors[category] || colors.default
}

// 获取分类标签
const getCategoryLabel = (category: string) => {
  return category
}

// 获取难度标签
const getDifficultyLabel = (difficulty: string) => {
  return difficulty
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
watch([() => props.nodes, () => props.links], () => {
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
</style>