"""
ASGI is the new, asynchronous-friendly standard that will allow your Django site to use asynchronous Python features,
and asynchronous Django features as they are developed.
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bingologyserver.settings')

application = get_asgi_application()
