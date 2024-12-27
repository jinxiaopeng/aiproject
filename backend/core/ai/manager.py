import os
from typing import Optional, List, Dict, Any
import logging
from .model import AIModel

logger = logging.getLogger(__name__)

class AIModelManager:
    _instance: Optional[AIModel] = None
    
    @classmethod
    def get_model(cls) -> AIModel:
        """获取AI模型实例（单例模式）
        
        Returns:
            AIModel实例
        """
        if cls._instance is None:
            api_url = os.getenv("AI_API_URL", "http://127.0.0.1:1234")
            
            try:
                cls._instance = AIModel(api_url)
                logger.info(f"AI模型实例创建成功: {api_url}")
            except Exception as e:
                logger.error(f"AI模型实例创建失败: {str(e)}")
                raise
        
        return cls._instance
    
    @classmethod
    def reload_model(cls) -> None:
        """重新加载AI模型"""
        if cls._instance is not None:
            del cls._instance
            cls._instance = None
        cls.get_model()
    
    @classmethod
    def list_models(cls) -> List[Dict[str, Any]]:
        """获取可用模型列表
        
        Returns:
            可用模型列表
        """
        api_url = os.getenv("AI_API_URL", "http://198.18.0.1:1234")
        return AIModel.list_models(api_url)

# 创建全局模型管理器实例
model_manager = AIModelManager() 