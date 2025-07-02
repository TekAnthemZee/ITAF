from typing import List, Dict
import re

class TextStrategy:
    """Text-based selector generation strategy"""
    
    def generate_selectors(self, element_data: Dict) -> List[Dict]:
        """Generate text-based selectors for an element"""
        selectors = []
        
        element_type = element_data.get('type', '').lower()
        text = element_data.get('text', '').strip()
        attributes = element_data.get('attributes', {})
        
        # Strategy 1: By exact text (Playwright text selector)
        if text:
            selectors.append({
                'selector': f'text="{text}"',
                'confidence': 0.9,
                'priority': 1,
                'description': 'Playwright exact text selector'
            })
            
            # Partial text match
            if len(text) > 5:  # Only for longer text
                selectors.append({
                    'selector': f'text="{text[:10]}..."',
                    'confidence': 0.7,
                    'priority': 3,
                    'description': 'Playwright partial text selector'
                })
        
        # Strategy 2: By placeholder text (for inputs)
        placeholder = attributes.get('placeholder', '')
        if placeholder and element_type == 'input':
            selectors.append({
                'selector': f'placeholder="{placeholder}"',
                'confidence': 0.9,
                'priority': 1,
                'description': 'Playwright placeholder selector'
            })
        
        # Strategy 3: By label text (for form inputs)
        if element_type == 'input' and text:
            # Assume text might be a label
            selectors.append({
                'selector': f'label="{text}"',
                'confidence': 0.8,
                'priority': 2,
                'description': 'Playwright label selector'
            })
        
        # Strategy 4: By button or link text
        if element_type in ['button', 'link', 'a'] and text:
            # Case-insensitive text matching
            selectors.append({
                'selector': f'text="{text}" >> visible=true',
                'confidence': 0.85,
                'priority': 2,
                'description': 'Playwright visible text selector'
            })
        
        # Strategy 5: By role and accessible name
        if text:
            role_mapping = {
                'button': 'button',
                'link': 'link',
                'input': 'textbox',
                'checkbox': 'checkbox',
                'select': 'combobox'
            }
            
            role = role_mapping.get(element_type, 'generic')
            selectors.append({
                'selector': f'role={role}[name="{text}"]',
                'confidence': 0.8,
                'priority': 2,
                'description': f'Playwright role selector with name'
            })
        
        # Strategy 6: Text pattern matching for common UI elements
        if 'sign in' in text.lower() or 'login' in text.lower():
            selectors.append({
                'selector': 'text=/sign.?in|login/i',
                'confidence': 0.75,
                'priority': 3,
                'description': 'Text pattern for sign in/login'
            })
        
        if 'submit' in text.lower() or 'send' in text.lower():
            selectors.append({
                'selector': 'text=/submit|send/i',
                'confidence': 0.7,
                'priority': 4,
                'description': 'Text pattern for submit actions'
            })
        
        # Strategy 7: By accessibility attributes
        if 'email' in text.lower() or 'email' in str(attributes).lower():
            selectors.append({
                'selector': 'input[type="email"], [placeholder*="email" i]',
                'confidence': 0.8,
                'priority': 2,
                'description': 'Email input pattern'
            })
        
        if 'password' in text.lower() or 'password' in str(attributes).lower():
            selectors.append({
                'selector': 'input[type="password"], [placeholder*="password" i]',
                'confidence': 0.8,
                'priority': 2,
                'description': 'Password input pattern'
            })
        
        return selectors
    
    def validate_selector(self, selector: str) -> Dict:
        """Validate text-based selector syntax"""
        try:
            if not selector or not isinstance(selector, str):
                return {'valid': False, 'reason': 'Empty or invalid selector'}
            
            # Check for Playwright text selector patterns
            playwright_patterns = ['text=', 'placeholder=', 'label=', 'role=']
            
            is_playwright_selector = any(selector.startswith(pattern) for pattern in playwright_patterns)
            
            if is_playwright_selector:
                # Validate Playwright selector format
                if 'text=' in selector:
                    # Check for balanced quotes in text selector
                    text_part = selector.split('text=')[1]
                    if text_part.startswith('"') and not text_part.endswith('"'):
                        return {'valid': False, 'reason': 'Unbalanced quotes in text selector'}
                
                return {'valid': True, 'reason': 'Valid Playwright text selector'}
            
            # For regex patterns
            if selector.startswith('text=/') and selector.endswith('/i'):
                return {'valid': True, 'reason': 'Valid regex text pattern'}
            
            return {'valid': True, 'reason': 'Valid text-based selector'}
            
        except Exception as e:
            return {'valid': False, 'reason': f'Validation error: {str(e)}'}