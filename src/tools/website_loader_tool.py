from playwright.async_api import async_playwright
from typing import Dict, List
from pathlib import Path
from datetime import datetime
import urllib.parse

class WebsiteLoaderTool:
    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None
        
        # Ensure screenshots directory exists
        self.screenshots_dir = Path("reports/screenshots")
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
    
    async def load_and_capture(self, url: str) -> Dict:
        """
        Load website and capture full page screenshot + basic info
        
        Returns:
        {
            'screenshot_path': str,
            'page_title': str,
            'url': str,
            'status_code': int,
            'timestamp': str
        }
        """
        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080}
            )
            page = await context.new_page()
            
            try:
                # Navigate to URL
                response = await page.goto(url, wait_until='networkidle')
                
                # Wait for page to be fully loaded
                await page.wait_for_load_state('domcontentloaded')
                
                # Get page info
                page_title = await page.title()
                
                # Generate screenshot filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                parsed_url = urllib.parse.urlparse(url)
                domain = parsed_url.netloc.replace('.', '_')
                path = parsed_url.path.strip('/').replace('/', '_')
                
                if not path:
                    path = "homepage"
                
                screenshot_filename = f"{domain}_{path}_{timestamp}.png"
                screenshot_path = self.screenshots_dir / screenshot_filename
                
                # Take full page screenshot
                await page.screenshot(
                    path=str(screenshot_path),
                    full_page=True,
                    type='png'
                )
                
                result = {
                    'screenshot_path': str(screenshot_path),
                    'page_title': page_title,
                    'url': url,
                    'status_code': response.status if response else 0,
                    'timestamp': datetime.now().isoformat()
                }
                
                return result
                
            except Exception as e:
                print(f"Error loading {url}: {str(e)}")
                raise
                
            finally:
                await browser.close()
    
    def _sanitize_filename(self, text: str) -> str:
        """Sanitize text for use in filename"""
        # Remove/replace invalid filename characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            text = text.replace(char, '_')
        return text[:50]  # Limit length