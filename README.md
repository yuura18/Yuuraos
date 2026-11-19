# Yuura OS
​Lingkungan CLI & telemetri Yuura OS yang berjalan di dalam Ubuntu (proot-distro) melalui Termux di Android.
​## Struktur Repositori

``` yuura-os/
├── README.md
├── install.sh
├── bin/
│   └── godmode
├── core/
│   ├── godmode.py
│   ├── godmode_ui.py
│   └── yuura_system_pulse.py
├── modules/
│   ├── yuura.py
│   ├── godmode_dumper.py
│   ├── yuura_core.py
│   ├── yuura_web.py
│   └── yuura_flasher.py
└── config/
    └── bashrc_snippet.sh

## Instalasi di Termux + Ubuntu
pkg update && pkg install -y proot-distro
proot-distro install ubuntu

Masuk ke shell Ubuntu

proot-distro login ubuntu

Masuk ke folder yuura-os lalu jalankan

sh install.sh

## Modul & Perintah Utama

System Pulse (core/yuura_system_pulse.py): Monitor penyimpanan, RAM, status ADB, dan baterai secara berkala.
​GodMode UI & CLI (core/godmode.py, core/godmode_ui.py, bin/godmode): Antarmuka telemetri dan kontrol perintah yuura list serta yuura status.
​Command Router & Agent (modules/yuura.py, modules/yuura_core.py): Menjalankan modul lokal, yuura list / yuuralist, update, install <paket>, dan eksekusi perintah sistem.
​GodMode Dumper (modules/godmode_dumper.py): Pemrosesan target/dump dan viewer laporan.
​Web Control Room (modules/yuura_web.py): Dashboard web Flask lokal di 127.0.0.1:5000 (memerlukan flask).
​Flasher Suite (modules/yuura_flasher.py): Deteksi mode perangkat (FASTBOOT, ADB, EDL, MTK_BROM), portal UBL, dan pemilih ROM (memerlukan android-tools-adb & android-tools-fastboot).

## Auto-Start (Opsional)
​Untuk mengaktifkan auto-start telemetri saat shell dibuka, tambahkan isi config/bashrc_snippet.sh ke ~/.bashrc:

cat config/bashrc_snippet.sh >> ~/.bashrc
(Tekan Ctrl + C untuk keluar dari loop System Pulse).

## Troubleshooting Singkat
​libmagic.so.1 not found: Jalankan apt-get update && apt-get install -y libmagic1 file.
​Kembali ke $ Termux setelah exit: Masuk lagi dengan proot-distro login ubuntu.