from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

# Load environment variables
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ===================== SECURITY =====================
# Load SECRET_KEY from env; in production (DEBUG=False) it must be set.
SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG", "False") == "True"

if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "unsafe-dev-key"
    else:
        raise RuntimeError("SECRET_KEY environment variable is required in production")

ALLOWED_HOSTS = ["*"]

# ===================== APPLICATIONS =====================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "social_django",
    "heart_charity.apps.HeartCharityConfig",
]

# ===================== MIDDLEWARE =====================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
]

ROOT_URLCONF = "ngo.urls"
WSGI_APPLICATION = "ngo.wsgi.application"

# ===================== TEMPLATES =====================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.login_redirect",
                "social_django.context_processors.backends",
            ],
        },
    },
]

# ===================== DATABASE =====================
# Prefer `DATABASE_URL` (Railway provides it). Fall back to DB_* env vars,
# then to a local sqlite file for development.
DATABASE_URL = os.getenv("DATABASE_URL")
db_config = {}
if DATABASE_URL:
    # parse returns a Django DATABASES-compatible dict
    try:
        db_config = dj_database_url.parse(DATABASE_URL, conn_max_age=600, ssl_require=True)
    except Exception:
        db_config = {}

if not db_config and os.getenv("DB_NAME"):
    db_config = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }

if not db_config:
    db_config = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }

DATABASES = {"default": db_config}

# ===================== PASSWORD VALIDATION =====================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ===================== INTERNATIONALIZATION =====================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ===================== STATIC FILES =====================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ===================== AUTHENTICATION =====================
AUTHENTICATION_BACKENDS = (
    "social_core.backends.google.GoogleOAuth2",
    "django.contrib.auth.backends.ModelBackend",
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv("GOOGLE_CLIENT_ID")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

LOGIN_URL = "login"
LOGOUT_URL = "logout"
LOGIN_REDIRECT_URL = "/welcome/"
LOGOUT_REDIRECT_URL = "/"

SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "social_core.pipeline.user.create_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
)

# ===================== EMAIL =====================
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
