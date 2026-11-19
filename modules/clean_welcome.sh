#!/bin/sh

if [ -f /etc/motd ]; then
    : > /etc/motd
fi

if [ -d /etc/update-motd.d ]; then
    chmod -x /etc/update-motd.d/* 2>/dev/null || true
fi

touch "$HOME/.yuura_welcome_cleaned"
echo "[OK] Tulisan welcome bawaan Ubuntu root sudah dibersihkan."
