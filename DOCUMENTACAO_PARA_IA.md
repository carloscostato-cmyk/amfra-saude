# 🤖 Documentação para IAs - AMFRA Saúde Mental

Guia completo para assistentes de IA trabalharem efetivamente no projeto AMFRA.

## 📋 Índice

1. [Visão Geral do Projeto](#visão-geral-do-projeto)
2. [Arquitetura](#arquitetura)
3. [Estrutura de Pastas](#estrutura-de-pastas)
4. [Padrões de Código](#padrões-de-código)
5. [Como Adicionar Features](#como-adicionar-features)
6. [Specs Existentes](#specs-existentes)
7. [Testes](#testes)
8. [Convenções](#convenções)

---

## 🎯 Visão Geral do Projeto

### O que é o AMFRA?

Sistema web para avaliação de riscos psicossociais em ambientes de trabalho, baseado no questionário HSE-IT (Health Safety Executive Indicator Tool) com 35 perguntas e 7 dimensões psicossociais, em conformidade com a NR-1.

### Objetivo Principal

Permitir que empresas avaliem o bem-estar psicossocial de seus colaboradores através de um questionário científico validado, gerando relatórios consolidados e individuais.

### Usuários do Sistema

1. **Colaboradores**: Respondem ao questionário HSE-IT (35 perguntas)
2. **Administradores**: Gerenciam empresas, visualizam relatórios, analisam dados

### Fluxo Principal

```
1. Admin cria empresa → Gera token
2. Admin compartilha link com colaboradores
3. Colaborador acessa link → Preenche questionário
4. Sistema calcula scores e classificação
5. Admin visualiza resultados individuais e consolidados
6. Admin acessa relatório NR-1 da empresa
```

---

## 🏗️ Arquitetura

### Stack Tecnológico

**Backend**:
- Flask 3.0 (framework web)
- SQLAlchemy (ORM)
- Flask-Login (autenticação)
- Flask-WTF (formulários + CSRF)
- Gunicorn (servidor WSGI)

**Frontend**:
- Jinja2 (templates)
- HTML5 + CSS3
- JavaScript (ES6+)
- Chart.js 4.4.2 (gráficos)

**Banco de Dados**:
- SQLite (desenvolvimento)
- PostgreSQL (produção)

### Padrão de Arquitetura

O projeto segue o padrão **MVC (Model-View-Controller)** adaptado para Flask:

- **Models** (`app/models.py`): Entidades do banco de dados
- **Views** (`app/templates/`): Templates HTML
- **Controllers** (`app/routes_*.py`): Lógica de rotas e controle
- **Services** (`app/services/`): Lógica de negócio reutilizável

### Estrutura de Módulos

```
app/
├── __init__.py           # Factory da aplicação (create_app)
├── extensions.py         # Extensões Flask (db, csrf, login_manager)
├── models.py             # Modelos SQLAlchemy
├── forms.py              # Formulários WTForms
├── questionnaire.py      # Definição do HSE-IT
├── routes_admin.py       # Rotas administrativas
├── routes_public.py      # Rotas públicas
├── services/             # Lógica de negócio
│   ├── nr1_agent.py      # Análise consolidada NR-1
│   ├── scoring.py        # Cálculo de scores
│   └── links.py          # Geração de URLs
├── templates/            # Templates Jinja2
└── static/               # Arquivos estáticos (CSS, JS, imagens)
```

---

## 📁 Estrutura de Pastas Detalhada

### `/app` - Aplicação Principal

```
app/
├── __init__.py
│   └── create_app()              # Factory da aplicação
│   └── ensure_admin_user()       # Seed automático de admin
│   └── _configure_logging()      # Configuração de logs
│   └── _register_blueprints()    # Registro de rotas
│   └── _register_cli_commands()  # Comandos Flask CLI
│
├── extensions.py
│   └── db                        # SQLAlchemy instance
│   └── csrf                      # CSRFProtect instance
│   └── login_manager             # LoginManager instance
│
├── models.py
│   └── AdminUser                 # Usuário administrativo
│   └── Company                   # Empresa
│   └── Employee                  # Colaborador
│   └── Submission                # Submissão de questionário
│   └── Answer                    # Resposta individual
│   └── EmployeeToken             # Token de colaborador
│
├── forms.py
│   └── LoginForm                 # Formulário de login
│   └── CompanyForm               # Formulário de empresa
│   └── QuestionnaireForm         # Formulário do questionário
│
├── questionnaire.py
│   └── QUESTIONNAIRE_CODE        # "HSE-IT"
│   └── LIKERT_CHOICES            # Escala 1-5
│   └── DIMENSIONS                # 7 dimensões psicossociais
│   └── QUESTION_TEXTS            # 35 perguntas
│   └── QUESTION_DEFINITIONS      # Estrutura completa
│
├── routes_admin.py
│   └── /admin/login              # Login administrativo
│   └── /admin/dashboard          # Dashboard principal
│   └── /admin/companies          # Listagem de empresas
│   └── /admin/companies/<id>     # Detalhes da empresa
│   └── /admin/companies/<id>/nr1 # Relatório NR-1
│   └── /admin/submissions/<id>   # Detalhes da submissão
│
├── routes_public.py
│   └── /                         # Página inicial (redireciona)
│   └── /q/<token>                # Questionário público
│   └── /thank-you                # Página de agradecimento
│
└── services/
    ├── nr1_agent.py
    │   └── NR1StudyAgent         # Análise consolidada por empresa
    │       └── run_study()       # Executa análise completa
    │
    ├── scoring.py
    │   └── score_for_option()    # Converte resposta em score
    │   └── classify_score()      # Classifica média (BAIXO/MÉDIO/ALTO)
    │   └── evaluate_submission() # Avalia submissão completa
    │
    └── links.py
        └── build_public_questionnaire_url()  # Gera URL do questionário
```

### `/app/templates` - Templates HTML

```
templates/
├── base.html                     # Template base (header, footer)
├── public_form.html              # Formulário público (35 questões)
├── thank_you.html                # Página de agradecimento
├── loading_amfra.html            # Animação de loading
├── admin_login.html              # Login administrativo
├── admin_dashboard.html          # Dashboard principal
├── admin_company_detail.html     # Detalhes da empresa
├── admin_company_form.html       # Formulário de empresa
├── admin_company_nr1.html        # Relatório NR-1 consolidado
├── admin_submission_detail.html  # Detalhes da submissão individual
└── errors/
    ├── 404.html                  # Página não encontrada
    └── 500.html                  # Erro interno
```

### `/app/static` - Arquivos Estáticos

```
static/
├── css/
│   ├── style.css                 # Estilos principais
│   └── modern.css                # Estilos modernos (alternativo)
├── js/
│   ├── main.js                   # Scripts gerais
│   └── submission_detail.js      # Scripts de detalhes (gráficos)
└── img/
    ├── logo.jpg                  # Logo da empresa AMFRA SAÚDE MENTAL
    └── brain-icon.svg            # Ícone de cérebro
```

### `/.kiro/specs` - Especificações de Features

```
.kiro/specs/
├── company-consolidated-nr1-chart/
│   ├── requirements.md           # Requisitos da feature
│   ├── design.md                 # Design técnico
│   └── tasks.md                  # Tarefas de implementação
├── copy-link-button-improvements/
├── mobile-button-overlap-fix/
└── nr1-pdf-print-fix/
```

---

## 💻 Padrões de Código

### Python

#### Estilo de Código

- **PEP 8**: Seguir convenções Python
- **Type Hints**: Usar sempre que possível
- **Docstrings**: Documentar funções complexas
- **Imports**: Organizar em ordem (stdlib, third-party, local)

**Exemplo**:
```python
from datetime import datetime
from typing import Dict, List, Any

from flask import render_template, request
from sqlalchemy import func

from app.extensions import db
from app.models import Company, Submission


def calculate_company_stats(company_id: int) -> Dict[str, Any]:
    """
    Calcula estatísticas consolidadas de uma empresa.
    
    Args:
        company_id: ID da empresa
        
    Returns:
        Dicionário com estatísticas (total_respondents, average_score, etc.)
    """
    company = Company.query.get_or_404(company_id)
    # ... lógica
    return {
        "total_respondents": total,
        "average_score": avg,
    }
```

#### Nomenclatura

- **Classes**: `PascalCase` (ex: `AdminUser`, `NR1StudyAgent`)
- **Funções**: `snake_case` (ex: `calculate_score`, `build_url`)
- **Constantes**: `UPPER_SNAKE_CASE` (ex: `QUESTIONNAIRE_CODE`, `DIMENSIONS`)
- **Variáveis privadas**: `_prefixo` (ex: `_band_label`, `_empty_report`)

#### Estrutura de Funções

```python
def nome_da_funcao(parametro: tipo) -> tipo_retorno:
    """Docstring explicando o que a função faz."""
    # 1. Validação de entrada
    if not parametro:
        raise ValueError("Parâmetro inválido")
    
    # 2. Lógica principal
    resultado = processar(parametro)
    
    # 3. Retorno
    return resultado
```

### HTML/Jinja2

#### Estrutura de Templates

```jinja2
{% extends "base.html" %}

{% block title %}Título da Página{% endblock %}

{% block content %}
<div class="container">
    <h1>{{ titulo }}</h1>
    
    {% if dados %}
        <ul>
        {% for item in dados %}
            <li>{{ item.nome }}</li>
        {% endfor %}
        </ul>
    {% else %}
        <p>Nenhum dado disponível.</p>
    {% endif %}
</div>
{% endblock %}

{% block scripts %}
<script src="{{ url_for('static', filename='js/meu_script.js') }}"></script>
{% endblock %}
```

#### Convenções

- **Indentação**: 4 espaços
- **Classes CSS**: `kebab-case` (ex: `admin-dashboard`, `submission-detail`)
- **IDs**: `camelCase` (ex: `submitButton`, `chartCanvas`)

### CSS

#### Estrutura

```css
/* ============================================
   SEÇÃO: Descrição
   ============================================ */

.classe-principal {
    /* Layout */
    display: flex;
    flex-direction: column;
    
    /* Dimensões */
    width: 100%;
    max-width: 1200px;
    
    /* Espaçamento */
    margin: 0 auto;
    padding: 20px;
    
    /* Tipografia */
    font-size: 16px;
    color: #333;
    
    /* Visual */
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 8px;
}
```

#### Nomenclatura

- **BEM-like**: `.bloco__elemento--modificador`
- **Exemplo**: `.card__title--large`, `.button--primary`

### JavaScript

#### Estilo

```javascript
// Usar const/let (não var)
const API_URL = '/api/data';
let currentPage = 1;

// Funções arrow quando apropriado
const calcularMedia = (valores) => {
    return valores.reduce((a, b) => a + b, 0) / valores.length;
};

// Async/await para operações assíncronas
async function carregarDados() {
    try {
        const response = await fetch(API_URL);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Erro ao carregar dados:', error);
        return null;
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    inicializarGraficos();
    configurarEventos();
});
```

---

## ➕ Como Adicionar Features

### Processo Geral

1. **Criar Spec** (`.kiro/specs/nome-da-feature/`)
2. **Implementar Backend** (models, routes, services)
3. **Implementar Frontend** (templates, CSS, JS)
4. **Testar** (manual e/ou automatizado)
5. **Documentar** (atualizar README, criar guias)
6. **Commit** (mensagem descritiva)

### Exemplo: Adicionar Nova Dimensão de Análise

#### 1. Criar Spec

```bash
mkdir -p .kiro/specs/nova-dimensao-analise
cd .kiro/specs/nova-dimensao-analise
```

Criar arquivos:
- `requirements.md`: Requisitos da feature
- `design.md`: Design técnico
- `tasks.md`: Tarefas de implementação

#### 2. Atualizar Modelos (se necessário)

`app/models.py`:
```python
class DimensionAnalysis(db.Model):
    __tablename__ = "dimension_analyses"
    
    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey("submissions.id"))
    dimension_name = db.Column(db.String(120), nullable=False)
    average_score = db.Column(db.Float, nullable=False)
    classification = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

#### 3. Criar Service

`app/services/dimension_analyzer.py`:
```python
from typing import Dict, List
from app.models import Submission, Answer
from app.questionnaire import DIMENSIONS
from app.services.scoring import classify_score


class DimensionAnalyzer:
    """Analisa dimensões psicossociais de uma submissão."""
    
    def __init__(self, submission_id: int):
        self.submission_id = submission_id
        self.submission = Submission.query.get(submission_id)
        
    def analyze(self) -> List[Dict]:
        """Retorna análise de todas as dimensões."""
        results = []
        
        for dim_name, q_nums in DIMENSIONS.items():
            avg = self._calculate_dimension_average(q_nums)
            classification = classify_score(avg)
            
            results.append({
                "dimension": dim_name,
                "average": avg,
                "classification": classification,
            })
            
        return results
    
    def _calculate_dimension_average(self, question_numbers: List[int]) -> float:
        """Calcula média de uma dimensão."""
        answers = Answer.query.filter(
            Answer.submission_id == self.submission_id,
            Answer.question_number.in_(question_numbers)
        ).all()
        
        if not answers:
            return 0.0
            
        total = sum(a.score for a in answers)
        return round(total / len(answers), 2)
```

#### 4. Adicionar Rota

`app/routes_admin.py`:
```python
from app.services.dimension_analyzer import DimensionAnalyzer

@admin_bp.route("/submissions/<int:submission_id>/dimensions")
@login_required
def submission_dimensions(submission_id):
    analyzer = DimensionAnalyzer(submission_id)
    dimensions = analyzer.analyze()
    
    return render_template(
        "admin_submission_dimensions.html",
        dimensions=dimensions
    )
```

#### 5. Criar Template

`app/templates/admin_submission_dimensions.html`:
```jinja2
{% extends "base.html" %}

{% block title %}Análise de Dimensões{% endblock %}

{% block content %}
<div class="container">
    <h1>Análise de Dimensões Psicossociais</h1>
    
    <table class="table">
        <thead>
            <tr>
                <th>Dimensão</th>
                <th>Média</th>
                <th>Classificação</th>
            </tr>
        </thead>
        <tbody>
        {% for dim in dimensions %}
            <tr>
                <td>{{ dim.dimension }}</td>
                <td>{{ dim.average }}</td>
                <td class="badge badge-{{ dim.classification|lower }}">
                    {{ dim.classification }}
                </td>
            </tr>
        {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
```

#### 6. Adicionar Estilos

`app/static/css/style.css`:
```css
/* Badges de classificação */
.badge-baixo {
    background-color: #dc3545;
    color: white;
}

.badge-medio {
    background-color: #ffc107;
    color: black;
}

.badge-alto {
    background-color: #28a745;
    color: white;
}
```

#### 7. Testar

```bash
# Rodar servidor
python run.py

# Testar manualmente:
# 1. Fazer login
# 2. Acessar submissão
# 3. Verificar análise de dimensões
```

#### 8. Commit

```bash
git add .
git commit -m "feat: adicionar análise detalhada de dimensões psicossociais"
git push
```

---

## 📊 Specs Existentes

### 1. Company Consolidated NR-1 Chart

**Localização**: `.kiro/specs/company-consolidated-nr1-chart/`

**Descrição**: Gráfico consolidado de distribuição de riscos por empresa.

**Arquivos Modificados**:
- `app/templates/admin_company_nr1.html`
- `app/static/js/submission_detail.js`
- `app/routes_admin.py`

**Tecnologias**:
- Chart.js 4.4.2
- chartjs-plugin-datalabels 2.2.0

**Status**: ✅ Implementado

### 2. Copy Link Button Improvements

**Localização**: `.kiro/specs/copy-link-button-improvements/`

**Descrição**: Melhorias no botão de copiar link do questionário.

**Arquivos Modificados**:
- `app/templates/admin_company_detail.html`
- `app/static/js/main.js`

**Status**: ✅ Implementado

### 3. Mobile Button Overlap Fix

**Localização**: `.kiro/specs/mobile-button-overlap-fix/`

**Descrição**: Correção de sobreposição de botões em dispositivos móveis.

**Arquivos Modificados**:
- `app/static/css/style.css`
- `app/templates/admin_submission_detail.html`

**Status**: ✅ Implementado

### 4. NR-1 PDF Print Fix

**Localização**: `.kiro/specs/nr1-pdf-print-fix/`

**Descrição**: Correção de impressão de PDF com gráficos Chart.js.

**Arquivos Modificados**:
- `app/templates/admin_company_nr1.html`
- `app/static/css/style.css`

**Status**: ✅ Implementado

---

## 🧪 Testes

### Testes Manuais

#### Checklist de Teste Completo

**Fluxo Público**:
- [ ] Acessar link do questionário
- [ ] Preencher dados pessoais
- [ ] Responder 35 questões
- [ ] Submeter formulário
- [ ] Visualizar página de agradecimento

**Fluxo Administrativo**:
- [ ] Fazer login
- [ ] Visualizar dashboard
- [ ] Criar empresa
- [ ] Editar empresa
- [ ] Gerar token de colaborador
- [ ] Visualizar submissões
- [ ] Acessar detalhes de submissão
- [ ] Visualizar gráficos
- [ ] Acessar relatório NR-1
- [ ] Visualizar gráfico consolidado
- [ ] Fazer logout

**Responsividade**:
- [ ] Testar em desktop (1920x1080)
- [ ] Testar em tablet (768x1024)
- [ ] Testar em mobile (375x667)

### Testes Automatizados (Futuro)

Estrutura sugerida:
```
tests/
├── test_models.py          # Testes de modelos
├── test_routes.py          # Testes de rotas
├── test_services.py        # Testes de services
└── test_scoring.py         # Testes de scoring
```

Exemplo:
```python
import pytest
from app import create_app, db
from app.models import Company, Employee
from app.services.scoring import score_for_option, classify_score


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


def test_score_for_option():
    assert score_for_option('1') == 1
    assert score_for_option('5') == 5
    
    with pytest.raises(ValueError):
        score_for_option('6')


def test_classify_score():
    assert classify_score(1.5) == "BAIXO"
    assert classify_score(3.0) == "MÉDIO"
    assert classify_score(4.5) == "ALTO"
```

---

## 📝 Convenções

### Commits

Seguir padrão **Conventional Commits**:

```
<tipo>(<escopo>): <descrição>

[corpo opcional]

[rodapé opcional]
```

**Tipos**:
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação (não afeta código)
- `refactor`: Refatoração
- `test`: Testes
- `chore`: Manutenção

**Exemplos**:
```bash
feat(scoring): adicionar cálculo de percentil
fix(charts): corrigir renderização em mobile
docs(readme): atualizar instruções de deploy
style(css): ajustar espaçamento do header
refactor(services): extrair lógica de NR-1 para service
test(scoring): adicionar testes unitários
chore(deps): atualizar Flask para 3.0.1
```

### Branches

- `main`: Produção (sempre estável)
- `develop`: Desenvolvimento (integração)
- `feature/<nome>`: Nova funcionalidade
- `fix/<nome>`: Correção de bug
- `docs/<nome>`: Documentação

**Exemplo**:
```bash
git checkout -b feature/analise-dimensional
git checkout -b fix/grafico-mobile
git checkout -b docs/guia-deploy
```

### Pull Requests

**Template**:
```markdown
## Descrição
Breve descrição da mudança.

## Tipo de Mudança
- [ ] Nova funcionalidade
- [ ] Correção de bug
- [ ] Documentação
- [ ] Refatoração

## Checklist
- [ ] Código testado manualmente
- [ ] Documentação atualizada
- [ ] Sem erros no console
- [ ] Responsivo (mobile/desktop)

## Screenshots (se aplicável)
[Adicionar screenshots]
```

---

## 🔍 Debugging

### Logs

**Localização**: `instance/logs/app_narcista.log`

**Visualizar em tempo real**:
```bash
tail -f instance/logs/app_narcista.log
```

**Adicionar logs no código**:
```python
from flask import current_app

current_app.logger.info("Mensagem informativa")
current_app.logger.warning("Aviso")
current_app.logger.error("Erro")
current_app.logger.debug("Debug (só aparece se LOG_LEVEL=DEBUG)")
```

### Flask Shell

```bash
flask --app run.py shell
```

```python
>>> from app.models import Company, Submission
>>> Company.query.all()
>>> Submission.query.count()
>>> db.session.query(Submission).filter_by(classification="BAIXO").all()
```

### Debugger

Adicionar breakpoint:
```python
import pdb; pdb.set_trace()
```

Ou usar Flask debugger (desenvolvimento):
```python
# run.py
if __name__ == "__main__":
    app.run(debug=True)
```

---

## 📚 Recursos Úteis

### Documentação Oficial

- **Flask**: https://flask.palletsprojects.com/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **Jinja2**: https://jinja.palletsprojects.com/
- **Chart.js**: https://www.chartjs.org/docs/

### Referências do Projeto

- **HSE-IT**: https://www.hse.gov.uk/stress/standards/
- **NR-1**: https://www.gov.br/trabalho-e-previdencia/pt-br/composicao/orgaos-especificos/secretaria-de-trabalho/inspecao/seguranca-e-saude-no-trabalho/normas-regulamentadoras/nr-01.pdf

### Ferramentas Recomendadas

- **IDE**: VS Code, PyCharm
- **Extensões VS Code**:
  - Python
  - Pylance
  - Jinja
  - SQLite Viewer
- **Ferramentas**:
  - Postman (testar APIs)
  - DB Browser for SQLite (visualizar banco)
  - Chrome DevTools (debug frontend)

---

## 🎯 Checklist para IAs

Ao trabalhar no projeto, sempre:

- [ ] Ler a documentação relevante antes de fazer mudanças
- [ ] Seguir os padrões de código estabelecidos
- [ ] Testar mudanças manualmente
- [ ] Atualizar documentação se necessário
- [ ] Fazer commits descritivos
- [ ] Verificar logs para erros
- [ ] Testar em diferentes dispositivos (se frontend)
- [ ] Verificar impacto em outras partes do sistema

---

**Desenvolvido para**: AMFRA Saúde Mental LTDA  
**Versão**: 2.0  
**Última atualização**: 2024  
**Mantido por**: Equipe de Desenvolvimento + Assistentes de IA
