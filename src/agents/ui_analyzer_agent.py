import os
import json
import logging
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
from pathlib import Path
from typing import Dict, List

class UIAnalyzerAgent:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._setup_gemini()
        
    def _setup_gemini(self):
        """Setup Gemini API"""
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in .env file")
            
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-pro")
        self.logger.info("Gemini API configured successfully")
    
    async def analyze_screenshot(self, screenshot_path: str, url: str) -> Dict:
        """
        Analyze screenshot to identify UI elements
        
        Returns:
        {
            'elements': [...],
            'page_structure': {...},
            'analysis_timestamp': str
        }
        """
        try:
            self.logger.info(f"Starting UI analysis for: {screenshot_path}")
            
            # Load image
            image_path = Path(screenshot_path)
            if not image_path.exists():
                raise FileNotFoundError(f"Screenshot not found: {screenshot_path}")
            
            image = Image.open(image_path)
            self.logger.info(f"Image loaded: {image.size}")
            
            # Generate analysis
            prompt = self._build_analysis_prompt(url)
            response = self.model.generate_content([prompt, image])
            
            # Parse response
            elements_data = self._parse_gemini_response(response.text)
            
            result = {
                'elements': elements_data,
                'page_structure': self._extract_page_structure(elements_data),
                'analysis_timestamp': self._get_timestamp(),
                'url': url,
                'screenshot_path': screenshot_path
            }
            
            self.logger.info(f"Analysis completed: {len(elements_data)} elements found")
            return result
            
        except Exception as e:
            self.logger.error(f"UI analysis failed: {str(e)}")
            raise
    
    def _build_analysis_prompt(self, url: str) -> str:
        """Build comprehensive prompt for UI analysis"""
        return f"""
You are an expert UI test planner for automated web testing. Given a full-page screenshot of website: {url}

Extract all actionable UI components with the following details for each:

1. **Type** of element (button, link, input, label, dropdown, checkbox, icon, image, text, etc.)
2. **Visible text** or label (exact text shown)
3. **Element purpose** (e.g., "submits login form", "opens product page", "toggles visibility")
4. **Recommended selector strategy** (ID, class, text, placeholder, aria-label, xpath, etc.)
5. **Whether the element is critical** to navigation or functionality (true/false)
6. **Interactive behavior** (click, input, hover, etc.)
7. **Position** (top, middle, bottom, left, right, center)
8. **Element attributes** (placeholder text, required fields, etc.)

Also identify UI sections like headers, nav bars, footers, forms, modals.

Output ONLY valid JSON format as a list of objects with keys:
- `type`
- `text` 
- `purpose`
- `selector_strategy`
- `critical`
- `behavior`
- `position`
- `attributes`
- `section`

Only describe what is clearly visible in the screenshot. Be thorough and precise.
        """
    
    def _parse_gemini_response(self, response_text: str) -> List[Dict]:
        """Parse Gemini response into structured data"""
        try:
            # Clean response text - remove markdown formatting
            cleaned_text = response_text.strip()
            if cleaned_text.startswith('```json'):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.endswith('```'):
                cleaned_text = cleaned_text[:-3]
            
            # Parse JSON
            elements = json.loads(cleaned_text)
            
            if isinstance(elements, list):
                return elements
            else:
                self.logger.warning("Gemini response is not a list, wrapping in list")
                return [elements]
                
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse Gemini response as JSON: {e}")
            # Return basic structure if parsing fails
            return [{
                'type': 'parsing_error',
                'text': 'Failed to parse Gemini response',
                'purpose': 'Error handling',
                'selector_strategy': 'manual',
                'critical': False,
                'behavior': 'none',
                'position': 'unknown',
                'attributes': {},
                'section': 'error'
            }]
    
    def _extract_page_structure(self, elements: List[Dict]) -> Dict:
        """Extract overall page structure from elements"""
        sections = {}
        element_types = {}
        
        for element in elements:
            # Count sections
            section = element.get('section', 'main')
            sections[section] = sections.get(section, 0) + 1
            
            # Count element types
            elem_type = element.get('type', 'unknown')
            element_types[elem_type] = element_types.get(elem_type, 0) + 1
        
        return {
            'sections': sections,
            'element_types': element_types,
            'total_elements': len(elements),
            'critical_elements': len([e for e in elements if e.get('critical', False)])
        }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()