# Streamlit Application Specification: AI Security Vulnerability Simulation Lab

## 1. Application Overview

This Streamlit application will serve as an interactive "AI Security Vulnerability Simulation Lab," providing users with hands-on experience in identifying, understanding, and analyzing AI-security vulnerabilities within agentic AI systems designed for industrial safety monitoring.

**Learning Goals:**
*   Understand key insights related to AI-security vulnerabilities in agentic systems.
*   Identify common AI-security vulnerabilities, such as 'synthetic-identity risk' (compromised agent impersonation) and 'untraceable data leakage' (covert data exfiltration).
*   Learn about adversarial testing techniques, including prompt injection and data poisoning.
*   Analyze the effectiveness of different defense strategies and risk controls in mitigating AI security threats.
*   Observe the impact of various attack vectors on system performance and security metrics.

## 2. User Interface Requirements

### Layout and Navigation Structure

The application will feature a clear, vertically structured layout with interactive controls consolidated in a sidebar for ease of access.

*   **Sidebar (`st.sidebar`):**
    *   Application title and brief description.
    *   Input widgets for simulation parameters (Attack Intensity, Attack Type, Number of Compromised Agents).
    *   Help text/tooltips for each control.
*   **Main Content Area:**
    *   **Introduction:** High-level overview and learning outcomes.
    *   **Setup:** Explanation of library imports.
    *   **Configuration Parameters:** Display of selected interactive parameters and fixed simulation parameters.
    *   **Mathematical Foundations:** Explanation of the underlying attack models using LaTeX.
    *   **Synthetic Data Generation:** Display of baseline synthetic data samples (sensor, agent logs, security metrics).
    *   **Data Validation and Initial Statistics:** Output from data validation and summary statistics for baseline data.
    *   **Vulnerability Simulation:** Display of attacked security metrics and attack event details.
    *   **Visualizations:** Dedicated sections for the Trend Plot, Relationship Plot, and Aggregated Comparison Plot.
    *   **Discussion of Results and Learning Outcomes:** Interpretation of simulation findings.
    *   **Conclusion:** Summary of the lab's key takeaways.
    *   **References:** Listing of resources.

### Input Widgets and Controls

All interactive parameters from the Jupyter Notebook will be implemented using Streamlit widgets, primarily located in the sidebar.

*   **Attack Intensity ($A_{intensity}$):**
    *   **Widget:** `st.sidebar.slider`
    *   **Label:** "Select Attack Intensity ($A_{intensity}$)"
    *   **Range:** $[0.0, 1.0]$
    *   **Step:** $0.05$
    *   **Default:** $0.5$
    *   **Help Text:** "Controls the severity of the simulated attack, ranging from $0.0$ (no attack) to $1.0$ (maximum intensity)."
*   **Attack Type:**
    *   **Widget:** `st.sidebar.selectbox`
    *   **Label:** "Select Attack Type"
    *   **Options:** `['Prompt Injection', 'Data Poisoning', 'Synthetic Identity', 'Untraceable Data Leakage']`
    *   **Default:** `'Prompt Injection'`
    *   **Help Text:** "Determines the specific type of AI security vulnerability being simulated."
*   **Number of Compromised Agents ($N_{agents}$):**
    *   **Widget:** `st.sidebar.slider` (since `NUM_AGENTS = 10` is fixed, an integer slider is appropriate)
    *   **Label:** "Select Number of Compromised Agents ($N_{agents}$)"
    *   **Range:** $[0, \text{NUM\_AGENTS}]$ (where `NUM_AGENTS` is a fixed parameter, typically 10)
    *   **Step:** $1$
    *   **Default:** $1$
    *   **Help Text:** "Specifies how many of the simulated agents are affected by the attack."

### Visualization Components (charts, graphs, tables)

*   **Data Previews:**
    *   `st.dataframe`: Display `head()` of `sensor_data_baseline`, `agent_logs_baseline`, `security_metrics_baseline`.
    *   `st.dataframe`: Display `head()` of `security_metrics_attacked`, `attack_events`.
    *   `st.dataframe` or `st.write`: Display `describe()` output from data validation for numeric columns.
*   **Trend Plot:**
    *   **Component:** `st.pyplot`
    *   **Description:** Line plot showing 'Alert Frequency over Time' ($F_{alerts\_attacked}(t)$) comparing baseline vs. attacked scenarios.
    *   **Function:** `plot_alert_frequency_trend`
*   **Relationship Plot:**
    *   **Component:** `st.pyplot`
    *   **Description:** Scatter plot of 'Attack Severity vs. Detection Latency'.
    *   **Function:** `plot_attack_severity_vs_latency`
*   **Aggregated Comparison Plot:**
    *   **Component:** `st.pyplot`
    *   **Description:** Bar chart comparing 'Agent Integrity Scores' for compromised vs. uncompromised agents.
    *   **Function:** `plot_agent_integrity_comparison`

### Interactive Elements and Feedback Mechanisms

*   Changing any input widget in the sidebar will trigger a re-run of the application, updating all subsequent data generation, simulation, and visualization components with the new parameters.
*   Data validation function (`validate_and_summarize_data`) will print status messages (`INFO`, `ERROR`) to the Streamlit app using `st.info`, `st.error`, or `st.success`. Any `AssertionError` or `TypeError` during validation should be caught and displayed as an error message to the user.

## 3. Additional Requirements

*   **Annotation and Tooltip Specifications:**
    *   Inline help text will be provided for all interactive controls as detailed in "Input Widgets and Controls".
    *   All narrative/markdown cells from the Jupyter Notebook will be rendered using `st.markdown`, including LaTeX-formatted mathematical equations and explanations, to provide context and learning outcomes.
*   **State Preservation:**
    *   The values selected by the user for `Attack Intensity`, `Attack Type`, and `Number of Compromised Agents` will be stored and managed using `st.session_state`. This ensures that these selections persist across application re-runs and user interactions.

## 4. Notebook Content and Code Requirements

This section details how the Jupyter Notebook content, including markdown and code, will be integrated into the Streamlit application. All mathematical content will strictly adhere to LaTeX formatting rules: `$$...$$` for display equations and `$...$` for inline equations, with no asterisks around mathematical variables.

### General Structure:

The Streamlit application will follow the logical flow of the Jupyter Notebook.

```python
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from datetime import timedelta # Import timedelta specifically as used in notebook

# Set page configuration for wider layout
st.set_page_config(layout="wide")

# Initialize session state variables for interactive controls
if 'selected_attack_intensity' not in st.session_state:
    st.session_state.selected_attack_intensity = 0.5
if 'selected_attack_type' not in st.session_state:
    st.session_state.selected_attack_type = 'Prompt Injection'
if 'selected_num_compromised_agents' not in st.session_state:
    st.session_state.selected_num_compromised_agents = 1

# Fixed simulation parameters (from notebook)
SIMULATION_DURATION_HOURS = 2
NUM_AGENTS = 10
BASE_ALERT_RATE_PER_HOUR = 5
ANOMALY_RATE_MULTIPLIER = 2.5
RANDOM_SEED = 42

# Coefficients for vulnerability impact (from notebook, Section 7)
COEFFS = {
    'C_type': {'Prompt Injection': 0.5, 'Data Poisoning': 0.8, 'Synthetic Identity': 0.6, 'Untraceable Data Leakage': 0.7},
    'K_type': {'Prompt Injection': 0.4, 'Data Poisoning': 0.7, 'Synthetic Identity': 0.8, 'Untraceable Data Leakage': 0.5},
    'D_type': {'Prompt Injection': 20, 'Data Poisoning': 60, 'Synthetic Identity': 45, 'Untraceable Data Leakage': 30}, # in minutes
    'L_base': 5 # nominal baseline detection latency in minutes
}

# --- Sidebar for user interaction ---
with st.sidebar:
    st.title("AI Security Vulnerability Simulation Lab")
    st.markdown("Adjust parameters to observe the impact of AI security vulnerabilities.")

    st.session_state.selected_attack_intensity = st.slider(
        "Select Attack Intensity ($A_{intensity}$)",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.selected_attack_intensity,
        step=0.05,
        help="Controls the severity of the simulated attack, ranging from $0.0$ (no attack) to $1.0$ (maximum intensity)."
    )

    st.session_state.selected_attack_type = st.selectbox(
        "Select Attack Type",
        options=list(COEFFS['C_type'].keys()),
        index=list(COEFFS['C_type'].keys()).index(st.session_state.selected_attack_type),
        help="Determines the specific type of AI security vulnerability being simulated."
    )

    st.session_state.selected_num_compromised_agents = st.slider(
        "Select Number of Compromised Agents ($N_{agents}$)",
        min_value=0,
        max_value=NUM_AGENTS,
        value=st.session_state.selected_num_compromised_agents,
        step=1,
        help=f"Specifies how many of the simulated agents (out of {NUM_AGENTS}) are affected by the attack."
    )

# --- Main Content Area ---

# Section 1: Application Overview (Markdown Cell)
st.markdown("""
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

# Section 2: Setup and Library Imports (Markdown Cell & Code Cell)
st.markdown("## Section 2: Setup and Library Imports")
st.markdown("First, we import all necessary Python libraries. This ensures that all required functionalities for data generation, manipulation, simulation, and visualization are available.")
st.markdown("""
The required libraries have been successfully loaded. We are now ready to define the parameters for our simulation and proceed with data generation and analysis.
""")

# Section 3: Define Configuration Parameters (User Interaction) (Markdown Cell & Code Cell)
st.markdown("## Section 3: Define Configuration Parameters (User Interaction)")
st.markdown("""
This section allows users to interactively set the parameters for the AI security vulnerability simulation. These parameters control the characteristics of the synthetic data and the nature of the simulated attack. Inline help text is provided for each control.

**Key parameters are:**
-   **Attack Intensity ($A_{intensity}$):** Controls the severity of the attack, ranging from $0.0$ (no attack) to $1.0$ (maximum intensity).
-   **Attack Type:** Determines the specific type of vulnerability being simulated (e.g., Prompt Injection, Data Poisoning).
-   **Number of Compromised Agents ($N_{agents}$):** Specifies how many of the simulated agents are affected by the attack.
""")
st.write("---")
st.markdown("### Current Simulation Parameters")
st.write(f"**Selected Attack Intensity:** {st.session_state.selected_attack_intensity}")
st.write(f"**Selected Attack Type:** {st.session_state.selected_attack_type}")
st.write(f"**Selected Number of Compromised Agents:** {st.session_state.selected_num_compromised_agents}")
st.write(f"**Simulation Duration (Hours):** {SIMULATION_DURATION_HOURS}")
st.write(f"**Number of Agents:** {NUM_AGENTS}")
st.write(f"**Base Alert Rate (Per Hour):** {BASE_ALERT_RATE_PER_HOUR}")
st.write(f"**Anomaly Rate Multiplier:** {ANOMALY_RATE_MULTIPLIER}")
st.write(f"**Random Seed:** {RANDOM_SEED}")
st.write("---")


# Section 4: Mathematical Foundations of Attack Simulation (Markdown Cell & Code Cell)
st.markdown("## Section 4: Mathematical Foundations of Attack Simulation")
st.markdown("""
To simulate the impact of AI security vulnerabilities concretely, we define mathematical relationships that govern how attacks influence key system metrics. These relationships ensure a quantifiable and consistent effect based on the chosen attack parameters.

#### Alert Frequency Over Time
The alert frequency under attack, $F_{alerts\_attacked}(t)$, is modeled as an increase over the baseline frequency, $F_{alerts\_base}(t)$, proportional to the attack intensity and a type-specific coefficient:
$$F_{alerts\_attacked}(t) = F_{alerts\_base}(t) \cdot (1 + A_{intensity} \cdot C_{type})$$
Where:
-   $A_{intensity}$ is the user-defined attack intensity, $A_{intensity} \in [0, 1]$.
-   $C_{type}$ is a scaling factor specific to the `Attack Type`, reflecting its inherent impact potential (e.g., a data poisoning attack might have a higher $C_{type}$ than a mild prompt injection).

#### Detection Latency
The simulated detection latency, $L_{detection}$, represents the delay between an attack incident and its detection. It increases with attack intensity:
$$L_{detection} = L_{base} + A_{intensity} \cdot D_{type}$$
Where:
-   $L_{base}$ is a nominal baseline detection latency.
-   $D_{type}$ is a coefficient related to the `Attack Type`, representing how challenging that specific attack is to detect quickly.

#### Agent Integrity Score
The integrity score for a compromised agent, $I_{agent\_attacked}$, is reduced from its baseline, $I_{agent\_base}$, based on attack intensity and type:
$$I_{agent\_attacked} = I_{agent\_base} \cdot (1 - A_{intensity} \cdot K_{type})$$
Where:
-   $K_{type}$ is a coefficient for the `Attack Type`, reflecting its detrimental effect on agent trustworthiness or operational integrity. For uncompromised agents, $I_{agent\_attacked} = I_{agent\_base}$.

These formulae provide a structured way to quantify the effects of 'synthetic-identity risk' and 'data poisoning' on system metrics, making the simulation robust and interpretable.
""")
st.markdown("""
The mathematical models above conceptually guide the implementation of the attack simulation logic. They provide the framework for how `attack_intensity` and `attack_type` will quantitatively alter the synthetic security metrics in the following steps.
""")

# Section 5: Synthetic Data Generation - Core Function Implementation (Markdown Cell & Code Cell)
st.markdown("## Section 5: Synthetic Data Generation - Core Function Implementation")
st.markdown("""
To provide a controlled environment for studying AI security, we first generate a synthetic dataset. This dataset simulates sensor readings from industrial equipment, communication logs from AI agents, and baseline security metrics. It includes realistic numeric, categorical, and time-series data, sufficient for demonstrating the lab's concepts without needing external data. A lightweight sample is ensured for quick execution.
""")

# Extracted function from notebook
def generate_synthetic_safety_data(num_agents, simulation_duration_hours, base_alert_rate, anomaly_rate_multiplier, random_seed):
    """
    Generates a synthetic dataset simulating an industrial safety monitoring environment.
    This includes sensor data, agent communication logs, and baseline security metrics,
    with realistic numeric, categorical, and time-series fields.

    Arguments:
        num_agents (int): The number of AI agents to simulate.
        simulation_duration_hours (int): The total duration of the simulation in hours.
        base_alert_rate (float): The baseline rate of security alerts per hour.
        anomaly_rate_multiplier (float): A multiplier for introducing anomalies in the data.
        random_seed (int): Seed for random number generation to ensure reproducibility.

    Output:
        sensor_data_df (DataFrame): Time-series sensor readings.
        agent_logs_df (DataFrame): Simulated agent communication logs.
        base_security_metrics_df (DataFrame): Baseline security metrics (alert frequency, agent integrity scores).
        simulation_config (dict): Dictionary containing parameters used for generation.
    """

    # --- 1. Input Validation ---
    if not isinstance(num_agents, int):
        raise TypeError("num_agents must be an integer.")
    if not isinstance(simulation_duration_hours, int):
        raise TypeError("simulation_duration_hours must be an integer.")
    if not isinstance(base_alert_rate, (int, float)):
        raise TypeError("base_alert_rate must be a float or integer.")
    if not isinstance(anomaly_rate_multiplier, (int, float)):
        raise TypeError("anomaly_rate_multiplier must be a float or integer.")
    if not isinstance(random_seed, int):
        raise TypeError("random_seed must be an integer.")

    if num_agents < 0:
        raise ValueError("num_agents cannot be negative.")
    if simulation_duration_hours < 0:
        raise ValueError("simulation_duration_hours cannot be negative.")
    if base_alert_rate < 0:
        raise ValueError("base_alert_rate cannot be negative.")
    if anomaly_rate_multiplier < 0:
        raise ValueError("anomaly_rate_multiplier cannot be negative.")

    # --- 2. Initialize Random Number Generator for reproducibility ---
    rng = np.random.default_rng(random_seed)

    # --- 3. Simulation Configuration ---
    simulation_config = {
        'num_agents': num_agents,
        'simulation_duration_hours': simulation_duration_hours,
        'base_alert_rate': base_alert_rate,
        'anomaly_rate_multiplier': anomaly_rate_multiplier,
        'random_seed': random_seed
    }

    # --- 4. Handle Edge Cases (zero agents or zero duration) ---
    if num_agents == 0 or simulation_duration_hours == 0:
        empty_sensor_df = pd.DataFrame(columns=['timestamp', 'agent_id', 'sensor_type', 'value', 'unit', 'status'])
        empty_agent_logs_df = pd.DataFrame(columns=['timestamp', 'agent_id', 'log_type', 'severity', 'message'])
        empty_metrics_df = pd.DataFrame(columns=['agent_id', 'total_alerts_generated', 'average_integrity_score', 'last_alert_time'])
        return empty_sensor_df, empty_agent_logs_df, empty_metrics_df, simulation_config

    # --- 5. Generate Simulation Timestamps ---
    start_time = pd.Timestamp('2023-01-01 00:00:00') # Fixed start time for reproducibility
    end_time = start_time + pd.Timedelta(hours=simulation_duration_hours)
    
    # Use finer granularity for shorter durations to ensure enough data points
    freq = '10min'
    if simulation_duration_hours < 1:
        freq = '1min'

    simulation_timestamps = pd.date_range(start=start_time, end=end_time, freq=freq)
    
    # Ensure at least one timestamp if duration is positive but too short for chosen freq
    if len(simulation_timestamps) == 0:
        simulation_timestamps = pd.Series([start_time])
        
    num_timesteps = len(simulation_timestamps)


    # --- 6. Generate Sensor Data ---
    sensor_data_records = []
    sensor_types = ['temperature', 'pressure', 'vibration']
    sensor_units = {'temperature': '°C', 'pressure': 'kPa', 'vibration': 'mm/s'}
    base_values = {'temperature': 25.0, 'pressure': 100.0, 'vibration': 5.0}
    noise_stds = {'temperature': 2.0, 'pressure': 5.0, 'vibration': 1.0}

    # Calculate probability of an anomaly in a single sensor reading
    readings_per_hour_per_sensor = (60 / int(freq.replace('min','')))
    total_sensor_readings_per_hour = num_agents * len(sensor_types) * readings_per_hour_per_sensor
    # Distribute the `base_alert_rate` (alerts per hour) across all individual sensor readings
    p_sensor_anomaly_per_reading = (base_alert_rate * anomaly_rate_multiplier) / total_sensor_readings_per_hour

    for agent_id in range(1, num_agents + 1):
        for ts in simulation_timestamps:
            for sensor_type in sensor_types:
                base = base_values[sensor_type]
                std = noise_stds[sensor_type]
                
                value = rng.normal(base, std)
                status = 'normal'

                if rng.random() < p_sensor_anomaly_per_reading:
                    anomaly_magnitude = rng.uniform(2, 5) * std # Larger deviation
                    value += rng.choice([-1, 1]) * anomaly_magnitude
                    status = rng.choice(['warning', 'critical'], p=[0.7, 0.3])

                sensor_data_records.append({
                    'timestamp': ts,
                    'agent_id': agent_id,
                    'sensor_type': sensor_type,
                    'value': round(value, 2),
                    'unit': sensor_units[sensor_type],
                    'status': status
                })
    sensor_data_df = pd.DataFrame(sensor_data_records)

    # --- 7. Generate Agent Communication Logs ---
    agent_log_records = []
    log_types = ['heartbeat', 'data_transfer', 'status_update', 'configuration_change']
    severities = {'heartbeat': 'INFO', 'data_transfer': 'INFO', 'status_update': 'INFO',
                  'configuration_change': 'INFO', 'alert_generated': 'WARNING'} # Add alert_generated severity
    messages = {
        'heartbeat': "Agent operational check.",
        'data_transfer': "Transferred sensor data to central server.",
        'status_update': "Reporting system status as normal.",
        'configuration_change': "Configuration updated successfully."
    }

    # Base frequency for non-alert logs (e.g., 2 logs per agent per hour)
    expected_normal_logs_per_agent_per_hour = 2
    total_normal_logs = int(expected_normal_logs_per_agent_per_hour * num_agents * simulation_duration_hours)
    
    # Expected number of alert logs based on base_alert_rate
    total_alert_logs = int(base_alert_rate * simulation_duration_hours * anomaly_rate_multiplier)

    # Ensure a minimum number of logs if simulation duration is very short but non-zero
    min_logs_per_agent = 1
    total_normal_logs = max(total_normal_logs, min_logs_per_agent * num_agents)
    total_alert_logs = max(total_alert_logs, 1) if base_alert_rate > 0 and simulation_duration_hours > 0 else 0


    # Generate normal logs
    if total_normal_logs > 0:
        for _ in range(total_normal_logs):
            ts = rng.choice(simulation_timestamps)
            agent_id = rng.choice(range(1, num_agents + 1))
            log_type = rng.choice(log_types)
            agent_log_records.append({
                'timestamp': ts,
                'agent_id': agent_id,
                'log_type': log_type,
                'severity': severities[log_type],
                'message': messages[log_type]
            })

    # Generate alert logs
    if total_alert_logs > 0:
        for _ in range(total_alert_logs):
            ts = rng.choice(simulation_timestamps)
            agent_id = rng.choice(range(1, num_agents + 1))
            severity = rng.choice(['WARNING', 'ERROR'], p=[0.7, 0.3])
            message = "CRITICAL ALERT: Abnormal condition detected in monitored area." if severity == 'ERROR' else "ALERT: Potential anomaly detected."
            
            agent_log_records.append({
                'timestamp': ts,
                'agent_id': agent_id,
                'log_type': 'alert_generated',
                'severity': severity,
                'message': message
            })

    agent_logs_df = pd.DataFrame(agent_log_records).sort_values(by='timestamp').reset_index(drop=True)
    
    # --- 8. Generate Base Security Metrics ---
    metrics_records = []
    
    for agent_id in range(1, num_agents + 1):
        agent_alerts = agent_logs_df[(agent_logs_df['agent_id'] == agent_id) &
                                     (agent_logs_df['log_type'] == 'alert_generated')]
        total_alerts_generated = len(agent_alerts)

        last_alert_time = agent_alerts['timestamp'].max() if not agent_alerts.empty else pd.NaT

        # Agent integrity score (0-100, lower for more alerts)
        base_integrity = 95.0
        # Scale deviation by simulation duration and number of agents for consistent impact
        deviation_factor = total_alerts_generated / (simulation_duration_hours * num_agents + 1e-6) # Alerts per agent per hour
        integrity_deviation = deviation_factor * 10.0 # Scale factor for impact
        
        integrity_score = max(0.0, min(100.0, base_integrity - integrity_deviation + rng.normal(0, 2)))

        metrics_records.append({
            'agent_id': agent_id,
            'total_alerts_generated': total_alerts_generated,
            'average_integrity_score': round(integrity_score, 2),
            'last_alert_time': last_alert_time
        })
    base_security_metrics_df = pd.DataFrame(metrics_records)

    return sensor_data_df, agent_logs_df, base_security_metrics_df, simulation_config

# Call data generation and display results
sensor_data_baseline, agent_logs_baseline, security_metrics_baseline, sim_config = generate_synthetic_safety_data(
    num_agents=NUM_AGENTS,
    simulation_duration_hours=SIMULATION_DURATION_HOURS,
    base_alert_rate=BASE_ALERT_RATE_PER_HOUR,
    anomaly_rate_multiplier=ANOMALY_RATE_MULTIPLIER,
    random_seed=RANDOM_SEED
)

st.subheader("Synthetic Data (Baseline)")
st.write("--- Sensor Data (Baseline) ---")
st.dataframe(sensor_data_baseline.head())
st.write("--- Agent Logs (Baseline) ---")
st.dataframe(agent_logs_baseline.head())
st.write("--- Security Metrics (Baseline) ---")
st.dataframe(security_metrics_baseline.head())

st.markdown("""
The synthetic dataset has been successfully generated. We now have a baseline representation of an industrial safety monitoring system, including sensor data, agent communications, and unattacked security metrics. This synthetic data simulates the operational environment before any security vulnerabilities are introduced.
""")


# Section 6: Data Validation and Initial Statistics (Markdown Cell & Code Cell)
st.markdown("## Section 6: Data Validation and Initial Statistics")
st.markdown("""
Data validation is a crucial step to ensure the integrity and quality of our synthetic dataset. This process confirms expected column names, data types, and primary-key uniqueness, and asserts the absence of missing values in critical fields. Summary statistics for numeric columns provide an initial understanding of the data distribution.
""")

# Extracted function from notebook
def validate_and_summarize_data(df, df_name, expected_columns, expected_dtypes, critical_fields_no_null, unique_key):
    """
    Confirms the integrity, types, and absence of critical missing values in a DataFrame,
    logs validation results, asserts critical conditions, and prints summary statistics.
    """
    
    st.write(f"--- Starting Validation for DataFrame: {df_name} ---")

    # 1. Input Type Validation
    if not isinstance(df, pd.DataFrame):
        st.error(f"[{df_name}] ERROR: Expected a pandas DataFrame, but received type: {type(df)}")
        raise TypeError(f"[{df_name}] ERROR: Expected a pandas DataFrame, but received type: {type(df)}")
    st.info(f"[{df_name}] INFO: DataFrame type check passed.")

    # 2. Column Presence Validation
    missing_columns = [col for col in expected_columns if col not in df.columns]
    if missing_columns:
        st.error(f"[{df_name}] ERROR: Missing expected columns: {", ".join(missing_columns)}")
        raise AssertionError(f"[{df_name}] ERROR: Missing expected columns: {", ".join(missing_columns)}")
    st.info(f"[{df_name}] INFO: All expected columns are present.")

    # 3. Data Type Validation
    for col, expected_dtype in expected_dtypes.items():
        if col not in df.columns: # Skip type check if column is already identified as missing
            continue
        actual_dtype = str(df[col].dtype)
        if actual_dtype != expected_dtype:
            st.error(f"[{df_name}] ERROR: Column '{col}' has incorrect data type. Expected '{expected_dtype}', got '{actual_dtype}'.")
            raise AssertionError(f"[{df_name}] ERROR: Column '{col}' has incorrect data type. Expected '{expected_dtype}', got '{actual_dtype}'.")
    st.info(f"[{df_name}] INFO: All column data types match expectations.")

    # 4. Critical Fields No Nulls Validation
    if critical_fields_no_null:  # Evaluates to False if None or empty list
        for field in critical_fields_no_null:
            if field not in df.columns: # Skip if column is already identified as missing
                continue
            if df[field].isnull().any():
                st.error(f"[{df_name}] ERROR: Critical field '{field}' contains missing values (NaN/None).")
                raise AssertionError(f"[{df_name}] ERROR: Critical field '{field}' contains missing values (NaN/None).")
        st.info(f"[{df_name}] INFO: Critical fields are free of missing values.")
    else:
        st.info(f"[{df_name}] INFO: No critical fields specified for null checks. Skipping.")

    # 5. Unique Key Validation
    if unique_key is not None:
        key_list = []
        if isinstance(unique_key, str):
            key_list = [unique_key]
        elif isinstance(unique_key, list):
            key_list = unique_key
        else:
            st.error(f"[{df_name}] ERROR: 'unique_key' must be a string or a list of strings, got {type(unique_key)}.")
            raise TypeError(f"[{df_name}] ERROR: 'unique_key' must be a string or a list of strings, got {type(unique_key)}.")

        if not key_list: # Handle empty list after conversion
            st.info(f"[{df_name}] INFO: 'unique_key' was provided as an empty list. Skipping unique key validation.")
        else:
            missing_key_cols = [col for col in key_list if col not in df.columns]
            if missing_key_cols:
                st.error(f"[{df_name}] ERROR: Unique key columns are missing from DataFrame: {", ".join(missing_key_cols)}")
                raise AssertionError(f"[{df_name}] ERROR: Unique key columns are missing from DataFrame: {", ".join(missing_key_cols)}")

            if df.duplicated(subset=key_list).any():
                st.error(f"[{df_name}] ERROR: Unique key '{", ".join(key_list)}' contains duplicate entries.")
                raise AssertionError(f"[{df_name}] ERROR: Unique key '{", ".join(key_list)}' contains duplicate entries.")
            st.info(f"[{df_name}] INFO: Unique key validation passed.")
    else: # unique_key is None
        st.info(f"[{df_name}] INFO: No unique key provided. Skipping unique key validation.")

    # 6. Summary Statistics for numeric columns
    numeric_cols = df.select_dtypes(include=np.number).columns
    if not numeric_cols.empty:
        st.write(f"\n[{df_name}] INFO: Summary Statistics for Numeric Columns:")
        st.dataframe(df[numeric_cols].describe())
    else:
        st.info(f"\n[{df_name}] INFO: No numeric columns found for summary statistics.")
        
    st.write(f"--- Validation for DataFrame: {df_name} Completed Successfully ---\n")

# Define expected columns and dtypes for validation
sensor_expected_columns = ['timestamp', 'agent_id', 'sensor_type', 'value', 'unit', 'status']
sensor_expected_dtypes = {'timestamp': 'datetime64[ns]', 'agent_id': 'int64', 'sensor_type': 'object', 'value': 'float64', 'unit': 'object', 'status': 'object'}

agent_logs_expected_columns = ['timestamp', 'agent_id', 'log_type', 'severity', 'message']
agent_logs_expected_dtypes = {'timestamp': 'datetime64[ns]', 'agent_id': 'int64', 'log_type': 'object', 'severity': 'object', 'message': 'object'}

security_metrics_expected_columns = ['agent_id', 'total_alerts_generated', 'average_integrity_score', 'last_alert_time']
security_metrics_expected_dtypes = {'agent_id': 'int64', 'total_alerts_generated': 'int64', 'average_integrity_score': 'float64', 'last_alert_time': 'datetime64[ns]'}

# Call `validate_and_summarize_data` for each baseline DataFrame
try:
    validate_and_summarize_data(sensor_data_baseline, "Sensor Data", sensor_expected_columns, sensor_expected_dtypes, critical_fields_no_null=['timestamp', 'value'], unique_key=['timestamp', 'agent_id', 'sensor_type'])
    validate_and_summarize_data(agent_logs_baseline, "Agent Logs", agent_logs_expected_columns, agent_logs_expected_dtypes, critical_fields_no_null=['timestamp', 'log_type'], unique_key=None)
    validate_and_summarize_data(security_metrics_baseline, "Security Metrics", security_metrics_expected_columns, security_metrics_expected_dtypes, critical_fields_no_null=['agent_id', 'average_integrity_score'], unique_key=['agent_id'])
    st.success("All baseline datasets passed validation checks.")
except (TypeError, AssertionError) as e:
    st.error(f"Data validation failed: {e}")

st.markdown("""
The synthetic datasets have passed validation checks, confirming their structural integrity and data types. The summary statistics provide a preliminary understanding of the distributions within the data, which forms a reliable foundation for simulating attacks.
""")

# Section 7: Vulnerability Simulation - Attack Logic Implementation (Markdown Cell & Code Cell)
st.markdown("## Section 7: Vulnerability Simulation - Attack Logic Implementation")
st.markdown("""
This section details the core logic for simulating AI security vulnerabilities. The `simulate_vulnerability_impact` function applies the mathematical models defined earlier to modify the baseline security metrics based on the user-selected `Attack Type`, `Attack Intensity`, and `Number of Compromised Agents`. This simulation will demonstrate the effects of 'synthetic-identity risk' (compromised agents acting maliciously) and 'untraceable data leakage' (covert data exfiltration via altered behavior).
""")

# Extracted function from notebook
def simulate_vulnerability_impact(base_metrics_df, attack_type, attack_intensity, num_compromised_agents, simulation_config):
    """
    Applies the mathematical effects of a selected AI-security vulnerability to baseline security metrics,
    increasing alert frequency, decreasing agent integrity scores, and introducing detection latency.
    
    Arguments:
        base_metrics_df (DataFrame): The baseline security metrics DataFrame before any attack.
        attack_type (str): The chosen type of AI security vulnerability to simulate.
        attack_intensity (float): A float between 0 and 1 indicating the severity of the attack.
        num_compromised_agents (int): The number of simulated agents affected by the attack.
        simulation_config (dict): Dictionary containing simulation parameters like 'random_seed' and 'start_time'.
    
    Output:
        attacked_security_metrics_df (DataFrame): Security metrics modified by the simulated attack.
        attack_events_df (DataFrame): Details of when and how attacks occurred, including simulated detection latency.
    """

    # Validate attack_type
    if attack_type not in COEFFS['C_type']:
        raise ValueError(f"Unknown attack_type: '{attack_type}'. Must be one of {list(COEFFS['C_type'].keys())}")

    # Validate attack_intensity
    if not (0 <= attack_intensity <= 1):
        raise ValueError(f"attack_intensity ({attack_intensity}) must be between 0 and 1.")

    # Create a deep copy of the base DataFrame to modify
    attacked_security_metrics_df = base_metrics_df.copy()

    all_agent_ids = attacked_security_metrics_df['agent_id'].unique()
    total_agents = len(all_agent_ids)

    # Validate num_compromised_agents
    if num_compromised_agents < 0 or num_compromised_agents > total_agents:
        raise ValueError(f"num_compromised_agents ({num_compromised_agents}) must be between 0 and the total number of agents ({total_agents}).")

    # Initialize a RandomState for deterministic agent selection if a seed is provided
    rng = np.random.RandomState(simulation_config.get('random_seed'))

    # Select compromised agents if any
    compromised_agents_ids = set()
    if num_compromised_agents > 0:
        compromised_agents_ids = set(rng.choice(all_agent_ids, size=num_compromised_agents, replace=False))

    # Retrieve attack-specific coefficients
    C_coeff = COEFFS['C_type'][attack_type]
    K_coeff = COEFFS['K_type'][attack_type]
    D_coeff = COEFFS['D_type'][attack_type]
    L_base = COEFFS['L_base']

    # Apply impact to 'alert_frequency' (system-wide effect)
    if attack_intensity > 0:
        if 'alert_frequency' not in attacked_security_metrics_df.columns:
            attacked_security_metrics_df['alert_frequency'] = attacked_security_metrics_df['total_alerts_generated'] / simulation_config['simulation_duration_hours']
        attacked_security_metrics_df['alert_frequency'] *= (1 + attack_intensity * C_coeff)

    # Apply impact to 'agent_integrity_score' (only for compromised agents)
    if compromised_agents_ids:
        attacked_security_metrics_df.loc[
            attacked_security_metrics_df['agent_id'].isin(list(compromised_agents_ids)),
            'average_integrity_score'
        ] *= (1 - attack_intensity * K_coeff)

    # Prepare the attack events DataFrame
    attack_events_df = pd.DataFrame(columns=['timestamp', 'attack_type', 'attack_intensity',
                                             'num_compromised_agents', 'attack_severity', 'detection_latency'])

    # Log an attack event only if there was an actual attack impact
    if attack_intensity > 0 or num_compromised_agents > 0:
        detection_latency = L_base + attack_intensity * D_coeff
        
        # A simple linear model for severity for logging purposes
        attack_severity = attack_intensity * num_compromised_agents

        attack_events_data = {
            'timestamp': pd.Timestamp('2023-01-01 00:00:00'),
            'attack_type': attack_type,
            'attack_intensity': attack_intensity,
            'num_compromised_agents': num_compromised_agents,
            'attack_severity': attack_severity,
            'detection_latency': detection_latency
        }
        attack_events_df = pd.DataFrame([attack_events_data])
    
    # Ensure `alert_frequency` is always present for the plotting function.
    if 'alert_frequency' not in attacked_security_metrics_df.columns:
        if simulation_config['simulation_duration_hours'] > 0:
            attacked_security_metrics_df['alert_frequency'] = attacked_security_metrics_df['total_alerts_generated'] / simulation_config['simulation_duration_hours']
        else:
            attacked_security_metrics_df['alert_frequency'] = 0.0

    return attacked_security_metrics_df, attack_events_df

# Call simulation function
sim_config['start_time'] = pd.Timestamp('2023-01-01 00:00:00') # Ensure start_time for attack events

security_metrics_attacked, attack_events = simulate_vulnerability_impact(
    base_metrics_df=security_metrics_baseline,
    attack_type=st.session_state.selected_attack_type,
    attack_intensity=st.session_state.selected_attack_intensity,
    num_compromised_agents=st.session_state.selected_num_compromised_agents,
    simulation_config=sim_config
)

st.subheader("Simulated Attack Results")
st.write("--- Attacked Security Metrics ---")
st.dataframe(security_metrics_attacked.head())
st.write("--- Attack Events ---")
st.dataframe(attack_events.head())

st.markdown("""
The simulation of the chosen AI security vulnerability has been applied to the baseline security metrics. We now have a modified dataset that reflects the impact of the attack on alert frequency, agent integrity, and provides details on simulated detection latency. This data will be used for visualization and further analysis.
""")

# Section 8: Trend Plot: Alert Frequency Over Time - Implementation (Markdown Cell & Code Cell)
st.markdown("## Section 8: Trend Plot: Alert Frequency Over Time - Implementation")
st.markdown("""
A trend plot is essential for visualizing time-based metrics. This line plot will compare the `Alert Frequency over Time` for both the baseline (unattacked) and the attacked scenarios. It provides a clear visual representation of how the simulated vulnerability impacts the system's ability to generate alerts, reflecting the concept of prompt injection 'hijacking LLM behavior' or data poisoning causing 'malicious samples' to alter outputs.
""")

# Extracted function from notebook
def plot_alert_frequency_trend(base_df, attacked_df, attack_type, attack_intensity, font_size):
    """
    Generates and displays a line plot showing alert frequency over time, comparing
    the baseline (unattacked) scenario to the attacked scenario. The plot is saved
    as a PNG file.
    """
    # Ensure required columns exist. Direct access will raise KeyError if missing,
    # which is expected by test cases.
    _ = base_df['timestamp']
    _ = base_df['alert_frequency']
    _ = attacked_df['timestamp']
    _ = attacked_df['alert_frequency']

    # Set seaborn style for better aesthetics and get color palette (mocked in tests)
    sns.set_style("whitegrid")
    colors = sns.color_palette("deep", 2)

    fig, ax = plt.subplots(figsize=(12, 7)) # Capture figure object for Streamlit

    # Plot baseline data
    ax.plot(base_df['timestamp'], base_df['alert_frequency'],
             label='Baseline', color=colors[0], linewidth=2)

    # Plot attacked data
    ax.plot(attacked_df['timestamp'], attacked_df['alert_frequency'],
             label=f'Attacked ({attack_type})', color=colors[1], linewidth=2)

    # Set plot title, labels, and legend
    title_text = f"Alert Frequency Over Time ({attack_type} at {attack_intensity*100:.0f}% Intensity)"
    ax.set_title(title_text, fontsize=font_size)
    ax.set_xlabel('Time', fontsize=font_size)
    ax.set_ylabel('Alert Frequency', fontsize=font_size)
    ax.legend(fontsize=font_size * 0.9) # Slightly smaller font for legend

    # Add grid for readability
    ax.grid(True)

    # Adjust layout to prevent labels/title from overlapping
    fig.tight_layout()

    # Streamlit displays the figure, no need to save to file for direct display
    # plt.savefig("alert_frequency_trend.png") # Not needed for Streamlit direct display
    # plt.show() # Not needed for Streamlit direct display

    return fig # Return figure for st.pyplot

# Prepare data for plotting trend
start_time = pd.Timestamp('2023-01-01 00:00:00')
simulation_duration_hours = SIMULATION_DURATION_HOURS
num_agents = NUM_AGENTS
base_alert_rate = BASE_ALERT_RATE_PER_HOUR

end_time = start_time + pd.Timedelta(hours=simulation_duration_hours)
freq = '10min'
if simulation_duration_hours < 1:
    freq = '1min'
plot_timestamps = pd.date_range(start=start_time, end=end_time, freq=freq)

if len(plot_timestamps) == 0:
    plot_timestamps = pd.Series([start_time])

baseline_alert_frequencies = [base_alert_rate + np.random.normal(0, 0.5) for _ in range(len(plot_timestamps))]
base_df_for_plot = pd.DataFrame({
    'timestamp': plot_timestamps,
    'alert_frequency': baseline_alert_frequencies
})

C_coeff = COEFFS['C_type'][st.session_state.selected_attack_type]
attacked_alert_rates = [
    rate * (1 + st.session_state.selected_attack_intensity * C_coeff) + np.random.normal(0, 0.5)
    for rate in baseline_alert_frequencies
]
attacked_df_for_plot = pd.DataFrame({
    'timestamp': plot_timestamps,
    'alert_frequency': attacked_alert_rates
})

# Call and display the plotting function
fig_trend = plot_alert_frequency_trend(
    base_df=base_df_for_plot,
    attacked_df=attacked_df_for_plot,
    attack_type=st.session_state.selected_attack_type,
    attack_intensity=st.session_state.selected_attack_intensity,
    font_size=14
)
st.pyplot(fig_trend)
plt.close(fig_trend) # Close the figure to free memory

st.markdown("""
The trend plot clearly illustrates the increase in alert frequency after the simulated attack. This direct visualization helps in understanding the real-time impact of AI security vulnerabilities on system monitoring and response, aligning with the concept that attacks can significantly alter system behavior.
""")

# Section 9: Relationship Plot: Attack Severity vs. Detection Latency - Implementation (Markdown Cell & Code Cell)
st.markdown("## Section 9: Relationship Plot: Attack Severity vs. Detection Latency - Implementation")
st.markdown("""
To examine correlations between attack characteristics and the system's response, a relationship plot is crucial. This scatter plot displays 'Attack Severity' against 'Simulated Detection Latency'. This visualization helps in understanding if more severe attacks are harder or slower to detect, providing insights into the challenges of detecting 'untraceable data leakage' or sophisticated 'synthetic-identity risk' incidents.
""")

# Extracted function from notebook
def plot_attack_severity_vs_latency(attack_events_df, font_size):
    """
    Generates and displays a scatter plot to examine the correlation between attack severity and simulated detection latency.
    The plot is saved as a PNG file.
    Arguments:
    attack_events_df (DataFrame): DataFrame detailing attack events, including severity and latency.
    font_size (int): The base font size for plot elements.
    Output:
    None: Displays the plot and saves it as "attack_severity_latency_plot.png".
    """

    # Ensure required columns exist
    _ = attack_events_df['attack_severity']
    _ = attack_events_df['detection_latency']

    fig, ax = plt.subplots(figsize=(10, 6)) # Capture figure object

    # Set seaborn's color palette as per test requirements
    sns.set_palette("colorblind")

    # Generate the scatter plot
    sns.scatterplot(x='attack_severity', y='detection_latency', data=attack_events_df, ax=ax, s=100, hue='attack_type', style='attack_type')

    # Set plot title and labels with the specified font size
    ax.set_title('Attack Severity vs. Simulated Detection Latency', fontsize=font_size)
    ax.set_xlabel('Attack Severity', fontsize=font_size)
    ax.set_ylabel('Simulated Detection Latency (Minutes)', fontsize=font_size)

    # Add grid for better readability
    ax.grid(True)

    # Add legend if there are multiple attack types, otherwise it might not be necessary for a single point
    if len(attack_events_df['attack_type'].unique()) > 1:
        ax.legend(title='Attack Type', fontsize=font_size*0.9, title_fontsize=font_size)
    elif len(attack_events_df) > 1: # If multiple events of same type, still show a point legend
         ax.legend(title='Attack Event', fontsize=font_size*0.9, title_fontsize=font_size)
    elif len(attack_events_df) == 1 and st.session_state.selected_attack_intensity > 0: # If only one attack event is logged (current scenario)
        ax.legend(title='Attack Type', fontsize=font_size*0.9, title_fontsize=font_size) # Show legend for the single type
    
    fig.tight_layout()
    return fig # Return figure for st.pyplot

# Call and display the plotting function
if not attack_events.empty:
    fig_rel = plot_attack_severity_vs_latency(attack_events_df=attack_events, font_size=14)
    st.pyplot(fig_rel)
    plt.close(fig_rel)
else:
    st.info("No attack events to plot for Attack Severity vs. Detection Latency.")


st.markdown("""
The scatter plot reveals the simulated relationship between the severity of an attack and the system's detection latency. This visualization helps users understand that more intense or complex attacks might lead to longer detection times, highlighting a critical aspect of AI security vulnerability analysis.
""")

# Section 10: Aggregated Comparison: Agent Integrity Scores - Implementation (Markdown Cell & Code Cell)
st.markdown("## Section 10: Aggregated Comparison: Agent Integrity Scores - Implementation")
st.markdown("""
Assessing the integrity of individual agents under attack is vital for understanding 'synthetic-identity risk'. This bar chart compares the average 'Agent Integrity Scores' for compromised versus uncompromised agents, providing a clear aggregated view of the attack's impact on agent trustworthiness or performance.
""")

# Extracted function from notebook
def plot_agent_integrity_comparison(attacked_df, num_compromised_agents, font_size):
    """
    Generates and displays a bar chart comparing the average agent integrity scores for compromised versus uncompromised agents under attack conditions. The plot is saved as a PNG file.
    Arguments:
        attacked_df (DataFrame): DataFrame with security metrics modified by the attack.
        num_compromised_agents (int): The count of simulated agents affected by the attack, used to differentiate groups.
        font_size (int): The base font size for plot elements.
    Output:
        None: Displays the plot and saves it as "agent_integrity_comparison.png".
    """

    # --- 1. Input Validation ---
    if not isinstance(attacked_df, pd.DataFrame):
        raise TypeError("attacked_df must be a pandas DataFrame.")
    if not all(col in attacked_df.columns for col in ['agent_id', 'average_integrity_score']):
        missing_cols = [col for col in ['agent_id', 'average_integrity_score'] if col not in attacked_df.columns]
        raise KeyError(f"Missing required column(s) in attacked_df: {", ".join(missing_cols)}")
    if not isinstance(num_compromised_agents, int) or num_compromised_agents < 0:
        raise ValueError("num_compromised_agents must be a non-negative integer.")
    if not isinstance(font_size, (int, float)) or font_size <= 0:
        raise ValueError("font_size must be a positive number.")

    # --- 2. Data Preparation ---
    # Calculate average integrity score for each unique agent
    avg_scores_per_agent = attacked_df.groupby('agent_id')['average_integrity_score'].mean().reset_index()

    unique_agent_ids = avg_scores_per_agent['agent_id'].sort_values().tolist()
    total_unique_agents = len(unique_agent_ids)

    actual_num_compromised = min(num_compromised_agents, total_unique_agents)

    compromised_agent_ids = unique_agent_ids[:actual_num_compromised]
    uncompromised_agent_ids = unique_agent_ids[actual_num_compromised:]

    compromised_avg = avg_scores_per_agent[avg_scores_per_agent['agent_id'].isin(compromised_agent_ids)]['average_integrity_score'].mean()
    uncompromised_avg = avg_scores_per_agent[avg_scores_per_agent['agent_id'].isin(uncompromised_agent_ids)]['average_integrity_score'].mean()

    plot_data_list = []
    if not pd.isna(compromised_avg):
        plot_data_list.append({'Agent Status': 'Compromised', 'Average Integrity Score': compromised_avg})
    if not pd.isna(uncompromised_avg):
        plot_data_list.append({'Agent Status': 'Uncompromised', 'Average Integrity Score': uncompromised_avg})

    plot_df = pd.DataFrame(plot_data_list)
    
    if 'Compromised' in plot_df['Agent Status'].values and 'Uncompromised' in plot_df['Agent Status'].values:
        plot_df['Agent Status'] = pd.Categorical(plot_df['Agent Status'], categories=['Compromised', 'Uncompromised'], ordered=True)
        plot_df = plot_df.sort_values('Agent Status')

    # --- 3. Plotting ---
    fig, ax = plt.subplots(figsize=(8, 6)) # Capture figure object
    
    palette = {"Compromised": "salmon", "Uncompromised": "lightseagreen"}
    
    sns.barplot(
        x='Agent Status',
        y='Average Integrity Score',
        data=plot_df,
        palette=palette,
        ax=ax
    )

    ax.set_title('Average Agent Integrity Scores: Compromised vs. Uncompromised', fontsize=font_size + 2)
    ax.set_xlabel('Agent Status', fontsize=font_size)
    ax.set_ylabel('Average Integrity Score', fontsize=font_size)
    ax.tick_params(axis='x', labelsize=font_size)
    ax.tick_params(axis='y', labelsize=font_size)
    ax.set_ylim(0, 100)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    fig.tight_layout()
    return fig # Return figure for st.pyplot

# Call and display the plotting function
if not security_metrics_attacked.empty:
    fig_comp = plot_agent_integrity_comparison(
        attacked_df=security_metrics_attacked,
        num_compromised_agents=st.session_state.selected_num_compromised_agents,
        font_size=14
    )
    st.pyplot(fig_comp)
    plt.close(fig_comp)
else:
    st.info("No security metrics data available to compare agent integrity scores.")

st.markdown("""
The bar chart visually demonstrates the reduction in integrity scores for compromised agents compared to their uncompromised counterparts. This clear aggregated comparison highlights how vulnerabilities like 'synthetic-identity risk' can directly impact the perceived reliability and trustworthiness of individual AI agents within the system.
""")

# Section 11: Discussion of Results and Learning Outcomes (Markdown Cell)
st.markdown("## Section 11: Discussion of Results and Learning Outcomes")
st.markdown("""
Through this simulation, we have observed the tangible impacts of various AI security vulnerabilities on an agentic industrial safety monitoring system. The lab provided a hands-on experience in:

-   **Identifying Vulnerabilities**: We saw how 'synthetic-identity risk' and 'untraceable data leakage' manifest through changes in system alerts and agent integrity.
-   **Adversarial Testing**: The simulation of 'prompt injection' and 'data poisoning' illustrated how malicious inputs can significantly alter system behavior and outputs, mirroring how such attacks can 'hijack LLM behavior'.
-   **Analyzing Defenses**: By manipulating `Attack Intensity` and `Attack Type`, users can infer the necessity of robust 'risk controls in the assurance plan' and 'red teaming chains of agents' for continuous validation.
-   **Understanding System Response**: The plots revealed how an attack can increase alert frequency and potentially lengthen detection latency, emphasizing the need for adaptive systems to implement effective defenses.

This practical exposure reinforces the theoretical concepts of AI security and the importance of rigorous testing and validation in building trustworthy AI systems.
""")

# Section 12: Conclusion (Markdown Cell)
st.markdown("## Section 12: Conclusion")
st.markdown("""
This AI Security Vulnerability Simulation Lab successfully demonstrated the critical need for understanding and mitigating threats in agentic AI systems. By generating synthetic data and simulating various attack scenarios, users gained valuable insights into the practical implications of AI security vulnerabilities. The interactive nature of the lab allows for continuous exploration of different attack parameters, fostering a deeper comprehension of how to design and validate resilient AI systems.
""")

# Section 13: References (Markdown Cell)
st.markdown("## Section 13: References")
st.markdown("""
1.  **[1] Case 3: Agentic AI for Safety Monitoring, Provided Resource Document.** This document describes AI-security vulnerabilities like 'synthetic-identity risk' and 'untraceable data leakage', and the importance of rigorous testing and risk controls.
2.  **[2] Unit 6: Testing, Validation and AI Security, Adversarial Testing and Red-Teaming, Provided Resource Document.** This section explores threats like prompt injection and data poisoning, and discusses the impact of malicious samples on LLM output.
3.  **Pandas Library**: A fast, powerful, flexible and easy to use open source data analysis and manipulation tool, built on top of the Python programming language. (https://pandas.pydata.org/)
4.  **NumPy Library**: The fundamental package for scientific computing with Python. (https://numpy.org/)
5.  **Matplotlib Library**: A comprehensive library for creating static, animated, and interactive visualizations in Python. (https://matplotlib.org/)
6.  **Seaborn Library**: A Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics. (https://seaborn.pydata.org/)
7.  **IPywidgets Library**: Interactive HTML widgets for Jupyter notebooks and the IPython kernel. (https://ipywidgets.readthedocs.io/en/latest/)
""")