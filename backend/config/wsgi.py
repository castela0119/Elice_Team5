"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
from pathlib import Path

import dotenv
from django.core.wsgi import get_wsgi_application

BASE_DIR = Path(__file__).resolve().parent.parent.parent
env_path = os.path.join(BASE_DIR, ".env")

if os.path.exists(env_path):
    dotenv.read_dotenv(env_path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.config.settings.prod")

application = get_wsgi_application()
