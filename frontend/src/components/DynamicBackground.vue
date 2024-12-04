<template>
  <div class="dynamic-background">
    <div class="particles" ref="particles"></div>
    <div class="gradient-overlay"></div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'

const particles = ref(null)
let animationFrame = null

const createParticle = () => {
  const particle = document.createElement('div')
  particle.className = 'particle'
  particle.style.left = Math.random() * 100 + 'vw'
  particle.style.animationDuration = Math.random() * 3 + 2 + 's'
  particle.style.opacity = Math.random() * 0.5 + 0.2
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
  background: linear-gradient(135deg, #1a1c2c 0%, #2a3c54 100%);
}

.gradient-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at 50% 50%, rgba(26, 28, 44, 0) 0%, rgba(26, 28, 44, 0.8) 100%);
  pointer-events: none;
}

.particles {
  position: absolute;
  width: 100%;
  height: 100%;
}

.particle {
  position: absolute;
  background: #ffffff;
  border-radius: 50%;
  animation: fall linear forwards;
  opacity: 0.3;
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
}

@keyframes fall {
  from {
    transform: translateY(-10px) rotate(45deg);
  }
  to {
    transform: translateY(100vh) rotate(45deg);
  }
}
</style> 