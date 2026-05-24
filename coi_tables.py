import pandas as pd

coi_df = pd.read_csv('./coi_rates.csv', skipinitialspace=True)
coi_df = coi_df.set_index('Age')


def get_coi_rate(age, gender, smoking_status):
    col_map = {
        ("Male", "Non-Smoker"): "Male_NS",
        ("Male", "Smoker"): "Male_S",
        ("Female", "Non-Smoker"): "Female_NS",
        ("Female", "Smoker"): "Female_S"
    }
    
    col = col_map[(gender, smoking_status)]
    annual_rate = coi_df.loc[age, col]
    monthly_rate = 1 - (1 - annual_rate) ** (1/12)
    return monthly_rate

