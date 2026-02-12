# 📦 Installation & Setup Guide

## Quick Setup (30 seconds)

```bash
# 1. Navigate to your project directory
cd /path/to/EPOCHAGENTICEMPLATE

# 2. Verify Python version (3.8+ required)
python --version

# 3. Run the agent!
python -m app sample_code.py
```

That's it! No dependencies to install. 🎉

## Detailed Setup

### Prerequisites

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **No external libraries required!**

### Step 1: Download Files

You should have the following files:

```
EPOCHAGENTICEMPLATE/
├── app/
│   ├── __init__.py
│   ├── __main__.py
│   ├── agents.py
│   ├── config.py
│   ├── models.py
│   └── tools.py
├── .gitignore
├── requirements.txt
├── README.md
├── QUICKSTART.md
├── PROJECT_SUMMARY.md
├── ARCHITECTURE.md
├── demo.py
└── sample_code.py
```

### Step 2: Verify Installation

```bash
# Check Python version
python --version
# Should show: Python 3.8.x or higher

# Verify package structure
python -c "import app; print('✅ Package OK')"
# Should print: ✅ Package OK

# Test the agent
python -m app sample_code.py
# Should display analysis results
```

### Step 3: Run Demo

```bash
python demo.py
```

This will demonstrate all features and confirm everything is working!

## File Placement Guide

### According to Your Structure

Based on the structure shown in your image:

```
app/
├── __init__.py          ← Copy this file here
├── __main__.py          ← Copy this file here  
├── agents.py            ← Copy this file here
├── config.py            ← Copy this file here
├── models.py            ← Copy this file here
└── tools.py             ← Copy this file here
```

### What Each File Does

| File | Purpose | Key Contents |
|------|---------|--------------|
| `__init__.py` | Package initialization | Exports, version info |
| `__main__.py` | CLI entry point | Argument parsing, main() |
| `agents.py` | Core agent logic | DocstringAgent class |
| `config.py` | Configuration | Config class, settings |
| `models.py` | Data structures | Dataclasses, enums |
| `tools.py` | Helper utilities | All helper classes |

## Testing Your Installation

### Test 1: Basic Functionality

```bash
python -m app sample_code.py
```

Expected output:
```
🤖 Docstring Generation Agent
============================================================
📂 Target: sample_code.py
📝 Style: google
📊 Format: console
============================================================
[... analysis results ...]
```

### Test 2: Different Styles

```bash
# Google style
python -m app sample_code.py --style google

# NumPy style
python -m app sample_code.py --style numpy

# Sphinx style
python -m app sample_code.py --style sphinx
```

### Test 3: Output Formats

```bash
# JSON output
python -m app sample_code.py --format json --output test.json

# Markdown output
python -m app sample_code.py --format markdown --output test.md

# HTML output
python -m app sample_code.py --format html --output test.html
```

### Test 4: Interactive Mode

```bash
python -m app --interactive
```

Then try:
```
> file sample_code.py
> help
> quit
```

### Test 5: Full Demo

```bash
python demo.py
```

## Common Issues & Solutions

### Issue 1: "ModuleNotFoundError: No module named 'app'"

**Solution**: Make sure you're running from the project root directory.

```bash
# Wrong
cd app
python -m app sample_code.py  # ❌

# Correct
cd EPOCHAGENTICEMPLATE
python -m app sample_code.py  # ✅
```

### Issue 2: "Python version too old"

**Solution**: Upgrade Python to 3.8 or higher.

```bash
# Check version
python --version

# If too old, install newer Python from python.org
```

### Issue 3: "File not found: sample_code.py"

**Solution**: The file must be in the same directory or provide full path.

```bash
# If in different directory
python -m app /path/to/myfile.py
```

### Issue 4: Import errors

**Solution**: Ensure all files are in the correct structure.

```bash
# Verify structure
ls -R app/
# Should show all 6 Python files
```

## Usage Examples

### Analyze Your Own Code

```bash
# Single file
python -m app /path/to/your/code.py

# Entire directory
python -m app /path/to/your/project --recursive

# With quality filter
python -m app your_code.py --min-quality 70
```

### Generate Documentation

```bash
# Markdown documentation
python -m app ./src --recursive --format markdown --output docs/api.md

# HTML report
python -m app ./src --recursive --format html --output docs/report.html

# JSON for CI/CD
python -m app ./src --recursive --format json --output quality-report.json
```

### Interactive Analysis

```bash
# Start interactive mode
python -m app --interactive

# Commands in interactive mode:
> file mycode.py              # Analyze file
> style numpy                 # Change style
> help                        # Show help
> quit                        # Exit
```

## Advanced Setup

### Optional: Create Virtual Environment

```bash
# Create venv (optional, but recommended)
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Now run the agent
python -m app sample_code.py
```

### Optional: Install Development Tools

While the agent needs no dependencies, you might want development tools:

```bash
# For code formatting
pip install black

# For linting
pip install pylint

# For testing
pip install pytest
```

### Optional: Add to PATH

To run from anywhere:

**Linux/macOS:**
```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="/path/to/EPOCHAGENTICEMPLATE:$PATH"

# Create alias
alias docgen="python -m app"

# Now you can run:
docgen myfile.py
```

**Windows:**
```batch
# Add to system PATH via System Properties
# Or create batch file in a PATH directory

# docgen.bat:
@echo off
python C:\path\to\EPOCHAGENTICEMPLATE\app myfile.py
```

## Integration with IDEs

### VS Code

1. Open the project folder in VS Code
2. Select Python interpreter (3.8+)
3. Run from terminal: `python -m app myfile.py`

Optional: Add to `.vscode/tasks.json`:
```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Analyze Docstrings",
            "type": "shell",
            "command": "python -m app ${file}",
            "group": "build",
            "presentation": {
                "reveal": "always"
            }
        }
    ]
}
```

### PyCharm

1. Open project in PyCharm
2. Set Python interpreter (3.8+)
3. Right-click on a .py file
4. "Run Python -m app"

Optional: Create run configuration:
- Script path: `-m app`
- Parameters: `${file}`

## Verification Checklist

Before using the agent, verify:

- [ ] Python 3.8+ installed
- [ ] All 6 files in `app/` directory
- [ ] Files: `__init__.py`, `__main__.py`, `agents.py`, `config.py`, `models.py`, `tools.py`
- [ ] Can import app: `python -c "import app"`
- [ ] Can run: `python -m app sample_code.py`
- [ ] Demo works: `python demo.py`

## Quick Reference

### Command Templates

```bash
# Basic analysis
python -m app <file.py>

# With options
python -m app <file.py> --style <google|numpy|sphinx> --format <console|json|markdown|html>

# Directory analysis
python -m app <directory> --recursive

# Export results
python -m app <file.py> --output <output-file>

# Interactive mode
python -m app --interactive

# Show help
python -m app --help
```

### Common Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--style` | Docstring style | `--style numpy` |
| `--recursive` | Analyze subdirectories | `--recursive` |
| `--output` | Output file | `--output report.json` |
| `--format` | Output format | `--format markdown` |
| `--min-quality` | Quality threshold | `--min-quality 70` |
| `--show-metrics` | Display metrics | `--show-metrics` |
| `--verbose` | Detailed output | `--verbose` |
| `--interactive` | Interactive mode | `--interactive` |
| `--inplace` | Modify files | `--inplace` |

## Next Steps

1. ✅ Complete installation
2. ✅ Run `python demo.py` to see features
3. ✅ Test with `sample_code.py`
4. ✅ Analyze your own code
5. ✅ Read `README.md` for full documentation
6. ✅ Check `QUICKSTART.md` for usage guide
7. ✅ Explore `ARCHITECTURE.md` to understand internals

## Support

If you encounter issues:

1. Check this installation guide
2. Verify Python version: `python --version`
3. Verify file structure: `ls -R app/`
4. Check import: `python -c "import app"`
5. Run demo: `python demo.py`

## Success!

If you see this output, you're ready to go:

```bash
$ python -m app sample_code.py

🤖 Docstring Generation Agent
============================================================
📂 Target: sample_code.py
📝 Style: google
📊 Format: console
============================================================
[... analysis results ...]
```

🎉 **Congratulations! Your installation is complete!**

Start analyzing code and generating high-quality docstrings! 🚀
