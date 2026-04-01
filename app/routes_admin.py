import secrets
from datetime import datetime
from typing import Optional
from urllib.parse import urlparse

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import func

from .extensions import db
from .forms import AdminLoginForm, CompanyForm
from .models import AdminUser, Company, Employee, Submission
from .questionnaire import QUESTION_DEFINITIONS
from .services import CLASSIFICATION_RULES, NR1StudyAgent
from .services.links import build_public_questionnaire_url


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

QUESTION_TOPICS = {
    1: "Cargo",           2: "Controle",          3: "Demandas",
    4: "Cargo",           5: "Relacionamentos",    6: "Demandas",
    7: "Apoio dos Colegas", 8: "Apoio da Chefia",  9: "Demandas",
    10: "Controle",       11: "Cargo",            12: "Demandas",
    13: "Cargo",          14: "Relacionamentos",   15: "Controle",
    16: "Demandas",       17: "Cargo",            18: "Demandas",
    19: "Controle",       20: "Demandas",          21: "Relacionamentos",
    22: "Demandas",       23: "Apoio da Chefia",   24: "Apoio dos Colegas",
    25: "Controle",       26: "Comunicação e Mudanças", 27: "Apoio dos Colegas",
    28: "Comunicação e Mudanças", 29: "Apoio da Chefia", 30: "Controle",
    31: "Apoio dos Colegas", 32: "Comunicação e Mudanças", 33: "Apoio da Chefia",
    34: "Relacionamentos", 35: "Apoio da Chefia",
}

SCORE_INTENSITY_LABELS = {
    1: "Nunca",
    2: "Raramente",
    3: "Às vezes",
    4: "Frequentemente",
    5: "Sempre",
}


def _is_safe_redirect_target(target: Optional[str]) -> bool:
    if not target:
        return False
    parsed_target = urlparse(target)
    return parsed_target.scheme == "" and parsed_target.netloc == ""


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))

    form = AdminLoginForm()
    if form.validate_on_submit():
        user = AdminUser.query.filter_by(username=form.username.data.strip()).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Login realizado com segurança.", "success")
            next_url = request.args.get("next")
            if _is_safe_redirect_target(next_url):
                return redirect(next_url)
            return redirect(url_for("admin.dashboard"))

        flash("Usuário ou senha inválidos.", "error")

    return render_template("admin_login.html", form=form, body_class="page-admin-login")


@admin_bp.post("/logout")
@login_required
def logout():
    logout_user()
    flash("Sessão encerrada.", "info")
    return redirect(url_for("admin.login"))


@admin_bp.get("/")
@login_required
def dashboard():
    return redirect(url_for("admin.company_list"))


@admin_bp.route("/companies", methods=["GET"])
@login_required
def company_list():
    companies = Company.query.order_by(Company.created_at.desc()).all()
    for company in companies:
        company.public_url = build_public_questionnaire_url(company)
    return render_template(
        "admin_dashboard.html",
        companies=companies,
        body_class="page-admin-dashboard",
    )


@admin_bp.route("/company/new", methods=["GET", "POST"])
@login_required
def company_new():
    form = CompanyForm()
    if form.validate_on_submit():
        token = secrets.token_urlsafe(16)
        company = Company(
            name=form.name.data.strip(),
            employee_count=form.employee_count.data,
            hr_data=form.hr_data.data,
            token=token,
        )
        db.session.add(company)
        db.session.flush()  # Garante que company.id está disponível
        
        # Gerar tokens individuais para cada colaborador
        from .models import EmployeeToken
        for i in range(form.employee_count.data):
            employee_token = EmployeeToken(
                company_id=company.id,
                token=secrets.token_urlsafe(16)
            )
            db.session.add(employee_token)
        
        db.session.commit()
        flash(f"Empresa cadastrada com sucesso. {form.employee_count.data} tokens individuais foram gerados.", "success")
        return redirect(url_for("admin.company_detail", company_id=company.id))

    return render_template("admin_company_form.html", form=form, title="Nova Empresa", body_class="page-admin-dashboard")


@admin_bp.route("/company/<int:company_id>", methods=["GET"])
@login_required
def company_detail(company_id):
    from .models import EmployeeToken
    company = Company.query.get_or_404(company_id)
    public_url = build_public_questionnaire_url(company)
    employees = Employee.query.filter_by(company_id=company.id).all()
    
    # Buscar todos os tokens individuais
    employee_tokens = EmployeeToken.query.filter_by(company_id=company.id).order_by(EmployeeToken.created_at).all()
    
    # Calcular estatísticas
    tokens_used = sum(1 for t in employee_tokens if t.used)
    tokens_available = len(employee_tokens) - tokens_used
    
    return render_template(
        "admin_company_detail.html",
        company=company,
        employees=employees,
        public_url=public_url,
        employee_tokens=employee_tokens,
        tokens_used=tokens_used,
        tokens_available=tokens_available,
        body_class="page-admin-dashboard",
    )


@admin_bp.route("/company/<int:company_id>/nr1", methods=["GET"])
@login_required
def company_nr1_report(company_id):
    agent = NR1StudyAgent(company_id)
    report = agent.run_study()
    return render_template(
        "admin_company_nr1.html",
        company=agent.company,
        report=report,
        body_class="page-admin-dashboard",
    )


@admin_bp.route("/company/delete/<int:company_id>", methods=["POST"])
@login_required
def company_delete(company_id):
    company = Company.query.get_or_404(company_id)
    # Deletar todos os sub-registros (Employees e Submissions) se necessário
    # Dependendo da configuração do DB (cascading), isso pode ser automático.
    # Aqui deletamos a empresa e o SQLAlchemy cuida do resto se os relacionamentos estiverem corretos.
    db.session.delete(company)
    db.session.commit()
    flash(f"Empresa '{company.name}' e todos os seus dados foram excluídos permanentemente.", "success")
    return redirect(url_for('admin.company_list'))


@admin_bp.get("/submissions/<int:submission_id>")
@login_required
def submission_detail(submission_id):
    submission = Submission.query.get_or_404(submission_id)

    question_lookup = {question["number"]: question["text"] for question in QUESTION_DEFINITIONS}
    chart_points = [
        {
            "label": f"Pergunta {answer.question_number}",
            "short_label": QUESTION_TOPICS.get(answer.question_number, f"Pergunta {answer.question_number}"),
            "question_number": answer.question_number,
            "score": answer.score,
            "question": question_lookup.get(answer.question_number, answer.question_text),
            "intensity": SCORE_INTENSITY_LABELS.get(answer.score, "Observação"),
        }
        for answer in submission.answers
    ]

    top_indicators = sorted(
        chart_points,
        key=lambda item: (item["score"], item["question_number"]),
        reverse=True,
    )[:3]

    detail_metrics = {
        "average_score": round(submission.total_score / len(chart_points), 1) if chart_points else 0,
        "items_requiring_attention": sum(1 for item in chart_points if item["score"] >= 4),
        "highest_score_count": sum(1 for item in chart_points if item["score"] == 5),
    }

    return render_template(
        "admin_submission_detail.html",
        submission=submission,
        detail_url=request.url,
        chart_points=chart_points,
        detail_metrics=detail_metrics,
        top_indicators=top_indicators,
        body_class="page-admin-detail",
    )


@admin_bp.get("/submissions/<int:submission_id>/advanced")
@login_required
def submission_detail_advanced(submission_id):
    submission = Submission.query.get_or_404(submission_id)

    question_lookup = {question["number"]: question["text"] for question in QUESTION_DEFINITIONS}
    chart_points = [
        {
            "label": f"Pergunta {answer.question_number}",
            "short_label": QUESTION_TOPICS.get(answer.question_number, f"Pergunta {answer.question_number}"),
            "question_number": answer.question_number,
            "score": answer.score,
            "question": question_lookup.get(answer.question_number, answer.question_text),
            "intensity": SCORE_INTENSITY_LABELS.get(answer.score, "Observação"),
        }
        for answer in submission.answers
    ]

    top_indicators = sorted(
        chart_points,
        key=lambda item: (item["score"], item["question_number"]),
        reverse=True,
    )[:3]

    detail_metrics = {
        "average_score": round(submission.total_score / len(chart_points), 1) if chart_points else 0,
        "items_requiring_attention": sum(1 for item in chart_points if item["score"] >= 4),
        "highest_score_count": sum(1 for item in chart_points if item["score"] == 5),
    }

    return render_template(
        "admin_submission_detail_NOVO.html",
        submission=submission,
        detail_url=request.url,
        chart_points=chart_points,
        detail_metrics=detail_metrics,
        top_indicators=top_indicators,
        body_class="page-admin-detail-advanced",
    )


@admin_bp.get("/migrate")
@login_required
def migrate_database():
    """Rota temporária para executar migração do banco de dados"""
    from app.models import EmployeeToken
    from sqlalchemy import inspect
    
    try:
        # Criar tabela employee_tokens
        db.create_all()
        
        # Verificar se a tabela foi criada
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        if 'employee_tokens' in tables:
            columns = [col['name'] for col in inspector.get_columns('employee_tokens')]
            flash(f"✅ Migração concluída! Tabela 'employee_tokens' criada com colunas: {', '.join(columns)}", "success")
        else:
            flash("❌ Erro: Tabela 'employee_tokens' não foi criada!", "error")
            
    except Exception as e:
        flash(f"❌ Erro na migração: {str(e)}", "error")
    
    return redirect(url_for("admin.company_list"))

