import streamlit as st

# Mathematical Foundations Page

def main():
    st.markdown(r"""
    ## Section 4: Mathematical Foundations of Attack Simulation
    
    To simulate the impact of AI security vulnerabilities concretely, we define mathematical relationships that govern how attacks influence key system metrics. These relationships ensure a quantifiable and consistent effect based on the chosen attack parameters.

    #### Alert Frequency Over Time
    The alert frequency under attack, $$F_{alerts\_attacked}(t)$$, is modeled as an increase over the baseline frequency, $$F_{alerts\_base}(t)$$, proportional to the attack intensity and a type-specific coefficient:
    $$F_{alerts\_attacked}(t) = F_{alerts\_base}(t) \cdot (1 + A_{intensity} \cdot C_{type})$$
    Where:
    - $$A_{intensity}$$ is the user-defined attack intensity, $$A_{intensity} \in [0, 1]$$.
    - $$C_{type}$$ is a scaling factor specific to the `Attack Type`, reflecting its inherent impact potential (e.g., a data poisoning attack might have a higher $$C_{type}$$ than a mild prompt injection).

    #### Detection Latency
    The simulated detection latency, $$L_{detection}$$, represents the delay between an attack incident and its detection. It increases with attack intensity:
    $$L_{detection} = L_{base} + A_{intensity} \cdot D_{type}$$
    Where:
    - $$L_{base}$$ is a nominal baseline detection latency.
    - $$D_{type}$$ is a coefficient related to the `Attack Type`, representing how challenging that specific attack is to detect quickly.

    #### Agent Integrity Score
    The integrity score for a compromised agent, $$I_{agent\_attacked}$$, is reduced from its baseline, $$I_{agent\_base}$$, based on attack intensity and type:
    $$I_{agent\_attacked} = I_{agent\_base} \cdot (1 - A_{intensity} \cdot K_{type})$$
    Where:
    - $$K_{type}$$ is a coefficient for the `Attack Type`, reflecting its detrimental effect on agent trustworthiness or operational integrity. For uncompromised agents, $$I_{agent\_attacked} = I_{agent\_base}$$.

    These formulae provide a structured way to quantify the effects of 'synthetic-identity risk' and 'data poisoning' on system metrics, making the simulation robust and interpretable.
    """)