# 🚀 DEPLOY GRATUITO NO RAILWAY.COM - PASSO A PASSO

## ✅ O QUE É O RAILWAY?

Railway é uma plataforma de hospedagem que permite fazer deploy de aplicações Flask **GRATUITAMENTE** com apenas alguns cliques.

**Vantagens**:
- ✅ $5 créditos grátis por mês
- ✅ Deploy automático via GitHub
- ✅ PostgreSQL/MySQL incluído
- ✅ SSL/HTTPS automático
- ✅ URL pública imediata

---

## 📋 PRÉ-REQUISITOS

1. Conta no GitHub (gratuita)
2. Conta no Railway.com (gratuita)
3. Código do AMFRA

---

## 🎯 PASSO A PASSO COMPLETO

### PASSO 1: Criar Conta no Railway

1. Acesse: https://railway.com
2. Clique em "Start a New Project"
3. Faça login com GitHub
4. Autorize o Railway a acessar seus repositórios

### PASSO 2: Preparar o Projeto

Certifique-se que seu projeto tem estes arquivos:

#### `requirements.txt` (já existe)
```
Flask==3.0.2
Flask-Login==0.6.3
Flask-SQLAlchemy==3.1.1
python-dotenv==1.0.1
requests==2.31.0
```

#### `Procfile` (CRIAR ESTE ARQUIVO)
```
web: gunicorn run:app
```

#### Adicionar `gunicorn` ao `requirements.txt`:
```bash
echo "gunicorn==21.2.0" >> requirements.txt
```

#### `runtime.txt` (CRIAR ESTE ARQUIVO)
```
python-3.11.8
```

### PASSO 3: Subir para o GitHub

```bash
# Inicializar repositório Git (se ainda não fez)
git init

# Adicionar todos os arquivos
git add .

# Fazer commit
git commit -m "Deploy AMFRA para Railway"

# Criar repositório no GitHub
# Vá em github.com e crie um novo repositório chamado "AMFRA"

# Conectar ao repositório remoto
git remote add origin https://github.com/SEU_USUARIO/AMFRA.git

# Enviar código
git push -u origin main
```

### PASSO 4: Deploy no Railway

1. No Railway, clique em "New Project"
2. Selecione "Deploy from GitHub repo"
3. Escolha o repositório "AMFRA"
4. Railway detecta automaticamente que é Flask
5. Clique em "Deploy"

### PASSO 5: Configurar Variáveis de Ambiente

No Railway, vá em "Variables" e adicione:

```
FLASK_ENV=production
SECRET_KEY=sua-chave-secreta-aqui-mude-isso
DATABASE_URL=sqlite:///instance/app_narcista.db
ADMIN_USERNAME=Deia
ADMIN_PASSWORD=JesusSalva
WHATSAPP_ENABLED=false
```

**IMPORTANTE**: Mude o `SECRET_KEY` para algo único!

### PASSO 6: Obter URL Pública

1. No Railway, vá em "Settings"
2. Clique em "Generate Domain"
3. Sua URL será algo como: `AMFRA-production.up.railway.app`

---

## 🎉 PRONTO!

Seu sistema está no ar! Acesse:
- **URL Pública**: https://seu-app.up.railway.app
- **Admin**: https://seu-app.up.railway.app/admin/login
- **Formulário**: https://seu-app.up.railway.app/questionario-pessoal

---

## 🔧 COMANDOS ÚTEIS

### Atualizar o App (após mudanças)
```bash
git add .
git commit -m "Atualização"
git push
```
Railway faz deploy automático!

### Ver Logs
No Railway, clique em "Deployments" → "View Logs"

### Reiniciar App
No Railway, clique em "Settings" → "Restart"

---

## 💰 LIMITES DO PLANO GRATUITO

- **Créditos**: $5/mês (suficiente para ~500 horas)
- **Tráfego**: Ilimitado
- **Banco**: 1GB PostgreSQL grátis
- **Dormência**: Não dorme (diferente do Render)

**Dica**: Se os créditos acabarem, o app para. Upgrade para $5/mês remove limites.

---

## 🆘 PROBLEMAS COMUNS

### Erro: "Application failed to respond"
**Solução**: Verifique se o `Procfile` está correto e `gunicorn` está no `requirements.txt`

### Erro: "No module named 'app'"
**Solução**: Certifique-se que o arquivo `run.py` existe e está correto

### Erro: "Database locked"
**Solução**: Use PostgreSQL em produção:
```bash
# No Railway, adicione PostgreSQL
# Atualize DATABASE_URL para usar PostgreSQL
```

---

## 🔐 SEGURANÇA EM PRODUÇÃO

1. **Mude o SECRET_KEY** para algo único
2. **Mude a senha do admin** (não use "JesusSalva" em produção)
3. **Use HTTPS** (Railway fornece automaticamente)
4. **Ative PostgreSQL** para banco mais robusto

---

## 📚 RECURSOS ADICIONAIS

- Documentação Railway: https://docs.railway.com
- Suporte Railway: https://railway.com/help
- Comunidade: https://discord.gg/railway

---

## ✅ CHECKLIST FINAL

- [ ] Conta Railway criada
- [ ] Repositório GitHub criado
- [ ] `Procfile` criado
- [ ] `gunicorn` adicionado ao requirements.txt
- [ ] Código enviado para GitHub
- [ ] Deploy feito no Railway
- [ ] Variáveis de ambiente configuradas
- [ ] URL pública gerada
- [ ] App testado e funcionando

---

**🎉 Parabéns! Seu AMFRA está online e acessível para qualquer pessoa na internet!**
