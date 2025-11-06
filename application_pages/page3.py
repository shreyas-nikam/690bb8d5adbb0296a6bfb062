
import streamlit as st
import pandas as pd
from application_pages.utils import simulate_vulnerability_impact, plot_alert_frequency_trend_plotly, plot_attack_severity_vs_latency_plotly, plot_agent_integrity_comparison_plotly, SIMULATION_DURATION_HOURS, NUM_AGENTS, BASE_ALERT_RATE_PER_HOUR, ANOMALY_RATE_MULTIPLIER, RANDOM_SEED

def run_page3():
    st.title("Vulnerability Simulation & Analysis")

    st.header("Simulation Results")
    st.markdown("""
    This section presents the results of the AI security vulnerability simulation based on the parameters you configured. We will visualize how different attack types and intensities impact key security metrics, providing insights into the system's resilience and vulnerabilities.
    """)

    if (
        'security_metrics_baseline' in st.session_state and
        'simulation_config' in st.session_state and
        'attack_intensity' in st.session_state and
        'attack_type' in st.session_state and
        'num_compromised_agents' in st.session_state
    ):
        security_metrics_baseline = st.session_state['security_metrics_baseline']
        simulation_config = st.session_state['simulation_config']
        attack_intensity = st.session_state['attack_intensity']
        attack_type = st.session_state['attack_type']
        num_compromised_agents = st.session_state['num_compromised_agents']

        st.subheader("Simulating Attack Impact")
        st.markdown(f"""
        Running simulation with:
        - **Attack Type**: `{attack_type}`
        - **Attack Intensity**: `{attack_intensity:.1f}`
        - **Number of Compromised Agents**: `{num_compromised_agents}`
        """)

        try:
            attacked_security_metrics, attack_events_df = simulate_vulnerability_impact(
                security_metrics_baseline, attack_type, attack_intensity, num_compromised_agents, simulation_config
            )
            st.session_state['security_metrics_attacked'] = attacked_security_metrics
            st.session_state['attack_events_df'] = attack_events_df
            st.success("Vulnerability simulation completed successfully!")
        except ValueError as e:
            st.error(f"Simulation error: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred during simulation: {e}")

        if 'security_metrics_attacked' in st.session_state and 'attack_events_df' in st.session_state:
            st.subheader("Attacked Data Preview (First 5 Rows)")
            st.markdown("#### Attacked Security Metrics")
            st.dataframe(st.session_state['security_metrics_attacked'].head())

            st.markdown("#### Attack Events")
            st.dataframe(st.session_state['attack_events_df'].head())

            st.header("Visualizations")
            st.markdown("""
            The following visualizations illustrate the impact of the simulated AI security vulnerability on key system metrics. Observe the differences between the baseline (normal operation) and the attacked scenarios.
            """)

            # Plot 1: Alert Frequency Over Time
            st.subheader("1. Trend Plot: Alert Frequency Over Time")
            st.markdown("This plot compares the average alert frequency over time for both baseline and attacked scenarios. A significant divergence indicates the attack's impact on system alerting mechanisms.")
            plot_alert_frequency_trend_plotly(security_metrics_baseline, attacked_security_metrics, attack_type, attack_intensity)

            # Plot 2: Attack Severity vs. Detection Latency
            st.subheader("2. Relationship Plot: Attack Severity vs. Detection Latency")
            st.markdown("This scatter plot explores the correlation between the severity of the simulated attack and the system's ability to detect it in a timely manner. Higher latency in detection can lead to more severe consequences.")
            plot_attack_severity_vs_latency_plotly(attack_events_df)

            # Plot 3: Aggregated Comparison: Agent Integrity Scores
            st.subheader("3. Aggregated Comparison: Agent Integrity Scores")
            st.markdown("This bar chart compares the average integrity scores of compromised versus uncompromised agents, highlighting the direct impact of the attack on agent trustworthiness and performance.")
            plot_agent_integrity_comparison_plotly(attacked_security_metrics)
        else:
            st.warning("Simulation results are not available. Please ensure the simulation ran without errors.")

    else:
        st.warning("Please navigate to 'Page 1: Overview & Data Generation' and 'Page 2: Simulation Configuration & Validation' first to generate data and configure parameters.")

    st.header("Discussion & Conclusion")
    st.markdown("""
    The simulation results clearly demonstrate how various AI security vulnerabilities, such as prompt injection and data poisoning, can significantly impact the performance and reliability of agentic AI systems for industrial safety monitoring. We observed changes in alert frequencies, detection latencies, and agent integrity scores, all of which are critical indicators of system health and security.

    Key takeaways from this lab:
    - **Impact of Attack Intensity**: Higher attack intensity generally leads to more pronounced effects across all metrics, emphasizing the need for robust defense mechanisms.
    - **Vulnerability-Specific Effects**: Different attack types exhibit distinct patterns of impact, underscoring the importance of understanding the unique characteristics of each vulnerability.
    - **Importance of Timely Detection**: The relationship between attack severity and detection latency highlights that delays in identifying and mitigating attacks can lead to amplified negative consequences.
    - **Agent Integrity**: Compromised agents show a clear degradation in integrity, pointing to the necessity of agent-level security monitoring and recovery protocols.

    This lab provides a foundational understanding of AI security risks and the efficacy of simulated adversarial testing. By visualizing these impacts, we can better design, implement, and validate adaptive AI systems that are resilient against emerging threats.
    """)

    st.header("References")
    st.markdown("""
    1.  **[1] Case 3: Agentic AI for Safety Monitoring, Provided Resource Document.** This document describes AI-security vulnerabilities like 'synthetic-identity risk' and 'untraceable data leakage', and the importance of rigorous testing and risk controls.
    2.  **[2] Unit 6: Testing, Validation and AI Security, Adversarial Testing and Red-Teaming, Provided Resource Document.** This section explores threats like prompt injection and data poisoning, and discusses the impact of malicious samples on LLM output.
    3.  **Pandas Library**: A fast, powerful, flexible and easy to use open source data analysis and manipulation tool, built on top of the Python programming language. (https://pandas.pydata.org/)
    4.  **NumPy Library**: The fundamental package for scientific computing with Python. (https://numpy.org/)
    5.  **Plotly Library**: An interactive, open-source, and browser-based graphing library for Python. (https://plotly.com/python/)
    """)
