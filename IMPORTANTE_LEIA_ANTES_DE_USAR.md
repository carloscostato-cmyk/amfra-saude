# ⚠️ IMPORTANTE: Leia Antes de Usar em Produção

## 🚨 Problema Crítico: URLs com localhost

O sistema está configurado para **desenvolvimento local** e **NÃO funcionará corretamente** se você enviar links para colaboradores sem ajustar a configuração.

### Por que isso é um problema?

Quando você está no arquivo `.env` com:

```env
APP_BASE_URL=http://127.0.0.1:5000
```

Os links gerados serão assim:
- ❌ `http://127.0.0.1:5000/q/abc123`
- ❌ `http://127.0.0.1:5000/admin/submissions/...`

**Esses links só funcionam no seu computador!** 

Se você enviar para um colaborador, eles verão um erro porque `127.0.0.1` é o endereço local da máquina deles, não do seu servidor.

---

## ✅ Solução Rápida

### Passo 1: Descubra o endereço do seu servidor

Você precisa saber qual é o endereço público/acessível do servidor:

**Opção A - Servidor na Internet (com domínio):**
```
https://amfra.com.br
```

**Opção B - Servidor na rede local da empresa:**
```
http://192.168.1.100:5000
```

**Opção C - Servidor em nuvem (Railway, Heroku, AWS):**
```
https://amfra-saude-mental.railway.app
```

### Passo 2: Edite o arquivo `.env`

Abra o arquivo `.env` e altere esta linha:

```env
# Antes (ERRADO para produção)
APP_BASE_URL=http://127.0.0.1:5000

# Depois (CORRETO - use SEU endereço)
APP_BASE_URL=https://amfra.com.br
```

**IMPORTANTE**: Se usar HTTPS, também configure:
```env
PREFERRED_URL_SCHEME=https
SESSION_COOKIE_SECURE=true
```

### Passo 3: Reinicie o servidor

```bash
# Pare o servidor (Ctrl+C)
# Inicie novamente
python run.py
```

### Passo 4: Teste

1. Faça login no admin
2. Acesse uma empresa
3. Copie o "Link para questionário"
4. Verifique se o link começa com seu domínio/IP público
5. Teste abrindo o link em outro dispositivo

---

## 🛠️ Ferramenta Auxiliar

Criamos um script para ajudar você a configurar corretamente:

### Verificar configuração atual:
```bash
python configurar_producao.py
```

### Configuração interativa (assistente):
```bash
python configurar_producao.py --setup
```

O script vai:
- ✅ Verificar se `APP_BASE_URL` está correto
- ✅ Validar `SECRET_KEY`
- ✅ Checar configurações de segurança
- ✅ Gerar novo `.env` configurado corretamente

---

## 📖 Documentação Completa

Para mais detalhes, leia: **CONFIGURACAO_PRODUCAO.md**

---

## 🆘 Precisa de Ajuda?

### Problema: "Não sei qual é o endereço do meu servidor"

**Se o servidor está na sua rede local:**
1. Abra o PowerShell/CMD no servidor
2. Digite: `ipconfig` (Windows) ou `ifconfig` (Linux/Mac)
3. Procure por "Endereço IPv4" (exemplo: 192.168.1.100)
4. Use: `http://192.168.1.100:5000`

**Se o servidor está na internet:**
1. Você deve ter um domínio registrado (exemplo: amfra.com.br)
2. Use: `https://amfra.com.br`

**Se está usando Railway/Heroku:**
1. Acesse o dashboard da plataforma
2. Copie a URL fornecida (exemplo: `https://seu-app.railway.app`)
3. Use essa URL no `APP_BASE_URL`

### Problema: "Colaboradores não conseguem acessar o link"

Verifique:
1. ✅ `APP_BASE_URL` está com o endereço correto?
2. ✅ O servidor está rodando?
3. ✅ O firewall permite acesso à porta?
4. ✅ Se usar rede local, o colaborador está na mesma rede?
5. ✅ Se usar domínio, o DNS está configurado corretamente?

### Problema: "Erro 500 ao acessar o sistema"

Verifique:
1. ✅ Banco de dados foi inicializado? (`flask --app run.py init-db`)
2. ✅ Variáveis de ambiente estão corretas?
3. ✅ Logs em `instance/logs/app_narcista.log`

---

## 🎯 Checklist Rápido

Antes de usar em produção:

- [ ] `APP_BASE_URL` configurado com domínio/IP público
- [ ] Testei o link em outro dispositivo
- [ ] `SECRET_KEY` alterado (não usar o padrão)
- [ ] `ADMIN_PASSWORD` alterado (senha forte)
- [ ] Banco de dados inicializado
- [ ] Servidor acessível pela rede/internet
- [ ] Se usar HTTPS, certificado SSL configurado
- [ ] `SESSION_COOKIE_SECURE=true` se usar HTTPS
- [ ] Backup do banco de dados configurado

---

## 💡 Dica Final

**Sempre teste os links antes de enviar para colaboradores!**

1. Configure o `.env`
2. Reinicie o servidor
3. Copie o link do questionário
4. Abra em outro celular/computador
5. Se funcionar, está pronto! ✅

---

## 🔒 Segurança em Produção

### Checklist de Segurança

- [ ] `SECRET_KEY` forte e aleatório (mínimo 32 caracteres)
- [ ] `ADMIN_PASSWORD` forte (letras, números, símbolos)
- [ ] `SESSION_COOKIE_SECURE=true` (se HTTPS)
- [ ] `AUTO_SEED_ADMIN=false` (criar admin manualmente)
- [ ] PostgreSQL em produção (não SQLite)
- [ ] Backup automático do banco
- [ ] Logs monitorados
- [ ] Firewall configurado
- [ ] HTTPS habilitado (certificado SSL)

### Gerar SECRET_KEY Forte

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 📊 Monitoramento

### Logs da Aplicação

Os logs ficam em: `instance/logs/app_narcista.log`

Para monitorar em tempo real:
```bash
# Linux/Mac
tail -f instance/logs/app_narcista.log

# Windows PowerShell
Get-Content instance/logs/app_narcista.log -Wait -Tail 50
```

### Verificar Status do Servidor

```bash
# Verificar se está rodando
curl http://localhost:5000

# Verificar logs de erro
grep ERROR instance/logs/app_narcista.log
```

---

## 🚀 Deploy Rápido no Railway

1. **Criar conta**: https://railway.app
2. **Novo projeto** → "Deploy from GitHub repo"
3. **Adicionar PostgreSQL**: Add → Database → PostgreSQL
4. **Configurar variáveis**:
   ```env
   SECRET_KEY=<gerar-com-comando-acima>
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=<senha-forte>
   APP_BASE_URL=https://${{RAILWAY_PUBLIC_DOMAIN}}
   PREFERRED_URL_SCHEME=https
   SESSION_COOKIE_SECURE=true
   ```
5. **Deploy automático** a cada push no GitHub

---

## 📞 Suporte Técnico

Se precisar de ajuda:

1. **Verifique os logs**: `instance/logs/app_narcista.log`
2. **Verifique o `.env`**: Todas as variáveis estão corretas?
3. **Teste localmente**: Funciona em `http://127.0.0.1:5000`?
4. **Verifique conectividade**: O servidor está acessível?
5. **Consulte a documentação**: `CONFIGURACAO_PRODUCAO.md`

---

**Criado para**: AMFRA Saúde Mental LTDA  
**Versão**: 2.0  
**Última atualização**: 2024
