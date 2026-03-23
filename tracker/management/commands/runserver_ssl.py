import ssl
import os
from django.core.management.commands.runserver import Command as RunServerCommand

class Command(RunServerCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            '--cert-file',
            dest='cert_file',
            default='cert.pem',
            help='Path to SSL certificate file'
        )
        parser.add_argument(
            '--key-file',
            dest='key_file',
            default='key.pem',
            help='Path to SSL key file'
        )

    def handle(self, *args, **options):
        cert_file = options.get('cert_file')
        key_file = options.get('key_file')
        
        if not os.path.exists(cert_file) or not os.path.exists(key_file):
            self.stdout.write(
                self.style.ERROR(
                    f'SSL certificate files not found. Please create them with:\n'
                    f'openssl req -x509 -newkey rsa:4096 -nodes -out {cert_file} -keyout {key_file} -days 365'
                )
            )
            return
        
        # Patch the server to use SSL
        from django.core.servers.wsgiref import WSGIServer, WSGIRequestHandler
        
        class SSLWSGIServer(WSGIServer):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.socket = ssl.wrap_socket(
                    self.socket,
                    certfile=cert_file,
                    keyfile=key_file,
                    server_side=True,
                    ssl_version=ssl.PROTOCOL_TLS
                )
        
        # Replace the server class
        import django.core.servers.wsgiref as wsgiref_module
        original_server = wsgiref_module.WSGIServer
        wsgiref_module.WSGIServer = SSLWSGIServer
        
        try:
            self.stdout.write(self.style.SUCCESS('Starting HTTPS server...'))
            super().handle(*args, **options)
        finally:
            wsgiref_module.WSGIServer = original_server
