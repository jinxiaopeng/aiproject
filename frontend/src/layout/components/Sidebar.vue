const menuItems = ref([
  {
    title: '首页',
    icon: 'House',
    path: '/'
  },
  {
    title: '知识图谱',
    icon: 'Connection',
    path: '/knowledge'
  },
  {
    title: '靶场训练',
    icon: 'Aim',
    path: '/challenges'
  },
  {
    title: '管理后台',
    icon: 'Monitor',
    path: '/admin',
    roles: ['admin']
  }
]) 