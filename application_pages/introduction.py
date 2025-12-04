import streamlit as st

def main():
    st.markdown(r"""
    # AI Security Vulnerability Simulation Lab

    This Streamlit application serves as an "AI Security Vulnerability Simulation Lab," designed to provide hands-on experience in identifying, understanding, and analyzing AI-security vulnerabilities within agentic AI systems used for industrial safety monitoring.

    #### Learning Outcomes
    -   Understand the key insights contained in the uploaded document and supporting data.
    -   Identify common AI-security vulnerabilities, including 'synthetic-identity risk' and 'untraceable data leakage'.
    -   Learn about adversarial testing techniques like prompt injection and data poisoning.
    -   Analyze the effectiveness of different defense strategies and risk controls in mitigating AI security threats.

    #### Scope and Constraints
    This lab is designed to execute end-to-end on a mid-spec laptop (8 GB RAM) in fewer than 5 minutes. It exclusively uses open-source Python libraries from PyPI. All major steps include both code comments and brief narrative cells explaining 'what' is happening and 'why'.
    """)
    