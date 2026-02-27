from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import SessionLocal
from app import models
class ResumeRequest(BaseModel):
    name: str
    email: str
    skills: str | None = None
    education: str | None = None
    job_title: str
    job_description: str | None = None
class ResumeResponse(BaseModel):
    id: int
    resume_text: str

    class Config:
        orm_mode = True
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
router = APIRouter(
    prefix="/resumes",
    tags=["resumes"],
)
@router.post("/generate", response_model=ResumeResponse)
def generate_resume(payload: ResumeRequest, db: Session = Depends(get_db)):
    # TODO: call your AI model here to generate text
    generated_text = f"Auto resume for {payload.name} applying as {payload.job_title}."

    # upsert student
    student = db.query(models.Student).filter_by(email=payload.email).first()
    if not student:
        student = models.Student(
            name=payload.name,
            email=payload.email,
            skills=payload.skills,
            education=payload.education,
        )
        db.add(student)
        db.flush()

    resume = models.GeneratedResume(
        student_id=student.id,
        job_title=payload.job_title,
        resume_text=generated_text,
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)

    return ResumeResponse(id=resume.id, resume_text=resume.resume_text)
