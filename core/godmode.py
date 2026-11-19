import os
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


def clear_screen():
    os.system("clear")


def run_cmd(cmd):
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return res.stdout.strip() if res.returncode == 0 else ""
    except Exception:
        return ""


def show_telemetry():
    total, used, free = shutil.disk_usage("/")
    total_gb = total // (2**30)
    used_gb = used // (2**30)
    free_gb = free // (2**30)
    pct = (used / total) * 100 if total > 0 else 0

    mem_line = run_cmd("free -m | grep Mem")
    ram_info = "N/A"
    if mem_line:
        parts = mem_line.split()
        if len(parts) >= 3:
            ram_info = f"{parts[2]} MB / {parts[1]} MB"

    print(f"{CYAN}[*]{RESET} Penyimpanan : {used_gb} GB / {total_gb} GB ({pct:.1f}% terpakai | Sisa {free_gb} GB)")
    print(f"{CYAN}[*]{RESET} Memori RAM  : {ram_info}")


def show_ui():
    clear_screen()
    print(BANNER)
    show_telemetry()
    print(f"{GREEN}[+]{RESET} Yuura Autonomous AI Agent & Live Telemetry Active.")
    print(f"{BLUE}[i]{RESET} Sistem siap. Ketik 'update' untuk pembaruan atau perintah lainnya.\n")


def get_files():
    base = os.path.expanduser("~/yuura-os")
    results = []
    for root, _, files in os.walk(base):
        for name in sorted(files):
            rel = os.path.relpath(os.path.join(root, name), base)
            results.append(rel)
    return results


def handle_yuura_cmd(args):
    sub = args[0].lower() if args else "help"
    if sub == "list":
        for item in get_files():
            print(f"  - {item}")
    elif sub == "status":
        show_telemetry()
    else:
        print("  Perintah: yuura list | yuura status")


def main():
    show_ui()
    while True:
        try:
            cmd = input(f"{BOLD}Yuura-AI (Live Monitor)>{RESET} ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{YELLOW}[+]{RESET} Keluar dari GodMode.")
            break

        if not cmd:
            continue

        parts = cmd.split()
        low = parts[0].lower()

        if low in ("exit", "quit", "keluar"):
            print(f"{YELLOW}[+]{RESET} Kembali ke shell Ubuntu...")
            break
        elif low == "clear":
            show_ui()
        elif low == "update":
            print(f"{CYAN}[i]{RESET} Mengecek file inti Yuura OS...")
            for item in get_files():
                print(f"  - {item}")
        elif low == "yuura":
            handle_yuura_cmd(parts[1:])
        else:
            subprocess.run(cmd, shell=True)


if __name__ == "__main__":
    main()
