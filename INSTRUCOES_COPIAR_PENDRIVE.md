# 📦 INSTRUÇÕES PARA COPIAR DEIAPSIC PARA PENDRIVE

## O QUE COPIAR

Copie TODA a pasta `Narcista3` para o pendrive. Ela contém:

### ✅ Arquivos da Aplicação
- `app/` - Toda a aplicação Flask
- `app/templates/` - Todos os arquivos HTML
- `app/static/` - CSS, JavaScript, imagens
- `instance/` - Banco de dados SQLite

### ✅ Arquivos de Configuração
- `.env` - Configurações do ambiente
- `config.py` - Configurações da aplicação
- `requirements.txt` - Dependências Python

### ✅ Scripts Úteis
- `run.py` - Iniciar o servidor
- `criar_pacientes_teste.py` - Criar dados de teste
- `configurar_producao.py` - Configurar para produção

### ✅ Documentação
- `README.md` - Documentação completa
- `CONFIGURACAO_PRODUCAO.md` - Guia de produção
- `IMPORTANTE_LEIA_ANTES_DE_USAR.md` - Avisos importantes

## COMO COPIAR

1. **Insira o pendrive** no computador
2. **Copie a pasta completa** `Narcista3` para o pendrive
3. **Aguarde** a cópia terminar (pode demorar alguns minutos)

## COMO USAR EM OUTRO COMPUTADOR

### Passo 1: Copiar do Pendrive
```bash
# Copie a pasta Narcista3 do pendrive para o computador
```

### Passo 2: Instalar Python
- Baixe Python 3.11+ de https://www.python.org/downloads/
- Durante instalação, marque "Add Python to PATH"

### Passo 3: Instalar Dependências
```bash
cd Narcista3
pip install -r requirements.txt
```

### Passo 4: Iniciar Servidor
```bash
python run.py
```

### Passo 5: Acessar
- Abra navegador em: http://127.0.0.1:5001
- Login: Deia
- Senha: JesusSalva

## ARQUIVOS IMPORTANTES NO PENDRIVE

```
📁 Narcista3/
├── 📁 app/
│   ├── 📁 templates/          ← Todos os HTML
│   │   ├── admin_dashboard.html
│   │   ├── admin_submission_detail.html
│   │   ├── admin_submission_detail_NOVO.html
│   │   ├── public_form.html
│   │   └── ...
│   ├── 📁 static/             ← CSS, JS, Imagens
│   │   ├── 📁 css/
│   │   │   └── style.css
│   │   ├── 📁 js/
│   │   │   ├── main.js
│   │   │   └── submission_detail.js
│   │   └── 📁 img/
│   └── 📁 services/           ← Lógica de negócio
├── 📁 instance/
│   └── app_narcista.db        ← Banco de dados
├── .env                       ← Configurações
├── config.py
├── run.py                     ← Iniciar servidor
├── requirements.txt           ← Dependências
└── README.md                  ← Documentação

```

## TAMANHO APROXIMADO
- Aplicação completa: ~5-10 MB
- Com banco de dados: +1-5 MB (depende dos dados)
- **Total**: ~10-15 MB

## PENDRIVE RECOMENDADO
- Mínimo: 128 MB (qualquer pendrive serve)
- Recomendado: 1 GB ou mais

## BACKUP
✅ Sempre mantenha uma cópia de segurança em outro local!

## SUPORTE
Em caso de dúvidas, consulte o README.md completo.
