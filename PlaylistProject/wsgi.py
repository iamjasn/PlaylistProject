"""
WSGI config for PlaylistProject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os, sys
sys.path.append('/Applications/djangostack/apps/django/django_projects/PlaylistProject')
os.environ.setdefault("PYTHON_EGG_CACHE", "/Applications/djangostack/apps/django/django_projects/PlaylistProject/egg_cache")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PlaylistProject.settings")

from django.core.wsgi import get_wsgi_application
from dj_static import Cling

application = Cling(get_wsgi_application())