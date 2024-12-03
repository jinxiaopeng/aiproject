from typing import Dict, List, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import mysql.connector
import logging
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from pathlib import Path
import networkx as nx
from datetime import datetime, timedelta
import json

from config import CONFIG

# 配置日志
logger = logging.getLogger(__name__)

class KnowledgeGraph:
    def __init__(self):
        """初始化知识图谱"""
        self.graph = nx.DiGraph()
        self.last_update = None
        self.update_interval = timedelta(hours=1)
        
    def needs_update(self) -> bool:
        """检查是否需要更新图谱"""
        if not self.last_update:
            return True
        return datetime.now() - self.last_update > self.update_interval
        
    def update_graph(self, conn):
        """更新知识图谱"""
        try:
            cursor = conn.cursor(dictionary=True)
            try:
                # 获取所有知识点
                cursor.execute("""
                    SELECT id, title, content, category, severity
                    FROM knowledge_base
                    WHERE status = 'active'
                """)
                nodes = cursor.fetchall()
                
                # 清空现有图谱
                self.graph.clear()
                
                # 添加节点
                for node in nodes:
                    self.graph.add_node(
                        node['id'],
                        title=node['title'],
                        category=node['category'],
                        severity=node['severity']
                    )
                
                # 计算节点间的关系
                vectorizer = TfidfVectorizer()
                content_matrix = vectorizer.fit_transform(
                    [node['content'] for node in nodes]
                )
                similarities = cosine_similarity(content_matrix)
                
                # 添加边
                for i in range(len(nodes)):
                    for j in range(i + 1, len(nodes)):
                        if similarities[i, j] > 0.3:  # 相似度阈值
                            self.graph.add_edge(
                                nodes[i]['id'],
                                nodes[j]['id'],
                                weight=float(similarities[i, j])
                            )
                
                self.last_update = datetime.now()
                logger.info("知识图谱更新成功")
                
            finally:
                cursor.close()
                
        except Exception as e:
            logger.error(f"更新知识图谱失败: {str(e)}")
            raise

    def get_related_knowledge(self, knowledge_id: int, limit: int = 5) -> List[Dict]:
        """获取相关知识点"""
        try:
            if knowledge_id not in self.graph:
                return []
                
            # 使用PageRank算法计算相关性
            personalization = {node: 1 if node == knowledge_id else 0
                             for node in self.graph.nodes()}
            ranks = nx.pagerank(self.graph, personalization=personalization)
            
            # 获取相关节点
            related = sorted(
                [(node, rank) for node, rank in ranks.items() if node != knowledge_id],
                key=lambda x: x[1],
                reverse=True
            )[:limit]
            
            return [{
                'id': node,
                'title': self.graph.nodes[node]['title'],
                'category': self.graph.nodes[node]['category'],
                'relevance': rank
            } for node, rank in related]
            
        except Exception as e:
            logger.error(f"获取相关知识点失败: {str(e)}")
            return []

class AIModel:
    def __init__(self):
        """初始化AI模型"""
        try:
            model_path = CONFIG["ai"]["model_path"]
            cache_dir = CONFIG["ai"]["cache_dir"]
            
            # 确保目录存在
            Path(cache_dir).mkdir(parents=True, exist_ok=True)
            
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_path,
                cache_dir=cache_dir
            )
            self.model = AutoModelForSequenceClassification.from_pretrained(
                model_path,
                cache_dir=cache_dir
            )
            
            # 设置模型参数
            self.max_length = CONFIG["ai"]["max_length"]
            self.batch_size = CONFIG["ai"]["batch_size"]
            
            logger.info("AI模型初始化成功")
            
        except Exception as e:
            logger.error(f"AI模型初始化失败: {str(e)}")
            raise
        
    def predict(self, text: str) -> Dict:
        """预测文本"""
        try:
            # 准备输入
            inputs = self.tokenizer(
                text,
                truncation=True,
                max_length=self.max_length,
                return_tensors="pt"
            )
            
            # 预测
            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = outputs.logits.softmax(dim=-1)
                
            return {
                "predictions": predictions.tolist()[0],
                "labels": self.model.config.id2label
            }
            
        except Exception as e:
            logger.error(f"预测失败: {str(e)}")
            return {"error": str(e)}

class AIAssistant:
    def __init__(self):
        """初始化AI助手"""
        try:
            self.vectorizer = TfidfVectorizer(
                max_features=5000,
                stop_words='english',
                ngram_range=(1, 2)
            )
            self.knowledge_base = self._load_knowledge_base()
            self.vectors = None
            self._initialize_vectors()
            
            # 加载AI模型
            self.model = AIModel()
            
            # 初始化知识图谱
            self.knowledge_graph = KnowledgeGraph()
            
        except Exception as e:
            logger.error(f"AI助手初始化失败: {str(e)}")
            self.knowledge_base = []
            self.vectors = None
            self.model = None
            self.knowledge_graph = None
        
    def _load_knowledge_base(self) -> List[Dict]:
        """加载知识库数据"""
        try:
            conn = mysql.connector.connect(**CONFIG["database"])
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute("""
                    SELECT id, title, content, category, severity 
                    FROM knowledge_base 
                    WHERE status = 'active'
                """)
                return cursor.fetchall()
            finally:
                cursor.close()
                conn.close()
        except Exception as e:
            logger.error(f"加载知识库失败: {str(e)}")
            return []
            
    def _initialize_vectors(self):
        """初始化文本向量"""
        try:
            if not self.knowledge_base:
                logger.warning("知识库为空，无法初始化向量")
                return
                
            texts = [item.get('content', '') for item in self.knowledge_base if item.get('content')]
            if not texts:
                logger.warning("没有有效的文本内容用于向量化")
                return
                
            self.vectors = self.vectorizer.fit_transform(texts)
            logger.info(f"成功初始化向量，维度: {self.vectors.shape}")
        except Exception as e:
            logger.error(f"初始化向量失败: {str(e)}")
            self.vectors = None
        
    def get_learning_suggestions(self, user_id: int) -> List[Dict]:
        """获取学习建议"""
        try:
            if not user_id:
                raise ValueError("用户ID不能为空")
                
            conn = mysql.connector.connect(**CONFIG["database"])
            cursor = conn.cursor(dictionary=True)
            try:
                # 获取用户学习历史和薄弱项
                cursor.execute("""
                    SELECT 
                        c.category,
                        COUNT(*) as completed_count,
                        AVG(h.score) as avg_score
                    FROM learning_history h
                    JOIN courses c ON h.course_id = c.id
                    WHERE h.user_id = %s
                    GROUP BY c.category
                    HAVING avg_score < 80
                    ORDER BY avg_score ASC
                    LIMIT 3
                """, (user_id,))
                weak_areas = cursor.fetchall()
                
                if not weak_areas:
                    # 如果没有学习历史，推荐基础课程
                    cursor.execute("""
                        SELECT * FROM courses
                        WHERE difficulty_level = 1
                        AND status = 'published'
                        LIMIT 3
                    """)
                    return cursor.fetchall()
                
                suggestions = []
                for area in weak_areas:
                    # 查找适合的课程
                    cursor.execute("""
                        SELECT c.*, COUNT(h.id) as student_count
                        FROM courses c
                        LEFT JOIN learning_history h ON c.id = h.course_id
                        WHERE c.category = %s
                        AND c.status = 'published'
                        AND c.id NOT IN (
                            SELECT course_id 
                            FROM learning_history 
                            WHERE user_id = %s
                        )
                        GROUP BY c.id
                        ORDER BY c.difficulty_level ASC, student_count DESC
                        LIMIT 2
                    """, (area['category'], user_id))
                    courses = cursor.fetchall()
                    suggestions.extend(courses)
                
                return suggestions
                
            finally:
                cursor.close()
                conn.close()
        except Exception as e:
            logger.error(f"获取学习建议失败: {str(e)}")
            return []
            
    def analyze_vulnerability(self, code: str) -> List[Dict]:
        """分析代码中的漏洞"""
        try:
            if not code or not isinstance(code, str):
                raise ValueError("无效的代码输入")
                
            if not self.vectors or not self.knowledge_base:
                logger.error("向量或知识库未初始化")
                return []
                
            # 将代码向量化
            try:
                code_vector = self.vectorizer.transform([code])
            except Exception as e:
                logger.error(f"代码向量化失败: {str(e)}")
                return []
            
            # 计算相似度
            similarities = cosine_similarity(code_vector, self.vectors)[0]
            
            # 获取最相似的漏洞模式
            results = []
            for idx, score in enumerate(similarities):
                if score > 0.3:  # 相似度阈值
                    result = {
                        'title': self.knowledge_base[idx]['title'],
                        'category': self.knowledge_base[idx]['category'],
                        'severity': self.knowledge_base[idx]['severity'],
                        'similarity': float(score),
                        'description': self.knowledge_base[idx]['content'][:200] + '...' if len(self.knowledge_base[idx]['content']) > 200 else self.knowledge_base[idx]['content']
                    }
                    results.append(result)
            
            # 按相似度排序
            results.sort(key=lambda x: x['similarity'], reverse=True)
            
            # 使用AI模型进行深度分析
            if self.model:
                for result in results:
                    try:
                        prediction = self.model.predict(code)
                        result['ai_analysis'] = prediction
                    except Exception as e:
                        logger.error(f"AI分析失败: {str(e)}")
            
            return results[:3]  # 返回前3个结果
            
        except Exception as e:
            logger.error(f"分析漏洞失败: {str(e)}")
            return []
        
    def get_skill_analysis(self, user_id: int) -> Dict:
        """获取技能分析"""
        try:
            conn = mysql.connector.connect(**CONFIG["database"])
            cursor = conn.cursor(dictionary=True)
            try:
                # 获取用户在各个类别的学习情况
                cursor.execute("""
                    SELECT 
                        c.category,
                        COUNT(*) as completed_count,
                        AVG(h.score) as avg_score,
                        MAX(c.difficulty_level) as max_difficulty
                    FROM learning_history h
                    JOIN courses c ON h.course_id = c.id
                    WHERE h.user_id = %s
                    GROUP BY c.category
                """, (user_id,))
                
                categories = cursor.fetchall()
                
                # 计算每个类别的技能得分
                skills = {}
                for cat in categories:
                    # 基于完成课程数、平均分和最高难度计算得分
                    base_score = cat['avg_score'] if cat['avg_score'] else 0
                    difficulty_bonus = (cat['max_difficulty'] - 1) * 5
                    completion_bonus = min(cat['completed_count'] * 2, 20)
                    
                    skill_score = min(base_score + difficulty_bonus + completion_bonus, 100)
                    skills[cat['category']] = round(skill_score, 2)
                
                # 获取学习建议
                suggestions = []
                for cat, score in skills.items():
                    if score < 60:
                        suggestions.append({
                            'category': cat,
                            'level': 'basic',
                            'message': f"建议从基础课程开始学习{cat}相关内容"
                        })
                    elif score < 80:
                        suggestions.append({
                            'category': cat,
                            'level': 'intermediate',
                            'message': f"建议尝试更高难度的{cat}课程来提升技能"
                        })
                    else:
                        suggestions.append({
                            'category': cat,
                            'level': 'advanced',
                            'message': f"您在{cat}领域已经有很好的基础，可以尝试实战项目"
                        })
                
                return {
                    'skills': skills,
                    'suggestions': suggestions,
                    'total_score': round(sum(skills.values()) / len(skills), 2) if skills else 0
                }
                
            finally:
                cursor.close()
                conn.close()
                
        except Exception as e:
            logger.error(f"获取技能分析失败: {str(e)}")
            return {
                'skills': {},
                'suggestions': [],
                'total_score': 0
            }

# 创建全局实例
ai_assistant = AIAssistant() 