# konsultan_karir/urls.py
from django.contrib import admin
from django.urls import path, include # Pastikan 'include' diimpor

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')), # Ini akan mengarahkan semua URL dari accounts/urls.py untuk halaman beranda
    path('accounts/', include('accounts.urls')), # Ini akan mengarahkan semua URL dari accounts/urls.py dengan prefix /accounts/
    # Anda bisa menambahkan URL lain di sini jika ada aplikasi lain
]
