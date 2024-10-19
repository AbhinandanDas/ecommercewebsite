import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = "django-insecure-4q5((j+k91#6^=+bfvhqh&-e$-c$0%co&(bs5rua@lil$6qmm="

DEBUG = True

ALLOWED_HOSTS = ["localhost", "yourdomain.com", "127.0.0.1"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "store",
    "basket",
    "account",
    "payment",
    "orders",
    "review",
    "mptt",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = "core.urls"

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
                "store.context_processors.categories",
                "basket.context_processors.basket",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom User Model
AUTH_USER_MODEL = "account.Customer"
LOGIN_REDIRECT_URL = "/account/dashboard"
LOGIN_URL = "/account/login/"

# Email setting
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Stripe Payment
os.environ.setdefault(
    "STRIPE_PUBLISHABLE_KEY",
    "pk_test_51PwI262KjvVWWPPo1SRTXFyi7DDthN9LW3AOvFYW0hBDntwEdBa9B6TRuqcVs2NawLHYSFFK2KXEGMFr4oc3HyD800BsHmHkm5",
)
SECRET_KEY = "sk_test_51PwI262KjvVWWPPokhq8qTod2TTL6SvG591IPkumNqkUFcFFu4RYWhy8M5VMrztwmf1DbxHa6Lu14nF3x8ODWr3j00g98Wweec"
STRIPE_ENDPOINT_SECRET = (
    "whsec_31c15dcf672c817887e6eb359ca668cf44881abd236696adc438b6bbc245bc72"
)
# stripe listen --forward-to localhost:8000/payment/webhook/
