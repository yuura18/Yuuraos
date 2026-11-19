# Yuura OS

Antarmuka CLI GodMode dengan telemetri sistem ringan di Ubuntu root (`proot-distro` Termux).

## Cara Install (Pengguna Baru)

### 1. Persiapan di Termux (Sebelum Masuk ke Ubuntu)
Buka aplikasi **Termux**, lalu siapkan semua kebutuhan dasar berikut sebelum masuk ke Ubuntu:

1. **Izinkan akses penyimpanan HP** (ketuk **Allow / Izinkan** jika muncul pop-up):
   termux-setup-storage

2. **Perbarui daftar paket Termux & pasang `proot-distro` serta `git`**:
   pkg update -y && pkg upgrade -y
   pkg install -y proot-distro git

3. **Unduh dan pasang lingkungan Ubuntu**:
   proot-distro install ubuntu

4. **Masuk ke lingkungan Ubuntu**:
   proot-distro login ubuntu

### 2. Instalasi Yuura OS di Dalam Ubuntu
Setelah prompt berubah menjadi `root@localhost:~#` (di dalam Ubuntu), jalankan perintah berikut:

apt update && apt install -y git
git clone https://github.com/yuura18/Yuuraos.git
cd Yuuraos
chmod +x install.sh
./install.sh

### Catatan Jika Menemui Kendala Umum
- **Error `Could not switch user` / `_apt` saat `apt update` di `proot-distro`**: jalankan dengan opsi sandbox `root`:
  apt update -o APT::Sandbox::User=root && apt install -y -o APT::Sandbox::User=root git
- **Pastikan penulisan perintah tepat**: gunakan spasi yang benar (`git clone ...`, `apt update && apt install -y git`) dan perhatikan huruf besar/kecil nama folder (`Yuuraos`).
