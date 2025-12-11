from schemas.rent import SalaryInfo, AffordabilityResult

class RentService:
    # Estimated Total Deduction Rates (Social Security + Approx. Tax)
    # Note: These are rough estimates for a single person. 
    # Real taxes vary by municipality (Gemeinde), age, and marital status.
    CANTON_DEDUCTION_RATES = {
        "ZH": 0.18,  # Zürich (Moderate)
        "BE": 0.22,  # Bern (High tax region)
        "GE": 0.25,  # Geneva (High tax region)
        "GR": 0.17,  # Graubünden (Generally lower tax) - ADDED
    }
    
    # Default rate if canton is not found
    DEFAULT_RATE = 0.18 

    @staticmethod
    def calculate_affordability(data: SalaryInfo) -> AffordabilityResult:
        """
        Calculates affordability using canton-specific deduction estimates.
        """
        # 1. Convert Annual to Monthly Gross
        monthly_gross = data.gross_annual_salary / 12
        
        # 2. Find the deduction rate for the selected Canton
        # If the canton is not in our list, use the default rate.
        rate = RentService.CANTON_DEDUCTION_RATES.get(data.canton, RentService.DEFAULT_RATE)
        
        # 3. Calculate Deduction & Net Income
        deduction = monthly_gross * rate
        monthly_net = monthly_gross - deduction
        
        # 4. Apply the '1/3 Rent Rule'
        rent_limit = monthly_net / 3
        is_affordable = data.monthly_rent <= rent_limit
        
        # 5. Generate Message
        if is_affordable:
            msg = f"✅ Safe in {data.canton}! (Est. Net Income: {monthly_net:,.0f} CHF)"
        else:
            msg = f"⚠️ Risk in {data.canton}! Rent exceeds 1/3 of your estimated net income."
            
        return AffordabilityResult(
            monthly_gross_income=round(monthly_gross, 2), # 👈 NEW: 여기에 값 추가
            monthly_net_income=round(monthly_net, 2),
            social_security_deduction=round(deduction, 2),
            is_affordable=is_affordable,
            message=msg
        )