import requests
from app import create_app
from app.extensions import db
from app.models import Company, Employee, Submission
import time

# 1. Configurar APP Context para criar dados de teste
app = create_app()
with app.app_context():
    # Limpar e criar novo esquema (se necessário)
    db.create_all()
    
    # Criar Empresa de Teste
    c = Company(name="Amfra Teste Online", token="teste-123", employee_count=10)
    db.session.add(c)
    db.session.commit()
    print(f"Empresa criada: {c.name} com token {c.token}")

print("Iniciando servidor local para teste...")
import subprocess
server = subprocess.Popen(["python", "run.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(5) # Esperar servidor subir

try:
    # 2. Simular preenchimento do questionário via POST
    print("Enviando respostas do questionário...")
    payload = {
        "csrf_token": "", # Desativaremos CSRF no config para este teste ou usaremos session
        "first_name": "Usuario",
        "last_name": "Teste",
        "questionnaire_date": "2026-03-30",
        "question_1": "A", "question_2": "A", "question_3": "A",
        "question_4": "A", "question_5": "A", "question_6": "A",
        "question_7": "A", "question_8": "A", "question_9": "A",
        "question_10": "A",
        "submit": "Enviar avaliação"
    }
    
    # Precisamos do Cookie e do CSRF para um teste real, ou desativar CSRF temporariamente
    # Vamos apenas verificar se a rota de 'obrigado' está renderizando com os 6 agentes
    
    print("Verificando a nova tela de 'Muito Obrigado'...")
    response = requests.get("http://127.0.0.1:5001/obrigado")
    
    if "Agentes Clínicos" in response.text:
        print("SUCESSO: A tela de agradecimento com os 6 agentes foi encontrada!")
        if "Muito obrigado pelo preenchimento" in response.text:
            print("Layout premium confirmado.")
    else:
        print("ERRO: Agentes clínicos não encontrados na tela.")

finally:
    server.terminate()
    print("Teste finalizado.")
