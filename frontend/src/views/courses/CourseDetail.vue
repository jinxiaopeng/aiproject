<template>
  <div class="course-detail">
    <!-- 课程头部 -->
    <div class="course-header">
      <div class="header-content">
        <div class="course-info">
          <h1>{{ course.title }}</h1>
          <p class="description">{{ course.description }}</p>
          <div class="meta">
            <div class="meta-item">
              <el-icon><User /></el-icon>
              <span>{{ course.students }}人学习</span>
            </div>
            <div class="meta-item">
              <el-icon><Timer /></el-icon>
              <span>{{ course.duration }}</span>
            </div>
            <div class="meta-item">
              <el-icon><Star /></el-icon>
              <span>{{ course.rating }}分</span>
            </div>
            <div class="meta-item">
              <el-tag :type="getLevelType(course.level)">
                {{ getLevelText(course.level) }}
              </el-tag>
            </div>
          </div>
        </div>
        <div class="course-action">
          <el-button 
            type="primary" 
            size="large"
            :loading="enrolling"
            @click="handleEnroll"
          >
            {{ enrolled ? '继续学习' : '立即报名' }}
          </el-button>
          <div class="price" v-if="!enrolled">
            <span class="original-price">¥{{ course.originalPrice }}</span>
            <span class="current-price">¥{{ course.price }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 课程内容 -->
    <div class="course-content">
      <el-tabs v-model="activeTab">
        <!-- 课程章节 -->
        <el-tab-pane label="课程章节" name="chapters">
          <el-collapse v-model="activeChapters">
            <el-collapse-item
              v-for="chapter in course.chapters"
              :key="chapter.id"
              :title="chapter.title"
              :name="chapter.id"
            >
              <div 
                v-for="lesson in chapter.lessons" 
                :key="lesson.id"
                class="lesson-item"
                :class="{ 'is-locked': !enrolled && !lesson.free }"
                @click="handleLessonClick(lesson)"
              >
                <div class="lesson-info">
                  <el-icon v-if="!enrolled && !lesson.free"><Lock /></el-icon>
                  <el-icon v-else-if="lesson.completed"><Check /></el-icon>
                  <span class="lesson-title">{{ lesson.title }}</span>
                  <span class="lesson-duration">{{ lesson.duration }}</span>
                </div>
                <div class="lesson-status">
                  <el-tag 
                    v-if="lesson.free" 
                    type="success" 
                    size="small"
                  >
                    免费
                  </el-tag>
                </div>
              </div>
            </el-collapse-item>
          </el-collapse>
        </el-tab-pane>

        <!-- 课程介绍 -->
        <el-tab-pane label="课程介绍" name="introduction">
          <div class="introduction" v-html="course.introduction"></div>
        </el-tab-pane>

        <!-- 课程评价 -->
        <el-tab-pane label="课程评价" name="reviews">
          <div class="reviews">
            <div class="review-summary">
              <div class="rating-overview">
                <div class="rating-score">
                  <span class="score">{{ course.rating }}</span>
                  <el-rate
                    v-model="course.rating"
                    disabled
                    show-score
                    text-color="#ff9900"
                  />
                </div>
                <div class="rating-distribution">
                  <div 
                    v-for="(count, index) in course.ratingDistribution"
                    :key="index"
                    class="rating-bar"
                  >
                    <span class="star-label">{{ 5 - index }}星</span>
                    <div class="progress-bar">
                      <div 
                        class="progress" 
                        :style="{ width: `${(count / course.students) * 100}%` }"
                      ></div>
                    </div>
                    <span class="count">{{ count }}</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="review-list">
              <div 
                v-for="review in course.reviews"
                :key="review.id"
                class="review-item"
              >
                <div class="review-header">
                  <el-avatar :src="review.avatar" />
                  <div class="review-info">
                    <div class="reviewer">{{ review.username }}</div>
                    <div class="review-meta">
                      <el-rate
                        v-model="review.rating"
                        disabled
                        size="small"
                      />
                      <span class="review-time">{{ review.time }}</span>
                    </div>
                  </div>
                </div>
                <div class="review-content">{{ review.content }}</div>
              </div>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Timer, Star, Lock, Check } from '@element-plus/icons-vue'

export default defineComponent({
  name: 'CourseDetail',
  components: {
    User,
    Timer,
    Star,
    Lock,
    Check
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const activeTab = ref('chapters')
    const activeChapters = ref(['1'])
    const enrolling = ref(false)
    const enrolled = ref(false)
    
    // 模拟课程数据
    const course = ref({
      id: 1,
      title: 'Web安全基础入门',
      description: '从零开始学习Web安全，掌握基本概念和常见漏洞原理，提升安全防护能力',
      cover: '/images/courses/web-basic.jpg',
      level: 'beginner',
      students: 1234,
      duration: '12小时',
      rating: 4.5,
      price: 199,
      originalPrice: 299,
      introduction: `
        <h3>课程简介</h3>
        <p>本课程将带你深入了解Web安全的基础知识，通过理论学习和实战演练，掌握常见的Web漏洞原理和防护方法。</p>
        
        <h3>课程特点</h3>
        <ul>
          <li>系统的知识体系</li>
          <li>实战案例分析</li>
          <li>在线靶场演练</li>
          <li>专业讲师指导</li>
        </ul>
        
        <h3>适合人群</h3>
        <ul>
          <li>Web开发人员</li>
          <li>网络安全爱好者</li>
          <li>信息安全从业者</li>
          <li>对Web安全感兴趣的学习者</li>
        </ul>
      `,
      chapters: [
        {
          id: '1',
          title: '第1章 Web安全基础',
          lessons: [
            {
              id: 1,
              title: '1-1 Web安全概述',
              duration: '15:00',
              free: true,
              completed: true
            },
            {
              id: 2,
              title: '1-2 HTTP协议基础',
              duration: '20:00',
              free: true,
              completed: false
            }
          ]
        },
        {
          id: '2',
          title: '第2章 常见Web漏洞',
          lessons: [
            {
              id: 3,
              title: '2-1 SQL注入原理',
              duration: '30:00',
              free: false,
              completed: false
            },
            {
              id: 4,
              title: '2-2 XSS跨站脚本',
              duration: '25:00',
              free: false,
              completed: false
            }
          ]
        }
      ],
      ratingDistribution: [1000, 150, 50, 20, 14],
      reviews: [
        {
          id: 1,
          username: '张三',
          avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
          rating: 5,
          content: '课程内容很实用，讲解深入浅出，很适合入门学习。',
          time: '2023-12-01'
        },
        {
          id: 2,
          username: '李四',
          avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
          rating: 4,
          content: '老师讲解很清晰，但是希望能有更多的实战案例。',
          time: '2023-11-30'
        }
      ]
    })
    
    // 获取难度等级文本
    const getLevelText = (level: string) => {
      const levelMap = {
        beginner: '入门',
        intermediate: '中级',
        advanced: '高级'
      }
      return levelMap[level as keyof typeof levelMap]
    }
    
    // 获取难度等级标签类型
    const getLevelType = (level: string) => {
      const typeMap = {
        beginner: 'success',
        intermediate: 'warning',
        advanced: 'danger'
      }
      return typeMap[level as keyof typeof typeMap]
    }
    
    // 处理课程报名
    const handleEnroll = async () => {
      if (enrolled.value) {
        router.push(`/course/${course.value.id}/learn`)
        return
      }
      
      try {
        enrolling.value = true
        // TODO: 调用报名API
        await new Promise(resolve => setTimeout(resolve, 1000))
        enrolled.value = true
        ElMessage.success('报名成功')
      } catch (error) {
        ElMessage.error('报名失败，请重试')
      } finally {
        enrolling.value = false
      }
    }
    
    // 处理课时点击
    const handleLessonClick = (lesson: any) => {
      if (!enrolled.value && !lesson.free) {
        ElMessage.warning('请先报名课程')
        return
      }
      
      router.push(`/course/${course.value.id}/learn?lesson=${lesson.id}`)
    }
    
    onMounted(() => {
      // TODO: 根据路由参数加载课程数据
      const courseId = route.params.id
      console.log('Loading course:', courseId)
    })
    
    return {
      activeTab,
      activeChapters,
      enrolling,
      enrolled,
      course,
      getLevelText,
      getLevelType,
      handleEnroll,
      handleLessonClick
    }
  }
})
</script>

<style scoped>
.course-detail {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.course-header {
  background: linear-gradient(135deg, #1890ff 0%, #36cfc9 100%);
  color: #fff;
  padding: 40px 0;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 40px;
}

.course-info {
  flex: 1;
}

.course-info h1 {
  font-size: 32px;
  margin: 0 0 16px;
}

.description {
  font-size: 16px;
  opacity: 0.9;
  margin: 0 0 24px;
}

.meta {
  display: flex;
  gap: 24px;
  align-items: center;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}

.course-action {
  text-align: center;
}

.price {
  margin-top: 16px;
  font-size: 14px;
}

.original-price {
  text-decoration: line-through;
  opacity: 0.7;
  margin-right: 8px;
}

.current-price {
  font-size: 24px;
  font-weight: bold;
}

.course-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px 20px;
  background: #fff;
  border-radius: 8px;
  margin-top: -20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.lesson-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.lesson-item:hover {
  background-color: #f5f7fa;
}

.lesson-item.is-locked {
  cursor: not-allowed;
  opacity: 0.7;
}

.lesson-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.lesson-title {
  font-size: 14px;
}

.lesson-duration {
  font-size: 12px;
  color: var(--text-color-secondary);
  margin-left: 8px;
}

.introduction {
  line-height: 1.8;
  color: var(--text-color);
}

.introduction h3 {
  margin: 24px 0 16px;
  font-size: 18px;
}

.introduction ul {
  padding-left: 20px;
  margin: 16px 0;
}

.reviews {
  padding: 20px 0;
}

.review-summary {
  margin-bottom: 32px;
}

.rating-overview {
  display: flex;
  gap: 40px;
}

.rating-score {
  text-align: center;
}

.rating-score .score {
  font-size: 48px;
  font-weight: bold;
  color: #ff9900;
  line-height: 1;
  margin-bottom: 8px;
  display: block;
}

.rating-distribution {
  flex: 1;
}

.rating-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.star-label {
  width: 40px;
  font-size: 12px;
  color: var(--text-color-secondary);
}

.progress-bar {
  flex: 1;
  height: 16px;
  background-color: #f5f7fa;
  border-radius: 8px;
  overflow: hidden;
}

.progress {
  height: 100%;
  background-color: #ff9900;
  transition: width 0.3s ease;
}

.count {
  width: 40px;
  font-size: 12px;
  color: var(--text-color-secondary);
  text-align: right;
}

.review-list {
  border-top: 1px solid var(--border-color);
  padding-top: 24px;
}

.review-item {
  margin-bottom: 24px;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--border-color);
}

.review-header {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
}

.review-info {
  flex: 1;
}

.reviewer {
  font-weight: 500;
  margin-bottom: 4px;
}

.review-meta {
  display: flex;
  align-items: center;
  gap: 8px;
}

.review-time {
  font-size: 12px;
  color: var(--text-color-secondary);
}

.review-content {
  font-size: 14px;
  line-height: 1.6;
  color: var(--text-color);
}

@media (max-width: 768px) {
  .course-header {
    padding: 24px 0;
  }
  
  .header-content {
    flex-direction: column;
    gap: 24px;
  }
  
  .course-info h1 {
    font-size: 24px;
  }
  
  .meta {
    flex-wrap: wrap;
    gap: 16px;
  }
  
  .rating-overview {
    flex-direction: column;
    gap: 24px;
  }
}
</style> 