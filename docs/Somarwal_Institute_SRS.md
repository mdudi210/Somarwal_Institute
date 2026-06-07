# Software Requirement Specification (SRS)
## Somarwal Computer & Tech Institute, Ajmer

---

## 1. Project Overview
The project is a fully dynamic web platform and comprehensive Admin Panel designed for the Somarwal Computer & Tech Institute, Ajmer. The system aims to digitalize the institute's operations, providing an attractive frontend for prospective students and a robust backend for staff. Core capabilities include online admissions, dynamic course and syllabus management, automated receipt generation, integrated communication (WhatsApp/Email), and secure certificate verification.

---

## 2. User Roles
The system will primarily support two distinct user roles, each with specific permissions and access levels:

### 2.1. Public User (Visitor / Prospective Student / Enrolled Student)
* **Access:** Frontend website only.
* **Capabilities:** * Browse institute information, facilities, and director's message.
  * View available courses, syllabi, and fee structures.
  * Submit online admission forms and make payments.
  * Verify issued certificates via a unique ID.
  * Submit enquiries and request demo classes.

### 2.2. Administrator (Institute Staff / Director)
* **Access:** Secure Backend Admin Dashboard.
* **Capabilities:**
  * **CRUD Operations:** Full control over Courses, Students, Galleries, and Enquiries.
  * **Financial Management:** Manage fees, view payments, and track revenue.
  * **Certificate Management:** Generate, upload, and disable certificates.
  * **Automation Oversight:** Manage placement records, student reviews, and system-generated communications.

---

## 3. Modules
The system is divided into functional modules to ensure separation of concerns and maintainability.

### 3.1. Website Frontend (Public Portal)
* **Home Page:** Hero section, admission announcements, scholarship exams, top courses, achievement counters, and placement highlights.
* **About Us:** History, facilities, training approach, and Director's message.
* **Dynamic Gallery:** Categorized visual media (labs, events, awards).

### 3.2. Course Management Module
* **Dynamic Catalog:** Display of diverse courses (Basic Computer, AI, Tally Prime, Graphic Design, etc.).
* **Course Details:** Dynamic syllabus management (chapters, topics, software covered), fee structure, and career opportunities.

### 3.3. Online Admission & Enrollment System
* **Registration:** Comprehensive data collection form (personal details, course selection, payment option).
* **Automation:** Auto-generation of unique Registration IDs (e.g., SCI20260001).
* **Communication triggers:** Automated Email and WhatsApp confirmation messages.
* **Receipts:** System-generated PDF fee receipts with authorized signatures.

### 3.4. Certificate Verification Module
* **Public Gateway:** Input fields for Certificate ID / Registration Number.
* **Validation display:** Student details, course duration, and certificate status.

### 3.5. Admin Control Panel
* **Dashboard:** High-level metrics (total students, active courses, revenue).
* **Student/Enquiry Management:** Review admissions, allocate courses, and track lead sources (Contact form, WhatsApp, Demo requests).
* **Media & Review Management:** Approve/delete testimonials and upload placement records.

### 3.6. Current Docker Implementation Coverage
The running Docker application now includes:
* Home page hero, admission/scholarship announcements, CTAs, counters, courses, placements, reviews, gallery, and Google Map embed.
* About page with institute introduction, mission, vision, director message/photo, lab photos, and team/faculty media.
* Dynamic catalog for all required courses: Basic Computer, MS Office, DCA, PGDCA, Tally Prime with GST, GST/ITR, Graphic Designing, AI Course, Typing Course, Advance Excel Mastery, Spoken English, Video Editing, Hardware & Networking, and Class 5th to 10th Coaching Classes.
* Individual course pages with duration, fees, syllabus, software covered, certification detail, career opportunities, and enroll CTA.
* Admission automation with registration number, receipt PDF path, queued email notification, and queued WhatsApp notification logs.
* Admin APIs for course create/update/disable, gallery create/delete, review create/delete, admission listing, dashboard metrics, certificate creation, and automation log review.

---

## 4. Functional Requirements
* **FR-1:** The system must generate a unique Registration Number for every successful admission.
* **FR-2:** The system must automatically generate and email a PDF receipt upon admission confirmation.
* **FR-3:** The system must trigger a WhatsApp API message to the registered mobile number post-admission.
* **FR-4:** The admin must be able to dynamically add, edit, or remove courses, modules, and syllabus topics without altering code.
* **FR-5:** The system must provide a secure portal for employers/students to verify certificate authenticity against the database.
* **FR-6:** The platform must support dynamic counter updates (students trained, placements) driven by database queries.

---

## 5. Non-Functional Requirements

### 5.1. Security Requirements
* **Authentication & Authorization:** Secure, token-based authentication (e.g., JWT) for the Admin Panel. Passwords must be hashed (e.g., bcrypt/Argon2id).
* **Data Protection:** Protection against SQL Injection, Cross-Site Scripting (XSS), and Cross-Site Request Forgery (CSRF).
* **Data Privacy:** Sensitive student data (contact info, IDs) must be encrypted at rest and in transit (HTTPS/SSL mandatory).
* **Rate Limiting:** Protect APIs (especially the Certificate Verification and Enquiry endpoints) from brute-force or scraping attacks.

### 5.2. Performance Requirements
* **Response Time:** Page load times should be under 2.5 seconds on standard broadband connections.
* **Concurrency:** The system should handle at least 500 concurrent users without degradation, specifically during scholarship exam result announcements or admission drives.
* **Responsiveness:** The UI must be fully responsive, scoring highly on Google Lighthouse for mobile rendering.

---

## 6. Backup Strategy
* **Database Backups:** Automated daily incremental backups and weekly full backups of the relational database (MySQL/PostgreSQL) to a secure, off-site cloud storage bucket (e.g., AWS S3).
* **Media Backups:** Syncing of all uploaded assets (student photos, gallery images, certificate PDFs) to a secondary storage location weekly.
* **Retention Policy:** Backups must be retained for a minimum of 90 days.
* **Disaster Recovery:** A documented protocol to restore the application from the latest backup within a 4-hour Recovery Time Objective (RTO).

---

## 7. Deployment Requirements

### 7.1. Technology Stack
* **Frontend Engine:** React.js or Next.js (preferred for SEO and SSR), styled with modern CSS frameworks (Tailwind CSS).
* **Backend API:** Node.js (Express), Django, or Laravel.
* **Database Engine:** MySQL or PostgreSQL.

### 7.2. Integrations & APIs
* **Messaging:** WhatsApp Business API (e.g., Twilio or Meta Graph API).
* **Emailing:** SMTP provider (e.g., SendGrid, AWS SES).
* **Document Generation:** Server-side PDF generation library (e.g., Puppeteer, PDFKit).
* **Mapping:** Google Maps API for location integration.

### 7.3. Hosting & Infrastructure
* **Server Environment:** Cloud-based Virtual Private Server (VPS) (e.g., AWS EC2, DigitalOcean Droplet, or Vercel for frontend/Render for backend).
* **CI/CD:** Automated deployment pipeline via GitHub Actions to ensure zero-downtime updates.
* **Domain & SSL:** Custom domain integration with auto-renewing Let's Encrypt SSL certificates.
