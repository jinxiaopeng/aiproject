from fastapi import APIRouter, HTTPException
from typing import List, Dict, Union
from pydantic import BaseModel

router = APIRouter()

class ResourceItem(BaseModel):
    name: str
    url: str
    description: str

class ResourceGroup(BaseModel):
    type: str
    items: List[ResourceItem]

class KnowledgeNode(BaseModel):
    id: Union[str, int]
    name: str
    category: str
    difficulty: str
    value: float
    description: str
    keyPoints: List[str]
    resources: List[ResourceGroup]
    prerequisites: List[str]
    nextSteps: List[str]

class KnowledgeLink(BaseModel):
    source: Union[str, int]
    target: Union[str, int]
    value: float
    type: str  # 关系类型：如 "依赖"、"相关"、"推荐" 等

class KnowledgeGraph(BaseModel):
    nodes: List[KnowledgeNode]
    links: List[KnowledgeLink]

@router.get("/graph", response_model=KnowledgeGraph)
async def get_knowledge_graph():
    """获取知识图谱数据"""
    try:
        return {
            "nodes": [
                {
                    "id": "1",
                    "name": "Web安全基础",
                    "category": "领域",
                    "difficulty": "入门",
                    "value": 10,
                    "description": "Web安全是网络安全的重要分支，主要关注Web应用程序的安全性。本节将介绍Web安全的基本概念和常见威胁。",
                    "keyPoints": [
                        "理解Web应用架构",
                        "HTTP协议基础",
                        "常见Web漏洞类型",
                        "基本的安全防护意识"
                    ],
                    "resources": [
                        {
                            "type": "在线课程",
                            "items": [
                                {
                                    "name": "Web安全入门实战",
                                    "url": "https://example.com/course1",
                                    "description": "适合初学者的Web安全入门课程"
                                }
                            ]
                        }
                    ],
                    "prerequisites": [],
                    "nextSteps": ["2", "3", "4", "5"]
                },
                {
                    "id": "2",
                    "name": "SQL注入攻击",
                    "category": "漏洞",
                    "difficulty": "进阶",
                    "value": 8,
                    "description": "SQL注入是最常见的Web应用程序漏洞之一，攻击者通过在用户输入中注入SQL代码来操纵数据库。",
                    "keyPoints": [
                        "SQL注入原理",
                        "常见的注入类型",
                        "注入攻击技术",
                        "防御措施"
                    ],
                    "resources": [
                        {
                            "type": "实验环境",
                            "items": [
                                {
                                    "name": "DVWA",
                                    "url": "https://example.com/dvwa",
                                    "description": "专门用于学习Web安全的脆弱性测试环境"
                                }
                            ]
                        }
                    ],
                    "prerequisites": ["1"],
                    "nextSteps": ["6", "7"]
                },
                {
                    "id": "3",
                    "name": "XSS跨站脚本",
                    "category": "漏洞",
                    "difficulty": "进阶",
                    "value": 8,
                    "description": "跨站脚本攻击是一种将恶意脚本注入到网页中的攻击方式，可能导致用户信息泄露或会话劫持。",
                    "keyPoints": [
                        "XSS攻击原理",
                        "反射型XSS",
                        "存储型XSS",
                        "DOM型XSS",
                        "XSS防御方法"
                    ],
                    "resources": [
                        {
                            "type": "在线实验",
                            "items": [
                                {
                                    "name": "XSS实验平台",
                                    "url": "https://example.com/xss",
                                    "description": "交互式XSS学习平台"
                                }
                            ]
                        }
                    ],
                    "prerequisites": ["1"],
                    "nextSteps": ["8", "9"]
                },
                {
                    "id": "4",
                    "name": "CSRF攻击",
                    "category": "漏洞",
                    "difficulty": "进阶",
                    "value": 7,
                    "description": "跨站请求伪造攻击利用用户已认证的会话执行未授权的操作。",
                    "keyPoints": [
                        "CSRF攻击原理",
                        "CSRF防御措施",
                        "Token验证",
                        "同源策略"
                    ],
                    "resources": [],
                    "prerequisites": ["1"],
                    "nextSteps": ["10"]
                },
                {
                    "id": "5",
                    "name": "文件上传漏洞",
                    "category": "漏洞",
                    "difficulty": "进阶",
                    "value": 7,
                    "description": "文件上传漏洞可能允许攻击者上传恶意文件到服务器。",
                    "keyPoints": [
                        "文件上传风险",
                        "文件类型验证",
                        "文件内容检查",
                        "存储位置安全"
                    ],
                    "resources": [],
                    "prerequisites": ["1"],
                    "nextSteps": ["11"]
                },
                {
                    "id": "6",
                    "name": "Python安全编程",
                    "category": "技能",
                    "difficulty": "进阶",
                    "value": 9,
                    "description": "使用Python进行安全开发和测试。",
                    "keyPoints": [
                        "Python基础",
                        "安全编程实践",
                        "常用安全库",
                        "自动化测试"
                    ],
                    "resources": [],
                    "prerequisites": ["2"],
                    "nextSteps": ["12"]
                },
                {
                    "id": "7",
                    "name": "JavaScript安全",
                    "category": "技能",
                    "difficulty": "进阶",
                    "value": 9,
                    "description": "前端JavaScript安全编程和防御技术。",
                    "keyPoints": [
                        "JavaScript安全编码",
                        "前端防御措施",
                        "客户端验证",
                        "API安全"
                    ],
                    "resources": [],
                    "prerequisites": ["3"],
                    "nextSteps": ["13"]
                },
                {
                    "id": "8",
                    "name": "渗透测试",
                    "category": "技术",
                    "difficulty": "高级",
                    "value": 9,
                    "description": "系统化的安全测试方法和技术。",
                    "keyPoints": [
                        "渗透测试方法论",
                        "信息收集",
                        "漏洞利用",
                        "后渗透阶段",
                        "报告编写"
                    ],
                    "resources": [],
                    "prerequisites": ["2", "3", "4"],
                    "nextSteps": ["14"]
                },
                {
                    "id": "9",
                    "name": "代码审计",
                    "category": "技术",
                    "difficulty": "高级",
                    "value": 8,
                    "description": "通过分析源代码发现安全漏洞。",
                    "keyPoints": [
                        "代码审计方法",
                        "常见漏洞模式",
                        "自动化工具",
                        "最佳实践"
                    ],
                    "resources": [],
                    "prerequisites": ["6", "7"],
                    "nextSteps": ["15"]
                },
                {
                    "id": "10",
                    "name": "WAF配置",
                    "category": "技术",
                    "difficulty": "进阶",
                    "value": 7,
                    "description": "Web应用防火墙的配置和管理。",
                    "keyPoints": [
                        "WAF原理",
                        "规则配置",
                        "绕过技术",
                        "日志分析"
                    ],
                    "resources": [],
                    "prerequisites": ["1"],
                    "nextSteps": []
                },
                {
                    "id": "11",
                    "name": "安全架构",
                    "category": "技术",
                    "difficulty": "高级",
                    "value": 8,
                    "description": "设计和实现安全的系统架构。",
                    "keyPoints": [
                        "安全架构原则",
                        "威胁建模",
                        "安全控制",
                        "风险评估"
                    ],
                    "resources": [],
                    "prerequisites": ["8", "9"],
                    "nextSteps": []
                },
                {
                    "id": "12",
                    "name": "漏洞扫描",
                    "category": "工具",
                    "difficulty": "入门",
                    "value": 7,
                    "description": "使用自动化工具发现系统漏洞。",
                    "keyPoints": [
                        "扫描器使用",
                        "漏洞验证",
                        "报告分析",
                        "误报处理"
                    ],
                    "resources": [],
                    "prerequisites": ["1"],
                    "nextSteps": ["8"]
                },
                {
                    "id": "13",
                    "name": "网络协议",
                    "category": "技能",
                    "difficulty": "进阶",
                    "value": 8,
                    "description": "理解和分析网络协议安全。",
                    "keyPoints": [
                        "TCP/IP协议栈",
                        "HTTP/HTTPS",
                        "DNS安全",
                        "加密通信"
                    ],
                    "resources": [],
                    "prerequisites": ["1"],
                    "nextSteps": ["14"]
                },
                {
                    "id": "14",
                    "name": "应急响应",
                    "category": "技术",
                    "difficulty": "高级",
                    "value": 8,
                    "description": "安全事件的处理和响应流程。",
                    "keyPoints": [
                        "事件分类",
                        "响应流程",
                        "取证分析",
                        "复盘总结"
                    ],
                    "resources": [],
                    "prerequisites": ["8", "9"],
                    "nextSteps": []
                },
                {
                    "id": "15",
                    "name": "安全开发流程",
                    "category": "技术",
                    "difficulty": "高级",
                    "value": 7,
                    "description": "在软件开发生命周期中集成安全实践。",
                    "keyPoints": [
                        "SDL流程",
                        "安全需求",
                        "安全测试",
                        "上线审核"
                    ],
                    "resources": [],
                    "prerequisites": ["11"],
                    "nextSteps": []
                }
            ],
            "links": [
                {"source": "1", "target": "2", "value": 5, "type": "依赖"},
                {"source": "1", "target": "3", "value": 5, "type": "依赖"},
                {"source": "1", "target": "4", "value": 4, "type": "依赖"},
                {"source": "1", "target": "5", "value": 4, "type": "依赖"},
                {"source": "2", "target": "6", "value": 3, "type": "依赖"},
                {"source": "3", "target": "7", "value": 3, "type": "依赖"},
                {"source": "2", "target": "8", "value": 4, "type": "依赖"},
                {"source": "3", "target": "8", "value": 4, "type": "依赖"},
                {"source": "4", "target": "8", "value": 3, "type": "依赖"},
                {"source": "6", "target": "9", "value": 4, "type": "依赖"},
                {"source": "7", "target": "9", "value": 4, "type": "依赖"},
                {"source": "8", "target": "11", "value": 3, "type": "依赖"},
                {"source": "9", "target": "11", "value": 3, "type": "依赖"},
                {"source": "1", "target": "12", "value": 3, "type": "依赖"},
                {"source": "12", "target": "8", "value": 3, "type": "依赖"},
                {"source": "1", "target": "13", "value": 4, "type": "依赖"},
                {"source": "13", "target": "14", "value": 3, "type": "依赖"},
                {"source": "8", "target": "14", "value": 4, "type": "依赖"},
                {"source": "9", "target": "14", "value": 3, "type": "依赖"},
                {"source": "11", "target": "15", "value": 4, "type": "依赖"}
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/node/{node_id}/complete")
async def mark_node_complete(node_id: str):
    """标记知识点为已学习"""
    try:
        # 实现标记逻辑
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/path/{node_id}")
async def get_learning_path(node_id: str):
    """获取指定知识点的学习路径"""
    try:
        # 实现学习路径生成逻辑
        return {"path": []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 