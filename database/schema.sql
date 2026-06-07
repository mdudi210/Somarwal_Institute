CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(150) UNIQUE NOT NULL,
  phone VARCHAR(20) UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  role VARCHAR(20) NOT NULL,
  status BOOLEAN DEFAULT TRUE,
  last_login TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE courses (
  id SERIAL PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  code VARCHAR(30) UNIQUE NOT NULL,
  category VARCHAR(80) NOT NULL,
  duration VARCHAR(50) NOT NULL,
  fees NUMERIC(10,2) NOT NULL,
  description TEXT,
  syllabus JSONB,
  software_covered JSONB,
  career_options JSONB,
  certificate_available BOOLEAN DEFAULT TRUE,
  status BOOLEAN DEFAULT TRUE
);

CREATE TABLE students (
  id SERIAL PRIMARY KEY,
  registration_no VARCHAR(50) UNIQUE NOT NULL,
  user_id INTEGER REFERENCES users(id),
  student_name VARCHAR(100) NOT NULL,
  father_name VARCHAR(100) NOT NULL,
  dob DATE NOT NULL,
  qualification VARCHAR(100),
  school_name VARCHAR(150),
  phone VARCHAR(20) NOT NULL,
  email VARCHAR(150),
  address TEXT,
  photo VARCHAR(255),
  course_id INTEGER REFERENCES courses(id),
  admission_date DATE NOT NULL,
  status VARCHAR(20) DEFAULT 'ACTIVE'
);

CREATE TABLE fees (
  id SERIAL PRIMARY KEY,
  student_id INTEGER REFERENCES students(id),
  total_amount NUMERIC(10,2) NOT NULL,
  paid_amount NUMERIC(10,2) NOT NULL,
  pending_amount NUMERIC(10,2) NOT NULL,
  payment_mode VARCHAR(20) NOT NULL,
  transaction_id VARCHAR(100),
  receipt_no VARCHAR(50) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE certificates (
  id SERIAL PRIMARY KEY,
  certificate_no VARCHAR(100) UNIQUE NOT NULL,
  student_id INTEGER REFERENCES students(id),
  course_id INTEGER REFERENCES courses(id),
  grade VARCHAR(10),
  percentage NUMERIC(5,2),
  issue_date DATE NOT NULL,
  qr_code VARCHAR(255),
  pdf_url VARCHAR(255) NOT NULL,
  status VARCHAR(20) DEFAULT 'ACTIVE'
);

