from typing import List, Dict, Any, Optional
import logging
import requests
import json

logger = logging.getLogger(__name__)

class AIModel:
    def __init__(self, api_url: str = "http://127.0.0.1:1234"):
        """初始化AI模型
        
        Args:
            api_url: API地址
        """
        self.api_url = api_url
        self.model_name = "qwen2.5-coder-7b-instruct"
        try:
            # 检查服务器健康状态
            health_response = requests.get(f"{self.api_url}/health")
            if health_response.status_code != 200:
                raise ConnectionError("AI模型服务器连接失败")
            
            # 检查模型是否可用
            models_response = requests.get(f"{self.api_url}/v1/models")
            if models_response.status_code != 200:
                raise Exception("无法获取模型列表")
            
            available_models = models_response.json()
            if not any(model["id"] == self.model_name for model in available_models["data"]):
                raise Exception(f"模型 {self.model_name} 不可用")
            
            logger.info(f"AI模型连接成功，使用模型: {self.model_name}")
        except Exception as e:
            logger.error(f"AI模型初始化失败: {str(e)}")
            raise

    @classmethod
    def list_models(cls, api_url: str = "http://198.18.0.1:1234") -> List[Dict[str, Any]]:
        """获取可用���型列表
        
        Args:
            api_url: API地址
            
        Returns:
            可用模型列表
        """
        try:
            response = requests.get(f"{api_url}/v1/models")
            if response.status_code != 200:
                raise Exception("无法获取模型列表")
            
            result = response.json()
            return result["data"]
        except Exception as e:
            logger.error(f"获取模型列表失败: {str(e)}")
            raise

    def generate(
        self,
        prompt: str,
        max_length: int = 2048,
        temperature: float = 0.7,
        top_p: float = 0.9,
    ) -> str:
        """生成回复
        
        Args:
            prompt: 提示词
            max_length: 最大生成长度
            temperature: 温度参数
            top_p: 核采样参数
            
        Returns:
            生成的回复文本
        """
        try:
            payload = {
                "model": self.model_name,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_length,
                "temperature": temperature,
                "top_p": top_p
            }
            
            response = requests.post(f"{self.api_url}/v1/chat/completions", json=payload)
            if response.status_code != 200:
                raise Exception(f"API调用失败: {response.text}")
                
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"AI生成失败: {str(e)}")
            raise

    def chat(self, message: str, context: List[Dict[str, str]] = []) -> Dict[str, Any]:
        """处理对话请求"""
        try:
            messages = [{"role": msg["role"], "content": msg["content"]} for msg in context]
            messages.append({"role": "user", "content": message})
            
            payload = {
                "model": self.model_name,
                "messages": messages,
                "temperature": 0.7,
                "top_p": 0.9
            }
            
            response = requests.post(f"{self.api_url}/v1/chat/completions", json=payload)
            if response.status_code != 200:
                raise Exception(f"API调用失败: {response.text}")
                
            result = response.json()
            assistant_message = result["choices"][0]["message"]["content"]
            
            new_context = context + [
                {"role": "user", "content": message},
                {"role": "assistant", "content": assistant_message}
            ]
            
            return {
                "response": assistant_message,
                "context": new_context
            }
        except Exception as e:
            logger.error(f"对话处理失败: {str(e)}")
            raise

    def analyze_code(self, code: str, language: str) -> Dict[str, Any]:
        """分析代码中的安全问题"""
        try:
            prompt = f"""作为一个安全专家，请分析以下{language}代码中的安全问题。
请按以下格式输出JSON：
{{
    "vulnerabilities": ["漏洞1", "漏洞2", ...],
    "suggestions": ["建议1", "建议2", ...],
    "risk_level": "high/medium/low"
}}

代码：
{code}"""
            
            response = self.generate(prompt)
            try:
                return json.loads(response)
            except:
                # 如果JSON解析失败，返回格式化的结果
                return self._parse_code_analysis(response)
        except Exception as e:
            logger.error(f"代码分析失败: {str(e)}")
            raise

    def explain_vulnerability(self, vulnerability_type: str) -> Dict[str, Any]:
        """解释漏洞原理"""
        try:
            prompt = f"""作为一个安全专家，请详细解释{vulnerability_type}漏洞。
请按以下格式输出JSON：
{{
    "vulnerability_type": "{vulnerability_type}",
    "explanation": "漏洞原理详细解释",
    "examples": ["示例1", "示例2", ...],
    "prevention": ["防护建议1", "防护建议2", ...]
}}"""
            
            response = self.generate(prompt)
            try:
                return json.loads(response)
            except:
                return self._parse_vulnerability_explanation(response)
        except Exception as e:
            logger.error(f"漏洞解释生成失败: {str(e)}")
            raise

    def generate_challenge(
        self,
        difficulty: str,
        category: str,
        skills: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """生成练习题目"""
        try:
            skills_str = "、".join(skills) if skills else "通用技能"
            prompt = f"""作为一个安全培训专家，请生成一个{difficulty}难度的{category}安全练习题目，涉及{skills_str}。
请按以下格式输出JSON：
{{
    "title": "题目标题",
    "description": "详细描述",
    "difficulty": "{difficulty}",
    "category": "{category}",
    "hints": ["提示1", "提示2", ...],
    "resources": [
        {{"name": "资源名称", "type": "article/video/lab", "url": "资源链接"}}
    ]
}}"""
            
            response = self.generate(prompt)
            try:
                return json.loads(response)
            except:
                return self._parse_challenge(response)
        except Exception as e:
            logger.error(f"题目生成失败: {str(e)}")
            raise

    def generate_learning_path(
        self,
        target_skill: str,
        current_level: str,
        time_commitment: str
    ) -> Dict[str, Any]:
        """生成学习路径"""
        try:
            prompt = f"""作为一个安全教育专家，请为{current_level}水平的学习者制定{target_skill}的学习路径，每周可投入{time_commitment}。
请按以下格式输出JSON：
{{
    "estimatedTime": "预计完成时间",
    "stages": [
        {{
            "title": "阶段标题",
            "description": "阶段描述",
            "duration": "持续时间",
            "status": "pending",
            "skills": ["技能1", "技能2"],
            "resources": [
                {{"name": "资源名称", "type": "课程类型", "difficulty": "难度", "url": "资源链接"}}
            ]
        }}
    ]
}}"""
            
            response = self.generate(prompt)
            try:
                return json.loads(response)
            except:
                return self._parse_learning_path(response)
        except Exception as e:
            logger.error(f"学习路径生成失败: {str(e)}")
            raise

    def _parse_code_analysis(self, analysis: str) -> Dict[str, Any]:
        """解析代码分析结果"""
        return {
            "vulnerabilities": [analysis.strip()],
            "suggestions": ["请根据分析结果进行修复"],
            "risk_level": "medium"
        }

    def _parse_vulnerability_explanation(self, explanation: str) -> Dict[str, Any]:
        """解析漏洞解释结果"""
        return {
            "explanation": explanation,
            "examples": ["请参考解释中的示例"],
            "prevention": ["请参考解释中的防护建议"]
        }

    def _parse_challenge(self, challenge: str) -> Dict[str, Any]:
        """解析题目生成结果"""
        return {
            "title": "安全挑战题目",
            "description": challenge,
            "hints": ["请仔细阅读题目描述"],
            "resources": []
        }

    def _parse_learning_path(self, path: str) -> Dict[str, Any]:
        """解析学习路径结果"""
        return {
            "estimatedTime": "根据学习内容确定",
            "stages": [
                {
                    "title": "学习阶段",
                    "description": path,
                    "duration": "请根据实际情况安排",
                    "status": "pending",
                    "skills": ["相关技能"],
                    "resources": []
                }
            ]
        } 