import os
from decouple import config
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='your-secret-key-here')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'books',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'books_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'books_project.wsgi.application'

# IPv4 Fix for Render + Supabase
if os.environ.get('RENDER') or 'render.com' in os.environ.get('RENDER_EXTERNAL_URL', ''):
    import socket
    
    def getaddrinfo_wrapper(host, port, family=0, type=0, proto=0, flags=0):
        return socket._original_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
    
    if not hasattr(socket, '_original_getaddrinfo'):
        socket._original_getaddrinfo = socket.getaddrinfo
        socket.getaddrinfo = getaddrinfo_wrapper

# Database Configuration Function
def get_database_config():
    # Check if running on Render (production)
    if os.environ.get('RENDER') or 'render.com' in os.environ.get('RENDER_EXTERNAL_URL', ''):
        return {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': os.environ.get('DB_NAME', 'postgres'),
                'USER': os.environ.get('DB_USER', 'postgres'),
                'PASSWORD': os.environ.get('DB_PASSWORD'),
                'HOST': os.environ.get('DB_HOST'),
                'PORT': os.environ.get('DB_PORT', '5432'),  # Use pooler port
                'OPTIONS': {
                    'sslmode': 'require',
                    'connect_timeout': 30,
                },
                'CONN_MAX_AGE': 60,
                'CONN_HEALTH_CHECKS': True,
            }
        }
    else:
        # Local development - check if environment variables are set for PostgreSQL
        if all([os.environ.get('DB_NAME'), os.environ.get('DB_USER'), 
                os.environ.get('DB_PASSWORD'), os.environ.get('DB_HOST')]):
            return {
                'default': {
                    'ENGINE': 'django.db.backends.postgresql',
                    'NAME': os.environ.get('DB_NAME'),
                    'USER': os.environ.get('DB_USER'),
                    'PASSWORD': os.environ.get('DB_PASSWORD'),
                    'HOST': os.environ.get('DB_HOST'),
                    'PORT': os.environ.get('DB_PORT', '6543'),
                    'OPTIONS': {
                        'sslmode': 'require',
                    },
                }
            }
        else:
            # Fallback to SQLite for local development
            return {
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': BASE_DIR / 'db.sqlite3',
                }
            }

# Apply the database configuration
DATABASES = get_database_config()

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 40,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}

# CORS Configuration
CORS_ALLOWED_ORIGINS = [
    "https://book-manager-frontend-five.vercel.app"
]

CORS_ALLOW_ALL_ORIGINS = False  # Only for development

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'