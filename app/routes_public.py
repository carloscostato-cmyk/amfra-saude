from flask import Blueprint, current_app, flash, redirect, render_template, url_for, jsonify
from flask_login import current_user

from .extensions import db
from .forms import PublicQuestionnaireForm
from .models import Answer, Company, Employee, Submission
from .questionnaire import QUESTION_DEFINITIONS
from .services import evaluate_submission


public_bp = Blueprint("public", __name__)


@public_bp.get("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))
    return redirect(url_for("admin.login"))


@public_bp.route("/q/<company_token>", methods=["GET", "POST"])
def questionnaire(company_token):
    company = Company.query.filter_by(token=company_token).first_or_404()
    form = PublicQuestionnaireForm()
    question_pairs = list(zip(QUESTION_DEFINITIONS, form.question_fields))

    if form.validate_on_submit():
        existing_emp = Employee.query.filter(
            Employee.company_id == company.id,
            Employee.first_name.ilike(form.first_name.data.strip()),
            Employee.last_name.ilike(form.last_name.data.strip())
        ).first()

        if existing_emp and existing_emp.submissions:
            flash("Você já respondeu a este questionário.", "warning")
            return redirect(url_for("public.questionnaire", company_token=company_token))

        if not existing_emp:
            existing_emp = Employee(
                company_id=company.id,
                first_name=form.first_name.data.strip(),
                last_name=form.last_name.data.strip(),
            )
            db.session.add(existing_emp)
            db.session.flush()

        evaluation = evaluate_submission(form.build_answer_payloads())

        submission = Submission(
            employee_id=existing_emp.id,
            questionnaire_date=form.questionnaire_date.data,
            total_score=evaluation.total_score,
            classification=evaluation.classification,
            interpretation=evaluation.interpretation,
        )

        for answer in evaluation.answers:
            submission.answers.append(
                Answer(
                    question_number=answer["question_number"],
                    question_text=answer["question_text"],
                    selected_option=answer["selected_option"],
                    selected_text=answer["selected_text"],
                    score=answer["score"],
                )
            )

        db.session.add(submission)
        db.session.commit()

        return redirect(url_for("public.thank_you"))

    if form.is_submitted():
        flash("Revise os campos destacados antes de enviar a avaliação.", "warning")

    return render_template(
        "public_form.html",
        form=form,
        company=company,
        question_pairs=question_pairs,
        body_class="page-public-form",
    )


@public_bp.get("/obrigado")
def thank_you():
    return render_template(
        "thank_you.html",
        body_class="page-thank-you",
    )


@public_bp.get("/health")
def health():
    return jsonify(status="ok", app=current_app.config.get("APP_NAME")), 200
