# Swiss Rent Affordability Analyzer 🇨🇭

A FastAPI web application designed to help users determine the affordability of housing in Switzerland. It calculates the estimated monthly net income based on the annual gross salary and checks if a proposed monthly rent adheres to the standard Swiss **'1/3 Affordability Rule'** (rent should not exceed one-third of net income).

This calculator uses **estimated canton-specific deduction rates** to provide a more realistic net income figure than simply deducting social security.

## 📁 Project Structure

This project is structured for a clean FastAPI application setup:

```

.
├── schemas/
│   └── rent.py           \# Pydantic schemas for input/output data (SalaryInfo, AffordabilityResult)
├── services/
│   └── rent\_service.py   \# Core calculation logic using canton-specific deduction rates
├── templates/
│   └── index.html        \# Jinja2 template for the web UI
├── main.py               \# FastAPI application entry point and routing
├── requirements.txt      \# List of Python dependencies
└── .gitignore            \# Files/folders to ignore in Git

````

## 🚀 Installation and Run

### Prerequisites

You need **Python 3.8+** installed on your system.

### 1. Clone the repository

If you are cloning the entire `fastapi_playground` repository:

```bash
git clone [YOUR_GITHUB_REPO_URL]
cd fastapi_playground/Rent_Affordability_Calculator
````

### 2\. Set up the environment (Recommended)

Create and activate a virtual environment to manage dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3\. Install dependencies

Install all required Python packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4\. Run the application

Start the server using Uvicorn:

```bash
uvicorn main:app --reload
```


## ⚙️ Core Logic: Canton Deduction Rates

The service uses the following rough estimates for **total monthly deductions (Social Security + Estimated Income Tax)** when calculating the Net Income for the affordability check.

| Canton | Abbreviation | Estimated Total Monthly Deduction Rate |
| :--- | :--- | :--- |
| **Zürich** | ZH | 18% |
| **Bern** | BE | 22% |
| **Geneva** | GE | 25% |
| **Graubünden** | GR | 17% |

*(Disclaimer: These rates are broad approximations for a single person's income tax and social contributions, designed for educational purposes. Actual tax liability varies significantly based on municipality, age, marital status, etc.)*

## 📜 License

This project is open-source and available under the MIT License.

