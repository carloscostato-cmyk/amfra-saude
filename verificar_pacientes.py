from app import create_app
from app.models import Submission

app = create_app()

with app.app_context():
    submissions = Submission.query.all()
    print(f'Total de pacientes: {len(submissions)}')
    for s in submissions:
        print(f'- {s.patient_name}: {s.total_score}/40 - UUID: {s.uuid}')
        print(f'  Token: {s.admin_url_token}')
        print(f'  Respostas: {len(s.answers)}')
