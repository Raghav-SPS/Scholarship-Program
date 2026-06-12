from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from decimal import Decimal

db = SQLAlchemy()

class Scholarship(db.Model):
    """Scholarship fund model"""
    __tablename__ = 'scholarships'

    id = db.Column(db.Integer, primary_key=True)
    sort_name = db.Column(db.String(50), unique=True, nullable=False)  # e.g., 'AIS'
    official_name = db.Column(db.String(255), nullable=False)
    account_number = db.Column(db.String(50))
    ug_eligible = db.Column(db.Boolean, default=False)
    ms_eligible = db.Column(db.Boolean, default=False)
    fall_award = db.Column(db.Boolean, default=True)
    spring_award = db.Column(db.Boolean, default=True)
    restrictions = db.Column(db.Text)  # Free text restrictions
    available_amount = db.Column(db.Numeric(10, 2), default=0)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    awards = db.relationship('Award', backref='scholarship', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Scholarship {self.sort_name}: {self.official_name}>'


class Student(db.Model):
    """Student applicant model"""
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    gpa = db.Column(db.Numeric(3, 2))
    program_level = db.Column(db.String(10), nullable=False)  # 'UG' or 'MS'
    financial_need = db.Column(db.String(1))  # 'H', 'M', 'L'
    permanent_address = db.Column(db.Text)

    # Employer/firm associations
    permanent_position_at = db.Column(db.String(255))  # e.g., 'Deloitte'
    internship_2025_at = db.Column(db.String(255))
    internship_2026_at = db.Column(db.String(255))

    score = db.relationship('Score', backref='student', lazy=True, uselist=False, cascade='all, delete-orphan')
    awards = db.relationship('Award', backref='student', lazy=True, cascade='all, delete-orphan')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Student {self.first_name} {self.last_name}>'

    def full_name(self):
        name = f"{self.first_name}"
        if self.middle_name:
            name += f" {self.middle_name}"
        name += f" {self.last_name}"
        return name


class Application(db.Model):
    """Student application data"""
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False, unique=True)

    # Raw application responses
    extracurricular_activities = db.Column(db.Text)
    college_activities = db.Column(db.Text)
    work_experience = db.Column(db.Text)

    # Structured parsed data
    activities_parsed = db.Column(db.JSON)  # List of activity entries with dates
    work_parsed = db.Column(db.JSON)  # List of work entries with dates/roles

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = db.relationship('Student', backref='application', lazy=True)

    def __repr__(self):
        return f'<Application for Student {self.student_id}>'


class Score(db.Model):
    """Calculated score for a student"""
    __tablename__ = 'scores'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False, unique=True)

    # Component scores
    accounting_experience_score = db.Column(db.Numeric(5, 2), default=0)
    work_experience_score = db.Column(db.Numeric(5, 2), default=0)
    leadership_score = db.Column(db.Numeric(5, 2), default=0)

    # Final score
    total_score = db.Column(db.Numeric(5, 2), default=0)

    # Metadata
    rubric_type = db.Column(db.String(10))  # 'UG' or 'MS'
    scoring_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Score Student {self.student_id}: {self.total_score}>'


class Award(db.Model):
    """Scholarship award assignment"""
    __tablename__ = 'awards'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    scholarship_id = db.Column(db.Integer, db.ForeignKey('scholarships.id'), nullable=False)

    amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'approved', 'rejected', 'notified'

    # Admin actions
    admin_notes = db.Column(db.Text)
    approved_by = db.Column(db.String(100))
    approved_at = db.Column(db.DateTime)

    # Notification
    email_sent_at = db.Column(db.DateTime)
    email_sent_to = db.Column(db.String(120))
    email_status = db.Column(db.String(20), default='not_sent')  # 'not_sent', 'sent', 'failed'
    email_error_message = db.Column(db.Text)  # Capture reason if email fails

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Award Student {self.student_id} - {self.amount} from {self.scholarship_id}>'


class ApplicationFile(db.Model):
    """Track uploaded application files"""
    __tablename__ = 'application_files'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    upload_path = db.Column(db.String(500), nullable=False)
    num_students = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='processing')  # 'processing', 'success', 'error'
    error_message = db.Column(db.Text)
    uploaded_by = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime)

    def __repr__(self):
        return f'<ApplicationFile {self.filename}>'
