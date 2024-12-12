<template>
  <div class="course-notes">
    <div class="notes-header">
      <h3>课程笔记</h3>
      <el-button type="primary" :icon="Plus" @click="addNote">添加笔记</el-button>
    </div>

    <!-- 笔记列表 -->
    <div class="notes-list">
      <el-empty v-if="!notes.length" description="暂无笔记" />
      <div v-else v-for="note in notes" :key="note.id" class="note-item">
        <div class="note-time">
          <el-tag size="small">{{ formatTime(note.video_time) }}</el-tag>
          <span class="date">{{ formatDate(note.created_at) }}</span>
        </div>
        <div class="note-content" v-if="!note.editing">
          {{ note.content }}
          <div class="note-actions">
            <el-button type="primary" link @click="editNote(note)">编辑</el-button>
            <el-button type="danger" link @click="deleteNote(note)">删除</el-button>
          </div>
        </div>
        <div v-else class="note-edit">
          <el-input
            v-model="note.editContent"
            type="textarea"
            :rows="3"
            placeholder="请输入笔记内容"
          />
          <div class="edit-actions">
            <el-button @click="cancelEdit(note)">取消</el-button>
            <el-button type="primary" @click="saveNote(note)">保存</el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 添加笔记对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="添加笔记"
      width="500px"
    >
      <el-form :model="newNote" label-position="top">
        <el-form-item label="视频时间点">
          <span>{{ formatTime(currentTime) }}</span>
        </el-form-item>
        <el-form-item label="笔记内容">
          <el-input
            v-model="newNote.content"
            type="textarea"
            :rows="4"
            placeholder="请输入笔记内容"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitNote">
            确认
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import dayjs from 'dayjs'

interface Note {
  id: number
  content: string
  video_time: number
  created_at: string
  editing?: boolean
  editContent?: string
}

const props = defineProps<{
  currentTime: number
  chapterId: number
}>()

const notes = ref<Note[]>([])
const dialogVisible = ref(false)
const newNote = ref({
  content: ''
})

// 添加笔记
const addNote = () => {
  newNote.value.content = ''
  dialogVisible.value = true
}

// 提交笔记
const submitNote = async () => {
  if (!newNote.value.content.trim()) {
    ElMessage.warning('请输入笔记内容')
    return
  }

  try {
    // TODO: 调用API保存笔记
    const note: Note = {
      id: Date.now(),
      content: newNote.value.content,
      video_time: props.currentTime,
      created_at: new Date().toISOString()
    }
    notes.value.unshift(note)
    dialogVisible.value = false
    ElMessage.success('添加笔记成功')
  } catch (error) {
    ElMessage.error('添加笔记失败')
  }
}

// 编辑笔记
const editNote = (note: Note) => {
  note.editing = true
  note.editContent = note.content
}

// 取消编辑
const cancelEdit = (note: Note) => {
  note.editing = false
  note.editContent = undefined
}

// 保存笔记
const saveNote = async (note: Note) => {
  if (!note.editContent?.trim()) {
    ElMessage.warning('请输入笔记内容')
    return
  }

  try {
    // TODO: 调用API更新笔记
    note.content = note.editContent
    note.editing = false
    ElMessage.success('更新笔记成功')
  } catch (error) {
    ElMessage.error('更新笔记失败')
  }
}

// 删除笔记
const deleteNote = async (note: Note) => {
  try {
    // TODO: 调用API删除笔记
    const index = notes.value.findIndex(n => n.id === note.id)
    if (index > -1) {
      notes.value.splice(index, 1)
    }
    ElMessage.success('删除笔记成功')
  } catch (error) {
    ElMessage.error('删除笔记失败')
  }
}

// 格式化视频时间
const formatTime = (seconds: number) => {
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = Math.floor(seconds % 60)
  return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`
}

// 格式化日期
const formatDate = (date: string) => {
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}
</script>

<style lang="scss" scoped>
.course-notes {
  padding: 1rem;

  .notes-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;

    h3 {
      margin: 0;
      font-size: 1.2rem;
    }
  }

  .notes-list {
    .note-item {
      padding: 1rem;
      border: 1px solid var(--el-border-color-light);
      border-radius: 4px;
      margin-bottom: 1rem;

      .note-time {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.5rem;

        .date {
          color: var(--el-text-color-secondary);
          font-size: 0.9rem;
        }
      }

      .note-content {
        line-height: 1.6;
        color: var(--el-text-color-regular);
      }

      .note-actions {
        margin-top: 0.5rem;
        display: flex;
        gap: 1rem;
      }

      .note-edit {
        .edit-actions {
          margin-top: 1rem;
          display: flex;
          justify-content: flex-end;
          gap: 1rem;
        }
      }
    }
  }
}
</style> 