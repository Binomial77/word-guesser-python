from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'dev-secret-change-me')
DEBUG = os.getenv('DJANGO_DEBUG', 'true').lower() == 'true'
ALLOWED_HOSTS = [x.strip() for x in os.getenv('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',') if x.strip()]

INSTALLED_APPS = ['django.contrib.sessions', 'django.contrib.staticfiles', 'game']
# Signed-cookie sessions: no django_session table needed, so the bundled SQLite DB works as-is.
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
MIDDLEWARE = ['django.middleware.security.SecurityMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware', 'game.middleware.AuthMiddleware']
ROOT_URLCONF = 'word_guess_game.urls'
TEMPLATES = [{'BACKEND':'django.template.backends.django.DjangoTemplates','DIRS':[BASE_DIR/'templates'],'APP_DIRS':True,'OPTIONS':{'context_processors':[]}}]
WSGI_APPLICATION = 'word_guess_game.wsgi.application'
DATABASES = {'default': {'ENGINE':'django.db.backends.sqlite3','NAME':BASE_DIR/'word-guess-game.db','OPTIONS':{'timeout':20}}}
LANGUAGE_CODE='en-us'; TIME_ZONE='localtime'; USE_I18N=True; USE_TZ=False
STATIC_URL='/static/'; STATICFILES_DIRS=[BASE_DIR/'static']; STATIC_ROOT=BASE_DIR/'staticfiles'
DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
ADMIN_USERNAME=os.getenv('APP_ADMIN_USERNAME','AdminUser'); ADMIN_PASSWORD=os.getenv('APP_ADMIN_PASSWORD','Admin$123')
DAILY_LIMIT=3; MAX_GUESSES=5
