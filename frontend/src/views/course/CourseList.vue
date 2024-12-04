<template>
  <div class="course-list">
    <div class="header">
      <h2>课程列表</h2>
      <el-button v-if="isAdmin" type="primary" @click="handleCreateCourse">
        创建课程
      </el-button>
    </div>

    <!-- 筛选器 -->
    <div class="filters">
      <el-select v-model="filters.category" placeholder="课程分类" clearable>
        <el-option
          v-for="category in categories"
          :key="category.value"
          :label="category.label"
          :value="category.value"
        />
      </el-select>

      <el-select v-model="filters.difficulty" placeholder="难度等级" clearable>
        <el-option
          v-for="level in difficultyLevels"
          :key="level.value"
          :label="level.label"
          :value="level.value"
        />
      </el-select>

      <el-input
        v-model="filters.search"
        placeholder="搜索课程"
        prefix-icon="el-icon-search"
        clearable
      />
    </div>

    <!-- 课程列表 -->
    <div class="course-grid">
      <el-card
        v-for="course in filteredCourses"
        :key="course.id"
        class="course-card"
        :body-style="{ padding: '0px' }"
      >
        <div class="course-image">
          <img :src="course.image || '/default-course.jpg'" alt="课程封面">
        </div>
        <div class="course-content">
          <h3>{{ course.title }}</h3>
          <p class="description">{{ course.description }}</p>
          <div class="meta">
            <el-tag size="small">{{ getCategoryLabel(course.category) }}</el-tag>
            <el-tag size="small" type="warning">{{ getDifficultyLabel(course.difficulty_level) }}</el-tag>
          </div>
          <div class="actions">
            <el-button type="text" @click="handleViewCourse(course.id)">查看详情</el-button>
            <template v-if="isAdmin">
              <el-button type="text" @click="handleEditCourse(course.id)">编辑</el-button>
              <el-button type="text" @click="handleDeleteCourse(course.id)">删除</el-button>
            </template>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 创建/编辑课程对话框 -->
    <el-dialog
      :title="dialogTitle"
      :visible.sync="dialogVisible"
      width="50%"
    >
      <el-form :model="courseForm" :rules="rules" ref="courseForm" label-width="100px">
        <el-form-item label="课程名称" prop="title">
          <el-input v-model="courseForm.title" />
        </el-form-item>
        <el-form-item label="课程描述" prop="description">
          <el-input type="textarea" v-model="courseForm.description" rows="4" />
        </el-form-item>
        <el-form-item label="课程分类" prop="category">
          <el-select v-model="courseForm.category" placeholder="请选择课程分类">
            <el-option
              v-for="category in categories"
              :key="category.value"
              :label="category.label"
              :value="category.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="难度等级" prop="difficulty_level">
          <el-select v-model="courseForm.difficulty_level" placeholder="请选择难度等级">
            <el-option
              v-for="level in difficultyLevels"
              :key="level.value"
              :label="level.label"
              :value="level.value"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmitCourse">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { courseApi } from '@/api';
import { useStore } from 'vuex';

export default {
  name: 'CourseList',
  setup() {
    const store = useStore();
    const router = useRouter();
    const courseForm = ref(null);

    // 状态定义
    const state = reactive({
      courses: [],
      filters: {
        category: '',
        difficulty: '',
        search: ''
      },
      dialogVisible: false,
      courseForm: {
        title: '',
        description: '',
        category: '',
        difficulty_level: ''
      },
      isEditing: false
    });

    // 计算属性
    const isAdmin = computed(() => store.state.user?.role === 'admin');
    const dialogTitle = computed(() => state.isEditing ? '编辑课程' : '创建课程');

    // 常量定义
    const categories = [
      { value: 'web', label: 'Web安全' },
      { value: 'network', label: '网络安全' },
      { value: 'system', label: '系统安全' },
      { value: 'crypto', label: '密码学' }
    ];

    const difficultyLevels = [
      { value: 'beginner', label: '入门' },
      { value: 'intermediate', label: '中级' },
      { value: 'advanced', label: '高级' }
    ];

    const rules = {
      title: [
        { required: true, message: '请输入课程名称', trigger: 'blur' },
        { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' }
      ],
      description: [
        { required: true, message: '请输入课程描述', trigger: 'blur' }
      ],
      category: [
        { required: true, message: '请选择课程分类', trigger: 'change' }
      ],
      difficulty_level: [
        { required: true, message: '请选择难度等级', trigger: 'change' }
      ]
    };

    // 过滤后的课程列表
    const filteredCourses = computed(() => {
      return state.courses.filter(course => {
        const matchCategory = !state.filters.category || course.category === state.filters.category;
        const matchDifficulty = !state.filters.difficulty || course.difficulty_level === state.filters.difficulty;
        const matchSearch = !state.filters.search || 
          course.title.toLowerCase().includes(state.filters.search.toLowerCase()) ||
          course.description.toLowerCase().includes(state.filters.search.toLowerCase());
        return matchCategory && matchDifficulty && matchSearch;
      });
    });

    // 方法定义
    const loadCourses = async () => {
      try {
        const response = await courseApi.getCourses();
        state.courses = response;
      } catch (error) {
        ElMessage.error('获取课程列表失败');
      }
    };

    const handleCreateCourse = () => {
      state.isEditing = false;
      state.courseForm = {
        title: '',
        description: '',
        category: '',
        difficulty_level: ''
      };
      state.dialogVisible = true;
    };

    const handleEditCourse = async (courseId) => {
      try {
        const course = await courseApi.getCourseDetail(courseId);
        state.courseForm = { ...course };
        state.isEditing = true;
        state.dialogVisible = true;
      } catch (error) {
        ElMessage.error('获取课程详情失败');
      }
    };

    const handleDeleteCourse = async (courseId) => {
      try {
        await ElMessageBox.confirm('确定要删除这个课程吗？', '警告', {
          type: 'warning'
        });
        await courseApi.deleteCourse(courseId);
        ElMessage.success('删除成功');
        loadCourses();
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('删除失败');
        }
      }
    };

    const handleViewCourse = (courseId) => {
      router.push(`/courses/${courseId}`);
    };

    const handleSubmitCourse = async () => {
      if (!courseForm.value) return;
      
      try {
        await courseForm.value.validate();
        if (state.isEditing) {
          await courseApi.updateCourse(state.courseForm.id, state.courseForm);
          ElMessage.success('更新成功');
        } else {
          await courseApi.createCourse(state.courseForm);
          ElMessage.success('创建成功');
        }
        state.dialogVisible = false;
        loadCourses();
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error(state.isEditing ? '更新失败' : '创建失败');
        }
      }
    };

    const getCategoryLabel = (value) => {
      const category = categories.find(c => c.value === value);
      return category ? category.label : value;
    };

    const getDifficultyLabel = (value) => {
      const level = difficultyLevels.find(l => l.value === value);
      return level ? level.label : value;
    };

    // 生命周期钩子
    onMounted(() => {
      loadCourses();
    });

    return {
      ...state,
      isAdmin,
      dialogTitle,
      categories,
      difficultyLevels,
      rules,
      filteredCourses,
      courseForm,
      handleCreateCourse,
      handleEditCourse,
      handleDeleteCourse,
      handleViewCourse,
      handleSubmitCourse,
      getCategoryLabel,
      getDifficultyLabel
    };
  }
};
</script>

<style scoped>
.course-list {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.filters {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
}

.course-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.course-card {
  transition: transform 0.3s;
}

.course-card:hover {
  transform: translateY(-5px);
}

.course-image {
  height: 200px;
  overflow: hidden;
}

.course-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.course-content {
  padding: 15px;
}

.course-content h3 {
  margin: 0 0 10px 0;
  font-size: 18px;
}

.description {
  color: #666;
  margin-bottom: 10px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.meta {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}

.actions {
  display: flex;
  justify-content: flex-start;
  gap: 15px;
}
</style> 