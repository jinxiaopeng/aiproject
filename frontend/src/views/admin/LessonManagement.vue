<template>
  <div class="lesson-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>课时管理</span>
          <el-button type="primary" @click="handleAddLesson">添加课时</el-button>
        </div>
      </template>
      
      <el-table
        v-loading="loading"
        :data="lessons"
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="title" label="标题" />
        <el-table-column prop="duration" label="时长" width="120" />
        <el-table-column prop="order" label="排序" width="100" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'published' ? 'success' : 'info'">
              {{ row.status === 'published' ? '已发布' : '草稿' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button-group>
              <el-button size="small" @click="handleEditLesson(row)">编辑</el-button>
              <el-button 
                size="small" 
                type="danger" 
                @click="handleDeleteLesson(row)"
              >删除</el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 添加/编辑课时对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '添加课时' : '编辑课时'"
      width="500px"
    >
      <el-form
        ref="formRef"
        :model="lessonForm"
        :rules="rules"
        label-width="80px"
      >
        <el-form-item label="标题" prop="title">
          <el-input v-model="lessonForm.title" />
        </el-form-item>
        <el-form-item label="时长" prop="duration">
          <el-input v-model="lessonForm.duration" />
        </el-form-item>
        <el-form-item label="排序" prop="order">
          <el-input-number v-model="lessonForm.order" :min="1" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="lessonForm.status">
            <el-option label="草稿" value="draft" />
            <el-option label="已发布" value="published" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, reactive } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage, ElMessageBox } from 'element-plus'

interface Lesson {
  id: number
  title: string
  duration: string
  order: number
  status: 'draft' | 'published'
}

export default defineComponent({
  name: 'LessonManagement',
  setup() {
    const loading = ref(false)
    const dialogVisible = ref(false)
    const dialogType = ref<'add' | 'edit'>('add')
    const formRef = ref<FormInstance>()
    
    // 模拟数据
    const lessons = ref<Lesson[]>([
      {
        id: 1,
        title: 'SQL注入基础',
        duration: '45分钟',
        order: 1,
        status: 'published'
      },
      {
        id: 2,
        title: 'XSS攻击防护',
        duration: '60分钟',
        order: 2,
        status: 'draft'
      }
    ])

    const lessonForm = reactive({
      id: 0,
      title: '',
      duration: '',
      order: 1,
      status: 'draft' as 'draft' | 'published'
    })

    const rules: FormRules = {
      title: [
        { required: true, message: '请输入课时标题', trigger: 'blur' },
        { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
      ],
      duration: [
        { required: true, message: '请输入课时时长', trigger: 'blur' }
      ],
      order: [
        { required: true, message: '请输入排序号', trigger: 'blur' }
      ],
      status: [
        { required: true, message: '请选择状态', trigger: 'change' }
      ]
    }

    const resetForm = () => {
      lessonForm.id = 0
      lessonForm.title = ''
      lessonForm.duration = ''
      lessonForm.order = 1
      lessonForm.status = 'draft'
    }

    const handleAddLesson = () => {
      dialogType.value = 'add'
      resetForm()
      dialogVisible.value = true
    }

    const handleEditLesson = (row: Lesson) => {
      dialogType.value = 'edit'
      Object.assign(lessonForm, row)
      dialogVisible.value = true
    }

    const handleDeleteLesson = (row: Lesson) => {
      ElMessageBox.confirm(
        '确定要删除这个课时吗？',
        '警告',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(() => {
        // 这里应该调用API删除课时
        const index = lessons.value.findIndex(item => item.id === row.id)
        if (index > -1) {
          lessons.value.splice(index, 1)
          ElMessage.success('删除成功')
        }
      }).catch(() => {
        // 取消删除
      })
    }

    const handleSubmit = async () => {
      if (!formRef.value) return
      
      await formRef.value.validate((valid, fields) => {
        if (valid) {
          // 这里应该调用API保存课时
          if (dialogType.value === 'add') {
            // 模拟添加
            const newLesson = {
              ...lessonForm,
              id: Math.max(...lessons.value.map(l => l.id)) + 1
            }
            lessons.value.push(newLesson)
            ElMessage.success('添加成功')
          } else {
            // 模拟编辑
            const index = lessons.value.findIndex(l => l.id === lessonForm.id)
            if (index > -1) {
              lessons.value[index] = { ...lessonForm }
              ElMessage.success('更新成功')
            }
          }
          dialogVisible.value = false
        }
      })
    }

    return {
      loading,
      lessons,
      dialogVisible,
      dialogType,
      lessonForm,
      rules,
      formRef,
      handleAddLesson,
      handleEditLesson,
      handleDeleteLesson,
      handleSubmit
    }
  }
})
</script>

<style scoped>
.lesson-management {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 