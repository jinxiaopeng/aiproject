from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any, Optional
import logging
from backend.core.deps import get_current_user
from backend.models.user import User
from pydantic import BaseModel
from backend.core.ai.manager import model_manager

router = APIRouter(prefix="/ai", tags=["ai"])
logger = logging.getLogger(__name__)

class ChatRequest(BaseModel):
    message: str
    context: List[Dict[str, str]] = []

class CodeAnalysisRequest(BaseModel):
    code: str
    language: str

class VulnerabilityRequest(BaseModel):
    vulnerability_type: str

class ChallengeRequest(BaseModel):
    difficulty: str
    category: str
    skills: Optional[List[str]] = None

class LearningPathRequest(BaseModel):
    target_skill: str
    current_level: str
    time_commitment: str

@router.get("/models")
async def list_models(
    current_user: User = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """获取可用的AI模型列表"""
    try:
        return model_manager.list_models()
    except Exception as e:
        logger.error(f"获取模型列表失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取模型列表失败: {str(e)}")

@router.post("/chat")
async def chat_with_ai(
    request: ChatRequest,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """与AI助手对话"""
    try:
        model = model_manager.get_model()
        return model.chat(request.message, request.context)
    except Exception as e:
        logger.error(f"AI对话失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI对话失败: {str(e)}")

@router.post("/analyze_code")
async def analyze_code(
    request: CodeAnalysisRequest,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """分析代码中的安全问题"""
    try:
        model = model_manager.get_model()
        return model.analyze_code(request.code, request.language)
    except Exception as e:
        logger.error(f"代码分析失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"代码分析失败: {str(e)}")

@router.post("/explain_vulnerability")
async def explain_vulnerability(
    request: VulnerabilityRequest,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """解释漏洞原理"""
    try:
        model = model_manager.get_model()
        return model.explain_vulnerability(request.vulnerability_type)
    except Exception as e:
        logger.error(f"漏洞解释生成失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"漏洞解释生成失败: {str(e)}")

@router.post("/generate_challenge")
async def generate_challenge(
    request: ChallengeRequest,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """生成练习题目"""
    try:
        model = model_manager.get_model()
        return model.generate_challenge(
            request.difficulty,
            request.category,
            request.skills
        )
    except Exception as e:
        logger.error(f"题目生成失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"题目生成失败: {str(e)}")

@router.post("/learning_path")
async def generate_learning_path(
    request: LearningPathRequest,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """生成个性化学习路径"""
    try:
        model = model_manager.get_model()
        return model.generate_learning_path(
            request.target_skill,
            request.current_level,
            request.time_commitment
        )
    except Exception as e:
        logger.error(f"学习路径生成失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"学习路径生成失败: {str(e)}")

@router.post("/reload_model")
async def reload_model(
    current_user: User = Depends(get_current_user)
) -> Dict[str, str]:
    """重新加载AI模型"""
    try:
        model_manager.reload_model()
        return {"message": "AI模型重新加载成功"}
    except Exception as e:
        logger.error(f"AI模型重新加载失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI模型重新加载失败: {str(e)}") 