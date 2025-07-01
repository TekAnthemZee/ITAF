#!/usr/bin/env python3
"""
Simple ITAF Template Creator
Creates project structure and empty files
Usage: python template.py
"""

from pathlib import Path

def create_folders():
    """Create full folder structure and __init__.py files"""

    folders = [
        "src/itaf/agents",
        "src/itaf/tools",
        "src/itaf/crew",
        "src/itaf/state",
        "src/itaf/strategies",
        "Test_Pages",
        "tests",
        "data",
        "config",
        "reports",
        "logs"
    ]

    for folder in folders:
        path = Path(folder)
        path.mkdir(parents=True, exist_ok=True)
        print(f"Created: {folder}")

        # Create __init__.py inside every folder (even if not strictly a Python package)
        init_file = path / "__init__.py"
        init_file.touch()
        print(f"Created: {init_file}")

def create_files():
    """Create empty template files"""

    files = [
        "run_pipeline.py",
        "src/itaf/crew/crew_setup.py",
        "src/itaf/agents/ui_analyzer_agent.py",
        "src/itaf/agents/test_generator_agent.py",
        "src/itaf/agents/self_healer_agent.py",
        "src/itaf/agents/report_agent.py",
        "src/itaf/tools/website_loader_tool.py",
        "src/itaf/tools/test_runner_tool.py",
        "src/itaf/tools/selector_tool.py",
        "src/itaf/state/state_manager.py",
        "src/itaf/state/test_history.py",
        "src/itaf/state/healing_tracker.py",
        "src/itaf/strategies/css_selector_strategy.py",
        "src/itaf/strategies/xpath_selector_strategy.py",
        "src/itaf/strategies/text_selector_strategy.py",
        "src/itaf/strategies/hybrid_selector_strategy.py",
        "tests/conftest.py",
        "tests/test_runner.py"
    ]

    for file_path in files:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()
        print(f"Created: {path}")

if __name__ == "__main__":
    print("Creating ITAF structure...")
    create_folders()
    create_files()
    print("Done!")
