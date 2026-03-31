# 🚀 Configuração para Produção - AMFRA

## ⚠️ IMPORTANTE: Configuração de URLs

O sistema usa a variável `APP_BASE_URL` para gerar links que serão enviados aos pacientes e ao WhatsApp. 

**NUNCA use `localhost` ou `127.0.0.1` em produção!**

---

## 📋 Passo a Passo para Configuração

### 1. Identifique o Domínio/IP do Servidor

Você precisa saber qual é o endereço público do seu servidor. Exemplos:

- **Com domínio**: `https://AMFRA.com.br`
- **Com IP público**: `http://192.168.1.100:5001`
- **Com subdomínio**: `https://app.AMFRA.com.br`

### 2. Edite o arquivo `.env`

Abra o arquivo `.env` e altere as seguintes linhas:

```env
# ❌ ERRADO (desenvolvimento local)
APP_BASE_URL=http://127.0.0.1:5000
APP_PORT=5001
PREFERRED_URL_SCHEME=http
SESSION_COOKIE_SECURE=false

# ✅ CORRETO (produção com domínio e HTTPS)
APP_BASE_URL=https://AMFRA.com.br
APP_PORT=5001
PREFERRED_URL_SCHEME=https
SESSION_COOKIE_SECURE=true

# ✅ CORRETO (produção com IP na rede local)
APP_BASE_URL=http://192.168.1.100:5001
APP_PORT=5001
PREFERRED_URL_SCHEME=http
SESSION_COOKIE_SECURE=false
```

### 3. Configure o SECRET_KEY

Em produção, SEMPRE use uma chave secreta forte:

```env
# ❌ ERRADO
SECRET_KEY=dev-secret-change-before-production-7b2f6f2e4f7a

# ✅ CORRETO (gere uma chave aleatória)
SECRET_KEY=sua-chave-super-secreta-e-aleatoria-aqui-com-pelo-menos-32-caracteres
```

**Como gerar uma chave segura:**

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 4. Configure o Banco de Dados (Produção)

Para produção, use PostgreSQL:

```env
# ❌ ERRADO (SQLite é só para desenvolvimento)
DATABASE_URL=

# ✅ CORRETO (PostgreSQL)
DATABASE_URL=postgresql+psycopg://usuario:senha@localhost:5432/AMFRA_db
```

### 5. Configure o WhatsApp (Opcional)

Se quiser ativar notificações via WhatsApp:

```env
WHATSAPP_ENABLED=true
WHATSAPP_ACCESS_TOKEN=seu_token_da_meta_aqui
WHATSAPP_PHONE_NUMBER_ID=seu_phone_number_id_aqui
WHATSAPP_DESTINATION_NUMBER=5511985879829
```

---

## 🔍 Como Verificar se Está Correto

### Teste 1: Verificar o Link do Questionário

1. Faça login no admin
2. Na dashboard, copie o "Link para paciente"
3. O link deve começar com seu domínio/IP público:
   - ✅ `https://AMFRA.com.br/questionario-pessoal`
   - ✅ `http://192.168.1.100:5001/questionario-pessoal`
   - ❌ `http://127.0.0.1:5000/questionario-pessoal`

### Teste 2: Verificar Notificação WhatsApp

1. Preencha um formulário de teste
2. Verifique o log de notificação no detalhe da submissão
3. A URL enviada deve usar seu domínio/IP público

---

## 🌐 Cenários Comuns

### Cenário 1: Servidor na Nuvem (AWS, Azure, etc.)

```env
APP_BASE_URL=https://seu-dominio.com.br
PREFERRED_URL_SCHEME=https
SESSION_COOKIE_SECURE=true
```

### Cenário 2: Servidor Local na Rede da Clínica

```env
APP_BASE_URL=http://192.168.1.100:5001
PREFERRED_URL_SCHEME=http
SESSION_COOKIE_SECURE=false
```

### Cenário 3: Desenvolvimento Local (Testes)

```env
APP_BASE_URL=http://127.0.0.1:5001
PREFERRED_URL_SCHEME=http
SESSION_COOKIE_SECURE=false
```

---

## 🔒 Checklist de Segurança para Produção

- [ ] `SECRET_KEY` alterado para valor aleatório forte
- [ ] `APP_BASE_URL` configurado com domínio/IP público
- [ ] `SESSION_COOKIE_SECURE=true` se usar HTTPS
- [ ] `ADMIN_PASSWORD` alterado para senha forte
- [ ] `DATABASE_URL` configurado com PostgreSQL
- [ ] `AUTO_SEED_ADMIN=false` (criar admin manualmente)
- [ ] Certificado SSL configurado (se usar HTTPS)
- [ ] Firewall configurado para permitir apenas portas necessárias

---

## 🆘 Problemas Comuns

### Problema: Links com `localhost` sendo enviados

**Causa**: `APP_BASE_URL` ainda está com `127.0.0.1`

**Solução**: 
1. Edite `.env` e altere `APP_BASE_URL`
2. Reinicie o servidor: `python run.py`

### Problema: Paciente não consegue acessar o link

**Causa**: URL usa IP local ou porta bloqueada

**Solução**:
1. Verifique se o servidor está acessível externamente
2. Configure port forwarding no roteador (se necessário)
3. Use um domínio público ou serviço como ngrok para testes

### Problema: WhatsApp não envia notificações

**Causa**: URL inválida ou credenciais incorretas

**Solução**:
1. Verifique `WHATSAPP_ENABLED=true`
2. Confirme `WHATSAPP_ACCESS_TOKEN` e `WHATSAPP_PHONE_NUMBER_ID`
3. Teste a URL manualmente no navegador

---

## 📞 Suporte

Se precisar de ajuda, verifique:
1. Os logs em `instance/logs/app_narcista.log`
2. A configuração do `.env`
3. Se o servidor está acessível na rede

---

## 🎯 Exemplo Completo de `.env` para Produção

```env
# Segurança
SECRET_KEY=gere-uma-chave-aleatoria-forte-aqui-32-caracteres-minimo

# URLs e Servidor
APP_BASE_URL=https://AMFRA.com.br
APP_PORT=5001
PREFERRED_URL_SCHEME=https

# Banco de Dados
DATABASE_URL=postgresql+psycopg://AMFRA_user:senha_forte@localhost:5432/AMFRA_db

# Segurança de Sessão
SESSION_COOKIE_SECURE=true

# Banco e Admin
AUTO_CREATE_DB=false
AUTO_SEED_ADMIN=false
ADMIN_USERNAME=dra_andrea
ADMIN_PASSWORD=senha-super-forte-aqui

# Logs
LOG_LEVEL=INFO

# WhatsApp
NOTIFICATION_RECIPIENT_NAME=Dra. Andrea Franco
WHATSAPP_ENABLED=true
WHATSAPP_API_BASE=https://graph.facebook.com
WHATSAPP_API_VERSION=v21.0
WHATSAPP_ACCESS_TOKEN=seu_token_meta_aqui
WHATSAPP_PHONE_NUMBER_ID=seu_phone_id_aqui
WHATSAPP_DESTINATION_NUMBER=5511985879829
WHATSAPP_TIMEOUT_SECONDS=15
```

---

**Última atualização**: 2024
**Versão**: 1.0
