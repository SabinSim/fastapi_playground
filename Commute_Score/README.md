
# 🚄 Swiss Commute Score Calculator

> **"Checking Google Maps manually became quite a chore as I thought about moving for work or staying in Graubünden. So, I built this project to handle those commute checks for me more efficiently."**

## 🌟 Project Overview
This is a **real-time commute analysis tool** that connects to the **Swiss Public Transport System (SBB)** via Open Data APIs. This module determines a "livability score" for potential homes based on the travel time to the workplace, helping users make data-driven relocation decisions.
> **Stage 3 of SwissHome Rush Roadmap**: External API Integration & Asynchronous Programming.

## 🎯 Features

* **Real-time Data**: Fetches live connection data from the Swiss public transport network (SBB/CFF/FFS).
* **Asynchronous Processing**: Uses `httpx` and `async/await` to handle external API requests without blocking the server.
* **Smart Scoring System**: Automatically grades locations from **A (Fantastic)** to **D (Hell)** based on commute duration.
* **Interactive UI**: A clean web interface built with **Jinja2** templates.

## 🛠️ Tech Stack

* **Framework**: FastAPI
* **HTTP Client**: `httpx` (Asynchronous)
* **Templating**: Jinja2
* **Validation**: Pydantic
* **Environment**: `python-dotenv` for managing configuration

## 📂 Project Structure

```bash
Commute_Score/
├── .env                 # Environment variables (API URL)
├── main.py              # FastAPI entry point & UI Router
├── services.py          # Business logic & Async API calls
├── schemas.py           # Pydantic data models
├── requirements.txt     # Dependencies
└── templates/
    └── commute.html     # Frontend UI

```

##🚀 Installation & Run###1. PrerequisitesEnsure you are in the `Commute_Score` directory.

### 2. Install Dependencies```bash
pip install -r requirements.txt



### 3. Configure EnvironmentCreate a `.env` file in this directory (if not exists) and add the API endpoint:

```ini
SWISS_TRANSPORT_API_URL=[http://transport.opendata.ch/v1/connections](http://transport.opendata.ch/v1/connections)

```

### 4. Run the Server
```bash
uvicorn main:app --reload
```

### 5. Usage1. Open your browser and go to `http://127.0.0.1:8000`.
2. Enter a **Home Station** (e.g., `Zurich HB`) and a **Work Station** (e.g., `Bern`).
3. Click **Check Time**.
4. View the calculated grade and detailed route info.

##🧠 Core Logic: Grading SystemThe service calculates a score based on the one-way travel time:

| Commute Time | Grade | Description |
| --- | --- | --- |
| **≤ 30 min** | **A** | 🌟 Fantastic! Quality of life improves. |
| **≤ 60 min** | **B** | ✅ Good. Standard commute distance. |
| **≤ 90 min** | **C** | ⚠️ Tired. Read a book or watch Netflix. |
| **> 90 min** | **D** | 🚨 Hell. Reconsider moving here. |

## 🔗 Learning Points (vs. C# .NET)* **Async/Await**: Similar to C#'s `async Task` pattern for non-blocking I/O operations.
* **External Service Integration**: Matches the pattern of using `HttpClient` in .NET to consume REST APIs.
* **Environment Variables**: Equivalent to managing secrets in `appsettings.json`.

---

*Part of the SwissHome Rush Project.*
