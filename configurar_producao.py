#!/usr/bin/env python3
"""
Script auxiliar para configurar o Deiapsic para produção.
Ajuda a validar e configurar corretamente o arquivo .env
"""

import os
import secrets
import sys
from pathlib import Path


def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def print_success(text):
    print(f"✅ {text}")


def print_warning(text):
    print(f"⚠️  {text}")


def print_error(text):
    print(f"❌ {text}")


def print_info(text):
    print(f"ℹ️  {text}")


def check_env_file():
    """Verifica se o arquivo .env existe"""
    env_path = Path(".env")
    if not env_path.exists():
        print_error("Arquivo .env não encontrado!")
        print_info("Copie o arquivo .env.example para .env primeiro:")
        print_info("  Copy-Item .env.example .env")
        return False
    return True


def load_env_vars():
    """Carrega variáveis do .env"""
    env_vars = {}
    with open(".env", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                env_vars[key.strip()] = value.strip()
    return env_vars


def check_app_base_url(env_vars):
    """Verifica se APP_BASE_URL está configurado corretamente"""
    print_header("Verificando APP_BASE_URL")
    
    app_base_url = env_vars.get("APP_BASE_URL", "")
    
    if not app_base_url:
        print_error("APP_BASE_URL não está configurado!")
        return False
    
    if "127.0.0.1" in app_base_url or "localhost" in app_base_url:
        print_warning("APP_BASE_URL está usando localhost/127.0.0.1")
        print_warning("Isso NÃO funcionará em produção!")
        print_info("Configure com o domínio ou IP público do servidor")
        print_info("Exemplo: https://deiapsic.com.br")
        print_info("Exemplo: http://192.168.1.100:5001")
        return False
    
    print_success(f"APP_BASE_URL configurado: {app_base_url}")
    return True


def check_secret_key(env_vars):
    """Verifica se SECRET_KEY é forte"""
    print_header("Verificando SECRET_KEY")
    
    secret_key = env_vars.get("SECRET_KEY", "")
    
    if not secret_key:
        print_error("SECRET_KEY não está configurado!")
        return False
    
    if "dev-secret" in secret_key or "change" in secret_key.lower():
        print_warning("SECRET_KEY parece ser a chave de desenvolvimento!")
        print_warning("Use uma chave forte em produção")
        print_info("Gere uma nova chave com:")
        print_info('  python -c "import secrets; print(secrets.token_urlsafe(32))"')
        return False
    
    if len(secret_key) < 32:
        print_warning("SECRET_KEY é muito curta (mínimo 32 caracteres)")
        return False
    
    print_success("SECRET_KEY parece estar configurada corretamente")
    return True


def check_database(env_vars):
    """Verifica configuração do banco de dados"""
    print_header("Verificando Banco de Dados")
    
    database_url = env_vars.get("DATABASE_URL", "")
    
    if not database_url:
        print_warning("DATABASE_URL vazio - usando SQLite (apenas para desenvolvimento)")
        print_info("Para produção, use PostgreSQL:")
        print_info("  DATABASE_URL=postgresql+psycopg://user:pass@host:5432/dbname")
        return False
    
    if database_url.startswith("postgresql"):
        print_success(f"PostgreSQL configurado: {database_url[:50]}...")
        return True
    
    if database_url.startswith("sqlite"):
        print_warning("SQLite configurado - recomendado apenas para desenvolvimento")
        return False
    
    print_error("DATABASE_URL com formato desconhecido")
    return False


def check_admin_credentials(env_vars):
    """Verifica credenciais do admin"""
    print_header("Verificando Credenciais Admin")
    
    admin_username = env_vars.get("ADMIN_USERNAME", "")
    admin_password = env_vars.get("ADMIN_PASSWORD", "")
    
    if not admin_username or not admin_password:
        print_error("ADMIN_USERNAME ou ADMIN_PASSWORD não configurados!")
        return False
    
    if admin_username in ["admin", "doutor", "Deia"] and admin_password in ["admin", "123456", "JesusSalva"]:
        print_warning("Credenciais admin parecem ser padrão/fracas!")
        print_warning("Altere para credenciais fortes em produção")
        return False
    
    if len(admin_password) < 8:
        print_warning("ADMIN_PASSWORD muito curta (mínimo 8 caracteres)")
        return False
    
    print_success("Credenciais admin configuradas")
    return True


def check_https_config(env_vars):
    """Verifica configuração HTTPS"""
    print_header("Verificando Configuração HTTPS")
    
    app_base_url = env_vars.get("APP_BASE_URL", "")
    session_cookie_secure = env_vars.get("SESSION_COOKIE_SECURE", "false").lower()
    preferred_url_scheme = env_vars.get("PREFERRED_URL_SCHEME", "http")
    
    uses_https = app_base_url.startswith("https://")
    
    if uses_https:
        if session_cookie_secure != "true":
            print_warning("APP_BASE_URL usa HTTPS mas SESSION_COOKIE_SECURE=false")
            print_info("Configure SESSION_COOKIE_SECURE=true para segurança")
            return False
        
        if preferred_url_scheme != "https":
            print_warning("APP_BASE_URL usa HTTPS mas PREFERRED_URL_SCHEME não é https")
            print_info("Configure PREFERRED_URL_SCHEME=https")
            return False
        
        print_success("Configuração HTTPS correta")
        return True
    else:
        print_info("APP_BASE_URL usa HTTP (sem SSL)")
        print_info("Considere usar HTTPS em produção para maior segurança")
        return True


def check_whatsapp_config(env_vars):
    """Verifica configuração do WhatsApp"""
    print_header("Verificando Configuração WhatsApp")
    
    whatsapp_enabled = env_vars.get("WHATSAPP_ENABLED", "false").lower()
    
    if whatsapp_enabled != "true":
        print_info("WhatsApp desabilitado (WHATSAPP_ENABLED=false)")
        return True
    
    required_vars = [
        "WHATSAPP_ACCESS_TOKEN",
        "WHATSAPP_PHONE_NUMBER_ID",
        "WHATSAPP_DESTINATION_NUMBER"
    ]
    
    missing = []
    for var in required_vars:
        if not env_vars.get(var):
            missing.append(var)
    
    if missing:
        print_error(f"WhatsApp habilitado mas faltam variáveis: {', '.join(missing)}")
        return False
    
    print_success("Configuração WhatsApp completa")
    return True


def generate_new_secret_key():
    """Gera uma nova SECRET_KEY"""
    return secrets.token_urlsafe(32)


def interactive_setup():
    """Modo interativo para configurar produção"""
    print_header("Configuração Interativa para Produção")
    
    print("Este assistente vai ajudar a configurar o .env para produção.\n")
    
    # APP_BASE_URL
    print("1. Qual é o endereço público do servidor?")
    print("   Exemplos:")
    print("   - https://deiapsic.com.br")
    print("   - http://192.168.1.100:5001")
    app_base_url = input("\nAPP_BASE_URL: ").strip()
    
    # SECRET_KEY
    print("\n2. Deseja gerar uma nova SECRET_KEY aleatória? (s/n)")
    if input().lower() == "s":
        secret_key = generate_new_secret_key()
        print(f"   Nova SECRET_KEY gerada: {secret_key}")
    else:
        secret_key = input("   Digite a SECRET_KEY: ").strip()
    
    # Admin
    print("\n3. Credenciais do administrador:")
    admin_username = input("   ADMIN_USERNAME: ").strip()
    admin_password = input("   ADMIN_PASSWORD: ").strip()
    
    # HTTPS
    uses_https = app_base_url.startswith("https://")
    session_cookie_secure = "true" if uses_https else "false"
    preferred_url_scheme = "https" if uses_https else "http"
    
    # Database
    print("\n4. Configuração do banco de dados:")
    print("   Deixe vazio para usar SQLite (desenvolvimento)")
    print("   Ou digite a URL do PostgreSQL:")
    database_url = input("   DATABASE_URL: ").strip()
    
    # WhatsApp
    print("\n5. Deseja habilitar notificações WhatsApp? (s/n)")
    whatsapp_enabled = "true" if input().lower() == "s" else "false"
    
    whatsapp_token = ""
    whatsapp_phone_id = ""
    whatsapp_dest = ""
    
    if whatsapp_enabled == "true":
        whatsapp_token = input("   WHATSAPP_ACCESS_TOKEN: ").strip()
        whatsapp_phone_id = input("   WHATSAPP_PHONE_NUMBER_ID: ").strip()
        whatsapp_dest = input("   WHATSAPP_DESTINATION_NUMBER: ").strip()
    
    # Gerar novo .env
    print("\n" + "=" * 60)
    print("Gerando novo arquivo .env...")
    
    env_content = f"""# Configuração de Produção - Deiapsic
# Gerado automaticamente em {Path.cwd()}

# Segurança
SECRET_KEY={secret_key}

# URLs e Servidor
APP_BASE_URL={app_base_url}
APP_PORT=5001
PREFERRED_URL_SCHEME={preferred_url_scheme}

# Banco de Dados
DATABASE_URL={database_url}

# Segurança de Sessão
SESSION_COOKIE_SECURE={session_cookie_secure}

# Banco e Admin
AUTO_CREATE_DB=true
AUTO_SEED_ADMIN=true
ADMIN_USERNAME={admin_username}
ADMIN_PASSWORD={admin_password}

# Logs
LOG_LEVEL=INFO

# WhatsApp
NOTIFICATION_RECIPIENT_NAME=Dra. Andrea Franco
WHATSAPP_ENABLED={whatsapp_enabled}
WHATSAPP_API_BASE=https://graph.facebook.com
WHATSAPP_API_VERSION=v21.0
WHATSAPP_ACCESS_TOKEN={whatsapp_token}
WHATSAPP_PHONE_NUMBER_ID={whatsapp_phone_id}
WHATSAPP_DESTINATION_NUMBER={whatsapp_dest}
WHATSAPP_TIMEOUT_SECONDS=15
"""
    
    # Backup do .env atual
    if Path(".env").exists():
        backup_path = Path(".env.backup")
        Path(".env").rename(backup_path)
        print(f"✅ Backup do .env anterior salvo em: {backup_path}")
    
    # Salvar novo .env
    with open(".env", "w", encoding="utf-8") as f:
        f.write(env_content)
    
    print_success("Novo arquivo .env criado com sucesso!")
    print_info("Reinicie o servidor para aplicar as mudanças:")
    print_info("  python run.py")


def main():
    """Função principal"""
    print_header("Deiapsic - Verificador de Configuração de Produção")
    
    if len(sys.argv) > 1 and sys.argv[1] == "--setup":
        interactive_setup()
        return
    
    if not check_env_file():
        return
    
    env_vars = load_env_vars()
    
    checks = [
        check_app_base_url(env_vars),
        check_secret_key(env_vars),
        check_database(env_vars),
        check_admin_credentials(env_vars),
        check_https_config(env_vars),
        check_whatsapp_config(env_vars)
    ]
    
    print_header("Resumo da Verificação")
    
    passed = sum(checks)
    total = len(checks)
    
    if passed == total:
        print_success(f"Todas as verificações passaram! ({passed}/{total})")
        print_success("Sistema pronto para produção! 🚀")
    else:
        print_warning(f"Algumas verificações falharam ({passed}/{total})")
        print_info("Revise as configurações acima e corrija os problemas")
        print_info("\nPara configuração interativa, execute:")
        print_info("  python configurar_producao.py --setup")


if __name__ == "__main__":
    main()
