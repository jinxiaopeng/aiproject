from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from ..database import get_db
from ..auth import get_current_user
from ..models import Note, NoteHistory
from ..schemas import (
    NoteCreate,
    NoteUpdate,
    NoteResponse,
    NoteHistoryResponse,
    User
)

router = APIRouter(prefix="/api/notes", tags=["notes"])

@router.get("/{lesson_id}", response_model=NoteResponse)
async def get_note(
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取课时笔记"""
    note = (
        db.query(Note)
        .filter(
            Note.lesson_id == lesson_id,
            Note.user_id == current_user.id
        )
        .first()
    )
    
    if not note:
        raise HTTPException(status_code=404, detail="笔记不存在")
    return note

@router.post("", response_model=NoteResponse)
async def create_note(
    note_data: NoteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建笔记"""
    # 检查是否已存在笔记
    existing_note = (
        db.query(Note)
        .filter(
            Note.lesson_id == note_data.lesson_id,
            Note.user_id == current_user.id
        )
        .first()
    )
    
    if existing_note:
        raise HTTPException(status_code=400, detail="笔记已存在")
    
    note = Note(
        user_id=current_user.id,
        lesson_id=note_data.lesson_id,
        content=note_data.content
    )
    
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: int,
    note_data: NoteUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新笔记"""
    note = (
        db.query(Note)
        .filter(
            Note.id == note_id,
            Note.user_id == current_user.id
        )
        .first()
    )
    
    if not note:
        raise HTTPException(status_code=404, detail="笔记不存在")
    
    # 保存历史记录
    note_history = NoteHistory(
        note_id=note.id,
        content=note.content
    )
    db.add(note_history)
    
    # 更新笔记
    note.content = note_data.content
    db.commit()
    db.refresh(note)
    return note

@router.delete("/{note_id}")
async def delete_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除笔记"""
    note = (
        db.query(Note)
        .filter(
            Note.id == note_id,
            Note.user_id == current_user.id
        )
        .first()
    )
    
    if not note:
        raise HTTPException(status_code=404, detail="笔记不存在")
    
    db.delete(note)
    db.commit()
    return {"message": "笔记已删除"}

@router.get("/{note_id}/history", response_model=List[NoteHistoryResponse])
async def get_note_history(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取笔记历史记录"""
    # 检查笔记所有权
    note = (
        db.query(Note)
        .filter(
            Note.id == note_id,
            Note.user_id == current_user.id
        )
        .first()
    )
    
    if not note:
        raise HTTPException(status_code=404, detail="笔记不存在")
    
    history = (
        db.query(NoteHistory)
        .filter(NoteHistory.note_id == note_id)
        .order_by(NoteHistory.created_at.desc())
        .all()
    )
    
    return history 