"""
WSGI config for bingologyserver project.
DJANGO is not a webserver

WSGI is the main Python standard for communicating between Web servers and applications, but it only supports synchronous code.
this is most commonly used

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bingologyserver.settings')

application = get_wsgi_application()
