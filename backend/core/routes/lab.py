from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..models.lab import Lab, LabInstance, LabReport, LabProgress
from ..models.user import User
from ..utils.auth import get_current_user
from ..utils.docker import create_lab_container, stop_lab_container
from ..database import get_db

router = APIRouter(prefix="/api/labs", tags=["labs"])

@router.get("/", response_model=List[Lab])
def get_labs(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取实验列表"""
    query = db.query(Lab)
    
    if category:
        query = query.filter(Lab.category == category)
    if difficulty:
        query = query.filter(Lab.difficulty == difficulty)
    if search:
        query = query.filter(
            or_(
                Lab.name.ilike(f"%{search}%"),
                Lab.description.ilike(f"%{search}%")
            )
        )
    
    labs = query.offset(skip).limit(limit).all()
    return labs

@router.get("/{lab_id}", response_model=Lab)
def get_lab(
    lab_id: int,
    db: Session = Depends(get_db)
):
    """获取实验详情"""
    lab = db.query(Lab).filter(Lab.id == lab_id).first()
    if not lab:
        raise HTTPException(status_code=404, detail="实验不存在")
    return lab

@router.post("/{lab_id}/start")
def start_lab(
    lab_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """启动实验环境"""
    # 检查实验是否存在
    lab = db.query(Lab).filter(Lab.id == lab_id).first()
    if not lab:
        raise HTTPException(status_code=404, detail="实验不存在")
    
    # 检查是否已有运行中的实验
    running_lab = db.query(LabInstance).filter(
        LabInstance.user_id == current_user.id,
        LabInstance.status == "running"
    ).first()
    
    if running_lab:
        raise HTTPException(status_code=400, detail="已有运行中的实验")
    
    # 创建实验容器
    try:
        container_id = create_lab_container(lab.docker_image)
        
        # 记录实验实例
        instance = LabInstance(
            user_id=current_user.id,
            lab_id=lab_id,
            container_id=container_id,
            status="running",
            start_time=datetime.utcnow()
        )
        db.add(instance)
        db.commit()
        
        return {
            "message": "实验环境启动成功",
            "container_id": container_id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{lab_id}/stop")
def stop_lab(
    lab_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """停止实验环境"""
    # 获取运行中的实验实例
    instance = db.query(LabInstance).filter(
        LabInstance.user_id == current_user.id,
        LabInstance.lab_id == lab_id,
        LabInstance.status == "running"
    ).first()
    
    if not instance:
        raise HTTPException(status_code=404, detail="没有运行中的实验")
    
    # 停止容器
    try:
        stop_lab_container(instance.container_id)
        
        # 更新实例状态
        instance.status = "stopped"
        instance.end_time = datetime.utcnow()
        db.commit()
        
        return {"message": "实验环境已停止"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{lab_id}/report")
def submit_lab_report(
    lab_id: int,
    report: LabReport,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """提交实验报告"""
    # 检查实验是否存在
    lab = db.query(Lab).filter(Lab.id == lab_id).first()
    if not lab:
        raise HTTPException(status_code=404, detail="实验不存在")
    
    # 创建实验报告
    report_obj = LabReport(
        user_id=current_user.id,
        lab_id=lab_id,
        content=report.content,
        findings=report.findings,
        conclusion=report.conclusion,
        attachments=report.attachments,
        submitted_at=datetime.utcnow()
    )
    db.add(report_obj)
    
    # 更新实验进度
    progress = db.query(LabProgress).filter(
        LabProgress.user_id == current_user.id,
        LabProgress.lab_id == lab_id
    ).first()
    
    if not progress:
        progress = LabProgress(
            user_id=current_user.id,
            lab_id=lab_id,
            status="completed",
            completed_at=datetime.utcnow()
        )
        db.add(progress)
    else:
        progress.status = "completed"
        progress.completed_at = datetime.utcnow()
    
    try:
        db.commit()
        return {"message": "实验报告提交成功"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{lab_id}/progress", response_model=LabProgress)
def get_lab_progress(
    lab_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取实验进度"""
    # 检查实验是否存在
    lab = db.query(Lab).filter(Lab.id == lab_id).first()
    if not lab:
        raise HTTPException(status_code=404, detail="实验不存在")
    
    # 获取进度记录
    progress = db.query(LabProgress).filter(
        LabProgress.user_id == current_user.id,
        LabProgress.lab_id == lab_id
    ).first()
    
    if not progress:
        progress = LabProgress(
            user_id=current_user.id,
            lab_id=lab_id,
            status="not_started"
        )
    
    return progress 