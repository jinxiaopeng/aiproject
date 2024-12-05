<template>
  <div class="course-list">
    <el-row :gutter="20">
      <el-col v-for="course in courses" :key="course.id" :span="8">
        <el-card class="course-card" shadow="hover">
          <img :src="course.cover" class="course-cover" />
          <div class="course-info">
            <h3>{{ course.title }}</h3>
            <p class="description">{{ course.description }}</p>
            <div class="stats">
              <span>
                <el-icon><User /></el-icon>
                {{ course.students }} 学员
              </span>
              <span>
                <el-icon><Clock /></el-icon>
                {{ course.duration }} 小时
              </span>
            </div>
            <el-button type="primary" @click="handleEnroll(course.id)">
              立即报名
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { User, Timer as Clock } from '@element-plus/icons-vue'

interface Course {
  id: number
  title: string
  description: string
  cover: string
  students: number
  duration: number
}

// 模拟数据
const courses = ref<Course[]>([
  {
    id: 1,
    title: 'Web安全基础',
    description: '学习Web安全的基本概念和常见漏洞，掌握基本的渗透测试技能。',
    cover: 'https://via.placeholder.com/300x200',
    students: 1234,
    duration: 12
  },
  {
    id: 2,
    title: '渗透测试实战',
    description: '通过实际案例，学习渗透测试的方法和技巧，提升实战能力。',
    cover: 'https://via.placeholder.com/300x200',
    students: 890,
    duration: 16
  },
  {
    id: 3,
    title: '代码审计入门',
    description: '学习代码审计的基本方法，发现和修复代码中的安全漏洞。',
    cover: 'https://via.placeholder.com/300x200',
    students: 567,
    duration: 10
  }
])

const handleEnroll = (courseId: number) => {
  ElMessage.success(`已成功报名课程 ${courseId}`)
}
</script>

<style lang="scss" scoped>
.course-list {
  padding: 20px;
  background: #0a192f;
  min-height: 100vh;

  .course-card {
    margin-bottom: 20px;
    background: #112240;
    border: 1px solid #1e3a8a;
    transition: transform 0.3s;

    &:hover {
      transform: translateY(-5px);
    }

    .course-cover {
      width: 100%;
      height: 200px;
      object-fit: cover;
    }

    .course-info {
      padding: 16px;

      h3 {
        margin: 0 0 8px;
        color: #64ffda;
        font-size: 18px;
      }

      .description {
        color: #8892b0;
        margin: 0 0 16px;
        height: 40px;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
      }

      .stats {
        display: flex;
        gap: 16px;
        margin-bottom: 16px;
        color: #8892b0;

        span {
          display: flex;
          align-items: center;
          gap: 4px;

          .el-icon {
            color: #64ffda;
          }
        }
      }

      .el-button {
        width: 100%;
      }
    }
  }
}
</style> 