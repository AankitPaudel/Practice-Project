# File: backend/api/routes/lectures.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db
from database.models.lecture import Lecture
from api.schemas.responses import LectureCreate, Lecture as LectureSchema
from rag.processor import RAGProcessor

router = APIRouter()
rag_processor = RAGProcessor()

@router.post("/", response_model=LectureSchema)
async def create_lecture(
    lecture: LectureCreate,
    db: Session = Depends(get_db)
):
    """Create new lecture"""
    db_lecture = Lecture(**lecture.dict())
    db.add(db_lecture)
    db.commit()
    db.refresh(db_lecture)
    
    # Process lecture for RAG
    await rag_processor.process_lecture(
        db_lecture.id,
        db_lecture.content
    )
    
    return db_lecture

@router.get("/", response_model=List[LectureSchema])
async def get_lectures(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get all lectures"""
    lectures = db.query(Lecture).offset(skip).limit(limit).all()
    return lectures

@router.get("/{lecture_id}", response_model=LectureSchema)
async def get_lecture(
    lecture_id: int,
    db: Session = Depends(get_db)
):
    """Get specific lecture"""
    lecture = db.query(Lecture).filter(Lecture.id == lecture_id).first()
    if lecture is None:
        raise HTTPException(status_code=404, detail="Lecture not found")
    return lecture