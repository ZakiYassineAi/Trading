#!/bin/bash

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                              ║"
echo "║        🚀 QUANTUM AIRDROP SYSTEM - ULTIMATE LAUNCHER                        ║"
echo "║                                                                              ║"
echo "║        The Most Advanced Airdrop Automation System Ever Created             ║"
echo "║                                                                              ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "🔍 Checking Python version..."
python3 --version

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p stealth_airdrop_data
mkdir -p logs
mkdir -p screenshots
mkdir -p wallets

# Install basic requirements if needed
echo "📦 Checking dependencies..."
pip3 install --quiet requests beautifulsoup4 aiohttp colorama 2>/dev/null

# Update configuration with target wallet
echo "💰 Configuring target wallet..."
echo "   Wallet: 0x958BD67f2f6be2Dc46D0e9e0Dd6d33F52EfCA67C"
echo "   Network: BSC (USDT BEP20)"

# Launch the quantum system
echo ""
echo "🚀 Launching Quantum System..."
echo "="*80

python3 quantum_launcher.py