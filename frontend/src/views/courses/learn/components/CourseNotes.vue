<template>
  <div class="course-notes">
    <div class="notes-header">
      <h3>课程笔记</h3>
      <div class="header-actions">
        <el-button type="primary" size="small" @click="addNote">
          <el-icon><Plus /></el-icon>添加笔记
        </el-button>
        <el-button type="success" size="small" @click="exportNotes">
          <el-icon><Download /></el-icon>导出笔记
        </el-button>
      </div>
    </div>

    <div class="notes-content">
      <el-empty v-if="!notes.length" description="暂无笔记">
        <el-button type="primary" @click="addNote">立即添加</el-button>
      </el-empty>

      <div v-else class="notes-list">
        <div v-for="note in notes" :key="note.id" class="note-item">
          <div class="note-header">
            <div class="time-info">
              <el-tag size="small" @click="seekToTime(note.videoTime)">
                {{ formatTime(note.videoTime) }}
              </el-tag>
              <span class="create-time">{{ formatDate(note.createTime) }}</span>
            </div>
            <div class="actions">
              <el-button type="primary" link @click="editNote(note)">
                <el-icon><Edit /></el-icon>
              </el-button>
              <el-button type="info" link @click="previewNote(note.content)">
                <el-icon><View /></el-icon>
              </el-button>
              <el-button type="danger" link @click="deleteNote(note)">
                <el-icon><Delete /></el-icon>
              </el-button>
            </div>
          </div>
          
          <div class="note-content" v-html="renderMarkdown(note.content)"></div>
          
          <div class="note-footer">
            <div class="tags">
              <el-tag 
                v-for="tag in note.tags" 
                :key="tag"
                size="small"
                effect="plain"
                class="tag"
              >
                {{ tag }}
              </el-tag>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 笔记编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="editingNote ? '编辑笔记' : '添加笔记'"
      width="1400px"
      class="note-edit-dialog"
      @close="handleDialogClose"
    >
      <div class="note-form">
        <div class="form-header">
          <span class="video-time">视频时间点：{{ formatTime(currentTime) }}</span>
          <el-button type="primary" link @click="insertScreenshot">
            <el-icon><Picture /></el-icon>插入截图
          </el-button>
        </div>

        <div class="edit-preview-container">
          <div class="edit-section">
            <el-form ref="formRef" :model="noteForm" :rules="rules">
              <el-form-item prop="content">
                <el-input
                  v-model="noteForm.content"
                  type="textarea"
                  :rows="20"
                  placeholder="输入笔记内容（支持 Markdown 格式）"
                />
              </el-form-item>

              <el-form-item label="标签">
                <el-select
                  v-model="noteForm.tags"
                  multiple
                  filterable
                  allow-create
                  default-first-option
                  placeholder="添加标签"
                >
                  <el-option
                    v-for="tag in commonTags"
                    :key="tag"
                    :label="tag"
                    :value="tag"
                  />
                </el-select>
              </el-form-item>
            </el-form>
          </div>

          <div class="preview-section">
            <div class="preview-header">预览</div>
            <div class="markdown-preview" v-html="renderMarkdown(noteForm.content || '暂无内容')"></div>
          </div>
        </div>
      </div>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveNote">保存</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 笔记预览对话框 -->
    <el-dialog
      v-model="previewVisible"
      title="笔记预览"
      width="600px"
    >
      <div class="markdown-preview" v-html="renderMarkdown(previewContent)"></div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Edit, Delete, Picture, Download, View } from '@element-plus/icons-vue'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import { useRoute } from 'vue-router'

interface Note {
  id: number
  content: string
  videoTime: number
  createTime: number
  updateTime?: number
  tags: string[]
}

const props = defineProps<{
  currentTime: number,
  videoRef?: HTMLVideoElement
}>()

const emit = defineEmits<{
  (e: 'seek', time: number): void
}>()

// 状态
const notes = ref<Note[]>([])
const dialogVisible = ref(false)
const editingNote = ref<Note | null>(null)
const noteForm = ref({
  content: '',
  tags: [] as string[]
})
const previewVisible = ref(false)
const previewContent = ref('')
const wasVideoPlaying = ref(false)  // 记录视频是否在播放

// 常用标签
const commonTags = [
  '重要概念',
  '实战技巧',
  '疑难点',
  '面试题',
  '待复习'
]

// 表单校验规则
const rules = {
  content: [
    { required: true, message: '请输入笔记内容', trigger: 'blur' }
  ]
}

// 格式化时间
const formatTime = (seconds: number) => {
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = Math.floor(seconds % 60)
  return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`
}

const formatDate = (timestamp: number) => {
  return new Date(timestamp).toLocaleString('zh-CN', {
    month: 'numeric',
    day: 'numeric',
    hour: 'numeric',
    minute: 'numeric'
  })
}

// Markdown 渲染
const renderMarkdown = (content: string) => {
  const html = marked(content)
  return DOMPurify.sanitize(html)
}

// 监听对话框关闭
const handleDialogClose = async () => {
  dialogVisible.value = false
  // 如果之前视频在播放，则恢复播放
  if (wasVideoPlaying.value && props.videoRef) {
    try {
      await props.videoRef.play()
    } catch (error) {
      console.error('Failed to resume video:', error)
    }
  }
}

// 添加笔记
const addNote = async () => {
  try {
    // 记录视频状态并暂停
    if (props.videoRef) {
      wasVideoPlaying.value = !props.videoRef.paused
      console.log('Video was playing:', wasVideoPlaying.value)
      await props.videoRef.pause()
      console.log('Video paused:', props.videoRef.paused)
    } else {
      console.warn('Video reference not found')
    }
    
    editingNote.value = null
    noteForm.value = {
      content: '',
      tags: []
    }
    dialogVisible.value = true
  } catch (error) {
    console.error('Failed to pause video:', error)
  }
}

// 编辑笔记
const editNote = async (note: Note) => {
  try {
    // 记录视频状态并暂停
    if (props.videoRef) {
      wasVideoPlaying.value = !props.videoRef.paused
      console.log('Video was playing:', wasVideoPlaying.value)
      await props.videoRef.pause()
      console.log('Video paused:', props.videoRef.paused)
    } else {
      console.warn('Video reference not found')
    }

    editingNote.value = note
    noteForm.value = {
      content: note.content,
      tags: [...note.tags]
    }
    dialogVisible.value = true
  } catch (error) {
    console.error('Failed to pause video:', error)
  }
}

// 删除笔记
const deleteNote = async (note: Note) => {
  try {
    await ElMessageBox.confirm('确定要删除这条笔记吗？', '提示', {
      type: 'warning'
    })
    const index = notes.value.findIndex(n => n.id === note.id)
    if (index !== -1) {
      notes.value.splice(index, 1)
      ElMessage.success('笔记已删除')
      saveNotesToStorage()
    }
  } catch {
    // 用户取消删除
  }
}

// 保存笔记
const saveNote = () => {
  if (editingNote.value) {
    // 更新笔记
    const index = notes.value.findIndex(n => n.id === editingNote.value!.id)
    if (index !== -1) {
      notes.value[index] = {
        ...editingNote.value,
        content: noteForm.value.content,
        tags: noteForm.value.tags,
        updateTime: Date.now()
      }
    }
  } else {
    // 添加新笔记
    const newNote: Note = {
      id: Date.now(),
      content: noteForm.value.content,
      videoTime: props.currentTime,
      createTime: Date.now(),
      tags: noteForm.value.tags
    }
    notes.value.push(newNote)
  }
  
  dialogVisible.value = false
  ElMessage.success(editingNote.value ? '笔记已更新' : '笔记已添加')
  saveNotesToStorage()
}

// 插入视频截图
const insertScreenshot = async () => {
  try {
    const video = props.videoRef || document.querySelector('.video-player video')
    if (!video) {
      throw new Error('未找到视频元素')
    }

    // 暂停视频以确保截图清晰
    const wasPlaying = !video.paused
    if (wasPlaying) {
      await video.pause()
    }

    const canvas = document.createElement('canvas')
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight
    const ctx = canvas.getContext('2d')
    if (!ctx) {
      throw new Error('无法创建canvas上下文')
    }

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height)
    
    // 压缩图片质量以减小大小
    const imageUrl = canvas.toDataURL('image/jpeg', 0.8)
    
    // 在光标位置插入图片markdown
    const textarea = document.querySelector('.el-textarea__inner') as HTMLTextAreaElement
    if (!textarea) {
      throw new Error('未找到文本输入框')
    }

    const cursorPos = textarea.selectionStart
    const textBefore = noteForm.value.content.substring(0, cursorPos)
    const textAfter = noteForm.value.content.substring(cursorPos)
    
    noteForm.value.content = `${textBefore}\n![截图](${imageUrl})\n${textAfter}`
    ElMessage.success('截图已插入')

    // 如果之前在播放，则恢复播放
    if (wasPlaying) {
      await video.play()
    }
  } catch (error) {
    console.error('截图失败:', error)
    ElMessage.error('截图失败，请重试')
  }
}

// 跳转到视频时间点
const seekToTime = (time: number) => {
  emit('seek', time)
}

// 从本地存储加载笔记
const loadNotesFromStorage = () => {
  const courseId = route.params.id
  const storedNotes = localStorage.getItem(`course-${courseId}-notes`)
  if (storedNotes) {
    try {
      notes.value = JSON.parse(storedNotes)
    } catch (error) {
      console.error('Failed to parse stored notes:', error)
    }
  }
}

// 保存笔记到本地存储
const saveNotesToStorage = () => {
  const courseId = route.params.id
  localStorage.setItem(`course-${courseId}-notes`, JSON.stringify(notes.value))
}

// 导出笔记
const exportNotes = () => {
  const notesContent = notes.value.map(note => {
    return `## 时间点：${formatTime(note.videoTime)}
创建时间：${formatDate(note.createTime)}
标签：${note.tags.join(', ')}

${note.content}
---`
  }).join('\n\n')

  const blob = new Blob([notesContent], { type: 'text/markdown' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `课程笔记-${new Date().toLocaleDateString()}.md`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
  ElMessage.success('笔记导出成功')
}

// 预览笔记
const previewNote = (content: string) => {
  previewContent.value = content
  previewVisible.value = true
}

// 组件挂载时加载笔记
onMounted(() => {
  loadNotesFromStorage()
})
</script>

<style lang="scss" scoped>
.course-notes {
  background: var(--el-bg-color-overlay);
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);

  .notes-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;

    h3 {
      margin: 0;
      font-size: 1.125rem;
      color: var(--el-text-color-primary);
    }
  }

  .notes-content {
    min-height: 200px;
  }

  .notes-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .note-item {
    background: var(--el-bg-color);
    border-radius: 6px;
    padding: 1rem;
    border: 1px solid var(--el-border-color-light);

    .note-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.75rem;

      .time-info {
        display: flex;
        align-items: center;
        gap: 0.75rem;

        .create-time {
          color: var(--el-text-color-secondary);
          font-size: 0.875rem;
        }
      }

      .actions {
        display: flex;
        gap: 0.5rem;
      }
    }

    .note-content {
      color: var(--el-text-color-regular);
      line-height: 1.6;
      margin-bottom: 0.75rem;

      :deep(p) {
        margin: 0.5em 0;
      }

      :deep(img) {
        max-width: 200px;  // 限制图片最大宽度
        height: auto;
        border: 1px solid var(--el-border-color-light);
        border-radius: 4px;
        margin: 0.5em 0;
        cursor: pointer;  // 添加鼠标手型
        transition: transform 0.2s;  // 添加过渡效果

        &:hover {
          transform: scale(1.5);  // 鼠标悬停时放大
        }
      }

      :deep(code) {
        background: var(--el-fill-color-light);
        padding: 0.2em 0.4em;
        border-radius: 3px;
        font-size: 0.875em;
      }
    }

    .note-footer {
      .tags {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
      }
    }
  }

  .header-actions {
    display: flex;
    gap: 8px;
  }

  .markdown-preview {
    padding: 16px;
    background: var(--el-bg-color-page);
    border-radius: 4px;
    
    :deep(img) {
      max-width: 100%;
      height: auto;
    }
    
    :deep(p) {
      line-height: 1.6;
      margin: 1em 0;
    }
    
    :deep(h1, h2, h3, h4, h5, h6) {
      margin: 1em 0 0.5em;
    }
  }
}

.note-form {
  .form-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;

    .video-time {
      color: var(--el-text-color-secondary);
    }
  }
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 1rem;
}

.note-edit-dialog {
  :deep(.el-dialog__body) {
    padding: 20px;
  }
}

.edit-preview-container {
  display: flex;
  gap: 20px;
  margin-top: 1rem;
  height: 600px;  // 增加高度

  .edit-section {
    flex: 1;
    min-width: 0;
    
    :deep(.el-form-item__content) {
      height: calc(100% - 32px);  // 减去标签的高度
      
      .el-textarea {
        height: 100%;
        
        textarea {
          height: 100%;
          font-family: monospace;
          resize: none;
        }
      }
    }
  }

  .preview-section {
    flex: 1;
    min-width: 0;
    border: 1px solid var(--el-border-color-light);
    border-radius: 4px;
    display: flex;
    flex-direction: column;
    
    .preview-header {
      padding: 8px 12px;
      border-bottom: 1px solid var(--el-border-color-light);
      font-weight: 500;
      color: var(--el-text-color-primary);
      background-color: var(--el-fill-color-light);
    }

    .markdown-preview {
      flex: 1;
      padding: 12px;
      overflow-y: auto;
      background: var(--el-bg-color-page);

      :deep(img) {
        max-width: 100%;
        height: auto;
        border: 1px solid var(--el-border-color-light);
        border-radius: 4px;
        margin: 0.5em 0;
      }

      :deep(p) {
        margin: 0.5em 0;
      }

      :deep(pre) {
        background: var(--el-fill-color-light);
        padding: 1em;
        border-radius: 4px;
        overflow-x: auto;
      }

      :deep(code) {
        background: var(--el-fill-color-light);
        padding: 0.2em 0.4em;
        border-radius: 3px;
        font-size: 0.875em;
      }

      :deep(blockquote) {
        margin: 1em 0;
        padding-left: 1em;
        border-left: 4px solid var(--el-border-color);
        color: var(--el-text-color-secondary);
      }

      :deep(table) {
        border-collapse: collapse;
        width: 100%;
        margin: 1em 0;

        th, td {
          border: 1px solid var(--el-border-color);
          padding: 0.5em;
        }

        th {
          background: var(--el-fill-color-light);
        }
      }

      :deep(ul), :deep(ol) {
        padding-left: 2em;
        margin: 0.5em 0;
      }
    }
  }
}
</style> 