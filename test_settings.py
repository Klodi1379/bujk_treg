"""
Test settings configuration to debug database issue
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Minimal settings for testing
DEBUG = True
SECRET_KEY = 'test-key'

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test.sqlite3',
    }
}

USE_TZ = True
