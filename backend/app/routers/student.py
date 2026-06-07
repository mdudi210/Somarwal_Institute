from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Result, Student, StudyMaterial, TypingResult, User
from ..schemas import TypingSubmit
from ..security import get_current_user


router = APIRouter()


def current_student(user: User, db: Session) -> Student:
    student = db.query(Student).filter(Student.user_id == user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    return student


@router.get("/dashboard", response_model=None)
def dashboard(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> dict:
    student = current_student(user, db)
    return {
        "profile": student,
        "course": student.course,
        "fees": student.fees,
        "certificates": student.certificates,
        "results": db.query(Result).filter(Result.student_id == student.id).all(),
        "materials": db.query(StudyMaterial).filter(StudyMaterial.course_id == student.course_id).all(),
        "attendance": {"present": 42, "absent": 3, "leave": 1},
    }


@router.get("/notes", response_model=None)
def notes(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[StudyMaterial]:
    student = current_student(user, db)
    return db.query(StudyMaterial).filter(StudyMaterial.course_id == student.course_id).all()


@router.get("/results", response_model=None)
def results(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[Result]:
    student = current_student(user, db)
    return db.query(Result).filter(Result.student_id == student.id).all()


@router.post("/typing/submit")
def typing_submit(payload: TypingSubmit, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> dict:
    student = current_student(user, db)
    rank = "Excellent" if payload.wpm >= 45 and payload.accuracy >= 95 else "Improving"
    result = TypingResult(student_id=student.id, wpm=payload.wpm, accuracy=payload.accuracy, time=payload.time, rank=rank)
    db.add(result)
    db.commit()
    return {"status": True, "rank": rank}


@router.post("/fees/pay-remaining")
def pay_remaining(payload: dict, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> dict:
    from datetime import date
    from ..models import Fee
    student = current_student(user, db)
    
    paid_amount = float(payload.get("paid_amount", 0))
    if paid_amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid amount")
        
    total_paid = sum(f.paid_amount for f in student.fees if f.status == "APPROVED")
    pending = max((student.course.fees if student.course else 0) - total_paid - paid_amount, 0)
    
    next_no = db.query(Fee).count() + 1
    receipt_no = f"RCP{date.today().year}{next_no:05d}"
    
    fee = Fee(
        student_id=student.id,
        total_amount=student.course.fees if student.course else 0,
        paid_amount=paid_amount,
        pending_amount=pending,
        payment_mode=payload.get("payment_mode", "UPI"),
        transaction_id=payload.get("transaction_id"),
        receipt_no=receipt_no,
        status="PENDING"
    )
    db.add(fee)
    db.commit()
    
    return {"status": True, "message": "Payment submitted for verification"}
