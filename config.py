"""
Configuration file for Pokemon Bot Scraper
"""

# Popular Pokemon TCG Marketplaces
MARKETPLACES = {
    'tcgplayer': 'https://www.tcgplayer.com/',
    'cardmarket': 'https://www.cardmarket.com/en/Pokemon',
    'ebay': 'https://www.ebay.com/b/Pokemon-Trading-Card-Game-Cards/183454/bn_2349808',
    'trollandtoad': 'https://www.trollandtoad.com/pokemon/11304',
}

# Browser settings
HEADLESS_MODE = False  # Set to True for headless browsing
BROWSER_TIMEOUT = 10  # seconds
PAGE_LOAD_TIMEOUT = 30  # seconds

# User agent strings for rotation
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
]

# Antibot detection settings
ANTIBOT_CHECK_TIMEOUT = 5  # seconds to wait for antibot checks
