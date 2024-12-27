<template>
  <div class="challenge-terminal">
    <!-- 终端标题栏 -->
    <div class="terminal-header">
      <div class="terminal-controls">
        <span class="control close"></span>
        <span class="control minimize"></span>
        <span class="control maximize"></span>
      </div>
      <div class="terminal-title">{{ title || 'Terminal' }}</div>
      <div class="terminal-actions">
        <el-button-group>
          <el-button 
            size="small"
            :icon="Refresh"
            @click="handleReset"
          >
            重置
          </el-button>
          <el-button 
            size="small"
            :icon="FullScreen"
            @click="toggleFullscreen"
          >
            全屏
          </el-button>
        </el-button-group>
      </div>
    </div>

    <!-- 终端输出区域 -->
    <div 
      class="terminal-output" 
      ref="outputContainer"
      :class="{ 'fullscreen': isFullscreen }"
    >
      <div 
        v-for="(line, index) in outputHistory" 
        :key="index" 
        class="output-line"
        :class="line.type"
      >
        <template v-if="line.type === 'command'">
          <span class="prompt">$</span>
          <span class="command">{{ line.content }}</span>
        </template>
        <template v-else-if="line.type === 'error'">
          <span class="error">{{ line.content }}</span>
        </template>
        <template v-else-if="line.type === 'success'">
          <span class="success">{{ line.content }}</span>
        </template>
        <template v-else>
          <span class="output">{{ line.content }}</span>
        </template>
      </div>

      <!-- 当前输入行 -->
      <div class="input-line" v-show="!isProcessing">
        <span class="prompt">$</span>
        <input
          ref="commandInput"
          v-model="currentCommand"
          @keyup.enter="executeCommand"
          @keyup.up="navigateHistory('up')"
          @keyup.down="navigateHistory('down')"
          @keyup.tab.prevent="handleTabCompletion"
          :placeholder="placeholder"
          spellcheck="false"
          autocomplete="off"
        />
      </div>
    </div>

    <!-- 终端状态栏 -->
    <div class="terminal-status">
      <div class="status-item">
        <el-icon><Connection /></el-icon>
        <span>{{ connectionStatus }}</span>
      </div>
      <div class="status-item">
        <el-icon><Timer /></el-icon>
        <span>{{ elapsedTime }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { 
  Refresh,
  FullScreen,
  Connection,
  Timer
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

// Props
interface Props {
  title?: string
  placeholder?: string
  initialCommands?: string[]
}

const props = withDefaults(defineProps<Props>(), {
  title: 'Cyber Terminal',
  placeholder: '输入命令...',
  initialCommands: () => []
})

// Emits
const emit = defineEmits<{
  (e: 'command-executed', command: string): void
  (e: 'command-result', result: any): void
}>()

// Refs
const outputContainer = ref<HTMLElement | null>(null)
const commandInput = ref<HTMLInputElement | null>(null)
const currentCommand = ref('')
const isProcessing = ref(false)
const isFullscreen = ref(false)
const connectionStatus = ref('已连接')
const startTime = ref(Date.now())

// Terminal state
const outputHistory = ref<Array<{type: string, content: string}>>([
  { type: 'output', content: '欢迎使用靶场终端！输入 help 获取帮助。' }
])
const commandHistory = ref<string[]>([])
const historyIndex = ref(-1)

// 计算运行时间
const elapsedTime = ref('00:00:00')
const updateElapsedTime = () => {
  const now = Date.now()
  const diff = now - startTime.value
  const hours = Math.floor(diff / 3600000)
  const minutes = Math.floor((diff % 3600000) / 60000)
  const seconds = Math.floor((diff % 60000) / 1000)
  elapsedTime.value = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
}

// 定时更新时间
let timeInterval: number
onMounted(() => {
  timeInterval = window.setInterval(updateElapsedTime, 1000)
})

onUnmounted(() => {
  if (timeInterval) {
    clearInterval(timeInterval)
  }
})

// Methods
const addToOutput = (content: string, type: string = 'output') => {
  outputHistory.value.push({ type, content })
  scrollToBottom()
}

const scrollToBottom = () => {
  setTimeout(() => {
    if (outputContainer.value) {
      outputContainer.value.scrollTop = outputContainer.value.scrollHeight
    }
  }, 0)
}

const executeCommand = async () => {
  const command = currentCommand.value.trim()
  if (!command) return

  // Add command to history
  addToOutput(command, 'command')
  commandHistory.value.push(command)
  historyIndex.value = commandHistory.value.length

  // Process command
  isProcessing.value = true
  try {
    // Basic command handling
    switch (command.toLowerCase()) {
      case 'help':
        addToOutput(`
可用命令：
- help          显示帮助信息
- clear         清空终端
- reset         重置环境
- info          显示靶机信息
- connect       连接靶机
- disconnect    断开连接
        `.trim())
        break
      
      case 'clear':
        outputHistory.value = []
        break
      
      case 'reset':
        handleReset()
        break
      
      default:
        // Emit command for parent handling
        emit('command-executed', command)
        // Simulate command output
        setTimeout(() => {
          addToOutput(`执行命令: ${command}`)
        }, 500)
    }
  } catch (error) {
    addToOutput(error instanceof Error ? error.message : '发生错误', 'error')
  } finally {
    isProcessing.value = false
    currentCommand.value = ''
    focusInput()
  }
}

const navigateHistory = (direction: 'up' | 'down') => {
  if (commandHistory.value.length === 0) return

  if (direction === 'up') {
    historyIndex.value = Math.max(0, historyIndex.value - 1)
  } else {
    historyIndex.value = Math.min(commandHistory.value.length, historyIndex.value + 1)
  }

  currentCommand.value = historyIndex.value < commandHistory.value.length 
    ? commandHistory.value[historyIndex.value] 
    : ''
}

const handleTabCompletion = () => {
  // 实现命令自动补全逻辑
  const commands = ['help', 'clear', 'reset', 'info', 'connect', 'disconnect']
  const input = currentCommand.value.toLowerCase()
  
  const matches = commands.filter(cmd => cmd.startsWith(input))
  if (matches.length === 1) {
    currentCommand.value = matches[0]
  } else if (matches.length > 1) {
    addToOutput(matches.join('  '))
  }
}

const handleReset = () => {
  ElMessage.success('环境重置中...')
  addToOutput('正在重置环境...', 'warning')
  setTimeout(() => {
    addToOutput('环境重置完成！', 'success')
  }, 1500)
}

const toggleFullscreen = () => {
  isFullscreen.value = !isFullscreen.value
  scrollToBottom()
}

const focusInput = () => {
  if (commandInput.value) {
    commandInput.value.focus()
  }
}

// Lifecycle hooks
onMounted(() => {
  focusInput()
  // Execute initial commands
  props.initialCommands.forEach(cmd => {
    currentCommand.value = cmd
    executeCommand()
  })
})
</script>

<style scoped lang="scss">
.challenge-terminal {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: rgba(16, 16, 24, 0.95);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  overflow: hidden;
  font-family: 'Fira Code', monospace;

  .terminal-header {
    display: flex;
    align-items: center;
    padding: 8px 16px;
    background: rgba(255, 255, 255, 0.05);
    border-bottom: 1px solid var(--border-color);

    .terminal-controls {
      display: flex;
      gap: 8px;
      margin-right: 16px;

      .control {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        
        &.close { background: #ff5f56; }
        &.minimize { background: #ffbd2e; }
        &.maximize { background: #27c93f; }
      }
    }

    .terminal-title {
      flex: 1;
      color: var(--text-secondary);
      font-size: 14px;
    }

    .terminal-actions {
      .el-button {
        background: transparent;
        border-color: var(--border-color);
        
        &:hover {
          background: rgba(255, 255, 255, 0.1);
        }
      }
    }
  }

  .terminal-output {
    flex: 1;
    padding: 16px;
    overflow-y: auto;
    font-size: 14px;
    line-height: 1.5;
    
    &.fullscreen {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      z-index: 1000;
      background: rgba(16, 16, 24, 0.98);
      padding: 20px;
    }

    &::-webkit-scrollbar {
      width: 4px;
    }

    &::-webkit-scrollbar-track {
      background: rgba(255, 255, 255, 0.05);
    }

    &::-webkit-scrollbar-thumb {
      background: var(--primary-color);
      border-radius: 2px;
    }

    .output-line {
      margin-bottom: 8px;
      word-break: break-word;

      &:last-child {
        margin-bottom: 0;
      }
      
      .prompt {
        color: var(--primary-color);
        margin-right: 8px;
      }

      &.command {
        color: #fff;
      }

      &.error {
        color: #ff5f56;
      }

      &.success {
        color: #27c93f;
      }

      &.warning {
        color: #ffbd2e;
      }

      &.output {
        color: #ddd;
      }
    }

    .input-line {
      display: flex;
      align-items: center;
      margin-top: 8px;

      .prompt {
        color: var(--primary-color);
        margin-right: 8px;
      }

      input {
        flex: 1;
        background: transparent;
        border: none;
        color: #fff;
        font-family: inherit;
        font-size: inherit;
        outline: none;

        &::placeholder {
          color: rgba(255, 255, 255, 0.3);
        }
      }
    }
  }

  .terminal-status {
    display: flex;
    align-items: center;
    padding: 4px 16px;
    background: rgba(255, 255, 255, 0.05);
    border-top: 1px solid var(--border-color);
    font-size: 12px;

    .status-item {
      display: flex;
      align-items: center;
      gap: 4px;
      margin-right: 16px;
      color: var(--text-secondary);

      .el-icon {
        font-size: 14px;
      }

      &:last-child {
        margin-right: 0;
      }
    }
  }
}
</style> 