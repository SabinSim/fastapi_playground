# 🏠 SwissHome Rush: The All-in-One Relocation Platform

## 🇨🇭 Why I Built This

I started this project to solve real-world problems I encountered while living in Switzerland—specifically the challenges of moving and commuting via SBB. I wanted to turn these daily needs into a functional service.

This roadmap represents my growth as a developer. It serves as a comprehensive study of **FastAPI** and system design, paving the way for my future transition into **C# .NET** development.

---

**SwissHome Rush** is a comprehensive backend development roadmap designed to solve the challenges of moving to Switzerland. The project evolves from basic data management to handling high-concurrency "viewing slot wars," mirroring real-world enterprise system complexities.

This repository serves as a playground for mastering **FastAPI**, **PostgreSQL**, **Asynchronous Programming**, and **System Architecture**.

---

## 🗺️ Step-up Roadmap & Status

| Stage | Module Name | Core Concepts | Status |
| :--- | :--- | :--- | :--- |
| **1** | **The Relocation Checklist** | CRUD, Auth (JWT), SQLite | ✅ **Completed** |
| **2** | **Rent Affordability Analyzer** | Business Logic, Service Layer, Pydantic | ✅ **Completed** |
| **3** | **Commute Score (SBB)** | External API (Async/Await), Env Vars | ✅ **Completed**  |
| **4** | **Document Vault** | File Uploads, OCR, Background Tasks, Docker | ✅ **Completed**  |
| **5** | **Viewing Slot War** | Concurrency, Redis, Distributed Locking | ✅ **Completed**  |

---

## 📂 Completed Modules

### ✅ Stage 1: The Relocation Checklist
* **Goal**: "Give the server a memory."
* **Description**: A task management API to organize relocation to-dos (documents, cleaning, packing).
* **Key Tech**:
    * **JWT Authentication**: Secure signup/login (Users manage their own lists).
    * **CRUD Operations**: Create, Read, Update, Delete checklist items.
    * **Database**: SQLite (Moving to PostgreSQL in Stage 4).

### ✅ Stage 2: Rent Affordability Calculator
* **Goal**: "Implement Swiss property laws in code."
* **Description**: A logic-heavy service that calculates estimated net income and validates rent against the Swiss "1/3 Affordability Rule."
* **Key Tech**:
    * **Service Layer Pattern**: Separating business logic from API routers.
    * **Canton-Specific Logic**: Dynamic tax/deduction estimation for ZH, BE, GE, GR.
    * **Jinja2 Templating**: Server-side rendering for a quick interactive UI.

---

## 🛠️ Technology Stack

* **Language**: Python 3.9+
* **Framework**: FastAPI
* **Server**: Uvicorn (ASGI)
* **Validation**: Pydantic v2
* **Templating**: Jinja2
* **Tools**: Git, Virtualenv

---

## 🚀 How to Run

Since this is a mono-repo structure containing multiple stages, navigate to the specific folder you want to run.

### Running Stage 2 (Rent Calculator)

1.  **Navigate to the folder**:
    ```bash
    cd Rent_Affordability_Calculator
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the server**:
    ```bash
    uvicorn main:app --reload
    ```

4.  **Open in Browser**:
    Go to `http://127.0.0.1:8000` to use the calculator.

---

## 📜 License

This project is open-source and available under the MIT License.
