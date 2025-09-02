#!/usr/bin/env python3
"""
🚀 ULTIMATE STEALTH AIRDROP COLLECTOR - QUICK LAUNCHER
═══════════════════════════════════════════════════════════════════════════════════════
Quick launcher script for the Ultimate Stealth Airdrop Collector
Run this script to start the collector with an interactive menu.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from ultimate_stealth_airdrop_collector import *
    
    async def interactive_launcher():
        """Interactive launcher with menu"""
        
        # Display banner
        command_center.display_welcome_banner()
        
        print(f"""
{Fore.GREEN}🎮 QUICK LAUNCHER - SELECT YOUR ACTION:
════════════════════════════════════════════════════════════════════════════════════════{Style.RESET_ALL}

{Fore.CYAN}1. 🚀 Run Single Collection Cycle{Style.RESET_ALL}
   Perfect for: One-time scan to discover current opportunities
   
{Fore.BLUE}2. 🔄 Start Continuous Monitoring{Style.RESET_ALL}
   Perfect for: Long-term automated operation (scans every 6 hours)
   
{Fore.YELLOW}3. 🔧 System Setup & Configuration{Style.RESET_ALL}
   Perfect for: First-time setup, configure API keys, test system
   
{Fore.MAGENTA}4. 📊 View System Status & Analytics{Style.RESET_ALL}
   Perfect for: Check system status, view collected data, analytics
   
{Fore.RED}5. 🎛️ Advanced Command Center{Style.RESET_ALL}
   Perfect for: Power users, advanced configuration, troubleshooting
   
{Fore.WHITE}0. ❌ Exit{Style.RESET_ALL}
        """)
        
        while True:
            try:
                choice = input(f"\n{Fore.GREEN}🎯 Select option (0-5): {Style.RESET_ALL}").strip()
                
                if choice == '1':
                    print(f"\n{Fore.CYAN}🚀 Starting Single Collection Cycle...{Style.RESET_ALL}")
                    await single_collection_cycle()
                    break
                    
                elif choice == '2':
                    print(f"\n{Fore.BLUE}🔄 Starting Continuous Monitoring...{Style.RESET_ALL}")
                    hours = input(f"⏰ Scan interval in hours (default: 6): ").strip()
                    interval = int(hours) if hours.isdigit() else 6
                    await run_continuous_monitoring(interval)
                    break
                    
                elif choice == '3':
                    print(f"\n{Fore.YELLOW}🔧 System Setup & Configuration{Style.RESET_ALL}")
                    await setup_and_configure()
                    break
                    
                elif choice == '4':
                    print(f"\n{Fore.MAGENTA}📊 System Status & Analytics{Style.RESET_ALL}")
                    show_status_and_analytics()
                    input("\nPress Enter to continue...")
                    continue
                    
                elif choice == '5':
                    print(f"\n{Fore.RED}🎛️ Advanced Command Center{Style.RESET_ALL}")
                    command_center.show_main_menu()
                    print(f"\n{Fore.GREEN}Advanced mode activated. Use Python console for advanced operations.{Style.RESET_ALL}")
                    break
                    
                elif choice == '0':
                    print(f"\n{Fore.WHITE}👋 Goodbye! Stay safe in the crypto world!{Style.RESET_ALL}")
                    break
                    
                else:
                    print(f"{Fore.RED}❌ Invalid choice. Please select 0-5.{Style.RESET_ALL}")
                    
            except KeyboardInterrupt:
                print(f"\n{Fore.WHITE}👋 Goodbye!{Style.RESET_ALL}")
                break
            except ValueError:
                print(f"{Fore.RED}❌ Please enter a valid number.{Style.RESET_ALL}")
    
    async def single_collection_cycle():
        """Run a single collection cycle"""
        try:
            print(f"""
{Fore.CYAN}🔥 SINGLE COLLECTION CYCLE STARTING...
════════════════════════════════════════════════════════════════════════════════════════

This will:
• Initialize the system if needed
• Scan 25+ intelligence sources
• Analyze content with advanced ML
• Generate comprehensive reports
• Send notifications (if configured)

Estimated time: 2-5 minutes depending on network speed{Style.RESET_ALL}
            """)
            
            input("Press Enter to continue or Ctrl+C to cancel...")
            
            # Run the collection
            results = await run_supreme_collection()
            
            if results and results.get('success'):
                new_count = results['collection_stats']['new_airdrops']
                total_found = results['collection_stats']['total_items_found']
                processing_time = results['collection_stats']['processing_time_seconds']
                
                print(f"""
{Fore.GREEN}✅ COLLECTION CYCLE COMPLETED SUCCESSFULLY!

📊 Results Summary:
├─ New Opportunities Found: {new_count}
├─ Total Items Analyzed: {total_found}
├─ Processing Time: {processing_time:.1f} seconds
└─ Reports Generated: {len(results.get('report_paths', {}))} files

📁 Check the 'stealth_airdrop_data/reports/' directory for detailed reports.{Style.RESET_ALL}
                """)
            else:
                print(f"{Fore.RED}❌ Collection cycle failed. Check the logs for details.{Style.RESET_ALL}")
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}⏹️ Collection cycle cancelled by user.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}💥 Error during collection: {e}{Style.RESET_ALL}")
    
    async def setup_and_configure():
        """Setup and configure the system"""
        print(f"""
{Fore.YELLOW}🔧 SYSTEM SETUP & CONFIGURATION
════════════════════════════════════════════════════════════════════════════════════════{Style.RESET_ALL}

{Fore.GREEN}Setup Options:{Style.RESET_ALL}
1. 🔐 Setup Quantum Security Vault (API Keys)
2. 🧪 Test System Components  
3. 🌐 Test Network Connectivity
4. 📊 Initialize Database
5. ↩️ Back to Main Menu
        """)
        
        while True:
            try:
                choice = input(f"\n{Fore.GREEN}Select setup option (1-5): {Style.RESET_ALL}").strip()
                
                if choice == '1':
                    print(f"\n{Fore.CYAN}🔐 Setting up Quantum Security Vault...{Style.RESET_ALL}")
                    success = setup_quantum_vault()
                    if success:
                        print(f"{Fore.GREEN}✅ Vault setup completed successfully!{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}❌ Vault setup failed.{Style.RESET_ALL}")
                        
                elif choice == '2':
                    print(f"\n{Fore.BLUE}🧪 Testing System Components...{Style.RESET_ALL}")
                    success = await initialize_system()
                    if success:
                        print(f"{Fore.GREEN}✅ System components test passed!{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}❌ System test failed.{Style.RESET_ALL}")
                        
                elif choice == '3':
                    print(f"\n{Fore.MAGENTA}🌐 Testing Network Connectivity...{Style.RESET_ALL}")
                    await test_network_connectivity()
                    
                elif choice == '4':
                    print(f"\n{Fore.GREEN}📊 Initializing Database...{Style.RESET_ALL}")
                    command_center.orchestrator.database.init_database()
                    print(f"{Fore.GREEN}✅ Database initialized successfully!{Style.RESET_ALL}")
                    
                elif choice == '5':
                    break
                    
                else:
                    print(f"{Fore.RED}❌ Invalid choice. Please select 1-5.{Style.RESET_ALL}")
                    
                input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"{Fore.RED}💥 Setup error: {e}{Style.RESET_ALL}")
    
    def show_status_and_analytics():
        """Show system status and analytics"""
        try:
            print(f"\n{Fore.CYAN}📊 SYSTEM STATUS & ANALYTICS{Style.RESET_ALL}")
            print("=" * 80)
            
            # System Status
            show_system_status()
            
            print(f"\n{Fore.BLUE}─" * 80 + f"{Style.RESET_ALL}")
            
            # Analytics Dashboard  
            show_analytics_dashboard()
            
        except Exception as e:
            print(f"{Fore.RED}💥 Error displaying status: {e}{Style.RESET_ALL}")
    
    if __name__ == "__main__":
        try:
            print(f"""
{Fore.GREEN}🔥 ULTIMATE STEALTH AIRDROP COLLECTOR - QUICK LAUNCHER
════════════════════════════════════════════════════════════════════════════════════════

Welcome to the most advanced airdrop intelligence system ever created!

⚡ Features:
• Military-grade stealth scraping from 25+ sources
• Advanced ML analysis with local processing  
• Quantum-level security and encryption
• Multi-channel notifications (Telegram, Discord, GitHub)
• Real-time analytics and comprehensive reporting
• Automated continuous monitoring

🎯 Target Wallet: {CONFIG.WALLET_ADDRESS}
🛡️ Security: All participation requires manual verification{Style.RESET_ALL}
            """)
            
            asyncio.run(interactive_launcher())
            
        except KeyboardInterrupt:
            print(f"\n{Fore.WHITE}👋 Launcher interrupted. Goodbye!{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}💥 Launcher error: {e}{Style.RESET_ALL}")
        
except ImportError as e:
    print(f"""
❌ IMPORT ERROR: {e}

📋 TROUBLESHOOTING:
1. Make sure you're in the correct directory
2. Run: pip install -r requirements.txt (if available)
3. Check that ultimate_stealth_airdrop_collector.py exists

🔧 If issues persist, run the package installer manually:
   python -c "from ultimate_stealth_airdrop_collector import IntelligentPackageManager; IntelligentPackageManager.smart_install()"
    """)
except Exception as e:
    print(f"💥 UNEXPECTED ERROR: {e}")