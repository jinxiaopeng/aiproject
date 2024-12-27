// 引入 Vue 创建应用的函数
import { createApp } from 'vue'
// 引入 Pinia 状态管理库
import { createPinia } from 'pinia'
// 引入 Element Plus 组件库
import ElementPlus from 'element-plus'
// 引入 Element Plus 的样式文件
import 'element-plus/dist/index.css'
// 引入 App.vue 组件
import App from './App.vue'
// 引入 router 配置
import router from './router'

// ECharts 相关导入
import { use } from 'echarts/core' // 引入 ECharts 的核心功能
import { CanvasRenderer } from 'echarts/renderers' // 引入 ECharts 的渲染器
import { LineChart, PieChart, RadarChart, BarChart } from 'echarts/charts'  // 引入图表类型
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  MarkPointComponent,
  MarkLineComponent
} from 'echarts/components' // 引入 ECharts 的组件
import VChart from 'vue-echarts' // 引入 Vue 的 ECharts 组件

// 注册 ECharts 组件
use([
  CanvasRenderer,
  LineChart,
  PieChart,
  RadarChart,
  BarChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  MarkPointComponent,
  MarkLineComponent
])

// 创建 Vue 应用
const app = createApp(App)

// 使用 Pinia 状态管理库
app.use(createPinia())
// 使用 Vue Router
app.use(router)
// 使用 Element Plus 组件库
app.use(ElementPlus)

// 全局注册 ECharts 组件
app.component('v-chart', VChart)

// 添加全局错误处理
app.config.errorHandler = (err, instance, info) => {
  console.error('Global error:', err)
  console.error('Error info:', info)
  console.error('Component instance:', instance)
}

// 添加全局警告处理
app.config.warnHandler = (msg, instance, trace) => {
  console.warn('Global warning:', msg)
  console.warn('Warning trace:', trace)
  console.warn('Component instance:', instance)
}

// 挂载应用到 DOM 中的 #app 元素
app.mount('#app')