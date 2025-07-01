#!/usr/bin/env python3
"""
Simple ITAF Template Creator
Creates project structure and empty files
Usage: python template.py
"""

import os
from pathlib import Path

def create_folders():
    """Create folder structure"""
    
    folders = [
        "src/agents",
        "src/tools", 
        "src/crew",
        "src/state",
        "src/strategies",
        "Test_Pages",
        "tests",
        "data",
        "config",
        "reports",
        "logs"
    ]
    
    for folder in folders:
        Path(folder).mkdir(parents=True, exist_ok=True)
        print(f"Created: {folder}")

def create_files():
    """Create empty template files"""
    
    files = [
        "run_pipeline.py",
        "src/crew/crew_setup.py",
        "src/agents/ui_analyzer_agent.py",
        "src/agents/test_generator_agent.py", 
        "src/agents/self_healer_agent.py",
        "src/agents/report_agent.py",
        "src/tools/website_loader_tool.py",
        "src/tools/test_runner_tool.py",
        "src/tools/selector_tool.py",
        "src/state/state_manager.py",
        "src/state/test_history.py",
        "src/state/healing_tracker.py",
        "src/strategies/css_selector_strategy.py",
        "src/strategies/xpath_selector_strategy.py",
        "src/strategies/text_selector_strategy.py",
        "src/strategies/hybrid_selector_strategy.py",
        "tests/conftest.py",
        "tests/test_runner.py"
    ]
    
    for file_path in files:
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch()
        print(f"Created: {file_path}")

if __name__ == "__main__":
    print("Creating ITAF structure...")
    create_folders()
    create_files()
    print("Done!")