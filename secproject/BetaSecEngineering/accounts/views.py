from urllib.parse import urlsplit

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import DatabaseError, connection
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import LabLoginForm, SignUpForm
from .models import LabAccount


LOCAL_LAB_HOSTS = {'127.0.0.1', 'localhost', 'testserver', '::1'}


def _require_local_lab(request):
    hostname = urlsplit(f'//{request.get_host()}').hostname
    if not settings.ENABLE_SECURITY_LABS or hostname not in LOCAL_LAB_HOSTS:
        raise Http404('The security lab is available only on localhost.')


def _lab_context(mode, form):
    is_vulnerable = mode == 'vulnerable'
    return {
        'form': form,
        'mode': mode,
        'is_vulnerable': is_vulnerable,
        'page_title': 'Vulnerable login' if is_vulnerable else 'Secure comparison',
        'comparison_url': reverse(
            'lab-secure-login' if is_vulnerable else 'lab-vulnerable-login'
        ),
        'comparison_label': (
            'Open secure comparison' if is_vulnerable else 'Open vulnerable lab'
        ),
        'mode_summary': (
            'Unsafe string-built SQL accepts the classroom bypass payload.'
            if is_vulnerable
            else 'Django ORM filtering treats the same payload as plain text.'
        ),
        'result_hint': (
            'Submit the dummy password, then try the bypass value in the username field.'
            if is_vulnerable
            else 'Submit the same bypass value here to show that the secure route rejects it.'
        ),
    }


def _start_lab_session(request, account, mode):
    request.session.cycle_key()
    request.session['lab_account'] = {
        'id': account['id'],
        'username': account['username'],
        'display_name': account['display_name'],
    }
    request.session['lab_mode'] = mode


def home(request):
    return redirect('account' if request.user.is_authenticated else 'login')


def transport_guide(request):
    return render(request, 'accounts/transport_guide.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect('account')

    form = SignUpForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Your local test account is ready.')
        return redirect('account')

    return render(request, 'registration/signup.html', {'form': form})


@login_required
def account(request):
    session_status = {
        'transport': 'HTTPS' if request.is_secure() else 'HTTP',
        'cookie_name': settings.SESSION_COOKIE_NAME,
        'http_only': settings.SESSION_COOKIE_HTTPONLY,
        'same_site': settings.SESSION_COOKIE_SAMESITE,
        'secure': settings.SESSION_COOKIE_SECURE,
    }
    return render(request, 'accounts/account.html', {'session_status': session_status})


def lab_vulnerable_login(request):
    _require_local_lab(request)
    form = LabLoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        table_name = connection.ops.quote_name(LabAccount._meta.db_table)

        # INTENTIONALLY VULNERABLE: local classroom demonstration only.
        unsafe_sql = (
            f"SELECT id, username, display_name FROM {table_name} "
            f"WHERE username = '{username}' "
            f"AND lab_password = '{password}' LIMIT 1"
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute(unsafe_sql)
                row = cursor.fetchone()
        except DatabaseError:
            form.add_error(None, 'The submitted values produced an invalid query.')
        else:
            if row:
                _start_lab_session(
                    request,
                    {'id': row[0], 'username': row[1], 'display_name': row[2]},
                    'vulnerable',
                )
                return redirect('lab-result')
            form.add_error(None, 'Invalid lab username or password.')

    return render(
        request,
        'accounts/lab_login.html',
        _lab_context('vulnerable', form),
    )


def lab_secure_login(request):
    _require_local_lab(request)
    form = LabLoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        account = LabAccount.objects.filter(
            username=form.cleaned_data['username'],
            lab_password=form.cleaned_data['password'],
        ).values('id', 'username', 'display_name').first()

        if account:
            _start_lab_session(request, account, 'secure')
            return redirect('lab-result')
        form.add_error(None, 'Invalid lab username or password.')

    return render(
        request,
        'accounts/lab_login.html',
        _lab_context('secure', form),
    )


def lab_result(request):
    _require_local_lab(request)
    account_data = request.session.get('lab_account')
    if not account_data:
        return redirect('lab-vulnerable-login')

    return render(
        request,
        'accounts/lab_result.html',
        {
            'lab_account': account_data,
            'lab_mode': request.session.get('lab_mode', 'unknown'),
        },
    )


@require_POST
def lab_logout(request):
    _require_local_lab(request)
    request.session.pop('lab_account', None)
    request.session.pop('lab_mode', None)
    return redirect('lab-vulnerable-login')
