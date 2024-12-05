<template>
  <div class="knowledge-container">
    <el-skeleton :loading="loading" animated>
      <template #template>
        <div class="skeleton-content">
          <el-skeleton-item variant="p" style="width: 100%; height: 600px" />
        </div>
      </template>
      
      <template #default>
        <!-- 错误提示 -->
        <el-alert
          v-if="error"
          type="error"
          :title="error"
          show-icon
          class="error-alert"
        >
          <template #default>
            <el-button type="primary" size="small" @click="handleRetry">
              重试
            </el-button>
          </template>
        </el-alert>

        <!-- 知识图谱 -->
        <el-card class="knowledge-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>知识图谱</span>
              <el-button type="primary" size="small" @click="handleRefresh">
                刷新
              </el-button>
            </div>
          </template>
          <div class="knowledge-content">
            <div id="knowledgeGraph" ref="graphRef" class="graph-container"></div>
          </div>
        </el-card>
      </template>
    </el-skeleton>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import type { EChartsOption } from 'echarts'
import { getKnowledgeGraph } from '@/api/profile'
import type { KnowledgeGraph } from '@/api/profile'

const loading = ref(true)
const error = ref('')
const graphRef = ref<HTMLElement>()
let knowledgeGraph: echarts.ECharts | null = null

// 清理图表实例
const disposeChart = () => {
  if (knowledgeGraph) {
    knowledgeGraph.dispose()
    knowledgeGraph = null
  }
}

// 初始化知识图谱
const initKnowledgeGraph = async () => {
  try {
    loading.value = true
    error.value = ''
    
    console.log('开始获取知识图谱数据...')
    const response = await getKnowledgeGraph()
    console.log('API响应:', response)
    
    // 验证数据格式
    if (!response) {
      throw new Error('API响应为空')
    }
    
    const graphData = response
    console.log('知识图谱数据:', {
      nodesCount: graphData.nodes?.length || 0,
      linksCount: graphData.links?.length || 0,
      nodes: graphData.nodes,
      links: graphData.links
    })
    
    if (!graphData.nodes || !Array.isArray(graphData.nodes) || graphData.nodes.length === 0) {
      throw new Error('知识图谱节点数据无效')
    }
    
    if (!graphData.links || !Array.isArray(graphData.links) || graphData.links.length === 0) {
      throw new Error('知识图谱连接数据无效')
    }
    
    await nextTick()
    
    const graphContainer = document.getElementById('knowledgeGraph')
    if (!graphContainer) {
      throw new Error('知识图谱容器未找到')
    }
    
    // 确保容器尺寸正确
    graphContainer.style.width = '100%'
    graphContainer.style.height = '600px'
    
    // 初始化图表
    disposeChart()
    console.log('初始化 ECharts 实例...')
    knowledgeGraph = echarts.init(graphContainer, 'dark')
    
    const option: EChartsOption = {
      backgroundColor: '#112240',
      title: {
        text: '知识体系',
        left: 'center',
        top: 20,
        textStyle: {
          color: '#64ffda'
        }
      },
      tooltip: {
        trigger: 'item',
        formatter: '{b}: {c}'
      },
      legend: {
        top: 60,
        data: ['领域', '漏洞', '技能', '工具', '技术'],
        textStyle: {
          color: '#8892b0'
        }
      },
      animationDurationUpdate: 1500,
      animationEasingUpdate: 'quinticInOut',
      series: [{
        name: '知识体系',
        type: 'graph',
        layout: 'force',
        force: {
          repulsion: 300,
          edgeLength: 150,
          gravity: 0.1
        },
        roam: true,
        draggable: true,
        label: {
          show: true,
          position: 'right',
          color: '#e6f1ff',
          fontSize: 14
        },
        edgeSymbol: ['circle', 'arrow'],
        edgeSymbolSize: [4, 8],
        edgeLabel: {
          fontSize: 12,
          color: '#8892b0'
        },
        data: graphData.nodes.map(node => ({
          id: String(node.id),
          name: node.name,
          value: node.value,
          symbolSize: node.value * 0.8,
          category: node.category,
          itemStyle: {
            color: node.category === '领域' ? '#64ffda' :
                   node.category === '漏洞' ? '#ff4d4f' :
                   node.category === '技能' ? '#40a9ff' :
                   node.category === '工具' ? '#ffa940' :
                   '#73d13d'
          }
        })),
        links: graphData.links.map(link => ({
          source: String(link.source),
          target: String(link.target),
          value: link.value,
          symbolSize: [4, 8],
          lineStyle: {
            width: link.value / 3,
            curveness: 0.3,
            opacity: 0.7,
            color: '#8892b0'
          }
        })),
        categories: [
          { name: '领域' },
          { name: '漏洞' },
          { name: '技能' },
          { name: '工具' },
          { name: '技术' }
        ],
        emphasis: {
          focus: 'adjacency',
          label: {
            position: 'right',
            show: true,
            fontSize: 16,
            fontWeight: 'bold'
          },
          lineStyle: {
            width: 4
          }
        }
      }]
    }
    
    console.log('设置知识图谱配置:', option)
    knowledgeGraph.setOption(option)
    
    // 添加窗口大小变化监听
    window.addEventListener('resize', handleResize)
    
    ElMessage.success('知识图谱加载成功')
  } catch (err: any) {
    console.error('初始化知识图谱失败:', err)
    error.value = `知识图谱加载失败: ${err.message || '未知错误'}`
    ElMessage.error(`知识图谱加载失败: ${err.message || '未知错误'}`)
  } finally {
    loading.value = false
  }
}

// 处理窗口大小变化
const handleResize = () => {
  if (knowledgeGraph) {
    knowledgeGraph.resize()
  }
}

// 刷新知识图谱
const handleRefresh = () => {
  initKnowledgeGraph()
}

// 组件挂载时加载数据
onMounted(() => {
  initKnowledgeGraph()
})

// 组件卸载时清理资源
onUnmounted(() => {
  disposeChart()
  window.removeEventListener('resize', handleResize)
})

// 添加错误重试功能
const handleRetry = () => {
  initKnowledgeGraph()
}
</script>

<style lang="scss" scoped>
.knowledge-container {
  padding: 20px;
  background: #0a192f;
  min-height: calc(100vh - 84px);
  color: #8892b0;

  .error-alert {
    margin-bottom: 20px;
    
    :deep(.el-alert__content) {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
  }

  .skeleton-content {
    padding: 20px;
  }

  .knowledge-card {
    background: #112240;
    border: 1px solid #1e3a8a;
    
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 16px;
      border-bottom: 1px solid #1e3a8a;

      span {
        font-size: 16px;
        font-weight: bold;
        color: #64ffda;
      }
    }

    .knowledge-content {
      padding: 20px;
      
      .graph-container {
        width: 100%;
        height: 600px;
        min-height: 600px;
      }
    }
  }
}
</style> 