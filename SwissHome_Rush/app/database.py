from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# [ENG] Database URL
# [KOR] 데이터베이스 연결 주소
SQLALCHEMY_DATABASE_URL = "postgresql://admin:password@db:5432/swiss_home"

# [ENG] Create Database Engine with increased pool size for the "War"
# [KOR] 전쟁(동시 접속)을 대비해 커넥션 풀 크기를 20으로 늘립니다.
# (기본값은 5라서, 15명이 동시에 오면 에러가 납니다)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=20,      # [NEW] 한 번에 20명까지 입장 가능
    max_overflow=0,    # [NEW] 추가 예비 인원은 두지 않음
    pool_timeout=30    # [NEW] 자리가 없으면 30초까지 대기
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()