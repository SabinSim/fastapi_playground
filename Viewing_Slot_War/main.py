from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import time
import models
from database import engine, SessionLocal

# [KOR] 서버 시작 시 테이블 자동 생성
# [ENG] Automatically create tables on server startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# -------------------------------------------------------------------
# [KOR] DB 세션 의존성 주입
# [ENG] Database Session Dependency Injection
# -------------------------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ===================================================================
# 1. Reserve Slot (Concurrency Control Logic)
# ===================================================================
@app.post("/booking/reserve")
def reserve_slot(db: Session = Depends(get_db)):
    """
    [KOR] 동기식 처리와 비관적 락을 사용한 예약 처리
    [ENG] Reservation processing using Synchronous execution and Pessimistic Locking
    """
    
    # ---------------------------------------------------------------
    # [Step 1] Acquire Lock (방어 시작)
    # ---------------------------------------------------------------
    # [KOR] 'with_for_update()'를 사용하여 해당 행(Row)을 잠급니다.
    #       트랜잭션이 끝날 때까지 다른 요청은 대기(Wait)합니다.
    # [ENG] Locks the row using 'with_for_update()'.
    #       Other requests must wait until this transaction is finished.
    prop = db.query(models.Property)\
             .filter(models.Property.id == 1)\
             .with_for_update()\
             .first()
    
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")

    # ---------------------------------------------------------------
    # [Step 2] Check Current State (검증)
    # ---------------------------------------------------------------
    # [KOR] 락이 걸린 상태에서 안전하게 현재 예약 수를 조회합니다.
    # [ENG] Safely query the current booking count under the lock.
    current_count = db.query(models.Booking).count()
    
    # ---------------------------------------------------------------
    # [Step 3] Business Logic & Delay Simulation (실행)
    # ---------------------------------------------------------------
    if current_count < prop.max_slots:
        # [KOR] 처리 지연 시뮬레이션 (락이 유지되는 동안)
        # [ENG] Simulation of processing delay (While lock is held)
        time.sleep(0.1) 
        
        # [KOR] 예약 생성 (메모리)
        # [ENG] Create Booking Object (In Memory)
        new_booking = models.Booking(
            property_id=prop.id,
            user_name=f"User-{int(time.time()*1000)}"
        )
        
        # [Step 4] Commit (확정 및 락 해제)
        db.add(new_booking)
        db.commit() # [KOR] 커밋 시점에 락이 해제됩니다. [ENG] Lock is released upon commit.
        db.refresh(new_booking)
        
        return {"status": "Success", "booking_id": new_booking.id}
    
    else:
        # [KOR] 정원 초과 시 실패 처리
        # [ENG] Reject if capacity is full
        raise HTTPException(status_code=400, detail="Sold Out! Too late.")

# ===================================================================
# 2. Reset System (For Testing)
# ===================================================================
@app.get("/booking/reset")
def reset_system(db: Session = Depends(get_db)):
    # [KOR] 기존 데이터 삭제
    # [ENG] Delete existing data
    db.query(models.Booking).delete()
    
    # [KOR] 매물 상태 초기화 (정원 5명)
    # [ENG] Reset property status (Capacity: 5)
    prop = db.query(models.Property).filter(models.Property.id == 1).first()
    if not prop:
        prop = models.Property(id=1, name="Zurich Penthouse", max_slots=5)
        db.add(prop)
    else:
        prop.max_slots = 5
    
    db.commit()
    return {"message": "System Reset Complete. Max Slots: 5"}

# ===================================================================
# 3. Status Dashboard (Monitoring)
# ===================================================================
@app.get("/booking/status")
def check_status(db: Session = Depends(get_db)):
    prop = db.query(models.Property).filter(models.Property.id == 1).first()
    bookings = db.query(models.Booking).all()
    
    return {
        "max_slots": prop.max_slots,
        "current_bookings": len(bookings),
        "is_overbooked": len(bookings) > prop.max_slots,
        "survivors": [b.user_name for b in bookings]
    }