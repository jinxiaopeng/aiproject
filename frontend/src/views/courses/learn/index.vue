<template>
  <div class="course-learning">
    <div class="main-content">
      <div class="video-section">
        <VideoPlayer
          ref="playerRef"
          :src="currentChapter?.video_url || ''"
          :current-time="currentVideoTime"
          :poster="course.cover_url"
          @timeupdate="handleTimeUpdate"
          @ended="handleVideoEnded"
        />
      </div>
      <div class="comments-section">
        <CourseComments
          :comments="comments"
          @add-comment="handleAddComment"
        />
      </div>
    </div>

    <div class="sidebar">
      <div class="outline-section">
        <div class="section-header">
          <h3>课程目录</h3>
          <el-button 
            type="primary" 
            size="small"
            @click="showQuiz = true"
          >
            课后测试
          </el-button>
        </div>
        <ChapterList
          :chapters="course.chapters"
          :current-chapter-id="currentChapterId"
          @select="switchChapter"
        />
      </div>

      <div class="notes-section">
        <CourseNotes
          :current-time="currentVideoTime"
          :video-ref="playerRef?.videoElement?.value"
          @seek="handleSeek"
        />
      </div>
    </div>

    <el-dialog
      v-model="showQuiz"
      title="课后测试"
      width="500px"
      :close-on-click-modal="false"
    >
      <QuizSection
        :chapter-id="currentChapterId"
        :video-progress="currentVideoTime"
      />
    </el-dialog>
  </div>
</template>

<style lang="scss" scoped>
.course-learning {
  display: flex;
  height: 100vh;
  background-color: var(--el-bg-color);

  .main-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    min-width: 0;
    overflow-y: auto;

    .video-section {
      width: 100%;
      height: 600px;
      background-color: #000;
      display: flex;
      align-items: center;
      justify-content: center;

      :deep(video) {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }
    }

    .comments-section {
      padding: 20px;
      background-color: var(--el-bg-color);
      flex: 1;
      overflow-y: auto;
    }
  }

  .sidebar {
    position: relative;
    width: 320px;
    display: flex;
    flex-direction: column;
    background-color: var(--el-bg-color);

    .outline-section {
      padding: 8px;
      flex: 0 1 auto;
      max-height: 50vh;
      overflow-y: auto;

      .section-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;
        padding: 0 8px;

        h3 {
          margin: 0;
          font-size: 16px;
          font-weight: bold;
        }
      }
    }

    .notes-section {
      padding: 16px;
      flex: 1;
      border-top: 1px solid var(--el-border-color-lighter);
      overflow-y: auto;
    }
  }
}
</style>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import VideoPlayer from './components/VideoPlayer.vue'
import ChapterList from './components/ChapterList.vue'
import CourseNotes from './components/CourseNotes.vue'
import CourseComments from './components/CourseComments.vue'
import QuizSection from './components/QuizSection.vue'

interface Chapter {
  id: number
  title: string
  description: string
  video_url: string
  duration: number
  progress: number
}

interface Course {
  id: number
  title: string
  description: string
  cover_url: string
  chapters: Chapter[]
}

interface VideoInfo {
  video_url: string
  duration: number
  title: string
  current_time?: number
}

interface Comment {
  id: number
  username: string
  avatar: string
  content: string
  time: string
}

const route = useRoute()
const router = useRouter()
const activeTab = ref('outline')
const playerRef = ref<any>(null)
const currentVideoTime = ref(0)
const currentChapterId = ref(0)
const course = ref<Course>({
  id: 0,
  title: '',
  description: '',
  cover_url: '',
  chapters: []
})

// 计算当前章节
const currentChapter = computed(() => {
  return course.value.chapters.find(chapter => chapter.id === currentChapterId.value)
})

// 视频信息
const videoInfo = ref<VideoInfo | null>(null)

// 添加一个格式化时间的函数
const formatDuration = (seconds: number) => {
  const minutes = Math.floor(seconds / 60)
  return `${minutes}分钟`
}

// 加载课程数据
const loadCourse = async () => {
  try {
    // TODO: 从API获取课程数据
    const mockCourse: Course = {
      id: 1,
      title: 'Web安全基础',
      description: '学习Web安全的基本概念和实践',
      cover_url: '/images/courses/web-security-basic.jpg',
      chapters: [
        {
          id: 1,
          title: 'Web安全概述',
          description: '了解Web安全的基本概念和常见威胁',
          video_url: '/videos/chapter1.mp4',
          duration: 1800, // 30分钟
          progress: 0
        },
        {
          id: 2,
          title: 'SQL注入攻击',
          description: 'SQL注入攻击原理和防御',
          video_url: '/videos/chapter2.mp4',
          duration: 2400, // 40分钟
          progress: 0
        },
        {
          id: 3,
          title: 'XSS跨站脚本',
          description: 'XSS攻击原理和防御',
          video_url: '/videos/chapter3.mp4',
          duration: 2100, // 35分钟
          progress: 0
        }
      ]
    }
    
    course.value = mockCourse
    currentChapterId.value = mockCourse.chapters[0].id
  } catch (error) {
    console.error('Failed to load course:', error)
  }
}

// 切换章节
const switchChapter = (chapterId: number) => {
  currentChapterId.value = chapterId
  // TODO: 保存学习进度
}

// 处理视频时间更新
const handleTimeUpdate = (time: number) => {
  currentVideoTime.value = time
  // TODO: 更新学习进度
}

// 处理视频播放结束
const handleVideoEnded = () => {
  const currentIndex = course.value.chapters.findIndex(chapter => chapter.id === currentChapterId.value)
  const nextChapter = course.value.chapters[currentIndex + 1]
  
  if (nextChapter) {
    switchChapter(nextChapter.id)
  }
}

// 处理跳转到指定时间点
const handleSeek = (time: number) => {
  if (playerRef.value) {
    playerRef.value.currentTime = time
  }
}

const comments = ref<Comment[]>([
  {
    id: 1,
    username: '张三',
    avatar: '',
    content: '讲得很清楚，特别是SQL注入的防御方法，学到了很多！',
    time: '2024/12/24 20:15:30'
  },
  {
    id: 2,
    username: '李四',
    avatar: '',
    content: '老师讲解很生动，举的例子也很实用。期待下一节课！',
    time: '2024/12/24 20:30:45'
  },
  {
    id: 3,
    username: '王五',
    avatar: '',
    content: '这节课信息量很大，建议大家多看几遍，做好笔记。',
    time: '2024/12/24 21:05:18'
  }
])

const handleAddComment = (content: string) => {
  const comment: Comment = {
    id: Date.now(),
    username: '我',
    avatar: '',
    content: content,
    time: new Date().toLocaleString()
  }
  comments.value.unshift(comment)
}

const showQuiz = ref(false)

onMounted(() => {
  loadCourse()
})
</script>
 