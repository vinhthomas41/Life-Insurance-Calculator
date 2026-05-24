# Universal Life Insurance Premium Calculator

A Shiny for Python web app that calculates minimum monthly premiums and projects account values for Universal Life insurance policies.

---

## Setup

### 1. Clone the repository
```
git clone https://github.com/yourusername/ul-calculator.git
cd ul-calculator
```

### 2. Create a virtual environment
```
python -m venv venv
```

### 3. Activate the virtual environment

**Windows:**
```
venv\Scripts\activate
```

**Mac/Linux:**
```
source venv/bin/activate
```

You'll know it's active when you see `(venv)` at the start of your terminal line.

### 4. Install dependencies
```
pip install shiny shinyswatch pandas numpy scipy matplotlib
```

### 5. Run the app
```
shiny run app.py
```

Then open your browser and go to `http://127.0.0.1:8000`

---

## Usage

1. Enter the insured's age, gender, and smoking status
2. Enter the desired face amount (death benefit)
3. Enter a monthly premium amount to test
4. Adjust the credited interest rate
5. Click **Calculate**

The app will show:
- The minimum monthly premium needed to keep the policy alive to age 100
- Whether your entered premium is sufficient
- A month-by-month projection table of the account value
- A chart of the account value vs death benefit over time

---

## Notes
- COI rates are based on the 2001 CSO Mortality Table (Residual Standard, ANB)
- Expense load is fixed at 5% of premium
- Flat monthly policy fee is fixed at $10
- This app is for illustrative purposes only and does not constitute an insurance contract