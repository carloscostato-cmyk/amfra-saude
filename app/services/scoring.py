"""
Scoring HSE-IT (Health Safety Executive Indicator Tool)
========================================================
Escala Likert: 1 (Nunca) a 5 (Sempre)

Regra de interpretação por DIMENSÃO (média aritmética das respostas):
  DE 1,00 a 2,29 → BAIXO
  DE 2,30 a 3,69 → MÉDIO
  DE 3,70 a 5,00 → ALTO

A classificação GLOBAL também segue a média aritmética das 35 respostas
com os mesmos limites acima.
"""

from dataclasses import dataclass, field as dc_field
from statistics import mean

from app.questionnaire import DIMENSIONS


# ─── Faixas de interpretação (Anexo 2) ──────────────────────────────────────
BAND_LOW    = (1.00, 2.29)
BAND_MEDIUM = (2.30, 3.69)
BAND_HIGH   = (3.70, 5.00)


def _band_label(average: float) -> str:
    if average <= BAND_LOW[1]:
        return "BAIXO"
    if average <= BAND_MEDIUM[1]:
        return "MÉDIO"
    return "ALTO"


# ─── Interpretações gerais ───────────────────────────────────────────────────
INTERPRETATIONS = {
    "BAIXO": (
        "A média geral indica baixa percepção de bem-estar no trabalho. "
        "Os colaboradores demonstram sinais significativos de insatisfação e exposição "
        "a riscos psicossociais relevantes. Recomenda-se intervenção prioritária nas "
        "dimensões com pior desempenho."
    ),
    "MÉDIO": (
        "A média geral aponta para um nível moderado de percepção de bem-estar. "
        "Existem aspectos positivos, mas também dimensões que merecem atenção e melhoria "
        "para promover um ambiente de trabalho mais saudável e seguro emocionalmente."
    ),
    "ALTO": (
        "A média geral indica boa percepção de bem-estar no trabalho. "
        "O ambiente apresenta fatores protetores consolidados. Recomenda-se manter as "
        "práticas atuais e monitorar continuamente as dimensões de menor pontuação."
    ),
}

# As classificações para compatibilidade com o código legado
CLASSIFICATION_RULES = [
    (1.00, 2.29, "BAIXO"),
    (2.30, 3.69, "MÉDIO"),
    (3.70, 5.00, "ALTO"),
]


@dataclass(frozen=True)
class DimensionResult:
    name: str
    question_numbers: list
    average: float
    band: str


@dataclass(frozen=True)
class EvaluationResult:
    answers: list
    total_score: int          # soma bruta (mantida por compatibilidade com DB)
    classification: str       # label global: BAIXO | MÉDIO | ALTO
    interpretation: str
    global_average: float     # média aritmética global (1–5)
    dimension_results: list   # lista de DimensionResult


def score_for_option(option: str) -> int:
    """Converte a resposta Likert '1'–'5' em inteiro."""
    try:
        val = int(option)
        if 1 <= val <= 5:
            return val
    except (TypeError, ValueError):
        pass
    raise ValueError(f"Opção inválida: '{option}'. Esperado '1' a '5'.")


def classify_score(average: float) -> str:
    return _band_label(average)


def evaluate_submission(answer_payloads: list[dict]) -> EvaluationResult:
    scored_answers = []
    for answer in answer_payloads:
        score = score_for_option(answer["selected_option"])
        scored_answers.append({**answer, "score": score})

    scores_by_question = {a["question_number"]: a["score"] for a in scored_answers}
    total_score = sum(a["score"] for a in scored_answers)
    global_average = total_score / len(scored_answers) if scored_answers else 0.0
    classification = classify_score(global_average)
    interpretation = INTERPRETATIONS[classification]

    # Calcular médias por dimensão
    dimension_results = []
    for dim_name, q_nums in DIMENSIONS.items():
        dim_scores = [scores_by_question[n] for n in q_nums if n in scores_by_question]
        if dim_scores:
            avg = round(mean(dim_scores), 2)
            band = _band_label(avg)
        else:
            avg = 0.0
            band = "N/D"
        dimension_results.append(DimensionResult(
            name=dim_name,
            question_numbers=q_nums,
            average=avg,
            band=band,
        ))

    return EvaluationResult(
        answers=scored_answers,
        total_score=total_score,
        classification=classification,
        interpretation=interpretation,
        global_average=round(global_average, 2),
        dimension_results=dimension_results,
    )


def interpretation_for_classification(classification: str) -> str:
    return INTERPRETATIONS.get(classification, "")
