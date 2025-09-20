from pathlib import Path
import os
import sys
from datetime import timedelta
import environ

# ==============================
# Environment
# ==============================
env = environ.Env(DEBUG=(bool, False))

BASE_DIR = Path(__file__).resolve().parent.parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, "backend", ".env"))

# Add backend to sys.path
sys.path.append(str(BASE_DIR / "backend"))

# ==============================
# Security
# ==============================
SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DJANGO_DEBUG")

ALLOWED_HOSTS = [
    h.strip()
    for h in os.getenv(
        "DJANGO_ALLOWED_HOSTS",
        "127.0.0.1,localhost,10.0.2.2,192.168.20.9,a71c5ff0df5b.ngrok-free.app",
    ).split(",")
]

if "RAILWAY_PUBLIC_DOMAIN" in os.environ:
    ALLOWED_HOSTS.append(os.environ["RAILWAY_PUBLIC_DOMAIN"])

# OAuth requires HTTPS (for Google/Facebook in production)
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

# ==============================
# Installed Apps
# ==============================
INSTALLED_APPS = [
    # Local apps
    "apps.users",
    "apps.tourism",
    "apps.content",
    "apps.ar",
    "apps.events",
    "apps.business",
    "apps.dashboards",
    
    # 3rd-party apps
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt.token_blacklist",
    "rest_framework_simplejwt",
    "dj_rest_auth",
    "django_extensions",
    "widget_tweaks",
    "whitenoise.runserver_nostatic",
    "sass_processor",
    
    # Allauth
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.facebook",
    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# ==============================
# Authentication
# ==============================
AUTH_USER_MODEL = "users.CustomUser"

AUTHENTICATION_BACKENDS = (
    "allauth.account.auth_backends.AuthenticationBackend",
    "django.contrib.auth.backends.ModelBackend",  # Django admin login
)

# ==============================
# Password Validation
# ==============================
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ==============================
# Login / Logout behavior
# ==============================

LOGIN_URL = "account_login"
LOGOUT_URL = "account_logout"
LOGIN_REDIRECT_URL = "/"  # after login
LOGOUT_REDIRECT_URL = "/"  # after logout

# Important: prevent logout loop
ACCOUNT_LOGOUT_ON_GET = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SOCIALACCOUNT_LOGIN_ON_GET = True

# ==============================
# Allauth
# ==============================
SITE_ID = 1

ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_LOGIN_METHODS = {"username", "email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "username*", "password1*", "password2*"]
ACCOUNT_FORMS = {
    "signup": "apps.users.forms.CustomSignupForm",
}

SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_STORE_TOKENS = True
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_ADAPTER = "apps.users.adapters.CustomSocialAccountAdapter"


# ==============================
# Middleware
# ==============================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ==============================
# URLS / WSGI
# ==============================
ROOT_URLCONF = "bicoltravelguide.urls"
WSGI_APPLICATION = "bicoltravelguide.wsgi.application"

# ==============================
# Templates
# ==============================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "frontend", "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ==============================
# Database
# ==============================
DATABASES = {"default": env.db()}


# ==============================
# Internationalization
# ==============================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ==============================
# Static & Media
# ==============================
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "backend", "staticfiles")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "shared", "static")]

SASS_PROCESSOR_ROOT = BASE_DIR / "frontend" / "static"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# ==============================
# DRF / JWT
# ==============================
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
}


# ==============================
# CORS
# ==============================
CORS_ALLOW_ALL_ORIGINS = True

# ==============================
# Providers config
# ==============================
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": "712453614509-kh2433d997g0dh08jin7p46d7r9kts0r.apps.googleusercontent.com",
            "secret": "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",
            "key": "",
        },
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
    },
    "facebook": {
        "APP": {
            "client_id": "622485894252208",
            "secret": "dbecd3b729a5afe2b08a9d85fac70e9c",
            "key": "",
        },
        "SCOPE": ["email"],
        "FIELDS": ["id", "email", "first_name", "last_name", "name", "picture"],
    },
}
