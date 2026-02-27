from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    skills = Column(Text, nullable=True)
    education = Column(Text, nullable=True)

    resumes = relationship("GeneratedResume", back_populates="student")
class GeneratedResume(Base):
    __tablename__ = "generated_resumes"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    job_title = Column(String(150), nullable=False)
    resume_text = Column(Text, nullable=False)

    student = relationship("Student", back_populates="resumes")
