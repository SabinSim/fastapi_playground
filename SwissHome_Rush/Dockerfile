# 1. 파이썬 3.11 버전의 가벼운 리눅스 이미지를 기반으로 합니다.
FROM python:3.11-slim

# 2. 컨테이너 내부의 작업 폴더를 /code로 설정합니다.
WORKDIR /code

# 3. 자재 목록을 복사하고 설치합니다.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 나머지 코드는 docker-compose가 볼륨으로 연결하므로 복사 생략 가능하지만,
#    배포를 대비해 복사해두는 것이 정석입니다.
COPY . .