from urllib.parse import urljoin, urlparse

from flask import current_app, has_request_context, url_for


def build_public_questionnaire_url(company) -> str:
    if has_request_context():
        return url_for("public.questionnaire", company_token=company.token, _external=True)

    # Fallback only if called from CLI/Background without web context
    configured_base_url = current_app.config.get("APP_BASE_URL", "http://127.0.0.1:5001")
    path = f"/q/{company.token}"
    return urljoin(f"{configured_base_url}/", path.lstrip("/"))
