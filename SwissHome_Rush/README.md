
# 🏠 SwissHome Rush: Concurrency-Safe Booking System

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green?style=flat&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=flat&logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat&logo=docker)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

> **A high-concurrency property booking system simulation designed to handle "Race Conditions" in real-time ticketing scenarios.**

---

## 🇨🇭 Preface: Why did I build this?

**"Finding an apartment in Switzerland is not just difficult; it's a war."**

I currently live in Cazis, Switzerland, with my wife and son. If you've ever tried to find a home here, you know the struggle: popular viewing slots disappear within seconds of being posted. It often feels like a lottery rather than a fair process.

As a Computer Engineering student, I started wondering:
*"What happens inside the server when hundreds of people click 'Book' at the exact same second?"*

I realized that without proper engineering, systems can easily double-book or crash. I built **SwissHome Rush** not just as a portfolio project, but to simulate this high-pressure environment and engineer a robust solution that ensures fairness and data integrity using **Row-Level Locking**.

---

## 🎯 The Core Problem: Race Conditions

In a typical web application, checking for availability and making a reservation happens in two steps:
1. **Read:** Check if seats are available (`SELECT count(*) ...`).
2. **Write:** If yes, insert a new reservation (`INSERT INTO ...`).

### The Scenario
Imagine **1 viewing slot** is left, and **15 users** click "Book" at the exact same millisecond.
1. All 15 users read the database and see "1 slot available".
2. All 15 users pass the check.
3. All 15 users write to the database.
4. **Result:** The system creates 15 reservations for 1 slot. **(Overbooking Disaster 💥)**

---

## 🛡️ The Solution: Pessimistic Locking

To solve this, I implemented **Pessimistic Locking** (specifically `SELECT ... FOR UPDATE`) using SQLAlchemy and PostgreSQL.

### How it works (My Implementation)
1. **Transaction Start**: When a booking request comes in, a database transaction begins.
2. **Locking**: The system selects the target property row and **locks it**.
```python
   # app/main.py
   target_property = db.query(models.Property)
                       .filter(models.Property.id == property_id)
                       .with_for_update() # 🔒 Crucial Line!
                       .first()

```

3. **Queueing**: Any other request trying to access this property must **wait** until the lock is released.
4. **Validation & Commit**: The system checks the count, adds the booking, and commits.
5. **Release**: The lock is released, allowing the next person in line to proceed.

**Result:** Even with 15 concurrent attacks, the system guarantees that **exactly 1** user succeeds, and **14** receive a distinct "Sold Out" message.

---

## 🏗️ System Architecture & Project Structure

The project is fully containerized using Docker to ensure a consistent development environment.

```bash
SwissHome_Rush/
├── app/
│   ├── templates/
│   │   ├── index.html       # Landing Page (Project Intro & Status)
│   │   └── booking.html     # Dashboard (Visualizes real-time slots & Sold Out logic)
│   ├── main.py              # Core Logic (Booking endpoints & Locking mechanism)
│   ├── models.py            # Database Schema (Property, Booking)
│   └── database.py          # DB Connection & Session Config (QueuePool)
├── attack.py                # ⚔️ Python Script for simulating concurrent attacks
├── docker-compose.yml       # Orchestration for App and DB
├── Dockerfile               # App environment setup
└── requirements.txt         # Dependencies

```

---

## 🚀 How to Run (Step-by-Step)

### Prerequisites

* Docker & Docker Compose installed on your machine.

### 1. Clone & Build

```bash
git clone [https://github.com/YOUR_GITHUB_ID/SwissHome_Rush.git](https://github.com/YOUR_GITHUB_ID/SwissHome_Rush.git)
cd SwissHome_Rush
docker-compose up -d --build

```

### 2. Initialize Data

Open your browser and visit the following URL to generate sample property data:

* URL: `http://127.0.0.1:8000/properties`
* *You should see 3 properties listed (Zurich, Bern, Geneva).*

### 3. Simulate the "Rush" (Attack Test)

I have included a script to simulate 15 concurrent users trying to book the "Zurich Penthouse" (which has only 5 slots).

Open your terminal and run:

```bash
# This script launches 15 threads simultaneously
python attack.py

```

### 4. Verify the Victory

Check the logs or database to see the result. You will see **exactly 5 successes** and **10 failures**.

```bash
# Check directly inside the Database container
docker-compose exec db psql -U admin -d swiss_home -c "SELECT count(*) FROM bookings;"

```

* **Expected Output:** `5`

---

## 📸 Visuals

### Dashboard

*The dashboard shows real-time availability. When a property is full, the system automatically disables the booking button and greys out the card (logic handled in `booking.html`).*

*(Placeholder: You can add a screenshot of your running app here)*

---

## 👨‍💻 Tech Stack Details

| Category | Technology | Reason for Choice |
| --- | --- | --- |
| **Language** | Python 3.11 | Clean syntax and rich ecosystem. |
| **Framework** | FastAPI | High performance, easy async support. |
| **Database** | PostgreSQL | Reliability and support for Row-Level Locking. |
| **DevOps** | Docker | "Infrastructure as Code" & easy deployment. |
| **Testing** | Threading (Python) | To simulate real-world concurrency scenarios. |

