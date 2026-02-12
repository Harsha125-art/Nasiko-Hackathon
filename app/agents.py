"""
Docstring Generation Agent - Main Agent Implementation

This module contains the core DocstringAgent class that orchestrates
the entire docstring generation process with AI-powered enhancements.

CREATIVE FEATURES:
1. Smart Pattern Detection - Recognizes common code patterns (factory, singleton, etc.)
2. Context-Aware Descriptions - Generates descriptions based on function name semantics
3. Example Generation - Auto-generates usage examples for complex functions
4. Cross-Reference Detection - Links related functions and classes
5. Sentiment Analysis - Detects TODO/FIXME comments and flags them
"""

import ast
import re
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.models import (
    CodeMetrics, FunctionInfo, ClassInfo, ParameterInfo,
    DocstringResult, CodeElementType, Suggestion, AnalysisReport
)
from app.config import Config
from app.tools import (
    CodeAnalyzer, ComplexityAnalyzer, DocstringBuilder,
    PatternDetector, ExampleGenerator
)


class DocstringAgent:
    """
    Main agent for intelligent docstring generation.
    
    This agent analyzes Python code and generates comprehensive docstrings
    with quality metrics, complexity analysis, and best practice suggestions.
    
    Features:
        - Multi-style docstring generation (Google, NumPy, Sphinx)
        - Cyclomatic complexity analysis
        - Type hint validation and inference
        - Pattern detection (design patterns, code smells)
        - Automatic example generation
        - Quality scoring and grading
    """
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize the Docstring Agent.
        
        Args:
            config: Configuration object. Defaults to standard config.
        """
        self.config = config or Config()
        self.code_analyzer = CodeAnalyzer(self.config)
        self.complexity_analyzer = ComplexityAnalyzer()
        self.docstring_builder = DocstringBuilder(self.config)
        self.pattern_detector = PatternDetector()
        self.example_generator = ExampleGenerator()
        
        # Statistics tracking (creative feature)
        self.stats = {
            'total_analyzed': 0,
            'total_functions': 0,
            'total_classes': 0,
            'patterns_detected': 0,
            'examples_generated': 0,
        }
    
    def process_file(self, file_path: str) -> List[DocstringResult]:
        """
        Process a Python file and generate docstrings for all elements.
        
        Args:
            file_path: Path to the Python file to analyze
            
        Returns:
            List of DocstringResult objects for each code element
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            SyntaxError: If the file contains invalid Python syntax
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Read source code
        with open(path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        # Parse AST
        try:
            tree = ast.parse(source_code, filename=str(path))
        except SyntaxError as e:
            raise SyntaxError(f"Syntax error in {file_path}: {e}")
        
        # Analyze file
        results = []
        
        # Process module-level elements
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                result = self._process_class(node, str(path), source_code)
                if result:
                    results.append(result)
                    self.stats['total_classes'] += 1
            
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Skip methods (they're processed with their class)
                if not self._is_method(node, tree):
                    result = self._process_function(node, str(path), source_code)
                    if result:
                        results.append(result)
                        self.stats['total_functions'] += 1
        
        self.stats['total_analyzed'] += len(results)
        return results
    
    def process_code(self, source_code: str) -> List[DocstringResult]:
        """
        Process a string of Python code and generate docstrings for all elements.
        
        Args:
            source_code: The Python source code to analyze
            
        Returns:
            List of DocstringResult objects for each code element
        """
        # Parse AST from the string
        try:
            tree = ast.parse(source_code)
        except SyntaxError as e:
            # You might want to import streamlit as st at the top if using this
            raise SyntaxError(f"Syntax error in provided code: {e}")
        
        results = []
        file_placeholder = "string_input.py"
        
        # Process the AST nodes just like in process_file
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                result = self._process_class(node, file_placeholder, source_code)
                if result:
                    results.append(result)
                    self.stats['total_classes'] += 1
            
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Skip methods (they're processed with their class)
                if not self._is_method(node, tree):
                    result = self._process_function(node, file_placeholder, source_code)
                    if result:
                        results.append(result)
                        self.stats['total_functions'] += 1
        
        self.stats['total_analyzed'] += len(results)
        return results
    
    def _is_method(self, func_node: ast.FunctionDef, tree: ast.AST) -> bool:
        """
        Check if a function is a method (inside a class).
        
        Args:
            func_node: Function AST node
            tree: Full AST tree
            
        Returns:
            True if function is a method
        """
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if func_node in ast.walk(node):
                    return True
        return False
    
    def _process_function(self, node: ast.FunctionDef, file_path: str, 
                         source_code: str) -> Optional[DocstringResult]:
        """
        Process a function and generate its docstring.
        
        Args:
            node: Function AST node
            file_path: Source file path
            source_code: Complete source code
            
        Returns:
            DocstringResult or None if processing fails
        """
        # Extract function information
        func_info = self._extract_function_info(node)
        
        # Analyze metrics
        metrics = self.complexity_analyzer.analyze_function(node)
        
        # Calculate quality score
        metrics.quality_score = self._calculate_quality_score(metrics, func_info)
        
        # Detect patterns (CREATIVE FEATURE)
        patterns = self.pattern_detector.detect_function_patterns(node, source_code)
        
        # Generate docstring
        docstring = self.docstring_builder.build_function_docstring(
            func_info, metrics, patterns
        )
        
        # Generate suggestions
        suggestions = self._generate_suggestions(func_info, metrics, patterns)
        
        # Generate example if complex (CREATIVE FEATURE)
        if metrics.cyclomatic_complexity > 5 or len(func_info.parameters) > 3:
            example = self.example_generator.generate_example(func_info, patterns)
            if example:
                docstring += f"\n\nExample:\n{example}"
                self.stats['examples_generated'] += 1
        
        # Calculate confidence score (CREATIVE FEATURE)
        confidence = self._calculate_confidence_score(func_info, metrics, patterns)
        
        return DocstringResult(
            element_type=CodeElementType.METHOD if func_info.is_method else CodeElementType.FUNCTION,
            element_name=func_info.name,
            file_path=file_path,
            line_number=node.lineno,
            generated_docstring=docstring,
            style=self.config.docstring_style,
            quality_score=metrics.quality_score,
            metrics=metrics,
            suggestions=suggestions,
            has_existing_docstring=func_info.existing_docstring is not None,
            confidence_score=confidence,
        )
    
    def _process_class(self, node: ast.ClassDef, file_path: str, 
                       source_code: str) -> Optional[DocstringResult]:
        """
        Process a class and generate its docstring.
        
        Args:
            node: Class AST node
            file_path: Source file path
            source_code: Complete source code
            
        Returns:
            DocstringResult or None if processing fails
        """
        # Extract class information
        class_info = self._extract_class_info(node)
        
        # Analyze metrics
        metrics = self.complexity_analyzer.analyze_class(node)
        
        # Calculate quality score
        metrics.quality_score = self._calculate_class_quality_score(metrics, class_info)
        
        # Detect design patterns (CREATIVE FEATURE)
        patterns = self.pattern_detector.detect_class_patterns(node, source_code)
        if patterns:
            self.stats['patterns_detected'] += len(patterns)
        
        # Generate docstring
        docstring = self.docstring_builder.build_class_docstring(
            class_info, metrics, patterns
        )
        
        # Generate suggestions
        suggestions = self._generate_class_suggestions(class_info, metrics, patterns)
        
        # Calculate confidence
        confidence = self._calculate_confidence_score(class_info, metrics, patterns)
        
        return DocstringResult(
            element_type=CodeElementType.CLASS,
            element_name=class_info.name,
            file_path=file_path,
            line_number=node.lineno,
            generated_docstring=docstring,
            style=self.config.docstring_style,
            quality_score=metrics.quality_score,
            metrics=metrics,
            suggestions=suggestions,
            has_existing_docstring=class_info.existing_docstring is not None,
            confidence_score=confidence,
        )
    
    def _extract_function_info(self, node: ast.FunctionDef) -> FunctionInfo:
        """
        Extract comprehensive information from a function node.
        
        Args:
            node: Function AST node
            
        Returns:
            FunctionInfo object with all function details
        """
        info = FunctionInfo(
            name=node.name,
            is_async=isinstance(node, ast.AsyncFunctionDef),
        )
        
        # Check if it's a method
        if node.args.args and node.args.args[0].arg in ('self', 'cls'):
            info.is_method = True
        
        # Check for property decorator
        info.is_property = any(
            isinstance(d, ast.Name) and d.id == 'property'
            for d in node.decorator_list
        )
        
        # Extract parameters
        for arg in node.args.args:
            if arg.arg in ('self', 'cls'):
                continue
            
            param = ParameterInfo(
                name=arg.arg,
                type_hint=ast.unparse(arg.annotation) if arg.annotation else None,
            )
            info.parameters.append(param)
        
        # Add defaults
        defaults = node.args.defaults
        num_defaults = len(defaults)
        if num_defaults > 0:
            for i, default in enumerate(defaults):
                param_idx = len(info.parameters) - num_defaults + i
                if param_idx >= 0:
                    info.parameters[param_idx].default_value = ast.unparse(default)
        
        # Extract return type
        if node.returns:
            info.return_type = ast.unparse(node.returns)
        
        # Detect raised exceptions
        for child in ast.walk(node):
            if isinstance(child, ast.Raise) and child.exc:
                exc_name = ast.unparse(child.exc).split('(')[0]
                if exc_name not in info.raises:
                    info.raises.append(exc_name)
        
        # Extract decorators
        for decorator in node.decorator_list:
            info.decorators.append(ast.unparse(decorator))
        
        # Check for existing docstring
        if (node.body and isinstance(node.body[0], ast.Expr) and
                isinstance(node.body[0].value, ast.Constant) and
                isinstance(node.body[0].value.value, str)):
            info.existing_docstring = node.body[0].value.value
        
        return info
    
    def _extract_class_info(self, node: ast.ClassDef) -> ClassInfo:
        """
        Extract comprehensive information from a class node.
        
        Args:
            node: Class AST node
            
        Returns:
            ClassInfo object with all class details
        """
        info = ClassInfo(name=node.name)
        
        # Extract base classes
        for base in node.bases:
            info.bases.append(ast.unparse(base))
        
        # Extract methods and attributes
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                info.methods.append(item.name)
            elif isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                info.attributes.append(item.target.id)
            elif isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        info.attributes.append(target.id)
        
        # Extract decorators
        for decorator in node.decorator_list:
            info.decorators.append(ast.unparse(decorator))
        
        # Check for existing docstring
        if (node.body and isinstance(node.body[0], ast.Expr) and
                isinstance(node.body[0].value, ast.Constant) and
                isinstance(node.body[0].value.value, str)):
            info.existing_docstring = node.body[0].value.value
        
        return info
    
    def _calculate_quality_score(self, metrics: CodeMetrics, 
                                 func_info: FunctionInfo) -> float:
        """
        Calculate quality score for a function.
        
        Args:
            metrics: Code metrics
            func_info: Function information
            
        Returns:
            Quality score (0-100)
        """
        score = 100.0
        
        # Penalize high complexity
        if metrics.cyclomatic_complexity > 10:
            score -= (metrics.cyclomatic_complexity - 10) * 5
        
        # Penalize long functions
        if metrics.lines_of_code > 50:
            score -= (metrics.lines_of_code - 50) * 0.5
        
        # Penalize many parameters
        if metrics.num_parameters > 5:
            score -= (metrics.num_parameters - 5) * 10
        
        # Reward type hints
        if metrics.has_type_hints:
            score += 15
        else:
            score -= 10
        
        # Reward existing docstring
        if func_info.existing_docstring:
            score += 10
        
        # Reward decorators (indicates thoughtful design)
        if func_info.decorators:
            score += 5
        
        return max(0.0, min(100.0, score))
    
    def _calculate_class_quality_score(self, metrics: CodeMetrics, 
                                       class_info: ClassInfo) -> float:
        """
        Calculate quality score for a class.
        
        Args:
            metrics: Code metrics
            class_info: Class information
            
        Returns:
            Quality score (0-100)
        """
        score = 100.0
        
        # Reward appropriate method count
        num_methods = len(class_info.methods)
        if num_methods == 0:
            score -= 20
        elif num_methods > 20:
            score -= (num_methods - 20) * 2
        
        # Reward documentation
        if class_info.existing_docstring:
            score += 15
        
        # Reward inheritance (but not too much)
        if 1 <= len(class_info.bases) <= 2:
            score += 10
        elif len(class_info.bases) > 2:
            score -= 10
        
        # Reward attributes
        if class_info.attributes:
            score += 5
        
        return max(0.0, min(100.0, score))
    
    def _calculate_confidence_score(self, info: Any, metrics: CodeMetrics, 
                                    patterns: List[str]) -> float:
        """
        Calculate AI confidence in generated docstring.
        
        CREATIVE FEATURE: Confidence scoring
        
        Args:
            info: Function or class info
            metrics: Code metrics
            patterns: Detected patterns
            
        Returns:
            Confidence score (0-100)
        """
        confidence = 70.0  # Base confidence
        
        # Increase confidence with type hints
        if metrics.has_type_hints:
            confidence += 15
        
        # Increase confidence with detected patterns
        if patterns:
            confidence += min(10, len(patterns) * 3)
        
        # Decrease confidence for complex code
        if metrics.cyclomatic_complexity > 15:
            confidence -= 10
        
        # Increase confidence if we have existing docstring to reference
        if hasattr(info, 'existing_docstring') and info.existing_docstring:
            confidence += 10
        
        return max(0.0, min(100.0, confidence))
    
    def _generate_suggestions(self, func_info: FunctionInfo, 
                             metrics: CodeMetrics, patterns: List[str]) -> List[Suggestion]:
        """
        Generate improvement suggestions for a function.
        
        Args:
            func_info: Function information
            metrics: Code metrics
            patterns: Detected patterns
            
        Returns:
            List of suggestions
        """
        suggestions = []
        
        # Type hint suggestions
        if not metrics.has_type_hints:
            suggestions.append(Suggestion(
                category='type_hints',
                severity='warning',
                message='Consider adding type hints to improve code clarity and enable static type checking'
            ))
        
        # Complexity suggestions
        if metrics.cyclomatic_complexity > 10:
            suggestions.append(Suggestion(
                category='complexity',
                severity='warning',
                message=f'High cyclomatic complexity ({metrics.cyclomatic_complexity}). Consider refactoring into smaller functions'
            ))
        
        # Parameter count suggestions
        if metrics.num_parameters > 5:
            suggestions.append(Suggestion(
                category='parameters',
                severity='info',
                message=f'Function has {metrics.num_parameters} parameters. Consider using a configuration object or dataclass'
            ))
        
        # Docstring suggestions
        if not func_info.existing_docstring:
            suggestions.append(Suggestion(
                category='documentation',
                severity='error',
                message='Missing docstring. Add documentation to improve code maintainability'
            ))
        
        return suggestions
    
    def _generate_class_suggestions(self, class_info: ClassInfo, 
                                    metrics: CodeMetrics, patterns: List[str]) -> List[Suggestion]:
        """
        Generate improvement suggestions for a class.
        
        Args:
            class_info: Class information
            metrics: Code metrics
            patterns: Detected patterns
            
        Returns:
            List of suggestions
        """
        suggestions = []
        
        # Docstring suggestions
        if not class_info.existing_docstring:
            suggestions.append(Suggestion(
                category='documentation',
                severity='error',
                message='Missing class docstring. Add documentation to describe the class purpose'
            ))
        
        # Method count suggestions
        if len(class_info.methods) == 0:
            suggestions.append(Suggestion(
                category='design',
                severity='warning',
                message='Class has no methods. Consider if a dataclass or named tuple would be more appropriate'
            ))
        
        # Inheritance suggestions
        if len(class_info.bases) > 3:
            suggestions.append(Suggestion(
                category='design',
                severity='warning',
                message='Multiple inheritance detected. Consider composition over inheritance'
            ))
        
        return suggestions
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get agent statistics.
        
        CREATIVE FEATURE: Statistics tracking
        
        Returns:
            Dictionary of statistics
        """
        return self.stats.copy()
    
    def generate_report(self, results: List[DocstringResult]) -> AnalysisReport:
        """
        Generate a comprehensive analysis report.
        
        Args:
            results: List of docstring results
            
        Returns:
            AnalysisReport with summary statistics
        """
        file_paths = list(set(r.file_path for r in results))
        
        report = AnalysisReport(
            file_paths=file_paths,
            results=results,
            timestamp=datetime.now().isoformat()
        )
        
        report.calculate_summary()
        return report
