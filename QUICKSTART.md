# 🚀 Quick Start Guide

Get started with the Docstring Generation Agent in 5 minutes!

## 📋 Prerequisites

- Python 3.8 or higher
- No external dependencies required!

## 🏃 Quick Start

### 1. Basic Usage

```bash
# Analyze a single file
python -m app sample_code.py
```

This will analyze `sample_code.py` and display:
- Generated docstrings
- Quality scores
- Code metrics
- Improvement suggestions

### 2. Try Different Styles

```bash
# Google style (default)
python -m app sample_code.py --style google

# NumPy style
python -m app sample_code.py --style numpy

# Sphinx style
python -m app sample_code.py --style sphinx
```

### 3. View Detailed Metrics

```bash
python -m app sample_code.py --show-metrics --verbose
```

### 4. Export Results

```bash
# Export to JSON
python -m app sample_code.py --format json --output report.json

# Export to Markdown
python -m app sample_code.py --format markdown --output report.md

# Export to HTML
python -m app sample_code.py --format html --output report.html
```

### 5. Analyze Multiple Files

```bash
# Analyze all Python files in a directory
python -m app ./your_project --recursive
```

### 6. Interactive Mode

```bash
python -m app --interactive
```

Then try:
```
> file sample_code.py
> style numpy
> help
> quit
```

### 7. Run the Demo

```bash
python demo.py
```

This showcases all the unique features!

## 📚 Common Use Cases

### Generate Documentation for Your Project

```bash
python -m app ./src --recursive --format markdown --output docs/docstrings.md
```

### Find Code Quality Issues

```bash
python -m app ./src --min-quality 70 --show-metrics
```

### Add Docstrings to Files (In-Place)

```bash
python -m app myfile.py --inplace
```

⚠️ **Warning**: This modifies your files! Make sure you have backups or use version control.

## 🎯 What Gets Analyzed?

The agent analyzes and generates docstrings for:

- ✅ **Functions**: All standalone functions
- ✅ **Methods**: Class methods (including static and class methods)
- ✅ **Classes**: Class definitions
- ✅ **Async Functions**: Coroutines and async methods

## 🔍 What Information Is Generated?

For each code element, you get:

1. **Docstring** in your chosen style
2. **Quality Score** (0-100)
3. **Complexity Metrics**
   - Cyclomatic complexity
   - Lines of code
   - Parameter count
4. **Type Hints Analysis**
5. **Pattern Detection**
6. **Best Practice Suggestions**
7. **Usage Examples** (for complex functions)

## 💡 Pro Tips

1. **Use `--verbose` for detailed analysis**
   ```bash
   python -m app myfile.py --verbose
   ```

2. **Filter by quality score**
   ```bash
   python -m app myfile.py --min-quality 80
   ```

3. **Combine options**
   ```bash
   python -m app ./src --recursive --style google --format json --output report.json --min-quality 70
   ```

4. **Use interactive mode for experimentation**
   ```bash
   python -m app --interactive
   ```

## 🎨 Understanding Output

### Quality Grades

- **A (90-100)**: Excellent - well-documented, low complexity
- **B (80-89)**: Good - minor improvements possible
- **C (70-79)**: Acceptable - some issues to address
- **D (60-69)**: Needs work - several issues
- **F (<60)**: Poor - requires attention

### Complexity Levels

- **Low (1-5)**: Simple, easy to understand
- **Moderate (6-10)**: Reasonable complexity
- **High (11-20)**: Complex, consider refactoring
- **Very High (>20)**: Too complex, definitely refactor

## 🐛 Troubleshooting

### Import Error

```bash
# Make sure you're in the project root directory
cd /path/to/EPOCHAGENTICEMPLATE
python -m app sample_code.py
```

### Syntax Error

If you get a syntax error analyzing a file:
- The file must be valid Python code
- Check for syntax errors in your source file

### No Results

If no results are shown:
- Make sure the file contains functions or classes
- Check that the file has a `.py` extension

## 📖 Next Steps

1. Read the full [README.md](README.md) for detailed documentation
2. Explore the code in `app/` to understand the implementation
3. Run `python demo.py` to see all features
4. Try the interactive mode: `python -m app --interactive`

## 🎓 Example Session

```bash
# Start with the sample file
$ python -m app sample_code.py --style google

🤖 Docstring Generation Agent
============================================================
📂 Target: sample_code.py
📝 Style: google
📊 Format: console
============================================================

🔍 Found 1 Python file(s)

📄 Processing: sample_code.py

============================================================
[1/5] DataProcessor (class)
============================================================
📂 File: sample_code.py:3
📊 Quality: 75.0/100 (Grade: C)

📈 Metrics:
   Complexity: 2 (Low)
   Lines of Code: 25
   Parameters: 3
   Type Hints: ❌
   Maintainability: 93.0/100

📝 Generated Docstring (google):
----------------------------------------------------------------------
DataProcessor class implementation.

Design Pattern: Dataclass

Attributes:
    name: Name
    config: Config
    _cache: Cache
----------------------------------------------------------------------

[... more results ...]

============================================================
📊 Summary Statistics
============================================================
Total items analyzed: 7
Average quality score: 78.5/100
High quality (≥80): 3
Needs improvement (<60): 0
```

## 🎉 You're Ready!

Start analyzing your code and generating high-quality docstrings! 🚀
