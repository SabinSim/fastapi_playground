from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from services import CommuteService

app = FastAPI(title="Swiss Commute Score Calculator 🚄")

# Specify the HTML templates directory
templates = Jinja2Templates(directory="templates")

# 1. [GET] Display the initial form
@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("commute.html", {"request": request, "result": None})

# 2. [POST] Process the calculation request
@app.post("/calculate_ui", response_class=HTMLResponse)
async def calculate_ui(
    request: Request,
    home: str = Form(..., description="Departure Station"),
    work: str = Form(..., description="Destination Station")
):
    
    print(f"📥 User Input Chec -> From: {home}, To: {work}")

    data = await CommuteService.get_commute_data(home, work)
    
    context = {
        "request": request,
        "home_input": home,  
        "work_input": work,  
    }

    if not data:
        context["error"] = f"❌ Cannot find a route from '{home}' to '{work}'. Please check the station names."
        return templates.TemplateResponse("commute.html", context)

    
    minutes = data["duration_min"]
    grade, msg = CommuteService.calculate_score(minutes)

    
    result = {
        "from": data["from"],
        "to": data["to"],
        "duration_min": minutes,
        "transfers": data["transfers"],
        "score": grade,
        "message": msg
    }

    
    context["result"] = result
    
    return templates.TemplateResponse("commute.html", context)
    
    # Calculate score
    minutes = data["duration_min"]
    grade, msg = CommuteService.calculate_score(minutes)

    
    # Construct result data to pass to the template
    result = {
        "from": data["from"],
        "to": data["to"],
        "duration_min": minutes,
        "transfers": data["transfers"],
        "score": grade,
        "message": msg
    }

    
    # Re-render HTML including the result
    return templates.TemplateResponse("commute.html", {
        "request": request, 
        "result": result
    })
