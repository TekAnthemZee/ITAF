import os
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
from pathlib import Path

# Load API key from .env
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env")

# Configure Gemini
genai.configure(api_key=api_key)

# Load image
image_path = Path("reports/screenshots/3_218_234_95_6060_dashboard_20250701_170111.png")
if not image_path.exists():
    raise FileNotFoundError(f"{image_path} does not exist!")

image = Image.open(image_path)

# Use the correct multimodal Gemini model
model = genai.GenerativeModel("gemini-2.5-pro")
# Optional: Use gemini-2.5-flash for faster, lighter inference
# model = genai.GenerativeModel("gemini-2.5-flash")

# Your prompt
prompt = """
You are an expert UI test planner for automated web testing. Given a full-page screenshot of a website, extract all actionable UI components with the following details for each:

1. **Type** of element (button, link, input, label, dropdown, checkbox, icon, etc.)
2. **Visible text** or label
3. **Element purpose** (e.g., "submits login form", "opens product page", "toggles visibility")
4. **Recommended selector strategy** (ID, text, placeholder, aria-label, etc.)
5. **Whether the element is critical to navigation or functionality**
6. **Any conditional or interactive behavior** (e.g., opens modal, triggers validation, toggles class)

Also include any UI sections like headers, nav bars, footers, or form blocks.

Output the results in JSON format as a list of objects with keys:
- `type`
- `text`
- `purpose`
- `selector_strategy`
- `critical`
- `behavior`
- `section` (optional)

Only describe what is clearly visible in the screenshot. Do not guess hidden behavior.
"""


# Generate response
response = model.generate_content([prompt, image])

# Print the output
print("\nGemini Vision Response:\n")
print(response.text)
