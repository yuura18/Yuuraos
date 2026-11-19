import os
import subprocess
import glob

def show_yuuralist():
    print("\n\033[1;33m[i] === DAFTAR MODUL & SKRIP TERSEDIA ===\033[0m")
    print("\033[1;32m[+] Skrip & Tools Python Lokal:\033[0m")
    
    # Mencari semua file .py atau skrip penting di direktori aktif
    scripts = glob.glob("*.py")
    for idx, scr in enumerate(scripts):
        print(f"    [{idx + 1}] {scr} (Ketik namanya langsung untuk jalankan)")
        
    print("\n\033[1;32m[+] Tools Sistem Terintegrasi:\033[0m")
    print("    - sqlmap (Jalankan injeksi database)")
    print("    - nmap   (Pemindai jaringan)")
    print("    - hydra  (Brute-force tool)")
    print("    - metasploit / msfconsole")
    print("="*45 + "\n")

def process_command(user_input):
    cmd_lower = user_input.strip().lower()
    
    if not cmd_lower:
        return
        
    # 1. Perintah untuk melihat list modul (yuuralist)
    if cmd_lower == "yuuralist" or cmd_lower == "yuura list":
        show_yuuralist()
        return
        
    # 2. Perintah pintas 'godmode' -> langsung jalankan python3 godmode.py
    if cmd_lower == "godmode":
        print("\n\033[1;32m[+] Memanggil GodMode Engine secara otonom...\033[0m")
        os.system("python3 godmode.py")
        return
        
    # 3. Perintah pintas untuk modul python lain (misal: yuura -> python3 yuura.py)
    if os.path.exists(f"{cmd_lower}.py"):
        print(f"\n\033[1;32m[+] Menjalankan skrip lokal: {cmd_lower}.py ...\033[0m")
        os.system(f"python3 {cmd_lower}.py")
        return
        
    # 4. Perintah untuk tools sistem (sqlmap, nmap, dll) tanpa ribet
    system_tools = ["sqlmap", "nmap", "hydra", "msfconsole", "netcat", "curl", "git"]
    if cmd_lower in system_tools or cmd_lower.startswith("sqlmap "):
        os.system(user_input)
        return
        
    # 5. Jika perintah bawaan Linux biasa (ls, clear, exit, dll)
    if cmd_lower in ["ls", "clear", "exit", "pwd", "whoami"]:
        os.system(user_input)
        return
        
    # Default: Coba eksekusi sebagai perintah sistem umum
    exit_code = os.system(user_input)
    if exit_code != 0:
        print(f"\n\033[1;31m[!] Perintah '{user_input}' tidak dikenali. Ketik 'yuuralist' untuk melihat daftar modul.\033[0m")

def main():
    print("\n\033[1;32m[+] Yuura-AI Smart Command Router Active!\033[0m")
    print("[i] Ketik 'yuuralist' untuk melihat modul, atau langsung ketik nama modulnya.\n")
    
    while True:
        try:
            user_input = input("\033[1;36mYuura-AI> \033[0m").strip()
            if user_input.lower() in ["exit", "quit"]:
                print("\n\033[1;32m[+] Sampai jumpa, Kapten!\033[0m")
                break
            process_command(user_input)
        except KeyboardInterrupt:
            print("\n")
            break

if __name__ == "__main__":
    main()
