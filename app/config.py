"""
Configuration module for Docstring Generation Agent.

This module manages all configuration settings including docstring styles,
output formats, quality thresholds, and agent behavior.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from app.models import DocstringStyle, OutputFormat
import os
from dotenv import load_dotenv

# ... (keep your other imports)

# Load variables from .env into the system environment
load_dotenv()

@dataclass
class Config:
    # --- Add this new field for the API Key ---
    api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))

    """
    Configuration settings for the Docstring Generation Agent.
    
    Attributes:
        docstring_style: Default docstring style to use
        output_format: Output format for results
        min_quality_score: Minimum quality score to report
        show_metrics: Whether to display code metrics
        verbose: Enable verbose output
        modify_inplace: Modify files in-place to add docstrings
        backup_files: Create backups before modifying files
        max_line_length: Maximum line length for docstrings
        indent_size: Number of spaces for indentation
        include_type_hints: Whether to include type hints in docstrings
        analyze_complexity: Perform complexity analysis
        generate_suggestions: Generate improvement suggestions
        ai_enhancement: Use AI for better descriptions (creative feature)
    """
    
    # Docstring settings
    docstring_style: DocstringStyle = DocstringStyle.GOOGLE
    max_line_length: int = 79
    indent_size: int = 4
    include_type_hints: bool = True
    
    # Output settings
    output_format: OutputFormat = OutputFormat.CONSOLE
    verbose: bool = False
    show_metrics: bool = True
    
    # Quality settings
    min_quality_score: float = 0.0
    analyze_complexity: bool = True
    generate_suggestions: bool = True
    
    # File modification settings
    modify_inplace: bool = False
    backup_files: bool = True
    
    # AI Enhancement (Creative Feature)
    ai_enhancement: bool = True
    use_smart_descriptions: bool = True
    detect_patterns: bool = True
    
    # Complexity thresholds
    complexity_thresholds: Dict[str, int] = field(default_factory=lambda: {
        'low': 5,
        'moderate': 10,
        'high': 20,
    })
    
    # Quality thresholds
    quality_thresholds: Dict[str, float] = field(default_factory=lambda: {
        'excellent': 90.0,
        'good': 80.0,
        'acceptable': 70.0,
        'poor': 60.0,
    })
    
    # Exclusion patterns
    exclude_patterns: List[str] = field(default_factory=lambda: [
        '__pycache__',
        '.git',
        '.venv',
        'venv',
        'env',
        '.tox',
        'build',
        'dist',
    ])
    
    # Template customization
    custom_templates: Dict[str, str] = field(default_factory=dict)
    
    def get_complexity_threshold(self, level: str) -> int:
        """
        Get complexity threshold for a given level.
        
        Args:
            level: Complexity level (low, moderate, high)
            
        Returns:
            Threshold value
        """
        return self.complexity_thresholds.get(level, 10)
    
    def get_quality_threshold(self, level: str) -> float:
        """
        Get quality threshold for a given level.
        
        Args:
            level: Quality level name
            
        Returns:
            Threshold value
        """
        return self.quality_thresholds.get(level, 70.0)
    
    def is_path_excluded(self, path: str) -> bool:
        """
        Check if a path should be excluded.
        
        Args:
            path: Path to check
            
        Returns:
            True if path should be excluded
        """
        return any(pattern in path for pattern in self.exclude_patterns)
    
    def to_dict(self) -> Dict:
        """
        Convert configuration to dictionary.
        
        Returns:
            Dictionary representation of configuration
        """
        return {
            'docstring_style': self.docstring_style.value,
            'output_format': self.output_format.value,
            'max_line_length': self.max_line_length,
            'indent_size': self.indent_size,
            'include_type_hints': self.include_type_hints,
            'verbose': self.verbose,
            'show_metrics': self.show_metrics,
            'min_quality_score': self.min_quality_score,
            'analyze_complexity': self.analyze_complexity,
            'generate_suggestions': self.generate_suggestions,
            'modify_inplace': self.modify_inplace,
            'backup_files': self.backup_files,
            'ai_enhancement': self.ai_enhancement,
            'use_smart_descriptions': self.use_smart_descriptions,
            'detect_patterns': self.detect_patterns,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Config':
        """
        Create configuration from dictionary.
        
        Args:
            data: Configuration dictionary
            
        Returns:
            Config instance
        """
        config = cls()
        
        if 'docstring_style' in data:
            config.docstring_style = DocstringStyle(data['docstring_style'])
        if 'output_format' in data:
            config.output_format = OutputFormat(data['output_format'])
        
        for key, value in data.items():
            if hasattr(config, key) and key not in ('docstring_style', 'output_format'):
                setattr(config, key, value)
        
        return config


# Predefined configurations for different use cases
PRESET_CONFIGS = {
    'minimal': Config(
        show_metrics=False,
        generate_suggestions=False,
        verbose=False,
    ),
    
    'standard': Config(
        show_metrics=True,
        generate_suggestions=True,
        verbose=False,
    ),
    
    'comprehensive': Config(
        show_metrics=True,
        generate_suggestions=True,
        verbose=True,
        analyze_complexity=True,
        ai_enhancement=True,
    ),
    
    'production': Config(
        docstring_style=DocstringStyle.GOOGLE,
        modify_inplace=True,
        backup_files=True,
        min_quality_score=70.0,
        generate_suggestions=True,
    ),
}


def get_preset_config(preset_name: str) -> Optional[Config]:
    """
    Get a predefined configuration preset.
    
    Args:
        preset_name: Name of the preset
        
    Returns:
        Config instance or None if preset not found
    """
    return PRESET_CONFIGS.get(preset_name)
