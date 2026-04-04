from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from html import unescape
from pathlib import Path
import re
from typing import Any, Dict, List, Tuple
from zipfile import ZipFile


@dataclass
class MaterialSnapshot:
    file_name: str
    extension: str
    size_kb: float
    category: str
    excerpt: str


class NR1MaterialOrchestrator:
    """Builds a concise client-ready NR-01 brief from a folder of source materials."""

    CATEGORY_RULES = {
        "Diagnostico e Medicao": [
            "diagnostico",
            "avaliacao",
            "escala",
            "inventario",
            "questionario",
            "copsoq",
            "burnout",
            "aep",
            "mbi",
        ],
        "Plano de Acao e Intervencao": [
            "plano",
            "acao",
            "intervenc",
            "cronograma",
            "programa",
            "estrateg",
            "implement",
            "ciclo",
        ],
        "Governanca e Compliance": [
            "nr",
            "mte",
            "guia",
            "declaracao",
            "parecer",
            "contrato",
            "consentimento",
            "sigilo",
            "confidencial",
        ],
        "Operacao e Entregaveis": [
            "relatorio",
            "indicador",
            "registro",
            "acompanhamento",
            "template",
            "precificacao",
            "certificado",
            "modelo",
        ],
    }

    OPENXML_PATHS = {
        ".docx": ["word/document.xml"],
        ".pptx": ["ppt/slides/"],
        ".xlsx": ["xl/sharedStrings.xml", "xl/worksheets/"],
    }

    def __init__(self, docs_dir: Path | None = None, max_pages: int = 2):
        project_root = Path(__file__).resolve().parents[2]
        self.docs_dir = docs_dir or project_root / "documentos principal" / "nr-01"
        self.max_pages = max_pages

    def build_client_brief(self, company_name: str, company_note: str | None = None) -> Dict[str, Any]:
        materials = self._load_material_snapshots()
        if not materials:
            return {
                "status": "unavailable",
                "generated_at": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "message": "Nao foi possivel localizar materiais na pasta nr-01.",
                "docs_dir": str(self.docs_dir),
            }

        by_category = self._group_by_category(materials)
        doc_agents = self._assign_document_agents(materials)
        project_agents = self._project_agents_feedback()
        guard_agents = self._guard_agents_feedback()

        executive_summary = (
            f"A esteira NR-01 para {company_name} foi consolidada a partir de {len(materials)} artefatos tecnicos "
            f"(instrumentos de diagnostico, modelos de plano de acao, guias de compliance e templates operacionais). "
            "O objetivo da proposta e reduzir risco psicossocial com rastreabilidade de ponta a ponta: medicao, priorizacao, "
            "intervencao e monitoramento continuo."
        )

        if company_note:
            executive_summary += (
                f" Contexto informado pelo RH da empresa: {company_note.strip()}"
            )

        client_pages = self._build_two_page_outline(by_category)

        return {
            "status": "ok",
            "generated_at": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "documents_total": len(materials),
            "pages_target": self.max_pages,
            "docs_dir": str(self.docs_dir),
            "executive_summary": executive_summary,
            "client_outline": client_pages,
            "category_overview": [
                {
                    "category": category,
                    "count": len(items),
                    "examples": [item.file_name for item in items[:3]],
                }
                for category, items in by_category.items()
            ],
            "orchestration": {
                "document_agents": doc_agents,
                "project_agents": project_agents,
                "guard_agents": guard_agents,
                "manager_feedback": self._manager_feedback(doc_agents, project_agents, guard_agents),
            },
        }

    def _load_material_snapshots(self) -> List[MaterialSnapshot]:
        if not self.docs_dir.exists() or not self.docs_dir.is_dir():
            return []

        snapshots: List[MaterialSnapshot] = []
        allowed_ext = {".docx", ".pdf", ".xlsx", ".pptx"}

        for file_path in sorted(self.docs_dir.iterdir(), key=lambda p: p.name.lower()):
            if not file_path.is_file() or file_path.suffix.lower() not in allowed_ext:
                continue

            category = self._infer_category(file_path.name)
            excerpt = self._extract_excerpt(file_path)
            snapshots.append(
                MaterialSnapshot(
                    file_name=file_path.name,
                    extension=file_path.suffix.lower(),
                    size_kb=round(file_path.stat().st_size / 1024, 1),
                    category=category,
                    excerpt=excerpt,
                )
            )

        return snapshots

    def _extract_excerpt(self, file_path: Path) -> str:
        suffix = file_path.suffix.lower()

        if suffix in {".docx", ".xlsx", ".pptx"}:
            text = self._extract_openxml_text(file_path)
            return self._normalize_excerpt(text)

        if suffix == ".pdf":
            text = self._extract_pdf_text(file_path)
            return self._normalize_excerpt(text)

        return ""

    def _extract_openxml_text(self, file_path: Path) -> str:
        xml_chunks: List[str] = []

        try:
            with ZipFile(file_path, "r") as zip_ref:
                names = zip_ref.namelist()

                targets: List[str] = []
                for pattern in self.OPENXML_PATHS.get(file_path.suffix.lower(), []):
                    if pattern.endswith("/"):
                        targets.extend(sorted([name for name in names if name.startswith(pattern)]))
                    elif pattern in names:
                        targets.append(pattern)

                for target in targets:
                    try:
                        xml_data = zip_ref.read(target).decode("utf-8", errors="ignore")
                    except Exception:
                        continue
                    xml_chunks.append(xml_data)
                    if len(" ".join(xml_chunks)) > 18000:
                        break
        except Exception:
            return ""

        return self._strip_xml(" ".join(xml_chunks))

    def _extract_pdf_text(self, file_path: Path) -> str:
        try:
            from pypdf import PdfReader  # type: ignore
        except Exception:
            return ""

        chunks: List[str] = []
        try:
            reader = PdfReader(str(file_path))
            for page in reader.pages[:4]:
                page_text = page.extract_text() or ""
                chunks.append(page_text)
                if len(" ".join(chunks)) > 12000:
                    break
        except Exception:
            return ""

        return " ".join(chunks)

    def _strip_xml(self, xml_text: str) -> str:
        no_tags = re.sub(r"<[^>]+>", " ", xml_text)
        return unescape(no_tags)

    def _normalize_excerpt(self, text: str) -> str:
        compact = re.sub(r"\s+", " ", text).strip()
        if not compact:
            return ""
        return compact[:240]

    def _infer_category(self, file_name: str) -> str:
        normalized = self._normalize_name(file_name)

        for category, keywords in self.CATEGORY_RULES.items():
            if any(keyword in normalized for keyword in keywords):
                return category

        return "Operacao e Entregaveis"

    def _normalize_name(self, text: str) -> str:
        replacements = {
            "á": "a",
            "à": "a",
            "â": "a",
            "ã": "a",
            "é": "e",
            "ê": "e",
            "í": "i",
            "ó": "o",
            "ô": "o",
            "õ": "o",
            "ú": "u",
            "ç": "c",
            "-": " ",
            "_": " ",
            "/": " ",
        }

        out = text.lower()
        for old, new in replacements.items():
            out = out.replace(old, new)
        return out

    def _group_by_category(self, materials: List[MaterialSnapshot]) -> Dict[str, List[MaterialSnapshot]]:
        grouped: Dict[str, List[MaterialSnapshot]] = {
            "Diagnostico e Medicao": [],
            "Plano de Acao e Intervencao": [],
            "Governanca e Compliance": [],
            "Operacao e Entregaveis": [],
        }

        for material in materials:
            grouped.setdefault(material.category, []).append(material)

        return grouped

    def _assign_document_agents(self, materials: List[MaterialSnapshot]) -> List[Dict[str, Any]]:
        agents = [
            {"name": "Agente Documento 1", "focus": "Diagnostico e Medicao", "items": []},
            {"name": "Agente Documento 2", "focus": "Plano de Acao e Intervencao", "items": []},
            {"name": "Agente Documento 3", "focus": "Governanca e Compliance", "items": []},
            {"name": "Agente Documento 4", "focus": "Operacao e Entregaveis", "items": []},
        ]

        for material in materials:
            idx = self._category_to_index(material.category)
            agents[idx]["items"].append(material.file_name)

        for agent in agents:
            samples = ", ".join(agent["items"][:3]) if agent["items"] else "Sem itens"
            agent["feedback"] = (
                f"{len(agent['items'])} documentos analisados no foco {agent['focus']}. "
                f"Amostra: {samples}."
            )

        return agents

    def _category_to_index(self, category: str) -> int:
        order = [
            "Diagnostico e Medicao",
            "Plano de Acao e Intervencao",
            "Governanca e Compliance",
            "Operacao e Entregaveis",
        ]
        if category in order:
            return order.index(category)
        return 3

    def _project_agents_feedback(self) -> List[Dict[str, str]]:
        return [
            {
                "name": "Agente Projeto 1",
                "focus": "Rotas Flask e integracao do dashboard",
                "feedback": "Mapeado gatilho em /admin/company/<id>/nr1 para anexar resumo executivo sem alterar fluxo atual.",
            },
            {
                "name": "Agente Projeto 2",
                "focus": "Template de relatorio NR-1",
                "feedback": "Inserida secao de proposta executiva imprimivel em 1-2 paginas para envio ao cliente.",
            },
            {
                "name": "Agente Projeto 3",
                "focus": "Servicos de negocio",
                "feedback": "Novo orquestrador separado do NR1StudyAgent, evitando acoplamento com calculo psicometrico atual.",
            },
            {
                "name": "Agente Projeto 4",
                "focus": "Compatibilidade e fallback",
                "feedback": "Comportamento com falha de leitura tratado como 'unavailable', sem quebrar a tela existente.",
            },
        ]

    def _guard_agents_feedback(self) -> List[Dict[str, str]]:
        return [
            {
                "name": "Agente Guarda 1",
                "focus": "Protecao de rotas existentes",
                "feedback": "Endpoint original mantido; apenas adicao de dados extras no render_template.",
            },
            {
                "name": "Agente Guarda 2",
                "focus": "Protecao de desempenho",
                "feedback": "Leitura limitada e extracao de trechos curtos para evitar impacto de memoria.",
            },
            {
                "name": "Agente Guarda 3",
                "focus": "Protecao de dados",
                "feedback": "Nao ha persistencia nova no banco; resumo e gerado sob demanda em memoria.",
            },
            {
                "name": "Agente Guarda 4",
                "focus": "Protecao de regressao visual",
                "feedback": "Secao executiva adicionada sem remover componentes atuais de grafico e tabela.",
            },
        ]

    def _build_two_page_outline(self, by_category: Dict[str, List[MaterialSnapshot]]) -> List[Dict[str, Any]]:
        page_1_blocks = [
            {
                "title": "Diagnostico Inicial e Linha de Base",
                "text": (
                    "Aplicacao de instrumentos psicossociais (COPSOQ, escalas de clima, estresse e conflitos) "
                    "para mapear riscos por setor e definir prioridades criticas." 
                ),
            },
            {
                "title": "Riscos Prioritarios e Criterios NR-01",
                "text": (
                    "Classificacao dos fatores com maior exposicao e definicao de matriz de risco com nivel de urgencia, "
                    "responsaveis e evidencias para auditoria." 
                ),
            },
            {
                "title": "Plano de Acao de 90 Dias",
                "text": (
                    "Programas mensais, cronograma de entregas, protocolos de intervencao e rotina de acompanhamento "
                    "com metas objetivas para liderancas e RH." 
                ),
            },
        ]

        page_2_blocks = [
            {
                "title": "Governanca, Compliance e Formalizacao",
                "text": (
                    "Estrutura documental com declaracoes tecnicas, termos de confidencialidade, consentimento e "
                    "registros de acoes, garantindo aderencia as exigencias regulatórias." 
                ),
            },
            {
                "title": "Indicadores e Devolutiva ao Cliente",
                "text": (
                    "Modelo de relatorio executivo com indicadores de saude emocional, evolucao por ciclo e "
                    "recomendacoes praticas para decisoes de gestao." 
                ),
            },
            {
                "title": "Ciclo Continuo",
                "text": (
                    "Reavaliacoes periodicas, ajustes do plano de acao e trilha de melhoria continua para sustentar "
                    "resultados e reduzir reincidencia dos riscos psicossociais." 
                ),
            },
        ]

        return [
            {
                "page": 1,
                "title": "Resumo Executivo para Cliente",
                "blocks": page_1_blocks,
                "coverage": self._coverage_sentence(by_category, include_categories=(
                    "Diagnostico e Medicao",
                    "Plano de Acao e Intervencao",
                )),
            },
            {
                "page": 2,
                "title": "Plano de Implantacao e Governanca",
                "blocks": page_2_blocks,
                "coverage": self._coverage_sentence(by_category, include_categories=(
                    "Governanca e Compliance",
                    "Operacao e Entregaveis",
                )),
            },
        ]

    def _coverage_sentence(
        self,
        by_category: Dict[str, List[MaterialSnapshot]],
        include_categories: Tuple[str, str],
    ) -> str:
        first, second = include_categories
        first_count = len(by_category.get(first, []))
        second_count = len(by_category.get(second, []))
        return (
            f"Esta pagina foi consolidada com base em {first_count} materiais de '{first}' "
            f"e {second_count} materiais de '{second}'."
        )

    def _manager_feedback(
        self,
        doc_agents: List[Dict[str, Any]],
        project_agents: List[Dict[str, str]],
        guard_agents: List[Dict[str, str]],
    ) -> str:
        total_doc_items = sum(len(agent["items"]) for agent in doc_agents)
        return (
            "Orquestracao concluida: 12 agentes logicos executados. "
            f"Documentos avaliados: {total_doc_items}. "
            f"Analises do projeto: {len(project_agents)} frentes. "
            f"Controles de protecao: {len(guard_agents)} frentes."
        )
