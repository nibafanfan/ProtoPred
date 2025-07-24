"""Setup configuration for protopred-api package"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="protopred-api",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Python client for the ProtoPRED prediction platform API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/protopred-api",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "pandas>=1.2.0",  # For Excel file handling
        "openpyxl>=3.0.0",  # For Excel file support
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.9",
            "mypy>=0.900",
            "sphinx>=4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "protopred=protopred.cli:main",
        ],
    },
)