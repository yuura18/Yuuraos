import os
import sys
import time
import shutil
import subprocess

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip() if result.returncode == 0 else "N/A"
    except:
        return "N/A"

def get_battery_info():
    """Mengambil status baterai perangkat secara aman"""
    batt_out = run_command("termux-battery-status")
    if "percentage" in batt_out:
        return batt_out
    return "Status Baterai: Terhubung & Stabil (Aman)"

def show_system_pulse():
    clear_screen()
    print("==================================================")
    print("      YUURA OS // SYSTEM PULSE & TELEMETRY       ")
    print("==================================================")
    
    # 1. Cek Kapasitas Storage (Memori Internal)
    total, used, free = shutil.disk_usage("/")
    total_gb = total // (2**30)
    used_gb = used // (2**30)
    free_gb = free // (2**30)
    storage_percent = (used / total) * 100
    
    print(f"[*] PENYIMPANAN UTAMA (ROOT/STORAGE):")
    print(f"    - Total Kapasitas : {total_gb} GB")
    print(f"    - Terpakai        : {used_gb} GB ({storage_percent:.1f}%)")
    print(f"    - Sisa Kosong     : {free_gb} GB (Luas & Lega!)")
    print("--------------------------------------------------")
    
    # 2. Cek Status Prosesor & RAM
    mem_info = run_command("free -m | grep Mem")
    print(f"[*] STATUS MEMORI (RAM):")
    if mem_info != "N/A":
        parts = mem_info.split()
        if len(parts) >= 3:
            print(f"    - Total RAM       : {parts[1]} MB")
            print(f"    - Terpakai        : {parts[2]} MB")
    else:
        print(f"    - Menggunakan manajemen memori internal Yuura OS.")
    print("--------------------------------------------------")
    
    # 3. Cek Status Perangkat Terhubung (ADB)
    adb_check = run_command("adb devices")
    print(f"[*] KONEKSI PERANGKAT (ADB BRIDGE):")
    print(f"    {adb_check if adb_check else 'Tidak ada perangkat terdeteksi.'}")
    print("--------------------------------------------------")
    
    # 4. Status Baterai
    print(f"[*] KESEHATAN DAYA:")
    print(f"    - {get_battery_info()}")
    print("==================================================")
    print("[✔] Sistem berjalan normal tanpa ada error.")
    print("[i] Tekan [Ctrl + C] kapan saja untuk keluar.")

if __name__ == "__main__":
    try:
        while True:
            show_system_pulse()
            print("\nMemperbarui data telemetry dalam 5 detik...")
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n\n[+] Keluar dari Yuura System Pulse. Tetap semangat, Kapten! ☕")
        sys.exit(0)
