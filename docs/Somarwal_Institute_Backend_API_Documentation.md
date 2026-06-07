# Backend API & System Architecture Documentation

## Somarwal Computer & Tech Institute, Ajmer

---

## 1. Recommended Technology Stack

- **Backend:** Python FastAPI, PostgreSQL, Redis, Celery (for background tasks), S3 Storage, Docker.
- **Frontend:** React / Next.js, Tailwind CSS, Progressive Web App (PWA).
- **Mobile:** PWA or React Native.

---

## 2. Authentication & Session Management

### 2.1. Registration API

- **Endpoint:** `POST /api/auth/register`
- **Request:**
  ```json
  {
    "name": "Rahul",
    "email": "rahul@gmail.com",
    "password": "123456",
    "role": "student"
  }
  ```
- **Response:**
  ```json
  {
    "status": true,
    "user_id": 101
  }
  ```

### 2.2. Login API

- **Endpoint:** `POST /api/auth/login`
- **Workflow:** Verify password hash -> Create JWT access & refresh tokens -> Store session in Redis.
- **Request:**
  ```json
  {
    "email": "admin@gmail.com",
    "password": "123456"
  }
  ```
- **Response:**
  ```json
  {
    "access_token": "xxxx",
    "refresh_token": "xxxx",
    "role": "ADMIN"
  }
  ```

### 2.3. Session Management Design

- **JWT Access Token:** Expiry = 15 minutes.
- **JWT Refresh Token:** Expiry = 7 days.
- **Redis Session Storage (`session:user_id`):**
  ```json
  {
    "device": "chrome",
    "ip": "192.168.x.x",
    "login_time": "2026-05-29T10:00:00Z",
    "token_id": "unique-token-id"
  }
  ```

### 2.4. Logout API

- **Endpoint:** `POST /api/auth/logout`
- **Action:** Delete Redis session, blacklist JWT.

---

## 3. Core Application APIs

### Current Docker Base URL

- Public app/API gateway: `http://localhost:8081`
- API docs: `http://localhost:8081/api/docs`
- Health check: `GET /api/health`

### 3.1. Admission API

- **Endpoint:** `POST /api/admission/apply`
- **Workflow:** Generate Registration ID (e.g., `REG20260001`) -> Create Student Account -> Generate Admission PDF -> Send Email & WhatsApp.
- **Request:**
  ```json
  {
    "name": "Amit",
    "dob": "2005-01-01",
    "father": "Raj",
    "phone": "9999999999",
    "course": "DCA"
  }
  ```
- **Response:**
  ```json
  {
    "registration_no": "REG20260001",
    "receipt": "receipt.pdf",
    "receipt_url": "/receipts/RCP20260001.pdf",
    "student_id": 1,
    "pending_amount": 0,
    "email_notification": "QUEUED",
    "whatsapp_notification": "QUEUED"
  }
  ```

- **Implemented Automation:** The Docker app generates registration number, receipt number, receipt PDF path, and stores notification logs for SMTP/WhatsApp processing. External SMTP and WhatsApp providers are integration-ready and represented by queued `notifications` rows until provider credentials are configured.

### 3.2. Certificate Verification API

- **Endpoint:** `GET /api/certificate/verify/{certificate_no}`
- **Response (Success):**
  ```json
  {
    "verified": true,
    "student": "Rahul",
    "course": "DCA",
    "grade": "A",
    "percentage": 90,
    "issue_date": "20-05-2026"
  }
  ```
- **Response (Fake):**
  ```json
  {
    "verified": false,
    "message": "Fake Certificate Detected"
  }
  ```

### 3.3. QR Verification Flow

- **QR Contains:** `https://website.com/verify/CERT1001`
- **Flow:** Scan QR -> API Call -> Database Check -> Display "Verified By Somarwal Institute" with Timestamp.

---

## 4. Portal Endpoints

### 4.1. Student Portal

- **Dashboard:** `GET /api/student/dashboard`
- **Study Material:** `GET /api/student/notes`, `GET /api/student/videos`
- **Academics:** `GET /api/student/results`, `GET /api/student/assignments`

### 4.2. Admin Dashboard

- **Dashboard:** `GET /api/admin/dashboard`
- **Student Management:** `GET /api/admin/students`
- **Course Management:** `GET /api/admin/courses`, `POST /api/admin/courses`, `PUT /api/admin/courses/{course_id}`, `DELETE /api/admin/courses/{course_id}`
- **Gallery Management:** `POST /api/admin/gallery`, `DELETE /api/admin/gallery/{gallery_id}`
- **Review Management:** `POST /api/admin/reviews`, `DELETE /api/admin/reviews/{review_id}`
- **Certificate Generation:** `POST /api/admin/certificate/create`
- **Content Overview:** `GET /api/admin/content`

---

## 5. Microservices & Modules

### 5.1. Typing Test Module

- **Table Schema (`typing_results`):** `student_id`, `wpm`, `accuracy`, `rank`, `time`, `created_at`.
- **API:** `POST /api/typing/submit`
  ```json
  {
    "wpm": 45,
    "accuracy": 96
  }
  ```

### 5.2. PDF & Utility Tools API

- **Microservice Stack:** Python (PyPDF, Pillow, OpenCV, OCR)
- **Endpoints:**
  - `POST /tools/pdf/merge`
  - `POST /tools/pdf/compress`
  - `POST /tools/pdf-to-word`
  - `POST /tools/image-to-text`
  - `POST /tools/remove-background`
  - `POST /tools/create-qr`

### 5.3. AI Chatbot Architecture

- **Flow:** User Query ("Fees of DCA?") -> Frontend Chat -> AI API -> Knowledge Base (courses, fees, timings, FAQ database) -> Response.

---

## 6. Security Design

- **Passwords:** `bcrypt` hashing.
- **API Security:** JWT, Refresh Token Rotation, Rate Limiting, CORS, Input Validation, SQL Injection Protection.
- **File Security:** Private Storage, Signed URLs for secure access, Virus Scanning on uploads.

---

## 7. Folder Structure

```text
somarwal-platform/
│
├── backend/
│   ├── app/
│   │   ├── auth/
│   │   ├── students/
│   │   ├── courses/
│   │   ├── exams/
│   │   ├── certificates/
│   │   ├── payments/
│   │   ├── chatbot/
│   │   └── tools/
│
├── frontend/
│   ├── pages/
│   ├── components/
│   ├── admin/
│   └── student/
│
├── database/
├── docker/
└── nginx/
```

---

## 8. Deployment Architecture

```text
                 [ Internet ]
                      |
                  [ NGINX ]
                      |
        +-------------+-------------+
        |                           |
    [ React ]                 [ FastAPI ]
                                    |
                 +------------------+------------------+
                 |                  |                  |
          [ PostgreSQL ]        [ Redis ]       [ File Storage ]
```
