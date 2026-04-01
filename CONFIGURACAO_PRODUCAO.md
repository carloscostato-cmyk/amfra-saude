# 🚀 Configuração para Produção - AMFRA Saúde Mental

Guia completo para configurar e fazer deploy do sistema AMFRA em ambiente de produção.

## 📋 Índice

1. [Configuração de URLs](#configuração-de-urls)
2. [Variáveis de Ambiente](#variáveis-de-ambiente)
3. [Banco de Dados](#banco-de-dados)
4. [Segurança](#segurança)
5. [Deploy no Railway](#deploy-no-railway)
6. [Deploy em Outras Plataformas](#deploy-em-outras-plataformas)
7. [Troubleshooting](#troubleshooting)

---

## ⚠️ Configuração de URLs

O sistema usa a variável `APP_BASE_URL` para gerar links que serão enviados aos colaboradores.

**NUNCA use `localhost` ou `127.0.0.1` em produção!**

### Identificar o Domínio/IP do Servidor

Você precisa saber qual é o endereço público do seu servidor:

| Cenário | Exemplo de URL |
|---------|----------------|
| Com domínio | `https://amfra.com.br` |
| Com IP público | `http://203.0.113.10:5000` |
| Com subdomínio | `https://app.amfra.com.br` |
| Railway | `https://amfra-saude-mental.railway.app` |
| Heroku | `https://amfra-saude-mental.herokuapp.com` |
| Rede local | `http://192.168.1.100:5000` |

---

## 🔧 Variáveis de Ambiente

### Arquivo `.env` Completo para Produção

```env
# ============================================
# SEGURANÇA
# ============================================
SECRET_KEY=<gerar-chave-forte-32-caracteres>

# ============================================
# URLs E SERVIDOR
# ============================================
APP_BASE_URL=https://amfra.com.br
PREFERRED_URL_SCHEME=https

# ============================================
# BANCO DE DADOS
# ============================================
DATABASE_URL=postgresql+psycopg://usuario:senha@host:5432/amfra_db

# ============================================
# SEGURANÇA DE SESSÃO
# ============================================
SESSION_COOKIE_SECURE=true

# ============================================
# ADMINISTRAÇÃO
# ============================================
AUTO_CREATE_DB=false
AUTO_SEED_ADMIN=false
ADMIN_USERNAME=admin
ADMIN_PASSWORD=<senha-super-forte>

# ============================================
# LOGS
# ============================================
LOG_LEVEL=INFO

# ============================================
# NOTIFICAÇÕES (OPCIONAL)
# ============================================
NOTIFICATION_RECIPIENT_NAME=Dra. Andrea Franco
```

### Descrição das Variáveis

#### Segurança

| Variável | Descrição | Exemplo | Obrigatório |
|----------|-----------|---------|-------------|
| `SECRET_KEY` | Chave secreta para sessões e CSRF | `abc123...` | ✅ Sim |

**Como gerar**:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### URLs e Servidor

| Variável | Descrição | Exemplo | Obrigatório |
|----------|-----------|---------|-------------|
| `APP_BASE_URL` | URL base da aplicação | `https://amfra.com.br` | ✅ Sim |
| `PREFERRED_URL_SCHEME` | Protocolo (http/https) | `https` | ✅ Sim |

#### Banco de Dados

| Variável | Descrição | Exemplo | Obrigatório |
|----------|-----------|---------|-------------|
| `DATABASE_URL` | URL de conexão do banco | `postgresql+psycopg://...` | ✅ Sim (produção) |

**Formatos suportados**:
- PostgreSQL: `postgresql+psycopg://user:pass@host:5432/dbname`
- SQLite (dev): `sqlite:///instance/app_narcista.db` ou vazio

#### Segurança de Sessão

| Variável | Descrição | Valores | Obrigatório |
|----------|-----------|---------|-------------|
| `SESSION_COOKIE_SECURE` | Cookies apenas via HTTPS | `true`/`false` | ✅ Sim (se HTTPS) |

#### Administração

| Variável | Descrição | Valores | Obrigatório |
|----------|-----------|---------|-------------|
| `AUTO_CREATE_DB` | Criar banco automaticamente | `true`/`false` | ❌ Não |
| `AUTO_SEED_ADMIN` | Criar admin automaticamente | `true`/`false` | ❌ Não |
| `ADMIN_USERNAME` | Nome de usuário admin | `admin` | ✅ Sim |
| `ADMIN_PASSWORD` | Senha do admin | `senha123` | ✅ Sim |

**IMPORTANTE**: Em produção, use `AUTO_SEED_ADMIN=false` e crie o admin manualmente:
```bash
flask --app run.py seed-admin
```

#### Logs

| Variável | Descrição | Valores | Obrigatório |
|----------|-----------|---------|-------------|
| `LOG_LEVEL` | Nível de log | `DEBUG`, `INFO`, `WARNING`, `ERROR` | ❌ Não |

---

## 🗄️ Banco de Dados

### SQLite (Desenvolvimento)

Para desenvolvimento local, deixe `DATABASE_URL` vazio ou use:
```env
DATABASE_URL=
```

O sistema criará automaticamente: `instance/app_narcista.db`

### PostgreSQL (Produção)

Para produção, **sempre use PostgreSQL**:

```env
DATABASE_URL=postgresql+psycopg://usuario:senha@host:5432/amfra_db
```

#### Criar Banco PostgreSQL

**Local (Linux/Mac)**:
```bash
# Instalar PostgreSQL
sudo apt-get install postgresql  # Ubuntu/Debian
brew install postgresql          # Mac

# Criar banco
sudo -u postgres createdb amfra_db
sudo -u postgres createuser amfra_user -P

# Dar permissões
sudo -u postgres psql
GRANT ALL PRIVILEGES ON DATABASE amfra_db TO amfra_user;
```

**Railway/Heroku**:
- O banco é criado automaticamente
- A variável `DATABASE_URL` é configurada automaticamente

#### Inicializar Banco

```bash
# Criar tabelas
flask --app run.py init-db

# Criar admin
flask --app run.py seed-admin
```

#### Backup do Banco

**PostgreSQL**:
```bash
# Backup
pg_dump -U usuario -h host amfra_db > backup.sql

# Restaurar
psql -U usuario -h host amfra_db < backup.sql
```

**SQLite**:
```bash
# Backup (copiar arquivo)
cp instance/app_narcista.db backup_$(date +%Y%m%d).db
```

---

## 🔒 Segurança

### Checklist de Segurança

- [ ] `SECRET_KEY` forte e aleatório (mínimo 32 caracteres)
- [ ] `ADMIN_PASSWORD` forte (letras, números, símbolos)
- [ ] `SESSION_COOKIE_SECURE=true` (se HTTPS)
- [ ] `PREFERRED_URL_SCHEME=https` (se HTTPS)
- [ ] `AUTO_SEED_ADMIN=false` (criar admin manualmente)
- [ ] PostgreSQL em produção (não SQLite)
- [ ] Backup automático do banco configurado
- [ ] Logs monitorados
- [ ] Firewall configurado
- [ ] HTTPS habilitado (certificado SSL)
- [ ] Variáveis de ambiente não commitadas no Git

### Gerar Credenciais Fortes

**SECRET_KEY**:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**ADMIN_PASSWORD**:
```bash
python -c "import secrets; print(secrets.token_urlsafe(16))"
```

### Configurar HTTPS

**Com Nginx**:
```nginx
server {
    listen 443 ssl;
    server_name amfra.com.br;

    ssl_certificate /etc/letsencrypt/live/amfra.com.br/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/amfra.com.br/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Com Let's Encrypt**:
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d amfra.com.br
```

---

## 🚂 Deploy no Railway

Railway é a plataforma recomendada para deploy rápido e fácil.

### Passo a Passo

#### 1. Criar Conta
- Acesse: https://railway.app
- Faça login com GitHub

#### 2. Criar Novo Projeto
- Clique em "New Project"
- Selecione "Deploy from GitHub repo"
- Escolha o repositório do AMFRA

#### 3. Adicionar PostgreSQL
- No projeto, clique em "New"
- Selecione "Database" → "PostgreSQL"
- O Railway criará automaticamente e configurará `DATABASE_URL`

#### 4. Configurar Variáveis de Ambiente

No painel do Railway, vá em "Variables" e adicione:

```env
SECRET_KEY=<gerar-com-comando-python>
ADMIN_USERNAME=admin
ADMIN_PASSWORD=<senha-forte>
APP_BASE_URL=https://${{RAILWAY_PUBLIC_DOMAIN}}
PREFERRED_URL_SCHEME=https
SESSION_COOKIE_SECURE=true
AUTO_CREATE_DB=true
AUTO_SEED_ADMIN=true
LOG_LEVEL=INFO
```

**IMPORTANTE**: Use `${{RAILWAY_PUBLIC_DOMAIN}}` para pegar automaticamente o domínio do Railway.

#### 5. Deploy

- O Railway fará deploy automaticamente
- Aguarde o build completar
- Acesse a URL fornecida (exemplo: `https://amfra-saude-mental.railway.app`)

#### 6. Inicializar Banco (se necessário)

Se `AUTO_CREATE_DB=false`:

```bash
# Conectar ao Railway CLI
railway login
railway link

# Inicializar banco
railway run flask --app run.py init-db

# Criar admin
railway run flask --app run.py seed-admin
```

#### 7. Configurar Domínio Customizado (Opcional)

- No Railway, vá em "Settings" → "Domains"
- Clique em "Add Domain"
- Configure o DNS do seu domínio:
  - Tipo: `CNAME`
  - Nome: `@` ou `app`
  - Valor: `<seu-projeto>.railway.app`

### Monitoramento no Railway

- **Logs**: Aba "Deployments" → Clique no deploy → "View Logs"
- **Métricas**: Aba "Metrics" (CPU, memória, rede)
- **Banco**: Aba "PostgreSQL" → "Data" (visualizar tabelas)

---

## 🌐 Deploy em Outras Plataformas

### Heroku

```bash
# Instalar Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Criar app
heroku create amfra-saude-mental

# Adicionar PostgreSQL
heroku addons:create heroku-postgresql:mini

# Configurar variáveis
heroku config:set SECRET_KEY=<chave>
heroku config:set ADMIN_USERNAME=admin
heroku config:set ADMIN_PASSWORD=<senha>
heroku config:set APP_BASE_URL=https://amfra-saude-mental.herokuapp.com
heroku config:set PREFERRED_URL_SCHEME=https
heroku config:set SESSION_COOKIE_SECURE=true

# Deploy
git push heroku main

# Inicializar banco
heroku run flask --app run.py init-db
heroku run flask --app run.py seed-admin
```

### AWS Elastic Beanstalk

```bash
# Instalar EB CLI
pip install awsebcli

# Inicializar
eb init -p python-3.10 amfra-saude-mental

# Criar ambiente
eb create amfra-production

# Configurar variáveis
eb setenv SECRET_KEY=<chave> ADMIN_USERNAME=admin ADMIN_PASSWORD=<senha>

# Deploy
eb deploy
```

### Google Cloud Run

```bash
# Criar Dockerfile (se não existir)
# Fazer build
gcloud builds submit --tag gcr.io/PROJECT_ID/amfra

# Deploy
gcloud run deploy amfra \
  --image gcr.io/PROJECT_ID/amfra \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars SECRET_KEY=<chave>,ADMIN_USERNAME=admin
```

### Servidor VPS (Ubuntu)

```bash
# Instalar dependências
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv postgresql nginx

# Clonar repositório
git clone <repo-url> /var/www/amfra
cd /var/www/amfra

# Criar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configurar .env
cp .env.example .env
nano .env  # Editar variáveis

# Inicializar banco
flask --app run.py init-db
flask --app run.py seed-admin

# Configurar systemd
sudo nano /etc/systemd/system/amfra.service
```

**amfra.service**:
```ini
[Unit]
Description=AMFRA Saude Mental
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/amfra
Environment="PATH=/var/www/amfra/.venv/bin"
ExecStart=/var/www/amfra/.venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 "app:create_app()"

[Install]
WantedBy=multi-user.target
```

```bash
# Iniciar serviço
sudo systemctl start amfra
sudo systemctl enable amfra

# Configurar Nginx (ver seção HTTPS acima)
```

---

## 🔍 Troubleshooting

### Problema: Links com `localhost` sendo enviados

**Causa**: `APP_BASE_URL` ainda está com `127.0.0.1`

**Solução**:
1. Edite `.env` e altere `APP_BASE_URL`
2. Reinicie o servidor: `python run.py`

### Problema: Colaboradores não conseguem acessar o link

**Causa**: URL usa IP local ou porta bloqueada

**Solução**:
1. Verifique se o servidor está acessível externamente
2. Configure port forwarding no roteador (se necessário)
3. Use um domínio público ou Railway/Heroku

### Problema: Erro 500 ao acessar o sistema

**Causa**: Banco não inicializado ou variáveis incorretas

**Solução**:
1. Verifique logs: `instance/logs/app_narcista.log`
2. Inicialize banco: `flask --app run.py init-db`
3. Verifique `.env`

### Problema: Erro de conexão com PostgreSQL

**Causa**: `DATABASE_URL` incorreta ou banco não acessível

**Solução**:
1. Verifique formato: `postgresql+psycopg://user:pass@host:5432/db`
2. Teste conexão: `psql -U user -h host -d db`
3. Verifique firewall

### Problema: Gráficos não aparecem

**Causa**: Chart.js não carregando

**Solução**:
1. Verifique console do navegador (F12)
2. Verifique se CDN está acessível
3. Limpe cache do navegador

### Problema: Sessão expira muito rápido

**Causa**: `PERMANENT_SESSION_LIFETIME` muito curto

**Solução**:
Edite `config.py`:
```python
PERMANENT_SESSION_LIFETIME = timedelta(hours=24)  # 24 horas
```

---

## 📊 Monitoramento e Logs

### Visualizar Logs

**Local**:
```bash
# Tempo real
tail -f instance/logs/app_narcista.log

# Últimas 100 linhas
tail -n 100 instance/logs/app_narcista.log

# Filtrar erros
grep ERROR instance/logs/app_narcista.log
```

**Railway**:
- Aba "Deployments" → Clique no deploy → "View Logs"

**Heroku**:
```bash
heroku logs --tail
```

### Métricas

**Railway**: Aba "Metrics"
**Heroku**: `heroku ps` ou dashboard web
**AWS**: CloudWatch

---

## 🎯 Checklist Final de Deploy

- [ ] `.env` configurado com todas as variáveis
- [ ] `APP_BASE_URL` com domínio/IP público
- [ ] `SECRET_KEY` forte e aleatório
- [ ] `ADMIN_PASSWORD` forte
- [ ] PostgreSQL configurado
- [ ] Banco inicializado (`flask init-db`)
- [ ] Admin criado (`flask seed-admin`)
- [ ] HTTPS configurado (se aplicável)
- [ ] `SESSION_COOKIE_SECURE=true` (se HTTPS)
- [ ] Firewall configurado
- [ ] Backup automático configurado
- [ ] Logs monitorados
- [ ] Testado em dispositivo externo
- [ ] Documentação atualizada

---

**Desenvolvido para**: AMFRA Saúde Mental LTDA  
**Versão**: 2.0  
**Última atualização**: 2024
