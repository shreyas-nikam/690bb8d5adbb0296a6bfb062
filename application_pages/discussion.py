import streamlit as st

# Discussion of Results Page

def main():
    st.markdown("""
    ## Section 11: Discussion of Results and Learning Outcomes
    
    Through this simulation, we have observed the tangible impacts of various AI security vulnerabilities on an agentic industrial safety monitoring system. The lab provided a hands-on experience in:

    - **Identifying Vulnerabilities**: We saw how 'synthetic-identity risk' and 'untraceable data leakage' manifest through changes in system alerts and agent integrity.
    - **Adversarial Testing**: The simulation of 'prompt injection' and 'data poisoning' illustrated how malicious inputs can significantly alter system behavior and outputs, mirroring how such attacks can 'hijack LLM behavior'.
    - **Analyzing Defenses**: By manipulating `Attack Intensity` and `Attack Type`, users can infer the necessity of robust 'risk controls in the assurance plan' and 'red teaming chains of agents' for continuous validation.
    - **Understanding System Response**: The plots revealed how an attack can increase alert frequency and potentially lengthen detection latency, emphasizing the need for adaptive systems to implement effective defenses.

    This practical exposure reinforces the theoretical concepts of AI security and the importance of rigorous testing and validation in building trustworthy AI systems.
    """)