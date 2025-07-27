"""Setup script for {{project_name}}"""
from setuptools import setup, find_packages

# Read long description from README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="{{project_name}}",
    version="0.1.0",
    author="{{AUTHOR_NAME}}",
    author_email="{{AUTHOR_EMAIL}}",
    description="{{PROJECT_DESCRIPTION}}",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/{{AUTHOR_NAME}}/{{project_name}}",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=[
        # Add your project dependencies here
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=23.0",
            "isort>=5.0",
            "flake8>=6.0",
            "mypy>=1.0",
        ]
    },
    entry_points={
        "console_scripts": [
            # Add command-line scripts here
            # "{{project_name}}={{project_name}}.cli:main",
        ],
    },
)