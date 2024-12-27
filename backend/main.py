import sys
import os
import time

# 添加项目根目录到 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)  # 获取项目根目录
sys.path.append(project_root)  # 添加项目根目录到路径

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.routers.auth import router as auth_router
from backend.routers.lab import router as lab_router
from backend.routers.user import router as user_router
from backend.routers.knowledge import router as knowledge_router
from backend.routers.challenge_router import router as challenge_router
from backend.routers.monitor import router as monitor_router
from backend.core.database import init_db
from backend.core.logger import get_logger

# 初始化日志系统
logger = get_logger(__name__)

app = FastAPI(
    title="Web安全智能学习平台",
    description="提供Web安全学习、靶场训练和AI辅助功能的综合平台",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")

# 标准格式的请求日志中间件
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # 获取真实的客户端IP
    forwarded_for = request.headers.get("x-forwarded-for")
    client_host = forwarded_for.split(",")[0] if forwarded_for else request.client.host
    
    # 获取用户代理
    user_agent = request.headers.get("user-agent", "Unknown")
    
    # 获取请求信息
    method = request.method
    path = request.url.path
    query_params = str(request.query_params) if request.query_params else ""
    
    # 记录请求开始
    logger.info(f"收到请求 | Method: {method} | Path: {path} | IP: {client_host} | UA: {user_agent[:50]}")
    
    try:
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        
        # 记录请求完成
        status_code = response.status_code
        status_text = "OK" if status_code < 400 else "Error"
        logger.info(
            f"请求完成 | Method: {method} | Path: {path} | Status: {status_code} {status_text} | "
            f"Time: {process_time:.2f}ms | IP: {client_host}"
        )
        
        return response
    except Exception as e:
        # 记录请求异常
        process_time = (time.time() - start_time) * 1000
        logger.error(
            f"请求异常 | Method: {method} | Path: {path} | Error: {str(e)} | "
            f"Time: {process_time:.2f}ms | IP: {client_host}"
        )
        raise

@app.get("/")
async def root():
    return {
        "message": "Welcome to Web Security Intelligent Learning Platform API",
        "version": "1.0.0",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

# 注册路由
app.include_router(auth_router, prefix="/api")  # 添加 /api 前缀
app.include_router(lab_router, prefix="/api")
app.include_router(user_router, prefix="/api")
app.include_router(knowledge_router, prefix="/api")
app.include_router(challenge_router, prefix="/api")  # 添加靶场路由
app.include_router(monitor_router, prefix="/api")  # 添加监控路由

# 初始化数据库
@app.on_event("startup")
async def startup_event():
    logger.info("Starting up application...")
    init_db()
    logger.info("Database initialized")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("应用关闭")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )