🤖 DocStream AI: Advanced Docstring Generation Agent
DocStream AI is an intelligent, agentic tool that transforms raw Python code into production-ready documentation. By combining AST-based structural analysis with AI-powered semantic understanding, it generates high-quality docstrings, calculates code health metrics, and detects complex design patterns in real-time.

🚀 New: Interactive Web Dashboard
We have launched a Streamlit-powered Web UI that allows you to:

Live Preview: Paste code and see documentation generated instantly.

Style Toggle: Switch between Google, NumPy, and Sphinx styles on the fly.

Quality Metrics: Visualize complexity and maintainability scores with color-coded grades.

AI Enhancement: Toggle LLM-powered semantic descriptions for deeper code understanding.

🎯 Key Features
🧠 Intelligent Analysis
AST Parsing: Deep structural analysis using Python's Abstract Syntax Tree.

Smart Pattern Detection: Automatically recognizes Singleton, Factory, and Builder patterns.

Type Hint Validation: Infers missing types and validates existing annotations.

Complexity Scoring: Calculates Cyclomatic Complexity to flag hard-to-maintain code.

🎨 Creative & Unique Features
Context-Aware Descriptions: Uses function semantics to write descriptions that make sense, not just repeat the function name.

Auto-Example Generation: Injects practical doctest style examples into your documentation.

Confidence Scoring: An AI-driven rating (0-100) reflecting how accurately the agent understood your logic.

Best Practice Guardrails: Flags high parameter counts, missing returns, and suggests refactoring.

📁 Project Structure
Plaintext
EPOCHAGENTICEMPLATE/
├── app/                  # Core Agent Logic
│   ├── agents.py         # The DocstringAgent implementation
│   ├── tools.py          # AST Analyzers & Pattern Detectors
│   ├── config.py         # Configuration & API Management
│   └── models.py         # Data Structures & Result Objects
├── streamlit_app.py      # NEW: Interactive Web Interface
├── requirements.txt      # Project Dependencies
├── .env.example          # Template for API Keys
└── README.md             # You are here!
🛠️ Installation & Setup
1. Clone & Install
Bash
git clone <your-repo-url>
cd EPOCHAGENTICEMPLATE
pip install -r requirements.txt
2. Configure AI (Optional)
To enable AI-Enhanced Descriptions, create a .env file in the root directory:

Bash
OPENAI_API_KEY=your_actual_key_here
💻 How to Use
Option A: Web Interface (Recommended)
Launch the dashboard to process code via your browser:

Bash
streamlit run streamlit_app.py
Option B: Command Line
Analyze files directly from your terminal:

Bash
# Analyze a single file
python -m app myfile.py --style google

# Interactive CLI mode
python -m app --interactive
📊 Evaluation & Grading
The agent assigns a Quality Grade to every function and class:

Grade A (90-100): Perfectly documented, low complexity.

Grade B (80-89): Good documentation, standard complexity.

Grade C (70-79): Acceptable, but needs more type hints.

Grade D/F (<70): High complexity or missing critical info.

🏆 Hackathon Highlights
Zero-Config: Works out of the box using Python's standard library.

Hybrid Intelligence: Uses deterministic AST rules for structure and LLMs for semantics.

Developer First: Focuses on reducing the "documentation tax" for engineers.

📝 License
Distributed under the MIT License. See LICENSE for more information.

Author: [Your Name/Team Name]

Event: AI Agents Hackathon 2026