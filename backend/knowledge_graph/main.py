from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .api import router
from .core.logger import logger

app = FastAPI(
    title="知识图谱服务",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 明确指定前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    # 记录请求信息
    logger.info(f"收到请求: {request.method} {request.url.path}")
    logger.info(f"请求头: {dict(request.headers)}")
    
    # 记录请求体
    try:
        body = await request.body()
        if body:
            logger.info(f"请求体: {body.decode()}")
    except Exception as e:
        logger.error(f"读取请求体失败: {str(e)}")
    
    # 记录查询参数
    if request.query_params:
        logger.info(f"查询参数: {dict(request.query_params)}")
    
    # 处理请求
    response = await call_next(request)
    
    # 记录响应信息
    logger.info(f"响应状态码: {response.status_code}")
    
    return response

# 注册路由
app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "知识图谱服务已启动"}

if __name__ == "__main__":
    import uvicorn
    logger.info("启动知识图谱服务...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info") 