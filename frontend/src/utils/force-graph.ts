import type { KnowledgeNode, KnowledgeLink } from '@/api/knowledge'

interface ForceGraphOptions {
  nodes: KnowledgeNode[]
  edges: KnowledgeLink[]
  width: number
  height: number
  onTick: (positions: Record<string, { x: number; y: number }>) => void
}

export class ForceGraph {
  private nodes: KnowledgeNode[]
  private edges: KnowledgeLink[]
  private width: number
  private height: number
  private onTick: (positions: Record<string, { x: number; y: number }>) => void
  private positions: Record<string, { x: number; y: number; vx: number; vy: number }>
  private animationId: number | null = null
  private isRunning: boolean = false

  constructor(options: ForceGraphOptions) {
    console.log('ForceGraph initialized with:', {
      nodes: options.nodes.length,
      edges: options.edges.length,
      width: options.width,
      height: options.height
    })

    this.nodes = options.nodes
    this.edges = options.edges
    this.width = options.width
    this.height = options.height
    this.onTick = options.onTick
    this.positions = {}
    
    this.initPositions()
    this.startSimulation()
  }

  private initPositions() {
    console.log('Initializing positions for nodes:', this.nodes.length)
    
    // 计算布局区域
    const margin = 150
    const availableWidth = this.width - 2 * margin
    const availableHeight = this.height - 2 * margin
    
    // 使用圆形布局初始化节点位置
    const radius = Math.min(availableWidth, availableHeight) / 3
    const centerX = this.width / 2
    const centerY = this.height / 2
    
    this.nodes.forEach((node, i) => {
      const angle = (i / this.nodes.length) * 2 * Math.PI
      this.positions[node.id] = {
        x: centerX + radius * Math.cos(angle),
        y: centerY + radius * Math.sin(angle),
        vx: 0,
        vy: 0
      }
    })
    
    console.log('Initial positions:', this.positions)
  }

  private startSimulation() {
    if (this.isRunning) {
      console.log('Simulation already running')
      return
    }
    
    console.log('Starting force simulation')
    this.isRunning = true
    
    let iteration = 0
    const tick = () => {
      if (!this.isRunning) return
      
      this.updateForces()
      this.updatePositions()
      
      const positions = Object.fromEntries(
        Object.entries(this.positions).map(([id, pos]) => [id, { x: pos.x, y: pos.y }])
      )
      this.onTick(positions)

      iteration++
      if (iteration % 60 === 0) {
        console.log('Simulation iteration:', iteration)
      }
      
      this.animationId = requestAnimationFrame(tick)
    }
    
    this.animationId = requestAnimationFrame(tick)
  }

  private updateForces() {
    // 重置力
    Object.values(this.positions).forEach(pos => {
      pos.vx = 0
      pos.vy = 0
    })

    // 节点间斥力
    this.nodes.forEach((node1, i) => {
      this.nodes.forEach((node2, j) => {
        if (i === j) return

        const pos1 = this.positions[node1.id]
        const pos2 = this.positions[node2.id]
        if (!pos1 || !pos2) {
          console.warn('Missing position for node:', !pos1 ? node1.id : node2.id)
          return
        }

        const dx = pos2.x - pos1.x
        const dy = pos2.y - pos1.y
        const distance = Math.sqrt(dx * dx + dy * dy)
        
        if (distance === 0) return

        // 增加斥力系数和最小距离
        const minDistance = 300
        const repulsionStrength = 5000
        const force = repulsionStrength / (distance * distance)
        const fx = (dx / distance) * force
        const fy = (dy / distance) * force

        pos1.vx -= fx
        pos1.vy -= fy
        pos2.vx += fx
        pos2.vy += fy
      })
    })

    // 边的弹力
    this.edges.forEach(edge => {
      const source = this.positions[edge.source]
      const target = this.positions[edge.target]
      if (!source || !target) {
        console.warn('Missing position for edge:', edge)
        return
      }

      const dx = target.x - source.x
      const dy = target.y - source.y
      const distance = Math.sqrt(dx * dx + dy * dy)
      
      if (distance === 0) return

      // 调整弹力系数和理想边长
      const idealLength = 350
      const springStrength = 0.01
      const force = (distance - idealLength) * springStrength
      const fx = (dx / distance) * force
      const fy = (dy / distance) * force

      source.vx += fx
      source.vy += fy
      target.vx -= fx
      target.vy -= fy
    })

    // 中心引力
    Object.values(this.positions).forEach(pos => {
      const dx = this.width / 2 - pos.x
      const dy = this.height / 2 - pos.y
      // 减小中心引力，让节点更分散
      pos.vx += dx * 0.0002
      pos.vy += dy * 0.0002
    })
  }

  private updatePositions() {
    Object.values(this.positions).forEach(pos => {
      pos.x += pos.vx
      pos.y += pos.vy

      // 阻尼
      pos.vx *= 0.8
      pos.vy *= 0.8

      // 边界限制（增加边距）
      const margin = 150
      pos.x = Math.max(margin, Math.min(this.width - margin, pos.x))
      pos.y = Math.max(margin, Math.min(this.height - margin, pos.y))
    })
  }

  public updateData(nodes: KnowledgeNode[], edges: KnowledgeLink[]) {
    console.log('Updating data:', { nodes: nodes.length, edges: edges.length })
    this.nodes = nodes
    this.edges = edges
    this.initPositions()
  }

  public updateSize(width: number, height: number) {
    console.log('Updating size:', width, height)
    this.width = width
    this.height = height
    
    // 重新调整节点位置
    Object.values(this.positions).forEach(pos => {
      pos.x = Math.min(pos.x, this.width - 50)
      pos.y = Math.min(pos.y, this.height - 50)
    })
  }

  public zoomIn() {
    console.log('Zoom in')
    // TODO: 实现缩放功能
  }

  public zoomOut() {
    console.log('Zoom out')
    // TODO: 实现缩放功能
  }

  public reset() {
    console.log('Reset positions')
    this.initPositions()
  }

  public center() {
    console.log('Center view')
    Object.values(this.positions).forEach(pos => {
      pos.x = this.width / 2
      pos.y = this.height / 2
    })
  }

  public destroy() {
    console.log('Destroying force graph')
    this.isRunning = false
    if (this.animationId !== null) {
      cancelAnimationFrame(this.animationId)
    }
  }
} 