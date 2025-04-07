"""
WSGI config for djCMS project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djCMS.settings')

application = get_wsgi_application()