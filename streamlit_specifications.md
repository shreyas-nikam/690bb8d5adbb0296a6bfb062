
# Streamlit Application Requirements Specification

This document outlines the requirements for developing a Streamlit application based on the provided Jupyter Notebook content and user requirements for an AI Security Vulnerability Simulation Lab. It serves as a blueprint, detailing interactive components, visualizations, and relevant code stubs.

## 1. Application Overview

The **AI Security Vulnerability Simulation Lab** is designed to provide hands-on experience in identifying, understanding, and analyzing AI-security vulnerabilities within agentic AI systems used for industrial safety monitoring.

**Learning Goals:**
- Understand the key insights contained in the uploaded document and supporting data regarding AI security.
- Identify common AI-security vulnerabilities, including 'synthetic-identity risk' and 'untraceable data leakage,' and comprehend their potential impact.
- Learn about adversarial testing techniques like prompt injection and data poisoning by observing their simulated effects.
- Analyze the effectiveness of different attack vectors and understand their impact on system performance and security metrics.
- Grasp practical implications of concepts like 'red teaming chains of agents' and 'documented risk controls in the assurance plan' through visualizing attack effects.
- Learn to design and validate adaptive systems by understanding how simulated attacks affect an industrial safety monitoring system.

**Scope & Constraints (from user requirements):**
- The lab must execute end-to-end on a mid-spec laptop (8 GB RAM) in fewer than 5 minutes.
- Only open-source Python libraries from PyPI may be used.
- All major steps need both code comments and brief narrative cells that describe **what** is happening and **why**.

## 2. User Interface Requirements

The Streamlit application will adopt a clean, intuitive layout with a sidebar for interactive controls and a main content area for displaying narrative, data summaries, and visualizations.

### Layout and Navigation Structure
- **Sidebar (`st.sidebar`):** Will host all user input widgets (sliders, dropdowns) for configuring the simulation parameters.
- **Main Content Area:**
    - **Introduction & Learning Goals:** Top section with narrative markdown and objectives.
    - **Fixed Parameters Display:** A section to show the non-interactive, fixed simulation parameters.
    - **Data Overview:** Markdown describing the synthetic data.
    - **Mathematical Foundations:** Markdown and LaTeX display of key formulas.
    - **Baseline Data Preview:** `st.dataframe` displays of the head of generated baseline data.
    - **Data Validation Summary:** `st.dataframe` displays of validation results and `.describe()` outputs.
    - **Attacked Data Preview:** `st.dataframe` displays of the head of the attacked data and attack events.
    - **Visualizations:** Dedicated sections for each plot.
    - **Discussion & Conclusion:** Markdown for interpreting results and summarizing key takeaways.
    - **References:** Markdown for credits and external resources.

### Input Widgets and Controls
The application will provide interactive widgets in the sidebar to allow users to modify simulation parameters. Changes to these widgets will trigger re-execution of the simulation and plot updates.

1.  **Attack Intensity ($A_{intensity}$):**
    -   **Streamlit Widget:** `st.sidebar.slider`
    -   **Type:** Float
    -   **Range:** $0.0$ to $1.0$
    -   **Step:** $0.1$
    -   **Default Value:** $0.5$
    -   **Description:** 'Attack Intensity ($A_{intensity}$):'
    -   **Help Text/Tooltip:** 'Controls the severity of the simulated attack ($0.0$ = no attack, $1.0$ = maximum impact).'
2.  **Attack Type:**
    -   **Streamlit Widget:** `st.sidebar.selectbox`
    -   **Type:** Categorical (String)
    -   **Options:** ['Prompt Injection', 'Data Poisoning', 'Synthetic Identity', 'Untraceable Data Leakage']
    -   **Default Value:** 'Prompt Injection'
    -   **Description:** 'Attack Type:'
    -   **Help Text/Tooltip:** 'Selects the type of AI security vulnerability to simulate.'
3.  **Number of Compromised Agents ($N_{agents}$):**
    -   **Streamlit Widget:** `st.sidebar.slider`
    -   **Type:** Integer
    -   **Range:** $0$ to $5$ (limited to 5 for lightweight sample as specified)
    -   **Step:** $1$
    -   **Default Value:** $1$
    -   **Description:** 'Number of Compromised Agents ($N_{agents}$):'
    -   **Help Text/Tooltip:** 'Specifies the count of simulated agents affected by the attack.'

### Visualization Components
All visualizations will be generated using `matplotlib` and `seaborn` and displayed via `st.pyplot`. They will adhere to color-blind friendly palettes and have a font size of at least 12 pt, with clear titles, labeled axes, and legends.

1.  **Trend Plot: Alert Frequency Over Time**
    -   **Type:** Line plot
    -   **Purpose:** Compares total alert frequency over time for baseline and attacked scenarios.
    -   **Data:** Aggregated `alert_frequency` from `security_metrics_baseline` and `security_metrics_attacked` (summed by `timestamp`).
    -   **Title:** "Alert Frequency Over Time (Attack Type at X% Intensity)"
    -   **Axes:** X: 'Time', Y: 'Total Alert Frequency'
    -   **Legend:** 'Baseline', 'Attacked'
2.  **Relationship Plot: Attack Severity vs. Detection Latency**
    -   **Type:** Scatter plot
    -   **Purpose:** Examines the correlation between attack severity and simulated detection latency.
    -   **Data:** `attack_events_df` (X: `attack_severity`, Y: `simulated_detection_latency`).
    -   **Title:** "Attack Severity vs. Simulated Detection Latency"
    -   **Axes:** X: 'Attack Severity', Y: 'Simulated Detection Latency (Minutes)'
    -   **Legend:** 'Attack Type' (if multiple types are derived/simulated; otherwise, a single color for simplicity).
3.  **Aggregated Comparison: Agent Integrity Scores**
    -   **Type:** Bar chart
    -   **Purpose:** Compares average agent integrity scores for compromised versus uncompromised agents.
    -   **Data:** Average `agent_integrity_score` from `security_metrics_attacked`, categorized by agent status (compromised/uncompromised).
    -   **Title:** "Average Agent Integrity Scores: Compromised vs. Uncompromised"
    -   **Axes:** X: 'Agent Status', Y: 'Average Integrity Score'
    -   **Labels:** Numerical values for average scores displayed on top of bars.

### Interactive Elements and Feedback Mechanisms
-   Changes to sidebar input widgets will automatically trigger the re-execution of the simulation logic and update all displayed plots and data summaries in the main content area.
-   Tooltips will be provided for all interactive controls (mapped from `ipywidgets` `help` attribute to Streamlit `help` parameter).
-   Markdown cells and data previews will be clearly displayed, reflecting the results of the current simulation parameters.

## 3. Additional Requirements

### Annotation and Tooltip Specifications
-   All user input widgets (`st.sidebar.slider`, `st.sidebar.selectbox`) will include concise help text accessible via the `help` parameter, providing context for each control.
-   Key concepts and formulas will be presented with `st.markdown` and `st.latex` for clarity.

### Save the States of the Fields Properly so that Changes are not Lost
-   Streamlit's `st.session_state` will be utilized to store the user-selected parameters (`attack_intensity`, `attack_type`, `num_compromised_agents`) and the results of computationally intensive steps (e.g., `sensor_data_baseline`, `agent_logs_baseline`, `security_metrics_baseline`, `security_metrics_attacked`, `attack_events`) to avoid unnecessary re-computation upon minor UI interactions. This ensures that the application remains responsive and maintains the state across reruns.

## 4. Notebook Content and Code Requirements

This section details the extracted code stubs and markdown content from the Jupyter Notebook, outlining how they will be integrated into the Streamlit application.

### General Setup and Global Parameters
-   **Library Imports:**
    ```python
    import streamlit as st
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    from scipy import stats
    from datetime import datetime, timedelta
    import warnings

    # Configure plot settings
    sns.set_theme(style="whitegrid", palette="colorblind")
    plt.rcParams['font.size'] = 14 # Ensure font size >= 12 pt
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 12

    # Suppress warnings for cleaner output
    warnings.filterwarnings('ignore')

    # Fixed simulation parameters (as per notebook)
    SIMULATION_DURATION_HOURS = 2
    NUM_AGENTS = 10
    BASE_ALERT_RATE_PER_HOUR = 0.5
    ANOMALY_RATE_MULTIPLIER = 1.5
    RANDOM_SEED = 42

    # Coefficients for mathematical models (from Section 4/7 details)
    C_TYPE_DICT = {
        'Prompt Injection': 0.5, 'Data Poisoning': 0.8,
        'Synthetic Identity': 0.6, 'Untraceable Data Leakage': 0.7
    }
    K_TYPE_DICT = {
        'Prompt Injection': 0.4, 'Data Poisoning': 0.7,
        'Synthetic Identity': 0.8, 'Untraceable Data Leakage': 0.5
    }
    D_TYPE_DICT = { # These are base minutes
        'Prompt Injection': 20, 'Data Poisoning': 60,
        'Synthetic Identity': 45, 'Untraceable Data Leakage': 30
    }
    L_BASE = 5 # Nominal baseline detection latency (minutes)
    ```

### Markdown Content Inclusion (`st.markdown`, `st.latex`)

The following narrative and mathematical content from the Jupyter Notebook will be rendered in the Streamlit application:

-   **Application Title & Initial Overview:**
    ```python
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
    ```

-   **Data/Inputs Overview:**
    ```python
    st.header("Data/Inputs Overview")
    st.markdown("""
    This lab operates on a synthetically generated dataset that simulates an industrial safety monitoring environment. This approach allows for a controlled study of AI security vulnerabilities without relying on sensitive real-world data. The synthetic data includes:
    -   **Sensor Readings**: Time-series data from various industrial sensors.
    -   **Agent Communication Logs**: Records of messages exchanged between AI agents.
    -   **Security Metrics**: Baseline measurements of system behavior, such as alert frequency and agent integrity scores.
    These inputs are designed to be realistic enough to demonstrate the concepts of AI security vulnerabilities, and their generation is configured to ensure a lightweight dataset for quick execution, making the lab accessible on standard hardware.
    """)
    ```

-   **Methodology Overview & Mathematical Foundations:**
    ```python
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
    st.markdown(r"""
    Where:
    -   $A_{intensity}$ is the user-defined attack intensity, $A_{intensity} \in [0, 1]$.
    -   $C_{type}$ is a scaling factor specific to the `Attack Type`, reflecting its inherent impact potential (e.g., a data poisoning attack might have a higher $C_{type}$ than a mild prompt injection).
    """)

    st.markdown("#### Detection Latency")
    st.latex(r"""
    L_{detection} = L_{base} + A_{intensity} \cdot D_{type}
    """)
    st.markdown(r"""
    Where:
    -   $L_{base}$ is a nominal baseline detection latency.
    -   $D_{type}$ is a coefficient related to the `Attack Type`, representing how challenging that specific attack is to detect quickly.
    """)

    st.markdown("#### Agent Integrity Score")
    st.latex(r"""
    I_{agent\_attacked} = I_{agent\_base} \cdot (1 - A_{intensity} \cdot K_{type})
    """)
    st.markdown(r"""
    Where:
    -   $K_{type}$ is a coefficient for the `Attack Type`, reflecting its detrimental effect on agent trustworthiness or operational integrity. For uncompromised agents, $I_{agent\_attacked} = I_{agent\_base}$.
    """)
    ```

-   **Section-specific introductory and concluding remarks** (e.g., for Data Generation, Data Validation, Vulnerability Simulation, Plot sections, Discussion, Conclusion, References) will be included using `st.markdown`.

### Extracted Code Stubs for Streamlit Application

1.  **`generate_synthetic_safety_data` Function (for synthetic data generation):**
    This function creates the baseline sensor data, agent logs, and security metrics.
    ```python
    def generate_synthetic_safety_data(num_agents, simulation_duration_hours, base_alert_rate, anomaly_rate_multiplier, random_seed):
        np.random.seed(random_seed)
        start_time = datetime.now().replace(second=0, microsecond=0)
        timestamps = [start_time + timedelta(minutes=i) for i in range(simulation_duration_hours * 60)]

        sensor_data_list = []
        for agent_id in range(num_agents):
            for timestamp in timestamps:
                sensor_value_temp = np.random.normal(loc=70, scale=5)
                sensor_value_pressure = np.random.normal(loc=100, scale=10)
                sensor_data_list.append([timestamp, agent_id, "temperature", sensor_value_temp, "Fahrenheit"])
                sensor_data_list.append([timestamp, agent_id, "pressure", sensor_value_pressure, "PSI"])
        sensor_data_df = pd.DataFrame(sensor_data_list, columns=["timestamp", "agent_id", "sensor_type", "value", "unit"])

        agent_logs_list = []
        for agent_id in range(num_agents):
            for timestamp in timestamps:
                message_type = np.random.choice(["status_update", "alert", "communication"])
                message_content = f"Agent {agent_id} reporting {message_type} at {timestamp.strftime('%Y-%m-%d %H:%M')}"
                risk_score = 0.1 if message_type == "status_update" else (0.5 if message_type == "communication" else 0.8)
                agent_logs_list.append([timestamp, agent_id, message_type, message_content, risk_score])
        agent_logs_df = pd.DataFrame(agent_logs_list, columns=["timestamp", "agent_id", "message_type", "message_content", "risk_score"])

        base_security_metrics_list = []
        for timestamp in timestamps:
            for agent_id in range(num_agents):
                agent_integrity_score = 0.95 + np.random.normal(0, 0.02)
                agent_integrity_score = max(0, min(1, agent_integrity_score))
                agent_alert_frequency = stats.poisson.rvs(mu=(base_alert_rate / (60 * num_agents)))
                base_security_metrics_list.append([timestamp, agent_id, agent_alert_frequency, agent_integrity_score])
        base_security_metrics_df = pd.DataFrame(base_security_metrics_list, columns=["timestamp", "agent_id", "alert_frequency", "agent_integrity_score"])

        simulation_config = {
            "num_agents": num_agents, "simulation_duration_hours": simulation_duration_hours,
            "base_alert_rate": base_alert_rate, "anomaly_rate_multiplier": anomaly_rate_multiplier,
            "random_seed": random_seed, "start_time": start_time, "end_time": timestamps[-1]
        }
        return sensor_data_df, agent_logs_df, base_security_metrics_df, simulation_config
    ```

2.  **`validate_and_summarize_data` Function (for data integrity checks):**
    This function validates the structure and content of the generated data. Output will be `st.dataframe`.
    ```python
    def validate_and_summarize_data(df, df_name, expected_columns, expected_dtypes, critical_fields_no_null=None, unique_key=None):
        st.subheader(f"--- Validating {df_name} ---")
        try:
            # 1. Check if expected columns are present
            missing_columns = [col for col in expected_columns if col not in df.columns]
            assert not missing_columns, f"Missing expected columns: {missing_columns}"
            st.success(f"{df_name}: All expected columns are present.")

            # 2. Check data types
            for col, dtype in expected_dtypes.items():
                if col in df.columns:
                    if 'datetime' in str(dtype) and 'datetime' in str(df[col].dtype):
                        pass
                    else:
                        assert str(df[col].dtype) == str(dtype), f"Column {col} expected type {dtype}, but got {df[col].dtype}"
            st.success(f"{df_name}: All expected column data types are correct.")

            # 3. Check critical fields for nulls
            if critical_fields_no_null:
                for field in critical_fields_no_null:
                    assert df[field].notnull().all(), f"Critical field {field} contains null values."
                st.success(f"{df_name}: No missing values in critical fields.")

            # 4. Check uniqueness of the unique key
            if unique_key:
                assert df.duplicated(subset=unique_key).sum() == 0, f"Duplicate values found in unique key columns: {unique_key}."
                st.success(f"{df_name}: Unique key columns are unique.")
            
            st.subheader(f"{df_name} Summary Statistics:")
            st.dataframe(df.describe())
            st.success(f"{df_name} validation successful.")
        except AssertionError as e:
            st.error(f"Validation failed for {df_name}: {e}")
        except Exception as e:
            st.error(f"An error occurred during validation of {df_name}: {e}")
    ```

3.  **`simulate_vulnerability_impact` Function (for applying attack logic):**
    This is the core simulation function that modifies security metrics based on user inputs and mathematical models.
    ```python
    def simulate_vulnerability_impact(base_metrics_df, attack_type, attack_intensity, num_compromised_agents, simulation_config):
        if not (0.0 <= attack_intensity <= 1.0):
            raise ValueError("Attack intensity must be between 0 and 1.")
        if not isinstance(num_compromised_agents, int) or num_compromised_agents < 0:
            raise ValueError("Number of compromised agents must be a non-negative integer.")

        attacked_security_metrics_df = base_metrics_df.copy()

        # Retrieve coefficients from global dictionaries
        c_type = C_TYPE_DICT.get(attack_type, 0.0)
        k_type = K_TYPE_DICT.get(attack_type, 0.0)
        d_type_minutes = D_TYPE_DICT.get(attack_type, 0)

        # Apply Alert Frequency modification
        attacked_security_metrics_df['alert_frequency'] = attacked_security_metrics_df['alert_frequency'] * (1 + attack_intensity * c_type)
        attacked_security_metrics_df['alert_frequency'] = attacked_security_metrics_df['alert_frequency'].clip(lower=0).astype(int)

        # Select compromised agents randomly for integrity score reduction
        all_agent_ids = attacked_security_metrics_df['agent_id'].unique()
        actual_num_compromised = min(num_compromised_agents, len(all_agent_ids))
        if actual_num_compromised > 0:
            np.random.seed(simulation_config['random_seed'])
            compromised_agent_ids = np.random.choice(all_agent_ids, actual_num_compromised, replace=False)
        else:
            compromised_agent_ids = np.array([]) # Ensure it's an array for consistency

        attacked_security_metrics_df['is_compromised'] = False # New column for plotting
        for agent_id in compromised_agent_ids:
            mask = attacked_security_metrics_df['agent_id'] == agent_id
            attacked_security_metrics_df.loc[mask, 'agent_integrity_score'] = \
                attacked_security_metrics_df.loc[mask, 'agent_integrity_score'] * (1 - attack_intensity * k_type)
            attacked_security_metrics_df.loc[mask, 'is_compromised'] = True
        attacked_security_metrics_df['agent_integrity_score'] = attacked_security_metrics_df['agent_integrity_score'].clip(lower=0)

        # Generate attack_events_df
        attack_severity = attack_intensity * actual_num_compromised * c_type
        simulated_detection_latency_minutes = L_BASE + attack_intensity * d_type_minutes

        attack_events_df = pd.DataFrame([{
            'timestamp': attacked_security_metrics_df['timestamp'].min(),
            'attack_type': attack_type,
            'attack_intensity': attack_intensity,
            'num_compromised_agents': actual_num_compromised,
            'attack_severity': attack_severity,
            'simulated_detection_latency': simulated_detection_latency_minutes
        }])
        
        return attacked_security_metrics_df, attack_events_df
    ```

4.  **`plot_alert_frequency_trend` Function (for visualizing alert trends):**
    ```python
    def plot_alert_frequency_trend(base_df, attacked_df, attack_type, attack_intensity, font_size=12):
        base_df_agg = base_df.groupby('timestamp')['alert_frequency'].mean().reset_index()
        attacked_df_agg = attacked_df.groupby('timestamp')['alert_frequency'].mean().reset_index()

        fig, ax = plt.subplots(figsize=(12, 7))
        sns.lineplot(x='timestamp', y='alert_frequency', data=base_df_agg, label='Baseline', marker='o', ax=ax)
        sns.lineplot(x='timestamp', y='alert_frequency', data=attacked_df_agg, label='Attacked', marker='x', ax=ax)

        ax.set_title(f"Alert Frequency Over Time: Baseline vs. Attacked\n({attack_type} at {attack_intensity*100:.0f}% Intensity)", fontsize=font_size+2)
        ax.set_xlabel('Time', fontsize=font_size)
        ax.set_ylabel('Average Alert Frequency', fontsize=font_size)
        ax.legend(fontsize=font_size)
        ax.grid(True, linestyle='--', alpha=0.7)
        plt.xticks(rotation=45, ha='right', fontsize=font_size-2)
        plt.yticks(fontsize=font_size-2)
        plt.tight_layout()
        st.pyplot(fig) # Display plot in Streamlit
    ```

5.  **`plot_attack_severity_vs_latency` Function (for correlation plot):**
    ```python
    def plot_attack_severity_vs_latency(attack_events_df, font_size=12):
        if attack_events_df.empty:
            st.warning("No attack events to plot for Attack Severity vs. Detection Latency.")
            return

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(x='attack_severity', y='simulated_detection_latency', data=attack_events_df,
                        hue='attack_type', s=150, alpha=0.7, ax=ax)

        ax.set_title('Attack Severity vs. Simulated Detection Latency', fontsize=font_size+2)
        ax.set_xlabel('Attack Severity', fontsize=font_size)
        ax.set_ylabel('Simulated Detection Latency (Minutes)', fontsize=font_size)
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend(title='Attack Type', fontsize=font_size-2, title_fontsize=font_size)
        plt.xticks(fontsize=font_size-2)
        plt.yticks(fontsize=font_size-2)
        plt.tight_layout()
        st.pyplot(fig)
    ```

6.  **`plot_agent_integrity_comparison` Function (for bar chart comparison):**
    ```python
    def plot_agent_integrity_comparison(attacked_df, font_size=12):
        if attacked_df.empty:
            st.warning("Attacked metrics DataFrame is empty, cannot plot agent integrity comparison.")
            return

        # Ensure 'is_compromised' column is present from `simulate_vulnerability_impact`
        if 'is_compromised' not in attacked_df.columns:
            st.error("The 'is_compromised' column is missing in the attacked DataFrame. Cannot plot integrity comparison.")
            return
        
        integrity_comparison = attacked_df.groupby('is_compromised')['agent_integrity_score'].mean().reset_index()
        integrity_comparison['Agent Status'] = integrity_comparison['is_compromised'].map({True: 'Compromised', False: 'Uncompromised'})

        fig, ax = plt.subplots(figsize=(9, 6))
        sns.barplot(x='Agent Status', y='agent_integrity_score', data=integrity_comparison, palette='colorblind', ax=ax)

        ax.set_title('Average Agent Integrity Scores: Compromised vs. Uncompromised', fontsize=font_size+2)
        ax.set_xlabel('Agent Status', fontsize=font_size)
        ax.set_ylabel('Average Integrity Score', fontsize=font_size)
        ax.set_ylim(0, 1)
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        plt.xticks(fontsize=font_size-2)
        plt.yticks(fontsize=font_size-2)

        for index, row in integrity_comparison.iterrows():
            ax.text(index, row['agent_integrity_score'] + 0.02, f"{row['agent_integrity_score']:.2f}",
                    color='black', ha="center", fontsize=font_size-2)
        plt.tight_layout()
        st.pyplot(fig)
    ```

### References

```python
st.header("References")
st.markdown("""
1.  **[1] Case 3: Agentic AI for Safety Monitoring, Provided Resource Document.** This document describes AI-security vulnerabilities like 'synthetic-identity risk' and 'untraceable data leakage', and the importance of rigorous testing and risk controls.
2.  **[2] Unit 6: Testing, Validation and AI Security, Adversarial Testing and Red-Teaming, Provided Resource Document.** This section explores threats like prompt injection and data poisoning, and discusses the impact of malicious samples on LLM output.
3.  **Pandas Library**: A fast, powerful, flexible and easy to use open source data analysis and manipulation tool, built on top of the Python programming language. (https://pandas.pydata.org/)
4.  **NumPy Library**: The fundamental package for scientific computing with Python. (https://numpy.org/)
5.  **Matplotlib Library**: A comprehensive library for creating static, animated, and interactive visualizations in Python. (https://matplotlib.org/)
6.  **Seaborn Library**: A Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics. (https://seaborn.pydata.org/)
7.  **IPywidgets Library**: Interactive HTML widgets for Jupyter notebooks and the IPython kernel. (https://ipywidgets.readthedocs.io/en/latest/)
""")
```

