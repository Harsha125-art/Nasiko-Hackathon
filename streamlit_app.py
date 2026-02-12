import streamlit as st
import os
from app.agents import DocstringAgent
from app.config import Config
from app.models import DocstringStyle

st.set_page_config(page_title="🤖 Docstring AI Agent", layout="wide")

# Sidebar for Configuration
with st.sidebar:
    st.title("Settings")
    style = st.selectbox("Docstring Style", ["google", "numpy", "sphinx"])
    ai_on = st.toggle("AI Enhancement", value=True)
    
    if not os.getenv("OPENAI_API_KEY"):
        st.warning("⚠️ No API Key found in .env")
    
    st.divider()
    st.markdown("### How to use")
    st.info("Paste your Python code in the main box and click 'Generate'. You can download the full documentation once finished.")

# Main UI
st.title("🤖 Advanced Docstring Generation Agent")
st.markdown("Analyze patterns and generate documentation for your Python projects.")

code_input = st.text_area("Paste Python Code Here:", height=300, placeholder="def my_function(x): ...")

# Use columns to position the buttons nicely
col1, col2 = st.columns([1, 5])

with col1:
    generate_btn = st.button("🚀 Generate")

# Logic to handle generation and storage
if generate_btn:
    if code_input:
        with st.spinner("Agent is analyzing AST and patterns..."):
            # 1. Setup Config
            cfg = Config(
                docstring_style=DocstringStyle(style),
                ai_enhancement=ai_on
            )
            
            # 2. Initialize Agent
            agent = DocstringAgent(cfg)
            
            # 3. Process the code
            results = agent.process_code(code_input) 
            
            # 4. Save to session state so it persists for the download button
            st.session_state['results'] = results
            
            # Create a compiled string of all docstrings for downloading
            full_docs = ""
            for res in results:
                full_docs += f"# {res.element_name}\n{res.generated_docstring}\n\n"
            st.session_state['full_docs'] = full_docs
    else:
        st.error("Please enter some code first!")

# --- Display Results and Download Button ---
if 'results' in st.session_state:
    st.success("Analysis Complete!")
    
    # 📥 THE DOWNLOAD BUTTON
    st.download_button(
        label="📥 Download Documentation (.txt)",
        data=st.session_state['full_docs'],
        file_name="generated_docs.txt",
        mime="text/plain"
    )

    for res in st.session_state['results']:
        with st.expander(f"📦 {res.element_name} ({res.element_type})"):
            st.metric("Quality Score", f"{res.quality_score}/100")
            st.code(res.generated_docstring, language="python")