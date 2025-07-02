from typing import List, Dict
import re

class CSSStrategy:
    """CSS selector generation strategy"""
    
    def generate_selectors(self, element_data: Dict) -> List[Dict]:
        """Generate CSS selectors for an element"""
        selectors = []
        
        element_type = element_data.get('type', '').lower()
        text = element_data.get('text', '').strip()
        attributes = element_data.get('attributes', {})
        
        # Strategy 1: By element type and text
        if text and element_type in ['button', 'link', 'a']:
            selectors.append({
                'selector': f'{element_type}:contains("{text}")',
                'confidence': 0.8,
                'priority': 2,
                'description': f'CSS by element type and text content'
            })
        
        # Strategy 2: By input attributes
        if element_type == 'input':
            placeholder = attributes.get('placeholder', '')
            if placeholder:
                selectors.append({
                    'selector': f'input[placeholder="{placeholder}"]',
                    'confidence': 0.9,
                    'priority': 1,
                    'description': 'CSS by placeholder attribute'
                })
            
            # By input type
            input_type = attributes.get('type', 'text')
            selectors.append({
                'selector': f'input[type="{input_type}"]',
                'confidence': 0.6,
                'priority': 4,
                'description': f'CSS by input type'
            })
        
        # Strategy 3: By common patterns
        if 'email' in text.lower() or 'email' in str(attributes).lower():
            selectors.append({
                'selector': 'input[type="email"], input[placeholder*="email" i]',
                'confidence': 0.85,
                'priority': 2,
                'description': 'CSS by email pattern'
            })
        
        if 'password' in text.lower() or 'password' in str(attributes).lower():
            selectors.append({
                'selector': 'input[type="password"], input[placeholder*="password" i]',
                'confidence': 0.85,
                'priority': 2,
                'description': 'CSS by password pattern'
            })
        
        # Strategy 4: By button text
        if element_type == 'button' and text:
            # Clean text for selector
            clean_text = re.sub(r'[^\w\s]', '', text).strip()
            selectors.append({
                'selector': f'button:contains("{clean_text}")',
                'confidence': 0.75,
                'priority': 3,
                'description': 'CSS by button text'
            })
        
        # Strategy 5: Generic fallbacks
        if element_type:
            selectors.append({
                'selector': element_type,
                'confidence': 0.3,
                'priority': 8,
                'description': f'CSS by element type only'
            })
        
        return selectors
    
    def validate_selector(self, selector: str) -> Dict:
        """Validate CSS selector syntax"""
        try:
            # Basic validation - check for common CSS selector patterns
            if not selector or not isinstance(selector, str):
                return {'valid': False, 'reason': 'Empty or invalid selector'}
            
            # Check for balanced brackets and quotes
            if selector.count('[') != selector.count(']'):
                return {'valid': False, 'reason': 'Unbalanced square brackets'}
            
            if selector.count('"') % 2 != 0:
                return {'valid': False, 'reason': 'Unbalanced quotes'}
            
            return {'valid': True, 'reason': 'Valid CSS selector'}
            
        except Exception as e:
            return {'valid': False, 'reason': f'Validation error: {str(e)}'}