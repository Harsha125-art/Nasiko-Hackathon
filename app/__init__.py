"""
Docstring Generation Agent Package

An advanced AI-powered tool for automatically generating comprehensive
docstrings for Python code with intelligent analysis and quality metrics.

Features:
- Multi-style docstring generation (Google, NumPy, Sphinx)
- Code complexity analysis
- Type hint inference
- Quality scoring system
- Best practice recommendations
- Interactive and batch processing modes
"""

__version__ = '1.0.0'
__author__ = 'Docstring Agent Team'

from app.agents import DocstringAgent
from app.config import Config
from app.models import DocstringStyle, OutputFormat

__all__ = [
    'DocstringAgent',
    'Config',
    'DocstringStyle',
    'OutputFormat',
]
