from typing import List, Dict
import re

class XPathStrategy:
    """XPath selector generation strategy"""
    
    def generate_selectors(self, element_data: Dict) -> List[Dict]:
        """Generate XPath selectors for an element"""
        selectors = []
        
        element_type = element_data.get('type', '').lower()
        text = element_data.get('text', '').strip()
        attributes = element_data.get('attributes', {})
        
        # Strategy 1: By exact text content
        if text and element_type in ['button', 'link', 'a', 'span', 'div']:
            selectors.append({
                'selector': f'//{element_type}[text()="{text}"]',
                'confidence': 0.9,
                'priority': 1,
                'description': 'XPath by exact text content'
            })
            
            # Partial text match
            selectors.append({
                'selector': f'//{element_type}[contains(text(), "{text}")]',
                'confidence': 0.8,
                'priority': 2,
                'description': 'XPath by partial text content'
            })
        
        # Strategy 2: By attributes
        if element_type == 'input':
            placeholder = attributes.get('placeholder', '')
            if placeholder:
                selectors.append({
                    'selector': f'//input[@placeholder="{placeholder}"]',
                    'confidence': 0.9,
                    'priority': 1,
                    'description': 'XPath by placeholder attribute'
                })
            
            input_type = attributes.get('type', 'text')
            selectors.append({
                'selector': f'//input[@type="{input_type}"]',
                'confidence': 0.7,
                'priority': 3,
                'description': f'XPath by input type'
            })
        
        # Strategy 3: By common patterns with contains
        if 'email' in text.lower() or 'email' in str(attributes).lower():
            selectors.append({
                'selector': '//input[contains(@placeholder, "email") or contains(@type, "email")]',
                'confidence': 0.85,
                'priority': 2,
                'description': 'XPath by email pattern'
            })
        
        if 'password' in text.lower() or 'password' in str(attributes).lower():
            selectors.append({
                'selector': '//input[@type="password" or contains(@placeholder, "password")]',
                'confidence': 0.85,
                'priority': 2,
                'description': 'XPath by password pattern'
            })
        
        # Strategy 4: By position and element type
        if element_type:
            selectors.append({
                'selector': f'//{element_type}[1]',
                'confidence': 0.4,
                'priority': 6,
                'description': f'XPath first {element_type} element'
            })
        
        # Strategy 5: Complex XPath with multiple conditions
        if text and element_type:
            clean_text = text.replace('"', "'")
            selectors.append({
                'selector': f'//{element_type}[normalize-space(text())="{clean_text}"]',
                'confidence': 0.8,
                'priority': 2,
                'description': 'XPath with normalized text'
            })
        
        # Strategy 6: By aria attributes (accessibility)
        if 'aria-label' in str(attributes).lower() or 'label' in text.lower():
            selectors.append({
                'selector': f'//*[@aria-label="{text}" or contains(@aria-label, "{text}")]',
                'confidence': 0.75,
                'priority': 3,
                'description': 'XPath by aria-label'
            })
        
        return selectors
    
    def validate_selector(self, selector: str) -> Dict:
        """Validate XPath selector syntax"""
        try:
            if not selector or not isinstance(selector, str):
                return {'valid': False, 'reason': 'Empty or invalid selector'}
            
            # Check if starts with // or /
            if not (selector.startswith('//') or selector.startswith('/')):
                return {'valid': False, 'reason': 'XPath must start with / or //'}
            
            # Check for balanced brackets and quotes
            if selector.count('[') != selector.count(']'):
                return {'valid': False, 'reason': 'Unbalanced square brackets'}
            
            if selector.count('(') != selector.count(')'):
                return {'valid': False, 'reason': 'Unbalanced parentheses'}
            
            # Count quotes (both single and double)
            single_quotes = selector.count("'")
            double_quotes = selector.count('"')
            
            if single_quotes % 2 != 0:
                return {'valid': False, 'reason': 'Unbalanced single quotes'}
            
            if double_quotes % 2 != 0:
                return {'valid': False, 'reason': 'Unbalanced double quotes'}
            
            return {'valid': True, 'reason': 'Valid XPath selector'}
            
        except Exception as e:
            return {'valid': False, 'reason': f'Validation error: {str(e)}'}