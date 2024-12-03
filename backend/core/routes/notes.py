from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..auth import get_current_user
from ..notes import NoteService, get_note_service
from ..schemas import NoteCreate, NoteUpdate, NoteResponse, User

router = APIRouter(prefix="/api/notes", tags=["notes"])

@router.get("/{lesson_id}", response_model=NoteResponse)
async def get_note(
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    note_service: NoteService = Depends(get_note_service)
):
    """获取指定课时的笔记"""
    note = note_service.get_note(current_user.id, lesson_id)
    if not note:
        raise HTTPException(
            status_code=404,
            detail="笔记不存在"
        )
    return note

@router.post("", response_model=NoteResponse)
async def create_note(
    note_data: NoteCreate,
    current_user: User = Depends(get_current_user),
    note_service: NoteService = Depends(get_note_service)
):
    """创建新笔记"""
    return note_service.create_note(current_user.id, note_data)

@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: int,
    note_data: NoteUpdate,
    current_user: User = Depends(get_current_user),
    note_service: NoteService = Depends(get_note_service)
):
    """更新笔记"""
    return note_service.update_note(current_user.id, note_id, note_data)

@router.delete("/{note_id}")
async def delete_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    note_service: NoteService = Depends(get_note_service)
):
    """删除笔记"""
    note_service.delete_note(current_user.id, note_id)
    return {"message": "笔记已删除"}

@router.get("/{note_id}/history", response_model=List[NoteResponse])
async def get_note_history(
    note_id: int,
    current_user: User = Depends(get_current_user),
    note_service: NoteService = Depends(get_note_service)
):
    """获取笔记历史记录"""
    # 验证笔记所有权
    note = note_service.get_note_by_id(note_id)
    if not note or note.user_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="笔记不存在"
        )
    return note_service.get_note_history(note_id) 