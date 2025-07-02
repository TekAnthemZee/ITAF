from typing import List, Dict

class HybridStrategy:
    """Hybrid selector generation strategy combining multiple approaches"""
    
    def generate_selectors(self, element_data: Dict) -> List[Dict]:
        """Generate hybrid selectors combining multiple strategies"""
        selectors = []
        
        element_type = element_data.get('type', '').lower()
        text = element_data.get('text', '').strip()
        attributes = element_data.get('attributes', {})
        position = element_data.get('position', '').lower()
        
        # Strategy 1: Combined CSS + text for buttons
        if element_type == 'button' and text:
            selectors.append({
                'selector': f'button:has-text("{text}")',
                'confidence': 0.9,
                'priority': 1,
                'description': 'Hybrid: CSS button with text content'
            })
        
        # Strategy 2: Form field with label association
        if element_type == 'input':
            placeholder = attributes.get('placeholder', '')
            if placeholder:
                # Combine placeholder and type for stronger selector
                input_type = attributes.get('type', 'text')
                selectors.append({
                    'selector': f'input[type="{input_type}"][placeholder="{placeholder}"]',
                    'confidence': 0.95,
                    'priority': 1,
                    'description': 'Hybrid: Input type + placeholder'
                })
        
        # Strategy 3: Position-aware selectors
        if position and text:
            if 'top' in position or 'header' in position:
                selectors.append({
                    'selector': f'header >> text="{text}", nav >> text="{text}"',
                    'confidence': 0.8,
                    'priority': 2,
                    'description': 'Hybrid: Header/nav context with text'
                })
            
            if 'bottom' in position or 'footer' in position:
                selectors.append({
                    'selector': f'footer >> text="{text}"',
                    'confidence': 0.8,
                    'priority': 2,
                    'description': 'Hybrid: Footer context with text'
                })
        
        # Strategy 4: Multi-attribute combination for inputs
        if element_type == 'input':
            conditions = []
            
            input_type = attributes.get('type', '')
            if input_type:
                conditions.append(f'type="{input_type}"')
            
            placeholder = attributes.get('placeholder', '')
            if placeholder:
                conditions.append(f'placeholder*="{placeholder.split()[0]}"')  # First word of placeholder
            
            if len(conditions) >= 2:
                selector_str = f'input[{" and ".join(conditions)}]'
                selectors.append({
                    'selector': selector_str,
                    'confidence': 0.85,
                    'priority': 2,
                    'description': 'Hybrid: Multiple input attributes'
                })
        
        # Strategy 5: Accessibility + visual combination
        if text:
            # Combine visible text with accessibility
            selectors.append({
                'selector': f'[aria-label="{text}"], [title="{text}"], text="{text}"',
                'confidence': 0.8,
                'priority': 2,
                'description': 'Hybrid: Accessibility attributes or text'
            })
        
        # Strategy 6: Form context selectors
        if element_type in ['input', 'button'] and text:
            # Look for form-specific patterns
            if any(keyword in text.lower() for keyword in ['email', 'username', 'login']):
                selectors.append({
                    'selector': f'form >> input[placeholder*="email" i], form >> input[type="email"]',
                    'confidence': 0.85,
                    'priority': 2,
                    'description': 'Hybrid: Form context for email input'
                })
            
            if any(keyword in text.lower() for keyword in ['password', 'pass']):
                selectors.append({
                    'selector': f'form >> input[type="password"]',
                    'confidence': 0.9,
                    'priority': 1,
                    'description': 'Hybrid: Form context for password input'
                })
            
            if any(keyword in text.lower() for keyword in ['submit', 'sign in', 'login']):
                selectors.append({
                    'selector': f'form >> button[type="submit"], form >> input[type="submit"]',
                    'confidence': 0.85,
                    'priority': 2,
                    'description': 'Hybrid: Form context for submit button'
                })
        
        # Strategy 7: Fallback combinations
        if element_type and text:
            # Generic fallback with multiple options
            selectors.append({
                'selector': f'{element_type}:has-text("{text}"), [data-testid*="{text.lower()}"], #{text.lower().replace(" ", "-")}',
                'confidence': 0.6,
                'priority': 4,
                'description': 'Hybrid: Multiple fallback approaches'
            })
        
        # Strategy 8: Link-specific hybrid selectors
        if element_type in ['link', 'a'] and text:
            selectors.append({
                'selector': f'a:has-text("{text}"), [href*="{text.lower().replace(" ", "-")}"]',
                'confidence': 0.8,
                'priority': 2,
                'description': 'Hybrid: Link text or href pattern'
            })
        
        return selectors
    
    def validate_selector(self, selector: str) -> Dict:
        """Validate hybrid selector syntax"""
        try:
            if not selector or not isinstance(selector, str):
                return {'valid': False, 'reason': 'Empty or invalid selector'}
            
            # Check for common hybrid patterns
            if '>>' in selector:
                # Playwright chaining selector
                parts = selector.split('>>')
                if len(parts) < 2:
                    return {'valid': False, 'reason': 'Invalid chaining syntax'}
            
            if ':has-text(' in selector:
                # Check for balanced parentheses in has-text
                has_text_parts = selector.split(':has-text(')
                for part in has_text_parts[1:]:  # Skip first part
                    if ')' not in part:
                        return {'valid': False, 'reason': 'Unbalanced parentheses in has-text'}
            
            # Check for multiple selectors separated by commas
            if ',' in selector:
                sub_selectors = [s.strip() for s in selector.split(',')]
                for sub_selector in sub_selectors:
                    if not sub_selector:
                        return {'valid': False, 'reason': 'Empty sub-selector in comma-separated list'}
            
            return {'valid': True, 'reason': 'Valid hybrid selector'}
            
        except Exception as e:
            return {'valid': False, 'reason': f'Validation error: {str(e)}'}