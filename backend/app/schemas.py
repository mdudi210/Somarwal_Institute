from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=6)
    role: str = "STUDENT"
    phone: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    role: str
    name: str


class CourseBase(BaseModel):
    name: str
    code: str
    category: str
    duration: str
    fees: float
    description: str
    syllabus: list[str] = []
    software_covered: list[str] = []
    career_options: list[str] = []
    certificate_available: bool = True
    status: bool = True


class CourseOut(CourseBase):
    id: int

    class Config:
        from_attributes = True


class AdmissionCreate(BaseModel):
    name: str
    dob: date
    father: str
    phone: str
    email: EmailStr | None = None
    qualification: str = ""
    school_name: str | None = None
    address: str = ""
    course: str
    batch_id: int
    payment_mode: str = "UPI"
    paid_amount: float = 0
    transaction_id: str | None = None
    otp_code: str | None = None


class VerifyOTPRequest(BaseModel):
    email: EmailStr
    email_otp: str
    phone_otp: str


class SendPhoneOTPRequest(BaseModel):
    phone: str


class AdmissionResponse(BaseModel):
    registration_no: str
    receipt: str
    receipt_url: str
    student_id: int
    pending_amount: float
    email_notification: str
    whatsapp_notification: str


class EnquiryCreate(BaseModel):
    name: str
    phone: str
    email: EmailStr | None = None
    course_interest: str | None = None
    source: str = "Website"
    comments_questions: str = ""
    preferred_time: str | None = None
    preferred_mode: str | None = None


class BatchCreate(BaseModel):
    course_id: int
    batch_no: str
    start_date: date
    end_date: date
    status: str = "UPCOMING"


class BatchOut(BatchCreate):
    id: int
    class Config:
        from_attributes = True


class BatchUpdate(BaseModel):
    batch_no: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    status: str | None = None


class CertificateCreate(BaseModel):
    student_id: int
    course_id: int
    grade: str = "A"
    percentage: float = 90
    certificate_no: str | None = None


class CertificateUpdate(BaseModel):
    grade: str | None = None
    percentage: float | None = None
    certificate_no: str | None = None


class GalleryCreate(BaseModel):
    title: str
    image: str
    category: str


class ReviewCreate(BaseModel):
    student_name: str
    course: str
    rating: int = 5
    message: str
    photo: str | None = None
    approved: bool = True


class CertificateVerify(BaseModel):
    verified: bool
    message: str | None = None
    student: str | None = None
    course: str | None = None
    grade: str | None = None
    percentage: float | None = None
    issue_date: date | None = None
    timestamp: datetime | None = None


class TypingSubmit(BaseModel):
    wpm: int
    accuracy: float
    time: int = 60
