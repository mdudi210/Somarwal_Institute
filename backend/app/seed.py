from __future__ import annotations

import json
from datetime import date

from sqlalchemy.orm import Session

from .models import Certificate, Course, Fee, Gallery, Placement, Result, Review, Student, StudyMaterial, User
from .security import hash_password


def seed_database(db: Session) -> None:
    admin = db.query(User).filter(User.email == "admin@somarwal.edu").first()
    if not admin:
        admin = User(
            name="Somarwal Admin",
            email="admin@somarwal.edu",
            phone="9001090010",
            password_hash=hash_password("admin123456"),
            role="ADMIN",
        )
        db.add(admin)
    student_user = db.query(User).filter(User.email == "student@somarwal.edu").first()
    if not student_user:
        student_user = User(
            name="Priya Sharma",
            email="student@somarwal.edu",
            phone="9001090011",
            password_hash=hash_password("student123456"),
            role="STUDENT",
        )
        db.add(student_user)

    course_rows = [
        ("Basic Computer", "BASIC-COMP", "Computer Course", "2 Months", 4500, ["Computer fundamentals", "Windows", "Internet", "Email", "Printing and scanning"], ["Windows", "Chrome", "Gmail"], ["Computer beginner", "Office helper"]),
        ("MS Office", "MS-OFFICE", "Computer Course", "2 Months", 5500, ["MS Word", "MS Excel", "PowerPoint", "File management", "Office projects"], ["Word", "Excel", "PowerPoint"], ["Office assistant", "Data entry operator"]),
        ("Diploma in Computer Applications", "DCA", "Diploma Course", "6 Months", 12000, ["Computer fundamentals", "MS Word", "MS Excel", "PowerPoint", "Internet and email", "Typing practice", "AI productivity tools"], ["Windows", "MS Office", "Google Workspace", "Canva"], ["Computer operator", "Office assistant", "Data entry executive"]),
        ("Post Graduate Diploma in Computer Applications", "PGDCA", "Diploma Course", "1 Year", 24000, ["IT fundamentals", "Office automation", "Database", "Programming basics", "Web basics", "Project work"], ["MS Office", "LibreOffice", "MySQL", "VS Code"], ["Computer faculty", "MIS assistant", "Junior developer"]),
        ("Tally Prime with GST", "TALLY-GST", "Accounting", "3 Months", 8500, ["Accounting basics", "Company setup", "Vouchers", "GST", "Inventory", "Reports"], ["Tally Prime", "Excel"], ["Account assistant", "Billing executive", "GST operator"]),
        ("GST and ITR", "GST-ITR", "Accounting", "2 Months", 7500, ["GST registration", "GST returns", "E-way bills", "ITR basics", "Tax reports"], ["GST Portal", "Income Tax Portal", "Excel"], ["Tax assistant", "GST filing executive"]),
        ("Graphic Designing", "GRAPHIC", "Creative Course", "4 Months", 15000, ["Design principles", "Canva", "Photoshop", "CorelDRAW", "Branding project"], ["Canva", "Photoshop", "CorelDRAW"], ["Graphic designer", "Print designer"]),
        ("AI Course", "AI", "Career Course", "3 Months", 14000, ["AI fundamentals", "Prompt engineering", "AI productivity", "Image tools", "Automation projects"], ["ChatGPT", "Canva AI", "Google AI tools"], ["AI tools operator", "Productivity assistant"]),
        ("Typing Course", "TYPING", "Skill Course", "1 Month", 2500, ["Hindi typing", "English typing", "Speed drills", "Accuracy practice", "Typing test"], ["Typing Master", "Indic input tools"], ["Data entry operator", "Clerk exam candidate"]),
        ("Advance Excel Mastery", "ADV-EXCEL", "Accounting", "2 Months", 9000, ["Formulas", "Pivot tables", "Charts", "Dashboards", "MIS reports"], ["MS Excel", "Google Sheets"], ["MIS executive", "Data assistant"]),
        ("Spoken English", "SPOKEN-ENG", "Language Course", "3 Months", 6000, ["Grammar basics", "Vocabulary", "Conversation", "Interview practice", "Presentation"], ["Language lab", "Audio practice"], ["Customer support", "Front office executive"]),
        ("Video Editing", "VIDEO-EDIT", "Creative Course", "3 Months", 13000, ["Editing basics", "Transitions", "Audio sync", "Reels editing", "Final project"], ["Premiere Pro", "CapCut", "Canva"], ["Video editor", "Content creator"]),
        ("Hardware and Networking", "HW-NET", "Technical Course", "5 Months", 18000, ["PC assembly", "Troubleshooting", "Networking basics", "Router setup", "Maintenance"], ["Windows tools", "LAN tools"], ["Hardware technician", "Network support"]),
        ("Class 5th to 10th Coaching Classes", "COACHING-5-10", "Coaching Classes", "Academic Year", 10000, ["Maths", "Science", "English", "Computer basics", "Exam practice"], ["Smart classes", "Practice worksheets"], ["School performance improvement"]),
    ]
    courses = []
    for name, code, category, duration, fees, syllabus, software, careers in course_rows:
        course = db.query(Course).filter(Course.code == code).first()
        if not course:
            course = Course(
                name=name,
                code=code,
                category=category,
                duration=duration,
                fees=fees,
                description=f"{name} with practical training, certification guidance, and career-focused assignments.",
                syllabus=json.dumps(syllabus),
                software_covered=json.dumps(software),
                career_options=json.dumps(careers),
            )
            db.add(course)
        courses.append(course)
    for legacy_code in ("PY-AI", "GD-DM"):
        legacy_course = db.query(Course).filter(Course.code == legacy_code).first()
        if legacy_course:
            legacy_course.status = False
    db.flush()

    student = db.query(Student).filter(Student.registration_no == "SCI20260001").first()
    if not student:
        student = Student(
        registration_no="SCI20260001",
        user_id=student_user.id,
        student_name="Priya Sharma",
        father_name="Mahesh Sharma",
        dob=date(2005, 8, 12),
        qualification="12th",
        school_name="Ajmer Public School",
        phone="9001090011",
        email="student@somarwal.edu",
        address="Ajmer, Rajasthan",
        course_id=courses[0].id,
        admission_date=date(2026, 5, 20),
        )
        db.add(student)
        db.flush()

    if not db.query(Fee).filter(Fee.receipt_no == "RCP20260001").first():
        db.add(Fee(student_id=student.id, total_amount=12000, paid_amount=7000, pending_amount=5000, payment_mode="UPI", receipt_no="RCP20260001", receipt_pdf="/receipts/RCP20260001.pdf"))
    if not db.query(Certificate).filter(Certificate.certificate_no == "CERT1001").first():
        db.add(
            Certificate(
                certificate_no="CERT1001",
                student_id=student.id,
                course_id=courses[0].id,
                grade="A",
                percentage=91,
                issue_date=date(2026, 5, 20),
                qr_code="/verify/CERT1001",
                pdf_url="/certificates/CERT1001.pdf",
            )
        )
    if not db.query(Result).filter(Result.student_id == student.id).first():
        db.add(Result(student_id=student.id, exam_name="DCA Final Practical", marks=91, percentage=91, grade="A"))
    if not db.query(StudyMaterial).filter(StudyMaterial.course_id == courses[0].id).first():
        db.add_all([
            StudyMaterial(course_id=courses[0].id, title="Excel Practice Workbook", type="PDF", file_url="/materials/excel-practice.pdf"),
            StudyMaterial(course_id=courses[0].id, title="Typing Speed Drill", type="NOTES", file_url="/materials/typing-drill.pdf"),
        ])

    images = [
        ("Modern Computer Lab", "Labs", "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=1200&q=80"),
        ("Certificate Ceremony", "Awards", "https://images.unsplash.com/photo-1523580846011-d3a5bc25702b?auto=format&fit=crop&w=1200&q=80"),
        ("Practical Training Session", "Events", "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1200&q=80"),
    ]
    for title, category, image in images:
        if not db.query(Gallery).filter(Gallery.title == title).first():
            db.add(Gallery(title=title, category=category, image=image))
    if not db.query(Review).first():
        db.add_all([
            Review(student_name="Aman Khan", course="Tally Prime with GST", rating=5, message="Practical GST entries and reports helped me get billing work quickly."),
            Review(student_name="Neha Soni", course="DCA", rating=5, message="The classes were simple, disciplined, and focused on real computer practice."),
        ])
    if not db.query(Placement).first():
        db.add_all([
            Placement(student_name="Rahul Meena", course="DCA", company="Ajmer Digital Services", package="2.4 LPA", description="Placed as junior computer operator."),
            Placement(student_name="Kavita Bairwa", course="Tally Prime with GST", company="Sharma Accounts", package="Internship", description="Selected for accounting internship after course completion."),
        ])
    db.commit()
