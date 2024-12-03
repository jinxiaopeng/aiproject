import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.append(str(project_root))
sys.path.append(str(project_root.parent))

from fastapi import FastAPI, HTTPException, Depends, Body, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from typing import Optional, Dict, List
import uvicorn
import mysql.connector
import traceback
from datetime import timedelta

from config import CONFIG, DEBUG, JWT_SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from core.auth import (
    authenticate_user, create_access_token, get_current_user,
    create_user_session, update_last_activity,
    invalidate_user_sessions
)
from core.lab.manager import lab_manager
from core.ai.model import ai_assistant
from core.monitor import system_monitor
from core.scheduler import task_scheduler
from core.logger import system_logger
from core.config_validator import config_validator
from core.middleware import (
    ExceptionMiddleware,
    RequestValidationErrorHandler,
    RateLimitMiddleware,
    SecurityMiddleware
)

# 创建FastAPI应用
app = FastAPI(
    title="Web安全智能学习平台",
    description="提供Web安全学习、靶场训练和AI辅助功能的综合平台",
    version="1.0.0",
    debug=DEBUG
)

# 配置中间件
app.add_middleware(SecurityMiddleware)
app.add_middleware(ExceptionMiddleware)
app.add_middleware(RateLimitMiddleware, rate_limit=100)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据库连接
def get_db():
    """获取数据库连接"""
    try:
        conn = mysql.connector.connect(**CONFIG['database'])
        return conn
    except Exception as e:
        error_msg = f"数据库连接失败: {str(e)}"
        system_logger.error(error_msg, "database")
        raise HTTPException(status_code=500, detail=error_msg)

@app.on_event("startup")
async def startup_event():
    """应用启动时的初始化操作"""
    try:
        # 检查数据库连接
        conn = get_db()
        conn.close()
        system_logger.info("数据库连接检查成功", "startup")
        
        # 启动任务调度器
        task_scheduler.start()
        system_logger.info("任务调度器启动成功", "startup")
        
    except Exception as e:
        error_msg = f"应用启动失败: {str(e)}"
        system_logger.critical(error_msg, "startup")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时的清理操作"""
    try:
        # 关闭任务调度器
        task_scheduler.shutdown()
        system_logger.info("任务调度器关闭成功", "shutdown")
        
    except Exception as e:
        error_msg = f"应用关闭时出错: {str(e)}"
        system_logger.error(error_msg, "shutdown")

# 异常处理
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """处理请求验证错误"""
    error_detail = {
        'method': request.method,
        'url': str(request.url),
        'client_ip': request.client.host,
        'errors': str(exc.errors())
    }
    system_logger.warning("请求验证错误", "validation", error_detail)
    
    return JSONResponse(
        status_code=400,
        content={"detail": "请求参数验证失败", "errors": exc.errors()}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """处理HTTP异常"""
    error_detail = {
        'method': request.method,
        'url': str(request.url),
        'client_ip': request.client.host,
        'status_code': exc.status_code,
        'detail': exc.detail
    }
    system_logger.warning("HTTP异常", "http", error_detail)
    
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """处理通用异常"""
    error_detail = {
        'method': request.method,
        'url': str(request.url),
        'client_ip': request.client.host,
        'error': str(exc),
        'traceback': traceback.format_exc()
    }
    system_logger.error("系统异常", "system", error_detail)
    
    return JSONResponse(
        status_code=500,
        content={"detail": "内部服务器错误"}
    )

# 认证路由
@app.post("/api/auth/login")
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """用户登录"""
    try:
        user = await authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=401,
                detail="用户名或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 创建访问令牌
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user["username"]},
            expires_delta=access_token_expires
        )
        
        # 创建用户会话
        create_user_session(
            user_id=user["id"],
            token=access_token,
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent")
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }
    except Exception as e:
        system_logger.error(f"登录失败: {str(e)}", "auth", {
            'username': form_data.username,
            'ip': request.client.host
        })
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/auth/logout")
async def logout(current_user: Dict = Depends(get_current_user)):
    """用户登出"""
    try:
        invalidate_user_sessions(current_user["id"])
        system_logger.info(f"用户登出成功: {current_user['username']}", "auth")
        return {"message": "登出成功"}
    except Exception as e:
        system_logger.error(f"登出失败: {str(e)}", "auth", {
            'user_id': current_user["id"]
        })
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/user/info")
async def read_users_me(
    request: Request,
    current_user: Dict = Depends(get_current_user)
):
    """获取当前用户信息"""
    try:
        # 更新用户活动时间
        token = request.headers.get("authorization", "").split(" ")[-1]
        update_last_activity(current_user["id"], token)
        return current_user
    except Exception as e:
        system_logger.error(f"获取用户信息失败: {str(e)}", "auth", {
            'user_id': current_user["id"]
        })
        raise HTTPException(status_code=500, detail=str(e))

# 系统监控路由
@app.get("/api/monitor/system")
async def get_system_status(current_user = Depends(get_current_user)):
    """获取系统状态"""
    if current_user['role'] != 'admin':
        raise HTTPException(status_code=403, detail="没有权限访问此接口")
    return system_monitor.get_system_status()

@app.get("/api/monitor/docker")
async def get_docker_status(current_user = Depends(get_current_user)):
    """获取Docker状态"""
    if current_user['role'] != 'admin':
        raise HTTPException(status_code=403, detail="没有权限访问此接口")
    return system_monitor.get_docker_status()

@app.get("/api/monitor/database")
async def get_database_status(current_user = Depends(get_current_user)):
    """获取数据库状态"""
    if current_user['role'] != 'admin':
        raise HTTPException(status_code=403, detail="没有权限访此接口")
    return system_monitor.get_database_status()

@app.get("/api/monitor/active-users")
async def get_active_users(current_user = Depends(get_current_user)):
    """获取活跃用户信息"""
    if current_user['role'] != 'admin':
        raise HTTPException(status_code=403, detail="没有权限访问此接口")
    return system_monitor.get_active_users()

# 课程相关路由
@app.get("/api/courses")
async def get_courses(current_user = Depends(get_current_user)):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM courses")
        courses = cursor.fetchall()
        return courses
    finally:
        cursor.close()
        conn.close()

@app.get("/api/courses/{course_id}")
async def get_course_detail(course_id: int, current_user = Depends(get_current_user)):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM courses WHERE id = %s", (course_id,))
        course = cursor.fetchone()
        if not course:
            raise HTTPException(status_code=404, detail="课程不存在")
        return course
    finally:
        cursor.close()
        conn.close()

# 靶场相关路由
@app.get("/api/labs")
async def get_labs(current_user = Depends(get_current_user)):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM labs")
        labs = cursor.fetchall()
        return labs
    finally:
        cursor.close()
        conn.close()

@app.post("/api/labs/{lab_id}/start")
async def start_lab(lab_id: int, current_user = Depends(get_current_user)):
    try:
        result = lab_manager.start_lab(lab_id, current_user["id"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/labs/{lab_id}/stop")
async def stop_lab(lab_id: int, current_user = Depends(get_current_user)):
    try:
        result = lab_manager.stop_lab(lab_id, current_user["id"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/labs/{lab_id}/status")
async def get_lab_status(lab_id: int, current_user = Depends(get_current_user)):
    try:
        result = lab_manager.get_lab_status(lab_id, current_user["id"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# AI辅助相关路由
@app.get("/api/ai/suggestions")
async def get_learning_suggestions(current_user = Depends(get_current_user)):
    try:
        suggestions = ai_assistant.get_learning_suggestions(current_user["id"])
        return suggestions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ai/analyze-vulnerability")
async def analyze_vulnerability(code: str = Body(...), current_user = Depends(get_current_user)):
    try:
        results = ai_assistant.analyze_vulnerability(code)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/ai/skill-analysis")
async def get_skill_analysis(current_user = Depends(get_current_user)):
    try:
        analysis = ai_assistant.get_skill_analysis(current_user["id"])
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 分析相关路由
@app.get("/api/analysis/skill-radar")
async def get_skill_radar(current_user = Depends(get_current_user)):
    try:
        analysis = ai_assistant.get_skill_analysis(current_user["id"])
        skills = analysis["skills"]
        return {
            "categories": list(skills.keys()),
            "values": list(skills.values())
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analysis/progress-trend")
async def get_progress_trend(current_user = Depends(get_current_user)):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT 
                DATE_FORMAT(created_at, '%Y-%m') as month,
                AVG(score) as avg_score
            FROM learning_history
            WHERE user_id = %s
            GROUP BY month
            ORDER BY month
            LIMIT 6
        """, (current_user["id"],))
        results = cursor.fetchall()
        return {
            "dates": [r["month"] for r in results],
            "values": [float(r["avg_score"]) for r in results]
        }
    finally:
        cursor.close()
        conn.close()

# 用户注册路由
@app.post("/api/auth/register")
async def register(
    username: str = Body(...),
    password: str = Body(...),
    email: str = Body(...)
):
    """用户注册"""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        try:
            # 检查用户名是否已存在
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="用户名已存在")
                
            # 检查邮箱是否已存在
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="邮箱已被注册")
                
            # 创建新用户
            hashed_password = get_password_hash(password)
            cursor.execute("""
                INSERT INTO users (username, password, email)
                VALUES (%s, %s, %s)
            """, (username, hashed_password, email))
            conn.commit()
            
            # 返回新用户信息
            cursor.execute("SELECT id, username, email, role FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            return user
            
        finally:
            cursor.close()
            conn.close()
            
    except HTTPException:
        raise
    except Exception as e:
        system_logger.error(f"注册失败: {str(e)}", "auth", {
            'username': username,
            'email': email
        })
        raise HTTPException(status_code=500, detail="注册失败")

# 用户资料更新路由
@app.put("/api/user/profile")
async def update_profile(
    email: Optional[str] = Body(None),
    current_password: Optional[str] = Body(None),
    new_password: Optional[str] = Body(None),
    current_user: Dict = Depends(get_current_user)
):
    """更新用户资料"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        try:
            updates = []
            values = []
            
            # 更新邮箱
            if email and email != current_user["email"]:
                # 检查邮箱是否已被使用
                cursor.execute("SELECT id FROM users WHERE email = %s AND id != %s", (email, current_user["id"]))
                if cursor.fetchone():
                    raise HTTPException(status_code=400, detail="邮箱已被使用")
                updates.append("email = %s")
                values.append(email)
            
            # 更新密码
            if current_password and new_password:
                # 验证当前密码
                cursor.execute("SELECT password FROM users WHERE id = %s", (current_user["id"],))
                stored_password = cursor.fetchone()[0]
                if not verify_password(current_password, stored_password):
                    raise HTTPException(status_code=400, detail="当前密码错误")
                    
                # 更新新密码
                hashed_password = get_password_hash(new_password)
                updates.append("password = %s")
                values.append(hashed_password)
            
            if updates:
                # 执行更新
                values.append(current_user["id"])
                cursor.execute(f"""
                    UPDATE users 
                    SET {", ".join(updates)}
                    WHERE id = %s
                """, values)
                conn.commit()
            
            # 返回更新后的用户信息
            cursor.execute("""
                SELECT id, username, email, role 
                FROM users 
                WHERE id = %s
            """, (current_user["id"],))
            return cursor.fetchone()
            
        finally:
            cursor.close()
            conn.close()
            
    except HTTPException:
        raise
    except Exception as e:
        system_logger.error(f"更新用户资料失败: {str(e)}", "user", {
            'user_id': current_user["id"]
        })
        raise HTTPException(status_code=500, detail="更新用户资料失败")

# 知识库相关路由
@app.get("/api/knowledge")
async def get_knowledge_list(
    category: Optional[str] = None,
    severity: Optional[str] = None,
    current_user: Dict = Depends(get_current_user)
):
    """获取知识库列表"""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM knowledge_base WHERE status = 'active'"
            params = []
            
            if category:
                query += " AND category = %s"
                params.append(category)
            
            if severity:
                query += " AND severity = %s"
                params.append(severity)
                
            cursor.execute(query, params)
            return cursor.fetchall()
            
        finally:
            cursor.close()
            conn.close()
            
    except Exception as e:
        system_logger.error(f"获取知识库列表失败: {str(e)}", "knowledge")
        raise HTTPException(status_code=500, detail="获取知识库列表失败")

@app.get("/api/knowledge/{knowledge_id}")
async def get_knowledge_detail(
    knowledge_id: int,
    current_user: Dict = Depends(get_current_user)
):
    """获取知识点详情"""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT * FROM knowledge_base 
                WHERE id = %s AND status = 'active'
            """, (knowledge_id,))
            knowledge = cursor.fetchone()
            
            if not knowledge:
                raise HTTPException(status_code=404, detail="知识点不存在")
                
            return knowledge
            
        finally:
            cursor.close()
            conn.close()
            
    except HTTPException:
        raise
    except Exception as e:
        system_logger.error(f"获取知识点详情失败: {str(e)}", "knowledge", {
            'knowledge_id': knowledge_id
        })
        raise HTTPException(status_code=500, detail="获取知识点详情失败")

# 学习进度追踪路由
@app.post("/api/learning/progress")
async def update_learning_progress(
    course_id: int = Body(...),
    score: float = Body(...),
    current_user: Dict = Depends(get_current_user)
):
    """更新学习进度"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        try:
            # 检查课程是否存在
            cursor.execute("SELECT id FROM courses WHERE id = %s", (course_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="课程不存在")
                
            # 更新或插入学习记录
            cursor.execute("""
                INSERT INTO learning_history (user_id, course_id, score)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE score = %s
            """, (current_user["id"], course_id, score, score))
            conn.commit()
            
            return {"message": "学习进度更新成功"}
            
        finally:
            cursor.close()
            conn.close()
            
    except HTTPException:
        raise
    except Exception as e:
        system_logger.error(f"更新学习进度失败: {str(e)}", "learning", {
            'user_id': current_user["id"],
            'course_id': course_id
        })
        raise HTTPException(status_code=500, detail="更新学习进度失败")

@app.get("/api/learning/progress")
async def get_learning_progress(
    current_user: Dict = Depends(get_current_user)
):
    """获取学习进度"""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT 
                    c.id as course_id,
                    c.title as course_title,
                    c.category,
                    c.difficulty_level,
                    h.score,
                    h.completed_at
                FROM courses c
                LEFT JOIN learning_history h ON c.id = h.course_id AND h.user_id = %s
                WHERE c.status = 'published'
                ORDER BY c.category, c.difficulty_level
            """, (current_user["id"],))
            
            return cursor.fetchall()
            
        finally:
            cursor.close()
            conn.close()
            
    except Exception as e:
        system_logger.error(f"获取学习进度失败: {str(e)}", "learning", {
            'user_id': current_user["id"]
        })
        raise HTTPException(status_code=500, detail="获取学习进度失败")

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=DEBUG,
        workers=4
    ) 