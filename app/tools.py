"""
Tools and Utilities for Docstring Generation Agent

This module contains all helper classes and utilities including:
- CodeAnalyzer: AST-based code analysis
- ComplexityAnalyzer: Cyclomatic complexity calculation
- DocstringBuilder: Multi-style docstring generation
- PatternDetector: Design pattern recognition (CREATIVE)
- ExampleGenerator: Automatic usage example generation (CREATIVE)
- FileHandler: File I/O operations
- DisplayFormatter: Result formatting and display
"""

import ast
import json
import shutil
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

from app.models import (
    CodeMetrics, FunctionInfo, ClassInfo, ParameterInfo,
    DocstringResult, Suggestion, DocstringStyle
)
from app.config import Config


class CodeAnalyzer:
    """Analyzes Python code using AST traversal."""
    
    def __init__(self, config: Config):
        self.config = config
    
    def parse_file(self, file_path: str) -> ast.AST:
        """
        Parse a Python file into an AST.
        
        Args:
            file_path: Path to Python file
            
        Returns:
            AST tree
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return ast.parse(f.read(), filename=file_path)


class ComplexityAnalyzer(ast.NodeVisitor):
    """
    Analyzes code complexity using cyclomatic complexity.
    
    Cyclomatic complexity measures the number of linearly independent
    paths through a program's source code.
    """
    
    def __init__(self):
        self.complexity = 1
        self.return_count = 0
        self.lines_of_code = 0
    
    def visit_If(self, node):
        self.complexity += 1
        self.generic_visit(node)
    
    def visit_For(self, node):
        self.complexity += 1
        self.generic_visit(node)
    
    def visit_While(self, node):
        self.complexity += 1
        self.generic_visit(node)
    
    def visit_ExceptHandler(self, node):
        self.complexity += 1
        self.generic_visit(node)
    
    def visit_With(self, node):
        self.complexity += 1
        self.generic_visit(node)
    
    def visit_Return(self, node):
        self.return_count += 1
        self.generic_visit(node)
    
    def visit_BoolOp(self, node):
        # Count 'and' and 'or' in conditions
        self.complexity += len(node.values) - 1
        self.generic_visit(node)
    
    def analyze_function(self, node: ast.FunctionDef) -> CodeMetrics:
        """
        Analyze a function and return metrics.
        
        Args:
            node: Function AST node
            
        Returns:
            CodeMetrics object
        """
        self.complexity = 1
        self.return_count = 0
        self.visit(node)
        
        # Calculate lines of code
        loc = node.end_lineno - node.lineno + 1
        
        # Check for type hints
        has_type_hints = any(arg.annotation for arg in node.args.args) or node.returns is not None
        
        # Calculate maintainability index (simplified version)
        # MI = 171 - 5.2 * ln(HV) - 0.23 * CC - 16.2 * ln(LOC)
        # Using simplified version
        mi = max(0, 100 - (self.complexity * 3) - (loc * 0.5))
        
        return CodeMetrics(
            cyclomatic_complexity=self.complexity,
            lines_of_code=loc,
            num_parameters=len(node.args.args),
            num_return_statements=self.return_count,
            has_type_hints=has_type_hints,
            quality_score=0.0,  # Will be calculated by agent
            maintainability_index=mi
        )
    
    def analyze_class(self, node: ast.ClassDef) -> CodeMetrics:
        """
        Analyze a class and return metrics.
        
        Args:
            node: Class AST node
            
        Returns:
            CodeMetrics object
        """
        loc = node.end_lineno - node.lineno + 1
        
        # Count methods
        methods = [n for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
        
        # Average complexity of methods
        total_complexity = 0
        for method in methods:
            analyzer = ComplexityAnalyzer()
            analyzer.visit(method)
            total_complexity += analyzer.complexity
        
        avg_complexity = total_complexity // len(methods) if methods else 1
        
        return CodeMetrics(
            cyclomatic_complexity=avg_complexity,
            lines_of_code=loc,
            num_parameters=len(methods),
            num_return_statements=0,
            has_type_hints=False,
            quality_score=0.0,
            maintainability_index=max(0, 100 - (avg_complexity * 2) - (loc * 0.3))
        )


class PatternDetector:
    """
    Detects design patterns and code patterns in Python code.
    
    CREATIVE FEATURE: Intelligent pattern recognition
    """
    
    COMMON_PATTERNS = {
        'factory': ['create', 'build', 'make', 'get_instance'],
        'singleton': ['__new__', '_instance', 'get_instance'],
        'decorator': ['wrapper', 'wrapped', 'decorator'],
        'observer': ['notify', 'subscribe', 'update', 'observer'],
        'strategy': ['strategy', 'algorithm', 'execute'],
        'builder': ['builder', 'build', 'construct'],
        'adapter': ['adapt', 'adapter', 'wrapper'],
    }
    
    def detect_function_patterns(self, node: ast.FunctionDef, source_code: str) -> List[str]:
        """
        Detect patterns in a function.
        
        Args:
            node: Function AST node
            source_code: Source code
            
        Returns:
            List of detected pattern names
        """
        patterns = []
        func_name = node.name.lower()
        
        # Check name-based patterns
        for pattern, keywords in self.COMMON_PATTERNS.items():
            if any(keyword in func_name for keyword in keywords):
                patterns.append(pattern)
        
        # Detect specific patterns
        if self._is_property_getter(node):
            patterns.append('property_getter')
        
        if self._is_property_setter(node):
            patterns.append('property_setter')
        
        if self._is_context_manager(node):
            patterns.append('context_manager')
        
        if self._is_generator(node):
            patterns.append('generator')
        
        if self._is_async_function(node):
            patterns.append('async_function')
        
        if self._is_recursive(node):
            patterns.append('recursive')
        
        return list(set(patterns))
    
    def detect_class_patterns(self, node: ast.ClassDef, source_code: str) -> List[str]:
        """
        Detect design patterns in a class.
        
        Args:
            node: Class AST node
            source_code: Source code
            
        Returns:
            List of detected pattern names
        """
        patterns = []
        
        # Check for singleton pattern
        if self._is_singleton(node):
            patterns.append('singleton')
        
        # Check for factory pattern
        if self._is_factory(node):
            patterns.append('factory')
        
        # Check for builder pattern
        if self._is_builder(node):
            patterns.append('builder')
        
        # Check for dataclass
        if self._is_dataclass(node):
            patterns.append('dataclass')
        
        # Check for abstract base class
        if self._is_abstract(node):
            patterns.append('abstract_base_class')
        
        # Check for mixin
        if self._is_mixin(node):
            patterns.append('mixin')
        
        return list(set(patterns))
    
    def _is_property_getter(self, node: ast.FunctionDef) -> bool:
        """Check if function is a property getter."""
        return any(
            isinstance(d, ast.Name) and d.id == 'property'
            for d in node.decorator_list
        )
    
    def _is_property_setter(self, node: ast.FunctionDef) -> bool:
        """Check if function is a property setter."""
        return any(
            isinstance(d, ast.Attribute) and d.attr == 'setter'
            for d in node.decorator_list
        )
    
    def _is_context_manager(self, node: ast.FunctionDef) -> bool:
        """Check if function is a context manager."""
        return node.name in ('__enter__', '__exit__')
    
    def _is_generator(self, node: ast.FunctionDef) -> bool:
        """Check if function is a generator."""
        for child in ast.walk(node):
            if isinstance(child, ast.Yield) or isinstance(child, ast.YieldFrom):
                return True
        return False
    
    def _is_async_function(self, node: ast.FunctionDef) -> bool:
        """Check if function is async."""
        return isinstance(node, ast.AsyncFunctionDef)
    
    def _is_recursive(self, node: ast.FunctionDef) -> bool:
        """Check if function is recursive."""
        func_name = node.name
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name) and child.func.id == func_name:
                    return True
        return False
    
    def _is_singleton(self, node: ast.ClassDef) -> bool:
        """Check if class implements singleton pattern."""
        has_new = any(
            isinstance(n, ast.FunctionDef) and n.name == '__new__'
            for n in node.body
        )
        has_instance = any(
            isinstance(n, ast.Assign) and any(
                isinstance(t, ast.Name) and 'instance' in t.id.lower()
                for t in n.targets
            )
            for n in node.body
        )
        return has_new or has_instance
    
    def _is_factory(self, node: ast.ClassDef) -> bool:
        """Check if class is a factory."""
        return node.name.endswith('Factory') or any(
            isinstance(n, ast.FunctionDef) and 'create' in n.name.lower()
            for n in node.body
        )
    
    def _is_builder(self, node: ast.ClassDef) -> bool:
        """Check if class is a builder."""
        return node.name.endswith('Builder') or any(
            isinstance(n, ast.FunctionDef) and n.name == 'build'
            for n in node.body
        )
    
    def _is_dataclass(self, node: ast.ClassDef) -> bool:
        """Check if class is a dataclass."""
        return any(
            isinstance(d, ast.Name) and d.id == 'dataclass'
            for d in node.decorator_list
        )
    
    def _is_abstract(self, node: ast.ClassDef) -> bool:
        """Check if class is abstract."""
        # Check for ABC base or abstractmethod decorators
        has_abc_base = any('ABC' in ast.unparse(base) for base in node.bases)
        has_abstract_method = any(
            isinstance(n, ast.FunctionDef) and any(
                'abstractmethod' in ast.unparse(d) for d in n.decorator_list
            )
            for n in node.body
        )
        return has_abc_base or has_abstract_method
    
    def _is_mixin(self, node: ast.ClassDef) -> bool:
        """Check if class is a mixin."""
        return node.name.endswith('Mixin')


class ExampleGenerator:
    """
    Generates usage examples for functions and classes.
    
    CREATIVE FEATURE: Automatic example generation
    """
    
    def generate_example(self, func_info: FunctionInfo, patterns: List[str]) -> Optional[str]:
        """
        Generate a usage example for a function.
        
        Args:
            func_info: Function information
            patterns: Detected patterns
            
        Returns:
            Example code as string or None
        """
        if not func_info.parameters:
            # Simple function with no parameters
            return f"    >>> {func_info.name}()\n    # Returns result"
        
        # Generate parameter values
        param_str = self._generate_param_values(func_info.parameters)
        
        if func_info.is_async:
            return f"    >>> await {func_info.name}({param_str})\n    # Returns result"
        else:
            return f"    >>> result = {func_info.name}({param_str})\n    >>> print(result)"
    
    def _generate_param_values(self, parameters: List[ParameterInfo]) -> str:
        """Generate example parameter values."""
        values = []
        
        for param in parameters:
            if param.default_value:
                continue  # Skip parameters with defaults
            
            # Generate value based on type hint or name
            value = self._infer_param_value(param)
            values.append(f"{param.name}={value}")
        
        return ", ".join(values)
    
    def _infer_param_value(self, param: ParameterInfo) -> str:
        """Infer an example value for a parameter."""
        # Check type hint
        if param.type_hint:
            type_lower = param.type_hint.lower()
            if 'int' in type_lower:
                return "42"
            elif 'float' in type_lower:
                return "3.14"
            elif 'str' in type_lower:
                return '"example"'
            elif 'bool' in type_lower:
                return "True"
            elif 'list' in type_lower:
                return "[]"
            elif 'dict' in type_lower:
                return "{}"
        
        # Infer from parameter name
        name_lower = param.name.lower()
        if 'count' in name_lower or 'num' in name_lower or 'id' in name_lower:
            return "1"
        elif 'name' in name_lower or 'text' in name_lower or 'message' in name_lower:
            return f'"{param.name}"'
        elif 'flag' in name_lower or 'is_' in name_lower or 'has_' in name_lower:
            return "True"
        elif 'list' in name_lower or 'items' in name_lower:
            return "[]"
        elif 'dict' in name_lower or 'map' in name_lower:
            return "{}"
        
        return '"value"'


class DocstringBuilder:
    """
    Builds docstrings in various formats.
    
    Supports Google, NumPy, and Sphinx styles with intelligent
    description generation.
    """
    
    def __init__(self, config: Config):
        self.config = config
        self.style = config.docstring_style
    
    def build_function_docstring(self, func_info: FunctionInfo, 
                                metrics: CodeMetrics, patterns: List[str]) -> str:
        """
        Build a docstring for a function.
        
        Args:
            func_info: Function information
            metrics: Code metrics
            patterns: Detected patterns
            
        Returns:
            Generated docstring
        """
        if self.style == DocstringStyle.GOOGLE:
            return self._build_google_function(func_info, metrics, patterns)
        elif self.style == DocstringStyle.NUMPY:
            return self._build_numpy_function(func_info, metrics, patterns)
        else:
            return self._build_sphinx_function(func_info, metrics, patterns)
    
    def build_class_docstring(self, class_info: ClassInfo, 
                             metrics: CodeMetrics, patterns: List[str]) -> str:
        """
        Build a docstring for a class.
        
        Args:
            class_info: Class information
            metrics: Code metrics
            patterns: Detected patterns
            
        Returns:
            Generated docstring
        """
        if self.style == DocstringStyle.GOOGLE:
            return self._build_google_class(class_info, metrics, patterns)
        elif self.style == DocstringStyle.NUMPY:
            return self._build_numpy_class(class_info, metrics, patterns)
        else:
            return self._build_sphinx_class(class_info, metrics, patterns)
    
    def _build_google_function(self, func_info: FunctionInfo, 
                              metrics: CodeMetrics, patterns: List[str]) -> str:
        """Build Google-style function docstring."""
        lines = []
        
        # Summary line
        summary = self._generate_smart_summary(func_info.name, 'function', patterns)
        lines.append(summary)
        lines.append("")
        
        # Add pattern information if detected
        if patterns:
            pattern_desc = ', '.join(patterns).replace('_', ' ').title()
            lines.append(f"Pattern: {pattern_desc}")
            lines.append("")
        
        # Add complexity warning
        if metrics.cyclomatic_complexity > 10:
            lines.append(f"Warning: High complexity (CC={metrics.cyclomatic_complexity}). Consider refactoring.")
            lines.append("")
        
        # Parameters
        if func_info.parameters:
            lines.append("Args:")
            for param in func_info.parameters:
                param_line = f"    {param.name}"
                if param.type_hint:
                    param_line += f" ({param.type_hint})"
                param_line += f": {self._generate_param_description(param.name, param.type_hint)}"
                if param.default_value:
                    param_line += f" Defaults to {param.default_value}."
                lines.append(param_line)
            lines.append("")
        
        # Returns
        if func_info.return_type or metrics.num_return_statements > 0:
            lines.append("Returns:")
            return_type = func_info.return_type if func_info.return_type else "Any"
            lines.append(f"    {return_type}: {self._generate_return_description(func_info.name)}")
            lines.append("")
        
        # Raises
        if func_info.raises:
            lines.append("Raises:")
            for exc in func_info.raises:
                lines.append(f"    {exc}: {self._generate_exception_description(exc)}")
            lines.append("")
        
        # Note for async
        if func_info.is_async:
            lines.append("Note:")
            lines.append("    This is an asynchronous function. Use with await.")
            lines.append("")
        
        return '\n'.join(lines).rstrip()
    
    def _build_numpy_function(self, func_info: FunctionInfo, 
                             metrics: CodeMetrics, patterns: List[str]) -> str:
        """Build NumPy-style function docstring."""
        lines = []
        
        # Summary
        summary = self._generate_smart_summary(func_info.name, 'function', patterns)
        lines.append(summary)
        lines.append("")
        
        # Parameters
        if func_info.parameters:
            lines.append("Parameters")
            lines.append("----------")
            for param in func_info.parameters:
                param_line = param.name
                if param.type_hint:
                    param_line += f" : {param.type_hint}"
                lines.append(param_line)
                desc = f"    {self._generate_param_description(param.name, param.type_hint)}"
                if param.default_value:
                    desc += f" Defaults to {param.default_value}."
                lines.append(desc)
            lines.append("")
        
        # Returns
        if func_info.return_type:
            lines.append("Returns")
            lines.append("-------")
            lines.append(func_info.return_type)
            lines.append(f"    {self._generate_return_description(func_info.name)}")
            lines.append("")
        
        # Raises
        if func_info.raises:
            lines.append("Raises")
            lines.append("------")
            for exc in func_info.raises:
                lines.append(exc)
                lines.append(f"    {self._generate_exception_description(exc)}")
            lines.append("")
        
        return '\n'.join(lines).rstrip()
    
    def _build_sphinx_function(self, func_info: FunctionInfo, 
                              metrics: CodeMetrics, patterns: List[str]) -> str:
        """Build Sphinx-style function docstring."""
        lines = []
        
        # Summary
        summary = self._generate_smart_summary(func_info.name, 'function', patterns)
        lines.append(summary)
        lines.append("")
        
        # Parameters
        for param in func_info.parameters:
            param_line = f":param {param.name}: {self._generate_param_description(param.name, param.type_hint)}"
            lines.append(param_line)
            if param.type_hint:
                lines.append(f":type {param.name}: {param.type_hint}")
        
        if func_info.parameters:
            lines.append("")
        
        # Returns
        if func_info.return_type:
            lines.append(f":return: {self._generate_return_description(func_info.name)}")
            lines.append(f":rtype: {func_info.return_type}")
            lines.append("")
        
        # Raises
        for exc in func_info.raises:
            lines.append(f":raises {exc}: {self._generate_exception_description(exc)}")
        
        if func_info.raises:
            lines.append("")
        
        return '\n'.join(lines).rstrip()
    
    def _build_google_class(self, class_info: ClassInfo, 
                           metrics: CodeMetrics, patterns: List[str]) -> str:
        """Build Google-style class docstring."""
        lines = []
        
        # Summary
        summary = self._generate_smart_summary(class_info.name, 'class', patterns)
        lines.append(summary)
        lines.append("")
        
        # Pattern description
        if patterns:
            pattern_desc = ', '.join(patterns).replace('_', ' ').title()
            lines.append(f"Design Pattern: {pattern_desc}")
            lines.append("")
        
        # Inheritance
        if class_info.bases:
            lines.append(f"Inherits from: {', '.join(class_info.bases)}")
            lines.append("")
        
        # Attributes
        if class_info.attributes:
            lines.append("Attributes:")
            for attr in class_info.attributes[:5]:  # Limit to first 5
                lines.append(f"    {attr}: {self._generate_attribute_description(attr)}")
            lines.append("")
        
        return '\n'.join(lines).rstrip()
    
    def _build_numpy_class(self, class_info: ClassInfo, 
                          metrics: CodeMetrics, patterns: List[str]) -> str:
        """Build NumPy-style class docstring."""
        lines = []
        
        # Summary
        summary = self._generate_smart_summary(class_info.name, 'class', patterns)
        lines.append(summary)
        lines.append("")
        
        # Attributes
        if class_info.attributes:
            lines.append("Attributes")
            lines.append("----------")
            for attr in class_info.attributes[:5]:
                lines.append(attr)
                lines.append(f"    {self._generate_attribute_description(attr)}")
            lines.append("")
        
        return '\n'.join(lines).rstrip()
    
    def _build_sphinx_class(self, class_info: ClassInfo, 
                           metrics: CodeMetrics, patterns: List[str]) -> str:
        """Build Sphinx-style class docstring."""
        lines = []
        
        # Summary
        summary = self._generate_smart_summary(class_info.name, 'class', patterns)
        lines.append(summary)
        lines.append("")
        
        return '\n'.join(lines).rstrip()
    
    def _generate_smart_summary(self, name: str, element_type: str, 
                               patterns: List[str]) -> str:
        """
        Generate intelligent summary based on name and patterns.
        
        CREATIVE FEATURE: Smart description generation
        """
        # Convert camelCase/snake_case to words
        words = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z][a-z]|\d|\W|$)|\d+', name.replace('_', ' '))
        readable_name = ' '.join(words).lower()
        
        # Check for common prefixes/patterns
        if name.startswith('get_'):
            return f"Get {readable_name.replace('get ', '')}."
        elif name.startswith('set_'):
            return f"Set {readable_name.replace('set ', '')}."
        elif name.startswith('is_') or name.startswith('has_'):
            return f"Check if {readable_name.replace('is ', '').replace('has ', '')}."
        elif name.startswith('create_') or name.startswith('make_'):
            return f"Create {readable_name.replace('create ', '').replace('make ', '')}."
        elif name.startswith('calculate_') or name.startswith('compute_'):
            return f"Calculate {readable_name.replace('calculate ', '').replace('compute ', '')}."
        elif name.startswith('process_'):
            return f"Process {readable_name.replace('process ', '')}."
        elif name.startswith('validate_'):
            return f"Validate {readable_name.replace('validate ', '')}."
        elif name.startswith('_'):
            return f"Internal helper for {readable_name.strip('_')}."
        
        # Pattern-based descriptions
        if 'factory' in patterns:
            return f"Factory {element_type} for creating {readable_name} instances."
        elif 'singleton' in patterns:
            return f"Singleton {element_type} ensuring single instance of {readable_name}."
        elif 'builder' in patterns:
            return f"Builder {element_type} for constructing {readable_name} objects."
        
        # Generic description
        if element_type == 'class':
            return f"{name} class implementation."
        else:
            return f"{name.replace('_', ' ').capitalize()}."
    
    def _generate_param_description(self, param_name: str, type_hint: Optional[str]) -> str:
        """Generate parameter description."""
        readable = param_name.replace('_', ' ')
        
        if 'file' in param_name or 'path' in param_name:
            return f"Path to {readable}"
        elif 'count' in param_name or 'num' in param_name:
            return f"Number of {readable}"
        elif 'name' in param_name:
            return f"Name of {readable}"
        elif 'id' in param_name:
            return f"Unique identifier for {readable}"
        elif 'flag' in param_name or param_name.startswith('is_') or param_name.startswith('has_'):
            return f"Whether to {readable}"
        elif 'data' in param_name:
            return f"Data for {readable}"
        elif 'config' in param_name:
            return f"Configuration for {readable}"
        
        return f"{readable.capitalize()}"
    
    def _generate_return_description(self, func_name: str) -> str:
        """Generate return value description."""
        if 'get_' in func_name:
            return "The requested data or object"
        elif 'is_' in func_name or 'has_' in func_name:
            return "True if condition is met, False otherwise"
        elif 'create_' in func_name or 'make_' in func_name:
            return "The newly created object"
        elif 'calculate_' in func_name or 'compute_' in func_name:
            return "The calculated result"
        elif 'process_' in func_name:
            return "The processed result"
        else:
            return "Result of the operation"
    
    def _generate_exception_description(self, exc_name: str) -> str:
        """Generate exception description."""
        if exc_name == 'ValueError':
            return "If the provided value is invalid"
        elif exc_name == 'TypeError':
            return "If the provided type is incorrect"
        elif exc_name == 'FileNotFoundError':
            return "If the specified file does not exist"
        elif exc_name == 'KeyError':
            return "If the specified key is not found"
        elif exc_name == 'IndexError':
            return "If the index is out of range"
        else:
            return f"If an error occurs during {exc_name.replace('Error', '').lower()}"
    
    def _generate_attribute_description(self, attr_name: str) -> str:
        """Generate attribute description."""
        readable = attr_name.replace('_', ' ')
        return f"{readable.capitalize()}"


class FileHandler:
    """Handles file operations for the agent."""
    
    @staticmethod
    def save_results(results: List[DocstringResult], output_path: str, 
                    output_format):
        """
        Save results to file.
        
        Args:
            results: List of results
            output_path: Output file path
            output_format: Output format
        """
        from app.models import OutputFormat
        
        if output_format == OutputFormat.JSON:
            FileHandler._save_json(results, output_path)
        elif output_format == OutputFormat.MARKDOWN:
            FileHandler._save_markdown(results, output_path)
        elif output_format == OutputFormat.HTML:
            FileHandler._save_html(results, output_path)
    
    @staticmethod
    def _save_json(results: List[DocstringResult], output_path: str):
        """Save results as JSON."""
        data = {
            'timestamp': datetime.now().isoformat(),
            'total_results': len(results),
            'results': [r.to_dict() for r in results]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def _save_markdown(results: List[DocstringResult], output_path: str):
        """Save results as Markdown."""
        lines = [
            "# Docstring Analysis Report",
            "",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Total Items:** {len(results)}",
            "",
            "---",
            ""
        ]
        
        for result in results:
            lines.append(f"## {result.element_name} ({result.element_type.value})")
            lines.append("")
            lines.append(f"**File:** `{result.file_path}:{result.line_number}`")
            lines.append(f"**Quality Score:** {result.quality_score:.1f}/100")
            lines.append(f"**Complexity:** {result.metrics.cyclomatic_complexity} ({result.metrics.get_complexity_level()})")
            lines.append("")
            lines.append("### Generated Docstring")
            lines.append("")
            lines.append("```python")
            lines.append(result.generated_docstring)
            lines.append("```")
            lines.append("")
            
            if result.suggestions:
                lines.append("### Suggestions")
                lines.append("")
                for sug in result.suggestions:
                    lines.append(f"- **{sug.severity.upper()}:** {sug.message}")
                lines.append("")
            
            lines.append("---")
            lines.append("")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    
    @staticmethod
    def _save_html(results: List[DocstringResult], output_path: str):
        """Save results as HTML."""
        html = [
            "<!DOCTYPE html>",
            "<html>",
            "<head>",
            "    <title>Docstring Analysis Report</title>",
            "    <style>",
            "        body { font-family: Arial, sans-serif; margin: 20px; }",
            "        .result { border: 1px solid #ddd; padding: 15px; margin: 10px 0; }",
            "        .header { background: #f0f0f0; padding: 10px; }",
            "        .docstring { background: #f9f9f9; padding: 10px; white-space: pre-wrap; }",
            "        .metric { display: inline-block; margin: 5px 10px 5px 0; }",
            "        .high-quality { color: green; }",
            "        .low-quality { color: red; }",
            "    </style>",
            "</head>",
            "<body>",
            "    <h1>Docstring Analysis Report</h1>",
            f"    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>",
            f"    <p>Total Items: {len(results)}</p>",
            "    <hr>",
        ]
        
        for result in results:
            quality_class = "high-quality" if result.quality_score >= 70 else "low-quality"
            html.append(f"    <div class='result'>")
            html.append(f"        <div class='header'>")
            html.append(f"            <h2>{result.element_name}</h2>")
            html.append(f"            <p><strong>Type:</strong> {result.element_type.value}</p>")
            html.append(f"            <p><strong>File:</strong> {result.file_path}:{result.line_number}</p>")
            html.append(f"        </div>")
            html.append(f"        <div class='metric'><strong>Quality:</strong> <span class='{quality_class}'>{result.quality_score:.1f}/100</span></div>")
            html.append(f"        <div class='metric'><strong>Complexity:</strong> {result.metrics.cyclomatic_complexity}</div>")
            html.append(f"        <div class='docstring'>{result.generated_docstring}</div>")
            html.append(f"    </div>")
        
        html.append("</body>")
        html.append("</html>")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(html))


class DisplayFormatter:
    """Formats and displays results in the console."""
    
    @staticmethod
    def display_results(results: List[DocstringResult], verbose: bool = False, 
                       show_metrics: bool = True):
        """
        Display results in the console.
        
        Args:
            results: List of results to display
            verbose: Show detailed information
            show_metrics: Show code metrics
        """
        if not results:
            print("No results to display.")
            return
        
        for i, result in enumerate(results, 1):
            print(f"\n{'='*70}")
            print(f"[{i}/{len(results)}] {result.element_name} ({result.element_type.value})")
            print(f"{'='*70}")
            print(f"📂 File: {result.file_path}:{result.line_number}")
            print(f"📊 Quality: {result.quality_score:.1f}/100 (Grade: {result.metrics.get_quality_grade()})")
            
            if show_metrics:
                print(f"\n📈 Metrics:")
                print(f"   Complexity: {result.metrics.cyclomatic_complexity} ({result.metrics.get_complexity_level()})")
                print(f"   Lines of Code: {result.metrics.lines_of_code}")
                print(f"   Parameters: {result.metrics.num_parameters}")
                print(f"   Type Hints: {'✅' if result.metrics.has_type_hints else '❌'}")
                print(f"   Maintainability: {result.metrics.maintainability_index:.1f}/100")
            
            print(f"\n📝 Generated Docstring ({result.style.value}):")
            print("-" * 70)
            print(result.generated_docstring)
            print("-" * 70)
            
            if result.suggestions and verbose:
                print(f"\n💡 Suggestions ({len(result.suggestions)}):")
                for sug in result.suggestions:
                    icon = "⚠️" if sug.severity == "warning" else "ℹ️" if sug.severity == "info" else "❌"
                    print(f"   {icon} [{sug.category}] {sug.message}")
            
            if result.has_existing_docstring:
                print("\n✓ Already has docstring")
