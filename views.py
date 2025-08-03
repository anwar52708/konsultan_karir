# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime, timedelta
from django.db.models import Count # Import Count untuk agregasi
from collections import Counter # Untuk menghitung frekuensi item

# Mengimpor SEMUA form yang dibutuhkan dari accounts.forms
from .forms import (
    KonsultasiForm as OriginalKonsultasiForm,
    UserLoginForm,
    ConsultationForm,
    ProfileForm,
    UserUpdateForm
)

# Mengimpor model Konsultasi dan Profile
from .models import Konsultasi, Profile

# Tampilan untuk halaman beranda utama (landing page)
def home(request):
    """
    Menampilkan halaman beranda.
    """
    return render(request, 'accounts/home.html')

# Tampilan untuk halaman login pengguna
def login_view(request):
    """
    Menangani proses login pengguna.
    """
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Selamat datang kembali, {username}!")
                return redirect('dashboard')
            else:
                messages.error(request, "Username atau password salah.")
        else:
            messages.error(request, "Terjadi kesalahan saat login. Mohon periksa input Anda.")
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

# Tampilan untuk logout pengguna
@login_required
def logout_view(request):
    """
    Menangani proses logout pengguna.
    """
    logout(request)
    messages.info(request, "Anda telah berhasil logout.")
    return redirect('home')

# Tampilan untuk dashboard konsultan (membutuhkan login)
@login_required
def dashboard(request):
    """
    Menampilkan dashboard konsultan dengan ringkasan data.
    """
    # Contoh data dummy atau data yang bisa Anda ambil dari database
    client_count = Konsultasi.objects.filter(user=request.user).values('email').distinct().count()
    today = datetime.now().date()
    today_appointments = Konsultasi.objects.filter(
        user=request.user,
        tanggal_janji=today,
        status='terjadwal'
    ).count()
    new_consultations = Konsultasi.objects.filter(
        user=request.user,
        tanggal_dibuat__date=today,
        status='pending'
    ).count()

    # Contoh data untuk Janji Mendatang (Anda perlu menyesuaikannya dengan kebutuhan Anda)
    upcoming_appointments = Konsultasi.objects.filter(
        user=request.user,
        tanggal_janji__gte=today, # Tanggal janji lebih besar atau sama dengan hari ini
        status='terjadwal'
    ).order_by('tanggal_janji', 'waktu_janji')[:5] # Ambil 5 janji mendatang

    # Contoh data aktivitas terkini (Anda perlu menyesuaikannya)
    # Ini masih dummy, Anda bisa membuat model ActivityLog untuk ini
    recent_activities = [
        {'description': 'Konsultasi baru dari John Doe', 'time': datetime.now() - timedelta(minutes=30)},
        {'description': 'Janji temu dengan Jane Smith dijadwalkan ulang', 'time': datetime.now() - timedelta(hours=2)},
        {'description': 'Profil Anda diperbarui', 'time': datetime.now() - timedelta(days=1)},
    ]

    # Contoh rating rata-rata (jika Anda memiliki sistem rating)
    # Saat ini masih hardcoded
    avg_rating = 4.7

    context = {
        'client_count': client_count,
        'today_appointments': today_appointments,
        'new_consultations': new_consultations,
        'avg_rating': avg_rating,
        'upcoming_appointments': upcoming_appointments,
        'recent_activities': recent_activities,
    }
    return render(request, 'accounts/dashboard.html', context)

# Tampilan untuk daftar klien (membutuhkan login)
@login_required
def clients(request):
    """
    Menampilkan daftar klien.
    """
    # Mengambil semua email unik yang terkait dengan user yang login
    distinct_emails = Konsultasi.objects.filter(user=request.user).values_list('email', flat=True).distinct()

    clients_list = []
    for email in distinct_emails:
        # Dapatkan konsultasi terbaru untuk email ini dan user yang login
        latest_konsultasi = Konsultasi.objects.filter(
            user=request.user,
            email=email
        ).order_by('-tanggal_dibuat').first() # Ambil yang terbaru

        if latest_konsultasi:
            clients_list.append({
                'pk': latest_konsultasi.pk, # Tambahkan primary key di sini
                'nama': latest_konsultasi.nama,
                'email': latest_konsultasi.email,
                'no_hp': latest_konsultasi.no_hp,
                'jurusan': latest_konsultasi.jurusan,
                'minat_karir': latest_konsultasi.minat_karir,
                'terakhir_konsultasi': latest_konsultasi.tanggal_dibuat.strftime("%d %b %Y"),
                'status_terakhir': latest_konsultasi.status,
            })

    context = {
        'clients': clients_list
    }
    return render(request, 'accounts/clients.html', context)


# Tampilan untuk daftar janji temu (membutuhkan login)
@login_required
def appointments(request):
    """
    Menampilkan daftar janji temu.
    """
    # Mengambil semua janji temu untuk pengguna yang login, diurutkan berdasarkan tanggal dan waktu
    all_appointments = Konsultasi.objects.filter(user=request.user).order_by('tanggal_janji', 'waktu_janji')
    context = {
        'appointments': all_appointments
    }
    return render(request, 'accounts/appointments.html', context)

# Tampilan untuk laporan (membutuhkan login)
@login_required
def reports(request):
    """
    Menampilkan laporan dan statistik.
    """
    current_month = datetime.now().month
    current_year = datetime.now().year

    # Total Konsultasi Bulan Ini
    total_consultations_month = Konsultasi.objects.filter(
        user=request.user,
        tanggal_dibuat__month=current_month,
        tanggal_dibuat__year=current_year
    ).count()

    # Klien Baru Bulan Ini (berdasarkan email unik yang pertama kali muncul di bulan ini)
    # Ini adalah contoh sederhana, mungkin perlu logika lebih kompleks untuk definisi "klien baru"
    new_clients_month = Konsultasi.objects.filter(
        user=request.user,
        tanggal_dibuat__month=current_month,
        tanggal_dibuat__year=current_year
    ).values('email').distinct().count()

    # Layanan Paling Populer
    # Ambil semua minat_karir untuk user yang login di bulan ini
    all_minat_karir = Konsultasi.objects.filter(
        user=request.user,
        tanggal_dibuat__month=current_month,
        tanggal_dibuat__year=current_year
    ).values_list('minat_karir', flat=True)

    popular_service = "Tidak Ada Data"
    if all_minat_karir:
        # Ekstrak jenis layanan dari string minat_karir
        service_types = []
        for item in all_minat_karir:
            if item and "Jenis Layanan:" in item:
                service_name = item.split("Jenis Layanan:")[1].split("\n")[0].strip()
                service_types.append(service_name)
            elif item: # Jika tidak ada "Jenis Layanan:", gunakan seluruh minat_karir sebagai layanan
                service_types.append(item.strip())

        if service_types:
            # Hitung frekuensi setiap jenis layanan
            service_counts = Counter(service_types)
            # Dapatkan layanan yang paling umum
            popular_service = service_counts.most_common(1)[0][0]
        else:
            popular_service = "Tidak Ada Data Layanan"


    # Data untuk Grafik Contoh (Anda bisa menyesuaikan ini dengan data nyata)
    # Contoh: Jumlah konsultasi per status
    consultation_status_data = Konsultasi.objects.filter(user=request.user).values('status').annotate(count=Count('status'))
    
    # Format data untuk grafik (misalnya untuk Chart.js)
    chart_labels = [item['status'].capitalize() for item in consultation_status_data]
    chart_data = [item['count'] for item in consultation_status_data]

    context = {
        'total_consultations_month': total_consultations_month,
        'new_clients_month': new_clients_month,
        'popular_service': popular_service,
        'chart_labels': chart_labels, # Data untuk label grafik
        'chart_data': chart_data,   # Data untuk nilai grafik
    }
    return render(request, 'accounts/reports.html', context)

# Tampilan untuk jadwal (membutuhkan login)
@login_required
def schedule(request):
    """
    Menampilkan jadwal konsultan.
    """
    # Anda bisa mengambil janji temu dari database di sini
    # Untuk contoh, kita akan menampilkan semua janji temu yang terjadwal
    scheduled_appointments = Konsultasi.objects.filter(user=request.user, status='terjadwal').order_by('tanggal_janji', 'waktu_janji')
    context = {
        'scheduled_appointments': scheduled_appointments
    }
    return render(request, 'accounts/schedule.html', context)

# Tampilan untuk halaman tentang kami
def about(request):
    """
    Menampilkan halaman tentang kami.
    """
    return render(request, 'accounts/about.html')

# Tampilan untuk halaman kontak
def contact(request):
    """
    Menampilkan halaman kontak.
    """
    return render(request, 'accounts/contact.html')

# Tampilan untuk halaman layanan karir
def career_services_view(request):
    """
    Menampilkan halaman layanan karir yang tersedia.
    """
    return render(request, 'accounts/career_services.html')

# Tampilan untuk formulir konsultasi publik
def consultation_form_view(request, service_name=None):
    """
    Menangani formulir permintaan konsultasi publik.
    """
    initial_data = {}
    if service_name:
        # Mengubah nama layanan menjadi format yang lebih mudah dibaca jika diperlukan
        display_service_name = service_name.replace('-', ' ').title()
        initial_data['service_type'] = display_service_name

    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            # Simpan data ke model Konsultasi
            Konsultasi.objects.create(
                user=None, # Karena ini konsultasi publik, tidak ada user yang login
                nama=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                no_hp=form.cleaned_data['phone_number'],
                # Gabungkan service_type dan message ke minat_karir
                minat_karir=f"Jenis Layanan: {form.cleaned_data['service_type'] or 'Tidak Specified'}\nPesan: {form.cleaned_data['message']}",
                tanggal_janji=form.cleaned_data['tanggal_janji'],
                waktu_janji=form.cleaned_data['waktu_janji'],
                status='pending' # Status awal selalu pending
            )
            messages.success(request, "Permintaan konsultasi Anda telah berhasil dikirim!")
            return redirect('consultation_success')
        else:
            messages.error(request, "Terjadi kesalahan saat mengirim formulir. Mohon periksa input Anda.")
    else:
        form = ConsultationForm(initial=initial_data)

    context = {
        'form': form,
        'service_name': service_name # Untuk menampilkan nama layanan di template
    }
    return render(request, 'accounts/consultation_form.html', context)

# Tampilan untuk halaman sukses konsultasi
def consultation_success_view(request):
    """
    Menampilkan halaman sukses setelah formulir konsultasi dikirim.
    """
    return render(request, 'accounts/consultation_success.html')

# Tampilan untuk membuat konsultasi baru (membutuhkan login)
@login_required
def create_konsultasi(request):
    """
    Menangani pembuatan entri konsultasi baru oleh konsultan.
    """
    if request.method == 'POST':
        form = OriginalKonsultasiForm(request.POST)
        if form.is_valid():
            konsultasi = form.save(commit=False)
            konsultasi.user = request.user # Kaitkan konsultasi dengan pengguna yang login
            konsultasi.save()
            messages.success(request, "Konsultasi baru berhasil ditambahkan!")
            return redirect('detail_konsultasi', pk=konsultasi.pk)
        else:
            messages.error(request, "Terjadi kesalahan saat menambahkan konsultasi. Mohon periksa input Anda.")
    else:
        form = OriginalKonsultasiForm()
    return render(request, 'accounts/create_konsultasi.html', {'form': form})

# Tampilan untuk detail konsultasi (membutuhkan login)
@login_required
def detail_konsultasi(request, pk):
    """
    Menampilkan detail entri konsultasi tertentu.
    """
    # Pastikan konsultasi yang diakses milik pengguna yang login
    konsultasi = get_object_or_404(Konsultasi, pk=pk, user=request.user)
    return render(request, 'accounts/detail_konsultasi.html', {'konsultasi': konsultasi})

# Tampilan untuk memperbarui konsultasi (membutuhkan login)
@login_required
def update_konsultasi(request, pk):
    """
    Menangani pembaruan entri konsultasi yang sudah ada.
    """
    konsultasi = get_object_or_404(Konsultasi, pk=pk, user=request.user)
    if request.method == 'POST':
        form = OriginalKonsultasiForm(request.POST, instance=konsultasi)
        if form.is_valid():
            form.save()
            messages.success(request, "Konsultasi berhasil diperbarui!")
            return redirect('detail_konsultasi', pk=konsultasi.pk)
        else:
            messages.error(request, "Terjadi kesalahan saat memperbarui konsultasi. Mohon periksa input Anda.")
    else:
        form = OriginalKonsultasiForm(instance=konsultasi)
    return render(request, 'accounts/update_konsultasi.html', {'form': form, 'konsultasi': konsultasi})

# Tampilan untuk menghapus konsultasi (membutuhkan login)
@login_required
def delete_konsultasi(request, pk):
    """
    Menangani penghapusan entri konsultasi.
    """
    konsultasi = get_object_or_404(Konsultasi, pk=pk, user=request.user)
    if request.method == 'POST':
        konsultasi.delete()
        messages.success(request, "Konsultasi berhasil dihapus.")
        return redirect('appointments') # Redirect ke daftar janji temu setelah penghapusan
    return render(request, 'accounts/delete_konsultasi_confirm.html', {'konsultasi': konsultasi}) # Anda perlu membuat template ini

# Tampilan untuk halaman pengaturan (membutuhkan login)
@login_required
def settings(request):
    """
    Menampilkan halaman pengaturan pengguna.
    """
    return render(request, 'accounts/settings.html')

# Tampilan untuk halaman profil pengguna (membutuhkan login)
@login_required
def profile(request):
    """
    Menampilkan halaman profil pengguna.
    """
    # Pastikan objek profil ada untuk pengguna saat ini
    profile_obj, created = Profile.objects.get_or_create(user=request.user)

    context = {
        'user_profile': {
            'username': request.user.username,
            'email': request.user.email,
            'full_name': request.user.first_name + ' ' + request.user.last_name if request.user.first_name or request.user.last_name else 'Nama Lengkap Pengguna',
            'bio': profile_obj.bio, # Ambil bio dari objek Profile
            'alamat': profile_obj.alamat, # Ambil alamat dari objek Profile
            'nomor_telepon': profile_obj.nomor_telepon, # Ambil nomor telepon dari objek Profile
            'tanggal_lahir': profile_obj.tanggal_lahir,
            'jenis_kelamin': profile_obj.jenis_kelamin,
        }
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def update_profile(request):
    """
    Menangani pembaruan informasi profil pengguna.
    """
    profile_obj, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=profile_obj)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profil Anda berhasil diperbarui!")
            return redirect('profile')
        else:
            messages.error(request, "Terjadi kesalahan saat memperbarui profil. Mohon periksa input Anda.")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=profile_obj)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'accounts/update_profile.html', context)

@login_required
def pending_consultations(request):
    """
    Menampilkan daftar konsultasi publik yang belum ditugaskan (user=None)
    dan berstatus 'pending'.
    """
    pending_list = Konsultasi.objects.filter(user__isnull=True, status='pending').order_by('tanggal_dibuat')
    context = {
        'pending_consultations': pending_list
    }
    return render(request, 'accounts/pending_consultations.html', context)

@login_required
def assign_consultation(request, pk):
    """
    Menugaskan konsultasi publik tertentu kepada konsultan yang sedang login
    dan mengubah statusnya menjadi 'terjadwal'.
    """
    konsultasi = get_object_or_404(Konsultasi, pk=pk, user__isnull=True, status='pending')
    if request.method == 'POST':
        konsultasi.user = request.user
        konsultasi.status = 'terjadwal'
        konsultasi.save()
        messages.success(request, f"Konsultasi dari {konsultasi.nama} berhasil ditugaskan kepada Anda dan dijadwalkan!")
        return redirect('pending_consultations') # Kembali ke daftar pending
    # Jika bukan POST request, mungkin redirect atau tampilkan error
    messages.error(request, "Metode tidak diizinkan untuk penugasan konsultasi.")
    return redirect('pending_consultations') # Atau ke halaman detail konsultasi jika ada

# Tampilan untuk membatalkan janji temu (membutuhkan login)
@login_required
def cancel_appointment(request, pk):
    """
    Menangani pembatalan janji temu tertentu.
    """
    konsultasi = get_object_or_404(Konsultasi, pk=pk, user=request.user)
    if request.method == 'POST':
        konsultasi.status = 'dibatalkan' # Ubah status menjadi dibatalkan
        konsultasi.save()
        messages.success(request, f"Janji temu dengan {konsultasi.nama} berhasil dibatalkan.")
        return redirect('appointments') # Kembali ke daftar janji temu
    # Jika bukan POST request, mungkin redirect atau tampilkan error
    messages.error(request, "Metode tidak diizinkan untuk pembatalan janji temu.")
    return redirect('appointments')

# Tampilan untuk menerima/menyetujui janji temu (membutuhkan login)
@login_required
def accept_appointment(request, pk):
    """
    Menangani penerimaan/persetujuan janji temu tertentu.
    Mengubah status menjadi 'terjadwal'.
    """
    # Hanya izinkan menerima janji temu yang masih 'pending' atau 'dibatalkan' (jika ingin bisa diaktifkan kembali)
    # Sesuaikan query sesuai logika bisnis Anda
    konsultasi = get_object_or_404(Konsultasi, pk=pk, user=request.user)
    if request.method == 'POST':
        # Pastikan hanya status tertentu yang bisa diterima
        if konsultasi.status == 'pending' or konsultasi.status == 'dibatalkan':
            konsultasi.status = 'terjadwal' # Ubah status menjadi terjadwal
            konsultasi.save()
            messages.success(request, f"Janji temu dengan {konsultasi.nama} berhasil diterima dan dijadwalkan!")
            return redirect('appointments') # Kembali ke daftar janji temu
        else:
            messages.warning(request, "Janji temu ini tidak dapat diterima karena statusnya bukan 'pending' atau 'dibatalkan'.")
            return redirect('appointments')
    messages.error(request, "Metode tidak diizinkan untuk penerimaan janji temu.")
    return redirect('appointments')
