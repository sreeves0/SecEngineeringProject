# BetaSecEngineering

BetaSecEngineering is a localhost-only Django authentication lab for comparing
HTTP and HTTPS, an intentionally vulnerable SQL login with its secure
equivalent, and browser session-cookie protections.

## Local setup

The project does not require Django REST Framework or a virtual environment.
From this directory, use the Python installation available on the local PATH:

```powershell
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 127.0.0.1:8000
```

If Windows uses the Python launcher, replace `python` with `py`.

Open `http://127.0.0.1:8000/`. The admin panel is available at
`http://127.0.0.1:8000/admin/` after creating a superuser.

## Routes

- `/login/` - standard Django login.
- `/signup/` - local test-account registration.
- `/account/` - authenticated account and session status.
- `/lab/sql-injection/vulnerable/` - deliberately unsafe dummy login.
- `/lab/sql-injection/secure/` - ORM-based comparison.

The SQL lab contains only seeded dummy accounts. Its deliberately unsafe query
must never be copied into a real application or exposed beyond localhost.

Set `ENABLE_SECURITY_LABS=0` to disable both SQL-lab routes. When serving the
application over HTTPS, set `DJANGO_SECURE_COOKIES=1` so the session and CSRF
cookies receive the `Secure` flag.

## Local HTTPS comparison

From this directory, generate a disposable certificate with PowerShell 7:

```powershell
pwsh -File .\create-local-cert.ps1
python serve_https.py
```

Use your existing Django Python executable in place of `python` if needed.
The launcher runs Django checks, serves CSS, and binds only to
`https://127.0.0.1:8443/`. Stop it with Ctrl+C. It does not automatically reload
code; restart it after changes. No extra Python dependencies are required.

The self-signed certificate expires after 30 days and is valid only for
localhost/127.0.0.1. Your browser will show a certificate warning: for this
dummy-data lab only, use its advanced option to proceed at that exact local
address. This encrypts traffic but does not demonstrate a publicly trusted
server identity. Nothing is installed in the Windows certificate trust store.
Some browser policies may prevent proceeding with a self-signed certificate.
Keep the generated private key local; never reuse it elsewhere. `local-certs/`
is ignored by Git. To renew, manually remove that generated directory and rerun
the certificate script.

HTTPS uses `settings_https.py`, enabling Secure session and CSRF cookies with
separate cookie names. CSRF, HttpOnly, and SameSite protections stay enabled.
TLS terminates directly in the launcher; proxy headers are not trusted.
The footer shows the actual transport on every page.

For the HTTP comparison, use a separate terminal:

```powershell
$env:DJANGO_SECURE_COOKIES = '0'
python manage.py runserver 127.0.0.1:8000
```

Use separate private browser sessions for the two runs to keep dummy sessions
easy to compare. HTTP intentionally remains available for the demonstration;
this is a local development setup, not a production deployment.
