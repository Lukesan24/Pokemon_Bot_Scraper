"""
Pokemon Bot Scraper - Main Module

A functional and discrete web scraper using Selenium to automate
digital purchasing of Pokemon TCG products.
"""

import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from typing import Optional, List, Dict

import config
from antibot_detector import AntibotDetector


class PokemonBotScraper:
    """
    Main scraper class for automating Pokemon TCG product purchases.
    
    This class provides stealth browsing capabilities and integrates
    antibot detection to ensure discrete operation.
    """
    
    def __init__(self, headless: bool = False, stealth_mode: bool = True):
        """
        Initialize the Pokemon Bot Scraper.
        
        Args:
            headless: Whether to run browser in headless mode
            stealth_mode: Whether to apply stealth techniques
        """
        self.headless = headless
        self.stealth_mode = stealth_mode
        self.driver = None
        self.antibot_detector = None
        
    def initialize_driver(self):
        """Initialize the Chrome WebDriver with stealth settings."""
        print("[*] Initializing Chrome WebDriver...")
        
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument('--headless')
        
        if self.stealth_mode:
            # Apply stealth techniques to avoid detection
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Set a realistic user agent
            user_agent = random.choice(config.USER_AGENTS)
            chrome_options.add_argument(f'user-agent={user_agent}')
            
            # Additional stealth options
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--start-maximized')
        
        # Initialize driver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Set timeouts
        self.driver.set_page_load_timeout(config.PAGE_LOAD_TIMEOUT)
        self.driver.implicitly_wait(config.BROWSER_TIMEOUT)
        
        if self.stealth_mode:
            # Execute stealth JavaScript
            self._apply_stealth_js()
        
        # Initialize antibot detector
        self.antibot_detector = AntibotDetector(self.driver)
        
        print("[✓] WebDriver initialized successfully")
        
    def _apply_stealth_js(self):
        """Apply JavaScript to hide automation indicators."""
        stealth_js = """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
            
            window.chrome = {
                runtime: {}
            };
            
            Object.defineProperty(navigator, 'permissions', {
                get: () => ({
                    query: () => Promise.resolve({ state: 'granted' })
                })
            });
        """
        
        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': stealth_js
        })
    
    def conduct_antibot_research(self, url: str) -> Dict:
        """
        Conduct fast research to identify antibot measures on a marketplace.
        
        Args:
            url: The marketplace URL to analyze
            
        Returns:
            Dictionary containing antibot detection results
        """
        if not self.driver:
            self.initialize_driver()
        
        print(f"\n[*] Conducting antibot research for: {url}")
        results = self.antibot_detector.detect_all_measures(url, timeout=config.ANTIBOT_CHECK_TIMEOUT)
        
        # Generate and print report
        report = self.antibot_detector.generate_report(results)
        
        return results
    
    def analyze_marketplace(self, marketplace_name: str) -> Dict:
        """
        Analyze a specific marketplace from config.
        
        Args:
            marketplace_name: Name of the marketplace (e.g., 'tcgplayer')
            
        Returns:
            Dictionary containing antibot detection results
        """
        if marketplace_name not in config.MARKETPLACES:
            print(f"[!] Unknown marketplace: {marketplace_name}")
            print(f"[*] Available marketplaces: {', '.join(config.MARKETPLACES.keys())}")
            return None
        
        url = config.MARKETPLACES[marketplace_name]
        return self.conduct_antibot_research(url)
    
    def analyze_all_marketplaces(self) -> Dict[str, Dict]:
        """
        Analyze all configured marketplaces for antibot measures.
        
        Returns:
            Dictionary mapping marketplace names to their detection results
        """
        results = {}
        
        print("\n" + "=" * 70)
        print("ANALYZING ALL POKEMON TCG MARKETPLACES")
        print("=" * 70 + "\n")
        
        for name, url in config.MARKETPLACES.items():
            print(f"\n[*] Analyzing {name.upper()}...")
            try:
                results[name] = self.conduct_antibot_research(url)
                time.sleep(2)  # Brief delay between requests
            except Exception as e:
                print(f"[!] Error analyzing {name}: {str(e)}")
                results[name] = {'error': str(e)}
        
        # Print summary
        self._print_summary(results)
        
        return results
    
    def _print_summary(self, results: Dict[str, Dict]):
        """Print a summary of all marketplace analyses."""
        print("\n" + "=" * 70)
        print("SUMMARY: MARKETPLACE RISK LEVELS")
        print("=" * 70 + "\n")
        
        for marketplace, data in results.items():
            if 'error' in data:
                print(f"{marketplace.upper():.<30} ERROR")
            else:
                risk = data.get('risk_level', 'unknown').upper()
                print(f"{marketplace.upper():.<30} {risk}")
        
        print("\n" + "=" * 70 + "\n")
    
    def human_like_delay(self, min_seconds: float = 1.0, max_seconds: float = 3.0):
        """
        Add a random delay to simulate human behavior.
        
        Args:
            min_seconds: Minimum delay in seconds
            max_seconds: Maximum delay in seconds
        """
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
    
    def navigate_to(self, url: str):
        """
        Navigate to a URL with human-like behavior.
        
        Args:
            url: The URL to navigate to
        """
        if not self.driver:
            self.initialize_driver()
        
        print(f"[*] Navigating to: {url}")
        self.driver.get(url)
        self.human_like_delay(1, 2)
    
    def close(self):
        """Close the browser and clean up resources."""
        if self.driver:
            print("[*] Closing browser...")
            self.driver.quit()
            self.driver = None
            print("[✓] Browser closed")
    
    def __enter__(self):
        """Context manager entry."""
        self.initialize_driver()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


def main():
    """Main function demonstrating scraper usage."""
    print("=" * 70)
    print("POKEMON BOT SCRAPER - ANTIBOT RESEARCH MODE")
    print("=" * 70)
    print("\nThis tool performs fast research to identify antibot measures")
    print("on Pokemon TCG marketplaces before attempting automation.\n")
    
    # Create scraper instance
    scraper = PokemonBotScraper(headless=False, stealth_mode=True)
    
    try:
        # Initialize the driver
        scraper.initialize_driver()
        
        # Analyze all marketplaces
        results = scraper.analyze_all_marketplaces()
        
        # You can also analyze individual marketplaces
        # scraper.analyze_marketplace('tcgplayer')
        
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user")
    except Exception as e:
        print(f"\n[!] Error: {str(e)}")
    finally:
        scraper.close()


if __name__ == "__main__":
    main()
