import axios from 'axios';
import config from '@/config'

// 创建axios实例
const api = axios.create({
  baseURL: `${config.baseUrl}/api`,
  timeout: config.apiTimeout,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 请求拦截器
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  response => response.data,
  error => {
    if (error.response) {
      switch (error.response.status) {
        case 401:
          // 未授权，清除token并跳转到登录页
          localStorage.removeItem('token');
          window.location.href = '/login';
          break;
        case 403:
          // 权限不足
          console.error('没有权限执行此操作');
          break;
        case 500:
          console.error('服务器错误');
          break;
        default:
          console.error('请求失败');
      }
    }
    return Promise.reject(error);
  }
);

// 课程相关API
export const courseApi = {
  // 获取课程列表
  getCourses() {
    return api.get('/courses');
  },

  // 获取课程详情
  getCourseDetail(courseId) {
    return api.get(`/courses/${courseId}`);
  },

  // 创建课程（管理员）
  createCourse(courseData) {
    return api.post('/courses', courseData);
  },

  // 更新课程（管理员）
  updateCourse(courseId, courseData) {
    return api.put(`/courses/${courseId}`, courseData);
  },

  // 删除课程（管理员）
  deleteCourse(courseId) {
    return api.delete(`/courses/${courseId}`);
  }
};

// 实验室相关API
export const labApi = {
  // 获取实验室列表
  getLabs() {
    return api.get('/labs');
  },

  // 获取实验室详情
  getLabDetail(labId) {
    return api.get(`/labs/${labId}`);
  },

  // 创建实验室（管理员）
  createLab(labData) {
    return api.post('/labs', labData);
  },

  // 更新实验室（管理员）
  updateLab(labId, labData) {
    return api.put(`/labs/${labId}`, labData);
  },

  // 删除实验室（管理员）
  deleteLab(labId) {
    return api.delete(`/labs/${labId}`);
  },

  // 启动实验室环境
  startLab(labId) {
    return api.post(`/labs/${labId}/start`);
  },

  // 停止实验室环境
  stopLab(labId) {
    return api.post(`/labs/${labId}/stop`);
  },

  // 获取实验室状态
  getLabStatus(labId) {
    return api.get(`/labs/${labId}/status`);
  },

  // 获取用户实验室历史
  getUserLabHistory(userId) {
    return api.get(`/labs/user/${userId}/history`);
  }
};

// 用户相关API
export const userApi = {
  // 用户登录
  login(username, password) {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    return api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },

  // 用户登出
  logout() {
    return api.post('/auth/logout');
  },

  // 获取当前用户信息
  getCurrentUser() {
    return api.get('/auth/user');
  }
};

// 系统监控API（管理员）
export const monitorApi = {
  // 获取系统状态
  getSystemStatus() {
    return api.get('/monitor/system');
  },

  // 获取Docker状态
  getDockerStatus() {
    return api.get('/monitor/docker');
  },

  // 获取数据库状态
  getDatabaseStatus() {
    return api.get('/monitor/database');
  },

  // 获取活跃用户
  getActiveUsers() {
    return api.get('/monitor/active-users');
  }
};

// AI辅助API
export const aiApi = {
  // 获取学习建议
  getLearningsuggestions() {
    return api.get('/ai/suggestions');
  },

  // 分析漏洞
  analyzeVulnerability(code) {
    return api.post('/ai/analyze-vulnerability', { code });
  },

  // 获取技能分析
  getSkillAnalysis() {
    return api.get('/ai/skill-analysis');
  }
};

// 数据分析API
export const analysisApi = {
  // 获取技能雷达图数据
  getSkillRadar() {
    return api.get('/analysis/skill-radar');
  },

  // 获取进度趋势数据
  getProgressTrend() {
    return api.get('/analysis/progress-trend');
  }
}; 