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
                },
                {
                    "id": "16",
                    "name": "密码学基础",
                    "category": "基础",
                    "difficulty": "入门",
                    "value": 8,
                    "description": "密码学是信息安全的基石，包括加密算法、哈希函数、数字签名等基础知识。",
                    "keyPoints": [
                        "对称加密与非对称加密",
                        "常见加密算法",
                        "哈希函数原理",
                        "数字签名和证书",
                        "密钥管理"
                    ],
                    "resources": [
                        {
                            "type": "在线课程",
                            "items": [
                                {
                                    "name": "密码学基础入门",
                                    "url": "https://example.com/crypto",
                                    "description": "面向安全工程师的密码学基础课程"
                                }
                            ]
                        }
                    ],
                    "prerequisites": ["1"],
                    "nextSteps": ["17", "18"]
                },
                {
                    "id": "17",
                    "name": "云安全基础",
                    "category": "技术",
                    "difficulty": "进阶",
                    "value": 9,
                    "description": "云计算环境下的安全架构、威胁和防护措施。",
                    "keyPoints": [
                        "云安全架构",
                        "容器安全",
                        "身份和访问管理",
                        "数据安全",
                        "合规性"
                    ],
                    "resources": [],
                    "prerequisites": ["11", "16"],
                    "nextSteps": ["19", "20"]
                },
                {
                    "id": "18",
                    "name": "安全开发实践",
                    "category": "技能",
                    "difficulty": "进阶",
                    "value": 8,
                    "description": "将安全实践集成到软件开发生命周期中。",
                    "keyPoints": [
                        "安全编码规范",
                        "代码审计实践",
                        "自动化安全测试",
                        "CI/CD安全集成"
                    ],
                    "resources": [],
                    "prerequisites": ["9", "16"],
                    "nextSteps": ["21"]
                },
                {
                    "id": "19",
                    "name": "微服务安全",
                    "category": "技术",
                    "difficulty": "高级",
                    "value": 9,
                    "description": "微服务架构特有的安全挑战和解决方案。",
                    "keyPoints": [
                        "服务认证与授权",
                        "API网关安全",
                        "服务间通信安全",
                        "容器编排安全"
                    ],
                    "resources": [],
                    "prerequisites": ["17"],
                    "nextSteps": ["22"]
                },
                {
                    "id": "20",
                    "name": "安全运维实践",
                    "category": "技术",
                    "difficulty": "高级",
                    "value": 8,
                    "description": "安全运维的最佳实践和工具使用。",
                    "keyPoints": [
                        "日志分析",
                        "安全监控",
                        "入侵检测",
                        "应急响应",
                        "漏洞管理"
                    ],
                    "resources": [],
                    "prerequisites": ["14", "17"],
                    "nextSteps": ["23"]
                },
                {
                    "id": "21",
                    "name": "移动应用安全",
                    "category": "技术",
                    "difficulty": "进阶",
                    "value": 8,
                    "description": "移动应用的安全开发和测试。",
                    "keyPoints": [
                        "移动应用漏洞",
                        "安全存储",
                        "通信安全",
                        "逆向分析防护"
                    ],
                    "resources": [],
                    "prerequisites": ["18"],
                    "nextSteps": ["24"]
                },
                {
                    "id": "22",
                    "name": "API安全设计",
                    "category": "技术",
                    "difficulty": "进阶",
                    "value": 7,
                    "description": "REST API和GraphQL API的安全设计和实现。",
                    "keyPoints": [
                        "认证机制",
                        "授权策略",
                        "限流防护",
                        "输入验证",
                        "错误处理"
                    ],
                    "resources": [],
                    "prerequisites": ["19"],
                    "nextSteps": []
                },
                {
                    "id": "23",
                    "name": "安全合规与审计",
                    "category": "管理",
                    "difficulty": "高级",
                    "value": 7,
                    "description": "安全合规要求、标准和审计实践。",
                    "keyPoints": [
                        "合规框架",
                        "安全策略制定",
                        "风险评估",
                        "审计方法",
                        "报告编写"
                    ],
                    "resources": [],
                    "prerequisites": ["20"],
                    "nextSteps": []
                },
                {
                    "id": "24",
                    "name": "物联网安全",
                    "category": "技术",
                    "difficulty": "高级",
                    "value": 8,
                    "description": "物联网设备和网络的安全防护。",
                    "keyPoints": [
                        "IoT协议安全",
                        "固件安全",
                        "硬件安全",
                        "通信加密",
                        "安全更新"
                    ],
                    "resources": [],
                    "prerequisites": ["21"],
                    "nextSteps": []
                },
                {
                    "id": "25",
                    "name": "区块链安全",
                    "category": "技术",
                    "difficulty": "高级",
                    "value": 9,
                    "description": "区块链技术的安全机制和漏洞分析。",
                    "keyPoints": [
                        "智能合约安全",
                        "共识机制安全",
                        "钱包安全",
                        "DeFi安全",
                        "区块链隐私保护"
                    ],
                    "resources": [],
                    "prerequisites": ["16", "22"],
                    "nextSteps": ["26"]
                },
                {
                    "id": "26",
                    "name": "AI安全与隐私",
                    "category": "技术",
                    "difficulty": "专家",
                    "value": 9,
                    "description": "人工智能系统的安全风险和防护策略。",
                    "keyPoints": [
                        "对抗性攻击",
                        "模型安全",
                        "数据隐私保护",
                        "AI伦理",
                        "可解释性安全"
                    ],
                    "resources": [],
                    "prerequisites": ["25"],
                    "nextSteps": []
                },
                {
                    "id": "27",
                    "name": "威胁情报分析",
                    "category": "技术",
                    "difficulty": "高级",
                    "value": 8,
                    "description": "网络威胁情报的收集、分析和应用。",
                    "keyPoints": [
                        "情报收集方法",
                        "威胁指标(IOC)",
                        "APT分析",
                        "情报共享",
                        "自动化分析"
                    ],
                    "resources": [],
                    "prerequisites": ["20", "25"],
                    "nextSteps": ["29"]
                },
                {
                    "id": "28",
                    "name": "零信任安全架构",
                    "category": "架构",
                    "difficulty": "高级",
                    "value": 8,
                    "description": "基于零信任模型的安全架构设计。",
                    "keyPoints": [
                        "零信任原则",
                        "身份验证",
                        "最小权限",
                        "微分段",
                        "持续监控"
                    ],
                    "resources": [],
                    "prerequisites": ["17", "26"],
                    "nextSteps": ["30"]
                },
                {
                    "id": "29",
                    "name": "恶意代码分析",
                    "category": "技术",
                    "difficulty": "专家",
                    "value": 9,
                    "description": "恶意软件的静态和动态分析技术。",
                    "keyPoints": [
                        "逆向工程",
                        "静态分析",
                        "动态分析",
                        "沙箱技术",
                        "混淆对抗"
                    ],
                    "resources": [],
                    "prerequisites": ["27"],
                    "nextSteps": ["31"]
                },
                {
                    "id": "30",
                    "name": "安全自动化",
                    "category": "技术",
                    "difficulty": "高级",
                    "value": 8,
                    "description": "安全运营和响应的自动化实践。",
                    "keyPoints": [
                        "SOAR平台",
                        "自动化响应",
                        "编排集成",
                        "安全工具开发",
                        "度量与优化"
                    ],
                    "resources": [],
                    "prerequisites": ["28"],
                    "nextSteps": ["32"]
                },
                {
                    "id": "31",
                    "name": "取证技术",
                    "category": "技术",
                    "difficulty": "专家",
                    "value": 8,
                    "description": "数字取证和事件调查技术。",
                    "keyPoints": [
                        "内存取证",
                        "网络取证",
                        "移动设备取证",
                        "证据提取",
                        "链式证据"
                    ],
                    "resources": [],
                    "prerequisites": ["29"],
                    "nextSteps": ["33"]
                },
                {
                    "id": "32",
                    "name": "量子密码学",
                    "category": "研究",
                    "difficulty": "专家",
                    "value": 9,
                    "description": "量子计算时代的密码学理论和实践。",
                    "keyPoints": [
                        "量子计算基础",
                        "后量子密码",
                        "量子密钥分发",
                        "量子安全协议",
                        "量子攻击防御"
                    ],
                    "resources": [],
                    "prerequisites": ["16", "30"],
                    "nextSteps": []
                },
                {
                    "id": "33",
                    "name": "硬件安全",
                    "category": "技术",
                    "difficulty": "专家",
                    "value": 8,
                    "description": "硬件级别的安全漏洞和防护措施。",
                    "keyPoints": [
                        "侧信道攻击",
                        "硬件木马",
                        "固件安全",
                        "安全启动",
                        "可信计算"
                    ],
                    "resources": [],
                    "prerequisites": ["31"],
                    "nextSteps": []
                },
                {
                    "id": "34",
                    "name": "云原生安全",
                    "category": "技术",
                    "difficulty": "高级",
                    "value": 9,
                    "description": "云原生应用和基础设施的安全防护。",
                    "keyPoints": [
                        "容器安全",
                        "K8s安全",
                        "服务网格安全",
                        "DevSecOps",
                        "云原生防火墙"
                    ],
                    "resources": [],
                    "prerequisites": ["17", "19"],
                    "nextSteps": ["35", "36"]
                },
                {
                    "id": "35",
                    "name": "供应链安全",
                    "category": "管理",
                    "difficulty": "高级",
                    "value": 8,
                    "description": "软件供应链的安全管理和防护。",
                    "keyPoints": [
                        "依赖包安全",
                        "构建过程安全",
                        "第三方组件管理",
                        "软件签名验证",
                        "漏洞追踪"
                    ],
                    "resources": [],
                    "prerequisites": ["34"],
                    "nextSteps": ["37"]
                },
                {
                    "id": "36",
                    "name": "红蓝对抗",
                    "category": "技术",
                    "difficulty": "专家",
                    "value": 9,
                    "description": "攻防实战演练和对抗技术。",
                    "keyPoints": [
                        "攻击链分析",
                        "战术技术分析",
                        "攻击模拟",
                        "防御体系",
                        "应急响应"
                    ],
                    "resources": [],
                    "prerequisites": ["29", "34"],
                    "nextSteps": ["38"]
                },
                {
                    "id": "37",
                    "name": "安全编排自动化",
                    "category": "技术",
                    "difficulty": "高级",
                    "value": 8,
                    "description": "安全运营的自动化和编排。",
                    "keyPoints": [
                        "安全编排平台",
                        "自动化响应",
                        "流程编排",
                        "集成开发",
                        "场景应用"
                    ],
                    "resources": [],
                    "prerequisites": ["30", "35"],
                    "nextSteps": ["39"]
                },
                {
                    "id": "38",
                    "name": "威胁狩猎",
                    "category": "技术",
                    "difficulty": "专家",
                    "value": 9,
                    "description": "主动寻找和分析潜在威胁。",
                    "keyPoints": [
                        "威胁假设",
                        "数据分析",
                        "异常检测",
                        "狩猎技术",
                        "工具开发"
                    ],
                    "resources": [],
                    "prerequisites": ["36"],
                    "nextSteps": ["40"]
                },
                {
                    "id": "39",
                    "name": "安全架构设计",
                    "category": "架构",
                    "difficulty": "专家",
                    "value": 9,
                    "description": "企业级安全架构的设计和实现。",
                    "keyPoints": [
                        "分层防御",
                        "纵深防御",
                        "安全基线",
                        "架构评估",
                        "风险控制"
                    ],
                    "resources": [],
                    "prerequisites": ["28", "37"],
                    "nextSteps": ["41"]
                },
                {
                    "id": "40",
                    "name": "高级持续威胁",
                    "category": "技术",
                    "difficulty": "专家",
                    "value": 9,
                    "description": "APT攻击分析与防御。",
                    "keyPoints": [
                        "APT组织分析",
                        "攻击特征",
                        "检测方法",
                        "防御策略",
                        "溯源技术"
                    ],
                    "resources": [],
                    "prerequisites": ["38"],
                    "nextSteps": ["42"]
                },
                {
                    "id": "41",
                    "name": "安全管理体系",
                    "category": "管理",
                    "difficulty": "高级",
                    "value": 8,
                    "description": "企业安全管理体系的建设。",
                    "keyPoints": [
                        "制度建设",
                        "流程管理",
                        "人员管理",
                        "资产管理",
                        "持续改进"
                    ],
                    "resources": [],
                    "prerequisites": ["39"],
                    "nextSteps": ["43"]
                },
                {
                    "id": "42",
                    "name": "安全研究方法",
                    "category": "研究",
                    "difficulty": "专家",
                    "value": 8,
                    "description": "安全漏洞研究和挖掘方法。",
                    "keyPoints": [
                        "漏洞挖掘",
                        "漏洞分析",
                        "利用开发",
                        "安全研究",
                        "论文发表"
                    ],
                    "resources": [],
                    "prerequisites": ["40"],
                    "nextSteps": []
                },
                {
                    "id": "43",
                    "name": "安全创新与发展",
                    "category": "研究",
                    "difficulty": "专家",
                    "value": 9,
                    "description": "安全技术的创新和未来发展。",
                    "keyPoints": [
                        "新技术应用",
                        "创新方向",
                        "发展趋势",
                        "学术研究",
                        "产业发展"
                    ],
                    "resources": [],
                    "prerequisites": ["41", "42"],
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
                {"source": "11", "target": "15", "value": 4, "type": "依赖"},
                {"source": "1", "target": "16", "value": 4, "type": "依赖"},
                {"source": "16", "target": "17", "value": 3, "type": "依赖"},
                {"source": "16", "target": "18", "value": 3, "type": "依赖"},
                {"source": "11", "target": "17", "value": 4, "type": "依赖"},
                {"source": "9", "target": "18", "value": 4, "type": "依赖"},
                {"source": "17", "target": "19", "value": 4, "type": "依赖"},
                {"source": "17", "target": "20", "value": 3, "type": "依赖"},
                {"source": "14", "target": "20", "value": 3, "type": "依赖"},
                {"source": "18", "target": "21", "value": 4, "type": "依赖"},
                {"source": "19", "target": "22", "value": 3, "type": "依赖"},
                {"source": "20", "target": "23", "value": 4, "type": "依赖"},
                {"source": "21", "target": "24", "value": 3, "type": "依赖"},
                {"source": "16", "target": "25", "value": 4, "type": "依赖"},
                {"source": "22", "target": "25", "value": 3, "type": "依赖"},
                {"source": "25", "target": "26", "value": 4, "type": "依赖"},
                {"source": "17", "target": "34", "value": 4, "type": "依赖"},
                {"source": "19", "target": "34", "value": 3, "type": "依赖"},
                {"source": "34", "target": "35", "value": 4, "type": "依赖"},
                {"source": "29", "target": "36", "value": 3, "type": "依赖"},
                {"source": "34", "target": "36", "value": 4, "type": "依赖"},
                {"source": "30", "target": "37", "value": 3, "type": "依赖"},
                {"source": "35", "target": "37", "value": 4, "type": "依赖"},
                {"source": "36", "target": "38", "value": 4, "type": "依赖"},
                {"source": "28", "target": "39", "value": 3, "type": "依赖"},
                {"source": "37", "target": "39", "value": 4, "type": "依赖"},
                {"source": "38", "target": "40", "value": 4, "type": "依赖"},
                {"source": "39", "target": "41", "value": 3, "type": "依赖"},
                {"source": "40", "target": "42", "value": 4, "type": "依赖"},
                {"source": "41", "target": "43", "value": 3, "type": "依赖"},
                {"source": "42", "target": "43", "value": 4, "type": "依赖"}
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