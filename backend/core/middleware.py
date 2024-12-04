from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
import time
from typing import Optional

from core.logger import system_logger

class SecurityMiddleware(BaseHTTPMiddleware):
    """安全中间件"""
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            # 添加安全响应头
            response = await call_next(request)
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["X-XSS-Protection"] = "1; mode=block"
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
            return response
        except Exception as e:
            system_logger.error(f"安全中间件错误: {str(e)}", "security")
            return JSONResponse(
                status_code=500,
                content={"detail": "内部服务器错误"}
            )

class ExceptionMiddleware(BaseHTTPMiddleware):
    """异常处理中间件"""
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            return await call_next(request)
        except HTTPException as e:
            system_logger.warning(f"HTTP异常: {str(e)}", "http", {
                "status_code": e.status_code,
                "detail": e.detail
            })
            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail}
            )
        except Exception as e:
            system_logger.error(f"未处理的异常: {str(e)}", "system")
            return JSONResponse(
                status_code=500,
                content={"detail": "内部服务器错误"}
            )

class RateLimitMiddleware(BaseHTTPMiddleware):
    """速率限制中间件"""
    def __init__(self, app, rate_limit: int = 100):
        super().__init__(app)
        self.rate_limit = rate_limit
        self.requests = {}

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # 获取客户端IP
        client_ip = request.client.host
        current_time = time.time()

        # 清理过期的请求记录
        if client_ip in self.requests:
            self.requests[client_ip] = [t for t in self.requests[client_ip] if current_time - t < 60]

        # 检查请求频率
        if client_ip in self.requests and len(self.requests[client_ip]) >= self.rate_limit:
            system_logger.warning(f"请求频率超限: {client_ip}", "rate_limit")
            return JSONResponse(
                status_code=429,
                content={"detail": "请求过于频繁，请稍后再试"}
            )

        # 记录请求时间
        if client_ip not in self.requests:
            self.requests[client_ip] = []
        self.requests[client_ip].append(current_time)

        return await call_next(request)

class RequestValidationErrorHandler:
    """请求验证错误处理器"""
    async def __call__(self, request: Request, exc: Exception) -> JSONResponse:
        system_logger.warning(f"请求验证错误: {str(exc)}", "validation")
        return JSONResponse(
            status_code=422,
            content={"detail": "请求参数验证失败"}
        )