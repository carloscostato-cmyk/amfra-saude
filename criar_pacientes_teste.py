"""Script para criar pacientes de teste no banco de dados"""
import sys
from datetime import date
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from app import create_app
from app.extensions import db
from app.models import Answer, Submission
from app.services import evaluate_submission, generate_admin_access_token, generate_submission_uuid

app = create_app()

with app.app_context():
    # Paciente 1: Caso Crítico
    print("Criando Paciente 1: Caso Crítico...")
    
    answers_patient1 = [
        {"question_number": 1, "question_text": "Como você se sente emocionalmente quando está perto do seu parceiro(a)?", "selected_option": "D", "selected_text": "Constantemente me sinto inferior ou sem valor"},
        {"question_number": 2, "question_text": "Seu parceiro(a) assume responsabilidade quando comete erros?", "selected_option": "D", "selected_text": "Nunca admite — sempre coloca a culpa em mim"},
        {"question_number": 3, "question_text": "Com que frequência seu parceiro(a) faz críticas negativas sobre você?", "selected_option": "D", "selected_text": "Constantemente me humilha ou diminui"},
        {"question_number": 4, "question_text": "Seu parceiro(a) demonstra empatia com seus sentimentos e necessidades?", "selected_option": "D", "selected_text": "Nunca demonstra empatia — ridiculariza ou ignora"},
        {"question_number": 5, "question_text": "Você sente que suas necessidades são consideradas no relacionamento?", "selected_option": "D", "selected_text": "Nunca — meu parceiro(a) é o centro absoluto"},
        {"question_number": 6, "question_text": "Seu parceiro(a) já tentou afastá-lo(a) de amigos ou familiares?", "selected_option": "D", "selected_text": "Totalmente me isolou das pessoas próximas"},
        {"question_number": 7, "question_text": "Como você descreveria a comunicação no seu relacionamento?", "selected_option": "D", "selected_text": "Ele(a) distorce a realidade e controla as conversas"},
        {"question_number": 8, "question_text": "Seu parceiro(a) já fez você duvidar da sua própria memória ou percepção da realidade (gaslighting)?", "selected_option": "D", "selected_text": "Constantemente questiono minha própria sanidade"},
        {"question_number": 9, "question_text": "Como está sua autoestima desde que está nesse relacionamento?", "selected_option": "D", "selected_text": "Muito pior — sinto que perdi minha identidade"},
        {"question_number": 10, "question_text": "Você já sentiu medo da reação emocional ou comportamental do seu parceiro(a)?", "selected_option": "D", "selected_text": "Sempre — ando na ponta dos pés com medo"},
    ]
    
    evaluation1 = evaluate_submission(answers_patient1)
    
    submission1 = Submission(
        uuid=generate_submission_uuid(),
        admin_url_token=generate_admin_access_token(),
        patient_name="Maria Silva",
        questionnaire_date=date.today(),
        total_score=evaluation1.total_score,
        classification=evaluation1.classification,
        interpretation=evaluation1.interpretation,
        notification_status="pending",
    )
    
    for answer in evaluation1.answers:
        submission1.answers.append(
            Answer(
                question_number=answer["question_number"],
                question_text=answer["question_text"],
                selected_option=answer["selected_option"],
                selected_text=answer["selected_text"],
                score=answer["score"],
            )
        )
    
    db.session.add(submission1)
    
    # Paciente 2: Caso Saudável
    print("Criando Paciente 2: Caso Saudável...")
    
    answers_patient2 = [
        {"question_number": 1, "question_text": "Como você se sente emocionalmente quando está perto do seu parceiro(a)?", "selected_option": "A", "selected_text": "Seguro(a), valorizado(a) e respeitado(a)"},
        {"question_number": 2, "question_text": "Seu parceiro(a) assume responsabilidade quando comete erros?", "selected_option": "A", "selected_text": "Sempre assume e pede desculpas sinceramente"},
        {"question_number": 3, "question_text": "Com que frequência seu parceiro(a) faz críticas negativas sobre você?", "selected_option": "A", "selected_text": "Raramente ou nunca me critica de forma negativa"},
        {"question_number": 4, "question_text": "Seu parceiro(a) demonstra empatia com seus sentimentos e necessidades?", "selected_option": "A", "selected_text": "Sempre demonstra compreensão genuína"},
        {"question_number": 5, "question_text": "Você sente que suas necessidades são consideradas no relacionamento?", "selected_option": "A", "selected_text": "Sim, há equilíbrio e reciprocidade"},
        {"question_number": 6, "question_text": "Seu parceiro(a) já tentou afastá-lo(a) de amigos ou familiares?", "selected_option": "A", "selected_text": "Nunca — meu círculo social é respeitado"},
        {"question_number": 7, "question_text": "Como você descreveria a comunicação no seu relacionamento?", "selected_option": "B", "selected_text": "Geralmente boa, com alguns conflitos pontuais"},
        {"question_number": 8, "question_text": "Seu parceiro(a) já fez você duvidar da sua própria memória ou percepção da realidade (gaslighting)?", "selected_option": "A", "selected_text": "Nunca — confio plenamente na minha percepção"},
        {"question_number": 9, "question_text": "Como está sua autoestima desde que está nesse relacionamento?", "selected_option": "A", "selected_text": "Melhor do que antes — me sinto crescendo"},
        {"question_number": 10, "question_text": "Você já sentiu medo da reação emocional ou comportamental do seu parceiro(a)?", "selected_option": "A", "selected_text": "Nunca — me sinto seguro(a) com ele(a)"},
    ]
    
    evaluation2 = evaluate_submission(answers_patient2)
    
    submission2 = Submission(
        uuid=generate_submission_uuid(),
        admin_url_token=generate_admin_access_token(),
        patient_name="João Santos",
        questionnaire_date=date.today(),
        total_score=evaluation2.total_score,
        classification=evaluation2.classification,
        interpretation=evaluation2.interpretation,
        notification_status="pending",
    )
    
    for answer in evaluation2.answers:
        submission2.answers.append(
            Answer(
                question_number=answer["question_number"],
                question_text=answer["question_text"],
                selected_option=answer["selected_option"],
                selected_text=answer["selected_text"],
                score=answer["score"],
            )
        )
    
    db.session.add(submission2)
    db.session.commit()
    
    print("\n✅ Pacientes criados com sucesso!")
    print(f"\nPaciente 1: {submission1.patient_name}")
    print(f"  - Score: {submission1.total_score}/40")
    print(f"  - Classificação: {submission1.classification}")
    print(f"  - Link: http://127.0.0.1:5001/admin/submissions/{submission1.uuid}/{submission1.admin_url_token}")
    
    print(f"\nPaciente 2: {submission2.patient_name}")
    print(f"  - Score: {submission2.total_score}/40")
    print(f"  - Classificação: {submission2.classification}")
    print(f"  - Link: http://127.0.0.1:5001/admin/submissions/{submission2.uuid}/{submission2.admin_url_token}")
