"""
Tools for the agent.
Define your LangChain tools here.
"""
from typing import List, Dict, Any
from langchain.tools import tool

# Example tool
@tool
def calculator(expression: str) -> str:
    """
    Evaluate a math expression.
    Example: "2 + 2 * 10"
    """
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {str(e)}"
    

