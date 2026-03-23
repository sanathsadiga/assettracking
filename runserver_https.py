#!/usr/bin/env python
"""
Run Django development server with HTTPS support using mkcert certificates.
Usage: python runserver_https.py
"""
import os
import sys
import ssl
import django
from django.conf import settings
from django.core.wsgi import get_wsgi_application
import http.server
import socketserver

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asset_system.settings')
django.setup()

class SSLTCPServer(socketserver.TCPServer):
    """TCP Server with SSL support"""
    allow_reuse_address = True
    
    def __init__(self, server_address, RequestHandlerClass, certfile, keyfile):
        self.certfile = certfile
        self.keyfile = keyfile
        super().__init__(server_address, RequestHandlerClass)
        
        # Wrap socket with SSL
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile, keyfile)
        self.socket = context.wrap_socket(self.socket, server_side=True)

class WSGIRequestHandler(http.server.BaseHTTPRequestHandler):
    """WSGI request handler"""
    def __init__(self, *args, wsgi_app=None, **kwargs):
        self.wsgi_app = wsgi_app
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        self.send_wsgi_response()
    
    def do_POST(self):
        self.send_wsgi_response()
    
    def do_PUT(self):
        self.send_wsgi_response()
    
    def do_DELETE(self):
        self.send_wsgi_response()
    
    def do_PATCH(self):
        self.send_wsgi_response()
    
    def do_HEAD(self):
        self.send_wsgi_response()
    
    def do_OPTIONS(self):
        self.send_wsgi_response()
    
    def send_wsgi_response(self):
        """Send WSGI application response"""
        environ = {
            'REQUEST_METHOD': self.command,
            'SCRIPT_NAME': '',
            'PATH_INFO': self.path.split('?')[0],
            'QUERY_STRING': self.path.split('?')[1] if '?' in self.path else '',
            'CONTENT_TYPE': self.headers.get('content-type', ''),
            'CONTENT_LENGTH': self.headers.get('content-length', ''),
            'SERVER_NAME': self.server.server_name,
            'SERVER_PORT': str(self.server.server_port),
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'https',
            'wsgi.input': self.rfile,
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': True,
            'wsgi.multiprocess': False,
            'wsgi.run_once': False,
        }
        
        # Add headers to environ
        for key, value in self.headers.items():
            key = key.upper().replace('-', '_')
            if key not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
                key = f'HTTP_{key}'
            environ[key] = value
        
        # Get response from WSGI app
        status = None
        response_headers = []
        
        def start_response(status_str, headers):
            nonlocal status, response_headers
            status = int(status_str.split(' ', 1)[0])
            response_headers = headers
        
        try:
            app_iter = self.wsgi_app(environ, start_response)
            self.send_response(status)
            for header, value in response_headers:
                self.send_header(header, value)
            self.end_headers()
            
            for data in app_iter:
                self.wfile.write(data)
        except Exception as e:
            self.send_error(500, str(e))
    
    def log_message(self, format, *args):
        """Log HTTP requests"""
        print(f"[{self.log_date_time_string()}] {format % args}")

if __name__ == '__main__':
    cert_file = 'cert.pem'
    key_file = 'key.pem'
    host = '0.0.0.0'
    port = 8443
    
    if not os.path.exists(cert_file) or not os.path.exists(key_file):
        print(f"❌ SSL certificate files not found!")
        print(f"Create them with:")
        print(f"  mkcert -cert-file {cert_file} -key-file {key_file} localhost 127.0.0.1 10.175.8.100")
        sys.exit(1)
    
    app = get_wsgi_application()
    
    print(f"\n{'='*60}")
    print(f"🔒 Starting HTTPS server...")
    print(f"{'='*60}")
    print(f"📱 Access from phone: https://10.175.8.100:{port}")
    print(f"💻 Access locally: https://localhost:{port}")
    print(f"{'='*60}")
    print(f"Press Ctrl+C to stop\n")
    
    # Create a custom handler with the WSGI app
    def handler(*args, **kwargs):
        return WSGIRequestHandler(*args, wsgi_app=app, **kwargs)
    
    try:
        with SSLTCPServer((host, port), handler, cert_file, key_file) as httpd:
            print(f"✅ Server started successfully")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n✅ Server stopped")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


