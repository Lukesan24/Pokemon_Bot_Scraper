#!/usr/bin/env python3
"""
Example usage of the Pokemon Bot Scraper antibot detection features.

This script shows various ways to use the scraper for antibot research.
"""

from scraper import PokemonBotScraper
import config


def example_1_single_marketplace():
    """
    Example 1: Analyze a single marketplace for antibot measures.
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Single Marketplace Analysis")
    print("=" * 70 + "\n")
    
    # Create scraper instance
    scraper = PokemonBotScraper(headless=False, stealth_mode=True)
    
    try:
        # Initialize the browser
        scraper.initialize_driver()
        
        # Analyze TCGPlayer
        print("[*] Analyzing TCGPlayer for antibot measures...")
        results = scraper.analyze_marketplace('tcgplayer')
        
        # Check results
        if results:
            print(f"\n[✓] Analysis complete!")
            print(f"[*] Risk Level: {results['risk_level'].upper()}")
            
            # Make decision based on risk level
            if results['risk_level'] == 'low':
                print("[*] ✓ Safe to proceed with automation")
            elif results['risk_level'] == 'medium':
                print("[*] ⚠ Use caution and implement delays")
            else:
                print("[*] ✗ High risk - use advanced techniques")
        
    finally:
        scraper.close()


def example_2_compare_marketplaces():
    """
    Example 2: Compare all marketplaces and find the safest one.
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Compare All Marketplaces")
    print("=" * 70 + "\n")
    
    with PokemonBotScraper(headless=False, stealth_mode=True) as scraper:
        # Analyze all marketplaces
        results = scraper.analyze_all_marketplaces()
        
        # Find the safest marketplace
        risk_order = ['low', 'medium', 'high', 'critical']
        safest = None
        lowest_risk = 'critical'
        
        for marketplace, data in results.items():
            if 'risk_level' in data:
                if risk_order.index(data['risk_level']) < risk_order.index(lowest_risk):
                    lowest_risk = data['risk_level']
                    safest = marketplace
        
        if safest:
            print(f"\n[✓] Safest marketplace: {safest.upper()}")
            print(f"[*] Risk level: {lowest_risk.upper()}")
        else:
            print("\n[!] Could not determine safest marketplace")


def example_3_custom_url():
    """
    Example 3: Analyze a custom URL and save report.
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Custom URL Analysis with Report")
    print("=" * 70 + "\n")
    
    custom_url = "https://www.tcgplayer.com/"
    
    with PokemonBotScraper(headless=False, stealth_mode=True) as scraper:
        # Analyze the URL
        print(f"[*] Analyzing: {custom_url}")
        results = scraper.conduct_antibot_research(custom_url)
        
        # Generate detailed report
        report = scraper.antibot_detector.generate_report(results)
        
        # Save report to file
        report_filename = 'antibot_report.txt'
        with open(report_filename, 'w') as f:
            f.write(report)
        
        print(f"\n[✓] Detailed report saved to: {report_filename}")


def example_4_check_specific_protections():
    """
    Example 4: Check for specific protection types.
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Check Specific Protection Types")
    print("=" * 70 + "\n")
    
    with PokemonBotScraper(headless=False, stealth_mode=True) as scraper:
        results = scraper.analyze_marketplace('tcgplayer')
        
        if results:
            print("[*] Specific protection checks:")
            print(f"    Cloudflare: {'YES' if results['cloudflare']['detected'] else 'NO'}")
            print(f"    reCAPTCHA: {'YES' if results['recaptcha']['detected'] else 'NO'}")
            print(f"    hCaptcha: {'YES' if results['hcaptcha']['detected'] else 'NO'}")
            print(f"    Bot Scripts: {'YES' if results['bot_detection_scripts']['detected'] else 'NO'}")
            print(f"    Rate Limiting: {'YES' if results['rate_limiting']['detected'] else 'NO'}")
            print(f"    WAF: {'YES' if results['waf_detection']['detected'] else 'NO'}")
            print(f"    Selenium Detection: {'YES' if results['selenium_detection']['detected'] else 'NO'}")


def main():
    """Run all examples."""
    print("=" * 70)
    print("POKEMON BOT SCRAPER - USAGE EXAMPLES")
    print("=" * 70)
    print("\nThese examples demonstrate antibot detection capabilities")
    print("for Pokemon TCG marketplace analysis.\n")
    
    examples = [
        ("Single Marketplace Analysis", example_1_single_marketplace),
        ("Compare All Marketplaces", example_2_compare_marketplaces),
        ("Custom URL with Report", example_3_custom_url),
        ("Check Specific Protections", example_4_check_specific_protections),
    ]
    
    print("Available examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    print("  5. Run all examples")
    print("  6. Exit")
    
    try:
        choice = input("\nSelect an example (1-6): ").strip()
        
        if choice == '1':
            example_1_single_marketplace()
        elif choice == '2':
            example_2_compare_marketplaces()
        elif choice == '3':
            example_3_custom_url()
        elif choice == '4':
            example_4_check_specific_protections()
        elif choice == '5':
            for name, func in examples:
                print(f"\n\n{'=' * 70}")
                print(f"Running: {name}")
                print('=' * 70)
                func()
                input("\nPress Enter to continue to next example...")
        elif choice == '6':
            print("\n[*] Exiting. Goodbye!\n")
        else:
            print("\n[!] Invalid choice. Please run again and select 1-6.")
    
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user. Goodbye!\n")
    except Exception as e:
        print(f"\n[!] Error: {str(e)}\n")


if __name__ == "__main__":
    main()
