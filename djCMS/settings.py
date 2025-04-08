"""
Django settings for djCMS project.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-change-this-in-production'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',  # For SEO sitemaps
    
    # Third-party apps
    'taggit',
    'crispy_forms',
    'crispy_tailwind',
    'ckeditor',
    'imagekit',
    
    # Custom apps
    'core',
    'pages',
    'categories',
    'media_library',
    'navigation',
    'theming',
    'comments',
    'search',
    'blog',
    'newsletter',
    'widgets',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djCMS.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'navigation.context_processors.menus',  # Custom context processor for menus
                'theming.context_processors.theme',  # Custom context processor for theme
            ],
        },
    },
]

WSGI_APPLICATION = 'djCMS.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model
AUTH_USER_MODEL = 'core.User'

# SEO settings
SITE_ID = 1

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # For development
DEFAULT_FROM_EMAIL = 'noreply@example.com'
ADMINS = [('Admin', 'admin@example.com')]

# Tailwind CSS settings
TAILWIND_APP_NAME = 'theme'

# Crispy Forms settings
CRISPY_ALLOWED_TEMPLATE_PACKS = 'tailwind'
CRISPY_TEMPLATE_PACK = 'tailwind'

# CKEditor settings
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Full',
        'toolbar_Full': [
            ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
             'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Table', 'HorizontalRule', 'SpecialChar', 'PageBreak'],
            ['Styles', 'Format', 'Font', 'FontSize'],
            ['TextColor', 'BGColor'],
            ['Maximize', 'ShowBlocks', 'Source'],
        ],
        'height': 400,
        'width': '100%',
        'extraPlugins': ','.join([
            'uploadimage',  # the upload image feature
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
        'contentsCss': [
            '/static/css/tailwind.css',
            'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;500;600;700&display=swap',
        ],
        'bodyClass': 'prose max-w-none',
        'allowedContent': True,
        'removePlugins': 'stylesheetparser',
        'removeButtons': '',
        'stylesSet': [
            {'name': 'Heading 1', 'element': 'h1', 'attributes': {'class': 'text-4xl font-bold mb-4'}},
            {'name': 'Heading 2', 'element': 'h2', 'attributes': {'class': 'text-3xl font-bold mb-3'}},
            {'name': 'Heading 3', 'element': 'h3', 'attributes': {'class': 'text-2xl font-bold mb-2'}},
            {'name': 'Paragraph', 'element': 'p', 'attributes': {'class': 'mb-4'}},
            {'name': 'Blockquote', 'element': 'blockquote', 'attributes': {'class': 'border-l-4 border-gray-300 pl-4 italic my-4'}},
            {'name': 'Code Block', 'element': 'pre', 'attributes': {'class': 'bg-gray-100 p-4 rounded my-4'}},
            {'name': 'Inline Code', 'element': 'code', 'attributes': {'class': 'bg-gray-100 px-1 py-0.5 rounded'}},
            {'name': 'Primary Button', 'element': 'a', 'attributes': {'class': 'btn btn-primary'}},
            {'name': 'Secondary Button', 'element': 'a', 'attributes': {'class': 'btn btn-secondary'}},
            {'name': 'Outline Button', 'element': 'a', 'attributes': {'class': 'btn btn-outline'}},
        ],
    },
}