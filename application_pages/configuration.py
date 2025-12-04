import streamlit as st

# Constants
SIMULATION_DURATION_HOURS = 2
NUM_AGENTS = 10
BASE_ALERT_RATE_PER_HOUR = 5
ANOMALY_RATE_MULTIPLIER = 2.5
RANDOM_SEED = 42


def main():
    st.sidebar.title("AI Security Vulnerability Simulation Lab")
    st.sidebar.markdown("Adjust parameters to observe the impact of AI security vulnerabilities.")

    # Sidebar user inputs
    st.session_state.selected_attack_intensity = st.sidebar.slider(
        "Select Attack Intensity ($A_{intensity}$)",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.selected_attack_intensity,
        step=0.05,
        help="Controls the severity of the simulated attack, ranging from $0.0$ (no attack) to $1.0$ (maximum intensity)."
    )

    st.session_state.selected_attack_type = st.sidebar.selectbox(
        "Select Attack Type",
        options=['Prompt Injection', 'Data Poisoning', 'Synthetic Identity', 'Untraceable Data Leakage'],
        index=['Prompt Injection', 'Data Poisoning', 'Synthetic Identity', 'Untraceable Data Leakage'].index(st.session_state.selected_attack_type),
        help="Determines the specific type of AI security vulnerability being simulated."
    )

    st.session_state.selected_num_compromised_agents = st.sidebar.slider(
        "Select Number of Compromised Agents ($N_{agents}$)",
        min_value=0,
        max_value=NUM_AGENTS,
        value=st.session_state.selected_num_compromised_agents,
        step=1,
        help=f"Specifies how many of the simulated agents (out of {NUM_AGENTS}) are affected by the attack."
    )

    st.markdown("## Current Simulation Parameters")
    st.write(f"**Selected Attack Intensity:** {st.session_state.selected_attack_intensity}")
    st.write(f"**Selected Attack Type:** {st.session_state.selected_attack_type}")
    st.write(f"**Selected Number of Compromised Agents:** {st.session_state.selected_num_compromised_agents}")
    st.write(f"**Simulation Duration (Hours):** {SIMULATION_DURATION_HOURS}")
    st.write(f"**Number of Agents:** {NUM_AGENTS}")
    st.write(f"**Base Alert Rate (Per Hour):** {BASE_ALERT_RATE_PER_HOUR}")
    st.write(f"**Anomaly Rate Multiplier:** {ANOMALY_RATE_MULTIPLIER}")
    st.write(f"**Random Seed:** {RANDOM_SEED}")
    