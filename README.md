# APP AMFRA

Sistema web completo para transformar um questionário clínico em uma aplicação real com:

- formulário público responsivo para o paciente
- painel administrativo protegido para o Doutor
- scoring automático com classificação clínica
- gráfico horizontal por pergunta com Chart.js
- persistência em banco relacional
- estrutura pronta para usar SQLite localmente e PostgreSQL em produção
- integração desacoplada com WhatsApp Cloud API da Meta, com fallback controlado

## Stack

- Python 3
- Flask
- Jinja2
- Flask-SQLAlchemy
- Flask-WTF
- Flask-Login
- SQLite no local
- PostgreSQL em produção via `DATABASE_URL`
- Chart.js
- HTML5, CSS3 e JavaScript

## Estrutura

```text
app/
  __init__.py
  extensions.py
  forms.py
  models.py
  questionnaire.py
  routes_admin.py
  routes_public.py
  services/
    __init__.py
    links.py
    scoring.py
    whatsapp.py
  templates/
    base.html
    public_form.html
    thank_you.html
    admin_login.html
    admin_dashboard.html
    admin_submission_detail.html
    errors/
      404.html
      500.html
  static/
    css/
      style.css
    js/
      main.js
      submission_detail.js
    img/
config.py
run.py
requirements.txt
.env.example
README.md
```

## Regras implementadas

- 10 perguntas
- 4 alternativas por pergunta
- pontuação fixa:
  - A = 1
  - B = 2
  - C = 3
  - D = 4
- classificação:
  - 10 a 15 = `RELACIONAMENTO SAUDÁVEL`
  - 16 a 25 = `ATENÇÃO: PADRÕES PREOCUPANTES`
  - 26 a 35 = `ALERTA: SINAIS NARCÍSICOS SIGNIFICATIVOS`
  - 36 a 40 = `CRÍTICO: ABUSO NARCÍSICO — INTERVENÇÃO NECESSÁRIA`

## Novidades: Gráfico Consolidado NR-1 📊

A partir de 2024, o sistema inclui um **gráfico consolidado de distribuição de riscos** na página de relatório NR-1 da empresa.

### Características:
- 📊 Gráfico de barras horizontais
- 🎨 Cores intuitivas: vermelho (BAIXO), amarelo (MÉDIO), verde (ALTO)
- 📈 Exibe contagem e percentual para cada nível
- 📱 Totalmente responsivo (desktop e mobile)
- ♿ Acessível (ARIA labels, screen readers)
- ⚡ Rápido (< 500ms de renderização)

### Tecnologias:
- Chart.js 4.4.2
- chartjs-plugin-datalabels 2.2.0

### Documentação:
- Resumo: `RESUMO_GRAFICO_NR1.md`
- Deploy: `DEPLOY_GRAFICO_NR1.md`
- Documentação completa: `.kiro/specs/company-consolidated-nr1-chart/`

### Teste:
```bash
python test_consolidated_chart.py
```


## Modelos principais

- `AdminUser`
- `Submission`
- `Answer`
- `NotificationLog`

## Segurança e privacidade

- proteção CSRF em formulários e logout
- autenticação administrativa com senha em hash
- sessões protegidas
- link administrativo com UUID + token seguro não enumerável
- validação server-side
- segredos via variáveis de ambiente
- logs sem exposição de tokens da API
- fallback controlado para falhas externas do WhatsApp

## Como executar localmente

### 1. Criar ambiente virtual

No PowerShell:

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Instalar dependências

```powershell
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente

```powershell
Copy-Item .env.example .env
```

Edite o arquivo `.env` com pelo menos:

- `SECRET_KEY`
- `ADMIN_USERNAME`
- `ADMIN_PASSWORD`

Se quiser que o admin seja criado automaticamente no boot local:

- defina `AUTO_SEED_ADMIN=true`

### 4. Rodar a aplicação

Recomendado (Windows, production-capable):

```powershell
python serve.py
```

Fallback (development builtin server):

```powershell
python run.py
```

Por padrão o app sobe em:

- [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Comandos úteis

Inicializar o banco manualmente:

```powershell
flask --app run.py init-db
```

Criar administrador manualmente:

```powershell
flask --app run.py seed-admin
```

## Fluxo esperado

1. O paciente acessa o formulário público.
2. Preenche nome, data e as 10 respostas.
3. O sistema salva `Submission` e `Answer`.
4. O scoring calcula pontuação total, classificação e interpretação.
5. O paciente é redirecionado para a página “Muito obrigado”.
6. O serviço de WhatsApp tenta notificar o Doutor com link privado do detalhe.
7. O Doutor entra na área admin, abre o detalhe e visualiza:
   - respostas selecionadas
   - score por pergunta
   - score total
   - classificação
   - interpretação
   - gráfico horizontal

## Integração com WhatsApp Cloud API

O envio é feito no back-end pelo serviço `WhatsAppService`.

Se a API não estiver configurada:

- o sistema continua funcionando
- a submissão é salva normalmente
- o envio é registrado como `pending_configuration` ou `disabled`
- o histórico fica disponível em `NotificationLog`

### Variáveis necessárias para ativar o envio real

Preencha no `.env`:

- `WHATSAPP_ENABLED=true`
- `WHATSAPP_ACCESS_TOKEN=<token da Meta>`
- `WHATSAPP_PHONE_NUMBER_ID=<phone number id do WhatsApp Business>`
- `WHATSAPP_DESTINATION_NUMBER=5511985879829`

O endpoint usado segue o padrão oficial:

- `https://graph.facebook.com/<VERSAO>/<PHONE_NUMBER_ID>/messages`

### Payload enviado

Mensagem de texto para o Doutor com o seguinte formato:

```text
A avaliação RN1 de {NOME_DO_PACIENTE} foi respondida e está disponível para o Doutor em: {URL_PRIVADA_DA_RESPOSTA}
```

## Banco local e produção

### SQLite local

Por padrão, deixando `DATABASE_URL` vazio:

- o app usa automaticamente o arquivo local `instance/app_narcista.db`
- caminhos relativos de SQLite também são normalizados para o diretório do projeto

### PostgreSQL em produção

Basta trocar:

- `DATABASE_URL=postgresql+psycopg://usuario:senha@host:5432/banco`

Nenhuma rota precisa ser alterada.

## Sugestão de teste local

1. Rode `python run.py`
2. Abra [http://127.0.0.1:5000](http://127.0.0.1:5000)
3. Envie um formulário com respostas variadas
4. Acesse [http://127.0.0.1:5000/admin/login](http://127.0.0.1:5000/admin/login)
5. Entre com o usuário admin configurado
6. Abra a resposta recém-criada
7. Confira tabela, score, classificação, interpretação e gráfico
8. Valide o status da notificação do WhatsApp no detalhe da submissão

## Observações de deploy

- use `SECRET_KEY` forte em produção
- habilite `SESSION_COOKIE_SECURE=true` atrás de HTTPS
- use PostgreSQL em produção
- considere adicionar Flask-Migrate em um próximo passo para versionamento formal do schema
- por lidar com dados sensíveis, revise base legal, retenção, consentimento e política de acesso conforme LGPD
