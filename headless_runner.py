import asyncio
import os
import sys
from ultimate_stealth_airdrop_collector import SupremeAirdropOrchestrator, logger

async def headless_start():
    """
    Starts the collector in a non-interactive way, using the new
    headless initialization function.
    """
    # Suppress output during initialization to prevent background job from stopping
    _original_stdout = sys.stdout
    _original_stderr = sys.stderr
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')

    try:
        orchestrator = SupremeAirdropOrchestrator()
        # Use the new headless initialization function
        initialized = await orchestrator.initialize_headless_system()
    finally:
        # Restore stdout and stderr
        sys.stdout.close()
        sys.stderr.close()
        sys.stdout = _original_stdout
        sys.stderr = _original_stderr

    if initialized:
        logger.info("✅ Headless initialization successful. Starting continuous monitoring...")
        await orchestrator.run_continuous_monitoring(interval_hours=6)
    else:
        logger.error("❌ Headless initialization failed. Aborting.")

if __name__ == "__main__":
    try:
        asyncio.run(headless_start())
    except KeyboardInterrupt:
        logger.info("⏹️ Headless runner stopped by user.")
    except Exception as e:
        logger.error(f"💥 Headless runner failed: {e}")
