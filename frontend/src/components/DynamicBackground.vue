<template>
  <div class="dynamic-background">
    <div class="particles" ref="particles"></div>
    <div class="gradient-overlay"></div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'

const particles = ref<HTMLElement | null>(null)
let animationFrame: number | null = null

const createParticle = () => {
  const particle = document.createElement('div')
  particle.className = 'particle'
  particle.style.left = Math.random() * 100 + 'vw'
  particle.style.animationDuration = Math.random() * 3 + 2 + 's'
  particle.style.opacity = (Math.random() * 0.5 + 0.2).toString()
  particle.style.width = Math.random() * 4 + 2 + 'px'
  particle.style.height = particle.style.width
  return particle
}

const addParticle = () => {
  if (particles.value) {
    const particle = createParticle()
    particles.value.appendChild(particle)
    particle.addEventListener('animationend', () => {
      particle.remove()
    })
  }
}

const animate = () => {
  if (Math.random() < 0.2) {
    addParticle()
  }
  animationFrame = requestAnimationFrame(animate)
}

onMounted(() => {
  animate()
})

onUnmounted(() => {
  if (animationFrame) {
    cancelAnimationFrame(animationFrame)
  }
})
</script>

<style scoped>
.dynamic-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: -1;
  overflow: hidden;
  background: linear-gradient(135deg, #1a2a4f, #0d1b2a);
}

.gradient-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: 
    radial-gradient(circle at 20% 20%, rgba(255, 127, 80, 0.15) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(26, 42, 79, 0.15) 0%, transparent 50%),
    radial-gradient(circle at 50% 50%, rgba(13, 27, 42, 0) 0%, rgba(13, 27, 42, 0.8) 100%);
  pointer-events: none;
}

.particles {
  position: absolute;
  width: 100%;
  height: 100%;
}

.particle {
  position: absolute;
  background: #ff7f50;
  border-radius: 50%;
  animation: fall linear forwards;
  opacity: 0.2;
  box-shadow: 0 0 15px rgba(255, 127, 80, 0.5);
  filter: blur(1px);
}

@keyframes fall {
  0% {
    transform: translateY(-10px) rotate(0deg);
    opacity: 0;
  }
  20% {
    opacity: 0.2;
  }
  80% {
    opacity: 0.2;
  }
  100% {
    transform: translateY(100vh) rotate(360deg);
    opacity: 0;
  }
}
</style> 