from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# [DB 연결 주소]
# 'db'는 docker-compose에서 이름 정의함
# 내부에서느 IP대신 이 이름으로 서로 찾음
SQLALCHEMY_DATABASE_URL = "postgresql://admin:password@db:5432/swiss_home"

# 엔진 생성 (누가 API로 요청 할때마다 DB연결을 새로 하나씩 해주는 공장)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 세션 공장 (요청이 올때마다 연결을 생성해줌)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모든 모델(Table)의 부모 클래스 
# Table 은 데이터를 저장하는 엑셀 시트와 같음 
# Base 는 엑셀 시트를 코드로 만들기 위한 기준점
Base = declarative_base()