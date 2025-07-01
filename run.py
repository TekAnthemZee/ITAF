import argparse
import asyncio
import sys
from pathlib import Path
from src.state.state_manager import StateManager
from src.tools.website_loader_tool import WebsiteLoaderTool

async def main():
    parser = argparse.ArgumentParser(description='Run ITAF Pipeline')
    parser.add_argument('--url', required=True, help='Target website URL')
    parser.add_argument('--depth', type=int, default=1, help='Crawl depth')
    
    args = parser.parse_args()
    
    print(f"Starting ITAF for: {args.url}")
    
    try:
        # Initialize components
        state_manager = StateManager()
        website_loader = WebsiteLoaderTool()
        
        # Load website and capture screenshot
        result = await website_loader.load_and_capture(args.url)
        
        # Save to state
        state_manager.add_page(args.url, result)
        
        print(f"Screenshot saved: {result['screenshot_path']}")
        print(f"Page data saved to state")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())