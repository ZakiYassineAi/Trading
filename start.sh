#!/usr/bin/env bash
# We remove 'set -e' to ensure we can capture logs even on failure.
set -uo pipefail

echo "[agent] Tick started at $(date -u +%FT%TZ)"
echo "[agent] Running the airdrop collection cycle with advanced logging..."

# Create a log file for this run
LOG_FILE="run_$(date +%s).log"
echo "--- Python Script Output ---" > $LOG_FILE

# Run the python script, redirecting all output (stdout and stderr) to the log file.
# The script's exit code will be captured.
python3 -u advanced_airdrop_automation.py &>> $LOG_FILE
EXIT_CODE=$?

# Print the entire log file to the GitHub Actions console
echo ""
echo "--- START OF SCRIPT LOG ---"
cat $LOG_FILE
echo "--- END OF SCRIPT LOG (Exit Code: $EXIT_CODE) ---"
echo ""

# Now, we check the exit code and exit the main script with it.
# This will make the GitHub Actions step succeed or fail correctly.
if [ $EXIT_CODE -ne 0 ]; then
  echo "[agent] Python script failed with exit code $EXIT_CODE."
  exit $EXIT_CODE
else
  echo "[agent] Tick finished successfully at $(date -u +%FT%TZ)"
fi
