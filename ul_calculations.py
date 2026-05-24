import pandas as pd
import numpy as np  
from coi_tables import get_coi_rate
from scipy.optimize import brentq

def project_account_value(age, gender, smoking_status, face_amount,
                          monthly_premium, credited_rate,
                          flat_fee, expense_load_pct):
    rows = []
    av = 0
    current_age = age
    month_count = (100 - age) * 12
    monthly_rate = (1 + credited_rate) ** (1/12) - 1
    for i in range(1, month_count + 1):
        if i % 12 == 0:
            current_age += 1
        lapsed = False
        av += monthly_premium # Add the monthly premium to account value
        av -= (monthly_premium * expense_load_pct) # Insurer takes a cut of the premium ("transcation fee")
        av -= flat_fee # Insurer charges a flat monthly fee ("account maintenance")
        coi_rate = get_coi_rate(current_age, gender, smoking_status)
        NAR = face_amount - av # How much liability is on the insurer?
        COI = (NAR / 1000) * coi_rate # Calculate COI based on NAR
        av -= COI # Deduct the cost of insurance
        av_before_interest = av
        av *= 1 + monthly_rate # Insurer pays interest on what is in your account
        if av <= 0:
            av = 0
            lapsed = True
        monthly_info = {
            "month": i,
            "year": (i-1)/12 + 1,
            "age": current_age,
            "premium": monthly_premium,
            "expense_charge": monthly_premium * expense_load_pct,
            "coi_charge": COI,
            "interest_credited": av_before_interest * monthly_rate,
            "account_value": av,
            "nar": NAR,
            "lapsed": lapsed,
        }
        rows.append(monthly_info)
        if lapsed:
            break
    return pd.DataFrame(rows)

def find_minimum_premium(age, gender, smoking_status,
                         face_amount, credited_rate, flat_fee, 
                         expense_load_pct):
    def objective(premium):
        av_df = project_account_value(age, gender, smoking_status,
                                    face_amount, premium, credited_rate,
                                    flat_fee, expense_load_pct)
        expected_months = (100 - age) * 12
        actual_months = len(av_df)
        last_lapsed = av_df["lapsed"].iloc[-1]
        if last_lapsed:
            return actual_months - expected_months  # negative
        else:
            return 1  # positive, policy survived
    return brentq(objective, 0, 10000)
    
        