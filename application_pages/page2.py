
import streamlit as st
import pandas as pd
from application_pages.utils import validate_and_summarize_data, C_TYPE_DICT, K_TYPE_DICT, D_TYPE_DICT, L_BASE

def run_page2():
    st.title("Simulation Configuration & Data Validation")

    st.header("Methodology Overview")
    st.markdown("""
    Our approach in this lab is to simulate an agentic AI system under various security attack scenarios. This involves several key steps:
    1.  **Synthetic Data Generation**: Create a baseline dataset representing normal operations of an industrial safety monitoring system.
    2.  **Interactive Parameter Definition**: Allow users to define key attack parameters such as type and intensity, providing a dynamic simulation environment.
    3.  **Attack Simulation**: Apply mathematical models to the baseline data, modifying security metrics to reflect the impact of the chosen attack.
    4.  **Visualization**: Generate plots and tables to visually demonstrate the effects of the attacks on system performance and security indicators.
    5.  **Analysis and Interpretation**: Discuss the observed impacts and relate them to real-world AI security concepts.
    """)
    st.subheader("Key Mathematical Foundations for Attack Simulation")
    st.markdown("To simulate the impact of AI security vulnerabilities concretely, we define mathematical relationships that govern how attacks influence key system metrics:")

    st.markdown("#### Alert Frequency Over Time")
    st.latex(r"""
    F_{alerts\_attacked}(t) = F_{alerts\_base}(t) \cdot (1 + A_{intensity} \cdot C_{type})
    """)
    st.markdown(f"""
    Where:
    -   $A_{{intensity}}$ is the user-defined attack intensity, $A_{{intensity}} \in [0, 1]$.
    -   $C_{{type}}$ is a scaling factor specific to the `Attack Type`, reflecting its inherent impact potential (e.g., a data poisoning attack might have a higher $C_{{type}}$ than a mild prompt injection). Current values: `{C_TYPE_DICT}`
    """)

    st.markdown("#### Detection Latency")
    st.latex(r"""
    L_{detection} = L_{base} + A_{intensity} \cdot D_{type}
    """)
    st.markdown(f"""
    Where:
    -   $L_{{base}}$ is a nominal baseline detection latency ($L_{{base}} = {L_BASE}$ minutes).
    -   $D_{{type}}$ is a coefficient related to the `Attack Type`, representing how challenging that specific attack is to detect quickly. Current values: `{D_TYPE_DICT}` (in minutes)
    """)

    st.markdown("#### Agent Integrity Score")
    st.latex(r"""
    I_{agent\_attacked} = I_{agent\_base} \cdot (1 - A_{intensity} \cdot K_{type})
    """)
    st.markdown(f"""
    Where:
    -   $K_{{type}}$ is a coefficient for the `Attack Type`, reflecting its detrimental effect on agent trustworthiness or operational integrity. For uncompromised agents, $I_{{agent\_attacked}} = I_{{agent\_base}}$. Current values: `{K_TYPE_DICT}`
    """)

    st.header("Configure Simulation Parameters")
    st.markdown("Use the sidebar to adjust the parameters of the AI security vulnerability simulation.")

    # Sidebar controls
    st.sidebar.header("Simulation Controls")
    attack_intensity = st.sidebar.slider(
        label='Attack Intensity ($A_{intensity}$):',
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.get('attack_intensity', 0.5),
        step=0.1,
        help='Controls the severity of the simulated attack ($0.0$ = no attack, $1.0$ = maximum impact).'
    )
    st.session_state['attack_intensity'] = attack_intensity

    attack_type = st.sidebar.selectbox(
        label='Attack Type:',
        options=['Prompt Injection', 'Data Poisoning', 'Synthetic Identity', 'Untraceable Data Leakage'],
        index=['Prompt Injection', 'Data Poisoning', 'Synthetic Identity', 'Untraceable Data Leakage'].index(
            st.session_state.get('attack_type', 'Prompt Injection')
        ),
        help='Selects the type of AI security vulnerability to simulate.'
    )
    st.session_state['attack_type'] = attack_type

    num_compromised_agents = st.sidebar.slider(
        label='Number of Compromised Agents ($N_{agents}$):',
        min_value=0,
        max_value=5,
        value=st.session_state.get('num_compromised_agents', 1),
        step=1,
        help='Specifies the count of simulated agents affected by the attack.'
    )
    st.session_state['num_compromised_agents'] = num_compromised_agents

    st.header("Data Validation Summary")
    st.markdown("Before proceeding to the simulation, we validate the structure and integrity of the generated baseline data.")

    if 'sensor_data_baseline' in st.session_state:
        # Sensor Data Validation
        sensor_expected_columns = ["timestamp", "agent_id", "sensor_type", "value", "unit"]
        sensor_expected_dtypes = {
            "timestamp": "datetime64[ns]", "agent_id": "int64",
            "sensor_type": "object", "value": "float64", "unit": "object"
        }
        validate_and_summarize_data(
            st.session_state['sensor_data_baseline'], "Sensor Data Baseline",
            sensor_expected_columns, sensor_expected_dtypes, ["timestamp", "agent_id", "value"], ["timestamp", "agent_id", "sensor_type"]
        )

        # Agent Logs Validation
        agent_logs_expected_columns = ["timestamp", "agent_id", "message_type", "message_content", "risk_score"]
        agent_logs_expected_dtypes = {
            "timestamp": "datetime64[ns]", "agent_id": "int64",
            "message_type": "object", "message_content": "object", "risk_score": "float64"
        }
        validate_and_summarize_data(
            st.session_state['agent_logs_baseline'], "Agent Logs Baseline",
            agent_logs_expected_columns, agent_logs_expected_dtypes, ["timestamp", "agent_id", "risk_score"], ["timestamp", "agent_id", "message_type"]
        )

        # Security Metrics Validation
        security_metrics_expected_columns = ["timestamp", "agent_id", "alert_frequency", "agent_integrity_score"]
        security_metrics_expected_dtypes = {
            "timestamp": "datetime64[ns]", "agent_id": "int64",
            "alert_frequency": "int64", "agent_integrity_score": "float64"
        }
        validate_and_summarize_data(
            st.session_state['security_metrics_baseline'], "Security Metrics Baseline",
            security_metrics_expected_columns, security_metrics_expected_dtypes, ["timestamp", "agent_id", "alert_frequency", "agent_integrity_score"], ["timestamp", "agent_id"]
        )
    else:
        st.warning("Baseline data not found. Please navigate to 'Page 1: Overview & Data Generation' first.")

    st.markdown("""
    Once you have configured the simulation parameters and reviewed the data validation, navigate to "Page 3: Vulnerability Simulation & Analysis" to observe the attack's impact.
    """)
