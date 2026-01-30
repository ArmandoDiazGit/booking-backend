# Spa Website Backend (FastAPI)

Backend API for my Spa & Massage website, built with **FastAPI**. This service provides **CRUD (Create, Read, Update, Delete)** operations for core app data (ex: bookings/services) and is designed to connect to a frontend and an admin panel.

> Note: **Authentication/login is not implemented yet**.

---

## Features
- FastAPI REST API
- **CRUD functions** for managing records (Create / Read / Update / Delete)
- JSON request/response
- Ready to be consumed by:
  - Spa Website Frontend (React/Vite)
  - Admin Panel (Angular)

---

## CRUD Operations (Overview)
This API follows a standard CRUD pattern:

- **Create** → add a new record (example: create a booking)
- **Read** → fetch one or many records (example: list bookings / get by id)
- **Update** → edit an existing record (example: update booking status or time)
- **Delete** → remove a record (example: cancel/delete a booking)

---

## Tech Stack
- **Framework:** FastAPI
- **Server:** Uvicorn
- **Database:** (add yours here: SQLite / Postgres / etc.)
- **Auth:** Not added yet

---

## Getting Started

### 1) Clone the repo
```bash
git clone https://github.com/ArmandoDiazGit/booking-backend.git
cd <your-repo-folder>
```

### 2) Create and activate a virtual environment (recommended)
```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows (PowerShell)
```

### 3) Install dependencies
```bash
pip install -r requirements.txt
```

### 4) Run the API
```bash
uvicorn app.main:app --reload
```
- API will be available at:

```http://127.0.0.1:8000 ```

Interactive docs:

- Swagger UI: ```http://127.0.0.1:8000/docs```

## Roadmap

- Add login/authentication (JWT or session-based)

- Admin-only protected endpoints

- Role-based access (admin vs public)

- Deployment configuration

## Related Repos

- Spa Website Frontend (React/Vite): ``` https://github.com/ArmandoDiazGit/My-spa-website ```

- Admin Panel (Angular): <link-here> ``` https://github.com/ArmandoDiazGit/angular-admin-panel ```
