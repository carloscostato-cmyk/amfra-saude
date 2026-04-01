#!/usr/bin/env python3
"""
Script de teste para verificar o gráfico consolidado NR-1
"""

import sys
from app import create_app
from app.models import Company, Employee, Submission
from app.services.nr1_agent import NR1StudyAgent

def test_consolidated_chart():
    """Testa se o NR1StudyAgent retorna os dados corretos para o gráfico"""
    app = create_app()
    
    with app.app_context():
        # Buscar primeira empresa com dados
        companies = Company.query.all()
        
        if not companies:
            print("❌ Nenhuma empresa encontrada no banco de dados")
            return False
        
        for company in companies:
            print(f"\n{'='*60}")
            print(f"Testando empresa: {company.name} (ID: {company.id})")
            print(f"{'='*60}")
            
            # Contar submissions
            employees = Employee.query.filter_by(company_id=company.id).all()
            employee_ids = [emp.id for emp in employees]
            submissions = Submission.query.filter(Submission.employee_id.in_(employee_ids)).all()
            
            print(f"📊 Colaboradores cadastrados: {len(employees)}")
            print(f"📝 Respostas recebidas: {len(submissions)}")
            
            if not submissions:
                print("⚠️  Empresa sem respostas, pulando...")
                continue
            
            # Executar agente NR-1
            try:
                agent = NR1StudyAgent(company.id)
                report = agent.run_study()
                
                print(f"\n✅ Relatório gerado com sucesso!")
                print(f"Status: {report['status']}")
                print(f"Total de respondentes: {report['total_respondents']}")
                print(f"Taxa de participação: {report['participation_rate']}%")
                print(f"Média global: {report['company_average_score']}")
                print(f"Classificação global: {report['global_band']}")
                
                # Verificar risk_distribution
                print(f"\n📈 Distribuição de Riscos:")
                risk_dist = report.get('risk_distribution', {})
                
                if not risk_dist:
                    print("❌ ERRO: risk_distribution está vazio!")
                    return False
                
                total_in_dist = 0
                for classification in ['BAIXO', 'MÉDIO', 'ALTO']:
                    count = risk_dist.get(classification, 0)
                    total_in_dist += count
                    pct = (count / report['total_respondents'] * 100) if report['total_respondents'] > 0 else 0
                    print(f"  {classification:8s}: {count:3d} colaboradores ({pct:5.1f}%)")
                
                # Validações
                print(f"\n🔍 Validações:")
                
                # 1. Soma deve ser igual ao total de respondentes
                if total_in_dist == report['total_respondents']:
                    print(f"  ✅ Soma da distribuição ({total_in_dist}) = Total de respondentes ({report['total_respondents']})")
                else:
                    print(f"  ❌ ERRO: Soma da distribuição ({total_in_dist}) ≠ Total de respondentes ({report['total_respondents']})")
                    return False
                
                # 2. Todas as classificações devem estar presentes
                expected_keys = {'BAIXO', 'MÉDIO', 'ALTO'}
                actual_keys = set(risk_dist.keys())
                if expected_keys == actual_keys:
                    print(f"  ✅ Todas as classificações presentes: {expected_keys}")
                else:
                    print(f"  ❌ ERRO: Classificações faltando. Esperado: {expected_keys}, Atual: {actual_keys}")
                    return False
                
                # 3. Percentuais devem somar ~100%
                total_pct = sum((count / report['total_respondents'] * 100) for count in risk_dist.values())
                if abs(total_pct - 100.0) < 0.1:
                    print(f"  ✅ Percentuais somam 100% (atual: {total_pct:.1f}%)")
                else:
                    print(f"  ❌ ERRO: Percentuais não somam 100% (atual: {total_pct:.1f}%)")
                    return False
                
                print(f"\n✅ Todos os testes passaram para {company.name}!")
                return True
                
            except Exception as e:
                print(f"❌ ERRO ao executar agente: {e}")
                import traceback
                traceback.print_exc()
                return False
        
        print("\n⚠️  Nenhuma empresa com dados para testar")
        return False

if __name__ == "__main__":
    success = test_consolidated_chart()
    sys.exit(0 if success else 1)
