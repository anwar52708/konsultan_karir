# konsultan_karir/settings.py
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# Kunci rahasia untuk keamanan aplikasi Django Anda.
# PASTIKAN untuk mengganti ini dengan kunci yang unik dan kompleks di lingkungan produksi!
SECRET_KEY = 'django-insecure-xxx' # Ganti 'django-insecure-xxx' dengan kunci acak yang kuat

# Mode Debug. Set False untuk produksi.
DEBUG = True

# Host yang diizinkan untuk melayani aplikasi Anda.
# Di lingkungan produksi, tambahkan domain Anda di sini, misal: ALLOWED_HOSTS = ['yourdomain.com']
ALLOWED_HOSTS = []

# Aplikasi yang terinstal di proyek Django Anda.
# Pastikan 'accounts' ada di sini.
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts', # <-- Pastikan aplikasi 'accounts' ditambahkan di sini
]

# Middleware yang digunakan oleh Django.
# Ini menangani sesi, autentikasi, perlindungan CSRF, dll.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URLconf utama proyek Anda.
ROOT_URLCONF = 'konsultan_karir.urls'

# Konfigurasi template Django.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Direktori di mana Django akan mencari file template.
        # Pastikan ini menunjuk ke folder 'templates' di root proyek Anda.
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True, # Mengizinkan aplikasi untuk memiliki folder 'templates' sendiri
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

# Aplikasi WSGI yang digunakan oleh server produksi.
WSGI_APPLICATION = 'konsultan_karir.wsgi.application'

# Konfigurasi database.
# Defaultnya adalah SQLite3, cocok untuk pengembangan.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Validator password bawaan Django.
# Anda bisa menambahkan atau menghapus validator di sini.
AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

# Pengaturan Internasionalisasi
LANGUAGE_CODE = 'id-id' # Mengubah ke Bahasa Indonesia
TIME_ZONE = 'Asia/Jakarta' # Mengatur zona waktu ke Jakarta
USE_I18N = True # Mengaktifkan sistem terjemahan Django
USE_TZ = True # Mengaktifkan dukungan zona waktu

# Pengaturan file statis (CSS, JavaScript, gambar, dll.)
STATIC_URL = 'static/'

# Tipe field default untuk primary key otomatis.
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# URL di mana pengguna dialihkan setelah login.
LOGIN_REDIRECT_URL = 'dashboard' # Arahkan ke halaman dashboard setelah login

# URL di mana pengguna dialihkan setelah logout.
LOGOUT_REDIRECT_URL = 'home' # Arahkan ke halaman beranda setelah logout

# Konfigurasi Message Storage
# Ini penting agar pesan 'messages' (misal: messages.success) berfungsi
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Konfigurasi media (untuk file yang diunggah pengguna, misal: gambar profil)
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
