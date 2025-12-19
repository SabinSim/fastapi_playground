import shutil    # 파일/디렉터리 복사, 이동
import os        # 운영체제 상호작용 (폴더 생성/삭제)
import pytesseract  # OCR 엔진 (파이썬 래퍼)
from PIL import Image   # 이미지 처리 라이브러리

# FastAPI 핵심 라이브러리
from fastapi import ( 
    FastAPI, UploadFile, File, Depends, 
    BackgroundTasks, Request, Form
)
# 👇 [중요] RedirectResponse가 빠져 있어서 추가했습니다!
from fastapi.responses import HTMLResponse, RedirectResponse 
from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db, engine, Base
import models

# ===============================
# 1. DB 테이블 생성
# ===============================
models.Base.metadata.create_all(bind=engine)

# ===============================
# 2. FastAPI 앱 생성
# ===============================
app = FastAPI(title="Swiss Document Vault 🏦")

# ===============================
# 3. 템플릿 & 정적 파일 설정
# ===============================
templates = Jinja2Templates(directory="templates")
os.makedirs("uploads", exist_ok=True) # 폴더가 없으면 생성

# [중요] 이 코드가 있어야 'Not Found'가 안 뜹니다.
# 실제 uploads 폴더를 /static 주소로 연결(Mount)합니다.
app.mount("/static", StaticFiles(directory="uploads"), name="static")

# ===============================
# 4. OCR 백그라운드 작업
# ===============================
def process_ocr_task(doc_id: int, file_path: str, db: Session):
    try:
        print(f"🔄 OCR Start: {file_path}")
        image = Image.open(file_path) # 이미지 열기
        text = pytesseract.image_to_string(image) # 글자 읽기
        
        # DB 업데이트
        doc = db.query(models.UserDocument).filter(models.UserDocument.id == doc_id).first()
        if doc:
            doc.extracted_text = text
            db.commit()
            print(f"✅ OCR Finish: Document {doc_id} updated.")
    except Exception as e:
        print(f"❌ OCR Error: {e}")

# ===============================
# 5. 메인 화면 (문서 목록)
# ===============================
@app.get("/", response_class=HTMLResponse)
async def read_documents(request: Request, db: Session = Depends(get_db)):
    docs = db.query(models.UserDocument).order_by(models.UserDocument.id.desc()).all()
    return templates.TemplateResponse("vault.html", {"request": request, "docs": docs})

@app.get("/documents/{doc_id}", response_class=HTMLResponse)
async def read_document_detail(request: Request, doc_id: int, db: Session = Depends(get_db)):
    # 1. DB에서 ID로 문서 찾기
    doc = db.query(models.UserDocument).filter(models.UserDocument.id == doc_id).first()
    
    # 2. 없으면 404 에러
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # 3. 상세 페이지(detail.html)에 데이터 넣어서 보여주기
    return templates.TemplateResponse("detail.html", {"request": request, "doc": doc})
# ===============================
# 6. 파일 업로드 처리
# ===============================
@app.post("/upload")
async def upload_document(
    request: Request,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    file_location = f"uploads/{file.filename}"
    
    # 1. 실제 파일 저장
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # 2. DB 기록
    new_doc = models.UserDocument(
        filename=file.filename,
        filepath=file_location,
        content_type=file.content_type,
        extracted_text="Processing..." 
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    # 3. 백그라운드 OCR 시작
    background_tasks.add_task(process_ocr_task, new_doc.id, file_location, db)

    # 4. 목록 데이터 다시 조회 (여기가 틀렸던 부분입니다!)
    # 먼저 변수에 담고 -> 그 다음에 딕셔너리에 넣습니다.
    docs = db.query(models.UserDocument).order_by(models.UserDocument.id.desc()).all()
    
    return RedirectResponse(url="/", status_code=303)
# ===============================
# 7. 문서 삭제 기능
# ===============================
@app.post("/delete/{doc_id}")
async def delete_document(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(models.UserDocument).filter(models.UserDocument.id == doc_id).first()
    
    if doc:
        # 실제 파일도 하드디스크에서 지움 (유령 파일 방지)
        if os.path.exists(doc.filepath):
            os.remove(doc.filepath)
            
        db.delete(doc)
        db.commit()
        
    # 삭제 후 메인 화면으로 이동
    return RedirectResponse(url="/", status_code=303)