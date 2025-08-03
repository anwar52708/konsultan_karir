from django.db import models
from django.contrib.auth.models import User
from datetime import date, time
from django.db.models.signals import post_save
from django.dispatch import receiver

class Konsultasi(models.Model):
    """
    Model untuk menyimpan detail permintaan konsultasi.
    Ini akan digunakan untuk fitur yang memerlukan login.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
    nama = models.CharField(max_length=100)
    email = models.EmailField()
    no_hp = models.CharField(max_length=20, blank=True, null=True)
    jurusan = models.CharField(max_length=100, blank=True, null=True) 
    minat_karir = models.TextField(blank=True, null=True)
    tanggal_janji = models.DateField(null=True, blank=True)
    waktu_janji = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=50, default='pending') 
    tanggal_dibuat = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Konsultasi {self.nama} pada {self.tanggal_janji} {self.waktu_janji}"

    class Meta:
        verbose_name_plural = "Konsultasi" 

class Profile(models.Model):
    """
    Model untuk menyimpan informasi profil tambahan untuk setiap pengguna.
    Terhubung satu-ke-satu dengan model User bawaan Django.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    alamat = models.CharField(max_length=255, blank=True, null=True)
    nomor_telepon = models.CharField(max_length=20, blank=True, null=True) 
    bio = models.TextField(blank=True, null=True)
    
    tanggal_lahir = models.DateField(blank=True, null=True)
    jenis_kelamin = models.CharField(max_length=10, blank=True, null=True, choices=[('Pria', 'Pria'), ('Wanita', 'Wanita'), ('Lainnya', 'Lainnya')])


    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Membuat objek Profile baru saat objek User baru dibuat.
    """
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Memastikan objek Profile disimpan saat objek User disimpan.
    """
    instance.profile.save()
