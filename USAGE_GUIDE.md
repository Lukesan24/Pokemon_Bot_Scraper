# Usage Guide - Pokemon Bot Scraper

This guide provides detailed instructions on how to use the Pokemon Bot Scraper's antibot detection capabilities.

## Table of Contents
1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Antibot Detection Features](#antibot-detection-features)
4. [Usage Patterns](#usage-patterns)
5. [Understanding Results](#understanding-results)
6. [Advanced Configuration](#advanced-configuration)
7. [Troubleshooting](#troubleshooting)

## Installation

### Prerequisites
- Python 3.7 or higher
- Google Chrome browser installed
- pip package manager

### Step-by-Step Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Lukesan24/Pokemon_Bot_Scraper.git
cd Pokemon_Bot_Scraper
```

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

3. **Verify installation:**
```bash
python3 -c "import selenium; print('Selenium version:', selenium.__version__)"
```

## Quick Start

### Method 1: Interactive Demo

Run the interactive demo to explore all features:

```bash
python demo_antibot_research.py
```

This will present you with a menu:
- Option 1: Analyze a single marketplace
- Option 2: Analyze all marketplaces
- Option 3: Analyze a custom URL
- Option 4: Exit

### Method 2: Example Scripts

Run the example usage script:

```bash
python example_usage.py
```

This provides several pre-configured examples demonstrating different use cases.

### Method 3: Main Scraper

Run the main scraper directly:

```bash
python scraper.py
```

This will automatically analyze all configured Pokemon TCG marketplaces.

## Antibot Detection Features

### What Gets Detected

The scraper performs comprehensive checks for the following antibot measures:

#### 1. Cloudflare Protection
- **What it is:** A popular CDN and security service that can block automated traffic
- **How we detect it:** 
  - Checks for Cloudflare challenge pages
  - Identifies Cloudflare cookies
  - Detects "Just a moment" or "Checking your browser" messages
- **Impact:** High - Can completely block automation

#### 2. CAPTCHA Systems
- **What it is:** Challenge-response tests to determine if the user is human
- **Types detected:**
  - Google reCAPTCHA v2
  - Google reCAPTCHA v3
  - hCaptcha
- **How we detect it:**
  - Searches for CAPTCHA iframes
  - Identifies CAPTCHA scripts in page source
  - Checks for CAPTCHA-specific elements
- **Impact:** High - Requires human interaction or advanced solving

#### 3. JavaScript Challenges
- **What it is:** JavaScript code that tests for automation indicators
- **How we detect it:**
  - Checks navigator.webdriver flag
  - Analyzes browser plugin count
  - Identifies suspicious browser properties
- **Impact:** Medium - Can be bypassed with stealth techniques

#### 4. Bot Detection Scripts
- **What it is:** Third-party services that detect and block bots
- **Services detected:**
  - DataDome
  - PerimeterX
  - Kasada
  - Akamai Bot Manager
  - Shape Security
  - Distil Networks
  - Imperva
- **How we detect it:**
  - Searches page source for service names
  - Identifies detection script URLs
- **Impact:** Critical - Very difficult to bypass

#### 5. Rate Limiting
- **What it is:** Restrictions on request frequency
- **How we detect it:**
  - Checks for "too many requests" messages
  - Identifies HTTP 429 errors
  - Detects rate limit warnings
- **Impact:** Medium - Can be avoided with delays

#### 6. Web Application Firewall (WAF)
- **What it is:** Security layer that filters malicious traffic
- **Types detected:**
  - Cloudflare WAF
  - Akamai WAF
  - AWS WAF
  - F5 BIG-IP
  - Imperva/Incapsula
  - Sucuri
- **How we detect it:**
  - Analyzes response headers
  - Searches for WAF signatures
- **Impact:** High - Can block suspicious traffic patterns

#### 7. Selenium Detection
- **What it is:** Techniques that specifically identify Selenium automation
- **How we detect it:**
  - Checks if navigator.webdriver is exposed
  - Identifies missing Chrome runtime
  - Detects zero plugin count
  - Checks for Selenium artifacts
- **Impact:** High - Directly targets automation tools

## Usage Patterns

### Pattern 1: Pre-Automation Research

Before attempting any automation, research the target site:

```python
from scraper import PokemonBotScraper

# Create scraper
scraper = PokemonBotScraper(headless=False, stealth_mode=True)
scraper.initialize_driver()

# Research the marketplace
results = scraper.analyze_marketplace('tcgplayer')

# Make decision
if results['risk_level'] in ['low', 'medium']:
    print("✓ Safe to proceed")
    # Continue with your automation logic here
else:
    print("✗ High risk - reconsider approach")

scraper.close()
```

### Pattern 2: Comparative Analysis

Compare multiple marketplaces to find the safest target:

```python
from scraper import PokemonBotScraper

with PokemonBotScraper(stealth_mode=True) as scraper:
    results = scraper.analyze_all_marketplaces()
    
    # Find marketplace with lowest risk
    safe_marketplaces = [
        name for name, data in results.items()
        if data.get('risk_level') in ['low', 'medium']
    ]
    
    print(f"Safe marketplaces: {safe_marketplaces}")
```

### Pattern 3: Custom URL Analysis

Analyze any URL, not just pre-configured marketplaces:

```python
from scraper import PokemonBotScraper

with PokemonBotScraper(stealth_mode=True) as scraper:
    # Analyze custom Pokemon card seller
    results = scraper.conduct_antibot_research('https://example.com')
    
    # Generate and save report
    report = scraper.antibot_detector.generate_report(results)
    
    with open('analysis_report.txt', 'w') as f:
        f.write(report)
```

### Pattern 4: Specific Protection Check

Check for specific types of protection:

```python
from scraper import PokemonBotScraper

with PokemonBotScraper(stealth_mode=True) as scraper:
    results = scraper.analyze_marketplace('cardmarket')
    
    # Check specific protections
    has_cloudflare = results['cloudflare']['detected']
    has_captcha = results['recaptcha']['detected'] or results['hcaptcha']['detected']
    has_bot_scripts = results['bot_detection_scripts']['detected']
    
    print(f"Cloudflare: {has_cloudflare}")
    print(f"CAPTCHA: {has_captcha}")
    print(f"Bot Detection Scripts: {has_bot_scripts}")
```

## Understanding Results

### Risk Levels Explained

#### Low Risk
- **Characteristics:**
  - Minimal or no bot protection detected
  - Standard Selenium automation should work
  - Basic rate limiting may be present
- **Recommendation:** Proceed with standard automation techniques

#### Medium Risk
- **Characteristics:**
  - Some bot protection measures detected
  - May have basic CAPTCHA or rate limiting
  - JavaScript challenges present
- **Recommendation:** 
  - Use stealth mode
  - Implement random delays
  - Rotate user agents
  - Monitor for blocks

#### High Risk
- **Characteristics:**
  - Significant bot protection in place
  - Multiple detection mechanisms
  - May have advanced JavaScript challenges
- **Recommendation:**
  - Use advanced stealth techniques
  - Implement human-like behavior
  - Consider using undetected-chromedriver
  - Add residential proxies
  - Use longer delays between actions

#### Critical Risk
- **Characteristics:**
  - Heavy bot detection services active
  - Multiple layers of protection
  - Advanced fingerprinting
  - Strong CAPTCHA systems
- **Recommendation:**
  - Automation may not be feasible
  - Consider manual approaches
  - Consult with security experts
  - May violate Terms of Service

### Interpreting Detection Results

Each detection result includes:

1. **detected:** Boolean indicating if the measure was found
2. **indicators:** List of specific findings
3. **type/version:** Additional details about what was detected

Example result structure:
```python
{
    'url': 'https://example.com',
    'timestamp': '2024-01-15 10:30:00',
    'risk_level': 'medium',
    'cloudflare': {
        'detected': True,
        'type': 'Challenge Page',
        'indicators': ['Cloudflare cookies found: [cf_clearance]']
    },
    'recaptcha': {
        'detected': False,
        'indicators': []
    },
    # ... other detections
}
```

## Advanced Configuration

### Custom Marketplaces

Add your own marketplaces to `config.py`:

```python
MARKETPLACES = {
    'tcgplayer': 'https://www.tcgplayer.com/',
    'your_marketplace': 'https://your-marketplace.com/',
}
```

### Browser Settings

Adjust browser behavior in `config.py`:

```python
HEADLESS_MODE = False  # Set True for headless browsing
BROWSER_TIMEOUT = 10  # seconds
PAGE_LOAD_TIMEOUT = 30  # seconds
```

### User Agent Rotation

Add more user agents in `config.py`:

```python
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...',
    'Your custom user agent string here',
]
```

### Detection Timeout

Adjust how long to wait for detection checks:

```python
ANTIBOT_CHECK_TIMEOUT = 5  # seconds
```

## Troubleshooting

### Issue: ChromeDriver not found

**Solution:**
```bash
pip install --upgrade webdriver-manager
```

The webdriver-manager package automatically downloads and manages ChromeDriver.

### Issue: Chrome browser not found

**Solution:**
- Ensure Google Chrome is installed
- Verify installation:
  ```bash
  google-chrome --version  # Linux
  # or check manually on Windows/Mac
  ```

### Issue: Selenium still detected

**Solutions:**
1. Ensure stealth_mode is enabled:
   ```python
   scraper = PokemonBotScraper(stealth_mode=True)
   ```

2. Use non-headless mode:
   ```python
   scraper = PokemonBotScraper(headless=False, stealth_mode=True)
   ```

3. Add more delays:
   ```python
   scraper.human_like_delay(2, 5)  # 2-5 second random delay
   ```

### Issue: Rate limited

**Solutions:**
1. Increase delays between requests
2. Don't analyze the same site repeatedly in short periods
3. Consider using proxies (not included in base version)

### Issue: Import errors

**Solution:**
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

Verify Python version:
```bash
python --version  # Should be 3.7 or higher
```

### Issue: Permission denied on Linux

**Solution:**
Make scripts executable:
```bash
chmod +x demo_antibot_research.py
chmod +x example_usage.py
```

## Best Practices

1. **Always research before automating:** Run antibot detection before attempting any automation
2. **Respect rate limits:** Don't overload servers with requests
3. **Use stealth mode:** Enable stealth techniques for better results
4. **Add human-like delays:** Use random delays to simulate human behavior
5. **Monitor risk levels:** Regularly check if protection measures have changed
6. **Save reports:** Keep records of detection results for analysis
7. **Stay legal:** Always comply with Terms of Service and applicable laws

## Legal and Ethical Considerations

⚠️ **Important:**
- This tool is for educational and research purposes
- Always review and comply with website Terms of Service
- Respect robots.txt files
- Don't overload servers with requests
- Obtain proper authorization before automating purchases
- Use responsibly and ethically

## Getting Help

If you encounter issues:
1. Check this usage guide
2. Review the main README.md
3. Check existing GitHub issues
4. Open a new issue with detailed information about your problem

## Next Steps

After understanding antibot detection:
1. Implement specific marketplace scrapers
2. Add product search functionality
3. Implement purchase automation (carefully and ethically)
4. Add notification systems
5. Implement proxy rotation for better anonymity

Remember: The antibot detection is just the first step. Always use automation responsibly and legally.
