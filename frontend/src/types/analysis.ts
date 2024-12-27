// 学习指标
export interface LearningMetrics {
  efficiency: number;  // 学习效率
  mastery: number;    // 知识掌握
  engagement: number; // 学习投入
}

// AI 建议
export interface AISuggestion {
  id: number;
  type: 'success' | 'warning' | 'info';
  color: string;
  hollow: boolean;
  timestamp: string;
  title: string;
  content: string;
}

// 技能数据
export interface SkillData {
  category: string;
  value: number;
  max: number;
}

// 分析数据
export interface AnalysisData {
  metrics: LearningMetrics;
  suggestions: AISuggestion[];
  skills: SkillData[];
  lastUpdated: string;
}

// 学习行为
export interface LearningBehavior {
  userId: number;
  courseId: number;
  type: 'start' | 'complete' | 'pause' | 'resume';
  timestamp: string;
  duration?: number;
  progress?: number;
}

// 知识点掌握度
export interface KnowledgePoint {
  id: string;
  name: string;
  category: string;
  mastery: number;
  lastReviewed?: string;
  relatedCourses: number[];
} 