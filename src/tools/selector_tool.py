import logging
from typing import List, Dict, Optional
from pathlib import Path

class SelectorTool:
    """Multi-strategy selector management tool"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.strategies = self._initialize_strategies()
        
    def _initialize_strategies(self) -> Dict:
        """Initialize all selector strategies"""
        from src.strategies.css_selector_strategy import CSSStrategy
        from src.strategies.xpath_selector_strategy import XPathStrategy
        from src.strategies.text_selector_strategy import TextStrategy
        from src.strategies.hybrid_selector_strategy import HybridStrategy
        
        return {
            'css': CSSStrategy(),
            'xpath': XPathStrategy(),
            'text': TextStrategy(),
            'hybrid': HybridStrategy()
        }
    
    def generate_selectors(self, element_data: Dict) -> List[Dict]:
        """
        Generate multiple selector options for an element
        
        Returns:
        [
            {
                'strategy': 'css',
                'selector': '#button-id',
                'confidence': 0.95,
                'priority': 1
            }
        ]
        """
        selectors = []
        
        # Generate selectors using each strategy
        for strategy_name, strategy in self.strategies.items():
            try:
                strategy_selectors = strategy.generate_selectors(element_data)
                for selector in strategy_selectors:
                    selectors.append({
                        'strategy': strategy_name,
                        'selector': selector['selector'],
                        'confidence': selector.get('confidence', 0.5),
                        'priority': selector.get('priority', 5),
                        'description': selector.get('description', '')
                    })
            except Exception as e:
                self.logger.warning(f"Strategy {strategy_name} failed: {e}")
        
        # Sort by priority and confidence
        selectors.sort(key=lambda x: (x['priority'], -x['confidence']))
        
        return selectors
    
    def validate_selector(self, selector: str, strategy: str) -> Dict:
        """Validate selector syntax and structure"""
        if strategy in self.strategies:
            return self.strategies[strategy].validate_selector(selector)
        
        return {'valid': False, 'reason': 'Unknown strategy'}
    
    def rank_selectors(self, selectors: List[Dict], historical_data: Dict = None) -> List[Dict]:
        """Rank selectors by performance and reliability"""
        if not historical_data:
            # Use default ranking based on confidence and priority
            return sorted(selectors, key=lambda x: (x['priority'], -x['confidence']))
        
        # Apply historical performance data
        for selector in selectors:
            selector_key = f"{selector['strategy']}:{selector['selector']}"
            if selector_key in historical_data:
                hist_data = historical_data[selector_key]
                # Adjust confidence based on historical success rate
                selector['confidence'] *= hist_data.get('success_rate', 0.5)
        
        return sorted(selectors, key=lambda x: -x['confidence'])
    
    def save_selectors_to_page(self, page_name: str, element_selectors: Dict):
        """Save generated selectors to page-specific file"""
        page_folder = Path("Test_Pages") / page_name
        selectors_file = page_folder / f"{page_name}_selectors.json"
        
        import json
        with open(selectors_file, 'w') as f:
            json.dump(element_selectors, f, indent=2)
        
        self.logger.info(f"Selectors saved to: {selectors_file}")