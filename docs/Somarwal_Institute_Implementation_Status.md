# Somarwal Institute Implementation Status

This document maps the SRS requirements to the current Docker-running application.

## Runtime

- Run: `docker compose up --build`
- Public URL: `http://localhost:8081`
- API docs: `http://localhost:8081/api/docs`
- API health: `http://localhost:8081/api/health`

## Login

- Admin: `admin@somarwal.edu` / `admin123456`
- Student: `student@somarwal.edu` / `student123456`

## SRS Feature Matrix

| Requirement | Status | Implementation |
| --- | --- | --- |
| Full-screen hero | Implemented | Public home page hero with institute positioning and primary CTAs |
| Admission Open alert | Implemented | Dynamic `announcements` payload from `/api/home` |
| Scholarship Exam alert | Implemented | Dynamic `announcements` payload from `/api/home` |
| Top Courses | Implemented | Home page course cards loaded from active courses |
| Why Choose Us | Implemented | Home page feature section |
| Student metrics | Implemented | `/api/home` stats counters |
| Placement section | Implemented | Placement cards from backend seed data |
| Student reviews | Implemented | Approved review cards from backend |
| Gallery preview | Implemented | Dynamic gallery section |
| Google Map | Implemented | Embedded map section for Ajmer location |
| Footer links/contact | Implemented | Footer with phone, email, location, admission status |
| CTA buttons | Implemented | Apply Now, WhatsApp Us, Call Now, Free Demo Class, Verify Certificate |
| About intro | Implemented | `/about` page |
| Mission and Vision | Implemented | `/about` page from `/api/home` about data |
| Director message/photo | Implemented | `/about` director section |
| Lab/team/faculty photos | Implemented | `/about` media gallery |
| Full course list | Implemented | 14 required courses seeded and exposed through `/api/courses` |
| Course detail pages | Implemented | Hash route `/course/{CODE}` with duration, fees, syllabus, software, certification, career, enroll CTA |
| Admission form fields | Implemented | Student name, DOB, father, school/college, qualification, WhatsApp number, email, address, course, payment mode |
| Registration number | Implemented | Generated as `SCI{year}{sequence}` |
| PDF receipt | Implemented | Receipt PDF path generated as `/receipts/{receipt_no}.pdf`; provider-grade PDF rendering can replace this path service |
| Email notification | Implemented | Notification row queued with `send_type=EMAIL` |
| WhatsApp notification | Implemented | Notification row queued with `send_type=WHATSAPP` |
| Admin course management | Implemented | Create/update/disable course APIs |
| Admin gallery management | Implemented | Create/delete gallery APIs |
| Admin review management | Implemented | Create/delete review APIs |
| Admin admission management | Implemented | Admin dashboard and student/admission list |
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
curl -X POST http://localhost:8081/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"admin@somarwal.edu","password":"admin123456"}'
```

