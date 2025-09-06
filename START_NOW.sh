#!/bin/bash

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                              ║"
echo "║     🚀 QUANTUM AIRDROP SYSTEM - STARTING 24/7 COLLECTION                    ║"
echo "║                                                                              ║"
echo "║     💰 YOUR WALLET: 0x958BD67f2f6be2Dc46D0e9e0Dd6d33F52EfCA67C             ║"
echo "║     🔗 NETWORK: BSC (USDT BEP20)                                           ║"
echo "║                                                                              ║"
echo "║     The system will now:                                                    ║"
echo "║     1. Collect airdrops from 10+ real sources                              ║"
echo "║     2. Submit your wallet to each airdrop                                  ║"
echo "║     3. Complete tasks automatically                                        ║"
echo "║     4. Run forever (24/7) without stopping                                 ║"
echo "║                                                                              ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Create required directories
echo "📁 Setting up directories..."
mkdir -p logs airdrop_data submissions

# Install basic requirements
echo "📦 Installing requirements..."
pip3 install requests beautifulsoup4 aiohttp colorama 2>/dev/null

echo ""
echo "🚀 STARTING PERPETUAL RUNNER..."
echo "="
echo ""

# Run the perpetual runner
python3 quantum_perpetual_runner.py