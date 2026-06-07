# Somarwal Institute Implementation Status

This document maps the SRS requirements to the current Docker-running application.

## Runtime

- Run: `docker compose up --build`
- Public URL: `http://localhost:8081`
- API docs: `http://localhost:8081/api/docs`
- API health: `http://localhost:8081/api/health`

## Current Staging Release Scope

The `staging` branch currently exposes only the production-critical public pages:

- Home page: `/#/`
- Courses page: `/#/courses`
- Certificate verification page: `/#/verify`
- Typing practice page: `/#/typing`

Admission, enquiry, about, login, admin, and student portal screens remain in the codebase for future rollout, but they are intentionally hidden from staging navigation while the first production goal is public course browsing, typing practice, and certificate verification.

## Login

- Admin: `admin@somarwal.edu` / `admin123456`
- Student: `student@somarwal.edu` / `student123456`

## SRS Feature Matrix

| Requirement | Status | Implementation |
| --- | --- | --- |
| Full-screen hero | Exposed | Public home page hero with institute positioning and certificate verification CTA |
| Admission Open alert | Hidden on staging | Backend data exists, but staging keeps public navigation focused |
| Scholarship Exam alert | Hidden on staging | Backend data exists, but staging keeps public navigation focused |
| Top Courses | Implemented | Home page course cards loaded from active courses |
| Why Choose Us | Implemented | Home page feature section |
| Student metrics | Implemented | `/api/home` stats counters |
| Placement section | Implemented | Placement cards from backend seed data |
| Student reviews | Implemented | Approved review cards from backend |
| Gallery preview | Implemented | Dynamic gallery section |
| Google Map | Implemented | Embedded map section for Ajmer location |
| Footer links/contact | Implemented | Footer with phone, email, location, admission status |
| CTA buttons | Exposed partially | Verify Certificate, View Courses, WhatsApp Us, Call Now |
| About intro | Hidden on staging | Code retained for future rollout |
| Mission and Vision | Hidden on staging | Code retained for future rollout |
| Director message/photo | Hidden on staging | Code retained for future rollout |
| Lab/team/faculty photos | Hidden on staging | Code retained for future rollout |
| Full course list | Implemented | 14 required courses seeded and exposed through `/api/courses` |
| Typing practice | Exposed | Public `/typing` page with timed, paragraph, custom, and numbers practice |
| Typing test metrics | Implemented | Live WPM, raw WPM, CPM, accuracy, errors, progress, time, result summary |
| Typing result history | Implemented | Browser-local history of last 10 test results with clear action |
| Course detail pages | Hidden on staging | Course list is exposed; detail/enroll pages are future rollout |
| Admission form fields | Hidden on staging | Backend code retained for future rollout |
| Registration number | Implemented | Generated as `SCI{year}{sequence}` |
| PDF receipt | Implemented | Receipt PDF path generated as `/receipts/{receipt_no}.pdf`; provider-grade PDF rendering can replace this path service |
| Email notification | Implemented | Notification row queued with `send_type=EMAIL` |
| WhatsApp notification | Implemented | Notification row queued with `send_type=WHATSAPP` |
| Admin course management | Implemented | Create/update/disable course APIs |
| Admin gallery management | Implemented | Create/delete gallery APIs |
| Admin review management | Implemented | Create/delete review APIs |
| Admin admission management | Hidden on staging | Backend code retained for future rollout |
| Responsiveness | Implemented | CSS breakpoints for desktop/tablet/mobile |
| Docker-only runtime | Implemented | All app services run through Docker Compose |

## Required Course Catalog

- Basic Computer
- MS Office
- DCA
- PGDCA
- Tally Prime with GST
- GST / ITR
- Graphic Designing
- AI Course
- Typing Course
- Advance Excel Mastery
- Spoken English
- Video Editing
- Hardware & Networking
- Class 5th to 10th Coaching Classes

## Tested Endpoints

Use the Docker gateway URL:

```bash
curl http://localhost:8081/api/health
curl http://localhost:8081/api/home
curl http://localhost:8081/api/courses
curl http://localhost:8081/api/certificate/verify/CERT1001
```

## Typing Practice Features

- Timed tests: 1, 2, 3, and 5 minute options
- Practice modes: timed, paragraph, and custom text
- Levels: beginner, intermediate, advanced, and numbers
- Live metrics: WPM, raw WPM, CPM, accuracy, errors, time, and progress
- Character-level highlighting for correct and incorrect typing
- Result summary after completion
- Local best WPM and recent history, saved in the browser
