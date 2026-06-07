# Database Design Document (DDD)
## Somarwal Computer & Tech Institute, Ajmer

---

## 1. Overview
This document outlines the database schema for the Somarwal Computer & Tech Institute management system. The architecture is designed for a relational database system (MySQL/PostgreSQL) to ensure data integrity across users, courses, financial records, and academic progress.

---

## 2. Core Entities & Schema Details

### 2.1. Users Table
Manages system access and authentication for all roles.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INT/UUID | Primary Key | Unique user identifier |
| `name` | VARCHAR(100) | Not Null | Full name of the user |
| `email` | VARCHAR(150) | Unique | Login email address |
| `phone` | VARCHAR(20) | Unique | Contact number |
| `password_hash` | VARCHAR(255) | Not Null | Encrypted password (e.g., bcrypt) |
| `role` | ENUM | Not Null | `SUPER_ADMIN`, `ADMIN`, `STAFF`, `TEACHER`, `STUDENT` |
| `status` | BOOLEAN/ENUM | Default Active | Account status (Active/Inactive) |
| `last_login` | DATETIME | Nullable | Timestamp of last access |
| `created_at` | TIMESTAMP | Default NOW()| Record creation timestamp |
| `updated_at` | TIMESTAMP | Default NOW()| Record update timestamp |

### 2.2. Students Table
Stores detailed academic and personal information for enrolled students.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INT/UUID | Primary Key | Unique student identifier |
| `registration_no` | VARCHAR(50) | Unique | System-generated ID (e.g., SCI20260001) |
| `user_id` | INT/UUID | FK (users.id) | Link to system login credentials |
| `student_name` | VARCHAR(100) | Not Null | Full name |
| `father_name` | VARCHAR(100) | Not Null | Father's name |
| `dob` | DATE | Not Null | Date of Birth |
| `qualification` | VARCHAR(100) | Not Null | Highest educational qualification |
| `school_name` | VARCHAR(150) | Nullable | Previous/Current school or college |
| `address` | TEXT | Not Null | Full residential address |
| `photo` | VARCHAR(255) | Nullable | S3/Local URL to student avatar |
| `course_id` | INT/UUID | FK (courses.id)| Enrolled course |
| `admission_date` | DATE | Not Null | Date of enrollment |
| `status` | ENUM | Default Active | `ACTIVE`, `COMPLETED`, `DROPPED` |

### 2.3. Courses Table
Catalog of all training programs offered by the institute.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INT/UUID | Primary Key | Unique course identifier |
| `name` | VARCHAR(100) | Not Null | E.g., DCA, PGDCA, Tally GST, AI Course |
| `duration` | VARCHAR(50) | Not Null | E.g., '3 Months', '1 Year' |
| `fees` | DECIMAL(10,2) | Not Null | Total course fee |
| `description` | TEXT | Nullable | Detailed course overview |
| `syllabus` | JSON/TEXT | Nullable | Module and chapter breakdown |
| `software_covered`| JSON/TEXT | Nullable | List of tools (e.g., Word, Excel, Tally) |
| `career_options` | JSON/TEXT | Nullable | Potential job roles |
| `certificate_available`| BOOLEAN | Default True | Does the course provide a certificate? |
| `status` | BOOLEAN | Default True | Is the course currently active/visible? |

### 2.4. Fees Table
Financial ledger tracking student payments and dues.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INT/UUID | Primary Key | Unique transaction identifier |
| `student_id` | INT/UUID | FK (students.id)| Link to student |
| `total_amount` | DECIMAL(10,2) | Not Null | Total fee for the course |
| `paid_amount` | DECIMAL(10,2) | Not Null | Amount paid in this transaction |
| `pending_amount` | DECIMAL(10,2) | Not Null | Remaining balance after payment |
| `payment_mode` | ENUM | Not Null | `CASH`, `UPI`, `CARD`, `NETBANKING` |
| `transaction_id` | VARCHAR(100) | Nullable | Gateway ID for online payments |
| `receipt_no` | VARCHAR(50) | Unique | Auto-generated receipt number |
| `receipt_pdf` | VARCHAR(255) | Default Empty | Generated receipt PDF path, e.g. `/receipts/RCP20260001.pdf` |
| `created_at` | TIMESTAMP | Default NOW()| Date and time of payment |

### 2.5. Certificates Table
Registry for verifiable digital certificates.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INT/UUID | Primary Key | Unique internal ID |
| `certificate_no` | VARCHAR(100) | Unique | Public verification ID |
| `student_id` | INT/UUID | FK (students.id)| Certificate owner |
| `course_id` | INT/UUID | FK (courses.id)| Course completed |
| `grade` | VARCHAR(10) | Nullable | Final grade achieved |
| `percentage` | DECIMAL(5,2) | Nullable | Final percentage score |
| `issue_date` | DATE | Not Null | Date of issuance |
| `qr_code` | VARCHAR(255) | Nullable | URL to generated validation QR code |
| `pdf_url` | VARCHAR(255) | Not Null | Storage URL for the PDF document |
| `status` | ENUM | Default Active | `ACTIVE`, `REVOKED` |

---

## 3. Academic & Examination Schema

### 3.1. Exams Table
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INT/UUID | Primary Key | Unique exam ID |
| `name` | VARCHAR(100) | Not Null | Exam title |
| `course_id` | INT/UUID | FK (courses.id)| Associated course |
| `exam_type` | ENUM | Not Null | `ONLINE`, `PRACTICAL` |
| `duration` | INT | Not Null | Exam duration in minutes |
| `date` | DATETIME | Not Null | Scheduled exam timestamp |

### 3.2. Practical Exam Tasks Table
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INT/UUID | Primary Key | Unique task ID |
| `exam_id` | INT/UUID | FK (exams.id) | Associated exam |
| `task_type` | ENUM | Not Null | `WORD`, `EXCEL`, `PPT`, `TALLY`, `TYPING` |
| `file` | VARCHAR(255) | Nullable | URL to required resources/files |
| `time_limit` | INT | Not Null | Time limit for this specific task |
| `marks` | INT | Not Null | Maximum marks achievable |

### 3.3. Results Table
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INT/UUID | Primary Key | Unique result ID |
| `student_id` | INT/UUID | FK (students.id)| Associated student |
| `exam_id` | INT/UUID | FK (exams.id) | Associated exam |
| `marks` | DECIMAL(5,2) | Not Null | Marks obtained |
| `percentage` | DECIMAL(5,2) | Not Null | Calculated percentage |
| `grade` | VARCHAR(10) | Not Null | Calculated grade |
| `result_pdf` | VARCHAR(255) | Nullable | URL to downloadable report card |

### 3.4. Attendance Table
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INT/UUID | Primary Key | Unique attendance ID |
| `student_id` | INT/UUID | FK (students.id)| Associated student |
| `date` | DATE | Not Null | Date of attendance |
| `status` | ENUM | Not Null | `PRESENT`, `ABSENT`, `LEAVE` |
| `qr_scan_time` | DATETIME | Nullable | Exact scan time if QR tech is used |

### 3.5. Study Material Table
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INT/UUID | Primary Key | Unique material ID |
| `course_id` | INT/UUID | FK (courses.id)| Target course |
| `teacher_id` | INT/UUID | FK (users.id) | Uploading teacher |
| `type` | ENUM | Not Null | `PDF`, `VIDEO`, `NOTES` |
| `file_url` | VARCHAR(255) | Not Null | Cloud storage link |
| `created_at` | TIMESTAMP | Default NOW()| Upload timestamp |

---

## 4. Operational & Frontend Schema

### 4.1. Gallery Table
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INT/UUID | Primary Key | Unique media ID |
| `title` | VARCHAR(150) | Nullable | Image/Video title |
| `image` | VARCHAR(255) | Not Null | Storage URL |
| `category` | VARCHAR(50) | Not Null | E.g., 'Labs', 'Events', 'Awards' |
| `created_at` | TIMESTAMP | Default NOW()| Upload timestamp |

### 4.2. Placements Table
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INT/UUID | Primary Key | Unique placement ID |
| `student_id` | INT/UUID | FK (students.id)| Placed student |
| `company` | VARCHAR(150) | Not Null | Hiring company name |
| `package` | VARCHAR(100) | Nullable | Salary package details |
| `photo` | VARCHAR(255) | Nullable | Celebration/Student photo URL |
| `description` | TEXT | Nullable | Success story details |

### 4.3. Blogs Table
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INT/UUID | Primary Key | Unique post ID |
| `title` | VARCHAR(200) | Not Null | Post title |
| `content` | TEXT | Not Null | Post body (HTML/Markdown) |
| `category` | VARCHAR(50) | Not Null | Post category |
| `image` | VARCHAR(255) | Nullable | Featured image URL |
| `author` | VARCHAR(100) | Not Null | Author name |
| `created_at` | TIMESTAMP | Default NOW()| Publishing timestamp |

### 4.4. Notifications Table
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INT/UUID | Primary Key | Unique log ID |
| `title` | VARCHAR(150) | Not Null | Alert subject |
| `message` | TEXT | Not Null | Alert body |
| `receiver` | VARCHAR(100) | Not Null | Target (User ID, Phone, or Email) |
| `send_type` | ENUM | Not Null | `EMAIL`, `WHATSAPP`, `APP` |
| `status` | ENUM/VARCHAR | Default Queued | `QUEUED`, `SENT`, `FAILED`, `SKIPPED` |
| `created_at` | TIMESTAMP | Default NOW()| Dispatch timestamp |

**Current Implementation Note:** Online admission creates one `EMAIL` notification row and one `WHATSAPP` notification row. These rows are provider-ready automation logs; SMTP and WhatsApp Business credentials can be connected later without changing the admission workflow.
