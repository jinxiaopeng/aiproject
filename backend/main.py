from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, challenge, knowledge

app = FastAPI(
    title="Web安全智能学习平台",
    description="提供Web安全学习、靶场训练和AI辅助功能的综合平台",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3017", "http://127.0.0.1:3000", "http://127.0.0.1:3017"],  # 允许前端开发服务器的来源
    allow_credentials=True,  # 允许携带凭证
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]  # 允许前端访问的响应头
)

# 注册路由
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(challenge.router, prefix="/api/challenges", tags=["challenges"])
app.include_router(knowledge.router, prefix="/api/knowledge", tags=["knowledge"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True  # 开发模式下启用热重载
    ) 