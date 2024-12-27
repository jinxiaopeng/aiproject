<template>
  <div class="achievement-card" :class="{ 'unlocked': isUnlocked }">
    <div class="achievement-icon">
      <el-icon :class="{ 'animate-unlock': isUnlocked }">
        <component :is="icon" />
      </el-icon>
      <div class="achievement-glow"></div>
    </div>
    <div class="achievement-content">
      <h3 class="achievement-title">{{ title }}</h3>
      <p class="achievement-description">{{ description }}</p>
      <div class="achievement-progress" v-if="showProgress">
        <div class="progress-bar">
          <div 
            class="progress-fill"
            :style="{ width: `${progress}%` }"
          ></div>
        </div>
        <span class="progress-text">{{ progress }}%</span>
      </div>
      <div class="achievement-reward" v-if="reward">
        <el-icon><Trophy /></el-icon>
        <span>{{ reward }}</span>
      </div>
    </div>
    <div class="achievement-date" v-if="unlockedDate">
      {{ formatDate(unlockedDate) }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Trophy } from '@element-plus/icons-vue'

interface Props {
  title: string
  description: string
  icon: string
  isUnlocked: boolean
  progress?: number
  reward?: string
  unlockedDate?: Date
  showProgress?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  progress: 0,
  showProgress: true
})

const formatDate = (date: Date) => {
  return new Intl.DateTimeFormat('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(date)
}
</script>

<style scoped>
.achievement-card {
  background: rgba(30, 35, 45, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 16px;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.achievement-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  border-color: rgba(255, 255, 255, 0.2);
}

.achievement-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.05) 0%, 
    rgba(255, 255, 255, 0) 100%
  );
  opacity: 0;
  transition: opacity 0.3s ease;
}

.achievement-card:hover::before {
  opacity: 1;
}

.achievement-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.achievement-icon .el-icon {
  font-size: 24px;
  color: rgba(255, 255, 255, 0.5);
  transition: all 0.3s ease;
}

.unlocked .achievement-icon .el-icon {
  color: #ffd700;
  text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
}

.achievement-glow {
  position: absolute;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at center,
    rgba(255, 215, 0, 0.2) 0%,
    transparent 70%
  );
  opacity: 0;
  transition: opacity 0.3s ease;
}

.unlocked .achievement-glow {
  opacity: 1;
  animation: pulse 2s infinite;
}

.achievement-content {
  flex: 1;
  min-width: 0;
}

.achievement-title {
  margin: 0 0 4px;
  font-size: 16px;
  font-weight: 600;
  color: #ffffff;
}

.achievement-description {
  margin: 0 0 8px;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.6);
  line-height: 1.4;
}

.achievement-progress {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
}

.progress-bar {
  flex: 1;
  height: 4px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #ffd700, #ffa500);
  border-radius: 2px;
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
  min-width: 40px;
  text-align: right;
}

.achievement-reward {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-top: 8px;
  color: #ffd700;
  font-size: 14px;
}

.achievement-date {
  position: absolute;
  top: 16px;
  right: 16px;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.4);
}

.animate-unlock {
  animation: unlock 0.5s ease;
}

@keyframes unlock {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
  }
}

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 0.5;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.8;
  }
  100% {
    transform: scale(1);
    opacity: 0.5;
  }
}

/* 不同成就状态的样式 */
.achievement-card.locked {
  filter: grayscale(1);
  opacity: 0.7;
}

.achievement-card.locked:hover {
  filter: grayscale(0.8);
  opacity: 0.8;
}

.achievement-card.unlocked {
  border-color: rgba(255, 215, 0, 0.3);
}

.achievement-card.unlocked:hover {
  border-color: rgba(255, 215, 0, 0.5);
  box-shadow: 0 8px 16px rgba(255, 215, 0, 0.1);
}
</style> 