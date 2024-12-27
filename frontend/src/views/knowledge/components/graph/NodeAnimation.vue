<template>
  <div 
    class="node-animation"
    :class="{
      'is-selected': isSelected,
      'is-related': isRelated,
      'is-hovered': isHovered
    }"
  >
    <el-card class="node-content" shadow="hover" :body-style="{ padding: '12px' }">
      <!-- 节点主体 -->
      <div class="node-body">
        <!-- 图标和标题 -->
        <div class="node-header">
          <div class="node-icon-wrapper" :style="{ background: getCategoryColor(node.category) }">
            <el-icon :size="20"><component :is="getCategoryIcon(node.category)" /></el-icon>
          </div>
          <div class="node-title">
            <div class="node-name">{{ node.name }}</div>
            <el-tag 
              size="small" 
              :type="getCategoryType(node.category)"
              effect="dark"
              class="category-tag"
            >
              {{ getCategoryLabel(node.category) }}
            </el-tag>
          </div>
        </div>

        <!-- 难度指示器 -->
        <div class="difficulty-indicator">
          <el-progress
            :percentage="getDifficultyPercentage(node.difficulty)"
            :status="getDifficultyStatus(node.difficulty)"
            :stroke-width="4"
            :show-text="false"
            class="difficulty-progress"
          />
          <span class="difficulty-label" :class="node.difficulty">
            {{ getDifficultyLabel(node.difficulty) }}
          </span>
        </div>
      </div>

      <!-- 连接指示器 -->
      <div class="connection-indicator" v-if="isSelected || isRelated">
        <div class="connection-line"></div>
        <div class="connection-dot"></div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { ElCard, ElIcon, ElTag, ElProgress } from 'element-plus'
import {
  Warning,
  Connection,
  Tools,
  MagicStick,
  InfoFilled,
  Lock,
  Aim,
  Shield
} from '@element-plus/icons-vue'
import type { KnowledgeNode } from '@/api/knowledge'

const props = defineProps<{
  node: KnowledgeNode
  isSelected: boolean
  isHovered: boolean
  isRelated: boolean
}>()

const emit = defineEmits<{
  (e: 'click', node: KnowledgeNode): void
  (e: 'mouseenter', node: KnowledgeNode): void
  (e: 'mouseleave', node: KnowledgeNode): void
}>()

// 获取分类颜色
const getCategoryColor = (category: string) => {
  const colors: Record<string, string> = {
    'vulnerability': 'linear-gradient(135deg, #41b883 0%, #34495e 100%)',
    'tools': 'linear-gradient(135deg, #f1c40f 0%, #f39c12 100%)',
    'authentication': 'linear-gradient(135deg, #3498db 0%, #2980b9 100%)',
    'penetration': 'linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)',
    'protection': 'linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%)',
    'default': 'linear-gradient(135deg, #95a5a6 0%, #7f8c8d 100%)'
  }
  return colors[category] || colors.default
}

// 获取分类图标
const getCategoryIcon = (category: string) => {
  const icons: Record<string, any> = {
    'vulnerability': Warning,
    'tools': Tools,
    'authentication': Lock,
    'penetration': Aim,
    'protection': Shield,
    'default': InfoFilled
  }
  return icons[category] || icons.default
}

// 获取分类标签类型
const getCategoryType = (category: string) => {
  const types: Record<string, string> = {
    'vulnerability': 'danger',
    'tools': 'warning',
    'authentication': 'primary',
    'penetration': 'danger',
    'protection': 'success',
    'default': 'info'
  }
  return types[category] || 'info'
}

// 获取分类标签
const getCategoryLabel = (category: string) => {
  const labels: Record<string, string> = {
    'vulnerability': '漏洞原理',
    'tools': '安全工具',
    'authentication': '身份认证',
    'penetration': '渗透测试',
    'protection': '防护措施',
    'default': '其他'
  }
  return labels[category] || category
}

// 获取难度百分比
const getDifficultyPercentage = (difficulty: string) => {
  const percentages: Record<string, number> = {
    'basic': 25,
    'intermediate': 50,
    'advanced': 75,
    'expert': 100
  }
  return percentages[difficulty] || 25
}

// 获取难度状态
const getDifficultyStatus = (difficulty: string) => {
  const status: Record<string, string> = {
    'basic': 'success',
    'intermediate': '',
    'advanced': 'warning',
    'expert': 'exception'
  }
  return status[difficulty] || ''
}

// 获取难度标签
const getDifficultyLabel = (difficulty: string) => {
  const labels: Record<string, string> = {
    'basic': '入门',
    'intermediate': '进阶',
    'advanced': '高级',
    'expert': '专家'
  }
  return labels[difficulty] || difficulty
}

// 获取节点颜色
const getNodeColor = computed(() => {
  const colors = {
    vulnerability: '#f56c6c',
    concept: '#409eff',
    tool: '#e6a23c',
    technique: '#67c23a',
    default: '#909399'
  }
  return colors[props.node.category as keyof typeof colors] || colors.default
})

// 获取节点图标
const getNodeIcon = computed(() => {
  const icons = {
    vulnerability: 'warning',
    concept: 'info',
    tool: 'tools',
    technique: 'code',
    default: 'help'
  }
  return icons[props.node.category as keyof typeof icons] || icons.default
})

// 计算节点样式
const nodeStyle = computed(() => {
  const baseStyle = {
    backgroundColor: props.isSelected ? `${getNodeColor.value}20` : 'transparent',
    borderColor: getNodeColor.value,
    transform: props.isSelected ? 'scale(1.1)' : 'scale(1)',
    boxShadow: props.isHovered
      ? `0 0 0 2px ${getNodeColor.value}40, 0 0 20px ${getNodeColor.value}20`
      : props.isSelected
      ? `0 0 0 2px ${getNodeColor.value}30`
      : 'none',
    opacity: props.isRelated || (!props.isSelected && !props.isHovered) ? 1 : 0.5
  }

  return baseStyle
})

// 处理事件
const handleClick = () => emit('click', props.node)
const handleMouseEnter = () => emit('mouseenter', props.node)
const handleMouseLeave = () => emit('mouseleave', props.node)
</script>

<style scoped>
.node-animation {
  position: relative;
  width: 240px;
  transform: scale(1);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.node-content {
  background: rgba(28, 28, 35, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.node-body {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.node-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.node-icon-wrapper {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  color: white;
  box-shadow: 
    0 4px 12px rgba(0, 0, 0, 0.2),
    inset 0 2px 0 rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.node-title {
  flex: 1;
  min-width: 0;
}

.node-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.category-tag {
  font-size: 10px;
  padding: 0 6px;
  height: 18px;
  line-height: 16px;
  border: none;
}

.difficulty-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
}

.difficulty-progress {
  flex: 1;
}

.difficulty-label {
  font-size: 11px;
  font-weight: 500;
  white-space: nowrap;
}

.difficulty-label.basic {
  color: var(--el-color-success);
}

.difficulty-label.intermediate {
  color: var(--el-color-primary);
}

.difficulty-label.advanced {
  color: var(--el-color-warning);
}

.difficulty-label.expert {
  color: var(--el-color-danger);
}

/* 连接指示器 */
.connection-indicator {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 200%;
  height: 200%;
  transform: translate(-50%, -50%);
  pointer-events: none;
  z-index: -1;
}

.connection-line {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 1px;
  background: linear-gradient(
    90deg,
    transparent 0%,
    var(--el-color-primary-light-5) 50%,
    transparent 100%
  );
  transform-origin: center;
  animation: line-pulse 2s infinite;
}

.connection-dot {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 6px;
  height: 6px;
  background: var(--el-color-primary-light-3);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  animation: dot-pulse 2s infinite;
}

/* 状态样式 */
.is-selected .node-content {
  transform: translateY(-2px);
  border-color: var(--el-color-primary);
  box-shadow: 
    0 8px 24px rgba(0, 0, 0, 0.2),
    0 0 0 1px var(--el-color-primary-light-5);
}

.is-selected .node-icon-wrapper {
  transform: scale(1.1);
}

.is-related .node-content {
  border-color: var(--el-color-primary-light-7);
}

.is-hovered .node-content {
  transform: translateY(-1px);
}

/* 动画 */
@keyframes line-pulse {
  0%, 100% {
    opacity: 0.2;
    transform: scaleX(0.8);
  }
  50% {
    opacity: 0.5;
    transform: scaleX(1);
  }
}

@keyframes dot-pulse {
  0%, 100% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 0.5;
  }
  50% {
    transform: translate(-50%, -50%) scale(1.5);
    opacity: 0.2;
  }
}

/* Element Plus 暗色主题适配 */
:deep(.el-card) {
  --el-card-bg-color: transparent;
  --el-border-color-light: rgba(255, 255, 255, 0.1);
}

:deep(.el-progress-bar__inner) {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

:deep(.el-tag) {
  border: none;
}
</style> 