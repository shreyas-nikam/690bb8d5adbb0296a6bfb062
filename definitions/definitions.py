import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_synthetic_safety_data(num_agents, simulation_duration_hours, base_alert_rate, anomaly_rate_multiplier, random_seed):
    """This function creates a comprehensive synthetic dataset for simulating an industrial safety monitoring environment."""
    
    if simulation_duration_hours < 0:
        raise ValueError("Simulation duration must be positive.")
    if base_alert_rate < 0:
        raise ValueError("Base alert rate must be non-negative.")
    
    np.random.seed(random_seed)

    # Generate timestamps based on simulation duration
    start_time = datetime.now()
    timestamps = [start_time + timedelta(hours=i) for i in range(simulation_duration_hours)]
    
    # Generate sensor data
    sensor_data_list = []
    for agent_id in range(num_agents):
        for timestamp in timestamps:
            sensor_value = np.random.normal(loc=10, scale=5)
            alert_probability = base_alert_rate / 10
            alert_status = np.random.rand() < alert_probability
            sensor_data_list.append([timestamp, agent_id, f"sensor_type_{np.random.randint(1, 5)}", sensor_value, alert_status])
    
    sensor_data_df = pd.DataFrame(sensor_data_list, columns=["timestamp", "agent_id", "sensor_type", "sensor_value", "alert_status"])

    # Generate agent logs
    agent_logs_list = []
    for agent_id in range(num_agents):
        for timestamp in timestamps:
            message_type = np.random.choice(["INFO", "WARN", "ERROR"])
            message_content = f"Sample message from agent {agent_id}"
            agent_logs_list.append([timestamp, agent_id, message_type, message_content])
    
    agent_logs_df = pd.DataFrame(agent_logs_list, columns=["timestamp", "agent_id", "message_type", "message_content"])

    # Generate base security metrics
    base_security_metrics_list = []
    for agent_id in range(num_agents):
        integrity_score = 1.0 - anomaly_rate_multiplier * np.random.rand()
        alert_freq = (base_alert_rate + np.random.normal(0, 1)) * (1 + anomaly_rate_multiplier)
        base_security_metrics_list.append([agent_id, integrity_score, alert_freq])
    
    base_security_metrics_df = pd.DataFrame(base_security_metrics_list, columns=["agent_id", "integrity_score", "alert_frequency"])
    
    # Simulation config
    simulation_config = {
        "num_agents": num_agents,
        "simulation_duration_hours": simulation_duration_hours,
        "base_alert_rate": base_alert_rate,
        "anomaly_rate_multiplier": anomaly_rate_multiplier,
        "random_seed": random_seed
    }
    
    return sensor_data_df, agent_logs_df, base_security_metrics_df, simulation_config

def validate_and_summarize_data(df, df_name, expected_columns, expected_dtypes, critical_fields_no_null, unique_key):
    """
    Confirms data integrity, types, and absence of critical missing values within a DataFrame.
    Logs validation results, asserts critical conditions, and prints summary statistics for numeric columns.
    """

    # Check if expected columns are present
    if expected_columns:
        assert set(expected_columns) <= set(df.columns), f"{df_name}: Missing expected columns"

    # Check data types
    for col, dtype in expected_dtypes.items():
        assert df[col].dtype == dtype, f"{df_name}: Column {col} not of type {dtype}"

    # Check critical fields for nulls
    if critical_fields_no_null:
        for field in critical_fields_no_null:
            assert df[field].notnull().all(), f"{df_name}: Critical field {field} contains null values"

    # Check uniqueness of the unique key
    if unique_key:
        assert df.duplicated(subset=unique_key).sum() == 0, f"{df_name}: Duplicate values in unique key columns"

    # Print summary statistics for numeric columns
    print(f"{df_name} Summary Statistics:")
    print(df.describe())

def simulate_vulnerability_impact(base_metrics_df, attack_type, attack_intensity, num_compromised_agents, simulation_config):
    """Simulates the impact of an AI-security vulnerability."""
    
    if not 0 <= attack_intensity <= 1:
        raise ValueError("Attack intensity must be between 0 and 1.")
    
    if not isinstance(num_compromised_agents, int) or num_compromised_agents < 0:
        raise ValueError("Number of compromised agents must be a non-negative integer.")
    
    # Extract configuration values
    L_base = simulation_config['L_base']
    C_type = simulation_config['C_type_dict'][attack_type]
    K_type = simulation_config['K_type_dict'][attack_type]
    D_type = simulation_config['D_type_dict'][attack_type]
    
    # Calculate attack metrics
    adjusted_alert_frequency = base_metrics_df['alert_frequency'][0] + int(L_base * attack_intensity * num_compromised_agents)
    integrity_reduction = attack_intensity * C_type
    adjusted_integrity_score = base_metrics_df['agent_integrity_score'][0] - integrity_reduction
    detection_latency = int(D_type * (1 + attack_intensity * K_type))
    
    # Apply changes to the DataFrame
    attacked_metrics_df = base_metrics_df.copy()
    attacked_metrics_df['alert_frequency'] = adjusted_alert_frequency
    attacked_metrics_df['agent_integrity_score'] = adjusted_integrity_score

    attack_events_df = pd.DataFrame({
        'timestamp': base_metrics_df['timestamp'],
        'detection_latency': [detection_latency] * len(base_metrics_df)
    })
    
    return attacked_metrics_df, attack_events_df

import matplotlib.pyplot as plt
import pandas as pd

def plot_alert_frequency_trend(base_df, attacked_df, attack_type, attack_intensity, font_size):
    """
    Generates a line plot showing alert frequency over time for baseline and attacked scenarios.
    """
    
    # Check for validity of inputs
    if base_df is None or attacked_df is None:
        raise TypeError("DataFrames cannot be None.")
    if base_df.empty or attacked_df.empty:
        raise ValueError("DataFrames cannot be empty.")
    if not (0 <= attack_intensity <= 1):
        raise ValueError("Attack intensity must be between 0 and 1.")
    
    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(base_df['timestamp'], base_df['alert_frequency'], label='Baseline', marker='o')
    plt.plot(attacked_df['timestamp'], attacked_df['alert_frequency'], label='Attacked', marker='o')

    # Customize plot
    plt.title(f"Alert Frequency Trend\nAttack Type: {attack_type} | Intensity: {attack_intensity}", fontsize=font_size)
    plt.xlabel('Timestamp', fontsize=font_size)
    plt.ylabel('Alert Frequency', fontsize=font_size)
    plt.legend(fontsize=font_size)
    plt.grid(True)
    plt.xticks(rotation=45, fontsize=font_size - 2)
    plt.yticks(fontsize=font_size - 2)

    # Save plot
    plt.tight_layout()
    plt.savefig("alert_frequency_trend.png")
    plt.show()

import matplotlib.pyplot as plt

def plot_attack_severity_vs_latency(attack_events_df, font_size):
    """
    Generates a scatter plot to examine the correlation between attack severity and detection latency.
    
    Args:
    attack_events_df: DataFrame detailing when and how attacks occurred, including simulated detection latency and attack severity.
    font_size: The base font size for plot elements.
    
    Output:
    Displays the plot and saves it as a PNG file (e.g., "attack_severity_latency_plot.png").
    """

    if attack_events_df.empty:
        raise ValueError("DataFrame is empty")

    if (attack_events_df['simulated_detection_latency'] < 0).any():
        raise ValueError("Negative latency values not allowed")

    if font_size <= 0:
        raise ValueError("Font size must be positive")

    plt.figure(figsize=(10, 6))
    plt.scatter(attack_events_df['attack_severity'], attack_events_df['simulated_detection_latency'],
                c='blue', alpha=0.5)
    plt.title('Attack Severity vs Detection Latency', fontsize=font_size)
    plt.xlabel('Attack Severity', fontsize=font_size)
    plt.ylabel('Detection Latency', fontsize=font_size)
    plt.grid(True)

    plt.savefig("attack_severity_latency_plot.png")
    plt.show()

import matplotlib.pyplot as plt
import pandas as pd

def plot_agent_integrity_comparison(attacked_df, num_compromised_agents, font_size):
    """
    Generates a bar chart comparing agent integrity scores for compromised and uncompromised agents.
    
    Args:
    attacked_df (DataFrame): DataFrame with 'agent_id' and 'agent_integrity_score'.
    num_compromised_agents (int): Number of designated compromised agents.
    font_size (int): Base font size for plot elements.
    
    Displays the plot and saves it as a PNG file.
    """
    if not isinstance(attacked_df, pd.DataFrame):
        raise TypeError("attacked_df must be a pandas DataFrame.")

    if not isinstance(num_compromised_agents, int):
        raise TypeError("num_compromised_agents must be an integer.")

    if not isinstance(font_size, int):
        raise TypeError("font_size must be an integer.")
    
    if 'agent_id' not in attacked_df or 'agent_integrity_score' not in attacked_df:
        raise KeyError("DataFrame must contain 'agent_id' and 'agent_integrity_score' columns.")
    
    total_agents = len(attacked_df)
    
    if num_compromised_agents > total_agents:
        raise ValueError("Number of compromised agents exceeds total available agents.")

    compromised_scores = attacked_df['agent_integrity_score'].iloc[:num_compromised_agents]
    uncompromised_scores = attacked_df['agent_integrity_score'].iloc[num_compromised_agents:]

    labels = ['Compromised', 'Uncompromised']
    scores = [compromised_scores.mean() if not compromised_scores.empty else 0, 
              uncompromised_scores.mean() if not uncompromised_scores.empty else 0]

    plt.figure(figsize=(8, 6))
    plt.bar(labels, scores, color=['red', 'green'])
    plt.xlabel('Agent Status', fontsize=font_size)
    plt.ylabel('Average Integrity Score', fontsize=font_size)
    plt.title('Agent Integrity Comparison', fontsize=font_size)
    plt.ylim(0, 1)
    
    for index, value in enumerate(scores):
        plt.text(index, value + 0.01, f"{value:.2f}", ha='center', fontsize=font_size)
    
    plt.tight_layout()
    plt.savefig("agent_integrity_comparison.png")
    plt.show()

import ipywidgets as widgets
from IPython.display import display

def define_interactive_parameters():
    """Creates interactive widgets for simulation parameters and sets default values."""
    
    # Interactive widgets
    attack_intensity = widgets.IntSlider(
        value=50,
        min=0,
        max=100,
        step=1,
        description='Attack Intensity:',
        continuous_update=False
    )
    attack_type = widgets.Dropdown(
        options=['DoS', 'Phishing', 'Malware'],
        value='DoS',
        description='Attack Type:'
    )
    num_comp_agents = widgets.IntSlider(
        value=10,
        min=1,
        max=500,
        step=1,
        description='Compromised Agents:',
        continuous_update=False
    )

    # Non-interactive global parameters
    global sim_duration, num_agents, base_alert_rate, anomaly_rate_multiplier, random_seed
    sim_duration = 60
    num_agents = 1000
    base_alert_rate = 0.1
    anomaly_rate_multiplier = 2.0
    random_seed = 42

    # Display widgets
    display(attack_intensity, attack_type, num_comp_agents)