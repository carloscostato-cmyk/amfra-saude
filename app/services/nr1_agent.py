from typing import Dict, List, Any
from sqlalchemy import func
from app.extensions import db
from app.models import Answer, Company, Employee, Submission
from app.questionnaire import QUESTION_DEFINITIONS, DIMENSIONS
from app.services.scoring import _band_label


class NR1StudyAgent:
    """Agente responsável por compilar e analisar o estudo NR-1 (HSE-IT) para uma empresa."""

    def __init__(self, company_id: int):
        self.company_id = company_id
        self.company = Company.query.get(company_id)
        if not self.company:
            raise ValueError("Empresa não encontrada.")

    def run_study(self) -> Dict[str, Any]:
        """Executa a análise dos riscos psicossociais com base no HSE-IT (35 perguntas, Likert 1-5)."""

        employees = Employee.query.filter_by(company_id=self.company_id).all()
        employee_ids = [emp.id for emp in employees]

        if not employee_ids:
            return self._empty_report()

        submissions = Submission.query.filter(Submission.employee_id.in_(employee_ids)).all()
        total_respondents = len(submissions)

        if total_respondents == 0:
            return self._empty_report()

        submission_ids = [sub.id for sub in submissions]

        # Média de cada questão (agrupada)
        question_averages = db.session.query(
            Answer.question_number,
            func.avg(Answer.score).label('avg_score')
        ).filter(
            Answer.submission_id.in_(submission_ids)
        ).group_by(
            Answer.question_number
        ).all()

        avg_by_q = {q_num: float(q_avg) for q_num, q_avg in question_averages}

        # Média global
        all_avg_values = list(avg_by_q.values())
        global_avg = round(sum(all_avg_values) / len(all_avg_values), 2) if all_avg_values else 0.0
        global_band = _band_label(global_avg)

        # Distribuição de classificações individuais
        distribution: Dict[str, int] = {}
        for sub in submissions:
            dist = distribution.get(sub.classification, 0)
            distribution[sub.classification] = dist + 1

        # Análise por dimensão
        dimension_analysis = []
        for dim_name, q_nums in DIMENSIONS.items():
            dim_scores = [avg_by_q[n] for n in q_nums if n in avg_by_q]
            if dim_scores:
                dim_avg = round(sum(dim_scores) / len(dim_scores), 2)
                dim_band = _band_label(dim_avg)
            else:
                dim_avg = 0.0
                dim_band = "N/D"
            dimension_analysis.append({
                "dimension_name": dim_name,
                "question_numbers": q_nums,
                "average": dim_avg,
                "band": dim_band,
            })

        # Ordena por média (menor primeiro = mais crítico)
        dimension_analysis.sort(key=lambda x: x["average"])

        # Questões com média mais baixa (maior risco)
        topics_risk = []
        for q_num, q_avg in sorted(avg_by_q.items(), key=lambda x: x[1]):
            q_def = next((q for q in QUESTION_DEFINITIONS if q["number"] == q_num), None)
            if q_def:
                topics_risk.append({
                    "question_number": q_num,
                    "topic_name": self._get_dimension_for_question(q_num),
                    "average_score": round(q_avg, 2),
                    "question_text": q_def["text"],
                    "band": _band_label(q_avg),
                })

        # Percentual com classificação BAIXO
        low_count = distribution.get("BAIXO", 0)
        low_percentage = round((low_count / total_respondents) * 100, 1)
        needs_immediate_action = low_percentage > 15.0

        return {
            "company_name": self.company.name,
            "total_employees": self.company.employee_count,
            "total_respondents": total_respondents,
            "participation_rate": round(
                (total_respondents / self.company.employee_count * 100) if self.company.employee_count else 0, 1
            ),
            "company_average_score": global_avg,
            "global_band": global_band,
            "risk_distribution": distribution,
            "dimension_analysis": dimension_analysis,
            "top_risk_topics": topics_risk[:3],
            "all_topics": topics_risk,
            "critical_percentage": low_percentage,
            "needs_immediate_action": needs_immediate_action,
            "status": "success",
        }

    def _empty_report(self) -> Dict[str, Any]:
        return {
            "company_name": self.company.name,
            "total_employees": self.company.employee_count,
            "total_respondents": 0,
            "participation_rate": 0,
            "company_average_score": 0,
            "global_band": "N/D",
            "risk_distribution": {},
            "dimension_analysis": [],
            "top_risk_topics": [],
            "all_topics": [],
            "critical_percentage": 0,
            "needs_immediate_action": False,
            "status": "empty",
        }

    def _get_dimension_for_question(self, question_number: int) -> str:
        for dim_name, q_nums in DIMENSIONS.items():
            if question_number in q_nums:
                return dim_name
        return f"Questão {question_number}"
