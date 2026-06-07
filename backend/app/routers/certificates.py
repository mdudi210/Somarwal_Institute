from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Certificate
from ..schemas import CertificateVerify


router = APIRouter()


@router.get("/verify/{certificate_no}", response_model=CertificateVerify)
def verify(certificate_no: str, db: Session = Depends(get_db)) -> CertificateVerify:
    certificate = db.query(Certificate).filter(Certificate.certificate_no == certificate_no).first()
    if not certificate or certificate.status != "ACTIVE":
        return CertificateVerify(verified=False, message="Fake Certificate Detected", timestamp=datetime.utcnow())
    return CertificateVerify(
        verified=True,
        student=certificate.student.student_name,
        course=certificate.course.name,
        grade=certificate.grade,
        percentage=certificate.percentage,
        issue_date=certificate.issue_date,
        timestamp=datetime.utcnow(),
    )
