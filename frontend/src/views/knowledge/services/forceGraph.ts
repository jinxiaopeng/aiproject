import * as d3 from 'd3'
import type { KnowledgeNode, KnowledgeLink } from '@/api/knowledge'

export interface SimulationNode extends d3.SimulationNodeDatum {
  id: string | number
  name: string
  category: string
  difficulty: string
  value: number
  x?: number
  y?: number
  fx?: number | null
  fy?: number | null
}

export interface SimulationLink extends d3.SimulationLinkDatum<SimulationNode> {
  source: string | number | SimulationNode
  target: string | number | SimulationNode
  value: number
  type: string
}

export class ForceGraph {
  private svg: SVGSVGElement
  private width: number
  private height: number
  private simulation: d3.Simulation<SimulationNode, SimulationLink>

  constructor(svg: SVGSVGElement, width: number, height: number) {
    this.svg = svg
    this.width = width
    this.height = height
    this.simulation = d3.forceSimulation<SimulationNode>()
  }

  init(nodes: KnowledgeNode[], links: KnowledgeLink[]) {
    // 清除旧的内容
    d3.select(this.svg).selectAll('*').remove()

    // 创建 SVG 组
    const g = d3.select(this.svg)
      .append('g')
      .attr('class', 'graph-container')

    // 初始化力导向图
    this.simulation = d3.forceSimulation<SimulationNode>(nodes as SimulationNode[])
      .force('link', d3.forceLink<SimulationNode, SimulationLink>(links as SimulationLink[])
        .id(d => d.id)
        .distance(200))
      .force('charge', d3.forceManyBody()
        .strength(-2000)
        .distanceMax(800))
      .force('collide', d3.forceCollide()
        .radius(60)
        .strength(0.7))
      .force('center', d3.forceCenter(this.width / 2, this.height / 2))
      .force('x', d3.forceX(this.width / 2).strength(0.05))
      .force('y', d3.forceY(this.height / 2).strength(0.05))
      .alpha(1)
      .alphaDecay(0.02)
      .velocityDecay(0.3)
      .on('tick', () => {
        // 限制节点位置在视图范围内
        nodes.forEach(node => {
          node.x = Math.max(60, Math.min(this.width - 60, node.x || this.width / 2))
          node.y = Math.max(60, Math.min(this.height - 60, node.y || this.height / 2))
        })
      })

    return {
      nodes: nodes as SimulationNode[],
      links: links as SimulationLink[],
      simulation: this.simulation
    }
  }

  stop() {
    if (this.simulation) {
      this.simulation.stop()
    }
  }
} 