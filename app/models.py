from datetime import datetime
import uuid

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db


class AdminUser(UserMixin, db.Model):
    __tablename__ = "admin_users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Company(db.Model):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    employee_count = db.Column(db.Integer, nullable=False, default=0)
    hr_data = db.Column(db.Text, nullable=True)
    token = db.Column(db.String(64), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    employees = db.relationship("Employee", back_populates="company", cascade="all, delete-orphan")


class Employee(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False, index=True)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    company = db.relationship("Company", back_populates="employees")
    submissions = db.relationship("Submission", back_populates="employee", cascade="all, delete-orphan")


class Submission(db.Model):
    __tablename__ = "submissions"

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False, index=True, unique=True)
    questionnaire_date = db.Column(db.Date, nullable=False, index=True)
    total_score = db.Column(db.Integer, nullable=False)
    classification = db.Column(db.String(120), nullable=False, index=True)
    interpretation = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)

    employee = db.relationship("Employee", back_populates="submissions")
    answers = db.relationship(
        "Answer",
        back_populates="submission",
        cascade="all, delete-orphan",
        order_by="Answer.question_number",
    )


class Answer(db.Model):
    __tablename__ = "answers"

    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey("submissions.id"), nullable=False, index=True)
    question_number = db.Column(db.Integer, nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    selected_option = db.Column(db.String(1), nullable=False)
    selected_text = db.Column(db.Text, nullable=False)
    score = db.Column(db.Integer, nullable=False)

    submission = db.relationship("Submission", back_populates="answers")
