from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User 
from .models import Konsultasi, Profile 

class KonsultasiForm(forms.ModelForm):
    """
    Formulir ini digunakan untuk membuat atau memperbarui objek Konsultasi.
    Field yang disertakan berasal dari model Konsultasi.
    """
    class Meta:
        model = Konsultasi
        fields = ['nama', 'email', 'no_hp', 'jurusan', 'minat_karir', 'tanggal_janji', 'waktu_janji', 'status'] 
        widgets = {
            'tanggal_janji': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'waktu_janji': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'status': forms.Select(choices=[('pending', 'Pending'), ('terjadwal', 'Terjadwal'), ('selesai', 'Selesai')], attrs={'class': 'form-control'}), 
            'nama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Lengkap Anda'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Anda'}),
            'no_hp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nomor Telepon (opsional)'}),
            'jurusan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Jurusan/Bidang Studi Anda'}),
            'minat_karir': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Jelaskan minat karir atau tujuan Anda'}),
        }
        labels = {
            'nama': 'Nama Lengkap',
            'email': 'Alamat Email',
            'no_hp': 'Nomor Telepon',
            'jurusan': 'Jurusan/Bidang Studi',
            'minat_karir': 'Minat Karir / Tujuan',
            'tanggal_janji': 'Tanggal Janji Temu',
            'waktu_janji': 'Waktu Janji Temu',
            'status': 'Status Konsultasi', 
        }

class UserLoginForm(AuthenticationForm):
    """
    Formulir ini digunakan untuk login pengguna.
    Ini memperluas AuthenticationForm bawaan Django.
    """
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class ConsultationForm(forms.Form):
    """
    Formulir ini digunakan untuk permintaan konsultasi dari pengguna publik (tidak perlu login).
    """
    name = forms.CharField(
        max_length=100,
        label="Nama Lengkap",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan nama lengkap Anda'})
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan alamat email Anda'})
    )
    phone_number = forms.CharField(
        max_length=20,
        required=False,
        label="Nomor Telepon (Opsional)",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: +6281234567890'})
    )
    tanggal_janji = forms.DateField(
        required=False,
        label="Tanggal Janji Temu Pilihan",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    waktu_janji = forms.TimeField(
        required=False,
        label="Waktu Janji Temu Pilihan",
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})
    )
    service_type = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Sertakan detail lebih lanjut tentang kebutuhan konsultasi Anda.'}),
        label="Pesan Anda",
        help_text="Sertakan detail lebih lanjut tentang kebutuhan konsultasi Anda."
    )

class ProfileForm(forms.ModelForm):
    """
    Formulir ini digunakan untuk mengedit informasi profil tambahan pengguna.
    """
    class Meta:
        model = Profile
        fields = ['alamat', 'nomor_telepon', 'bio', 'tanggal_lahir', 'jenis_kelamin']
        widgets = {
            'alamat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Alamat Lengkap Anda'}),
            'nomor_telepon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nomor Telepon Anda'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tulis bio singkat tentang diri Anda'}),
            'tanggal_lahir': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'jenis_kelamin': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'alamat': 'Alamat',
            'nomor_telepon': 'Nomor Telepon',
            'bio': 'Bio',
            'tanggal_lahir': 'Tanggal Lahir',
            'jenis_kelamin': 'Jenis Kelamin',
        }

class UserUpdateForm(forms.ModelForm):
    """
    Formulir ini digunakan untuk mengedit field dasar model User (misalnya nama depan, nama belakang, email).
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email'] 
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Depan'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Belakang'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }
        labels = {
            'first_name': 'Nama Depan',
            'last_name': 'Nama Belakang',
            'email': 'Email',
        }
