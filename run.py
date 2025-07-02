import argparse
import asyncio
import sys
import logging
from pathlib import Path
from datetime import datetime
from src.state.state_manager import StateManager
from src.tools.website_loader_tool import WebsiteLoaderTool
from src.agents.ui_analyzer_agent import UIAnalyzerAgent
from src.tools.selector_tool import SelectorTool

def setup_logging():
    """Setup logging to both file and console"""
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Create log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = logs_dir / f"itaf_{timestamp}.log"
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(__name__)

async def main():
    parser = argparse.ArgumentParser(description='Run ITAF Pipeline')
    parser.add_argument('--url', required=True, help='Target website URL')
    parser.add_argument('--depth', type=int, default=1, help='Crawl depth')
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logging()
    
    logger.info(f"Starting ITAF for: {args.url}")
    
    try:
        # Initialize components
        logger.info("Initializing components...")
        state_manager = StateManager()
        website_loader = WebsiteLoaderTool()
        ui_analyzer = UIAnalyzerAgent()
        selector_tool = SelectorTool()
        
        # Phase 1: Load website and capture screenshot
        logger.info("Phase 1: Loading website and capturing screenshot...")
        result = await website_loader.load_and_capture(args.url)
        
        # Save to state
        logger.info("Saving page data to state...")
        page_name = state_manager.add_page(args.url, result)
        
        logger.info(f"Screenshot saved: {result['screenshot_path']}")
        logger.info(f"Page title: {result['page_title']}")
        logger.info(f"Status code: {result['status_code']}")
        
        # Verify screenshot file exists
        screenshot_path = Path(result['screenshot_path'])
        if screenshot_path.exists():
            file_size = screenshot_path.stat().st_size
            logger.info(f"Screenshot file verified: {file_size} bytes")
        else:
            logger.error(f"Screenshot file not found at: {screenshot_path}")
            return
        
        # Phase 2: UI Analysis with Gemini
        logger.info("Phase 2: Analyzing UI elements with Gemini...")
        ui_analysis = await ui_analyzer.analyze_screenshot(
            result['screenshot_path'], 
            args.url
        )
        
        logger.info(f"UI Analysis completed: {len(ui_analysis['elements'])} elements found")
        logger.info(f"Page structure: {ui_analysis['page_structure']}")
        
        # Generate selectors for each element
        logger.info("Generating selectors for UI elements...")
        all_element_selectors = {}
        
        for i, element in enumerate(ui_analysis['elements']):
            element_id = f"element_{i}_{element.get('type', 'unknown')}"
            selectors = selector_tool.generate_selectors(element)
            all_element_selectors[element_id] = {
                'element_data': element,
                'selectors': selectors
            }
        
        # Save analysis and selectors to page folder
        state_manager.save_ui_analysis(page_name, ui_analysis)
        selector_tool.save_selectors_to_page(page_name, all_element_selectors)
        
        logger.info(f"UI analysis and selectors saved for page: {page_name}")
        logger.info("ITAF Phase 2 completed successfully")
        
        # Summary
        logger.info("=== PHASE 2 SUMMARY ===")
        logger.info(f"Total elements found: {len(ui_analysis['elements'])}")
        logger.info(f"Critical elements: {ui_analysis['page_structure']['critical_elements']}")
        logger.info(f"Element types: {ui_analysis['page_structure']['element_types']}")
        logger.info(f"Page sections: {ui_analysis['page_structure']['sections']}")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())