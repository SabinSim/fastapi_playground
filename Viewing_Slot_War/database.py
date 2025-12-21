from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# -------------------------------------------------------------------
# [KOR] PostgreSQL 데이터베이스 연결 주소
# [ENG] PostgreSQL database connection URL
# -------------------------------------------------------------------
# Docker Container: localhost:5433 -> 5432 (Internal)
SQLALCHEMY_DATABASE_URL = "postgresql://bini:password@localhost:5433/viewing_db"

# -------------------------------------------------------------------
# [KOR] 데이터베이스 엔진 생성 (동기 모드)
# [ENG] Create Database Engine (Synchronous Mode)
# -------------------------------------------------------------------
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# -------------------------------------------------------------------
# [KOR] 세션 팩토리 생성 (DB 연결을 위한 인스턴스 생성기)
# [ENG] Create Session Factory (Generator for DB connection instances)
# -------------------------------------------------------------------
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# -------------------------------------------------------------------
# [KOR] 모든 모델(테이블)이 상속받을 기본 클래스
# [ENG] Base class for all models (tables) to inherit from
# -------------------------------------------------------------------
Base = declarative_base()