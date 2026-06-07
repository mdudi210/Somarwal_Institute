from __future__ import annotations

import json
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..database import get_db
from ..mail import send_email
from ..models import Certificate, Course, Enquiry, Fee, Gallery, Notification, Placement, Result, Review, Student, User, Batch
from ..schemas import CertificateCreate, CertificateUpdate, CourseBase, GalleryCreate, ReviewCreate, BatchCreate, BatchUpdate
from ..security import require_admin


router = APIRouter(dependencies=[Depends(require_admin)])


def serialize_course(course: Course) -> dict:
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


def serialize_student(student: Student) -> dict:
    return {
        "id": student.id,
        "registration_no": student.registration_no,
        "student_name": student.student_name,
        "phone": student.phone,
        "status": student.status,
        "course_name": student.course.name if student.course else "",
        "receipt_no": student.fees[0].receipt_no if student.fees else "",
    }

def serialize_fee(fee: Fee) -> dict:
    return {
        "id": fee.id,
        "receipt_no": fee.receipt_no,
        "paid_amount": fee.paid_amount,
        "pending_amount": fee.pending_amount,
        "payment_mode": fee.payment_mode,
        "status": fee.status,
        "registration_no": fee.student.registration_no if fee.student else "",
        "course_name": fee.student.course.name if fee.student and fee.student.course else "",
    }


@router.get("/dashboard", response_model=None)
def dashboard(db: Session = Depends(get_db)) -> dict:
    revenue = db.query(func.coalesce(func.sum(Fee.paid_amount), 0)).filter(Fee.status == "APPROVED").scalar()
    pending = db.query(func.coalesce(func.sum(Fee.pending_amount), 0)).filter(Fee.status != "REJECTED").scalar()
    return {
        "metrics": {
            "students": db.query(Student).count(),
            "courses": db.query(Course).filter(Course.status.is_(True)).count(),
            "revenue": revenue,
            "pending": pending,
            "enquiries": db.query(Enquiry).filter(Enquiry.status == "NEW").count(),
            "certificates": db.query(Certificate).count(),
            "notifications": db.query(Notification).count(),
        },
        "students": [serialize_student(s) for s in db.query(Student).order_by(Student.id.desc()).limit(10).all()],
        "enquiries": db.query(Enquiry).order_by(Enquiry.id.desc()).limit(10).all(),
        "payments": [serialize_fee(f) for f in db.query(Fee).order_by(Fee.id.desc()).limit(10).all()],
        "notifications": db.query(Notification).order_by(Notification.id.desc()).limit(10).all(),
    }


@router.get("/students", response_model=None)
def students(db: Session = Depends(get_db)) -> list[Student]:
    return db.query(Student).order_by(Student.id.desc()).all()


@router.get("/students/{student_id}", response_model=None)
def get_student_details(student_id: int, db: Session = Depends(get_db)) -> dict:
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    total_paid = sum(f.paid_amount for f in student.fees if f.status == "APPROVED")
    pending_amount = max((student.course.fees if student.course else 0) - total_paid, 0)

    return {
        "profile": student,
        "course": student.course,
        "fees": student.fees,
        "certificates": student.certificates,
        "financials": {
            "total_paid": total_paid,
            "pending_amount": pending_amount
        }
    }


@router.post("/students/{student_id}/request-payment")
def request_payment(student_id: int, db: Session = Depends(get_db)) -> dict:
    from ..mail import send_email, send_whatsapp
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    total_paid = sum(f.paid_amount for f in student.fees if f.status == "APPROVED")
    pending = max((student.course.fees if student.course else 0) - total_paid, 0)
    
    if pending <= 0:
        return {"status": False, "message": "No pending amount"}
        
    msg = f"Dear {student.student_name}, you have a pending fee of Rs. {pending} for the course {student.course.name if student.course else ''}. Please log in to your student portal to complete the payment via QR."
    
    email_status = "SKIPPED"
    if student.email:
        success = send_email(student.email, "Pending Fee Reminder - Somarwal Institute", f"<p>{msg}</p>")
        email_status = "SENT" if success else "FAILED"
        
    wa_status = "QUEUED"
    if student.phone:
        wa_success = send_whatsapp(student.phone, msg)
        wa_status = "SENT" if wa_success else "FAILED"
        
    db.add(Notification(title="Payment Reminder", message=msg, receiver=student.phone or student.email or "unknown", send_type="WHATSAPP/EMAIL", status=f"E:{email_status} W:{wa_status}"))
    db.commit()
    
    return {"status": True, "message": "Payment request sent"}


@router.get("/courses")
def courses(db: Session = Depends(get_db)) -> list[dict]:
    return [serialize_course(course) for course in db.query(Course).order_by(Course.id.desc()).all()]


@router.post("/courses")
def create_course(payload: CourseBase, db: Session = Depends(get_db)) -> dict:
    if db.query(Course).filter(Course.code == payload.code).first():
        raise HTTPException(status_code=409, detail="Course code already exists")
    course = Course(
        **payload.model_dump(exclude={"syllabus", "software_covered", "career_options"}),
        syllabus=json.dumps(payload.syllabus),
        software_covered=json.dumps(payload.software_covered),
        career_options=json.dumps(payload.career_options),
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return serialize_course(course)


@router.put("/courses/{course_id}")
def update_course(course_id: int, payload: CourseBase, db: Session = Depends(get_db)) -> dict:
    course = db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    for key, value in payload.model_dump(exclude={"syllabus", "software_covered", "career_options"}).items():
        setattr(course, key, value)
    course.syllabus = json.dumps(payload.syllabus)
    course.software_covered = json.dumps(payload.software_covered)
    course.career_options = json.dumps(payload.career_options)
    db.commit()
    db.refresh(course)
    return serialize_course(course)


@router.delete("/courses/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)) -> dict:
    course = db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    course.status = False
    db.commit()
    return {"status": True, "message": "Course disabled"}


class TestEmailRequest(BaseModel):
    email: str


@router.post("/test-email")
def test_email(payload: TestEmailRequest, db: Session = Depends(get_db)):
    success = send_email(payload.email, "Test Email from Somarwal Institute", "<p>This is a test email sent from the admin dashboard to verify the Mailpit container integration.</p>")
    if success:
        return {"status": True, "message": "Email sent successfully"}
    raise HTTPException(status_code=500, detail="Failed to send email")


@router.post("/gallery")
def create_gallery(payload: GalleryCreate, db: Session = Depends(get_db)) -> dict:
    item = Gallery(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return {"status": True, "id": item.id}


@router.delete("/gallery/{gallery_id}")
def delete_gallery(gallery_id: int, db: Session = Depends(get_db)) -> dict:
    item = db.get(Gallery, gallery_id)
    if not item:
        raise HTTPException(status_code=404, detail="Gallery item not found")
    db.delete(item)
    db.commit()
    return {"status": True}


@router.post("/reviews")
def create_review(payload: ReviewCreate, db: Session = Depends(get_db)) -> dict:
    review = Review(**payload.model_dump())
    db.add(review)
    db.commit()
    db.refresh(review)
    return {"status": True, "id": review.id}


@router.delete("/reviews/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)) -> dict:
    review = db.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(review)
    db.commit()
    return {"status": True}


@router.post("/certificate/create")
def create_certificate(payload: CertificateCreate, db: Session = Depends(get_db)) -> dict:
    student = db.get(Student, payload.student_id)
    course = db.get(Course, payload.course_id)
    if not student or not course:
        raise HTTPException(status_code=404, detail="Student or course not found")
        
    certificate_no = payload.certificate_no or f"CERT{date.today().year}{db.query(Certificate).count() + 1:04d}"
    
    if db.query(Certificate).filter(Certificate.certificate_no == certificate_no).first():
        raise HTTPException(status_code=400, detail="Certificate ID already exists")
        
    certificate = Certificate(
        certificate_no=certificate_no,
        student_id=student.id,
        course_id=course.id,
        grade=payload.grade,
        percentage=payload.percentage,
        qr_code=f"/verify/{certificate_no}",
        pdf_url=f"/certificates/{certificate_no}.pdf",
    )
    db.add(certificate)
    db.commit()
    return {"status": True, "certificate_no": certificate_no}


@router.put("/certificate/{certificate_id}")
def update_certificate(certificate_id: int, payload: CertificateUpdate, db: Session = Depends(get_db)) -> dict:
    certificate = db.get(Certificate, certificate_id)
    if not certificate:
        raise HTTPException(status_code=404, detail="Certificate not found")
        
    if payload.certificate_no and payload.certificate_no != certificate.certificate_no:
        if db.query(Certificate).filter(Certificate.certificate_no == payload.certificate_no).first():
            raise HTTPException(status_code=400, detail="Certificate ID already exists")
        certificate.certificate_no = payload.certificate_no
        certificate.qr_code = f"/verify/{payload.certificate_no}"
        certificate.pdf_url = f"/certificates/{payload.certificate_no}.pdf"
        
    if payload.grade is not None:
        certificate.grade = payload.grade
    if payload.percentage is not None:
        certificate.percentage = payload.percentage
        
    db.commit()
    return {"status": True}


@router.post("/batches")
def create_batch(payload: BatchCreate, db: Session = Depends(get_db)) -> dict:
    batch = Batch(**payload.model_dump())
    db.add(batch)
    db.commit()
    db.refresh(batch)
    return {"status": True, "id": batch.id}


@router.get("/batches", response_model=None)
def get_batches(db: Session = Depends(get_db)) -> list[Batch]:
    return db.query(Batch).order_by(Batch.id.desc()).all()


@router.put("/batches/{batch_id}")
def update_batch(batch_id: int, payload: BatchUpdate, db: Session = Depends(get_db)) -> dict:
    batch = db.get(Batch, batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(batch, key, value)
    db.commit()
    return {"status": True}


@router.get("/content", response_model=None)
def content(db: Session = Depends(get_db)) -> dict:
    return {
        "gallery": db.query(Gallery).all(),
        "reviews": db.query(Review).all(),
        "placements": db.query(Placement).all(),
        "results": db.query(Result).all(),
        "notifications": db.query(Notification).all(),
        "users": db.query(User.id, User.name, User.email, User.role, User.status).all(),
    }


@router.put("/fees/{fee_id}/status")
def update_fee_status(fee_id: int, payload: dict, db: Session = Depends(get_db)) -> dict:
    from ..mail import send_email, send_whatsapp
    fee = db.get(Fee, fee_id)
    if not fee:
        raise HTTPException(status_code=404, detail="Fee not found")
    new_status = payload.get("status", "APPROVED")
    fee.status = new_status
    
    if new_status == "APPROVED" and fee.student:
        msg = f"Your payment of Rs. {fee.paid_amount} for receipt {fee.receipt_no} has been APPROVED. Somarwal Institute."
        email_status = "SKIPPED"
        if fee.student.email:
            success = send_email(fee.student.email, "Payment Approved - Somarwal Institute", f"<p>{msg}</p>")
            email_status = "SENT" if success else "FAILED"
        
        wa_status = "QUEUED"
        if fee.student.phone:
            wa_success = send_whatsapp(fee.student.phone, msg)
            wa_status = "SENT" if wa_success else "FAILED"
            
        db.add(Notification(title="Payment Approved", message=msg, receiver=fee.student.phone or fee.student.email or "unknown", send_type="WHATSAPP/EMAIL", status=f"E:{email_status} W:{wa_status}"))

    db.commit()
    return {"status": True, "message": "Fee status updated"}


