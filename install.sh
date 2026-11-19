#!/bin/sh

APP_DIR="$HOME/.yuuraos_runtime"
BOOT_FLAG="$HOME/.yuuraos_first_boot_done"
CORE_FILE="$APP_DIR/godmode_ui.py"

clear_screen() {
    clear 2>/dev/null || printf "\033c"
}

clean_welcome_and_cache() {
    if [ -f /etc/motd ]; then
        : > /etc/motd 2>/dev/null || true
    fi
    if [ -d /etc/update-motd.d ]; then
        chmod -x /etc/update-motd.d/* 2>/dev/null || true
    fi
    rm -rf "$APP_DIR/__pycache__" /tmp/yuura* 2>/dev/null || true
}

first_boot_animation() {
    clear_screen
    printf "\033[1;36m==================================================\033[0m\n"
    printf "\033[1;33m        Y U U R A   O S   //   F I R S T   B O O T\033[0m\n"
    printf "\033[1;36m==================================================\033[0m\n\n"
    sleep 0.8

    for step in \
        "Menyiapkan lingkungan inti Yuura OS..." \
        "Membersihkan pesan welcome bawaan..." \
        "Memuat modul telemetri & AI monitor..." \
        "Menghapus cache & log sisa..."
    do
        printf "\033[1;32m[+]\033[0m %s\n" "$step"
        sleep 0.9
    done

    printf "\n\033[1;35mBooting sistem pertama kali\033[0m"
    for _ in 1 2 3 4 5 6 7 8; do
        printf "."
        sleep 0.35
    done
    printf " \033[1;32m[SIAP]\033[0m\n"
    sleep 1.0
    touch "$BOOT_FLAG"
}

mkdir -p "$APP_DIR"
clean_welcome_and_cache

cat << 'PYEOF' > "$CORE_FILE"
import os
import platform
import shutil
import subprocess

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

BANNER = f"""{RED}  ____            _ {YELLOW} __  __           _      {RESET}
{RED} / ___|  ___   __| |{YELLOW}|  \\/  | ___   __| | ___ {RESET}
{GREEN}| |  _  / _ \\ / _` |{BLUE}| |\\/| |/ _ \\ / _` |/ _ \\{RESET}
{GREEN}| |_| || (_) | (_| |{BLUE}| |  | | (_) | (_| |  __/{RESET}
{MAGENTA} \\____| \\___/ \\__,_|{CYAN}|_|  |_|\\___/ \\__,_|\\___|{RESET}
{BOLD}{CYAN}          Yuura OS Official (Smart Telemetry & Auto-Update){RESET}
"""


def clear_ui():
    os.system("clear")


def get_cpu_info():
    cores = os.cpu_count() or 1
    arch = platform.machine() or "unknown"
    model = ""
    try:
        with open("/proc/cpuinfo", "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if line.lower().startswith(("model name", "hardware")):
                    val = line.split(":", 1)[1].strip()
                    if val:
                        model = val
                        break
    except Exception:
        pass
    if model:
        return f"{model} ({cores}C, {arch})"
    return f"{arch} ({cores} core)"


def show_telemetry():
    total, used, free = shutil.disk_usage("/")
    total_gb = total // (2**30)
    used_gb = used // (2**30)
    free_gb = free // (2**30)
    pct = (used / total) * 100 if total > 0 else 0

    ram_info = "N/A"
    try:
        out = subprocess.check_output("free -m | grep Mem", shell=True, text=True).strip()
        parts = out.split()
        if len(parts) >= 3:
            ram_info = f"{parts[2]} MB / {parts[1]} MB"
    except Exception:
        pass

    kernel_info = platform.release() or "N/A"
    print(f"{CYAN}[*]{RESET} CPU         : {get_cpu_info()}")
    print(f"{CYAN}[*]{RESET} Kernel      : {kernel_info}")
    print(f"{CYAN}[*]{RESET} Penyimpanan : {used_gb} GB / {total_gb} GB ({pct:.1f}% terpakai | Sisa {free_gb} GB)")
    print(f"{CYAN}[*]{RESET} Memori RAM  : {ram_info}")


def show_header():
    clear_ui()
    print(BANNER)
    show_telemetry()
    print(f"{GREEN}[+]{RESET} Yuura Autonomous AI Agent & Live Telemetry Active.")
    print(f"{BLUE}[i]{RESET} Sistem siap. Ketik 'update' untuk pembaruan atau perintah lainnya.\n")


def show_modules():
    print(f"{CYAN}[i]{RESET} Modul aktif Yuura OS:")
    print("  - godmode_ui.py (Live Monitor & Telemetry)")
    print("  - clean_welcome (Auto-Clean Banner)")


def run_loop():
    show_header()
    while True:
        try:
            raw = input(f"{BOLD}Yuura-AI (Live Monitor)>{RESET} ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{YELLOW}[+]{RESET} Keluar dari Yuura OS.")
            break

        if not raw:
            continue

        parts = raw.split()
        cmd = parts[0].lower()
        sub = parts[1].lower() if len(parts) > 1 else ""

        if cmd in ("exit", "quit", "keluar"):
            print(f"{YELLOW}[+]{RESET} Keluar ke shell.")
            break
        elif cmd == "clear":
            show_header()
        elif cmd == "update":
            print(f"{CYAN}[i]{RESET} Memeriksa status modul Yuura OS...")
            show_modules()
        elif cmd == "yuura":
            if sub == "list":
                show_modules()
            elif sub == "status":
                show_telemetry()
            else:
                print(f"{YELLOW}[i]{RESET} Perintah: yuura list | yuura status | update | clear | exit")
        else:
            subprocess.run(raw, shell=True)


if __name__ == "__main__":
    run_loop()
PYEOF

if [ ! -f "$BOOT_FLAG" ]; then
    first_boot_animation
fi

clean_welcome_and_cache
exec python3 -B "$CORE_FILE"
