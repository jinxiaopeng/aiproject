from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp, Message
from typing import Dict, Any, Callable
import time
import traceback
from .logger import system_logger

class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            # 记录请求开始时间
            start_time = time.time()
            
            # 处理请求
            response = await call_next(request)
            
            # 记录请求信息
            process_time = time.time() - start_time
            log_data = {
                'method': request.method,
                'url': str(request.url),
                'client_ip': request.client.host,
                'process_time': f"{process_time:.3f}s",
                'status_code': response.status_code
            }
            
            # 根据状态码记录不同级别的日志
            if response.status_code >= 500:
                system_logger.error("请求处理失败", "http", log_data)
            elif response.status_code >= 400:
                system_logger.warning("请求处理异常", "http", log_data)
            else:
                system_logger.info("请求处理成功", "http", log_data)
                
            return response
            
        except HTTPException as e:
            # 处理HTTP异常
            error_detail = {
                'method': request.method,
                'url': str(request.url),
                'client_ip': request.client.host,
                'error': str(e.detail)
            }
            system_logger.warning("HTTP异常", "http", error_detail)
            
            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail}
            )
            
        except Exception as e:
            # 处理其他异常
            error_detail = {
                'method': request.method,
                'url': str(request.url),
                'client_ip': request.client.host,
                'error': str(e),
                'traceback': traceback.format_exc()
            }
            system_logger.error("系统异常", "http", error_detail)
            
            return JSONResponse(
                status_code=500,
                content={"detail": "内部服务器错误"}
            )

class RequestValidationErrorHandler:
    """请求验证错误处理器"""
    def __init__(self, app: ASGIApp):
        self.app = app
        
    async def __call__(self, scope: Dict, receive: Callable, send: Callable):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
            
        async def wrapped_receive():
            message = await receive()
            return message
            
        async def wrapped_send(message: Message):
            if message["type"] == "http.response.start":
                status = message.get("status", 200)
                if status == 422:  # 请求验证错误
                    headers = [(k, v) for k, v in message.get("headers", [])]
                    await send({
                        "type": "http.response.start",
                        "status": 400,  # 修改状态码为400
                        "headers": headers
                    })
                    return
            await send(message)
            
        await self.app(scope, wrapped_receive, wrapped_send)

class RateLimitMiddleware(BaseHTTPMiddleware):
    """请求速率限制中间件"""
    def __init__(self, app: ASGIApp, rate_limit: int = 100):
        super().__init__(app)
        self.rate_limit = rate_limit
        self.requests = {}
        
    async def dispatch(self, request: Request, call_next):
        # 获取客户端IP
        client_ip = request.client.host
        current_time = time.time()
        
        # 清理过期的请求记录
        self.cleanup_old_requests(current_time)
        
        # 检查请求频率
        if self.is_rate_limited(client_ip, current_time):
            error_detail = {
                'client_ip': client_ip,
                'rate_limit': self.rate_limit,
                'url': str(request.url)
            }
            system_logger.warning("请求频率超限", "rate_limit", error_detail)
            
            return JSONResponse(
                status_code=429,
                content={"detail": "请求过于频繁，请稍后再试"}
            )
            
        # 记录请求
        self.record_request(client_ip, current_time)
        
        # 处理请求
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            system_logger.error(f"请求处理失败: {str(e)}", "rate_limit", {
                'client_ip': client_ip,
                'url': str(request.url)
            })
            raise
        
    def cleanup_old_requests(self, current_time: float):
        """清理超过1分钟的旧请求记录"""
        try:
            for ip in list(self.requests.keys()):
                self.requests[ip] = [ts for ts in self.requests[ip] if current_time - ts <= 60]
                if not self.requests[ip]:
                    del self.requests[ip]
        except Exception as e:
            system_logger.error(f"清理请求记录失败: {str(e)}", "rate_limit")
                
    def is_rate_limited(self, client_ip: str, current_time: float) -> bool:
        """检查是否超过速率限制"""
        try:
            if client_ip not in self.requests:
                return False
                
            # 获取最近1分钟的请求次数
            recent_requests = len([ts for ts in self.requests[client_ip] if current_time - ts <= 60])
            return recent_requests >= self.rate_limit
        except Exception as e:
            system_logger.error(f"检查速率限制失败: {str(e)}", "rate_limit")
            return False
        
    def record_request(self, client_ip: str, current_time: float):
        """记录请求"""
        try:
            if client_ip not in self.requests:
                self.requests[client_ip] = []
            self.requests[client_ip].append(current_time)
        except Exception as e:
            system_logger.error(f"记录请求失败: {str(e)}", "rate_limit")

class SecurityMiddleware(BaseHTTPMiddleware):
    """安全中间件"""
    async def dispatch(self, request: Request, call_next):
        try:
            # 处理请求
            response = await call_next(request)
            
            # 添加安全响应头
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["X-XSS-Protection"] = "1; mode=block"
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
            response.headers["Content-Security-Policy"] = "default-src 'self'"
            
            return response
        except Exception as e:
            system_logger.error(f"安全中间件处理失败: {str(e)}", "security", {
                'url': str(request.url),
                'client_ip': request.client.host
            })
            raise 