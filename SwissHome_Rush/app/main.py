import time
import random
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
import app.models as models
from app.sbb import SBBAgent

# [KOR] DB 테이블 생성 (없으면 자동 생성)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SwissHome Rush")
templates = Jinja2Templates(directory="app/templates")

def initialize_data(db: Session):
    """
    [KOR] DB가 비어있으면 초기 샘플 데이터를 생성하는 함수
    """
    if db.query(models.Property).count() == 0:
        sample_properties = [
            models.Property(
                name="Zurich Lakeview Penthouse",
                description="Luxury apartment with a stunning view of Lake Zurich. 10 mins to HB.",
                price=4500.0,
                image_url="https://images.unsplash.com/photo-1512917774080-9991f1c4c750",
                max_slots=5,
                commute_time=15
            ),
            models.Property(
                name="Bern Old Town Classic",
                description="Historic apartment near Zytglogge.",
                price=2800.0,
                image_url="https://images.unsplash.com/photo-1502672260266-1c1ef2d93688",
                max_slots=5,
                commute_time=60
            ),
            models.Property(
                name="Geneva Modern Studio",
                description="Close to UN headquarters.",
                price=3200.0,
                image_url="https://images.unsplash.com/photo-1522708323590-d24dbb6b0267",
                max_slots=5,
                commute_time=170
            )
        ]
        db.add_all(sample_properties)
        db.commit()
        print("✅ Sample Data Created!")

@app.get("/")
def read_root(request: Request, db: Session = Depends(get_db)):
    initialize_data(db)
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "project_name": "SwissHome Rush", 
        "status": "Phase 5 - Visualized 📊", 
        "location": "Cazis"
    })

@app.get("/properties")
def show_properties(request: Request, db: Session = Depends(get_db)):
    # 1. 데이터 확인
    initialize_data(db)
    
    # 2. 모든 집 목록 가져오기
    properties = db.query(models.Property).all()
    
    # 3. [NEW] 각 집마다 현재 예약된 인원 수 계산해서 붙여주기
    for p in properties:
        current_count = db.query(models.Booking).filter(models.Booking.property_id == p.id).count()
        p.current_count = current_count  # 화면에 보여주기 위해 임시로 숫자를 붙임
        
    return templates.TemplateResponse("booking.html", {"request": request, "properties": properties})

@app.post("/book/{property_id}")
def book_viewing(property_id: int, db: Session = Depends(get_db)):
    """
    [Flow] 동시성 제어가 적용된 예약 로직
    """
    try:
        # 1. Lock (줄 세우기)
        target_property = db.query(models.Property)\
                            .filter(models.Property.id == property_id)\
                            .with_for_update()\
                            .first()
        
        if not target_property:
            raise HTTPException(status_code=404, detail="House not found")

        # 2. Count (인원 확인)
        current_bookings = db.query(models.Booking)\
                             .filter(models.Booking.property_id == property_id)\
                             .count()
        
        # 3. Delay (경쟁 상황 시뮬레이션)
        time.sleep(0.1)

        # 4. Decide (판정)
        if current_bookings < target_property.max_slots:
            new_booking = models.Booking(
                property_id=property_id, 
                user_name=f"User-{random.randint(1000,9999)}"
            )
            db.add(new_booking)
            db.commit()
            print(f"✅ Booking Success! ({current_bookings + 1}/5)")
        else:
            db.rollback()
            print(f"❌ Sold Out! (5/5)")
            
    except Exception as e:
        db.rollback()
        print(f"🔥 Error: {e}")

    return RedirectResponse(url="/properties", status_code=303)