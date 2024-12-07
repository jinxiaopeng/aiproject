import { ref, onUnmounted } from 'vue'
import * as d3 from 'd3'
import type { KnowledgeNode, KnowledgeLink } from '@/api/knowledge'

interface ForceGraphOptions {
  nodeDistance?: number
  centerForce?: number
  collideForce?: number
  chargeForce?: number
}

export function useForceGraph(options: ForceGraphOptions = {}) {
  const {
    nodeDistance = 150,
    centerForce = 0.8,
    collideForce = 0.8,
    chargeForce = -50
  } = options

  const positions = ref<Record<string | number, { x: number; y: number }>>({})
  let simulation: d3.Simulation<any, any> | null = null

  const initializeForceGraph = (nodes: KnowledgeNode[], edges: KnowledgeLink[]) => {
    // 停止之前的模拟（如果存在）
    if (simulation) {
      simulation.stop()
    }

    // 创建力导向图模拟
    simulation = d3.forceSimulation()
      // 中心力 - 将节点拉向中心
      .force('center', d3.forceCenter(0, 0).strength(centerForce))
      // 连接力 - 控制边的长度
      .force('link', d3.forceLink()
        .id((d: any) => d.id)
        .distance(nodeDistance)
        .strength(0.5)
      )
      // 排斥力 - 控制节点间的排斥
      .force('charge', d3.forceManyBody()
        .strength(chargeForce * 5)
        .distanceMax(400)
        .distanceMin(50)
      )
      // 碰撞力 - 防止节点重叠
      .force('collision', d3.forceCollide()
        .radius(45)
        .strength(collideForce)
        .iterations(2)
      )

    // 设置节点和连接
    simulation.nodes(nodes).on('tick', () => {
      // 更新节点位置
      const newPositions: Record<string | number, { x: number; y: number }> = {}
      nodes.forEach((node: any) => {
        // 限制节点位置在更小的范围内
        node.x = Math.max(-300, Math.min(300, node.x))
        node.y = Math.max(-200, Math.min(200, node.y))
        
        // 根据节点类型调整位置
        if (node.category === 'concept') {
          node.y *= 0.9
        } else if (node.category === 'vulnerability') {
          node.x *= 1.1
        }

        newPositions[node.id] = { x: node.x, y: node.y }
      })
      positions.value = newPositions
    })

    // 设置连接力
    const forceLink = simulation.force('link')
    if (forceLink) {
      ;(forceLink as d3.ForceLink<any, any>).links(edges)
    }

    // 设置初始温度（alpha）和降温速度
    simulation
      .alpha(0.8)
      .alphaDecay(0.02)
      .alphaMin(0.001)
      .velocityDecay(0.6)
      .restart()
  }

  const updateForceGraph = (nodes: KnowledgeNode[], edges: KnowledgeLink[]) => {
    if (simulation) {
      // 保持现有节点的位置
      const oldPositions = positions.value
      nodes.forEach(node => {
        const oldPos = oldPositions[node.id]
        if (oldPos) {
          ;(node as any).x = oldPos.x
          ;(node as any).y = oldPos.y
          ;(node as any).vx = 0
          ;(node as any).vy = 0
        } else {
          ;(node as any).x = (Math.random() - 0.5) * 100
          ;(node as any).y = (Math.random() - 0.5) * 100
        }
      })

      // 更新模拟
      simulation.nodes(nodes)
      const forceLink = simulation.force('link')
      if (forceLink) {
        ;(forceLink as d3.ForceLink<any, any>).links(edges)
      }

      // 使用较小的初始温度重新启动
      simulation.alpha(0.2).restart()
    } else {
      initializeForceGraph(nodes, edges)
    }
  }

  onUnmounted(() => {
    if (simulation) {
      simulation.stop()
    }
  })

  return {
    positions,
    initializeForceGraph,
    updateForceGraph
  }
} 