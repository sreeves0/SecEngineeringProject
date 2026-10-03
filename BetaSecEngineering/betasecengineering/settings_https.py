"""HTTPS comparison settings for the loopback-only classroom launcher."""
from .settings import *  # noqa: F403

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# Cookies are shared across ports. Separate names avoid disturbing the HTTP run.
SESSION_COOKIE_NAME = 'betasec_https_sessionid'
CSRF_COOKIE_NAME = 'betasec_https_csrftoken'
# TLS terminates directly in serve_https.py; do not trust proxy headers.
SECURE_PROXY_SSL_HEADER = None
