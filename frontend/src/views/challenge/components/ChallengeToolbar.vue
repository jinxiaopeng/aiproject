<template>
  <div class="challenge-toolbar">
    <!-- 工具栏标题 -->
    <div class="toolbar-header">
      <el-icon><Tools /></el-icon>
      <span>工具箱</span>
    </div>

    <!-- 工具列表 -->
    <div class="tools-list">
      <!-- 终端工具 -->
      <div class="tool-item" @click="toggleTool('terminal')">
        <el-tooltip content="终端" placement="right">
          <div class="tool-icon">
            <el-icon><Terminal /></el-icon>
          </div>
        </el-tooltip>
      </div>

      <!-- 网络工具 -->
      <div class="tool-item" @click="toggleTool('network')">
        <el-tooltip content="网络监控" placement="right">
          <div class="tool-icon">
            <el-icon><Connection /></el-icon>
          </div>
        </el-tooltip>
      </div>

      <!-- 编辑器 -->
      <div class="tool-item" @click="toggleTool('editor')">
        <el-tooltip content="代码编辑器" placement="right">
          <div class="tool-icon">
            <el-icon><Edit /></el-icon>
          </div>
        </el-tooltip>
      </div>

      <!-- 文件管理器 -->
      <div class="tool-item" @click="toggleTool('files')">
        <el-tooltip content="文件管理器" placement="right">
          <div class="tool-icon">
            <el-icon><Folder /></el-icon>
          </div>
        </el-tooltip>
      </div>

      <!-- 笔记本 -->
      <div class="tool-item" @click="toggleTool('notes')">
        <el-tooltip content="笔记本" placement="right">
          <div class="tool-icon">
            <el-icon><Notebook /></el-icon>
          </div>
        </el-tooltip>
      </div>

      <!-- 调试工具 -->
      <div class="tool-item" @click="toggleTool('debug')">
        <el-tooltip content="调试工具" placement="right">
          <div class="tool-icon">
            <el-icon><Monitor /></el-icon>
          </div>
        </el-tooltip>
      </div>
    </div>

    <!-- 快捷操作 -->
    <div class="quick-actions">
      <!-- 重置环境 -->
      <el-tooltip content="重置环境" placement="right">
        <el-button
          circle
          type="warning"
          :icon="Refresh"
          @click="handleReset"
        />
      </el-tooltip>

      <!-- 全屏模式 -->
      <el-tooltip content="全屏模式" placement="right">
        <el-button
          circle
          :icon="FullScreen"
          @click="toggleFullscreen"
        />
      </el-tooltip>

      <!-- 帮助文档 -->
      <el-tooltip content="帮助文档" placement="right">
        <el-button
          circle
          :icon="QuestionFilled"
          @click="showHelp"
        />
      </el-tooltip>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import {
  Tools,
  Terminal,
  Connection,
  Edit,
  Folder,
  Notebook,
  Monitor,
  Refresh,
  FullScreen,
  QuestionFilled
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

// Emits
const emit = defineEmits<{
  (e: 'tool-toggle', tool: string): void
  (e: 'reset'): void
  (e: 'fullscreen'): void
}>()

// 切换工具
const toggleTool = (tool: string) => {
  emit('tool-toggle', tool)
}

// 重置环境
const handleReset = () => {
  ElMessage.warning('确定要重置环境吗？这将清除所有进度。')
  emit('reset')
}

// 切换全屏
const toggleFullscreen = () => {
  emit('fullscreen')
}

// 显示帮助
const showHelp = () => {
  ElMessage.info('正在准备帮助文档...')
}
</script>

<style scoped lang="scss">
.challenge-toolbar {
  width: 60px;
  height: 100%;
  background: rgba(16, 16, 24, 0.95);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px 0;

  .toolbar-header {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    margin-bottom: 20px;
    color: var(--text-color);
    font-size: 12px;

    .el-icon {
      font-size: 20px;
      color: var(--primary-color);
    }
  }

  .tools-list {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 16px;
    padding: 0 8px;
    width: 100%;

    .tool-item {
      cursor: pointer;
      transition: all 0.3s ease;

      .tool-icon {
        width: 40px;
        height: 40px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;

        .el-icon {
          font-size: 20px;
          color: var(--text-secondary);
        }

        &:hover {
          background: rgba(255, 255, 255, 0.1);
          border-color: var(--primary-color);
          transform: translateY(-2px);

          .el-icon {
            color: var(--primary-color);
          }
        }
      }

      &.active .tool-icon {
        background: var(--primary-color);
        border-color: var(--primary-color);

        .el-icon {
          color: #fff;
        }
      }
    }
  }

  .quick-actions {
    display: flex;
    flex-direction: column;
    gap: 8px;
    padding: 16px 0;
    border-top: 1px solid var(--border-color);

    .el-button {
      width: 36px;
      height: 36px;
      padding: 8px;
      background: transparent;
      border-color: var(--border-color);

      &:hover {
        background: rgba(255, 255, 255, 0.1);
        border-color: var(--primary-color);
      }

      .el-icon {
        font-size: 16px;
      }
    }
  }
}
</style> 