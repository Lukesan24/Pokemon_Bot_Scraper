# Pokemon Bot Scraper

A functional and discrete web scraper that uses Selenium to automate the process of digital purchasing of valuable Pokemon TCG products, with built-in antibot detection capabilities.

## Features

### 🔍 Antibot Detection & Research
The scraper includes comprehensive antibot detection capabilities to identify potential setbacks before attempting automation:

- **Cloudflare Protection Detection** - Identifies challenge pages, cookies, and protection mechanisms
- **CAPTCHA Detection** - Detects reCAPTCHA v2/v3 and hCaptcha implementations
- **JavaScript Challenge Detection** - Identifies JS-based bot detection techniques
- **Bot Detection Scripts** - Recognizes services like DataDome, PerimeterX, Kasada, Akamai, etc.
- **Rate Limiting Detection** - Identifies rate limiting and request throttling
- **WAF Detection** - Detects Web Application Firewalls (Cloudflare, Akamai, Imperva, etc.)
- **Selenium Detection** - Checks if the site detects automation tools
- **Risk Level Assessment** - Provides overall risk scoring (Low, Medium, High, Critical)

### 🥷 Stealth Capabilities
- Undetectable Chrome WebDriver configuration
- User-Agent rotation
- Human-like behavior simulation (random delays, realistic interactions)
- JavaScript automation hiding
- Browser fingerprint masking

### 🎯 Target Marketplaces
Pre-configured support for popular Pokemon TCG marketplaces:
- TCGPlayer
- CardMarket
- eBay
- Troll and Toad

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Lukesan24/Pokemon_Bot_Scraper.git
cd Pokemon_Bot_Scraper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure Chrome browser is installed on your system.

## Quick Start

### Running Antibot Research

The primary feature is conducting fast research to identify antibot measures:

```bash
# Run the demo script
python demo_antibot_research.py
```

Or use the main scraper directly:

```bash
# Analyze all marketplaces
python scraper.py
```

### Programmatic Usage

```python
from scraper import PokemonBotScraper

# Create scraper with stealth mode
with PokemonBotScraper(headless=False, stealth_mode=True) as scraper:
    # Analyze a single marketplace
    results = scraper.analyze_marketplace('tcgplayer')
    
    # Check risk level
    print(f"Risk Level: {results['risk_level']}")
    
    # Analyze all marketplaces
    all_results = scraper.analyze_all_marketplaces()
```

### Analyzing Custom URLs

```python
from scraper import PokemonBotScraper

with PokemonBotScraper(stealth_mode=True) as scraper:
    results = scraper.conduct_antibot_research('https://example.com')
    
    # Generate detailed report
    report = scraper.antibot_detector.generate_report(results)
    print(report)
```

## Configuration

Edit `config.py` to customize:
- Target marketplaces
- Browser settings (headless mode, timeouts)
- User agents for rotation
- Antibot detection timeouts

## Project Structure

```
Pokemon_Bot_Scraper/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── config.py                    # Configuration settings
├── antibot_detector.py          # Antibot detection module
├── scraper.py                   # Main scraper implementation
├── demo_antibot_research.py     # Interactive demo script
└── .gitignore                   # Git ignore rules
```

## Antibot Detection Details

The antibot detector performs the following checks:

1. **Cloudflare Protection**
   - Challenge page detection
   - Cookie analysis
   - Ray ID identification

2. **CAPTCHA Systems**
   - Google reCAPTCHA (v2 and v3)
   - hCaptcha
   - Iframe and script detection

3. **JavaScript Challenges**
   - WebDriver flag exposure
   - Plugin enumeration
   - Browser fingerprinting

4. **Bot Detection Services**
   - DataDome
   - PerimeterX
   - Kasada
   - Shape Security
   - Distil Networks
   - Akamai Bot Manager
   - Imperva

5. **Rate Limiting**
   - HTTP 429 responses
   - Rate limit messages
   - Temporary blocks

6. **WAF Detection**
   - Cloudflare WAF
   - Akamai WAF
   - AWS WAF
   - F5 BIG-IP
   - Imperva/Incapsula
   - Sucuri

7. **Selenium Detection**
   - navigator.webdriver checks
   - Chrome runtime presence
   - Plugin count validation
   - Permissions API checks

## Risk Levels

- **Low**: Minimal bot protection, standard automation should work
- **Medium**: Some protection present, use stealth techniques and delays
- **High**: Significant protection, requires advanced bypass techniques
- **Critical**: Heavy protection, automation very difficult

## Usage Examples

### Example 1: Check a Marketplace Before Automation

```python
from scraper import PokemonBotScraper

scraper = PokemonBotScraper(stealth_mode=True)
scraper.initialize_driver()

# Research antibot measures
results = scraper.analyze_marketplace('tcgplayer')

if results['risk_level'] in ['low', 'medium']:
    print("Safe to proceed with automation")
    # Continue with scraping/purchasing logic
else:
    print("High risk detected, use advanced techniques")

scraper.close()
```

### Example 2: Batch Analysis

```python
from scraper import PokemonBotScraper

with PokemonBotScraper(stealth_mode=True) as scraper:
    results = scraper.analyze_all_marketplaces()
    
    # Find the safest marketplace
    safest = min(results.items(), 
                 key=lambda x: ['low', 'medium', 'high', 'critical'].index(
                     x[1].get('risk_level', 'critical')
                 ))
    
    print(f"Safest marketplace: {safest[0]}")
```

## Legal & Ethical Considerations

⚠️ **Important Notice**: This tool is for educational and research purposes. Always ensure you:

1. Review and comply with the Terms of Service of any website you interact with
2. Respect rate limits and robots.txt files
3. Do not overload servers with excessive requests
4. Use the tool responsibly and ethically
5. Obtain proper authorization before automating purchases
6. Comply with all applicable laws and regulations

## Requirements

- Python 3.7+
- Chrome browser
- Internet connection
- Dependencies listed in `requirements.txt`

## Troubleshooting

### ChromeDriver Issues
If you encounter ChromeDriver issues:
```bash
pip install --upgrade webdriver-manager
```

### Selenium Not Working
Ensure Chrome browser is installed and up to date:
```bash
google-chrome --version  # Linux
# or check manually on Windows/Mac
```

### Detection Issues
If sites still detect automation:
1. Disable headless mode
2. Add more random delays
3. Use residential proxies (not included in base version)
4. Implement more sophisticated browser fingerprinting countermeasures

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

This project is provided as-is for educational purposes.

## Disclaimer

This tool is intended for educational and research purposes only. The authors are not responsible for any misuse or damage caused by this program. Use at your own risk and always comply with applicable laws and website terms of service.
