import shutil   
import os        
import pytesseract  
from PIL import Image   

# FastAPI 핵심 라이브러리
from fastapi import ( 
    FastAPI, UploadFile, File, Depends, 
    BackgroundTasks, Request, Form
)

from fastapi.responses import HTMLResponse, RedirectResponse 
from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db, engine, Base
import models


models.Base.metadata.create_all(bind=engine)


app = FastAPI(title="Swiss Document Vault 🏦")


templates = Jinja2Templates(directory="templates")
os.makedirs("uploads", exist_ok=True) 

app.mount("/static", StaticFiles(directory="uploads"), name="static")


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


@app.get("/", response_class=HTMLResponse)
async def read_documents(request: Request, db: Session = Depends(get_db)):
    docs = db.query(models.UserDocument).order_by(models.UserDocument.id.desc()).all()
    return templates.TemplateResponse("vault.html", {"request": request, "docs": docs})

@app.get("/documents/{doc_id}", response_class=HTMLResponse)
async def read_document_detail(request: Request, doc_id: int, db: Session = Depends(get_db)):

    doc = db.query(models.UserDocument).filter(models.UserDocument.id == doc_id).first()
    

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    

    return templates.TemplateResponse("detail.html", {"request": request, "doc": doc})

@app.post("/upload")
async def upload_document(
    request: Request,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    file_location = f"uploads/{file.filename}"
    

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        

    new_doc = models.UserDocument(
        filename=file.filename,
        filepath=file_location,
        content_type=file.content_type,
        extracted_text="Processing..." 
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)


    background_tasks.add_task(process_ocr_task, new_doc.id, file_location, db)


    docs = db.query(models.UserDocument).order_by(models.UserDocument.id.desc()).all()
    
    return RedirectResponse(url="/", status_code=303)


@app.post("/delete/{doc_id}")
async def delete_document(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(models.UserDocument).filter(models.UserDocument.id == doc_id).first()
    
    if doc:

        if os.path.exists(doc.filepath):
            os.remove(doc.filepath)
            
        db.delete(doc)
        db.commit()
        

    return RedirectResponse(url="/", status_code=303)
