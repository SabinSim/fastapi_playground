from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# ---------------------------------------------------------
# 1. Database Setup / 데이터베이스 설정
# ---------------------------------------------------------
DATABASE_URL = "sqlite:///./todos.db"

# Create Database Engine / DB 엔진 생성
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create Session / 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base Model Class / 기본 모델 클래스
Base = declarative_base()

# Define Task Table / Task 테이블 정의
class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    task = Column(String, index=True)
    is_completed = Column(Boolean, default=False)

# Create Tables / 테이블 생성
Base.metadata.create_all(bind=engine)

# ---------------------------------------------------------
# 2. App & CORS Configuration / 앱 및 CORS 설정
# ---------------------------------------------------------
app = FastAPI()

# Allow CORS for all domains / 모든 도메인에 대해 CORS 허용  middleware(경비원)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # Allow all origins / 모든 주소 허용(누구든지 와라)
    allow_credentials=True,
    allow_methods=["*"],    # Allow all methods / 모든 HTTP 메서드 허용  (CUSD 모든 종류가능)
    allow_headers=["*"],    # Allow all headers / 모든 헤더 허용
)

# Dependency to get DB session / DB 세션을 가져오는 의존성 함수
def get_db():   # 공구빌려줘
    db = SessionLocal()
    try:    # 모슨일이 있어도 작업 끝나면 닫아라
        yield db   
    finally:   
        db.close()

# ---------------------------------------------------------
# 3. API Routes / API 라우트
# ---------------------------------------------------------

# Read (Get) / 조회
@app.get("/checklist")
def get_checklist(db: Session = Depends(get_db)):
    return db.query(TaskDB).all()

# Create (Post) / 추가
@app.post("/checklist")
def add_item(item: str = Query(..., description="Task to add"), db: Session = Depends(get_db)):
    new_task = TaskDB(task=item)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"message": "Item added", "data": new_task}

# Update (Put) / 수정
@app.put("/checklist/{task_id}")
def update_item(task_id: int, item: str = Query(..., description="New content"), db: Session = Depends(get_db)):
    target_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    
    if target_task:
        target_task.task = item
        db.commit()
        db.refresh(target_task)
        return {"message": "Item updated", "new_item": target_task}
    
    return {"error": "Item not found"}

# Delete (Delete) / 삭제
@app.delete("/checklist/{task_id}")
def delete_item(task_id: int, db: Session = Depends(get_db)):
    target_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    
    if target_task:
        db.delete(target_task)
        db.commit()
        return {"message": "Item deleted"}
    
    return {"error": "Item not found"}