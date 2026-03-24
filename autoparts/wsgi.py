"""
WSGI config for autoparts project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""
from waitress import serve
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autoparts.settings')

application = get_wsgi_application()
if __name__ == "__main__":
    serve(application, host='0.0.0.0', port=80)  # Bind to all interfaces and port 8000
