"""
Data Models for Docstring Generation Agent

This module contains all the data models, enums, and dataclasses
used throughout the docstring generation system.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any


class DocstringStyle(Enum):
    """Supported docstring styles."""
    GOOGLE = "google"
    NUMPY = "numpy"
    SPHINX = "sphinx"


class OutputFormat(Enum):
    """Supported output formats for documentation."""
    CONSOLE = "console"
    JSON = "json"
    MARKDOWN = "markdown"
    HTML = "html"


class CodeElementType(Enum):
    """Types of code elements that can have docstrings."""
    FUNCTION = "function"
    METHOD = "method"
    CLASS = "class"
    MODULE = "module"


@dataclass
class CodeMetrics:
    """
    Metrics for code quality and complexity analysis.
    
    Attributes:
        cyclomatic_complexity: Measure of code complexity based on control flow
        lines_of_code: Total number of lines in the code element
        num_parameters: Number of parameters for functions/methods
        num_return_statements: Count of return statements
        has_type_hints: Whether the code includes type annotations
        quality_score: Overall quality score (0-100)
        maintainability_index: Code maintainability metric
    """
    cyclomatic_complexity: int = 0
    lines_of_code: int = 0
    num_parameters: int = 0
    num_return_statements: int = 0
    has_type_hints: bool = False
    quality_score: float = 0.0
    maintainability_index: float = 0.0
    
    def get_complexity_level(self) -> str:
        """
        Get human-readable complexity level.
        
        Returns:
            Complexity level as string
        """
        if self.cyclomatic_complexity <= 5:
            return "Low"
        elif self.cyclomatic_complexity <= 10:
            return "Moderate"
        elif self.cyclomatic_complexity <= 20:
            return "High"
        else:
            return "Very High"
    
    def get_quality_grade(self) -> str:
        """
        Get quality grade based on score.
        
        Returns:
            Letter grade (A, B, C, D, F)
        """
        if self.quality_score >= 90:
            return "A"
        elif self.quality_score >= 80:
            return "B"
        elif self.quality_score >= 70:
            return "C"
        elif self.quality_score >= 60:
            return "D"
        else:
            return "F"


@dataclass
class ParameterInfo:
    """
    Information about a function/method parameter.
    
    Attributes:
        name: Parameter name
        type_hint: Type annotation if present
        default_value: Default value if present
        description: AI-generated description
    """
    name: str
    type_hint: Optional[str] = None
    default_value: Optional[str] = None
    description: str = ""


@dataclass
class FunctionInfo:
    """
    Comprehensive information about a function or method.
    
    Attributes:
        name: Function name
        is_async: Whether function is async
        is_method: Whether it's a method (has self/cls)
        is_property: Whether it's a property decorator
        parameters: List of parameter information
        return_type: Return type annotation if present
        raises: List of exceptions that may be raised
        decorators: List of applied decorators
        existing_docstring: Existing docstring if any
    """
    name: str
    is_async: bool = False
    is_method: bool = False
    is_property: bool = False
    parameters: List[ParameterInfo] = field(default_factory=list)
    return_type: Optional[str] = None
    raises: List[str] = field(default_factory=list)
    decorators: List[str] = field(default_factory=list)
    existing_docstring: Optional[str] = None


@dataclass
class ClassInfo:
    """
    Comprehensive information about a class.
    
    Attributes:
        name: Class name
        bases: List of base classes
        methods: List of method names
        attributes: List of class/instance attributes
        decorators: List of applied decorators
        existing_docstring: Existing docstring if any
    """
    name: str
    bases: List[str] = field(default_factory=list)
    methods: List[str] = field(default_factory=list)
    attributes: List[str] = field(default_factory=list)
    decorators: List[str] = field(default_factory=list)
    existing_docstring: Optional[str] = None


@dataclass
class Suggestion:
    """
    Best practice suggestion for code improvement.
    
    Attributes:
        category: Suggestion category (e.g., 'type_hints', 'complexity')
        severity: Severity level (info, warning, error)
        message: Suggestion message
        line_number: Optional line number reference
    """
    category: str
    severity: str
    message: str
    line_number: Optional[int] = None


@dataclass
class DocstringResult:
    """
    Result of docstring generation for a code element.
    
    Attributes:
        element_type: Type of code element
        element_name: Name of the element
        file_path: Source file path
        line_number: Starting line number
        generated_docstring: The generated docstring
        style: Docstring style used
        quality_score: Quality score (0-100)
        metrics: Code metrics
        suggestions: List of improvement suggestions
        has_existing_docstring: Whether element already had a docstring
        confidence_score: AI confidence in generation quality
    """
    element_type: CodeElementType
    element_name: str
    file_path: str
    line_number: int
    generated_docstring: str
    style: DocstringStyle
    quality_score: float
    metrics: CodeMetrics
    suggestions: List[Suggestion] = field(default_factory=list)
    has_existing_docstring: bool = False
    confidence_score: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert result to dictionary for serialization.
        
        Returns:
            Dictionary representation
        """
        return {
            'element_type': self.element_type.value,
            'element_name': self.element_name,
            'file_path': self.file_path,
            'line_number': self.line_number,
            'generated_docstring': self.generated_docstring,
            'style': self.style.value,
            'quality_score': self.quality_score,
            'metrics': {
                'cyclomatic_complexity': self.metrics.cyclomatic_complexity,
                'lines_of_code': self.metrics.lines_of_code,
                'num_parameters': self.metrics.num_parameters,
                'num_return_statements': self.metrics.num_return_statements,
                'has_type_hints': self.metrics.has_type_hints,
                'quality_score': self.metrics.quality_score,
                'maintainability_index': self.metrics.maintainability_index,
                'complexity_level': self.metrics.get_complexity_level(),
                'quality_grade': self.metrics.get_quality_grade(),
            },
            'suggestions': [
                {
                    'category': s.category,
                    'severity': s.severity,
                    'message': s.message,
                    'line_number': s.line_number
                }
                for s in self.suggestions
            ],
            'has_existing_docstring': self.has_existing_docstring,
            'confidence_score': self.confidence_score,
        }


@dataclass
class AnalysisReport:
    """
    Complete analysis report for a file or project.
    
    Attributes:
        file_paths: List of analyzed files
        results: List of all docstring results
        summary: Summary statistics
        timestamp: Analysis timestamp
    """
    file_paths: List[str]
    results: List[DocstringResult]
    summary: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = ""
    
    def calculate_summary(self):
        """Calculate summary statistics from results."""
        if not self.results:
            return
        
        total = len(self.results)
        avg_quality = sum(r.quality_score for r in self.results) / total
        avg_complexity = sum(r.metrics.cyclomatic_complexity for r in self.results) / total
        
        self.summary = {
            'total_elements': total,
            'average_quality_score': round(avg_quality, 2),
            'average_complexity': round(avg_complexity, 2),
            'functions': sum(1 for r in self.results if r.element_type == CodeElementType.FUNCTION),
            'methods': sum(1 for r in self.results if r.element_type == CodeElementType.METHOD),
            'classes': sum(1 for r in self.results if r.element_type == CodeElementType.CLASS),
            'with_type_hints': sum(1 for r in self.results if r.metrics.has_type_hints),
            'high_quality': sum(1 for r in self.results if r.quality_score >= 80),
            'needs_improvement': sum(1 for r in self.results if r.quality_score < 60),
            'total_suggestions': sum(len(r.suggestions) for r in self.results),
        }
