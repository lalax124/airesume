from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router as resumes_router
from .database import Base, engine
from app.llm_service import generate_tailored_resume

Base.metadata.create_all(bind=engine)
app = FastAPI(title="AI Resume & Portfolio Builder")
app.include_router(resumes_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}
