from datetime import date

from flask_wtf import FlaskForm
from wtforms import DateField, HiddenField, IntegerField, PasswordField, RadioField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

from .questionnaire import QUESTION_DEFINITIONS, LIKERT_CHOICES


class PublicQuestionnaireForm(FlaskForm):
    first_name = StringField(
        "Nome",
        validators=[
            DataRequired(message="Informe seu nome."),
            Length(max=60, message="Use até 60 caracteres."),
        ],
    )
    last_name = StringField(
        "Sobrenome",
        validators=[
            DataRequired(message="Informe seu sobrenome."),
            Length(max=60, message="Use até 60 caracteres."),
        ],
    )
    questionnaire_date = DateField(
        "Data",
        validators=[DataRequired(message="Informe a data.")],
        default=date.today,
        format="%Y-%m-%d",
    )

    # 35 campos gerados dinamicamente com escala Likert 1-5
    question_1  = RadioField(validators=[DataRequired(message="Selecione uma alternativa.")], choices=LIKERT_CHOICES)
    question_2  = RadioField(validators=[DataRequired(message="Selecione uma alternativa.")], choices=LIKERT_CHOICES)
    question_3  = RadioField(validators=[DataRequired(message="Selecione uma alternativa.")], choices=LIKERT_CHOICES)
    question_4  = RadioField(validators=[DataRequired(message="Selecione uma alternativa.")], choices=LIKERT_CHOICES)
    question_5  = RadioField(validators=[DataRequired(message="Selecione uma alternativa.")], choices=LIKERT_CHOICES)
    question_6  = RadioField(validators=[DataRequired(message="Selecione uma alternativa.")], choices=LIKERT_CHOICES)
    question_7  = RadioField(validators=[DataRequired(message="Selecione uma alternativa.")], choices=LIKERT_CHOICES)
    question_8  = RadioField(validators=[DataRequired(message="Selecione uma alternativa.")], choices=LIKERT_CHOICES)
    question_9  = RadioField(validators=[DataRequired(message="Selecione uma alternativa.")], choices=LIKERT_CHOICES)
    question_10 = RadioField(validators=[DataRequired(message="Selecione uma alternativa.")], choices=LIKERT_CHOICES)
    question_11 = RadioField(validators=[DataRequired(message="Selecione uma alternativa.")], choices=LIKERT_CHOICES)
    question_12 = RadioField(validators=[DataRequired(message="Selecione uma alternativa.")], choices=LIKERT_CHOICES)
    question_13 = RadioField(validators=[DataRequired(message="Selecione uma alternativa.")], choices=LIKERT_CHOICES)
    question_14 = RadioField(validators=[DataRequired(message="Selecione uma alternativa.")], choices=LIKERT_CHOICES)
    question_15 = RadioField(validators=[DataRequired(message="Selecione uma alternativa.")], choices=LIKERT_CHOICES)
    question_16 = RadioField(validators=[DataRequired(message="Selecione uma alternativa.")], choices=LIKERT_CHOICES)
    question_17 = RadioField(validators=[DataRequired(message="Selecione uma alternativa.")], choices=LIKERT_CHOICES)
    question_18 = RadioField(validators=[DataRequired(message="Selecione uma alternativa.")], choices=LIKERT_CHOICES)
    question_19 = RadioField(validators=[DataRequired(message="Selecione uma alternativa.")], choices=LIKERT_CHOICES)
    question_20 = RadioField(validators=[DataRequired(message="Selecione uma alternativa.")], choices=LIKERT_CHOICES)
    question_21 = RadioField(validators=[DataRequired(message="Selecione uma alternativa.")], choices=LIKERT_CHOICES)
    question_22 = RadioField(validators=[DataRequired(message="Selecione uma alternativa.")], choices=LIKERT_CHOICES)
    question_23 = RadioField(validators=[DataRequired(message="Selecione uma alternativa.")], choices=LIKERT_CHOICES)
    question_24 = RadioField(validators=[DataRequired(message="Selecione uma alternativa.")], choices=LIKERT_CHOICES)
    question_25 = RadioField(validators=[DataRequired(message="Selecione uma alternativa.")], choices=LIKERT_CHOICES)
    question_26 = RadioField(validators=[DataRequired(message="Selecione uma alternativa.")], choices=LIKERT_CHOICES)
    question_27 = RadioField(validators=[DataRequired(message="Selecione uma alternativa.")], choices=LIKERT_CHOICES)
    question_28 = RadioField(validators=[DataRequired(message="Selecione uma alternativa.")], choices=LIKERT_CHOICES)
    question_29 = RadioField(validators=[DataRequired(message="Selecione uma alternativa.")], choices=LIKERT_CHOICES)
    question_30 = RadioField(validators=[DataRequired(message="Selecione uma alternativa.")], choices=LIKERT_CHOICES)
    question_31 = RadioField(validators=[DataRequired(message="Selecione uma alternativa.")], choices=LIKERT_CHOICES)
    question_32 = RadioField(validators=[DataRequired(message="Selecione uma alternativa.")], choices=LIKERT_CHOICES)
    question_33 = RadioField(validators=[DataRequired(message="Selecione uma alternativa.")], choices=LIKERT_CHOICES)
    question_34 = RadioField(validators=[DataRequired(message="Selecione uma alternativa.")], choices=LIKERT_CHOICES)
    question_35 = RadioField(validators=[DataRequired(message="Selecione uma alternativa.")], choices=LIKERT_CHOICES)

    submit = SubmitField("Enviar avaliação")

    @property
    def question_fields(self) -> list[RadioField]:
        return [getattr(self, f"question_{question['number']}") for question in QUESTION_DEFINITIONS]

    def build_answer_payloads(self) -> list[dict]:
        payloads = []
        for question in QUESTION_DEFINITIONS:
            field = getattr(self, f"question_{question['number']}")
            selected_value = field.data  # "1" .. "5"
            selected_text = dict(LIKERT_CHOICES)[selected_value]
            payloads.append(
                {
                    "question_number": question["number"],
                    "question_text": question["text"],
                    "selected_option": selected_value,
                    "selected_text": selected_text,
                }
            )
        return payloads


class AdminLoginForm(FlaskForm):
    username = StringField(
        "Usuário",
        validators=[DataRequired(message="Informe o usuário."), Length(max=64)],
        render_kw={"autocomplete": "username"},
    )
    password = PasswordField(
        "Senha",
        validators=[DataRequired(message="Informe a senha."), Length(min=8, max=128)],
        render_kw={"autocomplete": "current-password"},
    )
    submit = SubmitField("Entrar")


class CompanyForm(FlaskForm):
    name = StringField("Nome da Empresa", validators=[DataRequired(message="Informe o nome da empresa."), Length(max=120)])
    employee_count = IntegerField("Quantidade de Colaboradores", validators=[DataRequired(message="Informe a quantidade de colaboradores.")])
    hr_data = TextAreaField("Dados do RH", validators=[Length(max=1000)])
    submit = SubmitField("Salvar")
