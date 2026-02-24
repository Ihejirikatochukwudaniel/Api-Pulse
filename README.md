# ⚡ API Pulse

> **A demo-first backend system that models how APIs fail, how incidents form, and how alerts are triggered — without relying on live infrastructure.**

API Pulse is engineered to showcase real-world backend architecture, failure modeling, and engineering judgment. This isn't another CRUD demo. It's a controlled simulation of the things that actually matter in production systems.

---

## 🧭 Table of Contents

- [Why This Project Exists](#-why-this-project-exists)
- [Core Concepts](#-core-concepts)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [API Endpoints](#-api-endpoints)
- [Getting Started](#-getting-started)
- [Demo Seed Data](#-demo-seed-data)
- [Engineering Principles](#-engineering-principles)
- [Intended Audience](#-intended-audience)

---

## 💡 Why This Project Exists

Most backend demos focus on happy paths.

Real systems are evaluated on something harder:

- How failures are **detected**
- How incidents are **modeled**
- How timelines are **reconstructed**
- How alerts are **triggered and persisted**

API Pulse focuses on these problems exclusively.

Instead of hitting live URLs or running cron jobs, it simulates failures in a controlled, deterministic way — letting anyone explore incident behavior instantly, with no hosting or external dependencies required.

---

## 🔍 Core Concepts

### 🖥️ Monitors

A **Monitor** represents an API endpoint that would normally be polled in production. It defines:

- What is being monitored
- What a healthy response looks like
- How frequently checks would run

> In this demo, monitors do not perform real HTTP requests. They act as entities that can enter defined failure states.

---

### 🚨 Incidents

An **Incident** represents a failure event tied to a monitor. Each incident:

- Has a precise **start time**
- Tracks the **type of failure**
- Remains **open** until explicitly resolved
- Exposes a full **timeline view**

This avoids the common anti-pattern of using simple status flags that silently erase history.

---

### 🔔 Alerts

Alerts are **simulated but persisted**. Each alert:

- Stores a structured payload
- Includes accurate timestamps
- Behaves as if dispatched to an external notification system

Alerts are treated as **data**, not side effects.

---

## 🏗️ Architecture


![api pulse architecture](https://github.com/user-attachments/assets/fcd6ef24-28ba-417f-a7ee-2942c5ac5e79)

```
API Client
    ↓
FastAPI Routers
    ↓
Service Layer  (business logic)
    ↓
SQLite Database
    ↑
Simulation Layer  (failure & alert generation)
```

**Key principles:**

- Thin routers — routes handle only input/output
- Fat services — all business logic lives in the service layer
- Explicit domain models — no implicit state changes
- Deterministic behavior — no randomness, fully reproducible
- No hidden side effects — everything is traceable

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| API Framework | FastAPI |
| Database | SQLite |
| ORM | SQLModel / SQLAlchemy |
| Validation | Pydantic v2 |
| Authentication | JWT |
| Server | Uvicorn |

> No external services required. Runs entirely locally.

---

## 📁 Project Structure

```
app/
├── main.py              # Application entry point
├── core/                # Config, security, database setup
├── models/              # ORM models (database schema)
├── schemas/             # Request / response models (Pydantic)
├── services/            # Business logic layer
├── api/                 # Route definitions
├── demo/                # Demo seed data & simulation engine
└── tests/               # Test suite
```

> Business logic lives **exclusively** in the services layer. Routes are responsible only for input/output handling.

---

## 📡 API Endpoints

### 🔐 Authentication
- Register and login with JWT-based auth
- All protected routes require a valid token

### 🖥️ Monitors
- Create and manage monitors
- Simulate failures deterministically

### 🚨 Incidents
- View active and resolved incidents
- Inspect full incident timelines
- Resolve incidents explicitly

### 🔔 Alerts
- View all simulated alerts
- Trigger test alerts manually

> 📖 Full interactive documentation available at [`/docs`](http://localhost:8000/docs) (Swagger UI)

---

## 🚀 Getting Started

```bash
# 1. Clone the repository
git clone <repo-url>
cd api-pulse

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate       # macOS / Linux
.\venv\Scripts\activate        # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the server
uvicorn app.main:app --reload
```

Once running, open your browser to:

```
http://localhost:8000/docs
```

---

## 🌱 Demo Seed Data

Populate the system with realistic demo data in one command:

```bash
python app/demo/seed.py
```

This will:

- ✅ Create a demo user account
- ✅ Create sample monitors
- ✅ Simulate failure scenarios
- ✅ Generate incidents with full timelines
- ✅ Produce persisted alerts

You'll have a fully populated system ready to explore immediately — no manual setup required.

---

## ⚙️ Engineering Principles

API Pulse is built around a specific set of values:

| Principle | What it means in practice |
|---|---|
| Explicit domain modeling | Every concept has a clear, named representation |
| Predictable behavior | No randomness — all outcomes are reproducible |
| Clear data ownership | Each layer owns its concerns and nothing more |
| Readable architecture | Structure communicates intent without documentation |
| Realistic backend patterns | Failure states, timelines, and alert persistence mirror production patterns |

**Deliberately avoided:**

- Monolithic files
- Magic background jobs
- Hidden side effects
- Fragile demos that only work once

---

## 👥 Intended Audience

API Pulse is built for:

- **Founders** evaluating backend engineers
- **Backend developers** reviewing architecture and system design patterns
- **Engineers** interested in failure modeling and observability

> This is not a production uptime monitoring tool.
> It is a demonstration of backend thinking.

---

## 💬 Feedback & Discussion

Thoughtful feedback is welcome.

If you're building systems where **reliability and observability** matter, reach out — I'd love to exchange ideas.
