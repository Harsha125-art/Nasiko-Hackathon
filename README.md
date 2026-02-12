# 🤖 DocStream AI: Advanced Docstring Generation Agent

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B.svg)](https://streamlit.io/)


**DocStream AI** is an intelligent, agentic tool that transforms raw Python code into production-ready documentation. By combining **AST-based structural analysis** with **AI-powered semantic understanding**, it generates high-quality docstrings, calculates code health metrics, and detects complex design patterns in real-time.

---

## 🚀 Interactive Web Dashboard
We have launched a **Streamlit-powered Web UI** for a seamless developer experience:

* **Live Preview**: Paste code and see documentation generated instantly.
* **Style Toggle**: Switch between **Google, NumPy, and Sphinx** styles on the fly.
* **Quality Metrics**: Visualize complexity and maintainability scores with color-coded grades.
* **AI Enhancement**: Toggle LLM-powered semantic descriptions for deeper code understanding.

---

## 🎯 Key Features

### 🧠 Intelligent Analysis
* **AST Parsing**: Deep structural analysis using Python's Abstract Syntax Tree.
* **Smart Pattern Detection**: Automatically recognizes **Singleton, Factory, and Builder** patterns.
* **Type Hint Validation**: Infers missing types and validates existing annotations.
* **Complexity Scoring**: Calculates **Cyclomatic Complexity** to flag hard-to-maintain code.

### 🎨 Creative & Unique Features
* **Context-Aware Descriptions**: Uses function semantics to write descriptions that make sense, not just repeat the function name.
* **Auto-Example Generation**: Injects practical `doctest` style examples into your documentation.
* **Confidence Scoring**: An AI-driven rating (0-100) reflecting how accurately the agent understood your logic.
* **Best Practice Guardrails**: Flags high parameter counts, missing returns, and suggests refactoring.

---

## 📁 Project Structure

```text
EPOCHAGENTICEMPLATE/
├── app/                  # Core Agent Logic
│   ├── agents.py         # The DocstringAgent implementation
│   ├── tools.py          # AST Analyzers & Pattern Detectors
│   ├── config.py         # Configuration & API Management
│   └── models.py         # Data Structures & Result Objects
├── streamlit_app.py      # NEW: Interactive Web Interface
├── requirements.txt      # Project Dependencies

```
## 🛠️ Installation & Setup
1. Clone & Install
 ```text
# Clone the repository
git clone [https://github.com/Harsha125-art/Nasiko-Hackathon.git](https://github.com/Harsha125-art/Nasiko-Hackathon.git)

# Enter the project directory
cd EPOCHAGENTICEMPLATE

# Install dependencies
pip install -r requirements.txt
```
## 2. Configure AI (Optional)
To enable AI-Enhanced Descriptions, create a .env file in the root directory and add your key:
 ```text
OPENAI_API_KEY=your_actual_key_here
```

## 💻 How to Use
Option A: Web Interface (Recommended)
Launch the dashboard to process code via your browser:

 ```text
streamlit run streamlit_app.py
```
## Option B: Command Line
Analyze files directly from your terminal:
 ```text
# Analyze a single file
python -m app myfile.py --style google

# Interactive CLI mode
python -m app --interactive
```
## 📊 Evaluation & Grading
The agent assigns a Quality Grade based on maintainability and documentation depth:
 ```text
Grade,Score,Description
Grade A,90-100,"Perfectly documented, low complexity."
Grade B,80-89,"Good documentation, standard complexity."
Grade C,70-79,"Acceptable, but needs more type hints."
Grade D/F,<70,High complexity or missing critical info.
```


   





├── .env.example          # Template for API Keys
└── README.md             # You are here!
ts Hackathon 2026
