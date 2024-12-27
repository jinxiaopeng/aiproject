<template>
  <div class="graph-renderer">
    <!-- 工具栏 -->
    <div class="graph-toolbar">
      <el-button-group>
        <el-button @click="resetZoom">
          重置视图
        </el-button>
        <el-button @click="zoomIn">
          放大
        </el-button>
        <el-button @click="zoomOut">
          缩小
        </el-button>
      </el-button-group>
    </div>

    <!-- 图例 -->
    <div class="graph-legend">
      <div class="legend-title">图例</div>
      <div class="legend-items">
        <div v-for="category in categories" :key="category.key" class="legend-item">
          <svg width="24" height="24" class="legend-node">
            <circle
              cx="12"
              cy="12"
              r="10"
              :fill="category.color"
              fill-opacity="0.2"
              :stroke="category.color"
              stroke-width="1.5"
            />
          </svg>
          <span>{{ category.label }}</span>
        </div>
      </div>
    </div>

    <!-- SVG容器 -->
    <svg ref="svgEl" class="graph-svg"></svg>

    <!-- 加���状态 -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner"></div>
      <span>加载中...</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { storeToRefs } from 'pinia'
import * as d3 from 'd3'
import { useKnowledgeStore } from '../../store'
import { categories } from '../../mock/data'
import type { KnowledgeNode, KnowledgeLink } from '../../types'
import gsap from 'gsap'

// 类型定义
interface SimulationNode extends d3.SimulationNodeDatum, KnowledgeNode {
  x?: number
  y?: number
  fx?: number | null
  fy?: number | null
  progress?: number
  isRecommended?: boolean
}

interface SimulationLink extends d3.SimulationLinkDatum<SimulationNode> {
  source: string | SimulationNode
  target: string | SimulationNode
  value: number
  type: string
}

interface TreeNode extends d3.HierarchyNode<KnowledgeNode> {
  x: number
  y: number
  data: KnowledgeNode
}

interface TreeLink extends d3.HierarchyLink<KnowledgeNode> {
  source: TreeNode
  target: TreeNode
}

// Props
const props = defineProps<{
  layoutMode: 'force' | 'tree'
}>()

// Emits
const emit = defineEmits<{
  (e: 'node-click', node: KnowledgeNode): void
  (e: 'node-hover', node: KnowledgeNode | null): void
}>()

// Store
const store = useKnowledgeStore()
const { loading: isLoading, hoveredNode, filteredNodes, filteredLinks } = storeToRefs(store)

// Refs
const svgEl = ref<SVGSVGElement>()
let svg: d3.Selection<SVGSVGElement, unknown, null, undefined>
let g: d3.Selection<SVGGElement, unknown, null, undefined>
let simulation: d3.Simulation<SimulationNode, SimulationLink>
let zoom: d3.ZoomBehavior<SVGSVGElement, unknown>

// 初始化SVG和缩放行为
const initSvg = () => {
  if (!svgEl.value) return

  // 清除现有内容
  d3.select(svgEl.value).selectAll('*').remove()

  // 创建SVG和缩放容器
  svg = d3.select(svgEl.value)
  g = svg.append('g')

  // 添加滤镜
  addFilters()

  // 设置缩放行为
  zoom = d3.zoom<SVGSVGElement, unknown>()
    .scaleExtent([0.1, 4])
    .on('zoom', (event) => {
      g.attr('transform', event.transform)
    })

  svg.call(zoom)
  resetZoom()
}

// 重置缩放
const resetZoom = () => {
  if (!svg || !zoom) return
  
  const width = svgEl.value?.clientWidth || 0
  const height = svgEl.value?.clientHeight || 0
  
  svg.transition()
    .duration(750)
    .call(
      zoom.transform,
      d3.zoomIdentity
        .translate(width / 2, height / 2)
        .scale(0.7)
        .translate(-width / 2, -height / 2)
    )
}

// 控制
const zoomIn = () => {
  svg?.transition().call(zoom.scaleBy, 1.5)
}

const zoomOut = () => {
  svg?.transition().call(zoom.scaleBy, 0.75)
}

// 力向布局
const initForceLayout = () => {
  if (!g) return

  // 清除现有内容
  g.selectAll('*').remove()

  const width = svgEl.value?.clientWidth || 0
  const height = svgEl.value?.clientHeight || 0

  // 计算节点层级
  nodeLevels.value = calculateNodeLevels()
  maxLevel.value = Math.max(...Array.from(nodeLevels.value.values()))

  // 准备数据，使用 filteredNodes 和 filteredLinks
  const simulationNodes = filteredNodes.value.map(node => {
    const level = nodeLevels.value.get(String(node.id)) || 0
    const categoryIndex = categories.findIndex(c => c.key === node.category)
    const categoryCount = categories.length
    const angle = (categoryIndex / categoryCount) * 2 * Math.PI
    
    // 根据层级和类别计算初始位置
    const radius = level * 100
    const x = width / 2 + radius * Math.cos(angle)
    const y = height / 2 + radius * Math.sin(angle)
    
    return {
      ...node,
      x: level === 0 ? width / 2 : x,  // 根节点在中心
      y: level === 0 ? height / 2 : y,
      fx: level === 0 ? width / 2 : null,  // 固定根节点位置
      fy: level === 0 ? height / 2 : null,
      progress: learningProgress.value.get(String(node.id)) || 0,
      isRecommended: recommendedPath.value.includes(String(node.id))
    }
  }) as SimulationNode[]

  const simulationLinks = filteredLinks.value.map(link => ({
    ...link,
    source: String(link.source),
    target: String(link.target)
  })) as SimulationLink[]

  // 创建连接线
  const links_g = g.append('g')
    .attr('class', 'links')
    .selectAll('path')
    .data(simulationLinks)
    .enter()
    .append('path')
    .attr('stroke', d => {
      const source = d.source as SimulationNode
      const sourceCategory = categories.find(c => c.key === source.category)
      return sourceCategory?.color || '#4A90E2'
    })
    .attr('stroke-opacity', 0.4)
    .attr('stroke-width', d => Math.sqrt(d.value) + 1)
    .attr('fill', 'none')
    .attr('marker-end', d => {
      const source = d.source as SimulationNode
      const target = d.target as SimulationNode
      const sourceLvl = nodeLevels.value.get(String(source.id)) || 0
      const targetLvl = nodeLevels.value.get(String(target.id)) || 0
      return targetLvl > sourceLvl ? 'url(#arrow)' : null
    })

  // 添加箭头标记
  const defs = svg.append('defs')
  const marker = defs.append('marker')
    .attr('id', 'arrow')
    .attr('viewBox', '0 -5 10 10')
    .attr('refX', 40)
    .attr('refY', 0)
    .attr('markerWidth', 6)
    .attr('markerHeight', 6)
    .attr('orient', 'auto')
    .append('path')
    .attr('d', 'M0,-4L8,0L0,4')
    .attr('fill', '#4A90E2')
    .attr('opacity', 0.6)

  // 创建节点组
  const nodes_g = g.append('g')
    .attr('class', 'nodes')
    .selectAll('g')
    .data(simulationNodes)
    .enter()
    .append('g')
    .attr('class', 'node')

  // 添加节点外圈
  nodes_g.append('circle')
    .attr('r', 35)
    .attr('fill', 'none')
    .attr('stroke', d => {
      const category = categories.find(c => c.key === d.category)
      return category?.color || '#909399'
    })
    .attr('stroke-width', 2)
    .attr('stroke-opacity', 0.6)

  // 添加节点主体
  nodes_g.append('circle')
    .attr('r', 30)
    .attr('fill', d => {
      const category = categories.find(c => c.key === d.category)
      return category?.color || '#909399'
    })
    .attr('fill-opacity', 0.2)
    .attr('stroke', d => {
      const category = categories.find(c => c.key === d.category)
      return category?.color || '#909399'
    })
    .attr('stroke-width', 1.5)

  // 添加进度环
  nodes_g.append('circle')
    .attr('class', 'progress-ring')
    .attr('r', 38)
    .attr('fill', 'none')
    .attr('stroke', '#41b883')
    .attr('stroke-width', 3)
    .attr('stroke-linecap', 'round')
    .attr('transform', 'rotate(-90)')
    .attr('stroke-dasharray', d => {
      const circumference = 2 * Math.PI * 38
      return `${circumference * (d.progress || 0)} ${circumference}`
    })
    .style('opacity', 0.8)

  // 添加推荐标记
  nodes_g.filter((d: SimulationNode) => d.isRecommended === true)
    .append('circle')
    .attr('class', 'recommendation-marker')
    .attr('r', 6)
    .attr('cx', 30)
    .attr('cy', -30)
    .attr('fill', '#ffd04b')
    .attr('stroke', '#fff')
    .attr('stroke-width', 2)

  // 添加节点文本
  nodes_g.append('text')
    .text(d => d.name)
    .attr('text-anchor', 'middle')
    .attr('dy', '0.3em')
    .attr('fill', '#e5eaf3')
    .attr('font-size', '12px')
    .attr('font-weight', 'bold')

  // 设置事件处理
  nodes_g
    .on('click', (event: MouseEvent, d: SimulationNode) => {
      event.stopPropagation()
      toggleNode(d)
      emit('node-click', d)
    })
    .on('mouseenter', (event: MouseEvent, d: SimulationNode) => {
      gsap.to(event.currentTarget, {
        duration: 0.3,
        scale: 1.1,
        ease: 'back.out(1.5)'
      })
      emit('node-hover', d)
    })
    .on('mouseleave', (event: MouseEvent, d: SimulationNode) => {
      gsap.to(event.currentTarget, {
        duration: 0.3,
        scale: 1,
        ease: 'back.out(1.5)'
      })
      emit('node-hover', null)
    })

  // 创建力导向布局
  simulation = d3.forceSimulation<SimulationNode>(simulationNodes)
    .force('link', d3.forceLink<SimulationNode, SimulationLink>(simulationLinks)
      .id(d => String(d.id))
      .distance(d => {
        const source = d.source as SimulationNode
        const target = d.target as SimulationNode
        const sourceLvl = nodeLevels.value.get(String(source.id)) || 0
        const targetLvl = nodeLevels.value.get(String(target.id)) || 0
        const levelDiff = Math.abs(sourceLvl - targetLvl)
        const sameCategory = source.category === target.category
        
        // 优化节点间距
        const baseDistance = sameCategory ? 250 : 300
        return baseDistance + levelDiff * 50
      })
      .strength(d => {
        const source = d.source as SimulationNode
        const target = d.target as SimulationNode
        const sourceLvl = nodeLevels.value.get(String(source.id)) || 0
        const targetLvl = nodeLevels.value.get(String(target.id)) || 0
        
        if (sourceLvl === 0 || targetLvl === 0) {
          return 0.5  // 降低与根节点的连接强度
        }
        return Math.abs(sourceLvl - targetLvl) === 1 ? 0.3 : 0.1
      })
    )
    .force('charge', d3.forceManyBody<SimulationNode>()
      .strength(d => {
        const level = nodeLevels.value.get(String(d.id)) || 0
        // 增加排斥力
        return -500 * Math.pow(0.8, level)
      })
      .distanceMin(180)
      .distanceMax(700)
    )
    .force('collide', d3.forceCollide<SimulationNode>()
      .radius(d => {
        const level = nodeLevels.value.get(String(d.id)) || 0
        // 调整碰撞检测半径
        return 50 - level * 2
      })
      .strength(0.8)
      .iterations(4)
    )
    .force('radial', d3.forceRadial<SimulationNode>(
      d => {
        const level = nodeLevels.value.get(String(d.id)) || 0
        // 调整径向力半径
        return level * 200
      },
      width / 2,
      height / 2
    ).strength(0.8))
    .force('angular', (alpha: number) => {
      // 自定义力，使同类节点在同一方向
      const centerX = width / 2
      const centerY = height / 2
      simulationNodes.forEach(node => {
        if (!node.x || !node.y) return
        const level = nodeLevels.value.get(String(node.id)) || 0
        if (level === 0) return // 跳过根节点
        
        const categoryIndex = categories.findIndex(c => c.key === node.category)
        const categoryCount = categories.length
        
        // 计算目标角度（根据类别）
        const targetAngle = (categoryIndex / categoryCount) * 2 * Math.PI
        
        // 计算当前角度
        const dx = node.x - centerX
        const dy = node.y - centerY
        const currentAngle = Math.atan2(dy, dx)
        
        // 计算角度差
        let deltaAngle = targetAngle - currentAngle
        if (deltaAngle > Math.PI) deltaAngle -= 2 * Math.PI
        if (deltaAngle < -Math.PI) deltaAngle += 2 * Math.PI
        
        // 施加角度力
        const distance = Math.sqrt(dx * dx + dy * dy)
        const force = distance * alpha * 0.3
        node.vx! += Math.cos(currentAngle + deltaAngle) * force
        node.vy! += Math.sin(currentAngle + deltaAngle) * force
      })
    })
    .alphaDecay(0.01) // 减缓衰减速度
    .velocityDecay(0.35) // 增加阻尼，使运动更稳定
    .on('tick', () => {
      links_g
        .attr('d', d => {
          const source = d.source as SimulationNode
          const target = d.target as SimulationNode
          const sourceLvl = nodeLevels.value.get(String(source.id)) || 0
          const targetLvl = nodeLevels.value.get(String(target.id)) || 0
          
          // 计算控制点
          const dx = target.x! - source.x!
          const dy = target.y! - source.y!
          const dr = Math.sqrt(dx * dx + dy * dy)
          
          // 根据节点层级关系调整曲线弧度
          const curvature = sourceLvl >= targetLvl ? 2 : 1.2
          
          // 使用二次贝塞尔曲线，让连线更平滑
          const midX = (source.x! + target.x!) / 2
          const midY = (source.y! + target.y!) / 2
          const normalX = -dy / dr
          const normalY = dx / dr
          const controlX = midX + normalX * dr * curvature * 0.2
          const controlY = midY + normalY * dr * curvature * 0.2
          
          return `M${source.x},${source.y} Q${controlX},${controlY} ${target.x},${target.y}`
        })

      nodes_g
        .attr('transform', d => `translate(${d.x || 0},${d.y || 0})`)
    })

  // 添加拖拽行为
  nodes_g.call(d3.drag<SVGGElement, SimulationNode>()
    .on('start', (event: d3.D3DragEvent<SVGGElement, SimulationNode, SimulationNode>) => {
      if (!event.active) simulation.alphaTarget(0.3).restart()
      event.subject.fx = event.subject.x
      event.subject.fy = event.subject.y
    })
    .on('drag', (event: d3.D3DragEvent<SVGGElement, SimulationNode, SimulationNode>) => {
      event.subject.fx = event.x
      event.subject.fy = event.y
    })
    .on('end', (event: d3.D3DragEvent<SVGGElement, SimulationNode, SimulationNode>) => {
      if (!event.active) simulation.alphaTarget(0)
      event.subject.fx = null
      event.subject.fy = null
    })
  )

  // 调用添加层级指示器函数
  addLevelIndicators(width, height)

  // 添加节点发光效果
  nodes_g.append('circle')
    .attr('class', 'node-glow')
    .attr('r', 40)
    .attr('fill', 'none')
    .attr('stroke', d => {
      const category = categories.find(c => c.key === d.category)
      return category?.color || '#909399'
    })
    .attr('stroke-width', 2)
    .attr('filter', 'url(#glow)')
    .attr('opacity', 0.3)
}

// 树形布局
const initTreeLayout = () => {
  if (!g) return

  // 清除现有内容
  g.selectAll('*').remove()

  // 获取容器尺寸
  const width = svgEl.value?.clientWidth || 0
  const height = svgEl.value?.clientHeight || 0

  // 找到根节点（没有前置知识的节点）
  const rootNodes = filteredNodes.value.filter(node => !node.prerequisites?.length)
  if (!rootNodes.length) return

  // 使用第一个根节点作为主根节点
  const rootNode = rootNodes[0]

  // 创建层级数据
  const createHierarchy = (node: KnowledgeNode, visited = new Set<string>()): d3.HierarchyNode<KnowledgeNode> => {
    visited.add(String(node.id))
    
    // 找出所有以当前节点为前置条件的节点
    const children = filteredNodes.value.filter(n => 
      n.prerequisites?.includes(node.id) && !visited.has(String(n.id))
    )
    
    return d3.hierarchy(node, n => {
      if (n === node) {
        return children
      }
      // 对于子节点，递归构建层级
      return filteredNodes.value.filter(child => 
        child.prerequisites?.includes(n.id) && !visited.has(String(child.id))
      )
    })
  }

  try {
    // 创建层级结构
    const root = createHierarchy(rootNode)
      .sort((a, b) => (a.data.name).localeCompare(b.data.name))

    // 创建树形布局
    const treeLayout = d3.tree<KnowledgeNode>()
      .size([height * 0.9, width * 0.9])
      .nodeSize([60, 150])
      .separation((a, b) => {
        if (a.parent === b.parent) {
          return a.data.category === b.data.category ? 1.2 : 1.8
        }
        return a.depth === b.depth ? 2 : 2.5
      })

    // 计算节点位置
    const tree = treeLayout(root)

    // 平移整个树以居中显示
    const bounds = tree.descendants().reduce(
      (bounds, node) => {
        bounds.minX = Math.min(bounds.minX, node.x)
        bounds.maxX = Math.max(bounds.maxX, node.x)
        bounds.minY = Math.min(bounds.minY, node.y)
        bounds.maxY = Math.max(bounds.maxY, node.y)
        return bounds
      },
      { minX: Infinity, maxX: -Infinity, minY: Infinity, maxY: -Infinity }
    )

    const offsetX = (width - (bounds.maxY - bounds.minY)) / 2 - bounds.minY
    const offsetY = (height - (bounds.maxX - bounds.minX)) / 2 - bounds.minX

    // 更新节点和连接线位置
    g.attr('transform', `translate(${offsetX},${offsetY})`)

    // 创建所有可能的连接线
    const allLinks = [] as { source: TreeNode, target: TreeNode }[]
    tree.descendants().forEach(node => {
      const nodeId = node.data.id
      // 找出所有以当前节点为前置条件的节点
      const nextNodes = tree.descendants().filter(n => 
        n.data.prerequisites?.includes(nodeId)
      )
      nextNodes.forEach(target => {
        allLinks.push({
          source: node as TreeNode,
          target: target as TreeNode
        })
      })
    })

    // 创建连接线
    g.append('g')
      .attr('class', 'links')
      .selectAll('path')
      .data(allLinks)
      .enter()
      .append('path')
      .attr('d', d3.linkHorizontal<any, any>()
        .x(d => d.y)
        .y(d => d.x)
      )
      .attr('fill', 'none')
      .attr('stroke', '#2f3699')
      .attr('stroke-opacity', 0.6)
      .attr('stroke-width', 1)

    // 创建节点组
    const nodes_g = g.append('g')
      .attr('class', 'nodes')
      .selectAll('g')
      .data(tree.descendants())
      .enter()
      .append('g')
      .attr('class', 'node')
      .attr('transform', d => `translate(${d.y},${d.x})`)

    // 添加节点外圈
    nodes_g.append('circle')
      .attr('r', 25)
      .attr('fill', 'none')
      .attr('stroke', d => {
        const category = categories.find(c => c.key === d.data.category)
        return category?.color || '#909399'
      })
      .attr('stroke-width', 2)
      .attr('stroke-opacity', 0.6)

    // 添加节点主体
    nodes_g.append('circle')
      .attr('r', 20)
      .attr('fill', d => {
        const category = categories.find(c => c.key === d.data.category)
        return category?.color || '#909399'
      })
      .attr('fill-opacity', 0.2)
      .attr('stroke', d => {
        const category = categories.find(c => c.key === d.data.category)
        return category?.color || '#909399'
      })
      .attr('stroke-width', 1.5)

    // 添加节点文本
    nodes_g.append('text')
      .text(d => d.data.name)
      .attr('text-anchor', 'middle')
      .attr('dy', '0.3em')
      .attr('fill', '#e5eaf3')
      .attr('font-size', '12px')

    // 设置事件处理
    nodes_g
      .on('click', (event: MouseEvent, d: d3.HierarchyNode<KnowledgeNode>) => {
        event.stopPropagation()
        emit('node-click', d.data)
      })
      .on('mouseenter', (event: MouseEvent, d: d3.HierarchyNode<KnowledgeNode>) => {
        emit('node-hover', d.data)
      })
      .on('mouseleave', () => {
        emit('node-hover', null)
      })
  } catch (error) {
    console.error('Failed to create tree layout:', error)
  }
}

// 监听布局模式变化
watch(() => props.layoutMode, () => {
  if (props.layoutMode === 'force') {
    initForceLayout()
  } else {
    initTreeLayout()
  }
})

// 监听数据变化
watch([filteredNodes, filteredLinks], () => {
  if (props.layoutMode === 'force') {
    initForceLayout()
  } else {
    initTreeLayout()
  }
}, { deep: true })

// 监听窗口大小变化
const handleResize = () => {
  if (props.layoutMode === 'force') {
    initForceLayout()
  } else {
    initTreeLayout()
  }
}

// 生命周期钩子
onMounted(() => {
  initSvg()
  if (props.layoutMode === 'force') {
    initForceLayout()
  } else {
    initTreeLayout()
  }
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  simulation?.stop()
})

// 在 setup 中添加新的响应式变量
const expandedNodes = ref(new Set<string>())
const visibleNodes = ref(new Set<string>())
const visibleLinks = ref(new Set<string>())
const learningProgress = ref(new Map<string, number>())
const recommendedPath = ref<string[]>([])
const nodeLevels = ref(new Map<string, number>())
const maxLevel = ref(0)

// 计算层级的函数
const calculateNodeLevels = () => {
  const levels = new Map<string, number>()
  const visited = new Set<string>()
  
  // 找出所有没有前置依赖的节点（根节点）
  const roots = filteredNodes.value.filter(node => node.prerequisites.length === 0)
  
  // 使用BFS计算每个节点的层级
  const queue: { node: KnowledgeNode; level: number }[] = roots.map(node => ({ node, level: 0 }))
  
  while (queue.length > 0) {
    const { node, level } = queue.shift()!
    const nodeId = String(node.id)
    
    if (visited.has(nodeId)) {
      // 如果节点已访问，更新为最大层级
      levels.set(nodeId, Math.max(levels.get(nodeId) || 0, level))
      continue
    }
    
    visited.add(nodeId)
    levels.set(nodeId, level)
    
    // 找出所有以当前节点为前置条件的节点
    const nextNodes = filteredNodes.value.filter(n => 
      n.prerequisites.includes(node.id)
    )
    
    // 将这些节点加入队列
    nextNodes.forEach(nextNode => {
      // 检查所有前置条件是否都已处理
      const allPrerequisitesProcessed = nextNode.prerequisites.every(preId =>
        visited.has(String(preId))
      )
      
      if (allPrerequisitesProcessed) {
        queue.push({ node: nextNode, level: level + 1 })
      }
    })
  }
  
  return levels
}

// 添加层级指示器函数
const addLevelIndicators = (svgWidth: number, svgHeight: number) => {
  const levelGroups = Array.from(new Set(Array.from(nodeLevels.value.values())))
  maxLevel.value = Math.max(...levelGroups)
  
  // 为每层级添加形指示器
  levelGroups.forEach(level => {
    const radius = svgWidth * (0.15 + (level / maxLevel.value) * 0.7)
    const nodesInLevel = Array.from(nodeLevels.value.entries())
      .filter(([_, l]) => l === level)
      .map(([id]) => id)
    
    if (nodesInLevel.length > 0) {
      g.append('circle')
        .attr('class', 'level-indicator')
        .attr('cx', radius)
        .attr('cy', svgHeight / 2)
        .attr('r', 120 + level * 40)
        .attr('fill', 'none')
        .attr('stroke', '#2f3699')
        .attr('stroke-width', 1)
        .attr('stroke-dasharray', '5,5')
        .attr('stroke-opacity', 0.2)
    }
  })
}

// 添加节点展开/收起处理函数
const toggleNode = (node: SimulationNode) => {
  const nodeId = String(node.id)
  const isExpanded = expandedNodes.value.has(nodeId)
  
  if (isExpanded) {
    // 收起节点
    expandedNodes.value.delete(nodeId)
    visibleNodes.value.clear()
    visibleLinks.value.clear()
    
    // 恢复所有节点和��接线
    g?.selectAll<SVGGElement, SimulationNode>('.node')
      .transition()
      .duration(500)
      .style('opacity', 1)
      .style('filter', 'none')

    g?.selectAll<SVGPathElement, SimulationLink>('path')
      .transition()
      .duration(500)
      .style('opacity', 0.3)
      .attr('stroke', d => {
        const source = d.source as SimulationNode
        const sourceCategory = categories.find(c => c.key === source.category)
        return sourceCategory?.color || '#2f3699'
      })
      .attr('stroke-width', d => Math.sqrt(d.value))

    // 移除特效元素
    g?.selectAll('.glow, .ripple').remove()
  } else {
    // 展开节点
    expandedNodes.value.add(nodeId)
    
    // 找出相关节点和连接
    const relatedLinks = filteredLinks.value.filter(link => 
      String(link.source) === nodeId || String(link.target) === nodeId
    )
    const relatedNodes = new Set<string>()
    relatedLinks.forEach(link => {
      relatedNodes.add(String(link.source))
      relatedNodes.add(String(link.target))
      visibleLinks.value.add(`${link.source}-${link.target}`)
    })
    visibleNodes.value = relatedNodes

    // 淡化非相关节点
    g?.selectAll<SVGGElement, SimulationNode>('.node')
      .transition()
      .duration(500)
      .style('opacity', (d: SimulationNode) => visibleNodes.value.has(String(d.id)) ? 1 : 0.2)

    // 高亮相关节点
    g?.selectAll<SVGGElement, SimulationNode>('.node')
      .filter((d: SimulationNode) => visibleNodes.value.has(String(d.id)))
      .each(function(this: SVGGElement) {
        const node = d3.select(this)
        
        // 添加发光效果
        node.append('circle')
          .attr('class', 'glow')
          .attr('r', 45)
          .attr('fill', 'none')
          .attr('stroke', '#41b883')
          .attr('stroke-width', 2)
          .attr('stroke-opacity', 0)
          .transition()
          .duration(500)
          .attr('stroke-opacity', 0.5)

        // 添加波纹效果
        node.append('circle')
          .attr('class', 'ripple')
          .attr('r', 35)
          .attr('fill', 'none')
          .attr('stroke', '#41b883')
          .attr('stroke-width', 2)
          .attr('stroke-opacity', 0.8)
          .transition()
          .duration(2000)
          .attr('r', 60)
          .attr('stroke-opacity', 0)
          .remove()
      })

    // 高亮连接线
    g?.selectAll<SVGPathElement, SimulationLink>('path')
      .filter((d: SimulationLink) => {
        const sourceId = typeof d.source === 'string' ? d.source : d.source.id
        const targetId = typeof d.target === 'string' ? d.target : d.target.id
        // 只对与点击节点直接相连的连接线应用动画
        return String(sourceId) === nodeId || String(targetId) === nodeId
      })
      .each(function(this: SVGPathElement) {
        const path = d3.select(this)
        const pathLength = (this as SVGGeometryElement).getTotalLength()
        
        // 设置原始路径样式
        path
          .attr('stroke', '#41b883')
          .attr('stroke-width', 4)
          .style('opacity', 0.8)
          .attr('filter', 'url(#glow)')

        // 创建动画效果路径
        const animPath = path.clone()
          .attr('class', 'link-animation')
          .attr('stroke', '#41b883')
          .attr('stroke-width', 6)
          .style('opacity', 0)
          .lower()

        // 创建光效路径
        const glowPath = path.clone()
          .attr('class', 'link-glow')
          .attr('stroke', '#fff')
          .attr('stroke-width', 8)
          .style('opacity', 0)
          .attr('filter', 'url(#glow)')
          .lower()

        // 光效动画
        glowPath
          .attr('stroke-dasharray', `0 ${pathLength}`)
          .transition()
          .duration(600)
          .ease(d3.easeQuadIn)
          .style('opacity', 0.4)
          .attr('stroke-dasharray', `${pathLength * 0.2} ${pathLength}`)
          .attr('stroke-dashoffset', pathLength)
          .transition()
          .duration(1000)
          .ease(d3.easeQuadOut)
          .attr('stroke-dashoffset', 0)
          .style('opacity', 0)
          .remove()

        // 主动画路径
        animPath
          .attr('stroke-dasharray', `0 ${pathLength}`)
          .transition()
          .duration(600)
          .ease(d3.easeQuadIn)
          .style('opacity', 1)
          .attr('stroke-dasharray', `${pathLength} ${pathLength}`)
          .attr('stroke-dashoffset', pathLength)
          .transition()
          .duration(1000)
          .ease(d3.easeQuadOut)
          .attr('stroke-dashoffset', 0)
          .style('opacity', 0)
          .remove()

        // 原始路径动画
        path
          .attr('stroke-dasharray', `${pathLength} ${pathLength}`)
          .attr('stroke-dashoffset', pathLength)
          .transition()
          .duration(1200)
          .ease(d3.easeCubicOut)
          .attr('stroke-dashoffset', 0)
          .transition()
          .duration(300)
          .attr('stroke-dasharray', null)
      })

    // 高亮其他相关连接线（不带动画）
    g?.selectAll<SVGPathElement, SimulationLink>('path')
      .filter((d: SimulationLink) => {
        const sourceId = typeof d.source === 'string' ? d.source : d.source.id
        const targetId = typeof d.target === 'string' ? d.target : d.target.id
        const linkId = `${sourceId}-${targetId}`
        // 只高亮可见的连接线，但排除与点击节点直接相连的连接线
        return visibleLinks.value.has(linkId) && 
               String(sourceId) !== nodeId && 
               String(targetId) !== nodeId
      })
      .transition()
      .duration(500)
      .attr('stroke', '#41b883')
      .attr('stroke-width', 3)
      .style('opacity', 0.6)
  }
}

// 添加 createNodes 函数
const createNodes = (g: d3.Selection<SVGGElement, unknown, null, undefined>, nodes: SimulationNode[]) => {
  return g.append('g')
    .attr('class', 'nodes')
    .selectAll('g')
    .data(nodes)
    .enter()
    .append('g')
    .attr('class', 'node')
}

// 添加 addFilters 函数
const addFilters = () => {
  const defs = svg.append('defs')
  
  // 添加发光滤镜
  const filter = defs.append('filter')
    .attr('id', 'glow')
    .attr('x', '-50%')
    .attr('y', '-50%')
    .attr('width', '200%')
    .attr('height', '200%')
  
  filter.append('feGaussianBlur')
    .attr('stdDeviation', '3')
    .attr('result', 'coloredBlur')
  
  const feMerge = filter.append('feMerge')
  feMerge.append('feMergeNode')
    .attr('in', 'coloredBlur')
  feMerge.append('feMergeNode')
    .attr('in', 'SourceGraphic')

  // 添加连接线动画渐变
  const linkGradient = defs.append('linearGradient')
    .attr('id', 'linkGradient')
    .attr('gradientUnits', 'userSpaceOnUse')
  
  linkGradient.append('stop')
    .attr('offset', '0%')
    .attr('stop-color', '#41b883')
    .attr('stop-opacity', 1)
  
  linkGradient.append('stop')
    .attr('offset', '50%')
    .attr('stop-color', '#3eaf7c')
    .attr('stop-opacity', 0.8)
  
  linkGradient.append('stop')
    .attr('offset', '100%')
    .attr('stop-color', '#41b883')
    .attr('stop-opacity', 1)

  // 添加连接线流动效果滤镜
  const flowFilter = defs.append('filter')
    .attr('id', 'flow')
    .attr('x', '-50%')
    .attr('y', '-50%')
    .attr('width', '200%')
    .attr('height', '200%')
  
  flowFilter.append('feGaussianBlur')
    .attr('in', 'SourceGraphic')
    .attr('stdDeviation', '2')
    .attr('result', 'blur')
  
  flowFilter.append('feColorMatrix')
    .attr('in', 'blur')
    .attr('mode', 'matrix')
    .attr('values', '1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 18 -7')
    .attr('result', 'glow')
  
  const feMerge2 = flowFilter.append('feMerge')
  feMerge2.append('feMergeNode').attr('in', 'glow')
  feMerge2.append('feMergeNode').attr('in', 'SourceGraphic')
}

// 添加新的样式
const style = document.createElement('style')
style.textContent = `
.graph-renderer {
  position: relative;
  width: 100%;
  height: 100%;
  background-color: #1a1a1a;
  overflow: hidden;
}

.graph-svg {
  width: 100%;
  height: 100%;
}

.graph-toolbar {
  position: absolute;
  top: 20px;
  left: 20px;
  z-index: 10;
}

.graph-legend {
  position: absolute;
  top: 20px;
  right: 20px;
  background-color: rgba(0, 0, 0, 0.7);
  padding: 15px;
  border-radius: 8px;
  z-index: 10;
}

.legend-title {
  color: #e5eaf3;
  font-size: 14px;
  margin-bottom: 10px;
}

.legend-items {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #e5eaf3;
  font-size: 12px;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: #e5eaf3;
  gap: 15px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid transparent;
  border-top-color: #41b883;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.node.highlighted {
  filter: drop-shadow(0 0 8px rgba(65, 184, 131, 0.4));
}

.glow {
  pointer-events: none;
  mix-blend-mode: screen;
}

.ripple {
  pointer-events: none;
  mix-blend-mode: screen;
}

@keyframes flow {
  from {
    stroke-dashoffset: 20;
  }
  to {
    stroke-dashoffset: 0;
  }
}

line.highlighted {
  animation: flow 1s linear infinite;
}

.node-glow {
  transition: opacity 0.3s ease;
}

.node:hover .node-glow {
  opacity: 0.6;
}

.level-indicator {
  transition: opacity 0.3s ease;
}

.level-indicator:hover {
  opacity: 0.4;
}

path.link {
  transition: stroke-opacity 0.3s ease;
}

path.link:hover {
  stroke-opacity: 0.8;
}

path.link {
  transition: all 0.3s ease;
  cursor: pointer;
}

path.link:hover {
  stroke-opacity: 0.8;
  stroke-width: 3;
  filter: drop-shadow(0 0 3px rgba(47, 54, 153, 0.5));
}

.link-animation {
  pointer-events: none;
  mix-blend-mode: screen;
}

path.link {
  transition: all 0.3s ease;
  cursor: pointer;
}

path.link:hover {
  stroke-opacity: 0.8;
  stroke-width: 4;
  filter: url(#flow);
}
`
document.head.appendChild(style)
</script>

<style lang="scss" scoped>
.graph-renderer {
  width: 100%;
  height: 100%;
  position: relative;
  background: linear-gradient(135deg, #1a1f25 0%, #17212b 100%);
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: 
      radial-gradient(circle at 50% 50%, rgba(45, 85, 115, 0.1) 0%, transparent 60%),
      radial-gradient(circle at 85% 15%, rgba(45, 85, 115, 0.15) 0%, transparent 50%),
      radial-gradient(circle at 15% 85%, rgba(45, 85, 115, 0.15) 0%, transparent 50%);
    pointer-events: none;
  }

  .graph-svg {
    width: 100%;
    height: 100%;
    position: relative;
    z-index: 1;
  }

  // 添加网格背景
  &::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: 
      linear-gradient(rgba(65, 184, 131, 0.05) 1px, transparent 1px),
      linear-gradient(90deg, rgba(65, 184, 131, 0.05) 1px, transparent 1px);
    background-size: 30px 30px;
    pointer-events: none;
    opacity: 0.3;
  }
}
</style> 