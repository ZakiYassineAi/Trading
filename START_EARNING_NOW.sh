#!/bin/bash

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                              ║"
echo "║                    💰 START EARNING $1 IN 60 MINUTES 💰                     ║"
echo "║                                                                              ║"
echo "║            Wallet: 0x958BD67f2f6be2Dc46D0e9e0Dd6d33F52EfCA67C              ║"
echo "║                                                                              ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Create necessary directories
mkdir -p logs submissions airdrop_data ai_brain 2>/dev/null

echo "🚀 Starting all profit systems..."
echo ""

# Run aggressive profit engine first
echo "🔥 [1/5] Starting Aggressive Profit Engine..."
python3 aggressive_profit_engine.py &

# Run real money hunter
echo "🎯 [2/5] Starting Real Money Hunter..."
python3 real_money_hunter.py &

# Run instant profit system
echo "⚡ [3/5] Starting Instant Profit System..."
python3 instant_profit_system.py &

# Run pattern intelligence
echo "🧠 [4/5] Starting Pattern Intelligence..."
python3 pattern_intelligence_system.py &

# Run blockchain interface
echo "⛓️ [5/5] Starting Blockchain Interface..."
python3 blockchain_direct_interface.py &

echo ""
echo "✅ All systems started!"
echo ""
echo "📊 REAL OPPORTUNITIES FOUND:"
echo "   • BSC Testnet Faucet: https://testnet.binance.org/faucet-smart"
echo "   • Polygon Faucet: https://faucet.polygon.technology/"
echo "   • Layer3 Quests: https://layer3.xyz/quests"
echo "   • Galxe: https://galxe.com/"
echo "   • FaucetPay: https://faucetpay.io/"
echo ""
echo "💰 YOUR WALLET: 0x958BD67f2f6be2Dc46D0e9e0Dd6d33F52EfCA67C"
echo ""
echo "⏰ Timer started - 60 minutes to earn $1!"
echo ""
echo "Press Ctrl+C to stop"

# Keep running
wait