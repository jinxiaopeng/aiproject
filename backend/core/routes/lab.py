from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from typing import List, Optional
from datetime import datetime
from ..models.lab import Lab, LabCreate, LabUpdate, LabReport, LabProgress
from ..models.user import User
from ..utils.auth import get_current_user
from ..utils.docker import create_lab_container, stop_lab_container
from ..database import get_db

router = APIRouter(prefix="/api/labs", tags=["labs"])

@router.get("/", response_model=List[Lab])
async def get_labs(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    search: Optional[str] = None,
    db = Depends(get_db)
):
    """获取实验列表"""
    query = {}
    if category:
        query["category"] = category
    if difficulty:
        query["difficulty"] = difficulty
    if search:
        query["$or"] = [
            {"title": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}}
        ]
    
    labs = await db.labs.find(query).skip(skip).limit(limit).to_list(limit)
    return labs

@router.get("/{lab_id}", response_model=Lab)
async def get_lab(
    lab_id: str,
    db = Depends(get_db)
):
    """获取实验详情"""
    lab = await db.labs.find_one({"_id": lab_id})
    if not lab:
        raise HTTPException(status_code=404, detail="实验不存在")
    return lab

@router.post("/{lab_id}/start")
async def start_lab(
    lab_id: str,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """启动实验环境"""
    # 检查实验是否存在
    lab = await db.labs.find_one({"_id": lab_id})
    if not lab:
        raise HTTPException(status_code=404, detail="实验不存在")
    
    # 检查是否已有运行中的实验
    running_lab = await db.lab_instances.find_one({
        "user_id": current_user["id"],
        "status": "running"
    })
    if running_lab:
        raise HTTPException(status_code=400, detail="已有运行中的实验")
    
    # 创建实验容器
    try:
        container_id = await create_lab_container(lab["docker_image"])
        
        # 记录实验实例
        instance = {
            "user_id": current_user["id"],
            "lab_id": lab_id,
            "container_id": container_id,
            "started_at": datetime.utcnow(),
            "status": "running"
        }
        await db.lab_instances.insert_one(instance)
        
        return {
            "message": "实验环境启动成功",
            "container_id": container_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{lab_id}/stop")
async def stop_lab(
    lab_id: str,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """停止实验环境"""
    # 获取运行中的实验实例
    instance = await db.lab_instances.find_one({
        "user_id": current_user["id"],
        "lab_id": lab_id,
        "status": "running"
    })
    if not instance:
        raise HTTPException(status_code=404, detail="没有运行中的实验")
    
    # 停止容器
    try:
        await stop_lab_container(instance["container_id"])
        
        # 更新实例状态
        await db.lab_instances.update_one(
            {"_id": instance["_id"]},
            {
                "$set": {
                    "status": "stopped",
                    "stopped_at": datetime.utcnow()
                }
            }
        )
        
        return {"message": "实验环境已停止"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{lab_id}/report")
async def submit_lab_report(
    lab_id: str,
    report: LabReport,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """提交实验报告"""
    # 检查实验是否存在
    lab = await db.labs.find_one({"_id": lab_id})
    if not lab:
        raise HTTPException(status_code=404, detail="实验不存在")
    
    # 创建实验报告
    report_doc = {
        "user_id": current_user["id"],
        "lab_id": lab_id,
        "content": report.content,
        "screenshots": report.screenshots,
        "submitted_at": datetime.utcnow(),
        "status": "submitted"
    }
    await db.lab_reports.insert_one(report_doc)
    
    # 更新实验进度
    await db.lab_progress.update_one(
        {
            "user_id": current_user["id"],
            "lab_id": lab_id
        },
        {
            "$set": {
                "status": "completed",
                "completed_at": datetime.utcnow()
            }
        },
        upsert=True
    )
    
    return {"message": "实验报告提交成功"}

@router.get("/{lab_id}/progress", response_model=LabProgress)
async def get_lab_progress(
    lab_id: str,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """获取实验进度"""
    # 检查实验是否存在
    lab = await db.labs.find_one({"_id": lab_id})
    if not lab:
        raise HTTPException(status_code=404, detail="实验不存在")
    
    # 获取进度记录
    progress = await db.lab_progress.find_one({
        "user_id": current_user["id"],
        "lab_id": lab_id
    })
    if not progress:
        progress = {
            "status": "not_started",
            "completed_steps": [],
            "started_at": None,
            "completed_at": None
        }
    
    return progress 