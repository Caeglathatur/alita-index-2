from .settings_base import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "(k#y&)_wn*c_pc6d-#q9e)y53k=0bczv7ss_0+py(hg7k6=e2c"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = []


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
    "DEFAULT_THROTTLE_CLASSES": (
        "index.api.throttles.BurstRateThrottle",
        "index.api.throttles.SustainedRateThrottle",
    ),
    "DEFAULT_THROTTLE_RATES": {"burst": "60/min", "sustained": "1500/day"},
}
