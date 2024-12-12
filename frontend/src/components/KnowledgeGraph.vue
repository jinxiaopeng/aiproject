<template>
  <div class="knowledge-graph">
    <div class="graph-controls">
      <el-select v-model="displayMode" placeholder="选择显示模式">
        <el-option label="3D 力导向图" value="3d" />
        <el-option label="2D 力导向图" value="2d" />
      </el-select>
      <el-select v-model="filterType" placeholder="筛选类型" multiple>
        <el-option label="知识点" value="knowledge" />
        <el-option label="攻击类型" value="attack" />
        <el-option label="漏洞" value="vulnerability" />
      </el-select>
      <el-button @click="resetCamera">重置视角</el-button>
    </div>
    
    <div ref="graphContainer" class="graph-container"></div>
    
    <el-drawer
      v-model="showNodeDetail"
      title="节点详情"
      size="30%"
      :with-header="true"
    >
      <template v-if="selectedNode">
        <div class="node-detail">
          <h3>{{ selectedNode.name }}</h3>
          <p>{{ selectedNode.description }}</p>
          
          <template v-if="selectedNode.type === 'knowledge'">
            <h4>关键点</h4>
            <ul>
              <li v-for="point in selectedNode.key_points" :key="point">
                {{ point }}
              </li>
            </ul>
            
            <h4>学习进度</h4>
            <el-progress 
              :percentage="getLearningProgress(selectedNode.id)"
              :status="getLearningStatus(selectedNode.id)"
            />
            
            <h4>相关资源</h4>
            <div v-if="selectedNode.resources">
              <div v-for="group in selectedNode.resources" :key="group.type">
                <h5>{{ group.type }}</h5>
                <ul>
                  <li v-for="item in group.items" :key="item.url">
                    <a :href="item.url" target="_blank">{{ item.name }}</a>
                  </li>
                </ul>
              </div>
            </div>
          </template>
          
          <template v-if="selectedNode.type === 'attack'">
            <h4>影响范围</h4>
            <p>{{ selectedNode.impact }}</p>
            
            <h4>应对措施</h4>
            <p>{{ selectedNode.mitigation }}</p>
          </template>
          
          <template v-if="selectedNode.type === 'vulnerability'">
            <h4>CVE 编号</h4>
            <p>{{ selectedNode.cve_id }}</p>
            
            <h4>严重性</h4>
            <el-tag :type="getSeverityType(selectedNode.severity)">
              {{ selectedNode.severity }}
            </el-tag>
            
            <h4>受影响系统</h4>
            <ul>
              <li v-for="sys in selectedNode.affected_systems" :key="sys">
                {{ sys }}
              </li>
            </ul>
            
            <h4>修复方案</h4>
            <p>{{ selectedNode.solution }}</p>
          </template>
          
          <div class="feedback-section">
            <h4>提供反馈</h4>
            <el-rate v-model="feedback.rating" />
            <el-input
              v-model="feedback.comment"
              type="textarea"
              placeholder="请输入您的反馈..."
            />
            <el-button type="primary" @click="submitFeedback">
              提交反馈
            </el-button>
          </div>
        </div>
      </template>
    </el-drawer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useKnowledgeStore } from '@/stores/knowledge'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'
import { CSS2DRenderer, CSS2DObject } from 'three/examples/jsm/renderers/CSS2DRenderer'
import ForceGraph3D from '3d-force-graph'
import type { GraphNode, GraphLink } from '@/api/knowledge'

const store = useKnowledgeStore()
const graphContainer = ref<HTMLElement>()
const graph = ref<any>(null)
const displayMode = ref('3d')
const filterType = ref(['knowledge', 'attack', 'vulnerability'])
const showNodeDetail = ref(false)
const selectedNode = ref<GraphNode | null>(null)
const feedback = ref({
  rating: 0,
  comment: ''
})

// 初始化图谱
onMounted(async () => {
  await store.fetchAllData()
  await store.getGraph()
  initGraph()
})

// 监听显示模式变化
watch(displayMode, () => {
  if (graph.value) {
    graph.value.dispose()
    initGraph()
  }
})

// 监听过滤器变化
watch(filterType, () => {
  if (store.graph) {
    updateGraphData()
  }
})

// 初始化图谱
const initGraph = () => {
  if (!graphContainer.value || !store.graph) return
  
  if (displayMode.value === '3d') {
    init3DGraph()
  } else {
    init2DGraph()
  }
  
  updateGraphData()
}

// 初始化3D图谱
const init3DGraph = () => {
  graph.value = ForceGraph3D()(graphContainer.value)
    .nodeLabel('name')
    .nodeColor(node => getNodeColor(node.type))
    .nodeVal(node => node.value)
    .linkWidth(link => link.value)
    .linkColor(() => '#999')
    .onNodeClick(handleNodeClick)
    .onNodeDragEnd(node => {
      node.fx = node.x
      node.fy = node.y
      node.fz = node.z
    })
}

// 初始化2D图谱
const init2DGraph = () => {
  // 使用 D3.js 实现2D力导向图
  // ... 2D图谱实现代码 ...
}

// 更新图谱数据
const updateGraphData = () => {
  if (!store.graph) return
  
  const filteredNodes = store.graph.nodes.filter(node => 
    filterType.value.includes(node.type)
  )
  
  const filteredLinks = store.graph.links.filter(link => {
    const sourceNode = store.graph?.nodes.find(n => n.id === link.source)
    const targetNode = store.graph?.nodes.find(n => n.id === link.target)
    return sourceNode && targetNode && 
           filterType.value.includes(sourceNode.type) && 
           filterType.value.includes(targetNode.type)
  })
  
  graph.value.graphData({
    nodes: filteredNodes,
    links: filteredLinks
  })
}

// 获取节点颜色
const getNodeColor = (type: string) => {
  switch (type) {
    case 'knowledge':
      return '#1f77b4'
    case 'attack':
      return '#d62728'
    case 'vulnerability':
      return '#ff7f0e'
    default:
      return '#999'
  }
}

// 获取严重性标签类型
const getSeverityType = (severity: string) => {
  switch (severity) {
    case 'high':
      return 'danger'
    case 'medium':
      return 'warning'
    case 'low':
      return 'info'
    default:
      return ''
  }
}

// 获取学习进度
const getLearningProgress = (nodeId: number) => {
  const record = store.learningRecords.find(r => r.knowledge_point_id === nodeId)
  return record?.progress || 0
}

// 获取学习状态
const getLearningStatus = (nodeId: number) => {
  const record = store.learningRecords.find(r => r.knowledge_point_id === nodeId)
  return record?.status || 'not_started'
}

// 处理节点点击
const handleNodeClick = (node: GraphNode) => {
  selectedNode.value = node
  showNodeDetail.value = true
}

// 重置相机位置
const resetCamera = () => {
  if (displayMode.value === '3d') {
    graph.value.cameraPosition({ x: 0, y: 0, z: 1000 }, { x: 0, y: 0, z: 0 }, 1000)
  } else {
    // 重置2D视图
  }
}

// 提交反馈
const submitFeedback = async () => {
  if (!selectedNode.value) return
  
  await store.submitFeedback({
    knowledge_point_id: selectedNode.value.id,
    rating: feedback.value.rating,
    comment: feedback.value.comment
  })
  
  feedback.value = {
    rating: 0,
    comment: ''
  }
}
</script>

<style scoped>
.knowledge-graph {
  width: 100%;
  height: 100%;
  position: relative;
}

.graph-controls {
  position: absolute;
  top: 20px;
  left: 20px;
  z-index: 1;
  display: flex;
  gap: 10px;
}

.graph-container {
  width: 100%;
  height: 100%;
}

.node-detail {
  padding: 20px;
}

.node-detail h3 {
  margin-top: 0;
  margin-bottom: 16px;
}

.node-detail h4 {
  margin-top: 20px;
  margin-bottom: 10px;
}

.feedback-section {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.feedback-section .el-rate {
  margin-bottom: 16px;
}

.feedback-section .el-button {
  margin-top: 16px;
}
</style> 