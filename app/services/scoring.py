from dataclasses import dataclass


SCORE_MAP = {"A": 1, "B": 2, "C": 3, "D": 4}

CLASSIFICATION_RULES = [
    (10, 15, "RELACIONAMENTO SAUDÁVEL"),
    (16, 25, "ATENÇÃO: PADRÕES PREOCUPANTES"),
    (26, 35, "ALERTA: SINAIS NARCÍSICOS SIGNIFICATIVOS"),
    (36, 40, "CRÍTICO: ABUSO NARCÍSICO — INTERVENÇÃO NECESSÁRIA"),
]

INTERPRETATIONS = {
    "RELACIONAMENTO SAUDÁVEL": (
        "As respostas sugerem um vínculo com segurança emocional, respeito e abertura para diálogo. "
        "Mesmo em relações saudáveis, vale manter comunicação clara, limites consistentes e espaço para cuidado mútuo."
    ),
    "ATENÇÃO: PADRÕES PREOCUPANTES": (
        "Há sinais que merecem observação cuidadosa. O resultado aponta possíveis desgastes emocionais, "
        "situações de invalidação ou desequilíbrio relacional que podem se intensificar sem intervenção consciente."
    ),
    "ALERTA: SINAIS NARCÍSICOS SIGNIFICATIVOS": (
        "A pontuação indica padrões narcísicos relevantes com impacto emocional importante. "
        "É recomendável fortalecer limites, rede de apoio e considerar orientação profissional especializada."
    ),
    "CRÍTICO: ABUSO NARCÍSICO — INTERVENÇÃO NECESSÁRIA": (
        "O resultado é compatível com um cenário de abuso narcísico intenso e sofrimento elevado. "
        "A situação pede atenção clínica, rede de apoio confiável e avaliação cuidadosa de segurança emocional e prática."
    ),
}


@dataclass(frozen=True)
class EvaluationResult:
    answers: list[dict]
    total_score: int
    classification: str
    interpretation: str


def score_for_option(option: str) -> int:
    normalized_option = (option or "").strip().upper()
    if normalized_option not in SCORE_MAP:
        raise ValueError("Opção de resposta inválida.")
    return SCORE_MAP[normalized_option]


def calculate_total_score(options: list[str]) -> int:
    return sum(score_for_option(option) for option in options)


def classify_score(total_score: int) -> str:
    for minimum, maximum, label in CLASSIFICATION_RULES:
        if minimum <= total_score <= maximum:
            return label
    raise ValueError("Pontuação total fora da faixa esperada para 10 perguntas.")


def interpretation_for_classification(classification: str) -> str:
    if classification not in INTERPRETATIONS:
        raise ValueError("Classificação inválida para interpretação.")
    return INTERPRETATIONS[classification]


def evaluate_submission(answer_payloads: list[dict]) -> EvaluationResult:
    scored_answers = []
    for answer in answer_payloads:
        score = score_for_option(answer["selected_option"])
        scored_answers.append({**answer, "score": score})

    total_score = calculate_total_score([answer["selected_option"] for answer in scored_answers])
    classification = classify_score(total_score)
    interpretation = interpretation_for_classification(classification)

    return EvaluationResult(
        answers=scored_answers,
        total_score=total_score,
        classification=classification,
        interpretation=interpretation,
    )
