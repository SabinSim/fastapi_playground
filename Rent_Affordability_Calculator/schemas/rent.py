from pydantic import BaseModel, Field

# [Input] Data sent by the user
class SalaryInfo(BaseModel):
    """Schema for the input data required for the affordability check."""
    gross_annual_salary: float = Field(..., title="Annual Gross Salary", description="Pre-tax annual salary in CHF", example=85000)
    monthly_rent: float = Field(..., title="Monthly Rent", description="The desired monthly rent in CHF", example=1500)
    canton: str = Field("ZH", title="Canton", description="Region (e.g., ZH, BE, GR)", example="GR")

# [Output] Calculation result returned by the service
class AffordabilityResult(BaseModel):
    """Schema for the affordability calculation results."""
    monthly_gross_income: float = Field(..., title="Monthly Gross Income") # 👈 NEW: 월 세전 급여 추가
    monthly_net_income: float = Field(..., title="Estimated Monthly Net Income")
    social_security_deduction: float = Field(..., title="Social Security Deduction Amount")
    is_affordable: bool = Field(..., title="Affordability Status")
    message: str = Field(..., title="Guidance Message")