# 🚀 Ultimate Stealth Airdrop Collector - Installation & Setup Guide

## 📋 Quick Start (30 Seconds)

### Option 1: Instant Launch (Recommended)
```bash
# Download and run immediately
python3 quick_start.py
```

### Option 2: Interactive Setup
```bash
# Full interactive experience with guided setup
python3 run_collector.py
```

### Option 3: Advanced Usage
```python
# Import and use programmatically
python3 -c "
import asyncio
from ultimate_stealth_airdrop_collector import run_supreme_collection
asyncio.run(run_supreme_collection())
"
```

## 🔧 System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **Memory**: 512MB RAM
- **Storage**: 100MB free space
- **Network**: Internet connection

### Recommended Specifications  
- **Python**: 3.9+ (better performance)
- **Memory**: 2GB RAM (for optimal ML processing)
- **Storage**: 1GB free space (for reports and database)
- **Network**: Stable broadband connection

### Supported Operating Systems
- ✅ **Linux** (Ubuntu, CentOS, Debian, etc.)
- ✅ **macOS** (10.14+)
- ✅ **Windows** (10/11)
- ✅ **Docker** (any platform)

## 📦 Installation Methods

### Method 1: Automatic Installation (Easiest)
The system includes an intelligent package manager that automatically installs all required dependencies.

```bash
# Just run any script - dependencies install automatically
python3 quick_start.py
```

### Method 2: Manual Installation
```bash
# Install core dependencies
pip install requests beautifulsoup4 lxml cryptography fake-useragent
pip install fuzzywuzzy python-levenshtein pandas numpy cloudscraper
pip install aiohttp feedparser nltk scikit-learn textblob
pip install schedule tqdm colorama

# Or use requirements file
pip install -r requirements.txt
```

### Method 3: Virtual Environment (Recommended for developers)
```bash
# Create virtual environment
python3 -m venv airdrop_env
source airdrop_env/bin/activate  # Linux/Mac
# or
airdrop_env\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run the collector
python3 quick_start.py
```

### Method 4: Docker Installation (Coming Soon)
```bash
# Build Docker image
docker build -t airdrop-collector .

# Run container
docker run -it --rm airdrop-collector
```

## 🎯 Configuration Options

### Basic Configuration (No setup required)
The system works out-of-the-box with default settings:
- Target wallet: Pre-configured
- 25+ intelligence sources enabled
- Local ML processing
- SQLite database storage

### Advanced Configuration (Optional)

#### 1. API Keys Setup (Enhanced Notifications)
```bash
# Run secure vault setup
python3 -c "
from ultimate_stealth_airdrop_collector import setup_quantum_vault
setup_quantum_vault()
"
```

**Supported API Keys:**
- 📱 **Telegram Bot Token**: For real-time notifications
- 💬 **Discord Webhook**: For channel alerts
- 📋 **GitHub Token**: For automated issue reports
- 🌐 **Custom Proxy**: For enhanced anonymity

#### 2. Custom Wallet Address
```python
# Edit config.json or modify runtime
from ultimate_stealth_airdrop_collector import CONFIG
CONFIG.WALLET_ADDRESS = "YOUR_WALLET_ADDRESS_HERE"
```

#### 3. Performance Tuning
```python
# Faster scanning (more aggressive)
CONFIG.MAX_CONCURRENT_REQUESTS = 12
CONFIG.BATCH_SIZE = 100

# Conservative scanning (lower resource usage)  
CONFIG.MAX_CONCURRENT_REQUESTS = 4
CONFIG.BATCH_SIZE = 25

# Higher accuracy (stricter filtering)
CONFIG.ML_CONFIDENCE_THRESHOLD = 0.8
CONFIG.MIN_SIMILARITY_THRESHOLD = 0.9
```

## 🎮 Usage Examples

### Example 1: One-Time Scan
```python
import asyncio
from ultimate_stealth_airdrop_collector import run_supreme_collection

async def quick_scan():
    results = await run_supreme_collection()
    if results['success']:
        print(f"Found {results['collection_stats']['new_airdrops']} opportunities!")
    else:
        print("Scan failed:", results['error'])

asyncio.run(quick_scan())
```

### Example 2: Continuous Monitoring
```python
import asyncio
from ultimate_stealth_airdrop_collector import run_continuous_monitoring

# Monitor every 6 hours
asyncio.run(run_continuous_monitoring(interval_hours=6))
```

### Example 3: Custom Analysis
```python
from ultimate_stealth_airdrop_collector import AdvancedMLIntelligence

# Analyze custom airdrop data
ml_engine = AdvancedMLIntelligence()
airdrop_data = {
    "title": "DeFi Protocol Token Launch",
    "description": "Revolutionary decentralized finance protocol...",
    "source": "custom_source",
    "url": "https://example.com"
}

analysis = ml_engine.analyze_airdrop_intelligence(airdrop_data)
print(f"Category: {analysis['category']}")
print(f"Priority: {analysis['priority_score']}/5")
print(f"Risk: {analysis['risk_assessment']['level']}")
```

### Example 4: Database Operations
```python
from ultimate_stealth_airdrop_collector import QuantumIntelligenceDatabase

db = QuantumIntelligenceDatabase()

# Get top opportunities
top_airdrops = db.get_top_airdrops(limit=20, min_priority=4)

# Analytics dashboard
analytics = db.get_analytics_dashboard()
print(f"Total discoveries: {analytics['summary']['total_airdrops']}")
```

## 🔧 Troubleshooting

### Common Issues & Solutions

#### Issue: Import Errors
```bash
# Solution: Install missing packages
pip install --upgrade pip
pip install -r requirements.txt

# Alternative: Use auto-installer
python3 -c "
from ultimate_stealth_airdrop_collector import IntelligentPackageManager
IntelligentPackageManager.smart_install()
"
```

#### Issue: Permission Denied
```bash
# Solution: Fix file permissions
chmod +x *.py
chmod 755 stealth_airdrop_data/
```

#### Issue: Network Connectivity
```python
# Test network connectivity
import asyncio
from ultimate_stealth_airdrop_collector import test_network_connectivity

asyncio.run(test_network_connectivity())
```

#### Issue: Database Errors
```python
# Reinitialize database
from ultimate_stealth_airdrop_collector import QuantumIntelligenceDatabase

db = QuantumIntelligenceDatabase()
db.init_database()
print("Database reinitialized")
```

#### Issue: Memory Usage
```python
# Reduce memory usage
from ultimate_stealth_airdrop_collector import CONFIG

CONFIG.MAX_CONCURRENT_REQUESTS = 4
CONFIG.BATCH_SIZE = 25
CONFIG.CACHE_EXPIRY_HOURS = 1
```

### Performance Optimization

#### For Maximum Speed
```python
CONFIG.MAX_CONCURRENT_REQUESTS = 16
CONFIG.BATCH_SIZE = 100
CONFIG.REQUEST_TIMEOUT = 15
```

#### For Maximum Accuracy
```python
CONFIG.ML_CONFIDENCE_THRESHOLD = 0.85
CONFIG.MIN_SIMILARITY_THRESHOLD = 0.9
CONFIG.MAX_RETRIES = 7
```

#### For Minimum Resource Usage
```python
CONFIG.MAX_CONCURRENT_REQUESTS = 2
CONFIG.BATCH_SIZE = 10  
CONFIG.CACHE_EXPIRY_HOURS = 24
```

## 📊 Monitoring & Maintenance

### System Status Check
```python
from ultimate_stealth_airdrop_collector import show_system_status
show_system_status()
```

### Analytics Dashboard
```python
from ultimate_stealth_airdrop_collector import show_analytics_dashboard
show_analytics_dashboard()
```

### Database Maintenance
```python
from ultimate_stealth_airdrop_collector import cleanup_old_data

# Clean entries older than 90 days
deleted_count = cleanup_old_data(days=90)
print(f"Cleaned up {deleted_count} old entries")
```

### Export Data
```python
from ultimate_stealth_airdrop_collector import export_data

# Export to JSON
json_file = export_data(format_type='json', limit=1000)
print(f"Data exported to: {json_file}")

# Export to CSV
csv_file = export_data(format_type='csv', limit=1000)
print(f"Data exported to: {csv_file}")
```

## 🛡️ Security Best Practices

### System Security
1. **Keep Software Updated**: Regularly update Python and dependencies
2. **Secure Environment**: Use virtual environments for isolation
3. **File Permissions**: Restrict access to sensitive files
4. **Regular Backups**: Backup your database and configuration

### API Security
1. **Strong Passphrases**: Use complex passphrases for vault encryption
2. **Limited Permissions**: Use API keys with minimal required permissions
3. **Regular Rotation**: Rotate API keys periodically
4. **Secure Storage**: Never store credentials in plain text

### Operational Security
1. **Manual Verification**: Always verify opportunities manually
2. **Dedicated Wallet**: Use separate wallet for airdrop activities
3. **Research Thoroughly**: Investigate projects before participation
4. **Stay Updated**: Monitor security advisories and updates

## 📞 Support & Resources

### Getting Help
1. **Documentation**: Check README.md and this guide
2. **Error Messages**: Read error messages carefully - they often contain solutions
3. **Log Files**: Check `stealth_airdrop_data/stealth_collector.log` for detailed logs
4. **System Status**: Run `show_system_status()` for diagnostics

### Community Resources
- 📖 **Full Documentation**: README.md
- 🐛 **Bug Reports**: GitHub Issues  
- 💡 **Feature Requests**: GitHub Discussions
- 🤝 **Contributions**: Fork and contribute

### Advanced Support
- 🔧 **Custom Configuration**: Modify `config.json`
- 🧠 **ML Tuning**: Adjust ML parameters for your use case
- 🌐 **Source Addition**: Add custom intelligence sources
- 📊 **Analytics**: Create custom reports and dashboards

---

## 🎉 You're All Set!

The Ultimate Stealth Airdrop Collector is now ready for operation. Choose your preferred method to get started:

### 🚀 Quick Start
```bash
python3 quick_start.py
```

### 🎮 Interactive Mode
```bash
python3 run_collector.py
```

### 🔄 Continuous Monitoring
```python
import asyncio
from ultimate_stealth_airdrop_collector import run_continuous_monitoring
asyncio.run(run_continuous_monitoring())
```

**Happy hunting! Stay safe and always verify everything manually! 🛡️**