from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from monitor_service.api import learning

app = FastAPI(title="Learning Monitor Service")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(learning.router)

@app.get("/")
async def root():
    return {"message": "Learning Monitor Service is running"} 