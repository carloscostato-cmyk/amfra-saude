# AMFRA Saúde Mental - Sistema de Avaliação Psicossocial NR-1 (HSE-IT)

Sistema web profissional para avaliação de riscos psicossociais em ambientes de trabalho, baseado no questionário HSE-IT (Health Safety Executive Indicator Tool) com 35 perguntas e 7 dimensões psicossociais, em conformidade com a NR-1.

## 🎯 Funcionalidades Principais

### Avaliação Psicossocial
- ✅ **Questionário HSE-IT completo** (35 perguntas, escala Likert 1-5)
- ✅ **7 dimensões psicossociais**: Demandas, Controle, Apoio da Chefia, Apoio dos Colegas, Relacionamentos, Cargo, Comunicação e Mudanças
- ✅ **Scoring automático** com classificação em 3 níveis (BAIXO, MÉDIO, ALTO)
- ✅ **Análise dimensional** detalhada por dimensão e questão
- ✅ **Validação de formulário** com destaque visual de erros

### Gestão Empresarial
- ✅ **Gestão de empresas** com tokens únicos
- ✅ **Gestão de colaboradores** com tokens individuais
- ✅ **Relatórios NR-1** consolidados por empresa
- ✅ **Análise de participação** e distribuição de riscos

### Visualização e Relatórios
- ✅ **Gráficos profissionais** (barras horizontais + radar Chart.js)
- ✅ **Gráfico consolidado NR-1** com distribuição de riscos por empresa
- ✅ **Geração de PDF** profissional com rodapé e branding
- ✅ **Interface responsiva** (desktop e mobile)

### Administração
- ✅ **Painel administrativo** protegido com autenticação
- ✅ **Dashboard** com visão geral de empresas e submissões
- ✅ **Detalhamento individual** de cada avaliação
- ✅ **Links compartilháveis** para questionários

## 🏗️ Arquitetura e Tecnologias

### Backend
- **Python 3.10+**
- **Flask 3.0** - Framework web
- **Flask-SQLAlchemy** - ORM para banco de dados
- **Flask-Login** - Autenticação de usuários
- **Flask-WTF** - Formulários e proteção CSRF
- **Gunicorn** - Servidor WSGI para produção

### Frontend
- **Jinja2** - Template engine
- **HTML5, CSS3** - Interface responsiva
- **JavaScript (ES6+)** - Interatividade
- **Chart.js 4.4.2** - Gráficos profissionais
- **chartjs-plugin-datalabels 2.2.0** - Labels em gráficos

### Banco de Dados
- **SQLite** - Desenvolvimento local
- **PostgreSQL** - Produção (via DATABASE_URL)

## 📁 Estrutura do Projeto

```
amfra-saude-mental/
├── app/
│   ├── __init__.py              # Factory da aplicação Flask
│   ├── extensions.py            # Extensões (db, csrf, login_manager)
│   ├── models.py                # Modelos do banco (Company, Employee, Submission, Answer)
│   ├── forms.py                 # Formulários WTForms
│   ├── questionnaire.py         # Definição do HSE-IT (35 perguntas, dimensões)
│   ├── routes_admin.py          # Rotas administrativas
│   ├── routes_public.py         # Rotas públicas (questionário)
│   ├── services/
│   │   ├── nr1_agent.py         # Análise consolidada NR-1
│   │   ├── scoring.py           # Cálculo de scores e classificações
│   │   └── links.py             # Geração de URLs
│   ├── templates/
│   │   ├── base.html            # Template base
│   │   ├── public_form.html     # Formulário público
│   │   ├── thank_you.html       # Página de agradecimento
│   │   ├── admin_login.html     # Login administrativo
│   │   ├── admin_dashboard.html # Dashboard principal
│   │   ├── admin_company_detail.html      # Detalhes da empresa
│   │   ├── admin_company_nr1.html         # Relatório NR-1
│   │   ├── admin_submission_detail.html   # Detalhes da submissão
│   │   └── errors/              # Páginas de erro (404, 500)
│   └── static/
│       ├── css/
│       │   └── style.css        # Estilos principais
│       ├── js/
│       │   ├── main.js          # Scripts gerais
│       │   └── submission_detail.js  # Scripts de detalhes
│       └── img/                 # Imagens e logos
├── instance/
│   ├── app_narcista.db          # Banco SQLite (local)
│   └── logs/                    # Logs da aplicação
├── .kiro/
│   └── specs/                   # Especificações de features
├── config.py                    # Configurações da aplicação
├── run.py                       # Ponto de entrada (desenvolvimento)
├── requirements.txt             # Dependências Python
├── .env.example                 # Exemplo de variáveis de ambiente
├── README.md                    # Este arquivo
├── IMPORTANTE_LEIA_ANTES_DE_USAR.md  # Guia rápido de produção
├── CONFIGURACAO_PRODUCAO.md     # Guia detalhado de deploy
└── DOCUMENTACAO_PARA_IA.md      # Guia para IAs trabalharem no projeto
```

## 🚀 Como Executar Localmente

### 1. Pré-requisitos
- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)

### 2. Clonar o repositório
```bash
git clone <url-do-repositorio>
cd amfra-saude-mental
```

### 3. Criar ambiente virtual
```powershell
# Windows PowerShell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Instalar dependências
```bash
pip install -r requirements.txt
```

### 5. Configurar variáveis de ambiente
```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar .env com suas configurações
```

Variáveis mínimas necessárias:
```env
SECRET_KEY=sua-chave-secreta-forte-aqui
ADMIN_USERNAME=admin
ADMIN_PASSWORD=senha-forte-aqui
AUTO_SEED_ADMIN=true
```

### 6. Inicializar banco de dados
```bash
flask --app run.py init-db
```

### 7. Rodar a aplicação
```bash
# Desenvolvimento
python run.py

# Produção (recomendado)
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

A aplicação estará disponível em: http://127.0.0.1:5000

## 📊 Modelo de Dados

### Principais Entidades

**Company** (Empresa)
- `id`: Identificador único
- `name`: Nome da empresa
- `employee_count`: Número de colaboradores
- `token`: Token único para acesso ao questionário
- `created_at`: Data de criação

**Employee** (Colaborador)
- `id`: Identificador único
- `company_id`: Referência à empresa
- `first_name`: Primeiro nome
- `last_name`: Sobrenome
- `created_at`: Data de criação

**Submission** (Submissão)
- `id`: Identificador único
- `employee_id`: Referência ao colaborador
- `questionnaire_date`: Data do preenchimento
- `total_score`: Pontuação total (soma bruta)
- `classification`: Classificação (BAIXO, MÉDIO, ALTO)
- `interpretation`: Interpretação textual
- `created_at`: Data de criação

**Answer** (Resposta)
- `id`: Identificador único
- `submission_id`: Referência à submissão
- `question_number`: Número da questão (1-35)
- `question_text`: Texto da questão
- `selected_option`: Opção selecionada (1-5)
- `selected_text`: Texto da opção
- `score`: Pontuação (1-5)

## 🎓 Metodologia HSE-IT

### Escala Likert
- **1** = Nunca
- **2** = Raramente
- **3** = Às vezes
- **4** = Frequentemente
- **5** = Sempre

### Classificação por Média
- **BAIXO**: 1,00 a 2,29 (risco alto, intervenção prioritária)
- **MÉDIO**: 2,30 a 3,69 (risco moderado, atenção necessária)
- **ALTO**: 3,70 a 5,00 (risco baixo, ambiente saudável)

### 7 Dimensões Psicossociais

1. **DEMANDAS** (8 questões): Carga de trabalho, prazos, intensidade
2. **CONTROLE** (6 questões): Autonomia, flexibilidade, decisão
3. **APOIO DA CHEFIA** (5 questões): Suporte, incentivo, comunicação
4. **APOIO DOS COLEGAS** (4 questões): Colaboração, respeito, ajuda
5. **RELACIONAMENTOS** (4 questões): Conflitos, perseguição, tensão
6. **CARGO** (5 questões): Clareza de papéis, objetivos, responsabilidades
7. **COMUNICAÇÃO E MUDANÇAS** (3 questões): Consulta, explicações, adaptação

## 🔐 Segurança e Privacidade

- ✅ Proteção CSRF em todos os formulários
- ✅ Autenticação administrativa com senha em hash (Werkzeug)
- ✅ Sessões protegidas com cookies HttpOnly
- ✅ Tokens não enumeráveis (UUID)
- ✅ Validação server-side de todos os inputs
- ✅ Segredos via variáveis de ambiente
- ✅ Logs sem exposição de dados sensíveis
- ✅ Conformidade com LGPD (recomenda-se revisão legal)

## 🌐 Deploy em Produção

### Railway (Recomendado)

1. **Criar conta no Railway**: https://railway.app
2. **Criar novo projeto** e conectar repositório GitHub
3. **Adicionar PostgreSQL** ao projeto
4. **Configurar variáveis de ambiente**:
   ```env
   SECRET_KEY=<gerar-chave-forte>
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=<senha-forte>
   APP_BASE_URL=https://seu-app.railway.app
   PREFERRED_URL_SCHEME=https
   SESSION_COOKIE_SECURE=true
   DATABASE_URL=<fornecido-automaticamente-pelo-railway>
   ```
5. **Deploy automático** será feito a cada push

### Outras Plataformas

O sistema é compatível com:
- Heroku
- AWS Elastic Beanstalk
- Google Cloud Run
- Azure App Service
- Qualquer servidor com Python 3.10+ e PostgreSQL

Consulte `CONFIGURACAO_PRODUCAO.md` para detalhes.

## 🔧 Comandos Úteis

### Banco de Dados
```bash
# Inicializar banco
flask --app run.py init-db

# Recriar banco (APAGA TODOS OS DADOS)
flask --app run.py repair-db

# Criar administrador manualmente
flask --app run.py seed-admin
```

### Desenvolvimento
```bash
# Rodar servidor de desenvolvimento
python run.py

# Rodar com Gunicorn (produção)
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"

# Ativar ambiente virtual
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate    # Linux/Mac
```

## 📝 Fluxo de Uso

### Para Colaboradores
1. Receber link do questionário (via empresa)
2. Acessar link com token único
3. Preencher dados pessoais (nome, sobrenome)
4. Responder 35 questões do HSE-IT
5. Submeter formulário
6. Visualizar página de agradecimento

### Para Administradores
1. Acessar `/admin/login`
2. Fazer login com credenciais
3. Visualizar dashboard com empresas
4. Criar/editar empresas
5. Gerar tokens para colaboradores
6. Visualizar submissões individuais
7. Acessar relatório NR-1 consolidado
8. Exportar PDF (se implementado)

## 📈 Gráfico Consolidado NR-1

Recurso implementado para visualização da distribuição de riscos por empresa.

### Características
- 📊 Gráfico de barras horizontais
- 🎨 Cores intuitivas: vermelho (BAIXO), amarelo (MÉDIO), verde (ALTO)
- 📈 Exibe contagem e percentual para cada nível
- 📱 Totalmente responsivo
- ♿ Acessível (ARIA labels)
- ⚡ Renderização rápida (< 500ms)

### Documentação Técnica
- Especificação completa: `.kiro/specs/company-consolidated-nr1-chart/`
- Design: `.kiro/specs/company-consolidated-nr1-chart/design.md`
- Requisitos: `.kiro/specs/company-consolidated-nr1-chart/requirements.md`

## 🐛 Correções Recentes

### PDF Print Fix
- Correção de impressão de PDF com gráficos
- Especificação: `.kiro/specs/nr1-pdf-print-fix/`

### Mobile Button Overlap Fix
- Correção de sobreposição de botões em mobile
- Especificação: `.kiro/specs/mobile-button-overlap-fix/`

### Copy Link Button Improvements
- Melhorias no botão de copiar link
- Especificação: `.kiro/specs/copy-link-button-improvements/`

## 🤝 Contribuindo

Para contribuir com o projeto:

1. Leia `DOCUMENTACAO_PARA_IA.md` para entender padrões de código
2. Crie uma branch para sua feature: `git checkout -b feature/nova-funcionalidade`
3. Faça commit das mudanças: `git commit -m "feat: adicionar nova funcionalidade"`
4. Push para a branch: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

### Padrões de Commit
- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Documentação
- `style:` Formatação
- `refactor:` Refatoração
- `test:` Testes
- `chore:` Manutenção

## 📚 Documentação Adicional

- **IMPORTANTE_LEIA_ANTES_DE_USAR.md**: Guia rápido para configuração de produção
- **CONFIGURACAO_PRODUCAO.md**: Guia detalhado de deploy e configuração
- **DOCUMENTACAO_PARA_IA.md**: Guia para IAs trabalharem no projeto
- **.kiro/specs/**: Especificações técnicas de features

## 🆘 Suporte e Troubleshooting

### Problema: Links com localhost sendo enviados
**Solução**: Configure `APP_BASE_URL` no `.env` com o domínio/IP público

### Problema: Banco de dados não inicializa
**Solução**: Execute `flask --app run.py init-db`

### Problema: Erro de autenticação
**Solução**: Verifique `ADMIN_USERNAME` e `ADMIN_PASSWORD` no `.env`

### Problema: Gráficos não aparecem
**Solução**: Verifique se Chart.js está carregando (console do navegador)

### Logs
Verifique os logs em: `instance/logs/app_narcista.log`

## 📄 Licença

Este projeto é proprietário da AMFRA Saúde Mental LTDA.

## 👥 Credenciais Padrão

**IMPORTANTE**: Altere as credenciais padrão em produção!

- **Usuário**: definido em `ADMIN_USERNAME` (.env)
- **Senha**: definida em `ADMIN_PASSWORD` (.env)

## 🔗 Links Úteis

- **Documentação Flask**: https://flask.palletsprojects.com/
- **Chart.js**: https://www.chartjs.org/
- **HSE-IT**: https://www.hse.gov.uk/stress/standards/
- **NR-1**: https://www.gov.br/trabalho-e-previdencia/pt-br/composicao/orgaos-especificos/secretaria-de-trabalho/inspecao/seguranca-e-saude-no-trabalho/normas-regulamentadoras/nr-01.pdf

---

**Desenvolvido para**: AMFRA Saúde Mental LTDA  
**Versão**: 2.0  
**Última atualização**: 2024
