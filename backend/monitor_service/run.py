import asyncio
import logging
import sys
import os

from .service import MonitorService

async def main():
    """主函数"""
    try:
        # 创建并启动监控服务
        service = MonitorService()
        
        # 设置信号处理
        loop = asyncio.get_event_loop()
        for signal in ('SIGINT', 'SIGTERM'):
            try:
                loop.add_signal_handler(
                    getattr(signal, signal),
                    lambda: asyncio.create_task(service.stop())
                )
            except NotImplementedError:
                # Windows不支持SIGTERM
                pass
        
        # 启动服务
        await service.start()
        
    except Exception as e:
        logging.error(f"Service error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        # 运行主函数
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nService stopped by user")
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1) 