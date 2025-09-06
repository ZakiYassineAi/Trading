#!/usr/bin/env bash
set -euo pipefail

echo "[agent] Tick started at $(date -u +%FT%TZ)"

echo "[agent] Running the airdrop collection cycle..."
python3 -u advanced_airdrop_automation.py

echo "[agent] Tick finished successfully at $(date -u +%FT%TZ)"
