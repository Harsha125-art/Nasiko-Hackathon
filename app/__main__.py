#!/usr/bin/env python3
"""
Main entry point for the Docstring Generation Agent.

This module serves as the primary interface for running the agent,
providing CLI interactions and orchestrating the docstring generation process.
"""

import sys
import argparse
from pathlib import Path
from typing import Optional

from app.agents import DocstringAgent
from app.config import Config
from app.models import DocstringStyle, OutputFormat
from app.tools import FileHandler, DisplayFormatter


def parse_arguments():
    """
    Parse command-line arguments for the docstring agent.
    
    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="Advanced Docstring Generation Agent with AI-powered analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate docstrings for a single file
  python -m app myfile.py
  
  # Generate with specific style
  python -m app myfile.py --style numpy
  
  # Analyze entire directory
  python -m app ./src --recursive
  
  # Export as JSON report
  python -m app myfile.py --format json --output report.json
  
  # Interactive mode
  python -m app --interactive
        """
    )
    
    parser.add_argument(
        'path',
        nargs='?',
        type=str,
        help='Python file or directory to process'
    )
    
    parser.add_argument(
        '-s', '--style',
        type=str,
        choices=['google', 'numpy', 'sphinx'],
        default='google',
        help='Docstring style to use (default: google)'
    )
    
    parser.add_argument(
        '-r', '--recursive',
        action='store_true',
        help='Process directories recursively'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output file path for generated documentation'
    )
    
    parser.add_argument(
        '-f', '--format',
        type=str,
        choices=['console', 'json', 'markdown', 'html'],
        default='console',
        help='Output format (default: console)'
    )
    
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Run in interactive mode'
    )
    
    parser.add_argument(
        '--inplace',
        action='store_true',
        help='Modify files in-place to add docstrings'
    )
    
    parser.add_argument(
        '--min-quality',
        type=float,
        default=0.0,
        help='Minimum quality score to report (0-100)'
    )
    
    parser.add_argument(
        '--show-metrics',
        action='store_true',
        help='Show detailed code metrics'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Verbose output with detailed analysis'
    )
    
    return parser.parse_args()


def interactive_mode():
    """
    Run the agent in interactive mode.
    
    Provides a user-friendly interface for analyzing code snippets
    or files with real-time feedback.
    """
    print("🤖 Docstring Generation Agent - Interactive Mode")
    print("=" * 60)
    print("\nCommands:")
    print("  file <path>     - Analyze a Python file")
    print("  code <snippet>  - Analyze code snippet (end with 'END')")
    print("  style <style>   - Change docstring style (google/numpy/sphinx)")
    print("  help            - Show this help")
    print("  quit            - Exit interactive mode")
    print("=" * 60)
    
    config = Config()
    agent = DocstringAgent(config)
    current_style = DocstringStyle.GOOGLE
    
    while True:
        try:
            command = input("\n> ").strip()
            
            if not command:
                continue
            
            if command.lower() in ('quit', 'exit', 'q'):
                print("👋 Goodbye!")
                break
            
            elif command.lower() == 'help':
                print("\n📚 Available Commands:")
                print("  file <path>  - Analyze a Python file")
                print("  style google - Set Google-style docstrings")
                print("  style numpy  - Set NumPy-style docstrings")
                print("  style sphinx - Set Sphinx-style docstrings")
                print("  quit         - Exit")
            
            elif command.startswith('file '):
                file_path = command[5:].strip()
                if Path(file_path).exists():
                    print(f"\n📄 Analyzing: {file_path}")
                    results = agent.process_file(file_path)
                    DisplayFormatter.display_results(results, verbose=True)
                else:
                    print(f"❌ File not found: {file_path}")
            
            elif command.startswith('style '):
                style_name = command[6:].strip().lower()
                if style_name in ('google', 'numpy', 'sphinx'):
                    current_style = DocstringStyle(style_name)
                    agent.config.docstring_style = current_style
                    print(f"✅ Style changed to: {style_name}")
                else:
                    print("❌ Invalid style. Use: google, numpy, or sphinx")
            
            else:
                print("❌ Unknown command. Type 'help' for available commands.")
        
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    """
    Main function to run the docstring generation agent.
    
    Handles command-line arguments, processes files, and generates
    comprehensive documentation with quality metrics.
    """
    args = parse_arguments()
    
    # Interactive mode
    if args.interactive:
        interactive_mode()
        return
    
    # Validate input
    if not args.path:
        print("❌ Error: Please provide a file or directory path")
        print("Use --help for usage information")
        sys.exit(1)
    
    # Initialize configuration
    config = Config()
    config.docstring_style = DocstringStyle(args.style)
    config.output_format = OutputFormat(args.format)
    config.min_quality_score = args.min_quality
    config.show_metrics = args.show_metrics
    config.verbose = args.verbose
    config.modify_inplace = args.inplace
    
    # Initialize agent
    agent = DocstringAgent(config)
    
    # Process path
    path = Path(args.path)
    
    if not path.exists():
        print(f"❌ Error: Path not found: {args.path}")
        sys.exit(1)
    
    print(f"🤖 Docstring Generation Agent")
    print("=" * 60)
    print(f"📂 Target: {path}")
    print(f"📝 Style: {args.style}")
    print(f"📊 Format: {args.format}")
    print("=" * 60)
    
    all_results = []
    
    if path.is_file():
        if path.suffix == '.py':
            results = agent.process_file(str(path))
            all_results.extend(results)
        else:
            print(f"❌ Error: Not a Python file: {path}")
            sys.exit(1)
    
    elif path.is_dir():
        pattern = '**/*.py' if args.recursive else '*.py'
        python_files = list(path.glob(pattern))
        
        if not python_files:
            print(f"❌ No Python files found in: {path}")
            sys.exit(1)
        
        print(f"\n🔍 Found {len(python_files)} Python file(s)")
        
        for py_file in python_files:
            print(f"\n📄 Processing: {py_file}")
            try:
                results = agent.process_file(str(py_file))
                all_results.extend(results)
            except Exception as e:
                print(f"❌ Error processing {py_file}: {e}")
    
    # Display or save results
    if args.output:
        FileHandler.save_results(
            all_results,
            args.output,
            output_format=config.output_format
        )
        print(f"\n✅ Results saved to: {args.output}")
    else:
        DisplayFormatter.display_results(
            all_results,
            verbose=args.verbose,
            show_metrics=args.show_metrics
        )
    
    # Summary statistics
    if all_results:
        print("\n" + "=" * 60)
        print("📊 Summary Statistics")
        print("=" * 60)
        
        total = len(all_results)
        avg_quality = sum(r.quality_score for r in all_results) / total
        high_quality = sum(1 for r in all_results if r.quality_score >= 80)
        needs_improvement = sum(1 for r in all_results if r.quality_score < 60)
        
        print(f"Total items analyzed: {total}")
        print(f"Average quality score: {avg_quality:.1f}/100")
        print(f"High quality (≥80): {high_quality}")
        print(f"Needs improvement (<60): {needs_improvement}")
        
        if args.inplace:
            print(f"\n✅ Files modified in-place with generated docstrings")


if __name__ == '__main__':
    main()
