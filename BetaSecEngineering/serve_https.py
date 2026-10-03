"""Local classroom TLS server; never use for production or non-loopback hosting."""
import os
from pathlib import Path
import ssl
from wsgiref.simple_server import WSGIRequestHandler, make_server

BASE_DIR = Path(__file__).resolve().parent


class HTTPSRequestHandler(WSGIRequestHandler):
    def get_environ(self):
        environ = super().get_environ()
        environ['HTTPS'] = 'on'
        environ['wsgi.url_scheme'] = 'https'
        return environ


def create_tls_context(certfile, keyfile):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.load_cert_chain(certfile, keyfile)
    return context


def main():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'betasecengineering.settings_https'
    import django
    from django.core.management import call_command
    from django.core.wsgi import get_wsgi_application
    from django.contrib.staticfiles.handlers import StaticFilesHandler

    django.setup()
    call_command('check')
    context = create_tls_context(
        BASE_DIR / 'local-certs/localhost.pem',
        BASE_DIR / 'local-certs/localhost-key.pem',
    )
    application = StaticFilesHandler(get_wsgi_application())
    # Hard-coded loopback binding: no option to expose this vulnerable lab.
    with make_server('127.0.0.1', 8443, application,
                     handler_class=HTTPSRequestHandler) as server:
        server.socket = context.wrap_socket(server.socket, server_side=True)
        print('Local lab only: https://127.0.0.1:8443/ (Ctrl+C to stop)', flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    main()
