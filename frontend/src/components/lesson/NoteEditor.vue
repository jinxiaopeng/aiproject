<template>
  <div class="note-editor">
    <!-- 工具栏 -->
    <div class="editor-toolbar">
      <div class="left-tools">
        <el-button-group>
          <el-button
            :type="mode === 'edit' ? 'primary' : ''"
            @click="switchMode('edit')"
          >
            编辑
          </el-button>
          <el-button
            :type="mode === 'preview' ? 'primary' : ''"
            @click="switchMode('preview')"
          >
            预览
          </el-button>
        </el-button-group>

        <el-divider direction="vertical" />

        <template v-if="mode === 'edit'">
          <el-button-group>
            <el-tooltip
              v-for="tool in textTools"
              :key="tool.name"
              :content="tool.tooltip"
              placement="top"
            >
              <el-button @click="applyTool(tool)">
                <el-icon><component :is="tool.icon" /></el-icon>
              </el-button>
            </el-tooltip>
          </el-button-group>

          <el-divider direction="vertical" />

          <el-button-group>
            <el-tooltip
              v-for="tool in listTools"
              :key="tool.name"
              :content="tool.tooltip"
              placement="top"
            >
              <el-button @click="applyTool(tool)">
                <el-icon><component :is="tool.icon" /></el-icon>
              </el-button>
            </el-tooltip>
          </el-button-group>

          <el-divider direction="vertical" />

          <el-button-group>
            <el-tooltip
              v-for="tool in insertTools"
              :key="tool.name"
              :content="tool.tooltip"
              placement="top"
            >
              <el-button @click="applyTool(tool)">
                <el-icon><component :is="tool.icon" /></el-icon>
              </el-button>
            </el-tooltip>
          </el-button-group>
        </template>
      </div>

      <div class="right-tools">
        <el-tooltip content="历史记录" placement="top">
          <el-button @click="showHistory = true">
            <el-icon><Timer /></el-icon>
          </el-button>
        </el-tooltip>

        <el-button
          type="primary"
          :loading="saving"
          @click="saveNote"
        >
          保存
        </el-button>
      </div>
    </div>

    <!-- 编辑器主体 -->
    <div class="editor-main">
      <!-- 编辑模式 -->
      <div v-show="mode === 'edit'" class="editor-textarea">
        <el-input
          v-model="content"
          type="textarea"
          :rows="15"
          resize="none"
          @input="handleInput"
        />
      </div>

      <!-- 预览模式 -->
      <div
        v-show="mode === 'preview'"
        class="markdown-preview markdown-body"
        v-html="renderedContent"
      ></div>
    </div>

    <!-- 历史记录抽屉 -->
    <el-drawer
      v-model="showHistory"
      title="历史记录"
      size="50%"
      destroy-on-close
    >
      <div class="history-list">
        <el-timeline>
          <el-timeline-item
            v-for="(record, index) in history"
            :key="index"
            :timestamp="formatDate(record.created_at)"
            placement="top"
          >
            <el-card>
              <div class="history-preview">
                {{ record.content.substring(0, 100) }}...
              </div>
              <div class="history-actions">
                <el-button
                  type="primary"
                  link
                  @click="previewHistory(record)"
                >
                  预览
                </el-button>
                <el-button
                  type="primary"
                  link
                  @click="restoreHistory(record)"
                >
                  恢复
                </el-button>
              </div>
            </el-card>
          </el-timeline-item>
        </el-timeline>
      </div>
    </el-drawer>

    <!-- 历史记录预览对话框 -->
    <el-dialog
      v-model="showHistoryPreview"
      title="历史版本预览"
      width="60%"
    >
      <div
        class="markdown-preview markdown-body"
        v-html="selectedHistoryContent"
      ></div>
      <template #footer>
        <el-button @click="showHistoryPreview = false">关闭</el-button>
        <el-button
          type="primary"
          @click="restoreHistory(selectedHistory)"
        >
          恢复此版本
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Bold,
  Italic,
  List,
  Link,
  Picture,
  Timer,
  Document
} from '@element-plus/icons-vue'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import dayjs from 'dayjs'
import noteApi from '@/api/note'
import type { Note, NoteHistory } from '@/api/note'

// Props
const props = defineProps<{
  lessonId: number
  initialContent?: string
}>()

// Emits
const emit = defineEmits<{
  (e: 'save', content: string): void
  (e: 'update:content', content: string): void
}>()

// 状态
const mode = ref<'edit' | 'preview'>('edit')
const content = ref(props.initialContent || '')
const saving = ref(false)
const showHistory = ref(false)
const showHistoryPreview = ref(false)
const history = ref<NoteHistory[]>([])
const selectedHistory = ref<NoteHistory | null>(null)

// 编辑器工具
const textTools = [
  {
    name: 'bold',
    icon: Bold,
    tooltip: '粗体',
    prefix: '**',
    suffix: '**'
  },
  {
    name: 'italic',
    icon: Italic,
    tooltip: '斜体',
    prefix: '_',
    suffix: '_'
  }
]

const listTools = [
  {
    name: 'bullet-list',
    icon: List,
    tooltip: '无序列表',
    prefix: '- '
  }
]

const insertTools = [
  {
    name: 'link',
    icon: Link,
    tooltip: '插入链接',
    template: '[链接文字](URL)'
  },
  {
    name: 'image',
    icon: Picture,
    tooltip: '插入图片',
    template: '![图片描述](图片URL)'
  },
  {
    name: 'code',
    icon: Document,
    tooltip: '插入代码块',
    prefix: '```\n',
    suffix: '\n```'
  }
]

// 计算属性
const renderedContent = computed(() => {
  const html = marked(content.value)
  return DOMPurify.sanitize(html)
})

const selectedHistoryContent = computed(() => {
  if (!selectedHistory.value) return ''
  const html = marked(selectedHistory.value.content)
  return DOMPurify.sanitize(html)
})

// 方法
const switchMode = (newMode: 'edit' | 'preview') => {
  mode.value = newMode
}

const handleInput = (value: string) => {
  emit('update:content', value)
}

const applyTool = (tool: any) => {
  const textarea = document.querySelector('.editor-textarea textarea')
  if (!textarea) return

  const start = textarea.selectionStart
  const end = textarea.selectionEnd
  const selectedText = content.value.substring(start, end)

  let newText = ''
  if (tool.template) {
    newText = tool.template
  } else {
    newText = tool.prefix + selectedText + (tool.suffix || '')
  }

  content.value = 
    content.value.substring(0, start) +
    newText +
    content.value.substring(end)

  // 恢复焦点并选中新文本
  setTimeout(() => {
    textarea.focus()
    const newEnd = start + newText.length
    textarea.setSelectionRange(start, newEnd)
  }, 0)
}

const saveNote = async () => {
  if (!content.value.trim()) {
    ElMessage.warning('笔记内容不能为空')
    return
  }

  saving.value = true
  try {
    await noteApi.createNote({
      lesson_id: props.lessonId,
      content: content.value
    })
    ElMessage.success('保存成功')
    emit('save', content.value)
    loadHistory()
  } catch (error) {
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

const loadHistory = async () => {
  try {
    const { data } = await noteApi.getNoteHistory(props.lessonId)
    history.value = data
  } catch (error) {
    console.error('加载历史记录失败:', error)
  }
}

const formatDate = (date: string) => {
  return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
}

const previewHistory = (record: NoteHistory) => {
  selectedHistory.value = record
  showHistoryPreview.value = true
}

const restoreHistory = (record: NoteHistory) => {
  content.value = record.content
  showHistoryPreview.value = false
  showHistory.value = false
  ElMessage.success('已恢复到历史版本')
}

// 生命周期钩子
onMounted(() => {
  loadHistory()
})
</script>

<style scoped>
.note-editor {
  border: 1px solid var(--el-border-color);
  border-radius: 4px;
}

.editor-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px;
  border-bottom: 1px solid var(--el-border-color);
}

.left-tools,
.right-tools {
  display: flex;
  align-items: center;
  gap: 8px;
}

.editor-main {
  min-height: 400px;
}

.editor-textarea {
  height: 100%;
}

.markdown-preview {
  padding: 16px;
  min-height: 400px;
  overflow-y: auto;
}

.history-list {
  padding: 16px;
}

.history-preview {
  color: var(--el-text-color-regular);
  margin-bottom: 8px;
  white-space: pre-wrap;
}

.history-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

:deep(.el-timeline-item__content) {
  flex: 1;
}

:deep(.markdown-body) {
  font-family: var(--el-font-family);
  color: var(--el-text-color-primary);
}

:deep(.markdown-body h1),
:deep(.markdown-body h2),
:deep(.markdown-body h3),
:deep(.markdown-body h4),
:deep(.markdown-body h5),
:deep(.markdown-body h6) {
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
  line-height: 1.25;
}

:deep(.markdown-body p) {
  margin-top: 0;
  margin-bottom: 16px;
}

:deep(.markdown-body code) {
  padding: 0.2em 0.4em;
  margin: 0;
  font-size: 85%;
  background-color: var(--el-fill-color-light);
  border-radius: 3px;
}

:deep(.markdown-body pre) {
  padding: 16px;
  overflow: auto;
  font-size: 85%;
  line-height: 1.45;
  background-color: var(--el-fill-color);
  border-radius: 3px;
}

:deep(.markdown-body pre code) {
  display: inline;
  max-width: auto;
  padding: 0;
  margin: 0;
  overflow: visible;
  line-height: inherit;
  word-wrap: normal;
  background-color: transparent;
  border: 0;
}

:deep(.markdown-body blockquote) {
  padding: 0 1em;
  color: var(--el-text-color-secondary);
  border-left: 0.25em solid var(--el-border-color);
}

:deep(.markdown-body ul),
:deep(.markdown-body ol) {
  padding-left: 2em;
}

:deep(.markdown-body img) {
  max-width: 100%;
  box-sizing: content-box;
  background-color: var(--el-bg-color);
}
</style> 