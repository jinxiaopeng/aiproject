from fastapi import APIRouter
from .routes import entities, relationships

# 创建主路由，添加/api前缀
router = APIRouter(prefix="/api")

# 注册子路由（只保留知识图谱相关的路由）
router.include_router(entities.router)
router.include_router(relationships.router) 