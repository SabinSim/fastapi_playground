# 🎫 Ticketing War Simulator: Concurrency Control

> **A backend simulation project exploring Race Conditions and Database Locking.**

## 📝 Preface: The "K-Pop Ticketing" Phenomenon

In Korea, securing tickets for popular K-Pop concerts is notoriously difficult. I've heard countless stories from friends who wait anxiously for the ticketing window to open, clicking furiously the moment it goes live, only to often face the disappointment of a "Sold Out" screen.

As a developer, this phenomenon sparked a deep curiosity: **How does a system fairly select a handful of winners among tens or hundreds of thousands of concurrent requests in a split second?**

I created this project to simulate that very battlefield. My goal was to move beyond simple logic and understand how to engineer a system that remains accurate and robust under the pressure of high concurrency, ensuring that "Sold Out" really means sold out—without overbooking.

---

## 📂 Project Structure

This project is organized to separate the infrastructure, data modeling, business logic, and the ticketing interface.

```text
Ticketing_War_Simulator/
├── database.py       # Infrastructure: PostgreSQL connection & Session setup
├── models.py         # Data Layer: SQLAlchemy ORM schemas
├── main.py           # Core Logic: FastAPI endpoints with Pessimistic Locking
├── attack.py         # QA Tool: Multithreaded script to simulate high concurrency
└── templates/        # Frontend: Jinja2 Templates
    └── booking.html  # -> Ticketing page (The Battlefield)

```

---

## 🚀 Project Overview

This project simulates a **high-concurrency booking system** (like a concert ticketing site or a housing viewing slot).
It demonstrates the chaos of **Race Conditions** when multiple users attack a server simultaneously and shows how to solve it using **Database Pessimistic Locking**.

### 🎯 The Scenario

* **The Supply:** Only **5 tickets** (slots) are available for a "Zurich Penthouse".
* **The Demand:** **15 users** attempt to book simultaneously within milliseconds.
* **The Goal:** Ensure exactly 5 users succeed and 10 users fail. No overbooking allowed.

---

## 🛠 Tech Stack

* **Language:** Python 3.13
* **Framework:** FastAPI (Synchronous Mode)
* **Frontend:** Jinja2 Templates
* **Database:** PostgreSQL (Dockerized)
* **ORM:** SQLAlchemy
* **Key Concept:** ACID Transactions, Pessimistic Locking (`SELECT ... FOR UPDATE`)

---

## 📉 The Journey: From Failure to Success

This project evolved through several stages of architectural decisions to handle concurrency correctly.

| Stage | Method | Result | Analysis |
| --- | --- | --- | --- |
| **Phase 1** | Simple Logic (`if count < max`) | ❌ **FAILED** | **Overbooking occurred.** Due to the "Check-Then-Act" race condition, everyone saw "0 seats booked" and entered simultaneously. |
| **Phase 2** | SQLite + DB Lock | ❌ **FAILED** | **System Froze (Deadlock).** SQLite locks the entire file, causing read/write conflicts that halted the server. |
| **Phase 3** | PostgreSQL + Async | ❌ **FAILED** | **Blocking Issue.** The synchronous DB driver blocked the Python main thread, preventing the lock from being released. |
| **Phase 4** | **PostgreSQL + Sync + Row Lock** | ✅ **SUCCESS** | **Perfect Defense.** Using `FOR UPDATE` with a synchronous worker model properly serialized the requests. |

---

## 💻 Key Code Implementation

The heart of this defense system is the **Pessimistic Lock** implemented in `main.py`.

```python
# Synchronous handling with Pessimistic Locking
@app.post("/booking/reserve")
def reserve_slot(db: Session = Depends(get_db)):
    
    # [CRITICAL] Acquire a Row-Level Lock
    # This prevents other transactions from reading or writing 
    # to this specific row until the current transaction is committed.
    prop = db.query(models.Property)\
             .filter(models.Property.id == 1)\
             .with_for_update()\
             .first()
             
    # Safe Zone: Now we can trust the data
    current_count = db.query(models.Booking).count()
    
    if current_count < prop.max_slots:
        # Simulate processing time (0.1s delay)
        time.sleep(0.1) 
        
        # Proceed with booking...
        db.commit() # Lock is released here
        return {"status": "Success"}

```

---

## ⚡ How to Run

### 1. Prerequisites

* Docker (for PostgreSQL)
* Python 3.x

### 2. Infrastructure Setup

Run PostgreSQL using Docker (Port 5433 to avoid conflicts).

```bash
docker run --name viewing-war-db \
  -e POSTGRES_USER=bini \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=viewing_db \
  -p 5433:5432 \
  -d postgres

```

### 3. Install Dependencies

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary requests jinja2

```

### 4. Run the Server

Start the FastAPI server. It will automatically create the database tables.

```bash
uvicorn main:app --reload

```

### 5. Initialize & Attack

Open a new terminal to simulate the "Ticketing War".

**Step A: Reset the Battlefield**
Initialize the database (Max slots: 5).

```bash
# Using curl (or simply visit the URL in browser)
curl -X GET http://127.0.0.1:8000/booking/reset

```

**Step B: Launch the Attack**
Run the script to simulate 15 concurrent users.

```bash
python attack.py

```

### 6. Verify Results

Check the status dashboard JSON to see if the system survived.
Open in browser: `http://127.0.0.1:8000/booking/status`

**Expected Output:**

```json
{
  "max_slots": 5,
  "current_bookings": 5,
  "is_overbooked": false,
  "survivors": ["User-...", "User-...", "User-...", "User-...", "User-..."]
}

```

---

## 📚 Lessons Learned

* **Concurrency is tricky:** Code that works for one user often breaks for two.
* **The Database is the ultimate source of truth:** Handling logic solely in the application layer (Python) is insufficient for shared resources. We must leverage Database features like **Locks**.
* **Sync vs Async:** When dealing with strict transactional integrity and blocking I/O (like DB locks), a synchronous model with threading can sometimes be simpler and safer than `async/await` if the drivers are not fully non-blocking.
