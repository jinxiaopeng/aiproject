<template>
  <div class="toolbar">
    <div class="left">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索知识点..."
        class="search-input"
        clearable
        @input="handleSearch"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
    </div>

    <div class="right">
      <el-button-group>
        <el-tooltip content="重置视图" placement="bottom">
          <el-button @click="handleReset">
            <el-icon><Refresh /></el-icon>
          </el-button>
        </el-tooltip>
        <el-tooltip content="切换布局" placement="bottom">
          <el-button @click="handleToggleLayout">
            <el-icon><SetUp /></el-icon>
          </el-button>
        </el-tooltip>
        <el-tooltip content="全屏显示" placement="bottom">
          <el-button @click="handleFullscreen">
            <el-icon><FullScreen /></el-icon>
          </el-button>
        </el-tooltip>
      </el-button-group>

      <el-button-group class="view-controls">
        <el-tooltip content="放大" placement="bottom">
          <el-button @click="handleZoomIn">
            <el-icon><ZoomIn /></el-icon>
          </el-button>
        </el-tooltip>
        <el-tooltip content="缩小" placement="bottom">
          <el-button @click="handleZoomOut">
            <el-icon><ZoomOut /></el-icon>
          </el-button>
        </el-tooltip>
      </el-button-group>

      <el-button-group>
        <el-tooltip content="导出图片" placement="bottom">
          <el-button @click="handleExport">
            <el-icon><Download /></el-icon>
          </el-button>
        </el-tooltip>
        <el-tooltip content="帮助" placement="bottom">
          <el-button @click="handleHelp">
            <el-icon><QuestionFilled /></el-icon>
          </el-button>
        </el-tooltip>
      </el-button-group>
    </div>

    <!-- 帮助对话框 -->
    <el-dialog
      v-model="helpDialogVisible"
      title="使用帮助"
      width="500px"
      destroy-on-close
    >
      <div class="help-content">
        <h4>基本操作</h4>
        <ul>
          <li>点击节点：查看知识点详情</li>
          <li>拖拽节点：调整节点位置</li>
          <li>滚轮缩放：放大/缩小视图</li>
          <li>拖拽空白处：平移视图</li>
        </ul>

        <h4>快捷键</h4>
        <ul>
          <li><kbd>Space</kbd> + 拖拽：平移视图</li>
          <li><kbd>Ctrl</kbd> + 滚轮：缩放视图</li>
          <li><kbd>Ctrl</kbd> + <kbd>F</kbd>：搜索</li>
          <li><kbd>Esc</kbd>：取消选中</li>
        </ul>

        <h4>布局模式</h4>
        <ul>
          <li>力导向布局：节点自动分布，可拖拽调整</li>
          <li>环形布局：节点呈环形分布，适合查看整体结构</li>
        </ul>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useKnowledgeGraphStore } from '../store'
import { ElMessage } from 'element-plus'
import {
  Search,
  Refresh,
  SetUp,
  FullScreen,
  ZoomIn,
  ZoomOut,
  Download,
  QuestionFilled
} from '@element-plus/icons-vue'

const store = useKnowledgeGraphStore()
const searchKeyword = ref('')
const helpDialogVisible = ref(false)

// 搜索
const handleSearch = () => {
  store.setFilters({ search: searchKeyword.value })
}

// 重置视图
const handleReset = () => {
  store.resetLayout()
  ElMessage.success('视图已重置')
}

// 切换布局
const handleToggleLayout = () => {
  const newMode = store.layout.mode === 'force' ? 'circular' : 'force'
  store.setLayoutMode(newMode)
  ElMessage.success(`已切换到${newMode === 'force' ? '力导向' : '环形'}布局`)
}

// 全屏显示
const handleFullscreen = () => {
  const element = document.querySelector('.graph-container')
  if (element) {
    if (document.fullscreenElement) {
      document.exitFullscreen()
    } else {
      element.requestFullscreen()
    }
  }
}

// 缩放控制
const handleZoomIn = () => {
  const newZoom = Math.min(store.layout.zoom * 1.2, 2)
  store.setZoom(newZoom)
}

const handleZoomOut = () => {
  const newZoom = Math.max(store.layout.zoom / 1.2, 0.5)
  store.setZoom(newZoom)
}

// 导出图片
const handleExport = () => {
  ElMessage.info('导出功能开发中')
}

// 显示帮助
const handleHelp = () => {
  helpDialogVisible.value = true
}
</script>

<style scoped>
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
  padding: 0 16px;
  background: rgba(30, 35, 40, 0.95);
  border-bottom: 1px solid rgba(65, 184, 131, 0.1);
}

.left {
  flex: 1;
  max-width: 300px;
}

.right {
  display: flex;
  gap: 8px;
}

.search-input {
  width: 100%;
}

.view-controls {
  margin: 0 8px;
}

.help-content {
  color: #e5eaf3;
}

.help-content h4 {
  margin: 16px 0 8px;
  color: #409eff;
  font-size: 16px;
}

.help-content ul {
  margin: 0;
  padding-left: 20px;
  list-style: none;
}

.help-content li {
  margin: 4px 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.help-content li::before {
  content: '•';
  color: #409eff;
}

kbd {
  display: inline-block;
  padding: 2px 6px;
  font-family: monospace;
  font-size: 12px;
  color: #e5eaf3;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  box-shadow: 0 2px 0 rgba(0, 0, 0, 0.2);
}

:deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, 0.05);
  box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.1);
}

:deep(.el-input__inner) {
  color: #e5eaf3;
}

:deep(.el-button) {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #e5eaf3;
}

:deep(.el-button:hover) {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
}

:deep(.el-dialog) {
  background: rgba(30, 35, 40, 0.95);
  border: 1px solid rgba(65, 184, 131, 0.1);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}

:deep(.el-dialog__title) {
  color: #e5eaf3;
}

:deep(.el-dialog__headerbtn:hover .el-dialog__close) {
  color: #409eff;
}
</style> 