from typing import List, Optional
from datetime import datetime
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from .database import get_db
from .models import Note, NoteHistory
from .schemas import NoteCreate, NoteUpdate, NoteResponse
from .auth import get_current_user

class NoteService:
    def __init__(self, db: Session):
        self.db = db

    def get_note(self, user_id: int, lesson_id: int) -> Optional[Note]:
        """获取指定课时的笔记"""
        return self.db.query(Note).filter(
            Note.user_id == user_id,
            Note.lesson_id == lesson_id
        ).first()

    def get_note_history(self, note_id: int) -> List[NoteHistory]:
        """获取笔记的历史记录"""
        return self.db.query(NoteHistory).filter(
            NoteHistory.note_id == note_id
        ).order_by(desc(NoteHistory.created_at)).all()

    def create_note(self, user_id: int, note_data: NoteCreate) -> Note:
        """创建新笔记"""
        # 检查是否已存在笔记
        existing_note = self.get_note(user_id, note_data.lesson_id)
        if existing_note:
            raise HTTPException(
                status_code=400,
                detail="该课时的笔记已存在"
            )

        # 创建新笔记
        note = Note(
            user_id=user_id,
            lesson_id=note_data.lesson_id,
            content=note_data.content
        )
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        return note

    def update_note(self, user_id: int, note_id: int, note_data: NoteUpdate) -> Note:
        """更新笔记"""
        note = self.db.query(Note).filter(
            Note.id == note_id,
            Note.user_id == user_id
        ).first()

        if not note:
            raise HTTPException(
                status_code=404,
                detail="笔记不存在"
            )

        # 更新笔记内容
        note.content = note_data.content
        self.db.commit()
        self.db.refresh(note)
        return note

    def delete_note(self, user_id: int, note_id: int) -> None:
        """删除笔记"""
        note = self.db.query(Note).filter(
            Note.id == note_id,
            Note.user_id == user_id
        ).first()

        if not note:
            raise HTTPException(
                status_code=404,
                detail="笔记不存在"
            )

        self.db.delete(note)
        self.db.commit()

def get_note_service(db: Session = Depends(get_db)) -> NoteService:
    return NoteService(db) 