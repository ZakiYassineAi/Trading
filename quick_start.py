#!/usr/bin/env python3
"""
🚀 ULTIMATE STEALTH AIRDROP COLLECTOR - QUICK START
═══════════════════════════════════════════════════════════════════════════════════════
One-click launcher for immediate airdrop intelligence collection
"""

import asyncio
import sys
import os
from datetime import datetime

def display_banner():
    print("""
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                    🚀 ULTIMATE STEALTH AIRDROP COLLECTOR                             ║
║                           QUICK START LAUNCHER v3.0.0                               ║
╠══════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                      ║
║  ⚡ REVOLUTIONARY FEATURES:                                                          ║
║  • 🥷 Military-Grade Stealth Scraping        • 🧠 Advanced Local ML Intelligence    ║
║  • 🔐 Quantum-Level Security                 • 📊 25+ Premium Sources               ║
║  • 🛡️ Anti-Detection Technology              • 📱 Multi-Channel Notifications       ║
║  • 🎯 ML Risk Assessment                     • 💾 Bulletproof Database             ║
║                                                                                      ║
║  🎯 Target Wallet: 0x958BD67f2f6be2Dc46D0e9e0Dd6d33F52EfCA67C                       ║
║  🛡️ Security: All participation requires manual verification                        ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
    """)

async def quick_collection():
    """Run a quick collection cycle"""
    
    print("🔥 INITIATING QUICK INTELLIGENCE COLLECTION...")
    print("=" * 80)
    
    try:
        # Import the system
        from ultimate_stealth_airdrop_collector import (
            initialize_system, run_supreme_collection, 
            show_system_status, CONFIG
        )
        
        print("📦 System components loaded successfully")
        
        # Initialize if needed
        print("🔧 Initializing system components...")
        init_success = await initialize_system()
        
        if init_success:
            print("✅ System initialized successfully")
        else:
            print("⚠️ System initialization had issues, but continuing...")
        
        print("\n🚀 Starting Supreme Intelligence Collection...")
        print("=" * 80)
        
        # Run collection
        results = await run_supreme_collection()
        
        if results and results.get('success'):
            stats = results['collection_stats']
            
            print(f"""
🎉 COLLECTION COMPLETED SUCCESSFULLY!
════════════════════════════════════════════════════════════════════════════════════════

📊 RESULTS SUMMARY:
├─ 🎯 New Opportunities: {stats['new_airdrops']}
├─ ⚡ Sources Scanned: {stats['total_sources']}
├─ 🔍 Items Analyzed: {stats['total_items_found']}
├─ 🔄 Duplicates Filtered: {stats['duplicates_filtered']}
├─ ⏱️ Processing Time: {stats['processing_time_seconds']:.1f}s
└─ 📈 Success Rate: {stats['success_rate']:.1f}%

💰 Target Wallet: {CONFIG.WALLET_ADDRESS}

📁 GENERATED REPORTS:
   • HTML Report: stealth_airdrop_data/reports/ (Beautiful visual report)
   • JSON Data: stealth_airdrop_data/reports/ (Complete raw data)  
   • CSV Export: stealth_airdrop_data/reports/ (Spreadsheet format)
   • Text Summary: stealth_airdrop_data/reports/ (Quick overview)

🎯 Next Steps:
   1. 📋 Review the HTML report for detailed analysis
   2. 🔍 Research each opportunity thoroughly
   3. ✅ Verify legitimacy through official channels
   4. 🔐 Use dedicated airdrop wallet for safety
   5. 🚫 Never share private keys or seed phrases

🔄 For continuous monitoring: python run_collector.py
            """)
            
            # Show top opportunities if found
            if stats['new_airdrops'] > 0:
                print("🏆 TOP OPPORTUNITIES DISCOVERED:")
                print("-" * 80)
                
                new_airdrops = results.get('new_airdrops', [])
                for i, airdrop in enumerate(new_airdrops[:3], 1):
                    title = airdrop.get('title', 'Unknown')[:60]
                    category = airdrop.get('category', 'Other')
                    priority = airdrop.get('priority_score', 0)
                    legitimacy = airdrop.get('legitimacy_score', 0)
                    risk = airdrop.get('risk_level', 'Unknown')
                    
                    print(f"{i}. {title}")
                    print(f"   📂 Category: {category} | 🎯 Priority: {priority}/5")
                    print(f"   ✅ Legitimacy: {legitimacy}/100 | ⚠️ Risk: {risk}")
                    print(f"   🔗 Source: {airdrop.get('source', 'Unknown')}")
                    print()
                
                if len(new_airdrops) > 3:
                    remaining = len(new_airdrops) - 3
                    print(f"   ... and {remaining} more opportunities in the detailed reports!")
            
        else:
            error = results.get('error') if results else "Unknown error"
            print(f"""
❌ COLLECTION FAILED
════════════════════════════════════════════════════════════════════════════════════════

Error: {error}

🔧 TROUBLESHOOTING STEPS:
1. Check your internet connection
2. Verify system permissions  
3. Try running: python run_collector.py (interactive mode)
4. Check logs in: stealth_airdrop_data/stealth_collector.log

💡 The system may work in interactive mode even if quick start fails.
            """)
            
    except ImportError as e:
        print(f"""
❌ IMPORT ERROR: {e}

🔧 SOLUTION:
1. Install dependencies: pip install -r requirements.txt
2. Or run: python run_collector.py (includes auto-installation)
3. Check Python version (requires 3.8+)
        """)
        
    except Exception as e:
        print(f"""
💥 UNEXPECTED ERROR: {e}

🔧 TROUBLESHOOTING:
1. Try interactive mode: python run_collector.py
2. Check system requirements
3. Verify file permissions
4. Review error logs

💡 Contact support if the issue persists.
        """)

def main():
    """Main entry point"""
    try:
        display_banner()
        
        print(f"🕒 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("⚡ Launching quick intelligence collection...")
        print()
        
        # Run async collection
        asyncio.run(quick_collection())
        
        print(f"""
🎊 QUICK START COMPLETED!

🎮 Want more control? Try:
   • python run_collector.py (Interactive launcher)
   • python -c "from ultimate_stealth_airdrop_collector import *; help(run_supreme_collection)"

🔄 For automated monitoring:
   • python -c "import asyncio; from ultimate_stealth_airdrop_collector import *; asyncio.run(run_continuous_monitoring())"

⚠️  SECURITY REMINDER:
   All participation is MANUAL ONLY - always verify everything!
   Never share private keys or send crypto to unknown addresses!

🎯 Happy hunting! Stay safe in the crypto world! 🛡️
        """)
        
    except KeyboardInterrupt:
        print("\n⏹️ Quick start cancelled by user. Goodbye!")
    except Exception as e:
        print(f"\n💥 Quick start error: {e}")

if __name__ == "__main__":
    main()