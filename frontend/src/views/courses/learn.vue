<template>
  <div class="course-learn">
    <div class="video-container">
      <VideoPlayer
        v-if="videoInfo"
        ref="playerRef"
        :src="videoInfo.video_url"
        :poster="course?.cover_url"
        @timeupdate="handleTimeUpdate"
        @ended="handleVideoEnded"
      />
    </div>
    
    <div class="learn-content">
      <div class="chapter-info">
        <h2>{{ currentChapter?.title }}</h2>
        <p>{{ currentChapter?.description }}</p>
      </div>
      
      <div class="chapter-list">
        <h3>课程大纲</h3>
        <el-menu
          :default-active="String(chapterId)"
          class="chapter-menu"
        >
          <el-menu-item
            v-for="chapter in course?.chapters"
            :key="chapter.id"
            :index="String(chapter.id)"
            @click="switchChapter(chapter.id)"
          >
            <div class="chapter-item">
              <span class="title">{{ chapter.title }}</span>
              <div class="meta">
                <span class="duration">
                  <el-icon><VideoPlay /></el-icon>
                  {{ chapter.duration }}分钟
                </span>
                <el-tag
                  v-if="chapter.progress !== undefined"
                  :type="chapter.progress === 100 ? 'success' : 'warning'"
                  size="small"
                >
                  {{ chapter.progress === 100 ? '已完成' : '进行中' }}
                </el-tag>
              </div>
            </div>
          </el-menu-item>
        </el-menu>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  VideoPlay,
  Document,
  ChatDotRound,
  Folder
} from '@element-plus/icons-vue'
import VideoPlayer from '@/components/VideoPlayer.vue'
import CourseNotes from './components/CourseNotes.vue'
import CourseDiscussion from './components/CourseDiscussion.vue'

interface Chapter {
  id: number
  title: string
  description: string
  duration: number
  progress: number
  video_url: string
  order: number
}

interface Course {
  id: number
  title: string
  description: string
  cover_url: string
  teacher: {
    name: string
    avatar: string
  }
  created_at: string
  updated_at: string
  chapters: Chapter[]
}

interface VideoInfo {
  video_url: string
  duration: number
  title: string
  current_time?: number
}

// 模拟课程数据
const courseData: Course = {
  id: 1,
  title: "Web安全渗透测试实战",
  description: "系统学习Web安全渗透测试技术",
  cover_url: "/images/courses/web-pentest.jpg",
  teacher: {
    name: "张三",
    avatar: "/images/avatars/teacher1.jpg"
  },
  created_at: "2023-12-01",
  updated_at: "2023-12-11",
  chapters: [
    {
      id: 1,
      title: "Web安全概述",
      description: "了解Web安全的基本概念和重要性",
      duration: 45,
      progress: 0,
      video_url: "/videos/chapter1.mp4",
      order: 1
    },
    {
      id: 2,
      title: "常见Web漏洞分析",
      description: "学习SQL注入、XSS等常见漏洞的原理",
      duration: 60,
      progress: 0,
      video_url: "/videos/chapter2.mp4",
      order: 2
    }
  ]
}

const route = useRoute()
const router = useRouter()

// 当前课程信息
const course = ref<Course>(courseData)

// 当前章节
const currentChapterId = ref(Number(route.query.chapter) || course.value.chapters[0].id)
const currentChapter = computed(() => {
  return course.value.chapters.find(chapter => chapter.id === currentChapterId.value)
})

// 视频信息
const videoInfo = ref<VideoInfo>({
  video_url: '',
  duration: 0,
  title: ''
})

// 当前标签页
const activeTab = ref('video')

// 视频播放器引用
const playerRef = ref(null)
const currentVideoTime = ref(0)

// 加载课程信息
const loadCourse = async () => {
  try {
    // TODO: 调用API获取课程信息
    course.value = courseData
  } catch (error) {
    console.error('Failed to load course:', error)
    ElMessage.error('加载课程信息失败')
  }
}

// 加载视频信息
const loadVideo = async () => {
  try {
    const currentChapterVideo = currentChapter.value
    if (currentChapterVideo) {
      videoInfo.value = {
        video_url: currentChapterVideo.video_url,
        title: currentChapterVideo.title,
        duration: currentChapterVideo.duration || 0,
        current_time: 0
      }
    } else {
      throw new Error('章节不存在')
    }
  } catch (error) {
    console.error('Failed to load video:', error)
    ElMessage.error('加载视频失败')
  }
}

// 切换章节
const switchChapter = (chapterId: number) => {
  currentChapterId.value = chapterId
  router.push({
    query: { ...route.query, chapter: chapterId }
  })
  loadVideo()
}

// 视频进度更新
const handleTimeUpdate = async (time: number) => {
  currentVideoTime.value = time
  const totalDuration = playerRef.value?.getDuration() || 0
  if (totalDuration > 0) {
    const progress = Math.round((time / totalDuration) * 100)
    
    try {
      // 发送进度到后端API
      const response = await fetch('http://localhost:5173/api/learning/progress', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          course_id: course.value.id,
          chapter_id: currentChapterId.value,
          progress: progress,
          current_time: Math.round(time),
          duration: Math.round(totalDuration)
        })
      })
      
      const result = await response.json()
      if (result.status === 'error') {
        console.error('保存进度失败:', result.message)
      }
    } catch (error) {
      console.error('发送进度数据失败:', error)
    }
  }
}

// 视频播放完成
const handleVideoEnded = () => {
  console.log('视频播放完成')
  const currentIndex = course.value.chapters.findIndex(chapter => chapter.id === currentChapterId.value)
  const nextChapter = course.value.chapters[currentIndex + 1]
  
  // 更新完成状态
  const videoProgress = localStorage.getItem('videoProgress') || '{}'
  const progressData = JSON.parse(videoProgress)
  progressData[`${course.value.id}-${currentChapterId.value}`] = 100
  localStorage.setItem('videoProgress', JSON.stringify(progressData))
  
  if (nextChapter) {
    console.log('准备播放下一章节:', nextChapter.title)
    ElMessage.success('即将播放下一章节')
    setTimeout(() => {
      switchChapter(nextChapter.id)
    }, 2000)
  } else {
    console.log('所有章节已完成')
    ElMessage.success('恭喜你完成了所有章节的学习！')
  }
}

// 初始化
onMounted(() => {
  loadCourse()
  loadVideo()
})
</script>

<style lang="scss" scoped>
.course-learn {
  display: flex;
  gap: 2rem;
  padding: 2rem;
  max-width: 1600px;
  margin: 0 auto;
  min-height: calc(100vh - 60px);

  .video-container {
    flex: 1;
    max-width: 1000px;
  }

  .learn-content {
    width: 300px;
    
    .chapter-info {
      margin-bottom: 2rem;
      
      h2 {
        margin: 0 0 1rem;
        font-size: 1.5rem;
      }
      
      p {
        color: var(--el-text-color-secondary);
        line-height: 1.6;
      }
    }

    .chapter-list {
      h3 {
        margin: 0 0 1rem;
        font-size: 1.2rem;
      }
    }

    .chapter-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 100%;
      
      .title {
        flex: 1;
        margin-right: 1rem;
      }
      
      .meta {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        
        .duration {
          display: flex;
          align-items: center;
          gap: 0.25rem;
          color: var(--el-text-color-secondary);
          font-size: 0.9rem;
        }
      }
    }
  }
}
</style> 