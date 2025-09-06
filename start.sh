#!/usr/bin/env bash
set -euo pipefail

echo "[agent] Tick started at $(date -u +%FT%TZ)"

echo "[agent] Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "[agent] Running the airdrop collection cycle..."
# Using -u for unbuffered output, which is good for logging in Actions
python3 -u advanced_airdrop_automation.py

echo "[agent] Tick finished successfully at $(date -u +%FT%TZ)"
