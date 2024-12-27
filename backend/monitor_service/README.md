# 学习监控系统

## 数据库结构

### 1. 视频学习记录表 (video_progress)
记录用户观看视频的进度信息
- id: 主键
- user_id: 用户ID
- course_id: 课程ID
- chapter_id: 章节ID
- progress: 进度百分比(0-100)
- duration: 视频总时长(秒)
- current_time: 当前播放时间(秒)
- last_updated: 最后更新时间

### 2. 学习行为表 (learning_behavior)
记录用户的学习行为
- id: 主键
- user_id: 用户ID
- course_id: 课程ID
- start_time: 开始学习时间
- end_time: 结束学习时间
- duration: 学习时长(秒)
- behavior_type: 行为类型(video_watch/challenge/quiz)
- content_id: 对应内容ID

### 3. 靶场训练记录表 (challenge_progress)
记录用户的靶场训练进度
- id: 主键
- user_id: 用户ID
- challenge_id: 靶场ID
- status: 状态(not_started/in_progress/completed)
- start_time: 开始时间
- complete_time: 完成时间
- attempts: 尝试次数
- hints_used: 使用提示数
- score: 获得分数

### 4. 每日学习统计表 (daily_stats)
记录用户每日学习统计数据
- id: 主键
- user_id: 用户ID
- stats_date: 统计日期
- total_study_time: 总学习时长(秒)
- video_completion_count: 完成视频数
- challenge_completion_count: 完成靶场数
- score_gained: 获得分数

## 使用方法

### 初始化数据库
```python
from monitor_service.init_db import init_db

# 初始化数据库和表结构
init_db()
```

### 记录视频进度
```python
from monitor_service.database import MonitorDB

db = MonitorDB()
db.record_video_progress(
    user_id=1,
    course_id=1,
    chapter_id=1,
    progress=75,  # 75%
    duration=600,  # 10分钟
    current_time=450  # 7分30秒
)
```

### 记录学习行为
```python
db.record_learning_behavior(
    user_id=1,
    course_id=1,
    behavior_type='video_watch',
    content_id=1,
    duration=300  # 5分钟
)
```

### 更新靶场进度
```python
db.update_challenge_progress(
    user_id=1,
    challenge_id=1,
    status='completed',
    attempts=3,
    hints=1,
    score=100
)
```

### 更新每日统计
```python
db.update_daily_stats(
    user_id=1,
    study_time=1800,  # 30分钟
    video_complete=1,
    challenge_complete=1,
    score=100
)
```

### 获取用户统计数据
```python
stats = db.get_user_stats(
    user_id=1,
    days=7  # 最近7天
)
print(stats)
```

## 数据分析

系统会记录以下关键指标：

1. 视频学习
- 视频完成率
- 观看时长分布
- 重复观看次数

2. 靶场训练
- 完成率
- 平均尝试次数
- 提示使用情况
- 得分分布

3. 每日统计
- 总学习时长
- 完成任务数
- 获得积分

这些数据可用于：
- 学习进度监控
- 行为模式分析
- 学习效果评估
- 个性化推荐 