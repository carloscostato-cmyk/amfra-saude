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
    return redirect(url_for("public.loading"))


@public_bp.get("/loading")
def loading():
    return render_template("loading_amfra.html")


@public_bp.route("/q/<company_token>", methods=["GET", "POST"])
def questionnaire(company_token):
    # Buscar pelo token individual do colaborador
    from .models import EmployeeToken
    employee_token = EmployeeToken.query.filter_by(token=company_token).first()
    
    if not employee_token:
        # Fallback: tentar buscar como token antigo da empresa (compatibilidade)
        company = Company.query.filter_by(token=company_token).first()
        if not company:
            flash("Link inválido ou expirado.", "error")
            return render_template("errors/404.html"), 404
    else:
        # Verificar se o token já foi usado
        if employee_token.used:
            flash(f"Este link já foi utilizado por {employee_token.employee_name} em {employee_token.used_at.strftime('%d/%m/%Y às %H:%M')}.", "warning")
            return render_template("thank_you.html", body_class="page-thank-you")
        
        company = employee_token.company
    
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
        
        # Marcar token como usado (se for token individual)
        if employee_token:
            employee_token.used = True
            employee_token.used_at = datetime.utcnow()
            employee_token.employee_name = f"{form.first_name.data.strip()} {form.last_name.data.strip()}"
        
        db.session.commit()

        return redirect(url_for("public.thank_you"))

    if form.is_submitted():
        # Identificar quais perguntas (1-35) estão sem resposta
        missing_questions = []
        for i in range(1, 36):
            field = getattr(form, f"question_{i}")
            if not field.data:
                missing_questions.append(str(i))
        
        if missing_questions:
            flash(f"Respostas obrigatórias pendentes. Clique nas perguntas faltantes: {', '.join(missing_questions)}", "danger")
        else:
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
