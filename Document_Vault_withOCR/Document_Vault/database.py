from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. DB 연결 주소 (Docker 냉장고 주소)
# Role: 파이썬이 접속할 데이터베이스의 위치와 암호를 정의합니다.
SQLALCHEMY_DATABASE_URL = "postgresql://admin:password123@localhost:5432/swiss_home"

# 2. 엔진 생성
# Role: 실제 통신을 담당하는 엔진을 켭니다.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 3. 세션 공장 생성
# Role: 요청이 올 때마다 DB 연결을 하나씩 찍어낼 공장을 만듭니다.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. 모델의 조상님 생성
# Role: 앞으로 만들 모든 테이블(장부)의 기준이 되는 클래스입니다.
Base = declarative_base()

# 5. DB 세션 주입 함수 (Dependency)
# Role: 잠시 연결을 빌려주고, 볼일이 끝나면 반드시 닫아주는 역할을 합니다.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()