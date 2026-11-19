#!/bin/sh

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
INSTALL_DIR="$HOME/yuura-os"
BOOT_FLAG="$HOME/.yuura_os_booted"

clear_screen() {
    clear 2>/dev/null || printf "\033c"
}

step_log() {
    msg="$1"
    delay="${2:-0.45}"
    printf "[  OK  ] %s\n" "$msg"
    sleep "$delay"
}

run_one_time_boot() {
    clear_screen
    echo "=================================================="
    echo "        Y U U R A   O S   //   B O O T L O A D E R"
    echo "     Initializing Ubuntu Root Environment...     "
    echo "=================================================="
    sleep 0.6

    step_log "Preparing Yuura OS directory ($INSTALL_DIR)..." 0.45
    step_log "Cleaning default welcome banner..." 0.45
    step_log "Loading GodMode core interface..." 0.50
    step_log "Registering 'godmode' shortcut command..." 0.45

    echo "--------------------------------------------------"
    printf "Booting Yuura OS"
    for i in 1 2 3 4 5; do
        printf "."
        sleep 0.25
    done
    echo " [DONE]"
    sleep 0.5

    touch "$BOOT_FLAG"
}

mkdir -p "$INSTALL_DIR/core" "$INSTALL_DIR/modules"

if [ -f "$SCRIPT_DIR/core/godmode.py" ]; then
    cp "$SCRIPT_DIR/core/godmode.py" "$INSTALL_DIR/core/godmode.py"
fi

if [ -f "$SCRIPT_DIR/modules/clean_welcome.sh" ]; then
    cp "$SCRIPT_DIR/modules/clean_welcome.sh" "$INSTALL_DIR/modules/clean_welcome.sh"
    chmod +x "$INSTALL_DIR/modules/clean_welcome.sh"
fi

if [ ! -f "$BOOT_FLAG" ]; then
    run_one_time_boot
    if [ -f "$INSTALL_DIR/modules/clean_welcome.sh" ]; then
        sh "$INSTALL_DIR/modules/clean_welcome.sh" >/dev/null 2>&1 || true
    fi
else
    clear_screen
    echo "[i] Yuura OS sudah pernah di-booting sebelumnya. Melanjutkan..."
    sleep 0.3
fi

cat << INNER_EOF > /usr/local/bin/godmode
#!/bin/sh
python3 "$INSTALL_DIR/core/godmode.py" "\$@"
INNER_EOF
chmod +x /usr/local/bin/godmode

if [ -f "$INSTALL_DIR/core/godmode.py" ]; then
    exec python3 "$INSTALL_DIR/core/godmode.py"
else
    echo "[!] core/godmode.py tidak ditemukan di $INSTALL_DIR/core/godmode.py."
fi
