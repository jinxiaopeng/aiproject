# 创建动态背景组件
<template>
  <div class="dynamic-background">
    <canvas ref="canvasRef"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const canvasRef = ref<HTMLCanvasElement | null>(null)
let animationFrameId: number
let ctx: CanvasRenderingContext2D | null = null

interface Particle {
  x: number
  y: number
  vx: number
  vy: number
  radius: number
}

const particles: Particle[] = []
const connections: { p1: Particle; p2: Particle; distance: number }[] = []
const particleCount = 100
const connectionDistance = 150
const particleSpeed = 0.5

// 初始化粒子
const initParticles = () => {
  const canvas = canvasRef.value
  if (!canvas) return

  for (let i = 0; i < particleCount; i++) {
    particles.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * particleSpeed,
      vy: (Math.random() - 0.5) * particleSpeed,
      radius: Math.random() * 2 + 1
    })
  }
}

// 更新粒子位置
const updateParticles = () => {
  const canvas = canvasRef.value
  if (!canvas) return

  particles.forEach(p => {
    p.x += p.vx
    p.y += p.vy

    // 边界检查
    if (p.x < 0 || p.x > canvas.width) p.vx *= -1
    if (p.y < 0 || p.y > canvas.height) p.vy *= -1
  })
}

// 绘制连接线
const drawConnections = () => {
  if (!ctx) return
  
  connections.length = 0
  
  for (let i = 0; i < particles.length; i++) {
    for (let j = i + 1; j < particles.length; j++) {
      const dx = particles[i].x - particles[j].x
      const dy = particles[i].y - particles[j].y
      const distance = Math.sqrt(dx * dx + dy * dy)
      
      if (distance < connectionDistance) {
        connections.push({
          p1: particles[i],
          p2: particles[j],
          distance
        })
      }
    }
  }
  
  connections.forEach(({ p1, p2, distance }) => {
    const opacity = 1 - (distance / connectionDistance)
    ctx!.beginPath()
    ctx!.strokeStyle = `rgba(24, 144, 255, ${opacity * 0.5})`
    ctx!.lineWidth = 1
    ctx!.moveTo(p1.x, p1.y)
    ctx!.lineTo(p2.x, p2.y)
    ctx!.stroke()
  })
}

// 绘制粒子
const drawParticles = () => {
  if (!ctx) return
  
  particles.forEach(p => {
    ctx!.beginPath()
    ctx!.fillStyle = 'rgba(24, 144, 255, 0.8)'
    ctx!.arc(p.x, p.y, p.radius, 0, Math.PI * 2)
    ctx!.fill()
  })
}

// 动画循环
const animate = () => {
  if (!ctx || !canvasRef.value) return
  
  ctx.clearRect(0, 0, canvasRef.value.width, canvasRef.value.height)
  
  updateParticles()
  drawConnections()
  drawParticles()
  
  animationFrameId = requestAnimationFrame(animate)
}

// 调整画布大小
const resizeCanvas = () => {
  const canvas = canvasRef.value
  if (!canvas) return
  
  canvas.width = window.innerWidth
  canvas.height = window.innerHeight
}

// 生命周期钩子
onMounted(() => {
  const canvas = canvasRef.value
  if (!canvas) return
  
  ctx = canvas.getContext('2d')
  if (!ctx) return
  
  resizeCanvas()
  initParticles()
  animate()
  
  window.addEventListener('resize', resizeCanvas)
})

onUnmounted(() => {
  cancelAnimationFrame(animationFrameId)
  window.removeEventListener('resize', resizeCanvas)
})
</script>

<style scoped>
.dynamic-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  background: #f5f7fa;
}

canvas {
  display: block;
}
</style> 