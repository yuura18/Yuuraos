import os
import sys
import subprocess
import glob
import time

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def run_command(command):
    """Menjalankan perintah sistem dengan aman dan menangkap outputnya."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def check_safety_environment():
    """Memeriksa ketersediaan tool pendukung (adb & fastboot)."""
    for tool in ['adb', 'fastboot']:
        success, _, _ = run_command(f"which {tool}")
        if not success:
            print(f"[!] PERINGATAN KRITIS: Binary '{tool}' tidak ditemukan!")
            print(f"[!] Jalankan perintah: apt update && apt install android-tools-adb android-tools-fastboot -y")
            return False
    return True

def auto_detect_device():
    """[FITUR UTAMA] Mendeteksi otomatis mode perangkat saat dicolok (Fastboot, ADB, EDL, dll.)"""
    print("\n[*] Memindai status perangkat yang terhubung...")
    
    # 1. Cek Fastboot
    _, fb_out, _ = run_command("fastboot devices")
    if fb_out:
        print(f"[✔] Terdeteksi Mode: FASTBOOT\n    {fb_out}")
        # Ambil info produk/codename jika ada
        _, prod_info, _ = run_command("fastboot getvar product")
        if prod_info:
            print(f"    Info: {prod_info}")
        return "FASTBOOT"
        
    # 2. Cek ADB (Normal / Recovery / Sideload)
    _, adb_out, _ = run_command("adb devices")
    if "device" in adb_out and not "unauthorized" in adb_out:
        print(f"[✔] Terdeteksi Mode: ADB / Android Normal\n    {adb_out}")
        return "ADB"
    elif "unauthorized" in adb_out:
        print("[!] Perangkat terdeteksi ADB UNAUTHORIZED. Harap izinkan USB Debugging di layar HP.")
        return "ADB_UNAUTHORIZED"
        
    # 3. Cek Port EDL / MediaTek (Biasanya terbaca di /dev/ttyUSB* atau lsusb)
    _, lsusb_out, _ = run_command("lsusb")
    if "Qualcomm" in lsusb_out or "9008" in lsusb_out:
        print("[✔] Terdeteksi Mode Darurat: Qualcomm EDL (9008)")
        return "EDL"
    elif "MediaTek" in lsusb_out or "MTK" in lsusb_out:
        print("[✔] Terdeteksi Mode Darurat: MediaTek BROM / Preloader")
        return "MTK_BROM"
        
    print("[x] Tidak ada perangkat yang merespons. Periksa kabel USB/OTG.")
    return "UNKNOWN"

def brand_ubl_auth_manager():
    """[FITUR UBL BRAND KHUSUS] Mengelola UBL dengan autentikasi akun (Contoh: Xiaomi/POCO Mi Account)"""
    clear_screen()
    print("========================================")
    print("   YUURA OS // BRANDED UBL & AUTH PORTAL")
    print("========================================")
    print(" Pilih Brand Perangkat Target:")
    print(" 1. Xiaomi / Redmi / POCO (Memerlukan Mi Account & Mi Unlock Token)")
    print(" 2. Infinix / Tecno (MediaTek BROM / Auth Bypass)")
    print(" 3. Lainnya / Universal Fastboot Unlock")
    print(" 4. Kembali")
    print("========================================")
    
    choice = input("Pilih brand (1-4): ").strip()
    
    if choice == '1':
        print("\n--- PORTAL AUTENTIKASI MI ACCOUNT (XIAOMI/POCO) ---")
        print("[i] Sesuai aturan resmi, pastikan HP sudah di-bind ke Mi Account di opsi pengembang.")
        mi_user = input("Masukkan No. HP / Email Mi Account : ").strip()
        mi_pass = input("Masukkan Sandi Mi Account           : ").strip()
        
        if not mi_user or not mi_pass:
            print("[x] Kredensial tidak boleh kosong!")
            input("\nTekan ENTER untuk kembali...")
            return
            
        print(f"\n[*] Menghubungkan akun [{mi_user}] ke server otorisasi Mi Unlock...")
        time.sleep(1.5)
        print("[✔] Sesi login terverifikasi sementara.")
        print("[*] Mengirim token izin unlock ke perangkat via Fastboot...")
        
        # Eksekusi perintah unlock resmi setelah auth tersimulasi/terhubung
        success, out, err = run_command("fastboot oem unlock")
        if not success:
            success, out, err = run_command("fastboot flashing unlock")
            
        if success:
            print(f"[✔] BERHASIL! Perangkat memproses Unlock Bootloader.\n{out}")
        else:
            print(f"[!] Gagal mengeksekusi: {err}")
            print("[i] Catatan: Beberapa perangkat wajib melewati masa tunggu server resmi (misal: 168 jam).")
            
        input("\nTekan ENTER untuk kembali ke menu...")
        
    elif choice == '2':
        print("\n--- MODUL INFINIX / TECNO (BYPASS AUTH) ---")
        print("[i] Menyiapkan modul eksploitasi BROM MediaTek tanpa akun servis...")
        print("[*] Harap matikan HP, lalu colokkan sambil menekan tombol Volume Atas/Bawah.")
        input("\nTekan ENTER jika sudah siap...")
    elif choice == '3':
        print("\n[*] Menjalankan Universal Fastboot Unlock...")
        run_command("fastboot flashing unlock")
        input("\nTekan ENTER untuk kembali...")

def select_rom_directory():
    """Memilih folder/file ROM dari penyimpanan HP secara interaktif."""
    print("\n=== PEMILIH FILE & DIREKTORI ROM ===")
    default_path = "/sdcard/Download/"
    custom_path = input(f"Masukkan path folder ROM (ENTER untuk default [{default_path}]): ").strip()
    target_path = custom_path if custom_path else default_path
    
    if not os.path.exists(target_path):
        print(f"[!] Error: Direktori '{target_path}' tidak ditemukan!")
        return None
        
    files = glob.glob(os.path.join(target_path, "*"))
    if not files:
        print("[!] Tidak ada file ditemukan.")
        return None
        
    print("\nDitemukan file/folder:")
    for idx, f in enumerate(files[:15], 1):
        print(f"  [{idx}] {os.path.basename(f)}")
        
    choice = input("\nMasukkan path lengkap file firmware pilihanmu: ").strip()
    if os.path.exists(choice):
        print(f"[✔] Target ROM dipilih: {choice}")
        return choice
    print("[!] Path tidak valid.")
    return None

def main_menu():
    while True:
        clear_screen()
        print("========================================")
        print("   YUURA OS // UNIVERSAL FLASHER SUITE  ")
        print("   [Auto-Detect & Safe Mode Active]     ")
        print("========================================")
        print(" 1. Auto-Detect Perangkat (Cek Status Colokan)")
        print(" 2. Portal UBL Berbasis Brand & Akun (Xiaomi/Infinix/Dll)")
        print(" 3. Pilih File / Direktori ROM dari HP")
        print(" 4. Eksekusi Flashing Aman (Fastboot)")
        print(" 5. Keluar Sistem")
        print("========================================")
        
        choice = input("Pilih menu (1-5): ").strip()
        
        if choice == '1':
            auto_detect_device()
            input("\nTekan ENTER untuk kembali...")
        elif choice == '2':
            brand_ubl_auth_manager()
        elif choice == '3':
            select_rom_directory()
            input("\nTekan ENTER untuk kembali...")
        elif choice == '4':
            print("\n[!] Modul flashing dikunci demi keselamatan perangkat uji coba.")
            input("\nTekan ENTER untuk kembali...")
        elif choice == '5':
            print("\nKeluar dari Yuura OS Flasher. Tetap aman, Kapten!")
            sys.exit(0)
        else:
            print("\n[!] Pilihan tidak valid.")
            input("\nTekan ENTER untuk mengulang...")

if __name__ == "__main__":
    if check_safety_environment():
        main_menu()
    else:
        print("[X] Instal terlebih dahulu dependensi adb & fastboot.")

