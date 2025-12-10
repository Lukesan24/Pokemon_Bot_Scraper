"""
Antibot Detection Module

This module provides fast research capabilities to identify potential antibot measures
that marketplaces may have implemented. It detects common bot protection services and
techniques before attempting any automated purchasing.
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from typing import Dict, List, Optional


class AntibotDetector:
    """
    Detects antibot measures on e-commerce websites.
    
    This class performs fast reconnaissance to identify:
    - Cloudflare protection
    - reCAPTCHA challenges
    - hCaptcha challenges
    - Rate limiting
    - JavaScript challenges
    - WAF (Web Application Firewall) detection
    - Bot detection scripts
    """
    
    def __init__(self, driver: webdriver.Chrome):
        """
        Initialize the antibot detector.
        
        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.detection_results = {}
        
    def detect_all_measures(self, url: str, timeout: int = 5) -> Dict[str, any]:
        """
        Perform comprehensive antibot detection on a given URL.
        
        Args:
            url: The marketplace URL to analyze
            timeout: Maximum time to wait for page elements (seconds)
            
        Returns:
            Dictionary containing detection results for all antibot measures
        """
        print(f"\n[*] Analyzing antibot measures for: {url}")
        print("=" * 70)
        
        try:
            self.driver.get(url)
            time.sleep(2)  # Allow initial page load
            
            results = {
                'url': url,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'cloudflare': self._detect_cloudflare(),
                'recaptcha': self._detect_recaptcha(),
                'hcaptcha': self._detect_hcaptcha(),
                'javascript_challenge': self._detect_js_challenge(),
                'bot_detection_scripts': self._detect_bot_scripts(),
                'rate_limiting': self._detect_rate_limiting(),
                'waf_detection': self._detect_waf(),
                'selenium_detection': self._detect_selenium_detection(),
                'risk_level': 'unknown'
            }
            
            # Calculate overall risk level
            results['risk_level'] = self._calculate_risk_level(results)
            
            self._print_results(results)
            return results
            
        except Exception as e:
            print(f"[!] Error during detection: {str(e)}")
            return {
                'url': url,
                'error': str(e),
                'risk_level': 'unknown'
            }
    
    def _detect_cloudflare(self) -> Dict[str, any]:
        """Detect Cloudflare protection."""
        indicators = {
            'detected': False,
            'type': None,
            'indicators': []
        }
        
        try:
            # Check for Cloudflare challenge page
            page_source = self.driver.page_source.lower()
            
            if 'cloudflare' in page_source:
                indicators['detected'] = True
                indicators['indicators'].append('Cloudflare mentioned in page source')
            
            # Check for Cloudflare challenge elements
            cf_selectors = [
                "//div[@id='cf-wrapper']",
                "//div[@class='cf-browser-verification']",
                "//*[contains(@class, 'cf-challenge')]",
                "//*[contains(text(), 'Checking your browser')]",
                "//*[contains(text(), 'Just a moment')]"
            ]
            
            for selector in cf_selectors:
                try:
                    element = self.driver.find_element(By.XPATH, selector)
                    if element:
                        indicators['detected'] = True
                        indicators['type'] = 'Challenge Page'
                        indicators['indicators'].append(f'Found element: {selector}')
                        break
                except NoSuchElementException:
                    continue
            
            # Check for Cloudflare cookies
            cookies = self.driver.get_cookies()
            cf_cookies = [c for c in cookies if 'cf_' in c.get('name', '').lower() or 'cloudflare' in c.get('name', '').lower()]
            if cf_cookies:
                indicators['detected'] = True
                indicators['type'] = 'Cookie-based'
                indicators['indicators'].append(f'Cloudflare cookies found: {[c["name"] for c in cf_cookies]}')
                
        except Exception as e:
            indicators['error'] = str(e)
        
        return indicators
    
    def _detect_recaptcha(self) -> Dict[str, any]:
        """Detect Google reCAPTCHA."""
        indicators = {
            'detected': False,
            'version': None,
            'indicators': []
        }
        
        try:
            page_source = self.driver.page_source.lower()
            
            # Check for reCAPTCHA v2
            if 'g-recaptcha' in page_source or 'recaptcha' in page_source:
                indicators['detected'] = True
                indicators['indicators'].append('reCAPTCHA reference in page source')
            
            # Look for reCAPTCHA iframes
            recaptcha_selectors = [
                "//iframe[contains(@src, 'recaptcha')]",
                "//div[@class='g-recaptcha']",
                "//*[@data-sitekey]",
                "//script[contains(@src, 'recaptcha')]"
            ]
            
            for selector in recaptcha_selectors:
                try:
                    element = self.driver.find_element(By.XPATH, selector)
                    if element:
                        indicators['detected'] = True
                        indicators['version'] = 'v2 or v3'
                        indicators['indicators'].append(f'Found element: {selector}')
                        break
                except NoSuchElementException:
                    continue
                    
        except Exception as e:
            indicators['error'] = str(e)
        
        return indicators
    
    def _detect_hcaptcha(self) -> Dict[str, any]:
        """Detect hCaptcha."""
        indicators = {
            'detected': False,
            'indicators': []
        }
        
        try:
            page_source = self.driver.page_source.lower()
            
            if 'hcaptcha' in page_source:
                indicators['detected'] = True
                indicators['indicators'].append('hCaptcha reference in page source')
            
            # Look for hCaptcha iframes
            hcaptcha_selectors = [
                "//iframe[contains(@src, 'hcaptcha')]",
                "//div[@class='h-captcha']",
                "//script[contains(@src, 'hcaptcha')]"
            ]
            
            for selector in hcaptcha_selectors:
                try:
                    element = self.driver.find_element(By.XPATH, selector)
                    if element:
                        indicators['detected'] = True
                        indicators['indicators'].append(f'Found element: {selector}')
                        break
                except NoSuchElementException:
                    continue
                    
        except Exception as e:
            indicators['error'] = str(e)
        
        return indicators
    
    def _detect_js_challenge(self) -> Dict[str, any]:
        """Detect JavaScript challenges."""
        indicators = {
            'detected': False,
            'indicators': []
        }
        
        try:
            # Check if JavaScript is being evaluated for bot detection
            js_check_script = """
                return {
                    webdriver: navigator.webdriver,
                    plugins: navigator.plugins.length,
                    languages: navigator.languages,
                    platform: navigator.platform
                };
            """
            
            result = self.driver.execute_script(js_check_script)
            
            if result.get('webdriver'):
                indicators['detected'] = True
                indicators['indicators'].append('WebDriver flag is exposed (navigator.webdriver = true)')
            
            if result.get('plugins') == 0:
                indicators['detected'] = True
                indicators['indicators'].append('No plugins detected (suspicious for real browser)')
            
            # Check for common anti-automation JS patterns
            page_source = self.driver.page_source.lower()
            js_patterns = [
                'navigator.webdriver',
                'phantom',
                'selenium',
                'bot detection',
                'antibot'
            ]
            
            for pattern in js_patterns:
                if pattern in page_source:
                    indicators['detected'] = True
                    indicators['indicators'].append(f'Pattern found in source: {pattern}')
                    
        except Exception as e:
            indicators['error'] = str(e)
        
        return indicators
    
    def _detect_bot_scripts(self) -> Dict[str, any]:
        """Detect known bot detection scripts."""
        indicators = {
            'detected': False,
            'scripts': [],
            'indicators': []
        }
        
        try:
            page_source = self.driver.page_source.lower()
            
            # Common bot detection services
            bot_services = [
                'datadome',
                'perimetrix',
                'distil',
                'shapesecurity',
                'kasada',
                'akamai',
                'imperva',
                'px-captcha',
                'perimeterx'
            ]
            
            for service in bot_services:
                if service in page_source:
                    indicators['detected'] = True
                    indicators['scripts'].append(service)
                    indicators['indicators'].append(f'Bot detection service found: {service}')
            
            # Check for suspicious script tags
            try:
                scripts = self.driver.find_elements(By.TAG_NAME, 'script')
                for script in scripts[:20]:  # Limit to first 20 scripts
                    src = script.get_attribute('src')
                    if src:
                        src_lower = src.lower()
                        for service in bot_services:
                            if service in src_lower:
                                indicators['detected'] = True
                                indicators['scripts'].append(service)
                                indicators['indicators'].append(f'Script src contains: {service}')
            except Exception:
                pass
                
        except Exception as e:
            indicators['error'] = str(e)
        
        return indicators
    
    def _detect_rate_limiting(self) -> Dict[str, any]:
        """Detect rate limiting indicators."""
        indicators = {
            'detected': False,
            'indicators': []
        }
        
        try:
            page_source = self.driver.page_source.lower()
            
            # Check for rate limit messages
            rate_limit_patterns = [
                'rate limit',
                'too many requests',
                'slow down',
                '429',
                'request limit exceeded',
                'temporarily blocked'
            ]
            
            for pattern in rate_limit_patterns:
                if pattern in page_source:
                    indicators['detected'] = True
                    indicators['indicators'].append(f'Rate limiting message found: {pattern}')
            
            # Check HTTP response (this would require additional implementation)
            # For now, we'll check the page title and content
            title = self.driver.title.lower()
            if 'error' in title or 'blocked' in title or '429' in title:
                indicators['detected'] = True
                indicators['indicators'].append(f'Suspicious page title: {self.driver.title}')
                
        except Exception as e:
            indicators['error'] = str(e)
        
        return indicators
    
    def _detect_waf(self) -> Dict[str, any]:
        """Detect Web Application Firewall."""
        indicators = {
            'detected': False,
            'type': None,
            'indicators': []
        }
        
        try:
            page_source = self.driver.page_source.lower()
            
            # Common WAF signatures
            waf_signatures = {
                'cloudflare': ['cloudflare', 'cf-ray'],
                'akamai': ['akamai', 'akam'],
                'imperva': ['imperva', 'incapsula'],
                'f5': ['f5', 'bigip'],
                'aws': ['aws waf', 'x-amzn'],
                'sucuri': ['sucuri']
            }
            
            for waf_type, signatures in waf_signatures.items():
                for sig in signatures:
                    if sig in page_source:
                        indicators['detected'] = True
                        indicators['type'] = waf_type.upper()
                        indicators['indicators'].append(f'WAF signature found: {sig}')
                        break
                if indicators['detected']:
                    break
            
            # Check response headers (through page source or JavaScript)
            headers_script = """
                var req = new XMLHttpRequest();
                req.open('GET', window.location.href, false);
                req.send(null);
                return req.getAllResponseHeaders();
            """
            
            try:
                headers = self.driver.execute_script(headers_script)
                if headers:
                    headers_lower = headers.lower()
                    for waf_type, signatures in waf_signatures.items():
                        for sig in signatures:
                            if sig in headers_lower:
                                indicators['detected'] = True
                                indicators['type'] = waf_type.upper()
                                indicators['indicators'].append(f'WAF header found: {sig}')
                                break
            except Exception:
                pass
                
        except Exception as e:
            indicators['error'] = str(e)
        
        return indicators
    
    def _detect_selenium_detection(self) -> Dict[str, any]:
        """Detect if the site is checking for Selenium/WebDriver."""
        indicators = {
            'detected': False,
            'indicators': []
        }
        
        try:
            # Run various detection checks
            detection_script = """
                var indicators = [];
                
                // Check for webdriver property
                if (navigator.webdriver) {
                    indicators.push('navigator.webdriver is true');
                }
                
                // Check for common automation properties
                if (window.document.documentElement.getAttribute("webdriver")) {
                    indicators.push('webdriver attribute present');
                }
                
                // Check for phantom/selenium artifacts
                if (window._phantom || window.callPhantom) {
                    indicators.push('PhantomJS detected');
                }
                
                if (window._selenium || document.$cdc_asdjflasutopfhvcZLmcfl_) {
                    indicators.push('Selenium artifacts detected');
                }
                
                // Check Chrome-specific indicators
                if (window.chrome && !window.chrome.runtime) {
                    indicators.push('Chrome runtime missing (suspicious)');
                }
                
                // Check for missing plugins
                if (navigator.plugins.length === 0) {
                    indicators.push('No plugins detected');
                }
                
                // Check permissions
                try {
                    var permissions = navigator.permissions;
                    if (!permissions) {
                        indicators.push('Permissions API unavailable');
                    }
                } catch(e) {}
                
                return indicators;
            """
            
            detected_indicators = self.driver.execute_script(detection_script)
            
            if detected_indicators:
                indicators['detected'] = True
                indicators['indicators'] = detected_indicators
                
        except Exception as e:
            indicators['error'] = str(e)
        
        return indicators
    
    def _calculate_risk_level(self, results: Dict) -> str:
        """
        Calculate overall risk level based on detection results.
        
        Args:
            results: Dictionary of detection results
            
        Returns:
            Risk level string: 'low', 'medium', 'high', or 'critical'
        """
        risk_score = 0
        
        # Assign weights to different protections
        if results['cloudflare']['detected']:
            risk_score += 3
        if results['recaptcha']['detected']:
            risk_score += 3
        if results['hcaptcha']['detected']:
            risk_score += 3
        if results['javascript_challenge']['detected']:
            risk_score += 2
        if results['bot_detection_scripts']['detected']:
            risk_score += 4
        if results['rate_limiting']['detected']:
            risk_score += 2
        if results['waf_detection']['detected']:
            risk_score += 2
        if results['selenium_detection']['detected']:
            risk_score += 3
        
        # Determine risk level
        if risk_score == 0:
            return 'low'
        elif risk_score <= 4:
            return 'medium'
        elif risk_score <= 8:
            return 'high'
        else:
            return 'critical'
    
    def _print_results(self, results: Dict):
        """Print formatted detection results."""
        print(f"\n{'=' * 70}")
        print(f"ANTIBOT DETECTION RESULTS")
        print(f"{'=' * 70}")
        print(f"URL: {results['url']}")
        print(f"Timestamp: {results['timestamp']}")
        print(f"Risk Level: {results['risk_level'].upper()}")
        print(f"{'=' * 70}\n")
        
        measures = [
            ('Cloudflare Protection', results['cloudflare']),
            ('reCAPTCHA', results['recaptcha']),
            ('hCaptcha', results['hcaptcha']),
            ('JavaScript Challenge', results['javascript_challenge']),
            ('Bot Detection Scripts', results['bot_detection_scripts']),
            ('Rate Limiting', results['rate_limiting']),
            ('WAF Detection', results['waf_detection']),
            ('Selenium Detection', results['selenium_detection']),
        ]
        
        for name, data in measures:
            detected = data.get('detected', False)
            status = '✓ DETECTED' if detected else '✗ Not detected'
            print(f"{name:.<40} {status}")
            
            if detected and data.get('indicators'):
                for indicator in data['indicators'][:3]:  # Show first 3 indicators
                    print(f"    → {indicator}")
            
            if data.get('error'):
                print(f"    ! Error: {data['error']}")
            print()
        
        print(f"{'=' * 70}\n")
    
    def generate_report(self, results: Dict) -> str:
        """
        Generate a detailed text report of antibot measures.
        
        Args:
            results: Detection results dictionary
            
        Returns:
            Formatted report string
        """
        report_lines = [
            "=" * 70,
            "ANTIBOT DETECTION REPORT",
            "=" * 70,
            f"URL: {results['url']}",
            f"Timestamp: {results['timestamp']}",
            f"Overall Risk Level: {results['risk_level'].upper()}",
            "=" * 70,
            "",
            "DETECTED MEASURES:",
            ""
        ]
        
        for key, value in results.items():
            if key in ['url', 'timestamp', 'risk_level']:
                continue
                
            if isinstance(value, dict) and value.get('detected'):
                report_lines.append(f"• {key.replace('_', ' ').title()}")
                if value.get('indicators'):
                    for indicator in value['indicators']:
                        report_lines.append(f"  - {indicator}")
                report_lines.append("")
        
        report_lines.extend([
            "=" * 70,
            "RECOMMENDATIONS:",
            ""
        ])
        
        if results['risk_level'] == 'low':
            report_lines.append("• Site appears to have minimal bot protection")
            report_lines.append("• Standard Selenium automation should work")
        elif results['risk_level'] == 'medium':
            report_lines.append("• Some bot protection detected")
            report_lines.append("• Consider using stealth techniques and delays")
        elif results['risk_level'] == 'high':
            report_lines.append("• Significant bot protection in place")
            report_lines.append("• Use undetected-chromedriver or similar tools")
            report_lines.append("• Implement human-like behavior patterns")
        else:  # critical
            report_lines.append("• Heavy bot protection detected")
            report_lines.append("• Automation may be very difficult")
            report_lines.append("• Consider manual approaches or advanced bypass techniques")
        
        report_lines.append("")
        report_lines.append("=" * 70)
        
        return "\n".join(report_lines)
