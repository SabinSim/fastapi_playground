from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from services import CommuteService

app = FastAPI(title="Swiss Commute Score Calculator 🚄")

# HTML 템플릿 폴더 지정
# Specify the HTML templates directory
templates = Jinja2Templates(directory="templates")

# 1. [GET] 초기 화면 보여주기
# 1. [GET] Display the initial form
@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("commute.html", {"request": request, "result": None})

# 2. [POST] 계산 요청 처리하기
# 2. [POST] Process the calculation request
@app.post("/calculate_ui", response_class=HTMLResponse)
async def calculate_ui(
    request: Request,
    home: str = Form(..., description="출발지"),
    work: str = Form(..., description="도착지")
):
    # [🔍 디버깅] 터미널에 입력값 출력해보기 (이게 터미널에 뜨는지 확인하세요!)
    print(f"📥 사용자 입력 확인 -> 출발: {home}, 도착: {work}")

    # 서비스 로직 호출
    data = await CommuteService.get_commute_data(home, work)
    
    # 공통으로 템플릿에 넘겨줄 데이터 (입력했던 값을 그대로 유지하기 위해)
    context = {
        "request": request,
        "home_input": home,  # 👈 사용자가 입력한 값 다시 전달
        "work_input": work,  # 👈 사용자가 입력한 값 다시 전달
    }

    if not data:
        context["error"] = f"❌ '{home}'에서 '{work}'로 가는 경로를 찾을 수 없습니다."
        return templates.TemplateResponse("commute.html", context)

    # 점수 계산
    minutes = data["duration_min"]
    grade, msg = CommuteService.calculate_score(minutes)

    # 결과 데이터 구성
    result = {
        "from": data["from"],
        "to": data["to"],
        "duration_min": minutes,
        "transfers": data["transfers"],
        "score": grade,
        "message": msg
    }

    # 결과 포함하여 컨텍스트 업데이트
    context["result"] = result
    
    return templates.TemplateResponse("commute.html", context)
    # 점수 계산
    # Calculate score
    minutes = data["duration_min"]
    grade, msg = CommuteService.calculate_score(minutes)

    # 템플릿에 전달할 결과 데이터 구성
    # Construct result data to pass to the template
    result = {
        "from": data["from"],
        "to": data["to"],
        "duration_min": minutes,
        "transfers": data["transfers"],
        "score": grade,
        "message": msg
    }

    # 결과를 포함하여 HTML 다시 렌더링
    # Re-render HTML including the result
    return templates.TemplateResponse("commute.html", {
        "request": request, 
        "result": result
    })