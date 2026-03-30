import logging
from logging.handlers import RotatingFileHandler

import click
from flask import Flask, render_template

from config import Config

from .extensions import csrf, db, login_manager
from .models import AdminUser


def create_app(config_class: type[Config] = Config) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "admin.login"
    login_manager.login_message = "Faça login para acessar o painel administrativo."
    login_manager.login_message_category = "warning"

    _configure_logging(app)
    _register_blueprints(app)
    _register_context_processors(app)
    _register_error_handlers(app)
    _register_cli_commands(app)

    @login_manager.user_loader
    def load_user(user_id: str):
        return db.session.get(AdminUser, int(user_id))

    return app


def ensure_admin_user(app: Flask) -> bool:
    username = app.config.get("ADMIN_USERNAME")
    password = app.config.get("ADMIN_PASSWORD")
    if not app.config.get("AUTO_SEED_ADMIN") or not username or not password:
        return False

    with app.app_context():
        existing_user = AdminUser.query.filter_by(username=username).first()
        if existing_user:
            return False

        admin = AdminUser(username=username)
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        app.logger.info("Usuário administrador semeado automaticamente.")
        return True


def _configure_logging(app: Flask) -> None:
    app.config["LOG_DIR"].mkdir(parents=True, exist_ok=True)
    log_file = app.config["LOG_DIR"] / "app_narcista.log"
    file_handler = RotatingFileHandler(log_file, maxBytes=1_048_576, backupCount=3, encoding="utf-8")
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    )

    app.logger.setLevel(app.config["LOG_LEVEL"])
    if not any(isinstance(handler, RotatingFileHandler) for handler in app.logger.handlers):
        app.logger.addHandler(file_handler)


def _register_blueprints(app: Flask) -> None:
    from .routes_admin import admin_bp
    from .routes_public import public_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp)


def _register_context_processors(app: Flask) -> None:
    @app.context_processor
    def inject_globals():
        return {"app_name": app.config["APP_NAME"]}


def _register_error_handlers(app: Flask) -> None:
    @app.errorhandler(404)
    def not_found(error):  # noqa: ARG001
        return render_template("errors/404.html", body_class="page-error"), 404

    @app.errorhandler(500)
    def internal_error(error):  # noqa: ARG001
        db.session.rollback()
        return render_template("errors/500.html", body_class="page-error"), 500


def _register_cli_commands(app: Flask) -> None:
    @app.cli.command("init-db")
    def init_db_command():
        db.create_all()
        click.echo("Banco inicializado com sucesso.")

    @app.cli.command("repair-db")
    def repair_db_command():
        """Força o recarregamento do esquema do banco (DROP and CREATE)."""
        if click.confirm("Isso apagará TODOS os dados. Tem certeza?", abort=True):
            db.drop_all()
            db.create_all()
            click.echo("Esquema do banco recriado com sucesso.")

    @app.cli.command("seed-admin")
    @click.option("--username", prompt=True, help="Nome de usuário do administrador.")
    @click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True, help="Senha do administrador.")
    def seed_admin_command(username: str, password: str):
        existing_user = AdminUser.query.filter_by(username=username).first()
        if existing_user:
            click.echo("Usuário já existe. Nenhuma alteração foi feita.")
            return

        admin = AdminUser(username=username.strip())
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        click.echo("Administrador criado com sucesso.")
