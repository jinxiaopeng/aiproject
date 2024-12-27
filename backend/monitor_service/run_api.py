import uvicorn
from app import app
from database import MonitorDB

def main():
    # 初始化数据库
    db = MonitorDB()
    
    # 启动API服务
    uvicorn.run(
        "monitor_service.app:app",
        host="0.0.0.0",
        port=8001,  # 修改默认端口为8001
        reload=True  # 开发模式下启用热重载
    )

if __name__ == "__main__":
    main() 