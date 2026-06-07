from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    phone: Mapped[str | None] = mapped_column(String(20), unique=True, nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20), default="STUDENT")
    status: Mapped[bool] = mapped_column(Boolean, default=True)
    last_login: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    phone_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    student: Mapped["Student | None"] = relationship(back_populates="user")
    sessions: Mapped[list["Session"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    otps: Mapped[list["OTP"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class OTP(Base, TimestampMixin):
    __tablename__ = "otps"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    contact: Mapped[str] = mapped_column(String(150), index=True)
    otp_code: Mapped[str] = mapped_column(String(10))
    otp_type: Mapped[str] = mapped_column(String(50))
    expires_at: Mapped[datetime] = mapped_column(DateTime)
    is_used: Mapped[bool] = mapped_column(Boolean, default=False)

    user: Mapped["User | None"] = relationship(back_populates="otps")


class Session(Base, TimestampMixin):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    jti: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    session_expires_at: Mapped[datetime] = mapped_column(DateTime)
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False)

    user: Mapped["User"] = relationship(back_populates="sessions")


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), index=True)
    code: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    category: Mapped[str] = mapped_column(String(80), index=True)
    duration: Mapped[str] = mapped_column(String(50))
    fees: Mapped[float] = mapped_column(Float)
    description: Mapped[str] = mapped_column(Text)
    syllabus: Mapped[str] = mapped_column(Text, default="[]")
    software_covered: Mapped[str] = mapped_column(Text, default="[]")
    career_options: Mapped[str] = mapped_column(Text, default="[]")
    certificate_available: Mapped[bool] = mapped_column(Boolean, default=True)
    status: Mapped[bool] = mapped_column(Boolean, default=True)

    students: Mapped[list["Student"]] = relationship(back_populates="course")
    certificates: Mapped[list["Certificate"]] = relationship(back_populates="course")
    batches: Mapped[list["Batch"]] = relationship(back_populates="course", cascade="all, delete-orphan")


class Batch(Base, TimestampMixin):
    __tablename__ = "batches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    batch_no: Mapped[str] = mapped_column(String(50), index=True)
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(20), default="UPCOMING")

    course: Mapped[Course] = relationship(back_populates="batches")
    students: Mapped[list["Student"]] = relationship(back_populates="batch")


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    registration_no: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    student_name: Mapped[str] = mapped_column(String(100), index=True)
    father_name: Mapped[str] = mapped_column(String(100))
    dob: Mapped[date] = mapped_column(Date)
    qualification: Mapped[str] = mapped_column(String(100), default="")
    school_name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    phone: Mapped[str] = mapped_column(String(20), index=True)
    email: Mapped[str | None] = mapped_column(String(150), nullable=True)
    address: Mapped[str] = mapped_column(Text, default="")
    photo: Mapped[str | None] = mapped_column(String(255), nullable=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    batch_id: Mapped[int | None] = mapped_column(ForeignKey("batches.id"), nullable=True)
    admission_date: Mapped[date] = mapped_column(Date, default=date.today)
    status: Mapped[str] = mapped_column(String(20), default="ACTIVE")

    user: Mapped[User | None] = relationship(back_populates="student")
    course: Mapped[Course] = relationship(back_populates="students")
    batch: Mapped[Batch | None] = relationship(back_populates="students")
    fees: Mapped[list["Fee"]] = relationship(back_populates="student")
    certificates: Mapped[list["Certificate"]] = relationship(back_populates="student")


class Fee(Base):
    __tablename__ = "fees"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    total_amount: Mapped[float] = mapped_column(Float)
    paid_amount: Mapped[float] = mapped_column(Float)
    pending_amount: Mapped[float] = mapped_column(Float)
    payment_mode: Mapped[str] = mapped_column(String(20))
    transaction_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    receipt_no: Mapped[str] = mapped_column(String(50), unique=True)
    receipt_pdf: Mapped[str] = mapped_column(String(255), default="")
    status: Mapped[str] = mapped_column(String(20), default="PENDING")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    student: Mapped[Student] = relationship(back_populates="fees")


class Certificate(Base):
    __tablename__ = "certificates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    certificate_no: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    grade: Mapped[str] = mapped_column(String(10), default="A")
    percentage: Mapped[float] = mapped_column(Float, default=0)
    issue_date: Mapped[date] = mapped_column(Date, default=date.today)
    qr_code: Mapped[str | None] = mapped_column(String(255), nullable=True)
    pdf_url: Mapped[str] = mapped_column(String(255), default="")
    status: Mapped[str] = mapped_column(String(20), default="ACTIVE")

    student: Mapped[Student] = relationship(back_populates="certificates")
    course: Mapped[Course] = relationship(back_populates="certificates")


class Enquiry(Base, TimestampMixin):
    __tablename__ = "enquiries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(20))
    email: Mapped[str | None] = mapped_column(String(150), nullable=True)
    course_interest: Mapped[str | None] = mapped_column(String(120), nullable=True)
    source: Mapped[str] = mapped_column(String(50), default="Website")
    comments_questions: Mapped[str] = mapped_column(Text, default="")
    preferred_time: Mapped[str | None] = mapped_column(String(50), nullable=True)
    preferred_mode: Mapped[str | None] = mapped_column(String(50), nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="NEW")


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(150))
    message: Mapped[str] = mapped_column(Text)
    receiver: Mapped[str] = mapped_column(String(150))
    send_type: Mapped[str] = mapped_column(String(20))
    status: Mapped[str] = mapped_column(String(30), default="QUEUED")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class Gallery(Base):
    __tablename__ = "gallery"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(150))
    image: Mapped[str] = mapped_column(String(500))
    category: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class Placement(Base):
    __tablename__ = "placements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_name: Mapped[str] = mapped_column(String(100))
    course: Mapped[str] = mapped_column(String(120))
    company: Mapped[str] = mapped_column(String(150))
    package: Mapped[str | None] = mapped_column(String(100), nullable=True)
    photo: Mapped[str | None] = mapped_column(String(500), nullable=True)
    description: Mapped[str] = mapped_column(Text, default="")


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_name: Mapped[str] = mapped_column(String(100))
    course: Mapped[str] = mapped_column(String(120))
    rating: Mapped[int] = mapped_column(Integer, default=5)
    message: Mapped[str] = mapped_column(Text)
    photo: Mapped[str | None] = mapped_column(String(500), nullable=True)
    approved: Mapped[bool] = mapped_column(Boolean, default=True)


class StudyMaterial(Base):
    __tablename__ = "study_material"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    title: Mapped[str] = mapped_column(String(150))
    type: Mapped[str] = mapped_column(String(20))
    file_url: Mapped[str] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class Result(Base):
    __tablename__ = "results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    exam_name: Mapped[str] = mapped_column(String(120))
    marks: Mapped[float] = mapped_column(Float)
    percentage: Mapped[float] = mapped_column(Float)
    grade: Mapped[str] = mapped_column(String(10))
    result_pdf: Mapped[str | None] = mapped_column(String(255), nullable=True)


class TypingResult(Base):
    __tablename__ = "typing_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int | None] = mapped_column(ForeignKey("students.id"), nullable=True)
    wpm: Mapped[int] = mapped_column(Integer)
    accuracy: Mapped[float] = mapped_column(Float)
    rank: Mapped[str] = mapped_column(String(30), default="Learner")
    time: Mapped[int] = mapped_column(Integer, default=60)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
