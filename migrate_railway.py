"""
Script para migrar banco de dados no Railway
Adiciona tabela employee_tokens
"""
import os
from app import create_app, db
from app.models import EmployeeToken

print("🚀 Iniciando migração do banco de dados...")

app = create_app()

with app.app_context():
    try:
        # Criar tabela employee_tokens
        db.create_all()
        print("✅ Tabela employee_tokens criada com sucesso!")
        
        # Verificar se a tabela foi criada
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        if 'employee_tokens' in tables:
            print("✅ Verificação: Tabela employee_tokens existe no banco!")
            
            # Mostrar colunas
            columns = [col['name'] for col in inspector.get_columns('employee_tokens')]
            print(f"📋 Colunas: {', '.join(columns)}")
        else:
            print("❌ ERRO: Tabela employee_tokens não foi criada!")
            
    except Exception as e:
        print(f"❌ Erro na migração: {e}")
        raise

print("\n🎉 Migração concluída!")
