"""Setup configuration for Banking Transactions API package."""

from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="banking-transactions-api",
    version="1.0.0",
    author="ESG MBA Team",
    description="API for exposing and analyzing banking transaction data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/banking-transactions-api",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
    install_requires=[
        "fastapi==0.109.0",
        "uvicorn[standard]==0.27.0",
        "pydantic==2.5.3",
        "pandas==2.1.4",
        "numpy==1.26.3",
    ],
    extras_require={
        "dev": [
            "pytest==7.4.4",
            "pytest-cov==4.1.0",
            "pytest-asyncio==0.23.3",
            "flake8==7.0.0",
            "mypy==1.8.0",
            "black==24.1.1",
            "types-setuptools==69.0.0.0",
            "pandas-stubs==2.1.4.231227",
        ],
    },
    entry_points={
        "console_scripts": [
            "banking-api=banking_api.app:app",
        ],
    },
)
