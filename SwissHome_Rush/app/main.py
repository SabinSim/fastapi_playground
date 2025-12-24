from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates # UI 템플릿 엔진
from app.database import engine, Base

# 앱 시작 시 DB 테이블 생성 (models.py가 생기면서 작동됨)

app = FastAPI(title="SwissHome Rush 🏠")

# [UI 설정]
# HTML 파일들이 'app/templates' 폴더에 있다고 알려줍니다. 
# Jinja2Templates 으로 구성됨 (Jinja2Templates은 HTML에 문법 구문을 씌어줌 If를 사용가능하게 만듬)
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
def read_root(request:Request):
    """
    메인 페이지를 렌더링함 완성된 HTML화면으로 반환함
    """

    # 템플릿(index.html)에 기입할 데이터
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "project_name": "SwissHome Rush",
            "status": "Phase 1 - Infrastructure Ready 🏗️",
            "location": "Cazis, Switzerland"
        }
    )