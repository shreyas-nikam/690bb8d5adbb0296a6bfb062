
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from application_pages.utils import generate_synthetic_safety_data, SIMULATION_DURATION_HOURS, NUM_AGENTS, BASE_ALERT_RATE_PER_HOUR, ANOMALY_RATE_MULTIPLIER, RANDOM_SEED

def run_page1():
    st.title("AI Security Vulnerability Simulation Lab")
    st.markdown("""
    This lab provides hands-on experience in identifying, understanding, and analyzing AI-security vulnerabilities within agentic AI systems used for industrial safety monitoring. Participants will gain practical insights into how various attack vectors, such as prompt injection and data poisoning, can impact system performance and security. The lab covers key concepts like 'synthetic-identity risk' and 'untraceable data leakage' by visualizing their effects on simulated security metrics.
    """)

    st.header("Learning Goals")
    st.markdown("""
    Upon completion of this lab, users will be able to:
    -   **Understand the key insights** presented in the provided resource documents and simulated data regarding AI security.
    -   **Identify common AI-security vulnerabilities**, such as 'synthetic-identity risk' and 'untraceable data leakage,' and comprehend their potential impact.
    -   **Learn about adversarial testing techniques** including prompt injection and data poisoning, by observing their simulated effects.
    -   **Analyze the effectiveness** of different attack vectors and understand their impact on system performance and security metrics.
    -   **Grasp practical implications** of concepts like 'red teaming chains of agents' and 'documented risk controls in the assurance plan' through visualizing attack effects.
    -   **Learn to design and validate adaptive systems** by understanding how simulated attacks affect an industrial safety monitoring system.
    """)

    st.header("Data/Inputs Overview")
    st.markdown("""
    This lab operates on a synthetically generated dataset that simulates an industrial safety monitoring environment. This approach allows for a controlled study of AI security vulnerabilities without relying on sensitive real-world data. The synthetic data includes:
    -   **Sensor Readings**: Time-series data from various industrial sensors.
    -   **Agent Communication Logs**: Records of messages exchanged between AI agents.
    -   **Security Metrics**: Baseline measurements of system behavior, such as alert frequency and agent integrity scores.
    These inputs are designed to be realistic enough to demonstrate the concepts of AI security vulnerabilities, and their generation is configured to ensure a lightweight dataset for quick execution, making the lab accessible on standard hardware.
    """)

    st.subheader("Fixed Simulation Parameters")
    st.markdown(f"""
    - **Simulation Duration**: {SIMULATION_DURATION_HOURS} hours
    - **Number of Agents**: {NUM_AGENTS}
    - **Base Alert Rate (per hour)**: {BASE_ALERT_RATE_PER_HOUR}
    - **Anomaly Rate Multiplier**: {ANOMALY_RATE_MULTIPLIER}
    - **Random Seed**: {RANDOM_SEED}
    """)

    st.subheader("Generating Baseline Data")
    st.markdown("""
    We start by generating a synthetic baseline dataset that represents the normal, secure operation of an industrial safety monitoring system. This data includes sensor readings, agent communication logs, and initial security metrics, which will serve as a reference point to observe the impact of simulated attacks.
    """)

    if 'sensor_data_baseline' not in st.session_state:
        sensor_data_baseline, agent_logs_baseline, security_metrics_baseline, simulation_config = \
            generate_synthetic_safety_data(NUM_AGENTS, SIMULATION_DURATION_HOURS, BASE_ALERT_RATE_PER_HOUR, ANOMALY_RATE_MULTIPLIER, RANDOM_SEED)

        st.session_state['sensor_data_baseline'] = sensor_data_baseline
        st.session_state['agent_logs_baseline'] = agent_logs_baseline
        st.session_state['security_metrics_baseline'] = security_metrics_baseline
        st.session_state['simulation_config'] = simulation_config

    st.success("Baseline data generated and stored in session state.")

    st.subheader("Baseline Data Preview (First 5 Rows)")
    st.markdown("#### Sensor Data Baseline")
    st.dataframe(st.session_state['sensor_data_baseline'].head())

    st.markdown("#### Agent Logs Baseline")
    st.dataframe(st.session_state['agent_logs_baseline'].head())

    st.markdown("#### Security Metrics Baseline")
    st.dataframe(st.session_state['security_metrics_baseline'].head())

    st.markdown("""
    Navigate to "Page 2: Simulation Configuration & Validation" in the sidebar to configure attack parameters and validate the generated data.
    """)
