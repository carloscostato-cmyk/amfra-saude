from typing import Dict, List, Any
from sqlalchemy import func
from app.extensions import db
from app.models import Answer, Company, Employee, Submission
from app.questionnaire import QUESTION_DEFINITIONS

class NR1StudyAgent:
    """Agente responsável por compilar e analisar o estudo da NR-1 (Riscos Psicossociais) para uma empresa."""

    def __init__(self, company_id: int):
        self.company_id = company_id
        self.company = Company.query.get(company_id)
        if not self.company:
            raise ValueError("Empresa não encontrada.")

    def run_study(self) -> Dict[str, Any]:
        """Executa a análise de dados da NR-1 mapeando riscos psicossociais da organização."""
        
        employees = Employee.query.filter_by(company_id=self.company_id).all()
        employee_ids = [emp.id for emp in employees]
        
        if not employee_ids:
            return self._empty_report()
            
        submissions = Submission.query.filter(Submission.employee_id.in_(employee_ids)).all()
        total_respondents = len(submissions)
        
        if total_respondents == 0:
            return self._empty_report()
            
        # 1. Total Score Average
        avg_score = sum(sub.total_score for sub in submissions) / total_respondents
        
        # 2. Risk Distribution (Classifications)
        distribution = {}
        for sub in submissions:
            dist = distribution.get(sub.classification, 0)
            distribution[sub.classification] = dist + 1
            
        # 3. Question / Topic Analysis
        submission_ids = [sub.id for sub in submissions]
        
        # Calculate average score per question
        question_averages = db.session.query(
            Answer.question_number,
            func.avg(Answer.score).label('avg_score')
        ).filter(
            Answer.submission_id.in_(submission_ids)
        ).group_by(
            Answer.question_number
        ).all()
        
        topics_risk = []
        for q_num, q_avg in question_averages:
            q_def = next((q for q in QUESTION_DEFINITIONS if q["number"] == q_num), None)
            if q_def:
                topics_risk.append({
                    "question_number": q_num,
                    "topic_name": self._get_topic_name(q_num),
                    "average_score": round(float(q_avg), 2),
                    "question_text": q_def["text"]
                })
                
        # Sort topics by highest risk (highest average score)
        topics_risk.sort(key=lambda x: x["average_score"], reverse=True)
        
        # 4. Critical Need Identifier
        critical_percentage = (distribution.get("CRÍTICO: ABUSO NARCÍSICO — INTERVENÇÃO NECESSÁRIA", 0) / total_respondents) * 100
        needs_immediate_action = critical_percentage > 15.0  # Threshold conceptual for HR action
        
        return {
            "company_name": self.company.name,
            "total_employees": self.company.employee_count,
            "total_respondents": total_respondents,
            "participation_rate": round((total_respondents / self.company.employee_count * 100) if self.company.employee_count else 0, 1),
            "company_average_score": round(avg_score, 1),
            "risk_distribution": distribution,
            "top_risk_topics": topics_risk[:3],  # Top 3 highest risk areas
            "all_topics": topics_risk,
            "critical_percentage": round(critical_percentage, 1),
            "needs_immediate_action": needs_immediate_action,
            "status": "success"
        }
        
    def _empty_report(self) -> Dict[str, Any]:
        return {
            "company_name": self.company.name,
            "total_employees": self.company.employee_count,
            "total_respondents": 0,
            "participation_rate": 0,
            "company_average_score": 0,
            "risk_distribution": {},
            "top_risk_topics": [],
            "all_topics": [],
            "critical_percentage": 0,
            "needs_immediate_action": False,
            "status": "empty"
        }

    def _get_topic_name(self, question_number: int) -> str:
        topics = {
            1: "Estado emocional", 2: "Responsabilização", 3: "Críticas",
            4: "Empatia", 5: "Reciprocidade", 6: "Isolamento",
            7: "Comunicação", 8: "Confusão mental", 9: "Autoestima", 10: "Medo da reação"
        }
        return topics.get(question_number, f"Tópico {question_number}")
