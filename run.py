import os

from app import create_app, ensure_admin_user
from app.extensions import db


app = create_app()


with app.app_context():
    if app.config.get("AUTO_CREATE_DB"):
        db.create_all()
    ensure_admin_user(app)


if __name__ == "__main__":
    # Railway fornece a porta na variável de ambiente PORT. 
    # Usamos ela para garantir que o roteador encontre o app.
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
