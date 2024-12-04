<template>
  <div class="user-management">
    <!-- 搜索和操作栏 -->
    <div class="toolbar">
      <div class="search-box">
        <el-input
          v-model="searchQuery"
          placeholder="搜索用户..."
          class="search-input"
          :prefix-icon="Search"
          clearable
          @input="handleSearch"
        />
        <el-select
          v-model="filterRole"
          placeholder="角色"
          class="filter-select"
          clearable
        >
          <el-option label="管理员" value="admin" />
          <el-option label="教师" value="teacher" />
          <el-option label="学生" value="student" />
        </el-select>
        <el-select
          v-model="filterStatus"
          placeholder="状态"
          class="filter-select"
          clearable
        >
          <el-option label="正常" value="active" />
          <el-option label="禁用" value="disabled" />
        </el-select>
      </div>
      <div class="actions">
        <el-button type="primary" @click="handleAdd">
          <el-icon><Plus /></el-icon>
          添加用户
        </el-button>
        <el-button type="success" @click="handleExport">
          <el-icon><Download /></el-icon>
          导出数据
        </el-button>
      </div>
    </div>

    <!-- 用户表格 -->
    <el-table
      v-loading="loading"
      :data="filteredUsers"
      style="width: 100%"
      border
    >
      <el-table-column type="selection" width="55" />
      
      <el-table-column label="用户信息" min-width="200">
        <template #default="{ row }">
          <div class="user-info">
            <el-avatar :size="40" :src="row.avatar" />
            <div class="user-details">
              <div class="username">{{ row.username }}</div>
              <div class="email">{{ row.email }}</div>
            </div>
          </div>
        </template>
      </el-table-column>
      
      <el-table-column prop="role" label="角色" width="120">
        <template #default="{ row }">
          <el-tag :type="getRoleType(row.role)">
            {{ getRoleText(row.role) }}
          </el-tag>
        </template>
      </el-table-column>
      
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.status === 'active' ? 'success' : 'danger'">
            {{ row.status === 'active' ? '正常' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      
      <el-table-column prop="lastLogin" label="最后登录" width="180" />
      
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button-group>
            <el-button 
              size="small" 
              @click="handleEdit(row)"
            >
              编辑
            </el-button>
            <el-button 
              size="small" 
              type="danger" 
              @click="handleDelete(row)"
            >
              删除
            </el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <div class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <!-- 用户表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '添加用户' : '编辑用户'"
      width="500px"
    >
      <el-form
        ref="formRef"
        :model="userForm"
        :rules="rules"
        label-width="80px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="userForm.username" />
        </el-form-item>
        
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="userForm.email" />
        </el-form-item>
        
        <el-form-item 
          label="密码" 
          prop="password"
          v-if="dialogType === 'add'"
        >
          <el-input
            v-model="userForm.password"
            type="password"
            show-password
          />
        </el-form-item>
        
        <el-form-item label="角色" prop="role">
          <el-select v-model="userForm.role" style="width: 100%">
            <el-option label="管理员" value="admin" />
            <el-option label="教师" value="teacher" />
            <el-option label="学生" value="student" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="状态" prop="status">
          <el-switch
            v-model="userForm.status"
            :active-value="'active'"
            :inactive-value="'disabled'"
          />
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
import { defineComponent, ref, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Plus, Download } from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'

interface User {
  id: number
  username: string
  email: string
  avatar: string
  role: string
  status: string
  lastLogin: string
}

export default defineComponent({
  name: 'UserManagement',
  components: {
    Search,
    Plus,
    Download
  },
  setup() {
    const loading = ref(false)
    const searchQuery = ref('')
    const filterRole = ref('')
    const filterStatus = ref('')
    const currentPage = ref(1)
    const pageSize = ref(10)
    const total = ref(100)
    const dialogVisible = ref(false)
    const dialogType = ref<'add' | 'edit'>('add')
    const formRef = ref<FormInstance>()
    
    // 用户表单
    const userForm = ref({
      id: 0,
      username: '',
      email: '',
      password: '',
      role: 'student',
      status: 'active'
    })
    
    // 表单验证规则
    const rules: FormRules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
      ],
      email: [
        { required: true, message: '请输入邮箱地址', trigger: 'blur' },
        { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
      ],
      role: [
        { required: true, message: '请选择角色', trigger: 'change' }
      ]
    }
    
    // 模拟用户数据
    const users = ref<User[]>([
      {
        id: 1,
        username: '张三',
        email: 'zhangsan@example.com',
        avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
        role: 'admin',
        status: 'active',
        lastLogin: '2023-12-01 10:30:00'
      },
      {
        id: 2,
        username: '李四',
        email: 'lisi@example.com',
        avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
        role: 'teacher',
        status: 'active',
        lastLogin: '2023-12-01 09:15:00'
      },
      {
        id: 3,
        username: '王五',
        email: 'wangwu@example.com',
        avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
        role: 'student',
        status: 'disabled',
        lastLogin: '2023-11-30 15:45:00'
      }
    ])
    
    // 过滤用户
    const filteredUsers = computed(() => {
      return users.value.filter(user => {
        const matchQuery = user.username.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                          user.email.toLowerCase().includes(searchQuery.value.toLowerCase())
        const matchRole = !filterRole.value || user.role === filterRole.value
        const matchStatus = !filterStatus.value || user.status === filterStatus.value
        
        return matchQuery && matchRole && matchStatus
      })
    })
    
    // 获取角色文本
    const getRoleText = (role: string) => {
      const roleMap: { [key: string]: string } = {
        admin: '管理员',
        teacher: '教师',
        student: '学生'
      }
      return roleMap[role] || role
    }
    
    // 获取角色标签类型
    const getRoleType = (role: string) => {
      const typeMap: { [key: string]: string } = {
        admin: 'danger',
        teacher: 'warning',
        student: 'info'
      }
      return typeMap[role] || 'info'
    }
    
    // 搜索处理
    const handleSearch = () => {
      currentPage.value = 1
      // TODO: 实现搜索逻辑
    }
    
    // 分页处理
    const handleSizeChange = (val: number) => {
      pageSize.value = val
      // TODO: 重新加载数据
    }
    
    const handleCurrentChange = (val: number) => {
      currentPage.value = val
      // TODO: 重新加载数据
    }
    
    // 添加用户
    const handleAdd = () => {
      dialogType.value = 'add'
      userForm.value = {
        id: 0,
        username: '',
        email: '',
        password: '',
        role: 'student',
        status: 'active'
      }
      dialogVisible.value = true
    }
    
    // 编辑用户
    const handleEdit = (row: User) => {
      dialogType.value = 'edit'
      userForm.value = {
        ...userForm.value,
        id: row.id,
        username: row.username,
        email: row.email,
        role: row.role,
        status: row.status
      }
      dialogVisible.value = true
    }
    
    // 删除用户
    const handleDelete = (row: User) => {
      ElMessageBox.confirm(
        '确定要删除该用户吗？此操作不可恢复',
        '警告',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(async () => {
        try {
          // TODO: 调用删除API
          await new Promise(resolve => setTimeout(resolve, 1000))
          ElMessage.success('删除成功')
        } catch (error) {
          ElMessage.error('删除失败')
        }
      }).catch(() => {
        // 取消删除
      })
    }
    
    // 导出数据
    const handleExport = () => {
      // TODO: 实现导出逻辑
      ElMessage.success('导出成功')
    }
    
    // 提交表单
    const handleSubmit = async () => {
      if (!formRef.value) return
      
      await formRef.value.validate(async (valid, fields) => {
        if (valid) {
          try {
            // TODO: 调用保存API
            await new Promise(resolve => setTimeout(resolve, 1000))
            ElMessage.success(dialogType.value === 'add' ? '添加成功' : '更新成功')
            dialogVisible.value = false
          } catch (error) {
            ElMessage.error(dialogType.value === 'add' ? '添加失败' : '更新失败')
          }
        }
      })
    }
    
    return {
      loading,
      searchQuery,
      filterRole,
      filterStatus,
      currentPage,
      pageSize,
      total,
      dialogVisible,
      dialogType,
      formRef,
      userForm,
      rules,
      filteredUsers,
      getRoleText,
      getRoleType,
      handleSearch,
      handleSizeChange,
      handleCurrentChange,
      handleAdd,
      handleEdit,
      handleDelete,
      handleExport,
      handleSubmit
    }
  }
})
</script>

<style scoped>
.user-management {
  padding: 20px;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.search-box {
  display: flex;
  gap: 16px;
}

.search-input {
  width: 300px;
}

.filter-select {
  width: 160px;
}

.actions {
  display: flex;
  gap: 16px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-details {
  display: flex;
  flex-direction: column;
}

.username {
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 4px;
}

.email {
  font-size: 12px;
  color: var(--text-color-secondary);
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

@media (max-width: 768px) {
  .toolbar {
    flex-direction: column;
    gap: 16px;
  }
  
  .search-box {
    flex-direction: column;
  }
  
  .search-input,
  .filter-select {
    width: 100%;
  }
  
  .actions {
    flex-direction: column;
  }
  
  .actions .el-button {
    width: 100%;
  }
}
</style> 