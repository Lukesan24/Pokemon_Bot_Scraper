#!/usr/bin/env python3
"""
Demo script for antibot detection research.

This script demonstrates how to use the antibot detection capabilities
to analyze Pokemon TCG marketplaces before attempting automation.
"""

import sys
from scraper import PokemonBotScraper
import config


def demo_single_marketplace():
    """Demo: Analyze a single marketplace."""
    print("\n" + "=" * 70)
    print("DEMO: Single Marketplace Analysis")
    print("=" * 70 + "\n")
    
    # Create scraper with stealth mode enabled
    with PokemonBotScraper(headless=False, stealth_mode=True) as scraper:
        # Analyze TCGPlayer as an example
        results = scraper.analyze_marketplace('tcgplayer')
        
        if results:
            print(f"\n[*] Risk Level: {results['risk_level'].upper()}")
            print(f"[*] Cloudflare Detected: {results['cloudflare']['detected']}")
            print(f"[*] reCAPTCHA Detected: {results['recaptcha']['detected']}")


def demo_all_marketplaces():
    """Demo: Analyze all configured marketplaces."""
    print("\n" + "=" * 70)
    print("DEMO: All Marketplaces Analysis")
    print("=" * 70 + "\n")
    
    with PokemonBotScraper(headless=False, stealth_mode=True) as scraper:
        results = scraper.analyze_all_marketplaces()
        
        # Print detailed summary
        print("\n[*] Analysis Complete!")
        print(f"[*] Total marketplaces analyzed: {len(results)}")


def demo_custom_url():
    """Demo: Analyze a custom URL."""
    print("\n" + "=" * 70)
    print("DEMO: Custom URL Analysis")
    print("=" * 70 + "\n")
    
    # Get URL from command line or use default
    if len(sys.argv) > 1:
        custom_url = sys.argv[1]
    else:
        custom_url = "https://www.tcgplayer.com/"
    
    print(f"[*] Analyzing custom URL: {custom_url}\n")
    
    with PokemonBotScraper(headless=False, stealth_mode=True) as scraper:
        results = scraper.conduct_antibot_research(custom_url)
        
        # Generate detailed report
        report = scraper.antibot_detector.generate_report(results)
        
        # Save report to file
        report_file = 'antibot_report.txt'
        with open(report_file, 'w') as f:
            f.write(report)
        
        print(f"\n[✓] Detailed report saved to: {report_file}")


def print_menu():
    """Print demo menu."""
    print("\n" + "=" * 70)
    print("ANTIBOT RESEARCH DEMO - MENU")
    print("=" * 70)
    print("\nAvailable demos:")
    print("  1. Analyze a single marketplace (TCGPlayer)")
    print("  2. Analyze all configured marketplaces")
    print("  3. Analyze a custom URL")
    print("  4. Exit")
    print("\nConfigured marketplaces:")
    for name, url in config.MARKETPLACES.items():
        print(f"  • {name}: {url}")
    print()


def main():
    """Main demo function."""
    print("=" * 70)
    print("POKEMON BOT SCRAPER - ANTIBOT DETECTION DEMO")
    print("=" * 70)
    print("\nThis demo showcases the antibot detection capabilities")
    print("for Pokemon TCG marketplace analysis.\n")
    
    while True:
        print_menu()
        
        try:
            choice = input("Select a demo (1-4): ").strip()
            
            if choice == '1':
                demo_single_marketplace()
            elif choice == '2':
                demo_all_marketplaces()
            elif choice == '3':
                demo_custom_url()
            elif choice == '4':
                print("\n[*] Exiting demo. Goodbye!\n")
                break
            else:
                print("\n[!] Invalid choice. Please select 1-4.")
            
            input("\nPress Enter to continue...")
            
        except KeyboardInterrupt:
            print("\n\n[!] Demo interrupted by user. Goodbye!\n")
            break
        except Exception as e:
            print(f"\n[!] Error: {str(e)}")
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
