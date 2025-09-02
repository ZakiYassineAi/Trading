# ═══════════════════════════════════════════════════════════════════════════════════════
# 🎛️ SUPREME ORCHESTRATOR - THE MASTER BRAIN
# ═══════════════════════════════════════════════════════════════════════════════════════

class SupremeAirdropOrchestrator:
    """The master orchestrator that coordinates all systems"""
    
    def __init__(self):
        self.vault = QuantumVault()
        self.scraper = SupremeStealthScraper()
        self.extractor = SupremeContentExtractor(self.scraper)
        self.ml_engine = AdvancedMLIntelligence()
        self.database = QuantumIntelligenceDatabase()
        self.notification_system = SupremeNotificationSystem()
        
        self.performance_monitor = {
            'start_time': None,
            'end_time': None,
            'total_processing_time': 0,
            'stage_timings': {},
            'memory_usage': {},
            'errors': []
        }
        
        self.is_initialized = False
    
    async def initialize_supreme_system(self) -> bool:
        """Initialize the complete supreme system"""
        logger.banner("SUPREME AIRDROP ORCHESTRATOR", f"Version {CONFIG.VERSION} - Initializing...")
        
        start_time = time.time()
        
        try:
            # Step 1: Vault Setup and Security
            logger.info("🔐 Initializing Quantum Security Vault...")
            await self._initialize_vault()
            
            # Step 2: Database Initialization
            logger.info("💾 Initializing Quantum Intelligence Database...")
            self.database.cleanup_old_entries(90)  # Cleanup old entries
            
            # Step 3: ML Engine Warmup
            logger.info("🧠 Warming up ML Intelligence Engine...")
            await self._warmup_ml_engine()
            
            # Step 4: Network Systems Check
            logger.info("🌐 Verifying Network Systems...")
            await self._verify_network_systems()
            
            # Step 5: Notification System Setup
            logger.info("📱 Configuring Notification Systems...")
            await self._setup_notifications()
            
            initialization_time = time.time() - start_time
            logger.success(f"✅ Supreme system initialized in {initialization_time:.2f}s")
            
            self.is_initialized = True
            return True
            
        except Exception as e:
            logger.error(f"💥 Supreme system initialization failed: {e}")
            return False
    
    async def _initialize_vault(self):
        """Initialize security vault"""
        vault_data = self.vault.load_vault()
        
        if not vault_data:
            logger.info("🔐 No quantum vault detected. Setting up new vault...")
            if not self.vault.interactive_setup():
                logger.warning("⚠️ Continuing without vault - limited functionality")
                return
        
        # Load secrets
        secrets = self.vault.load_secrets()
        if secrets:
            logger.success(f"🔑 Loaded {len(secrets)} secrets from quantum vault")
        else:
            logger.info("🔧 Operating in offline mode - basic functionality only")
    
    async def _warmup_ml_engine(self):
        """Warm up ML engine with test data"""
        test_airdrop = {
            'title': 'Test DeFi Token Airdrop Launch',
            'description': 'Revolutionary DeFi protocol launching mainnet with token distribution for early testnet users.',
            'source': 'test_source',
            'url': 'https://example.com'
        }
        
        # Run test analysis to warm up models
        _ = self.ml_engine.analyze_airdrop_intelligence(test_airdrop)
        logger.success("🧠 ML Intelligence Engine warmed up successfully")
    
    async def _verify_network_systems(self):
        """Verify network connectivity and systems"""
        test_urls = [
            'https://www.coingecko.com',
            'https://dappradar.com',
            'https://api.github.com'
        ]
        
        successful_tests = 0
        
        for url in test_urls:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, timeout=10) as response:
                        if response.status == 200:
                            successful_tests += 1
            except:
                pass
        
        connectivity_rate = (successful_tests / len(test_urls)) * 100
        
        if connectivity_rate >= 70:
            logger.success(f"🌐 Network connectivity verified ({connectivity_rate:.0f}%)")
        else:
            logger.warning(f"⚠️ Limited network connectivity ({connectivity_rate:.0f}%)")
    
    async def _setup_notifications(self):
        """Setup and verify notification channels"""
        channels = []
        
        if os.environ.get('TELEGRAM_BOT_TOKEN') and os.environ.get('TELEGRAM_CHAT_ID'):
            channels.append('Telegram')
        
        if os.environ.get('DISCORD_WEBHOOK'):
            channels.append('Discord')
        
        if os.environ.get('GITHUB_TOKEN'):
            channels.append('GitHub')
        
        if channels:
            logger.success(f"📱 Notification channels configured: {', '.join(channels)}")
        else:
            logger.info("📱 No notification channels configured - reports will be local only")
    
    async def run_supreme_collection_cycle(self) -> Dict[str, Any]:
        """Run complete supreme collection cycle with advanced monitoring"""
        if not self.is_initialized:
            logger.error("❌ System not initialized! Run initialize_supreme_system() first")
            return {'success': False, 'error': 'System not initialized'}
        
        logger.banner("SUPREME COLLECTION CYCLE", "Advanced Intelligence Gathering in Progress...")
        
        self.performance_monitor['start_time'] = time.time()
        
        # Initialize collection statistics
        collection_stats = {
            'cycle_id': secrets.token_hex(8),
            'start_time': datetime.now(timezone.utc).isoformat(),
            'total_sources': len(SUPREME_AIRDROP_SOURCES),
            'successful_sources': 0,
            'failed_sources': 0,
            'total_items_found': 0,
            'new_airdrops': 0,
            'duplicates_filtered': 0,
            'processing_time_seconds': 0,
            'success_rate': 0,
            'ml_performance': {},
            'extraction_performance': {},
            'top_sources': {},
            'errors': []
        }
        
        try:
            # Stage 1: Intelligence Extraction
            logger.info("🔍 Stage 1: Supreme Intelligence Extraction")
            stage_start = time.time()
            
            all_extracted_items = await self.extractor.extract_from_all_sources(SUPREME_AIRDROP_SOURCES)
            
            collection_stats['total_items_found'] = len(all_extracted_items)
            collection_stats['extraction_performance'] = self.extractor.get_extraction_stats()
            self.performance_monitor['stage_timings']['extraction'] = time.time() - stage_start
            
            logger.success(f"📦 Extracted {len(all_extracted_items)} items from {len(SUPREME_AIRDROP_SOURCES)} sources")
            
            # Stage 2: ML Intelligence Analysis
            logger.info("🧠 Stage 2: Advanced ML Intelligence Analysis")
            stage_start = time.time()
            
            analyzed_airdrops = []
            ml_processing_times = []
            
            # Process in batches for better performance
            batch_size = CONFIG.BATCH_SIZE
            
            for i in range(0, len(all_extracted_items), batch_size):
                batch = all_extracted_items[i:i + batch_size]
                
                logger.info(f"🔬 Analyzing batch {i//batch_size + 1}/{(len(all_extracted_items)-1)//batch_size + 1}")
                
                for item in tqdm(batch, desc="ML Analysis", leave=False):
                    try:
                        analysis_start = time.time()
                        
                        # Run comprehensive ML analysis
                        ml_analysis = self.ml_engine.analyze_airdrop_intelligence(item)
                        
                        # Record processing time
                        processing_time = time.time() - analysis_start
                        ml_processing_times.append(processing_time)
                        
                        # Combine item with analysis
                        analyzed_item = {**item, **ml_analysis}
                        analyzed_airdrops.append(analyzed_item)
                        
                    except Exception as e:
                        logger.debug(f"⚠️ ML analysis failed for item: {e}")
                        collection_stats['errors'].append(f"ML analysis error: {str(e)}")
                        continue
            
            # Calculate ML performance metrics
            if ml_processing_times:
                collection_stats['ml_performance'] = {
                    'total_analyzed': len(analyzed_airdrops),
                    'avg_processing_time': sum(ml_processing_times) / len(ml_processing_times),
                    'min_processing_time': min(ml_processing_times),
                    'max_processing_time': max(ml_processing_times),
                    'high_confidence_count': len([a for a in analyzed_airdrops if a.get('confidence_level', 0) > 0.8]),
                    'medium_confidence_count': len([a for a in analyzed_airdrops if 0.5 <= a.get('confidence_level', 0) <= 0.8]),
                    'low_confidence_count': len([a for a in analyzed_airdrops if a.get('confidence_level', 0) < 0.5])
                }
            
            self.performance_monitor['stage_timings']['ml_analysis'] = time.time() - stage_start
            
            logger.success(f"🧠 ML analysis completed: {len(analyzed_airdrops)} items analyzed")
            
            # Stage 3: Database Intelligence Storage
            logger.info("💾 Stage 3: Quantum Database Storage")
            stage_start = time.time()
            
            new_airdrops = []
            duplicate_count = 0
            
            for analyzed_item in analyzed_airdrops:
                success, message = self.database.save_airdrop_intelligence(analyzed_item, analyzed_item)
                
                if success:
                    new_airdrops.append(analyzed_item)
                    collection_stats['new_airdrops'] += 1
                else:
                    if 'duplicate' in message.lower():
                        duplicate_count += 1
                    else:
                        collection_stats['errors'].append(f"Database save error: {message}")
            
            collection_stats['duplicates_filtered'] = duplicate_count
            self.performance_monitor['stage_timings']['database_storage'] = time.time() - stage_start
            
            logger.success(f"💾 Database storage: {len(new_airdrops)} new items, {duplicate_count} duplicates filtered")
            
            # Stage 4: Performance Analytics
            logger.info("📊 Stage 4: Performance Analytics Generation")
            stage_start = time.time()
            
            # Calculate success rate and other metrics
            collection_stats['success_rate'] = (collection_stats['successful_sources'] / collection_stats['total_sources'] * 100) if collection_stats['total_sources'] > 0 else 0
            collection_stats['processing_time_seconds'] = time.time() - self.performance_monitor['start_time']
            
            # Generate source performance analysis
            collection_stats['top_sources'] = self._analyze_source_performance(all_extracted_items)
            
            # Record collection run in database
            self.database.record_collection_run(collection_stats)
            
            self.performance_monitor['stage_timings']['analytics'] = time.time() - stage_start
            
            # Stage 5: Notification Distribution
            logger.info("📱 Stage 5: Supreme Notification Distribution")
            stage_start = time.time()
            
            notification_results = await self.notification_system.send_comprehensive_notifications(
                new_airdrops, collection_stats
            )
            
            self.performance_monitor['stage_timings']['notifications'] = time.time() - stage_start
            
            # Stage 6: Report Generation
            logger.info("📋 Stage 6: Comprehensive Report Generation")
            stage_start = time.time()
            
            report_paths = await self._generate_comprehensive_reports(new_airdrops, collection_stats)
            
            self.performance_monitor['stage_timings']['report_generation'] = time.time() - stage_start
            
            # Finalize performance monitoring
            self.performance_monitor['end_time'] = time.time()
            self.performance_monitor['total_processing_time'] = (
                self.performance_monitor['end_time'] - self.performance_monitor['start_time']
            )
            
            # Display final results
            self._display_supreme_results(collection_stats, new_airdrops, notification_results, report_paths)
            
            return {
                'success': True,
                'collection_stats': collection_stats,
                'new_airdrops': new_airdrops,
                'all_analyzed_items': analyzed_airdrops,
                'notification_results': notification_results,
                'report_paths': report_paths,
                'performance_monitor': self.performance_monitor
            }
            
        except Exception as e:
            logger.error(f"💥 Supreme collection cycle failed: {e}")
            collection_stats['errors'].append(f"Critical error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'collection_stats': collection_stats,
                'performance_monitor': self.performance_monitor
            }
    
    def _analyze_source_performance(self, extracted_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze source performance and reliability"""
        source_stats = {}
        
        for item in extracted_items:
            source = item.get('source', 'Unknown')
            
            if source not in source_stats:
                source_stats[source] = {
                    'items': 0,
                    'total_reliability': 0,
                    'avg_reliability': 0,
                    'extraction_methods': set()
                }
            
            source_stats[source]['items'] += 1
            source_stats[source]['total_reliability'] += item.get('reliability', 0.5)
            source_stats[source]['extraction_methods'].add(item.get('extraction_method', 'unknown'))
        
        # Calculate averages and convert sets to lists
        for source, stats in source_stats.items():
            stats['avg_reliability'] = stats['total_reliability'] / stats['items'] if stats['items'] > 0 else 0
            stats['extraction_methods'] = list(stats['extraction_methods'])
        
        # Return top 10 sources by item count
        return dict(sorted(source_stats.items(), key=lambda x: x[1]['items'], reverse=True)[:10])
    
    async def _generate_comprehensive_reports(self, airdrops: List[Dict[str, Any]], 
                                            stats: Dict[str, Any]) -> Dict[str, str]:
        """Generate comprehensive reports in multiple formats"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_paths = {}
        
        try:
            # JSON Report (Detailed)
            json_report = {
                'metadata': {
                    'version': CONFIG.VERSION,
                    'timestamp': datetime.now(timezone.utc).isoformat(),
                    'cycle_id': stats.get('cycle_id'),
                    'collector': 'Supreme Airdrop Collector',
                    'target_wallet': CONFIG.WALLET_ADDRESS
                },
                'collection_statistics': stats,
                'performance_metrics': self.performance_monitor,
                'new_airdrops': airdrops,
                'system_info': {
                    'total_airdrops_in_db': len(self.database.get_top_airdrops(1000)),
                    'database_analytics': self.database.get_analytics_dashboard(),
                    'scraper_performance': self.scraper.get_stats(),
                    'extraction_performance': self.extractor.get_extraction_stats(),
                    'notification_stats': self.notification_system.get_notification_stats()
                }
            }
            
            json_path = os.path.join(CONFIG.REPORTS_DIR, f"supreme_report_{timestamp}.json")
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(json_report, f, ensure_ascii=False, indent=2)
            
            report_paths['json'] = json_path
            
            # CSV Report (Tabular)
            if airdrops:
                csv_data = []
                for airdrop in airdrops:
                    csv_data.append({
                        'timestamp': airdrop.get('extracted_at'),
                        'title': airdrop.get('title'),
                        'category': airdrop.get('category'),
                        'source': airdrop.get('source'),
                        'priority_score': airdrop.get('priority_score'),
                        'legitimacy_score': airdrop.get('legitimacy_score'),
                        'risk_level': airdrop.get('risk_level'),
                        'value_category': airdrop.get('value_category'),
                        'estimated_value_range': airdrop.get('estimated_value_range'),
                        'confidence_level': airdrop.get('confidence_level'),
                        'recommendation': airdrop.get('recommendation'),
                        'url': airdrop.get('url'),
                        'key_insights': '; '.join(airdrop.get('key_insights', [])),
                        'red_flags': '; '.join(airdrop.get('red_flags', [])),
                        'green_flags': '; '.join(airdrop.get('green_flags', []))
                    })
                
                df = pd.DataFrame(csv_data)
                csv_path = os.path.join(CONFIG.REPORTS_DIR, f"supreme_report_{timestamp}.csv")
                df.to_csv(csv_path, index=False, encoding='utf-8')
                report_paths['csv'] = csv_path
            
            # HTML Report (Visual)
            html_report = self._generate_html_report(airdrops, stats, timestamp)
            html_path = os.path.join(CONFIG.REPORTS_DIR, f"supreme_report_{timestamp}.html")
            
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_report)
            
            report_paths['html'] = html_path
            
            # Summary Report (Text)
            summary_report = self._generate_summary_report(airdrops, stats)
            summary_path = os.path.join(CONFIG.REPORTS_DIR, f"summary_{timestamp}.txt")
            
            with open(summary_path, 'w', encoding='utf-8') as f:
                f.write(summary_report)
            
            report_paths['summary'] = summary_path
            
            logger.success(f"📋 Reports generated: {len(report_paths)} formats")
            
        except Exception as e:
            logger.error(f"💥 Report generation failed: {e}")
        
        return report_paths
    
    def _generate_html_report(self, airdrops: List[Dict[str, Any]], 
                            stats: Dict[str, Any], timestamp: str) -> str:
        """Generate beautiful HTML report"""
        
        # Sort airdrops for display
        sorted_airdrops = sorted(airdrops, key=lambda x: (
            x.get('priority_score', 0),
            x.get('legitimacy_score', 0)
        ), reverse=True)
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Supreme Airdrop Intelligence Report</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #333; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); overflow: hidden; }}
        .header {{ background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 2.5em; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }}
        .header p {{ margin: 10px 0 0 0; opacity: 0.9; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; padding: 30px; background: #f8f9fa; }}
        .stat-card {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; }}
        .stat-card h3 {{ color: #2a5298; margin: 0 0 10px 0; }}
        .stat-card .value {{ font-size: 2em; font-weight: bold; color: #1e3c72; }}
        .airdrops {{ padding: 30px; }}
        .airdrop-card {{ background: white; border: 1px solid #ddd; border-radius: 10px; margin: 20px 0; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        .airdrop-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }}
        .airdrop-title {{ font-size: 1.3em; font-weight: bold; color: #2a5298; margin: 0; }}
        .priority-badge {{ padding: 5px 15px; border-radius: 20px; color: white; font-weight: bold; }}
        .priority-5 {{ background: #28a745; }}
        .priority-4 {{ background: #17a2b8; }}
        .priority-3 {{ background: #ffc107; color: #333; }}
        .priority-2 {{ background: #fd7e14; }}
        .priority-1 {{ background: #dc3545; }}
        .airdrop-details {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin: 15px 0; }}
        .detail-item {{ text-align: center; }}
        .detail-label {{ font-size: 0.8em; color: #666; text-transform: uppercase; }}
        .detail-value {{ font-weight: bold; margin-top: 5px; }}
        .description {{ background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 15px 0; }}
        .footer {{ background: #333; color: white; text-align: center; padding: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Supreme Airdrop Intelligence Report</h1>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')} | Version: {CONFIG.VERSION}</p>
            <p>Target Wallet: {CONFIG.WALLET_ADDRESS}</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <h3>🎯 New Opportunities</h3>
                <div class="value">{len(airdrops)}</div>
            </div>
            <div class="stat-card">
                <h3>⚡ Sources Scanned</h3>
                <div class="value">{stats.get('total_sources', 0)}</div>
            </div>
            <div class="stat-card">
                <h3>🔍 Items Analyzed</h3>
                <div class="value">{stats.get('total_items_found', 0)}</div>
            </div>
            <div class="stat-card">
                <h3>📈 Success Rate</h3>
                <div class="value">{stats.get('success_rate', 0):.1f}%</div>
            </div>
            <div class="stat-card">
                <h3>⏱️ Processing Time</h3>
                <div class="value">{stats.get('processing_time_seconds', 0):.1f}s</div>
            </div>
        </div>
        
        <div class="airdrops">
            <h2 style="text-align: center; color: #2a5298; margin-bottom: 30px;">🏆 Priority Intelligence Discoveries</h2>
        """
        
        for i, airdrop in enumerate(sorted_airdrops[:20], 1):
            priority = airdrop.get('priority_score', 0)
            
            html += f"""
            <div class="airdrop-card">
                <div class="airdrop-header">
                    <h3 class="airdrop-title">{i}. {airdrop.get('title', 'Unknown')[:60]}</h3>
                    <span class="priority-badge priority-{priority}">Priority {priority}/5</span>
                </div>
                
                <div class="airdrop-details">
                    <div class="detail-item">
                        <div class="detail-label">Category</div>
                        <div class="detail-value">{airdrop.get('category', 'Other')}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Legitimacy</div>
                        <div class="detail-value">{airdrop.get('legitimacy_score', 0)}/100</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Risk Level</div>
                        <div class="detail-value">{airdrop.get('risk_level', 'Unknown')}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Value Est.</div>
                        <div class="detail-value">{airdrop.get('value_category', 'Unknown')}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Confidence</div>
                        <div class="detail-value">{airdrop.get('confidence_level', 0) * 100:.0f}%</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Source</div>
                        <div class="detail-value">{airdrop.get('source', 'Unknown')}</div>
                    </div>
                </div>
                
                <div class="description">
                    <strong>Description:</strong> {airdrop.get('description', 'No description available')[:200]}...
                </div>
                
                <div class="description">
                    <strong>🤖 AI Recommendation:</strong> {airdrop.get('recommendation', 'Manual review required')}
                </div>
                
                <div style="margin-top: 15px;">
                    <strong>🔗 URL:</strong> <a href="{airdrop.get('url', '#')}" target="_blank">{airdrop.get('url', 'N/A')}</a>
                </div>
            </div>
            """
        
        html += f"""
        </div>
        
        <div class="footer">
            <p>🤖 Generated by Supreme Airdrop Collector v{CONFIG.VERSION}</p>
            <p>⚡ Powered by Advanced ML Intelligence & Quantum Security</p>
            <p>🛡️ For Educational and Research Purposes Only</p>
        </div>
    </div>
</body>
</html>
        """
        
        return html
    
    def _generate_summary_report(self, airdrops: List[Dict[str, Any]], 
                               stats: Dict[str, Any]) -> str:
        """Generate concise summary report"""
        
        report = f"""
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                         SUPREME AIRDROP INTELLIGENCE SUMMARY                         ║
╠══════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                      ║
║  🕒 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}                                        ║
║  🚀 Version: {CONFIG.VERSION}                                                      ║
║  🎯 Target Wallet: {CONFIG.WALLET_ADDRESS}              ║
║                                                                                      ║
║  📊 COLLECTION STATISTICS:                                                           ║
║  ├─ 🎯 New Opportunities: {len(airdrops):>3}                                                     ║
║  ├─ ⚡ Sources Scanned: {stats.get('total_sources', 0):>5}                                                   ║
║  ├─ 🔍 Items Analyzed: {stats.get('total_items_found', 0):>6}                                                ║
║  ├─ 🔄 Duplicates Filtered: {stats.get('duplicates_filtered', 0):>4}                                            ║
║  ├─ ⏱️ Processing Time: {stats.get('processing_time_seconds', 0):>8.1f}s                                          ║
║  └─ 📈 Success Rate: {stats.get('success_rate', 0):>8.1f}%                                               ║
║                                                                                      ║
"""
        
        if airdrops:
            report += "║  🏆 TOP PRIORITY DISCOVERIES:                                                        ║\n"
            report += "║                                                                                      ║\n"
            
            # Sort and show top 5
            sorted_airdrops = sorted(airdrops, key=lambda x: (
                x.get('priority_score', 0),
                x.get('legitimacy_score', 0)
            ), reverse=True)
            
            for i, airdrop in enumerate(sorted_airdrops[:5], 1):
                title = airdrop.get('title', 'Unknown')[:45]
                priority = airdrop.get('priority_score', 0)
                legitimacy = airdrop.get('legitimacy_score', 0)
                category = airdrop.get('category', 'Other')[:10]
                
                report += f"║  {i}. {title:<45} │ 🎯 {priority}/5 │ ✅ {legitimacy:>3}/100 │ 📂 {category:<10} ║\n"
            
            report += "║                                                                                      ║\n"
        else:
            report += "║  📊 STATUS: No new opportunities detected in this scan cycle                        ║\n"
            report += "║                                                                                      ║\n"
        
        # Performance metrics
        if self.performance_monitor.get('stage_timings'):
            report += "║  ⚡ PERFORMANCE BREAKDOWN:                                                           ║\n"
            for stage, timing in self.performance_monitor['stage_timings'].items():
                stage_name = stage.replace('_', ' ').title()
                report += f"║  ├─ {stage_name:<20}: {timing:>8.2f}s                                           ║\n"
            report += "║                                                                                      ║\n"
        
        report += """║  🛡️ SECURITY REMINDERS:                                                             ║
║  • All participation is MANUAL ONLY - verify everything                             ║
║  • Never share private keys or seed phrases                                         ║
║  • Research projects thoroughly before participating                                ║
║  • Use dedicated airdrop wallet for safety                                         ║
║                                                                                      ║
║  📋 FULL REPORTS: Check reports directory for detailed analysis                     ║
║  🔄 NEXT SCAN: Automated monitoring continues every 4-6 hours                      ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
"""
        
        return report
    
    def _display_supreme_results(self, stats: Dict[str, Any], airdrops: List[Dict[str, Any]], 
                               notification_results: Dict[str, Any], report_paths: Dict[str, str]):
        """Display beautiful final results"""
        
        # Performance summary
        total_time = self.performance_monitor.get('total_processing_time', 0)
        stage_timings = self.performance_monitor.get('stage_timings', {})
        
        print(f"""
{Fore.CYAN}╔════════════════════════════════════════════════════════════════════════════════════════╗
║                           🚀 SUPREME COLLECTION COMPLETE                               ║
╠════════════════════════════════════════════════════════════════════════════════════════╣{Style.RESET_ALL}
""")
        
        # Collection Summary
        print(f"""{Fore.GREEN}║                                📊 FINAL SUMMARY                                      ║
║  ──────────────────────────────────────────────────────────────────────────────────  ║
║  🎯 New Opportunities: {len(airdrops):>8}     ⚡ Sources Scanned: {stats.get('total_sources', 0):>10}              ║
║  🔍 Items Analyzed: {stats.get('total_items_found', 0):>11}     🔄 Duplicates Filtered: {stats.get('duplicates_filtered', 0):>7}         ║
║  ⏱️  Total Processing: {total_time:>8.1f}s     📈 Success Rate: {stats.get('success_rate', 0):>10.1f}%              ║
║  💰 Target Wallet: {CONFIG.WALLET_ADDRESS:>56}  ║{Style.RESET_ALL}""")
        
        # Performance Breakdown
        if stage_timings:
            print(f"""{Fore.YELLOW}║                               ⚡ PERFORMANCE BREAKDOWN                                ║
║  ──────────────────────────────────────────────────────────────────────────────────  ║""")
            
            for stage, timing in stage_timings.items():
                stage_display = stage.replace('_', ' ').title()[:20]
                percentage = (timing / total_time * 100) if total_time > 0 else 0
                print(f"║  📊 {stage_display:<20}: {timing:>6.2f}s ({percentage:>5.1f}%)                              ║")
        
        # Notification Status
        print(f"""{Fore.BLUE}║                               📱 NOTIFICATION STATUS                                  ║
║  ──────────────────────────────────────────────────────────────────────────────────  ║""")
        
        for channel, result in notification_results.items():
            status = "✅ SENT" if result.get('success') else "❌ FAILED"
            channel_name = channel.title()
            print(f"║  📡 {channel_name:<12}: {status:<8}                                                      ║")
        
        # Report Files
        if report_paths:
            print(f"""║                                📋 GENERATED REPORTS                                   ║
║  ──────────────────────────────────────────────────────────────────────────────────  ║""")
            
            for format_type, path in report_paths.items():
                filename = os.path.basename(path)
                format_display = format_type.upper()
                print(f"║  📄 {format_display:<4}: {filename:<65} ║")
        
        print(f"""{Fore.CYAN}║                                                                                        ║
║  🎉 Supreme Intelligence Collection completed successfully!                        ║
║  📊 Reports saved | 🔐 Data encrypted | 🚀 Ready for next scan                    ║
╚════════════════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}""")
        
        # Results Summary
        if len(airdrops) > 0:
            print(f"""
{Fore.GREEN}🎯 DISCOVERED {len(airdrops)} NEW HIGH-QUALITY OPPORTUNITIES!

📋 Access your intelligence reports:
   📱 Notifications: Real-time alerts sent to configured channels
   💬 Discord: Rich embeds with detailed analysis
   📋 GitHub: Comprehensive intelligence reports with security protocols
   📊 Local Reports: {CONFIG.REPORTS_DIR}/
   
⚠️  SECURITY PROTOCOL ACTIVE:
   🔐 All participation requires MANUAL verification
   🧐 Research each opportunity thoroughly  
   💼 Use dedicated airdrop wallet for safety
   🚫 Never share private keys or seed phrases{Style.RESET_ALL}
            """)
        else:
            print(f"""
{Fore.YELLOW}🤖 No new opportunities discovered in this scan cycle.

🔄 The Supreme Collector continues monitoring...
📊 {stats.get('total_items_found', 0)} items analyzed, {stats.get('duplicates_filtered', 0)} duplicates filtered
⏱️  Processing completed in {total_time:.1f}s
🎯 Next automated scan scheduled in 4-6 hours{Style.RESET_ALL}
            """)
    
    async def run_continuous_monitoring(self, interval_hours: int = 6):
        """Run continuous monitoring with scheduled scans"""
        logger.banner("CONTINUOUS MONITORING", f"Scanning every {interval_hours} hours")
        
        while True:
            try:
                logger.info(f"🔄 Starting scheduled scan cycle...")
                
                # Run collection cycle
                results = await self.run_supreme_collection_cycle()
                
                if results['success']:
                    logger.success(f"✅ Scan completed: {results['collection_stats']['new_airdrops']} new opportunities")
                else:
                    logger.error(f"❌ Scan failed: {results.get('error')}")
                
                # Wait for next cycle
                logger.info(f"😴 Sleeping for {interval_hours} hours until next scan...")
                await asyncio.sleep(interval_hours * 3600)  # Convert to seconds
                
            except KeyboardInterrupt:
                logger.info("⏹️ Continuous monitoring stopped by user")
                break
            except Exception as e:
                logger.error(f"💥 Monitoring error: {e}")
                logger.info("🔄 Retrying in 1 hour...")
                await asyncio.sleep(3600)
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        return {
            'system_initialized': self.is_initialized,
            'version': CONFIG.VERSION,
            'config': asdict(CONFIG),
            'performance_monitor': self.performance_monitor,
            'database_analytics': self.database.get_analytics_dashboard(),
            'scraper_stats': self.scraper.get_stats(),
            'extraction_stats': self.extractor.get_extraction_stats() if hasattr(self, 'extractor') else {},
            'notification_stats': self.notification_system.get_notification_stats(),
            'sources_count': len(SUPREME_AIRDROP_SOURCES)
        }

# ═══════════════════════════════════════════════════════════════════════════════════════
# 🎮 INTERACTIVE COMMAND CENTER & UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════════════

class SupremeCommandCenter:
    """Interactive command center for the Supreme Airdrop Collector"""
    
    def __init__(self):
        self.orchestrator = SupremeAirdropOrchestrator()
    
    def display_welcome_banner(self):
        """Display beautiful welcome banner"""
        print(f"""
{Fore.CYAN}
 ███████╗██╗   ██╗██████╗ ██████╗ ███████╗███╗   ███╗███████╗
 ██╔════╝██║   ██║██╔══██╗██╔══██╗██╔════╝████╗ ████║██╔════╝
 ███████╗██║   ██║██████╔╝██████╔╝█████╗  ██╔████╔██║█████╗  
 ╚════██║██║   ██║██╔═══╝ ██╔══██╗██╔══╝  ██║╚██╔╝██║██╔══╝  
 ███████║╚██████╔╝██║     ██║  ██║███████╗██║ ╚═╝ ██║███████╗
 ╚══════╝ ╚═════╝ ╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚══════╝
                                                               
    🚀 AIRDROP COLLECTOR v{CONFIG.VERSION} - SUPREME EDITION 🚀
{Style.RESET_ALL}

{Fore.GREEN}═══════════════════════════════════════════════════════════════════════════════════════
⚡ REVOLUTIONARY FEATURES:
   🥷 Military-Grade Stealth Scraping    🧠 Advanced Local ML Intelligence
   🔐 Quantum-Level Security Vault       📊 25+ Premium Intelligence Sources
   🛡️ Advanced Anti-Detection Tech       📱 Multi-Channel Notifications
   🎯 ML-Based Risk Assessment           💾 Bulletproof Database System
   🚀 Async High-Performance Engine      📈 Real-Time Analytics Dashboard
   
🎯 TARGET WALLET: {CONFIG.WALLET_ADDRESS}
═══════════════════════════════════════════════════════════════════════════════════════{Style.RESET_ALL}

{Fore.YELLOW}⚠️  LEGAL NOTICE: For educational and legitimate research purposes only!
🛡️  SECURITY: All participation requires manual verification - never share private keys!{Style.RESET_ALL}
        """)
    
    def show_main_menu(self):
        """Display main menu"""
        print(f"""
{Fore.CYAN}🎮 SUPREME COMMAND CENTER - AVAILABLE OPERATIONS:
══════════════════════════════════════════════════════════════════════════════════════{Style.RESET_ALL}

{Fore.GREEN}📊 CORE OPERATIONS:{Style.RESET_ALL}
   1. 🚀 run_supreme_collection()       - Launch complete intelligence gathering
   2. 🔄 run_continuous_monitoring()    - Start automated monitoring (6h intervals)
   3. 📊 show_system_status()           - Display comprehensive system status
   4. 📈 show_analytics_dashboard()     - View detailed analytics and trends

{Fore.BLUE}🔧 SYSTEM MANAGEMENT:{Style.RESET_ALL}
   5. 🔐 setup_quantum_vault()          - Configure secure API vault
   6. 🗄️ show_database_stats()          - Display database statistics
   7. 🧹 cleanup_old_data()             - Clean up old database entries
   8. ⚡ initialize_system()             - Initialize/reinitialize the system

{Fore.MAGENTA}🛠️ ADVANCED UTILITIES:{Style.RESET_ALL}
   9. 🔍 test_single_source()           - Test extraction from specific source
  10. 📋 export_data()                  - Export data in various formats
  11. 🌐 test_network_connectivity()    - Test network and source connectivity
  12. 💥 nuclear_reset()                - Complete system reset (DANGER!)

{Fore.RED}🎯 QUICK ACTIONS:{Style.RESET_ALL}
   • run_supreme_collection()          - For immediate intelligence gathering
   • run_continuous_monitoring()       - For long-term automated operation

{Fore.YELLOW}📖 DOCUMENTATION: All functions include comprehensive help and safety features
💡 TIP: Start with initialize_system() if this is your first run{Style.RESET_ALL}
        """)

# Initialize command center
command_center = SupremeCommandCenter()

# ═══════════════════════════════════════════════════════════════════════════════════════
# 🎯 MAIN EXECUTION FUNCTIONS - SIMPLIFIED API
# ═══════════════════════════════════════════════════════════════════════════════════════

async def run_supreme_collection():
    """🚀 Launch complete supreme intelligence collection cycle"""
    try:
        if not command_center.orchestrator.is_initialized:
            logger.info("🔧 System not initialized. Initializing now...")
            success = await command_center.orchestrator.initialize_supreme_system()
            if not success:
                logger.error("❌ System initialization failed!")
                return False
        
        results = await command_center.orchestrator.run_supreme_collection_cycle()
        return results
        
    except KeyboardInterrupt:
        logger.info("⏹️ Collection interrupted by user")
        return False
    except Exception as e:
        logger.error(f"💥 Collection failed: {e}")
        return False

async def run_continuous_monitoring(interval_hours: int = 6):
    """🔄 Start continuous monitoring with automatic scans"""
    try:
        if not command_center.orchestrator.is_initialized:
            logger.info("🔧 Initializing system for continuous monitoring...")
            success = await command_center.orchestrator.initialize_supreme_system()
            if not success:
                logger.error("❌ System initialization failed!")
                return False
        
        await command_center.orchestrator.run_continuous_monitoring(interval_hours)
        
    except KeyboardInterrupt:
        logger.info("⏹️ Continuous monitoring stopped")
    except Exception as e:
        logger.error(f"💥 Monitoring failed: {e}")

async def initialize_system():
    """🔧 Initialize the supreme system"""
    return await command_center.orchestrator.initialize_supreme_system()

def setup_quantum_vault():
    """🔐 Setup quantum security vault"""
    return command_center.orchestrator.vault.interactive_setup()

def show_system_status():
    """📊 Display comprehensive system status"""
    status = command_center.orchestrator.get_system_status()
    
    logger.banner("SYSTEM STATUS", f"Supreme Collector v{CONFIG.VERSION}")
    
    print(f"""
{Fore.GREEN}🔧 SYSTEM INFORMATION:
├─ Initialization Status: {'✅ Ready' if status['system_initialized'] else '❌ Not Initialized'}
├─ Version: {status['version']}
├─ Database Entries: {status['database_analytics']['summary']['total_airdrops']:,}
├─ Intelligence Sources: {status['sources_count']}
└─ Performance: {status.get('scraper_stats', {}).get('success_rate', 0):.1f}% success rate

🎯 CONFIGURATION:
├─ Target Wallet: {CONFIG.WALLET_ADDRESS}
├─ Output Directory: {CONFIG.OUTPUT_DIR}
├─ Max Concurrent Requests: {CONFIG.MAX_CONCURRENT_REQUESTS}
└─ ML Confidence Threshold: {CONFIG.ML_CONFIDENCE_THRESHOLD:.0%}{Style.RESET_ALL}
    """)
    
    # Database analytics
    db_stats = status['database_analytics']
    if db_stats['summary']['total_airdrops'] > 0:
        print(f"""
{Fore.BLUE}📊 DATABASE ANALYTICS:
├─ Total Airdrops: {db_stats['summary']['total_airdrops']:,}
├─ New Airdrops: {db_stats['summary']['new_airdrops']:,}
├─ Average Legitimacy: {db_stats['summary']['avg_legitimacy']:.1f}/100
└─ Average Priority: {db_stats['summary']['avg_priority']:.1f}/5{Style.RESET_ALL}""")
    
    # Notification stats
    notif_stats = status['notification_stats']
    if notif_stats['channels_configured'] > 0:
        print(f"""
{Fore.MAGENTA}📱 NOTIFICATION SYSTEM:
├─ Channels Configured: {notif_stats['channels_configured']}
├─ Total Sent: {notif_stats['total_sent']:,}
└─ Success Rate: {(notif_stats['total_sent'] / (notif_stats['total_sent'] + notif_stats['total_failed']) * 100) if (notif_stats['total_sent'] + notif_stats['total_failed']) > 0 else 0:.1f}%{Style.RESET_ALL}""")
    
    return status

def show_analytics_dashboard():
    """📈 Display analytics dashboard"""
    analytics = command_center.orchestrator.database.get_analytics_dashboard()
    
    logger.banner("ANALYTICS DASHBOARD", "Intelligence & Performance Metrics")
    
    summary = analytics['summary']
    print(f"""
{Fore.GREEN}📊 COLLECTION SUMMARY:
├─ Total Opportunities: {summary['total_airdrops']:,}
├─ New & Unprocessed: {summary['new_airdrops']:,}  
├─ Average Legitimacy: {summary['avg_legitimacy']:.1f}/100
└─ Average Priority: {summary['avg_priority']:.1f}/5{Style.RESET_ALL}
    """)
    
    # Category breakdown
    if analytics['categories']:
        print(f"\n{Fore.BLUE}📂 CATEGORY DISTRIBUTION:")
        for category in analytics['categories'][:8]:
            name = category['name']
            count = category['count']
            avg_leg = category['avg_legitimacy']
            print(f"├─ {name:<15}: {count:>4} items (avg: {avg_leg:.1f}/100)")
    
    # Top sources
    if analytics['top_sources']:
        print(f"\n{Fore.YELLOW}🏆 TOP PERFORMING SOURCES:")
        for source in analytics['top_sources'][:5]:
            name = source['name'][:20]
            count = source['count']
            avg_leg = source['avg_legitimacy']
            print(f"├─ {name:<20}: {count:>3} items (quality: {avg_leg:.1f}/100)")
    
    # Recent trends
    if analytics['daily_trends']:
        print(f"\n{Fore.CYAN}📈 RECENT ACTIVITY (Last 7 Days):")
        for trend in analytics['daily_trends'][:5]:
            date = trend['date']
            count = trend['count']
            avg_leg = trend['avg_legitimacy']
            print(f"├─ {date}: {count:>2} discoveries (avg quality: {avg_leg:.1f}/100)")
    
    print(f"{Style.RESET_ALL}")
    return analytics

def show_database_stats():
    """🗄️ Show detailed database statistics"""
    return show_analytics_dashboard()

def cleanup_old_data(days: int = 90):
    """🧹 Clean up old database entries"""
    logger.info(f"🧹 Cleaning up entries older than {days} days...")
    
    deleted_count = command_center.orchestrator.database.cleanup_old_entries(days)
    
    if deleted_count > 0:
        logger.success(f"✅ Cleaned up {deleted_count} old entries")
    else:
        logger.info("ℹ️ No old entries found to clean up")
    
    return deleted_count

async def test_single_source(source_name: str = None):
    """🔍 Test extraction from a specific source"""
    if not source_name:
        logger.info("📋 Available sources:")
        for i, source in enumerate(SUPREME_AIRDROP_SOURCES, 1):
            print(f"  {i:2}. {source['name']} ({source['base_url']})")
        
        try:
            choice = int(input(f"\n🎯 Select source (1-{len(SUPREME_AIRDROP_SOURCES)}): ")) - 1
            if 0 <= choice < len(SUPREME_AIRDROP_SOURCES):
                source = SUPREME_AIRDROP_SOURCES[choice]
            else:
                logger.error("❌ Invalid selection")
                return False
        except (ValueError, KeyboardInterrupt):
            logger.info("⏹️ Test cancelled")
            return False
    else:
        # Find source by name
        source = next((s for s in SUPREME_AIRDROP_SOURCES if s['name'].lower() == source_name.lower()), None)
        if not source:
            logger.error(f"❌ Source '{source_name}' not found")
            return False
    
    logger.info(f"🔍 Testing extraction from {source['name']}...")
    
    try:
        if not hasattr(command_center.orchestrator, 'extractor'):
            command_center.orchestrator.extractor = SupremeContentExtractor(command_center.orchestrator.scraper)
        
        results = await command_center.orchestrator.extractor._extract_from_source_async(
            source, 
            aiohttp.ClientSession()
        )
        
        logger.success(f"✅ Extracted {len(results)} items from {source['name']}")
        
        # Display sample results
        for i, item in enumerate(results[:3], 1):
            print(f"\n{i}. {item.get('title', 'Unknown')[:60]}")
            print(f"   Source: {item.get('source')}")
            print(f"   URL: {item.get('url', 'N/A')}")
        
        return results
        
    except Exception as e:
        logger.error(f"💥 Test failed: {e}")
        return False

def export_data(format_type: str = 'json', limit: int = 100):
    """📋 Export data in various formats"""
    try:
        airdrops = command_center.orchestrator.database.get_top_airdrops(limit)
        
        if not airdrops:
            logger.warning("⚠️ No data to export")
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format_type.lower() == 'json':
            filename = f"export_{timestamp}.json"
            filepath = os.path.join(CONFIG.REPORTS_DIR, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(airdrops, f, ensure_ascii=False, indent=2)
        
        elif format_type.lower() == 'csv':
            filename = f"export_{timestamp}.csv"
            filepath = os.path.join(CONFIG.REPORTS_DIR, filename)
            
            # Flatten data for CSV
            csv_data = []
            for airdrop in airdrops:
                csv_data.append({
                    'title': airdrop.get('title'),
                    'category': airdrop.get('category'),
                    'priority_score': airdrop.get('priority_score'),
                    'legitimacy_score': airdrop.get('legitimacy_score'),
                    'risk_level': airdrop.get('risk_level'),
                    'value_category': airdrop.get('value_category'),
                    'source_name': airdrop.get('source_name'),
                    'url': airdrop.get('url'),
                    'created_at': airdrop.get('created_at')
                })
            
            df = pd.DataFrame(csv_data)
            df.to_csv(filepath, index=False, encoding='utf-8')
        
        else:
            logger.error(f"❌ Unsupported format: {format_type}")
            return None
        
        logger.success(f"✅ Exported {len(airdrops)} items to {filepath}")
        return filepath
        
    except Exception as e:
        logger.error(f"💥 Export failed: {e}")
        return None

async def test_network_connectivity():
    """🌐 Test network connectivity and source availability"""
    logger.info("🌐 Testing network connectivity and source availability...")
    
    test_results = {}
    
    async with aiohttp.ClientSession() as session:
        for source in SUPREME_AIRDROP_SOURCES[:10]:  # Test first 10 sources
            source_name = source['name']
            test_url = source['endpoints'][0] if source['endpoints'] else source.get('base_url')
            
            if not test_url:
                test_results[source_name] = {'status': 'No URL', 'response_time': 0}
                continue
            
            try:
                start_time = time.time()
                async with session.get(test_url, timeout=10) as response:
                    response_time = time.time() - start_time
                    test_results[source_name] = {
                        'status': f"HTTP {response.status}",
                        'response_time': response_time,
                        'success': response.status == 200
                    }
            except asyncio.TimeoutError:
                test_results[source_name] = {'status': 'Timeout', 'response_time': 10, 'success': False}
            except Exception as e:
                test_results[source_name] = {'status': f'Error: {str(e)}', 'response_time': 0, 'success': False}
    
    # Display results
    print(f"\n{Fore.CYAN}🌐 NETWORK CONNECTIVITY TEST RESULTS:{Style.RESET_ALL}\n")
    
    successful = 0
    total = len(test_results)
    
    for source_name, result in test_results.items():
        status = result['status']
        response_time = result['response_time']
        success_icon = "✅" if result.get('success') else "❌"
        
        if result.get('success'):
            successful += 1
        
        print(f"{success_icon} {source_name:<25}: {status:<15} ({response_time:.2f}s)")
    
    success_rate = (successful / total * 100) if total > 0 else 0
    print(f"\n📊 Overall Success Rate: {success_rate:.1f}% ({successful}/{total})")
    
    return test_results

def nuclear_reset():
    """💥 Complete system reset - DANGER!"""
    logger.banner("NUCLEAR RESET", "⚠️ EXTREME CAUTION REQUIRED ⚠️")
    
    print(f"""
{Fore.RED}💥 WARNING: NUCLEAR SYSTEM RESET
════════════════════════════════════════════════════════════════════════════════════════

This will PERMANENTLY DELETE:
🔐 Quantum security vault (all API keys)  
📊 Complete intelligence database
📋 All generated reports and analytics
🗃️ Cache and temporary files
⚙️ All configuration and preferences

This action is IRREVERSIBLE and will destroy ALL collected intelligence data!{Style.RESET_ALL}

{Fore.YELLOW}Only proceed if you want to start completely fresh.{Style.RESET_ALL}
    """)
    
    # Triple confirmation
    try:
        confirm1 = input("Type 'NUCLEAR' to confirm: ").strip()
        if confirm1 != 'NUCLEAR':
            logger.info("⏹️ Nuclear reset cancelled")
            return False
        
        confirm2 = input("Type 'DELETE ALL DATA' to double confirm: ").strip()  
        if confirm2 != 'DELETE ALL DATA':
            logger.info("⏹️ Nuclear reset cancelled")
            return False
        
        confirm3 = input("Type 'I UNDERSTAND THE CONSEQUENCES' to final confirm: ").strip()
        if confirm3 != 'I UNDERSTAND THE CONSEQUENCES':
            logger.info("⏹️ Nuclear reset cancelled")
            return False
        
        logger.warning("💥 Executing nuclear reset...")
        
        # Delete quantum vault
        if os.path.exists(CONFIG.VAULT_PATH):
            os.remove(CONFIG.VAULT_PATH)
            logger.info("🗑️ Quantum vault destroyed")
        
        # Delete entire output directory
        if os.path.exists(CONFIG.OUTPUT_DIR):
            shutil.rmtree(CONFIG.OUTPUT_DIR)
            logger.info("🗑️ All intelligence data destroyed")
        
        # Recreate basic structure
        os.makedirs(CONFIG.OUTPUT_DIR, exist_ok=True)
        os.makedirs(CONFIG.REPORTS_DIR, exist_ok=True)
        os.makedirs(CONFIG.CACHE_DIR, exist_ok=True)
        
        logger.success("✅ Nuclear reset completed!")
        logger.info("🔄 Run initialize_system() to start fresh")
        
        return True
        
    except KeyboardInterrupt:
        logger.info("⏹️ Nuclear reset cancelled by user")
        return False
    except Exception as e:
        logger.error(f"💥 Nuclear reset failed: {e}")
        return False

# ═══════════════════════════════════════════════════════════════════════════════════════
# 🎬 MAIN EXECUTION & STARTUP
# ═══════════════════════════════════════════════════════════════════════════════════════

def main():
    """Main entry point"""
    try:
        # Display welcome
        command_center.display_welcome_banner()
        command_center.show_main_menu()
        
        print(f"""
{Fore.CYAN}🚀 SUPREME AIRDROP COLLECTOR IS READY!
═══════════════════════════════════════════════════════════════════════════════════════{Style.RESET_ALL}

{Fore.GREEN}💡 QUICK START GUIDE:
1. First time? Run: await initialize_system()
2. Setup security: setup_quantum_vault() (optional but recommended)
3. Start collecting: await run_supreme_collection()
4. For automation: await run_continuous_monitoring()

⚡ INSTANT ACTION: Just run await run_supreme_collection() to start immediately!{Style.RESET_ALL}
        """)
        
    except KeyboardInterrupt:
        logger.info("⏹️ Startup interrupted")
    except Exception as e:
        logger.error(f"💥 Startup failed: {e}")

if __name__ == "__main__":
    main()

# ═══════════════════════════════════════════════════════════════════════════════════════
# 🎯 DIRECT EXECUTION SHORTCUT (Uncomment to auto-run)
# ═══════════════════════════════════════════════════════════════════════════════════════

# import asyncio
# 
# async def auto_start():
#     """Auto-start the supreme collector"""
#     logger.banner("AUTO-START", "Supreme Collection Beginning...")
#     
#     # Initialize system
#     success = await initialize_system()
#     if success:
#         # Run collection
#         await run_supreme_collection()
#     
# # Uncomment the next line to auto-run the collector:
# # asyncio.run(auto_start())