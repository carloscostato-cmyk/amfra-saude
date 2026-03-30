# ⚠️ IMPORTANTE: Leia Antes de Usar em Produção

## 🚨 Problema Crítico: URLs com localhost

O sistema está configurado para **desenvolvimento local** e **NÃO funcionará corretamente** se você enviar links para pacientes ou pelo WhatsApp.

### Por que isso é um problema?

Quando você está no arquivo `.env` com:

```env
APP_BASE_URL=http://127.0.0.1:5000
```

Os links gerados serão assim:
- ❌ `http://127.0.0.1:5000/questionario-pessoal`
- ❌ `http://127.0.0.1:5000/admin/submissions/...`

**Esses links só funcionam no seu computador!** 

Se você enviar para um paciente ou pelo WhatsApp, eles verão um erro porque `127.0.0.1` é o endereço local da máquina deles, não do seu servidor.

---

## ✅ Solução Rápida

### Passo 1: Descubra o endereço do seu servidor

Você precisa saber qual é o endereço público/acessível do servidor:

**Opção A - Servidor na Internet (com domínio):**
```
https://deiapsic.com.br
```

**Opção B - Servidor na rede local da clínica:**
```
http://192.168.1.100:5001
```

**Opção C - Servidor em nuvem (AWS, Azure, etc):**
```
https://ec2-xxx-xxx-xxx-xxx.compute.amazonaws.com
```

### Passo 2: Edite o arquivo `.env`

Abra o arquivo `.env` e altere esta linha:

```env
# Antes (ERRADO para produção)
APP_BASE_URL=http://127.0.0.1:5000

# Depois (CORRETO - use SEU endereço)
APP_BASE_URL=https://deiapsic.com.br
```

### Passo 3: Reinicie o servidor

```bash
# Pare o servidor (Ctrl+C)
# Inicie novamente
python run.py
```

### Passo 4: Teste

1. Faça login no admin
2. Copie o "Link para paciente"
3. Verifique se o link começa com seu domínio/IP público
4. Teste abrindo o link em outro dispositivo

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
2. Digite: `ipconfig`
3. Procure por "Endereço IPv4" (exemplo: 192.168.1.100)
4. Use: `http://192.168.1.100:5001`

**Se o servidor está na internet:**
1. Você deve ter um domínio registrado (exemplo: deiapsic.com.br)
2. Use: `https://deiapsic.com.br`

### Problema: "Pacientes não conseguem acessar o link"

Verifique:
1. ✅ `APP_BASE_URL` está com o endereço correto?
2. ✅ O servidor está rodando?
3. ✅ O firewall permite acesso à porta?
4. ✅ Se usar rede local, o paciente está na mesma rede?

---

## 🎯 Checklist Rápido

Antes de usar em produção:

- [ ] `APP_BASE_URL` configurado com domínio/IP público
- [ ] Testei o link em outro dispositivo
- [ ] `SECRET_KEY` alterado (não usar o padrão)
- [ ] `ADMIN_PASSWORD` alterado (senha forte)
- [ ] Servidor acessível pela rede/internet
- [ ] Se usar HTTPS, certificado SSL configurado

---

## 💡 Dica Final

**Sempre teste os links antes de enviar para pacientes!**

1. Configure o `.env`
2. Reinicie o servidor
3. Copie o link do questionário
4. Abra em outro celular/computador
5. Se funcionar, está pronto! ✅

---

**Criado para**: Deiapsic - Sistema de Avaliação Clínica  
**Versão**: 1.0  
**Data**: 2024
