# accounts/admin.py
from django.contrib import admin
from .models import Konsultasi, Profile # Impor model Anda
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Batalkan pendaftaran model User bawaan Django untuk sementara
admin.site.unregister(User)

# Daftarkan model Konsultasi
@admin.register(Konsultasi)
class KonsultasiAdmin(admin.ModelAdmin):
    """
    Konfigurasi untuk tampilan admin model Konsultasi.
    """
    list_display = ('nama', 'email', 'service_display', 'tanggal_janji', 'waktu_janji', 'status', 'user', 'tanggal_dibuat')
    list_filter = ('status', 'tanggal_janji', 'user')
    search_fields = ('nama', 'email', 'minat_karir', 'no_hp')
    date_hierarchy = 'tanggal_dibuat' # Memungkinkan navigasi berdasarkan tanggal

    def service_display(self, obj):
        """
        Mengekstrak dan menampilkan jenis layanan dari field minat_karir
        untuk tampilan yang lebih rapi di admin.
        """
        if obj.minat_karir and "Jenis Layanan:" in obj.minat_karir:
            return obj.minat_karir.split("Jenis Layanan:")[1].split("\n")[0].strip()
        return obj.minat_karir if obj.minat_karir else "N/A"
    service_display.short_description = "Jenis Layanan" # Nama kolom di admin

# Definisikan inline admin untuk model Profile
# Ini akan memungkinkan Anda mengedit profil pengguna langsung dari halaman admin User.
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False # Tidak mengizinkan penghapusan profil tanpa menghapus pengguna
    verbose_name_plural = 'Profile' # Nama yang ditampilkan di admin

# Daftarkan ulang UserAdmin dengan inline Profile
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Konfigurasi kustom untuk tampilan admin model User,
    menambahkan field dari model Profile.
    """
    inlines = (ProfileInline,) # Menambahkan inline Profile ke admin User
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_nomor_telepon', 'get_alamat')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

    # Metode untuk menampilkan field dari model Profile di list_display User
    def get_nomor_telepon(self, obj):
        return obj.profile.nomor_telepon
    get_nomor_telepon.short_description = 'Nomor Telepon' # Nama kolom di admin

    def get_alamat(self, obj):
        return obj.profile.alamat
    get_alamat.short_description = 'Alamat' # Nama kolom di admin

    # Anda bisa menyesuaikan fieldsets jika ingin mengubah tata letak form admin User
    fieldsets = UserAdmin.fieldsets + (
        (('Informasi Profil Tambahan', {'fields': ('tanggal_lahir', 'jenis_kelamin')}),) # Contoh penambahan field dari Profile
    )
