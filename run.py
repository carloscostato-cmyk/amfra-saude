import os

from app import create_app, ensure_admin_user
from app.extensions import db


app = create_app()


with app.app_context():
    if app.config.get("AUTO_CREATE_DB"):
        db.create_all()
    ensure_admin_user(app)


if __name__ == "__main__":
    target_port = int(os.getenv("PORT", os.getenv("APP_PORT", "5001")))
    app.run(
        host="0.0.0.0",
        port=target_port,
        debug=False,
    )
