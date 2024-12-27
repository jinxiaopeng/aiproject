<!-- 通知中心组件 -->
<template>
  <div class="notification-center">
    <!-- 通知图标 -->
    <a-badge :count="unreadCount">
      <a-button
        type="text"
        shape="circle"
        @click="showDrawer"
      >
        <template #icon>
          <BellOutlined />
        </template>
      </a-button>
    </a-badge>
    
    <!-- 通知抽屉 -->
    <a-drawer
      title="通知中心"
      placement="right"
      :visible="visible"
      @close="closeDrawer"
      width="400"
    >
      <template #extra>
        <a-space>
          <a-button size="small" @click="clearAll">
            清空通知
          </a-button>
          <a-button size="small" type="primary" @click="markAllRead">
            全部已读
          </a-button>
        </a-space>
      </template>
      
      <!-- 通知列表 -->
      <a-list
        :data-source="notifications"
        :loading="loading"
      >
        <template #renderItem="{ item }">
          <a-list-item>
            <a-list-item-meta>
              <template #title>
                <span :class="['notification-title', item.type]">
                  {{ item.title }}
                </span>
              </template>
              <template #description>
                <div class="notification-content">
                  <p>{{ item.message }}</p>
                  <span class="notification-time">
                    {{ formatTime(item.timestamp) }}
                  </span>
                </div>
              </template>
            </a-list-item-meta>
            
            <!-- 操作按钮 -->
            <template #actions>
              <a-button
                v-if="item.challenge_id"
                type="link"
                size="small"
                @click="goToChallenge(item.challenge_id)"
              >
                查看靶场
              </a-button>
            </template>
          </a-list-item>
        </template>
        
        <!-- 空状态 -->
        <template #empty>
          <a-empty description="暂无通知" />
        </template>
      </a-list>
    </a-drawer>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import { BellOutlined } from '@ant-design/icons-vue'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import 'dayjs/locale/zh-cn'

dayjs.extend(relativeTime)
dayjs.locale('zh-cn')

interface Notification {
  title: string
  message: string
  type: string
  challenge_id?: number
  timestamp: string
  read?: boolean
}

export default defineComponent({
  name: 'NotificationCenter',
  
  components: {
    BellOutlined
  },
  
  setup() {
    const router = useRouter()
    const visible = ref(false)
    const loading = ref(false)
    const notifications = ref<Notification[]>([])
    const unreadCount = ref(0)
    let ws: WebSocket | null = null
    
    // 显示抽屉
    const showDrawer = () => {
      visible.value = true
      loadHistory()
    }
    
    // 关闭抽屉
    const closeDrawer = () => {
      visible.value = false
    }
    
    // 加载历史通知
    const loadHistory = async () => {
      try {
        loading.value = true
        const response = await fetch('/api/notifications/history')
        const data = await response.json()
        notifications.value = data
        updateUnreadCount()
      } catch (error) {
        message.error('加载通知失败')
      } finally {
        loading.value = false
      }
    }
    
    // 清空通知
    const clearAll = async () => {
      try {
        await fetch('/api/notifications/clear', { method: 'DELETE' })
        notifications.value = []
        unreadCount.value = 0
        message.success('已清空通知')
      } catch (error) {
        message.error('清空通知失败')
      }
    }
    
    // 标记全部已读
    const markAllRead = () => {
      notifications.value.forEach(item => {
        item.read = true
      })
      unreadCount.value = 0
    }
    
    // 更新未读数
    const updateUnreadCount = () => {
      unreadCount.value = notifications.value.filter(item => !item.read).length
    }
    
    // 跳转到靶场
    const goToChallenge = (id: number) => {
      router.push(`/challenge/${id}`)
      closeDrawer()
    }
    
    // 格式化时间
    const formatTime = (timestamp: string) => {
      return dayjs(timestamp).fromNow()
    }
    
    // 连接WebSocket
    const connectWebSocket = () => {
      const token = localStorage.getItem('token')
      if (!token) return
      
      ws = new WebSocket(`ws://${window.location.host}/api/notifications/ws?token=${token}`)
      
      ws.onmessage = (event) => {
        const notification: Notification = JSON.parse(event.data)
        notifications.value.unshift(notification)
        if (notifications.value.length > 100) {
          notifications.value.pop()
        }
        updateUnreadCount()
        
        // 显示消息提示
        message[notification.type]({
          content: notification.message,
          duration: 3
        })
      }
      
      ws.onclose = () => {
        setTimeout(connectWebSocket, 3000)
      }
      
      // 保持连接活跃
      setInterval(() => {
        if (ws?.readyState === WebSocket.OPEN) {
          ws.send('ping')
        }
      }, 30000)
    }
    
    onMounted(() => {
      connectWebSocket()
    })
    
    onUnmounted(() => {
      ws?.close()
    })
    
    return {
      visible,
      loading,
      notifications,
      unreadCount,
      showDrawer,
      closeDrawer,
      clearAll,
      markAllRead,
      goToChallenge,
      formatTime
    }
  }
})
</script>

<style scoped>
.notification-center {
  display: inline-block;
}

.notification-title {
  font-weight: 500;
}

.notification-title.info {
  color: #1890ff;
}

.notification-title.warning {
  color: #faad14;
}

.notification-title.error {
  color: #ff4d4f;
}

.notification-content {
  display: flex;
  flex-direction: column;
}

.notification-time {
  font-size: 12px;
  color: rgba(0, 0, 0, 0.45);
}
</style> 