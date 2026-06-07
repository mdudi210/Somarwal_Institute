# Somarwal Institute Full Stack Platform

Fresh full stack implementation for Somarwal Computer & Tech Institute, Ajmer, based on the requirement, API, architecture, and database documents in `docs/`.

## Stack

- Backend: FastAPI, SQLAlchemy, JWT auth, PostgreSQL via Docker Compose
- Frontend: React, Vite, PWA manifest/service worker, responsive institute website, admin panel, and student portal
- Runtime: Docker Compose with backend, frontend, PostgreSQL, Redis, and NGINX

## Docker Only Quick Start

Run the complete application in containers:

```bash
docker compose up --build
```

Open:

- Website/PWA/Admin/Student app: `http://localhost:8081`
- Backend API docs through NGINX: `http://localhost:8081/api/docs`
- Backend health check: `http://localhost:8081/api/health`

Seeded login:

- Admin: `admin@somarwal.edu` / `admin123456`
- Student: `student@somarwal.edu` / `student123456`

Stop containers:

```bash
docker compose down
```

Reset database data:

```bash
docker compose down -v
docker compose up --build
```

Do not run `npm install`, `uvicorn`, or local virtualenv commands on the host machine. All dependencies are installed inside Docker images.

## Core Features

- Dynamic courses, syllabus, fee, gallery, reviews, placement, blog, and notification data
- Admission form with generated registration number and receipt number
- Public certificate verification by certificate number
- JWT login with admin/student roles
- Admin dashboard for metrics, admissions, courses, certificates, payments, enquiries, gallery, and results
- Student dashboard with profile, fees, results, study material, attendance, typing test, and certificate status
- PWA install metadata and offline shell fallback
