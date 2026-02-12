#!/usr/bin/env python3
"""
Demo script for the Docstring Generation Agent.

This script demonstrates all the creative and unique features of the agent.
"""

from app.agents import DocstringAgent
from app.config import Config
from app.models import DocstringStyle, OutputFormat
from app.tools import DisplayFormatter


def main():
    """Run the demo showcasing all agent features."""
    
    print("🎯 Docstring Generation Agent - Feature Showcase")
    print("=" * 70)
    print()
    
    # Feature 1: Multi-Style Support
    print("📝 FEATURE 1: Multi-Style Docstring Generation")
    print("-" * 70)
    print("Supporting Google, NumPy, and Sphinx styles")
    print()
    
    for style in [DocstringStyle.GOOGLE, DocstringStyle.NUMPY, DocstringStyle.SPHINX]:
        print(f"\n🎨 Testing {style.value.upper()} style:")
        config = Config(docstring_style=style, show_metrics=False)
        agent = DocstringAgent(config)
        
        results = agent.process_file('sample_code.py')
        if results:
            result = results[0]  # Show first result
            print(f"   Element: {result.element_name}")
            print(f"   Preview: {result.generated_docstring[:100]}...")
    
    # Feature 2: Pattern Detection
    print("\n\n🔍 FEATURE 2: Smart Pattern Detection")
    print("-" * 70)
    config = Config(docstring_style=DocstringStyle.GOOGLE)
    agent = DocstringAgent(config)
    results = agent.process_file('sample_code.py')
    
    print("Detected patterns in sample_code.py:")
    pattern_count = 0
    for result in results:
        if hasattr(result, 'patterns'):
            print(f"   • {result.element_name}: Found patterns!")
            pattern_count += 1
    
    stats = agent.get_statistics()
    print(f"\nTotal patterns detected: {stats.get('patterns_detected', 0)}")
    print(f"Examples generated: {stats.get('examples_generated', 0)}")
    
    # Feature 3: Quality Scoring
    print("\n\n📊 FEATURE 3: Code Quality Scoring")
    print("-" * 70)
    print("Quality analysis for all code elements:\n")
    
    for result in results[:5]:  # Show first 5
        grade = result.metrics.get_quality_grade()
        complexity = result.metrics.get_complexity_level()
        print(f"   {result.element_name:30} | Score: {result.quality_score:5.1f} | Grade: {grade} | Complexity: {complexity}")
    
    # Feature 4: Comprehensive Metrics
    print("\n\n📈 FEATURE 4: Code Metrics Analysis")
    print("-" * 70)
    if results:
        result = results[0]
        print(f"\nDetailed metrics for '{result.element_name}':")
        print(f"   Cyclomatic Complexity: {result.metrics.cyclomatic_complexity}")
        print(f"   Lines of Code: {result.metrics.lines_of_code}")
        print(f"   Parameters: {result.metrics.num_parameters}")
        print(f"   Return Statements: {result.metrics.num_return_statements}")
        print(f"   Has Type Hints: {'✅ Yes' if result.metrics.has_type_hints else '❌ No'}")
        print(f"   Maintainability Index: {result.metrics.maintainability_index:.1f}/100")
    
    # Feature 5: Best Practice Suggestions
    print("\n\n💡 FEATURE 5: Best Practice Suggestions")
    print("-" * 70)
    suggestion_count = 0
    for result in results:
        if result.suggestions:
            print(f"\n   {result.element_name}:")
            for sug in result.suggestions[:2]:  # Show max 2 per element
                icon = "⚠️" if sug.severity == "warning" else "ℹ️" if sug.severity == "info" else "❌"
                print(f"      {icon} [{sug.category}] {sug.message}")
                suggestion_count += 1
    
    print(f"\nTotal suggestions generated: {suggestion_count}")
    
    # Feature 6: Multiple Output Formats
    print("\n\n📤 FEATURE 6: Multiple Output Formats")
    print("-" * 70)
    print("Agent supports:")
    print("   • Console output (colored and formatted)")
    print("   • JSON export (for programmatic access)")
    print("   • Markdown export (for documentation)")
    print("   • HTML export (for web viewing)")
    
    # Feature 7: Statistics Tracking
    print("\n\n📊 FEATURE 7: Statistics Tracking")
    print("-" * 70)
    stats = agent.get_statistics()
    print(f"   Total analyzed: {stats['total_analyzed']}")
    print(f"   Functions: {stats['total_functions']}")
    print(f"   Classes: {stats['total_classes']}")
    print(f"   Patterns detected: {stats['patterns_detected']}")
    print(f"   Examples generated: {stats['examples_generated']}")
    
    # Feature 8: Confidence Scoring
    print("\n\n🎯 FEATURE 8: AI Confidence Scoring")
    print("-" * 70)
    print("Confidence scores for generated docstrings:\n")
    for result in results[:5]:
        confidence = result.confidence_score
        bar = "█" * int(confidence / 10)
        print(f"   {result.element_name:30} | {confidence:5.1f}% {bar}")
    
    # Summary
    print("\n\n" + "=" * 70)
    print("🎉 Demo Complete!")
    print("=" * 70)
    print("\n✨ Unique Features Demonstrated:")
    print("   1. ✅ Multi-style docstring generation (Google, NumPy, Sphinx)")
    print("   2. ✅ Smart pattern detection (Factory, Singleton, etc.)")
    print("   3. ✅ Code quality scoring and grading")
    print("   4. ✅ Comprehensive code metrics")
    print("   5. ✅ Best practice suggestions")
    print("   6. ✅ Multiple output formats")
    print("   7. ✅ Statistics tracking")
    print("   8. ✅ AI confidence scoring")
    print("   9. ✅ Automatic example generation")
    print("   10. ✅ Context-aware descriptions")
    
    print("\n💡 Try it yourself:")
    print("   python -m app sample_code.py --style google --show-metrics")
    print("   python -m app sample_code.py --format json --output report.json")
    print("   python -m app --interactive")
    print()


if __name__ == '__main__':
    main()
