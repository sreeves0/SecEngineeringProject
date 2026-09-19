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
