# Intelligent Test Automation Framework (ITAF)

An AI-powered test automation framework that uses multiple AI agents (Claude, OpenAI, Gemini) with CrewAI orchestration to automatically generate, execute, heal, and report on web UI tests using Playwright.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git
- Internet connection (for AI API calls)

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/TekAnthemZee/ITAF.git
cd ITAF

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
python -m playwright install
```

### 2. Environment Setup

Create a `.env` file in the root directory:

```bash
# AI API Keys
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_claude_api_key
GOOGLE_API_KEY=your_gemini_api_key

# Optional configurations
PLAYWRIGHT_HEADLESS=true
TEST_TIMEOUT=30000
```

### 3. Create Project Structure

```bash
python template.py
```

### 4. Run the Framework

```bash
python run_pipeline.py --url https://example.com
```

## 📁 Project Structure

```
ITAF/
├── src/itaf/                    # Core framework code
│   ├── agents/                  # AI agent implementations
│   ├── tools/                   # Playwright and utility wrappers
│   ├── crew/                    # CrewAI orchestration
│   ├── state/                   # State management and tracking
│   └── strategies/              # Element selection strategies
├── Test_Pages/                  # Generated test files per page
├── tests/                       # Test configuration and runners
├── data/                        # Test data and fixtures
├── config/                      # Configuration files
├── reports/                     # Generated test reports
├── logs/                        # Execution logs
├── run_pipeline.py              # Main entry point
├── template.py                  # Project structure creator
└── requirements.txt             # Python dependencies
```

## 🤖 AI Agents

### UI Analyzer Agent (`src/itaf/agents/ui_analyzer_agent.py`)
- **Purpose**: Analyzes web page screenshots and DOM structure
- **AI Model**: Gemini Vision API
- **Input**: Full-page screenshot + DOM structure
- **Output**: Structured list of testable UI elements (buttons, forms, links)
- **Key Features**: Visual element detection, accessibility analysis

### Test Generator Agent (`src/itaf/agents/test_generator_agent.py`)
- **Purpose**: Generates Playwright + pytest test scripts
- **AI Model**: Claude API
- **Input**: UI analysis results from analyzer agent
- **Output**: Complete test files with assertions and selectors
- **Key Features**: Best practices implementation, modular test design

### Self-Healer Agent (`src/itaf/agents/self_healer_agent.py`)
- **Purpose**: Fixes broken tests automatically
- **AI Model**: Claude API (with optional Gemini for visual context)
- **Input**: Test failure logs + current page state
- **Output**: Updated test code with fixed selectors
- **Key Features**: Intelligent selector healing, retry logic

### Report Agent (`src/itaf/agents/report_agent.py`)
- **Purpose**: Generates comprehensive test reports
- **AI Model**: OpenAI GPT
- **Input**: Test execution results and screenshots
- **Output**: Markdown/HTML reports with insights
- **Key Features**: Executive summaries, failure analysis, trends

## 🛠️ Tools

### Website Loader Tool (`src/itaf/tools/website_loader_tool.py`)
- **Purpose**: Browser automation and page capture
- **Technology**: Playwright
- **Functions**:
  - Opens URLs in browser
  - Takes full-page screenshots
  - Captures DOM structure
  - Handles dynamic content loading

### Test Runner Tool (`src/itaf/tools/test_runner_tool.py`)
- **Purpose**: Test execution and result collection
- **Technology**: pytest + Playwright
- **Functions**:
  - Executes generated test files
  - Captures pass/fail results
  - Collects error logs and screenshots
  - Provides execution metrics

### Selector Tool (`src/itaf/tools/selector_tool.py`)
- **Purpose**: Element identification and selection
- **Functions**:
  - CSS selector generation
  - XPath creation
  - Text-based selection
  - Selector validation and fallbacks

## 🧠 State Management

### State Manager (`src/itaf/state/state_manager.py`)
- Manages global framework state
- Tracks current execution context
- Handles data persistence

### Test History (`src/itaf/state/test_history.py`)
- Maintains record of all test executions
- Tracks test success/failure patterns
- Provides historical analysis data

### Healing Tracker (`src/itaf/state/healing_tracker.py`)
- Records all healing attempts and outcomes
- Tracks selector reliability metrics
- Optimizes healing strategies over time

## 🎯 Selection Strategies

### CSS Selector Strategy (`src/itaf/strategies/css_selector_strategy.py`)
- Primary selection method using CSS selectors
- Optimized for modern web applications
- Fast execution and broad browser support

### XPath Selector Strategy (`src/itaf/strategies/xpath_selector_strategy.py`)
- Advanced element targeting using XPath
- Useful for complex DOM structures
- Fallback for CSS selector failures

### Text Selector Strategy (`src/itaf/strategies/text_selector_strategy.py`)
- Text-based element identification
- Resilient to DOM structure changes
- Best for user-facing elements

### Hybrid Selector Strategy (`src/itaf/strategies/hybrid_selector_strategy.py`)
- Combines multiple selection methods
- Provides maximum reliability
- Adaptive selection based on element type

## 🔄 Workflow

1. **Load Website**: Playwright opens target URL and captures page state
2. **UI Analysis**: Gemini analyzes screenshot and identifies testable elements
3. **Test Generation**: Claude creates comprehensive test scripts
4. **Test Execution**: pytest runs generated tests with Playwright
5. **Healing (if needed)**: Failed tests are automatically analyzed and fixed
6. **Reporting**: OpenAI generates detailed reports with insights

## 📋 Generated Test Files

- **Location**: `Test_Pages/` directory
- **Naming**: Automatically based on page URL/title
- **Format**: pytest-compatible Python files
- **Features**:
  - Page Object Model implementation
  - Robust selectors with fallbacks
  - Comprehensive assertions
  - Screenshot capture on failure

## 📊 Reports

Generated reports include:
- **Test Coverage**: Elements tested vs. available
- **Success Metrics**: Pass/fail rates and trends
- **Healing Analysis**: Automatic fixes applied
- **Performance Data**: Execution times and bottlenecks
- **Screenshots**: Visual evidence of test execution

## 🔧 Configuration

### Environment Variables
```bash
# Required
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=AIza...

# Optional
PLAYWRIGHT_HEADLESS=true
TEST_TIMEOUT=30000
MAX_RETRIES=3
HEALING_ENABLED=true
REPORT_FORMAT=markdown
```

### Custom Configuration
Edit files in `config/` directory to customize:
- Agent prompts and behavior
- Test generation templates
- Selector preferences
- Report formatting

## 🚀 Usage Examples

### Basic Website Testing
```bash
python run_pipeline.py --url https://example.com
```

### Multiple Pages
```bash
python run_pipeline.py --url https://example.com --depth 2
```

### Custom Configuration
```bash
python run_pipeline.py --url https://example.com --config custom_config.json
```

### Healing Only Mode
```bash
python run_pipeline.py --heal-only --test-file tests/failing_test.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Issues**: GitHub Issues
- **Documentation**: Wiki section
- **Community**: Discussions tab

## 🔮 Roadmap

- [ ] Multi-browser support (Chrome, Firefox, Safari)
- [ ] Visual regression testing
- [ ] API testing integration
- [ ] CI/CD pipeline templates
- [ ] Cloud execution support
- [ ] Real-time collaboration features