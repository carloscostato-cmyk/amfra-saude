"""Script para testar o sistema de tokens individuais"""
from app import create_app, db
from app.models import Company, EmployeeToken
import secrets

app = create_app()

with app.app_context():
    # Criar empresa de teste
    print("🏢 Criando empresa de teste...")
    test_company = Company(
        name="Empresa Teste Tokens",
        employee_count=5,
        hr_data="Teste do sistema de tokens individuais",
        token=secrets.token_urlsafe(16)
    )
    db.session.add(test_company)
    db.session.flush()
    
    # Gerar 5 tokens individuais
    print(f"🔐 Gerando {test_company.employee_count} tokens individuais...")
    tokens_gerados = []
    for i in range(test_company.employee_count):
        employee_token = EmployeeToken(
            company_id=test_company.id,
            token=secrets.token_urlsafe(16)
        )
        db.session.add(employee_token)
        tokens_gerados.append(employee_token)
    
    db.session.commit()
    
    print(f"\n✅ Empresa criada: {test_company.name} (ID: {test_company.id})")
    print(f"📊 Total de colaboradores: {test_company.employee_count}")
    print(f"\n🔗 Tokens gerados:")
    
    for idx, token in enumerate(tokens_gerados, 1):
        url = f"http://localhost:5000/q/{token.token}"
        print(f"  {idx}. {url}")
        print(f"     Status: {'✓ Disponível' if not token.used else '✗ Usado'}")
    
    print(f"\n🌐 Acesse o admin em: http://localhost:5000/admin/company/{test_company.id}")
    print(f"   Usuário: Deia")
    print(f"   Senha: JesusSalva")
