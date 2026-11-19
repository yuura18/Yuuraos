import sys
import time
import os
import glob
import threading

def show_boot_screen():
    print("\033[H\033[J", end="")
    print("\033[1;31m  ____           _  __  __           _      \033[0m")
    print("\033[1;33m / ___| ___   __| | |  \/  | ___   __| | ___ \033[0m")
    print("\033[1;32m| |  _ / _ \ / _` | | |\/| |/ _ \ / _` |/ _ \033[0m")
    print("\033[1;36m| |_| | (_) | (_| | | |  | | (_) | (_| |  __/\033[0m")
    print("\033[1;35m \____|\___/ \__,_| |_|  |_|\___/ \__,_|\___/\033[0m")
    print("\033[1;32m       Yuura OS Official (Smart Telemetry & Auto-Update)\033[0m\n")

def show_yuuralist():
    print("\n\033[1;33m[i] === DAFTAR MODUL & SKRIP TERSEDIA ===\033[0m")
    print("\033[1;32m[+] Skrip Python Lokal:\033[0m")
    scripts = glob.glob("*.py")
    for idx, scr in enumerate(scripts):
        print(f"    [{idx + 1}] {scr}")
    print("\n\033[1;32m[+] Tools Sistem Terintegrasi Ubuntu:\033[0m")
    print("    - sqlmap, nmap, hydra, metasploit, dll.")
    print("="*47 + "\n")

def process_command(user_input):
    cmd_raw = user_input.strip()
    cmd_lower = cmd_raw.lower()
    if not cmd_lower:
        return True
        
    if cmd_lower in ["exit", "quit"]:
        print("\n\033[1;32m[+] Sampai jumpa, Kapten!\033[0m")
        return False
        
    if cmd_lower in ["yuuralist", "yuura list", "list"]:
        show_yuuralist()
        return True
        
    if cmd_lower == "godmode":
        if os.path.exists("godmode.py"):
            print("\n\033[1;36m[Yuura Monitor]: Meluncurkan modul GodMode...\033[0m")
            os.system("python3 godmode.py")
        else:
            print("\033[1;31m[!] File godmode.py tidak ditemukan!\033[0m")
        return True

    # Smart Update Handler
    if cmd_lower == "update":
        print("\n\033[1;32m[Yuura AI Update Engine]: Memeriksa pembaruan sistem Ubuntu & tools...\033[0m")
        # Mengecek apakah sqlmap ada, jika ya tawarkan/lakukan update, atau update paket sistem
        if os.path.exists("/usr/bin/sqlmap") or os.system("which sqlmap > /dev/null 2>&1") == 0:
            print("[~] Menjalankan pembaruan sqlmap (--update)...")
            os.system("sqlmap --update")
        print("[~] Memperbarui daftar paket sistem Ubuntu...")
        os.system("apt-get update")
        return True

    if cmd_lower.startswith("install "):
        tool_name = cmd_raw.split(" ", 1)[1].strip()
        print(f"\n\033[1;32m[Yuura AI Telemetry]: Memulai instalasi untuk '{tool_name}'...\033[0m")
        os.system(f"apt-get update && apt-get install -y {tool_name}")
        return True

    if os.path.exists(f"{cmd_lower}.py"):
        print(f"\n\033[1;35m[Yuura Monitor]: Mengeksekusi modul '{cmd_lower}.py'...\033[0m")
        os.system(f"python3 {cmd_lower}.py")
        return True

    # Menampilkan indikator monitor proses aktif
    print(f"\n\033[1;34m[Yuura Monitor Active]: Mengeksekusi -> {cmd_raw}\033[0m")
    exit_code = os.system(cmd_raw)
    return True

def ai_assistant():
    show_boot_screen()
    print("\033[1;32m[+] Yuura Autonomous AI Agent & Live Telemetry Active.\033[0m")
    print("[i] Sistem siap. Ketik 'update' untuk pembaruan atau perintah lainnya.\n")
    
    while True:
        try:
            user_input = input("\033[1;36mYuura-AI (Live Monitor)> \033[0m")
            running = process_command(user_input)
            if not running:
                break
        except Exception as e:
            print("\n\033[1;31m[!] Yuura AI mendeteksi anomali / error sistem:\033[0m")
            print(f"\033[1;33m    -> {str(e)}\033[0m")
            print("\033[1;32m[~] AI memproses pemulihan mandiri & merestart sistem...\033[0m")
            time.sleep(2)
            os.execv(sys.executable, ['python3'] + sys.argv)
        except KeyboardInterrupt:
            print("\n\n\033[1;32m[+] Keluar dari sesi. Sampai jumpa, Kapten!\033[0m")
            break

if __name__ == "__main__":
    ai_assistant()
