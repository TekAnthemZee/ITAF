from typing import List, Dict

class HybridStrategy:
    """Hybrid selector generation strategy combining multiple approaches"""
    
    def generate_selectors(self, element_data: Dict) -> List[Dict]:
        """Generate hybrid selectors combining multiple strategies"""
        selectors = []
        
        # Safe extraction with None checks
        element_type = ''
        text = ''
        attributes = {}
        position = ''
        
        try:
            if element_data.get('type'):
                element_type = str(element_data.get('type', '')).lower()
            
            if element_data.get('text'):
                text = str(element_data.get('text', '')).strip()
            
            if element_data.get('attributes'):
                attributes = element_data.get('attributes', {})
                if not isinstance(attributes, dict):
                    attributes = {}
            
            if element_data.get('position'):
                position = str(element_data.get('position', '')).lower()
                
        except Exception:
            # If any extraction fails, use empty defaults
            element_type = ''
            text = ''
            attributes = {}
            position = ''
        
        # Strategy 1: Combined CSS + text for buttons
        if element_type == 'button' and text:
            selectors.append({
                'selector': f'button:has-text("{text}")',
                'confidence': 0.9,
                'priority': 1,
                'description': 'Hybrid: CSS button with text content'
            })
        
        # Strategy 2: Form field with label association
        if element_type == 'input' and isinstance(attributes, dict):
            placeholder = attributes.get('placeholder', '') if attributes else ''
            if placeholder:
                # Combine placeholder and type for stronger selector
                input_type = attributes.get('type', 'text') if attributes else 'text'
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
        if element_type == 'input' and isinstance(attributes, dict):
            conditions = []
            
            input_type = attributes.get('type', '') if attributes else ''
            if input_type:
                conditions.append(f'type="{input_type}"')
            
            placeholder = attributes.get('placeholder', '') if attributes else ''
            if placeholder:
                try:
                    first_word = placeholder.split()[0] if placeholder.split() else placeholder
                    conditions.append(f'placeholder*="{first_word}"')
                except Exception:
                    conditions.append(f'placeholder*="{placeholder}"')
            
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
            selectors.append({
                'selector': f'[aria-label="{text}"], [title="{text}"], text="{text}"',
                'confidence': 0.8,
                'priority': 2,
                'description': 'Hybrid: Accessibility attributes or text'
            })
        
        # Strategy 6: Form context selectors
        if element_type in ['input', 'button']:
            # Look for form-specific patterns
            if text and any(keyword in text.lower() for keyword in ['email', 'username', 'login']):
                selectors.append({
                    'selector': 'form >> input[placeholder*="email" i], form >> input[type="email"]',
                    'confidence': 0.85,
                    'priority': 2,
                    'description': 'Hybrid: Form context for email input'
                })
            
            if text and any(keyword in text.lower() for keyword in ['password', 'pass']):
                selectors.append({
                    'selector': 'form >> input[type="password"]',
                    'confidence': 0.9,
                    'priority': 1,
                    'description': 'Hybrid: Form context for password input'
                })
            
            if text and any(keyword in text.lower() for keyword in ['submit', 'sign in', 'login']):
                selectors.append({
                    'selector': 'form >> button[type="submit"], form >> input[type="submit"]',
                    'confidence': 0.85,
                    'priority': 2,
                    'description': 'Hybrid: Form context for submit button'
                })
        
        # Strategy 7: Fallback combinations
        if element_type and text:
            try:
                clean_text = text.lower().replace(" ", "-")
                selectors.append({
                    'selector': f'{element_type}:has-text("{text}"), [data-testid*="{clean_text}"], #{clean_text}',
                    'confidence': 0.6,
                    'priority': 4,
                    'description': 'Hybrid: Multiple fallback approaches'
                })
            except Exception:
                pass
        
        # Strategy 8: Link-specific hybrid selectors
        if element_type in ['link', 'a'] and text:
            try:
                clean_text = text.lower().replace(" ", "-")
                selectors.append({
                    'selector': f'a:has-text("{text}"), [href*="{clean_text}"]',
                    'confidence': 0.8,
                    'priority': 2,
                    'description': 'Hybrid: Link text or href pattern'
                })
            except Exception:
                pass
        
        # Always provide a fallback selector
        if not selectors:
            selectors.append({
                'selector': f'{element_type or "*"}',
                'confidence': 0.1,
                'priority': 10,
                'description': 'Hybrid fallback selector'
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