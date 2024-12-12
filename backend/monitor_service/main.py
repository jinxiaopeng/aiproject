from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from routes import monitor
from database import Base, engine

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="监控预警服务",
    description="提供系统监控和安全预警功能",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

# 注册路由
app.include_router(monitor.router, prefix="/api")

@app.get("/")
async def root():
    return {
        "message": "监控预警服务API",
        "version": "1.0.0",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "monitor_service.main:app",
        host="0.0.0.0",
        port=8001,
        reload=True
    ) 