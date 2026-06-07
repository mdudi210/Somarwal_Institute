from __future__ import annotations

import json
from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..database import get_db
from ..mail import send_email
from ..models import Certificate, Course, Enquiry, Fee, Gallery, Notification, Placement, Review, Student
from ..schemas import AdmissionCreate, AdmissionResponse, EnquiryCreate, SendPhoneOTPRequest


router = APIRouter()


def course_to_dict(course: Course) -> dict:
    return {
        "id": course.id,
        "name": course.name,
        "code": course.code,
        "category": course.category,
        "duration": course.duration,
        "fees": course.fees,
        "description": course.description,
        "syllabus": json.loads(course.syllabus or "[]"),
        "software_covered": json.loads(course.software_covered or "[]"),
        "career_options": json.loads(course.career_options or "[]"),
        "certificate_available": course.certificate_available,
        "status": course.status,
    }


def gallery_to_dict(item: Gallery) -> dict:
    return {"id": item.id, "title": item.title, "image": item.image, "category": item.category}


def review_to_dict(item: Review) -> dict:
    return {"id": item.id, "student_name": item.student_name, "course": item.course, "rating": item.rating, "message": item.message, "photo": item.photo}


def placement_to_dict(item: Placement) -> dict:
    return {"id": item.id, "student_name": item.student_name, "course": item.course, "company": item.company, "package": item.package, "photo": item.photo, "description": item.description}


from ..security import get_current_user
from ..models import User

@router.get("/home")
def home(db: Session = Depends(get_db)) -> dict:
    courses = db.query(Course).filter(Course.status.is_(True)).all()
    return {
        "announcements": [
            {"title": "Admission Open 2026", "message": "New batches for DCA, Tally, AI, Excel, and Coaching are open now.", "action": "Apply Now"},
            {"title": "Scholarship Exam", "message": "Register for the institute scholarship test and earn fee benefits.", "action": "Free Demo Class"},
        ],
        "about": {
            "mission": "Deliver affordable, practical, job-oriented computer education in Ajmer.",
            "vision": "Build a confident generation of digitally skilled students, professionals, and entrepreneurs.",
            "director_message": "Our institute focuses on discipline, hands-on practice, and guidance that helps every learner move forward.",
        },
        "stats": {
            "students": db.query(Student).count(),
            "courses": db.query(Course).filter(Course.status.is_(True)).count(),
            "placements": db.query(Placement).count(),
            "certificates": db.query(Certificate).count(),
        },
        "courses": [course_to_dict(course) for course in courses],
        "gallery": [gallery_to_dict(item) for item in db.query(Gallery).limit(6).all()],
        "reviews": [review_to_dict(item) for item in db.query(Review).filter(Review.approved.is_(True)).limit(8).all()],
        "placements": [placement_to_dict(item) for item in db.query(Placement).limit(6).all()],
    }


@router.get("/courses")
def courses(db: Session = Depends(get_db)) -> list[dict]:
    return [course_to_dict(course) for course in db.query(Course).filter(Course.status.is_(True)).all()]


@router.get("/courses/{code}")
def course_detail(code: str, db: Session = Depends(get_db)) -> dict:
    course = db.query(Course).filter(func.lower(Course.code) == code.lower()).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course_to_dict(course)


@router.get("/courses/{code}/batches")
def course_batches(code: str, db: Session = Depends(get_db)) -> list[dict]:
    from ..models import Batch
    course = db.query(Course).filter(func.lower(Course.code) == code.lower()).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    batches = db.query(Batch).filter(Batch.course_id == course.id, Batch.status.in_(["UPCOMING", "ACTIVE"])).all()
    return [{"id": b.id, "batch_no": b.batch_no, "start_date": b.start_date.isoformat(), "end_date": b.end_date.isoformat(), "status": b.status} for b in batches]


@router.post("/admission/apply", response_model=AdmissionResponse)
def apply(payload: AdmissionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> AdmissionResponse:
    from ..mail import send_whatsapp
    import re
    from ..models import Batch

    course = db.query(Course).filter((Course.code == payload.course) | (Course.name == payload.course)).first()
    if not course:
        raise HTTPException(status_code=404, detail="Selected course not found")
        
    batch = db.get(Batch, payload.batch_id)
    if not batch or batch.course_id != course.id:
        raise HTTPException(status_code=400, detail="Invalid batch selected for this course")
    if batch.status not in ["UPCOMING", "ACTIVE"]:
        raise HTTPException(status_code=400, detail="Selected batch is no longer accepting admissions")

    existing_enrollment = db.query(Student).filter(Student.user_id == current_user.id, Student.course_id == course.id, Student.status == "ACTIVE").first()
    if existing_enrollment:
        raise HTTPException(status_code=400, detail="You are already actively enrolled in this course. You cannot enroll again.")

    has_pending = db.query(Fee).join(Student).filter(Student.user_id == current_user.id, Fee.pending_amount > 0).first()
    if has_pending:
        raise HTTPException(status_code=400, detail="You cannot apply for a new course until you clear your pending dues.")


    if payload.payment_mode == "UPI":
        if not payload.transaction_id or not re.match(r"^\d{12}$", payload.transaction_id):
            raise HTTPException(status_code=400, detail="Invalid UPI Transaction ID. It must be a 12-digit number.")
        if db.query(Fee).filter(Fee.transaction_id == payload.transaction_id).first():
            raise HTTPException(status_code=400, detail="Transaction ID has already been used.")

    next_no = db.query(Student).count() + 1
    registration_no = f"SCI{date.today().year}{next_no:04d}"
    receipt_no = f"RCP{date.today().year}{next_no:04d}"
    paid_amount = payload.paid_amount or 0
    if paid_amount < 1000:
        raise HTTPException(status_code=400, detail="Minimum payment of 1000 is required for admission.")
    pending = max(course.fees - paid_amount, 0)
    student = Student(
        registration_no=registration_no,
        user_id=current_user.id,
        student_name=payload.name,
        father_name=payload.father,
        dob=payload.dob,
        qualification=payload.qualification,
        school_name=payload.school_name,
        phone=payload.phone,
        email=payload.email,
        address=payload.address,
        course_id=course.id,
        batch_id=batch.id,
    )
    db.add(student)
    db.flush()
    receipt_url = f"/receipts/{receipt_no}.pdf"
    db.add(Fee(student_id=student.id, total_amount=course.fees, paid_amount=paid_amount, pending_amount=pending, payment_mode=payload.payment_mode, transaction_id=payload.transaction_id, receipt_no=receipt_no, receipt_pdf=receipt_url))
    
    email_status = "SKIPPED"
    if payload.email:
        subject = "Admission Confirmation - Somarwal Institute"
        content = f"<h3>Dear {payload.name},</h3><p>Your admission for {course.name} is confirmed!</p><p>Registration No: {registration_no}</p>"
        success = send_email(payload.email, subject, content)
        email_status = "SENT" if success else "FAILED"

    whatsapp_status = "QUEUED"
    if payload.phone:
        msg = f"Dear {payload.name}, your Somarwal registration number is {registration_no}. Course: {course.name}."
        wa_success = send_whatsapp(payload.phone, msg)
        whatsapp_status = "SENT" if wa_success else "FAILED"

    db.add_all([
        Notification(title="Admission Confirmation", message=f"Registration {registration_no} created for {course.name}. Receipt {receipt_no}.", receiver=payload.email or "not-provided", send_type="EMAIL", status=email_status),
        Notification(title="WhatsApp Admission Confirmation", message=f"Dear {payload.name}, your Somarwal registration number is {registration_no}.", receiver=payload.phone, send_type="WHATSAPP", status=whatsapp_status),
    ])
    db.commit()
    db.refresh(student)
    return AdmissionResponse(
        registration_no=registration_no,
        receipt=f"{receipt_no}.pdf",
        receipt_url=receipt_url,
        student_id=student.id,
        pending_amount=pending,
        email_notification=email_status,
        whatsapp_notification=whatsapp_status,
    )


@router.post("/enquiries")
def create_enquiry(payload: EnquiryCreate, db: Session = Depends(get_db)) -> dict[str, bool | int]:
    enquiry = Enquiry(**payload.model_dump())
    db.add(enquiry)
    db.commit()
    db.refresh(enquiry)
    return {"status": True, "id": enquiry.id}
