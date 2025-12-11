from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# Import our custom logic
from schemas.rent import SalaryInfo, AffordabilityResult
from services.rent_service import RentService

app = FastAPI(title="Swiss Rent Affordability Calculator UI")

# Specify the directory where HTML files are located
templates = Jinja2Templates(directory="templates")

# 1. Display the main screen (GET endpoint)
@app.get("/", response_class=HTMLResponse, summary="Display Rent Analyzer UI")
def read_root(request: Request):
    """
    Renders the main HTML page ('index.html').
    """
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

# 2. Handle calculation submission from the UI (POST endpoint)
@app.post("/calculate_ui", response_class=HTMLResponse, summary="Process UI form submission and calculate affordability")
def calculate_ui(
    request: Request,
    gross_annual_salary: float = Form(..., description="Annual Gross Salary in CHF"),
    monthly_rent: float = Form(..., description="Monthly Rent in CHF"),
    canton: str = Form(..., description="Canton of Residence (e.g., ZH, BE)")
):
    """
    Receives form data, calculates affordability, and re-renders the page with the results.
    """
    # 1. Create the data schema from form inputs
    input_data = SalaryInfo(
        gross_annual_salary=gross_annual_salary,
        monthly_rent=monthly_rent,
        canton=canton
    )
    
    # 2. Call the core service logic (reusable!)
    result = RentService.calculate_affordability(input_data)
    
    # 3. Re-render the HTML page including the result data
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "result": result
    })

# (Optional) API-only endpoint maintained for programmatic access
@app.post("/api/calculate", response_model=AffordabilityResult, summary="Calculate affordability via API request (JSON body)")
def calculate_api(info: SalaryInfo):
    """
    Accepts a JSON payload (SalaryInfo) and returns the affordability check result.
    """
    return RentService.calculate_affordability(info)