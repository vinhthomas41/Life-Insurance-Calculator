from shiny import App, ui, render, reactive
import pandas as pd
import numpy as np
from ul_calculations import project_account_value, find_minimum_premium
import matplotlib.pyplot as plt

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_numeric("age", "Age", value = 35, min = 18, max = 100), # Age
        ui.input_select("gender", "Gender", ("Male", "Female")), # Gender
        ui.input_select("smoking_status", "Do you smoke?", ("Smoker", "Non-Smoker")), # Smoking_Status
        ui.input_numeric("face_amount", "Face amount", value = 500000), # Face_amount
        ui.input_numeric("monthly_premium", "Monthly Premium", value = 500), # Monthly_premium
        ui.input_slider("credited_rate", "Credited Rate", min=0.02, max=0.08, value=0.04, step=0.001, post="%"), # credited_rate
        ui.input_action_button("calculate", "Calculate") # START IT NOW
    ),
    ui.navset_tab(
        ui.nav_panel("Summary",
            ui.output_text("min_premium"),
            ui.output_text("lapse_status")
        ),
        ui.nav_panel("Projection Table",
            ui.output_data_frame("projection_table")
        ),
        ui.nav_panel("Chart",
            ui.output_plot("av_chart")
        )
    )
)

def server(input, output, session):
    @reactive.calc
    def projection():
        av = project_account_value(input.age(), input.gender(), input.smoking_status(),
                              input.face_amount(), input.monthly_premium(), input.credited_rate(),
                              10, 0.05)
        return av
    
    @render.text
    def min_premium():
        monthly_premium = find_minimum_premium(input.age(), input.gender(), input.smoking_status(),
                              input.face_amount(), input.credited_rate(), 10, 0.05)
        return f"Minimum Monthly Premium: ${monthly_premium:,.2f}"
    
    @render.text
    def lapse_status():
        df = projection()
        lapsed = df["lapsed"].iloc[-1]
        if lapsed:
            return "Policy lapses before the age of 100 at this premium"
        else:
            return "Policy survives to the age of 100 at this premium"
        
    @render.data_frame
    def projection_table():
        df = projection().round(2)
        return render.DataGrid(df)
        
    @render.plot
    def av_chart():
        df = projection()
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(df["month"], df["account_value"], label="Account Value")
        ax.axhline(y=input.face_amount(), color="red", linestyle="--", label="Death Benefit")
        ax.set_xlabel("Month")
        ax.set_ylabel("Amount ($)")
        ax.set_title("Policy Projection")
        ax.legend()
        return fig

app = App(app_ui, server)
        
        