<template>
  <div class="course-detail">
    <div class="header">
      <el-page-header @back="goBack" :content="course.title || '课程详情'" />
    </div>

    <el-row :gutter="20" v-loading="loading">
      <el-col :span="16">
        <!-- 课程主要内容 -->
        <el-card class="main-content">
          <div class="course-header">
            <h1>{{ course.title }}</h1>
            <div class="meta">
              <el-tag size="small">{{ getCategoryLabel(course.category) }}</el-tag>
              <el-tag size="small" type="warning">{{ getDifficultyLabel(course.difficulty_level) }}</el-tag>
              <span class="created-time">创建时间：{{ formatDate(course.created_at) }}</span>
            </div>
          </div>

          <div class="course-image">
            <img :src="course.image || '/default-course.jpg'" :alt="course.title">
          </div>

          <div class="description">
            <h2>课程描述</h2>
            <p>{{ course.description }}</p>
          </div>

          <div class="content" v-if="course.content">
            <h2>课程内容</h2>
            <div v-html="course.content"></div>
          </div>
        </el-card>
      </el-col>

      <el-col :span="8">
        <!-- 学习进度卡片 -->
        <el-card class="progress-card">
          <template #header>
            <div class="progress-header">
              <span>学习进度</span>
              <el-progress
                type="circle"
                :percentage="learningProgress.percentage || 0"
                :status="learningProgress.status"
              />
            </div>
          </template>
          <div class="progress-content">
            <div class="progress-item">
              <span>开始时间</span>
              <span>{{ formatDate(learningProgress.start_time) || '尚未开始' }}</span>
            </div>
            <div class="progress-item">
              <span>最近学习</span>
              <span>{{ formatDate(learningProgress.last_activity) || '尚未学习' }}</span>
            </div>
            <div class="progress-item">
              <span>当前得分</span>
              <span>{{ learningProgress.score || '暂无得分' }}</span>
            </div>
            <el-button type="primary" @click="startLearning" :disabled="loading">
              {{ learningProgress.percentage > 0 ? '继续学习' : '开始学习' }}
            </el-button>
          </div>
        </el-card>

        <!-- 相关课程推荐 -->
        <el-card class="related-courses">
          <template #header>
            <div class="card-header">
              <span>相关课程推荐</span>
            </div>
          </template>
          <div class="related-list">
            <div
              v-for="course in relatedCourses"
              :key="course.id"
              class="related-item"
              @click="viewCourse(course.id)"
            >
              <img :src="course.image || '/default-course.jpg'" :alt="course.title">
              <div class="related-info">
                <h4>{{ course.title }}</h4>
                <el-tag size="small">{{ getCategoryLabel(course.category) }}</el-tag>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { courseApi } from '@/api';

export default {
  name: 'CourseDetail',
  setup() {
    const route = useRoute();
    const router = useRouter();
    const loading = ref(false);

    const state = reactive({
      course: {},
      learningProgress: {},
      relatedCourses: []
    });

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

    // 方法定义
    const loadCourseDetail = async () => {
      loading.value = true;
      try {
        const courseId = route.params.id;
        const [courseDetail, progress] = await Promise.all([
          courseApi.getCourseDetail(courseId),
          courseApi.getLearningProgress(courseId)
        ]);
        
        state.course = courseDetail;
        state.learningProgress = progress;
        
        // 加载相关课程
        const relatedResponse = await courseApi.getCourses({
          category: courseDetail.category,
          exclude_id: courseId,
          limit: 3
        });
        state.relatedCourses = relatedResponse.filter(c => c.id !== courseId);
      } catch (error) {
        ElMessage.error('加载课程详情失败');
      } finally {
        loading.value = false;
      }
    };

    const startLearning = async () => {
      try {
        // 这里可以根据实际需求实现学习逻辑
        // 例如：跳转到学习页面、更新学习状态等
        router.push(`/courses/${route.params.id}/learn`);
      } catch (error) {
        ElMessage.error('操作失败');
      }
    };

    const goBack = () => {
      router.push('/courses');
    };

    const viewCourse = (courseId) => {
      router.push(`/courses/${courseId}`);
    };

    const getCategoryLabel = (value) => {
      const category = categories.find(c => c.value === value);
      return category ? category.label : value;
    };

    const getDifficultyLabel = (value) => {
      const level = difficultyLevels.find(l => l.value === value);
      return level ? level.label : value;
    };

    const formatDate = (date) => {
      if (!date) return '';
      return new Date(date).toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      });
    };

    // 生命周期钩子
    onMounted(() => {
      loadCourseDetail();
    });

    return {
      ...state,
      loading,
      startLearning,
      goBack,
      viewCourse,
      getCategoryLabel,
      getDifficultyLabel,
      formatDate
    };
  }
};
</script>

<style scoped>
.course-detail {
  padding: 20px;
}

.header {
  margin-bottom: 20px;
}

.main-content {
  margin-bottom: 20px;
}

.course-header {
  margin-bottom: 20px;
}

.course-header h1 {
  margin: 0 0 15px 0;
}

.meta {
  display: flex;
  gap: 10px;
  align-items: center;
}

.created-time {
  color: #666;
  font-size: 14px;
  margin-left: auto;
}

.course-image {
  width: 100%;
  height: 400px;
  margin-bottom: 20px;
  overflow: hidden;
  border-radius: 4px;
}

.course-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.description {
  margin-bottom: 30px;
}

.description h2 {
  margin-bottom: 15px;
}

.content h2 {
  margin-bottom: 15px;
}

.progress-card {
  margin-bottom: 20px;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.progress-content {
  padding: 10px 0;
}

.progress-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
}

.progress-item span:first-child {
  color: #666;
}

.related-courses .related-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.related-item {
  display: flex;
  gap: 10px;
  cursor: pointer;
  padding: 10px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.related-item:hover {
  background-color: #f5f7fa;
}

.related-item img {
  width: 80px;
  height: 60px;
  object-fit: cover;
  border-radius: 4px;
}

.related-info {
  flex: 1;
}

.related-info h4 {
  margin: 0 0 5px 0;
  font-size: 14px;
}
</style> 