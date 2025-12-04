import streamlit as st

# Configuration Page

def main():
    st.markdown("""
    ## Section 3: Define Configuration Parameters (User Interaction)
    
    This section allows users to interactively set the parameters for the AI security vulnerability simulation. These parameters control the characteristics of the synthetic data and the nature of the simulated attack. Inline help text is provided for each control.

    **Key parameters are:**
    - **Attack Intensity ($$A_{intensity}$$):** Controls the severity of the attack, ranging from $$0.0$$ (no attack) to $$1.0$$ (maximum intensity).
    - **Attack Type:** Determines the specific type of vulnerability being simulated (e.g., Prompt Injection, Data Poisoning).
    - **Number of Compromised Agents ($$N_{agents}$$):** Specifies how many of the simulated agents are affected by the attack.
    """)

    st.write("---")
    st.markdown("### Current Simulation Parameters")
    st.write(f"**Selected Attack Intensity:** {st.session_state.selected_attack_intensity}")
    st.write(f"**Selected Attack Type:** {st.session_state.selected_attack_type}")
    st.write(f"**Selected Number of Compromised Agents:** {st.session_state.selected_num_compromised_agents}")
    st.write(f"**Simulation Duration (Hours):** 2")
    st.write(f"**Number of Agents:** 10")
    st.write(f"**Base Alert Rate (Per Hour):** 5")
    st.write(f"**Anomaly Rate Multiplier:** 2.5")
    st.write(f"**Random Seed:** 42")
    st.write("---")