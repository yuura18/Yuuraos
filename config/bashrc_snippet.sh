# === YUURA SYSTEM PULSE AUTO-START ===
if [ -n "$PS1" ] && [ -f "$HOME/yuura_system_pulse.py" ]; then
    python3 "$HOME/yuura_system_pulse.py"
fi
