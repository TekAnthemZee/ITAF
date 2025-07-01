from setuptools import setup, find_packages
from pathlib import Path

# Read requirements from file
requirements = Path("requirements.txt").read_text().splitlines()

setup(
    name="itaf",
    version="0.1.0",
    description="Intelligent Test Automation Framework (ITAF) with AI agents and Playwright",
    author="Mohammed Azeezulla",
    author_email="azeezulla.m@tekanthem.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
