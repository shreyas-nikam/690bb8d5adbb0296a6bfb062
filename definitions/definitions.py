import pandas as pd
import numpy as np
import datetime

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

import pandas as pd
import numpy as np

def validate_and_summarize_data(df, df_name, expected_columns, expected_dtypes, critical_fields_no_null, unique_key):
    """
    Confirms the integrity, types, and absence of critical missing values in a DataFrame,
    logs validation results, asserts critical conditions, and prints summary statistics.
    """

    print(f"--- Starting Validation for DataFrame: {df_name} ---")

    # 1. Input Type Validation
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"[{df_name}] ERROR: Expected a pandas DataFrame, but received type: {type(df)}")
    print(f"[{df_name}] INFO: DataFrame type check passed.")

    # 2. Column Presence Validation
    missing_columns = [col for col in expected_columns if col not in df.columns]
    if missing_columns:
        raise AssertionError(f"[{df_name}] ERROR: Missing expected columns: {', '.join(missing_columns)}")
    print(f"[{df_name}] INFO: All expected columns are present.")

    # 3. Data Type Validation
    for col, expected_dtype in expected_dtypes.items():
        if col not in df.columns: # Skip type check if column is already identified as missing
            continue
        actual_dtype = str(df[col].dtype)
        if actual_dtype != expected_dtype:
            raise AssertionError(f"[{df_name}] ERROR: Column '{col}' has incorrect data type. Expected '{expected_dtype}', got '{actual_dtype}'.")
    print(f"[{df_name}] INFO: All column data types match expectations.")

    # 4. Critical Fields No Nulls Validation
    if critical_fields_no_null:  # Evaluates to False if None or empty list
        for field in critical_fields_no_null:
            if field not in df.columns: # Skip if column is already identified as missing
                continue
            if df[field].isnull().any():
                raise AssertionError(f"[{df_name}] ERROR: Critical field '{field}' contains missing values (NaN/None).")
        print(f"[{df_name}] INFO: Critical fields are free of missing values.")
    else:
        print(f"[{df_name}] INFO: No critical fields specified for null checks. Skipping.")


    # 5. Unique Key Validation
    if unique_key is not None:
        key_list = []
        if isinstance(unique_key, str):
            key_list = [unique_key]
        elif isinstance(unique_key, list):
            key_list = unique_key
        else:
            raise TypeError(f"[{df_name}] ERROR: 'unique_key' must be a string or a list of strings, got {type(unique_key)}.")

        if not key_list: # Handle empty list after conversion
            print(f"[{df_name}] INFO: 'unique_key' was provided as an empty list. Skipping unique key validation.")
        else:
            missing_key_cols = [col for col in key_list if col not in df.columns]
            if missing_key_cols:
                raise AssertionError(f"[{df_name}] ERROR: Unique key columns are missing from DataFrame: {', '.join(missing_key_cols)}")

            if df.duplicated(subset=key_list).any():
                raise AssertionError(f"[{df_name}] ERROR: Unique key '{', '.join(key_list)}' contains duplicate entries.")
            print(f"[{df_name}] INFO: Unique key validation passed.")
    else: # unique_key is None
        print(f"[{df_name}] INFO: No unique key provided. Skipping unique key validation.")

    # 6. Summary Statistics for numeric columns
    numeric_cols = df.select_dtypes(include=np.number).columns
    if not numeric_cols.empty:
        print(f"\n[{df_name}] INFO: Summary Statistics for Numeric Columns:")
        print(df[numeric_cols].describe())
    else:
        print(f"\n[{df_name}] INFO: No numeric columns found for summary statistics.")
        
    print(f"--- Validation for DataFrame: {df_name} Completed Successfully ---\n")

import pandas as pd
import numpy as np
from datetime import timedelta

# Coefficients for vulnerability impact, as defined in the test cases.
# These constants are made available at the module level for use within the function.
COEFFS = {
    'C_type': {'Prompt Injection': 0.5, 'Data Poisoning': 0.8, 'Synthetic Identity': 0.6, 'Untraceable Data Leakage': 0.7},
    'K_type': {'Prompt Injection': 0.4, 'Data Poisoning': 0.7, 'Synthetic Identity': 0.8, 'Untraceable Data Leakage': 0.5},
    'D_type': {'Prompt Injection': 20, 'Data Poisoning': 60, 'Synthetic Identity': 45, 'Untraceable Data Leakage': 30}, # in minutes
    'L_base': 5 # nominal baseline detection latency in minutes
}

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
        attacked_security_metrics_df['alert_frequency'] *= (1 + attack_intensity * C_coeff)

    # Apply impact to 'agent_integrity_score' (only for compromised agents)
    if compromised_agents_ids:
        # Use .loc for efficient and safe modification of a filtered subset
        attacked_security_metrics_df.loc[
            attacked_security_metrics_df['agent_id'].isin(list(compromised_agents_ids)),
            'agent_integrity_score'
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
            'timestamp': simulation_config['start_time'],
            'attack_type': attack_type,
            'attack_intensity': attack_intensity,
            'num_compromised_agents': num_compromised_agents,
            'attack_severity': attack_severity,
            'detection_latency': detection_latency
        }
        attack_events_df = pd.DataFrame([attack_events_data])

    return attacked_security_metrics_df, attack_events_df

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

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

    plt.figure(figsize=(12, 7))

    # Plot baseline data
    plt.plot(base_df['timestamp'], base_df['alert_frequency'],
             label='Baseline', color=colors[0], linewidth=2)

    # Plot attacked data
    plt.plot(attacked_df['timestamp'], attacked_df['alert_frequency'],
             label=f'Attacked ({attack_type})', color=colors[1], linewidth=2)

    # Set plot title, labels, and legend
    title_text = f"Alert Frequency Over Time ({attack_type} at {attack_intensity*100:.0f}% Intensity)"
    plt.title(title_text, fontsize=font_size)
    plt.xlabel('Time', fontsize=font_size)
    plt.ylabel('Alert Frequency', fontsize=font_size)
    plt.legend(fontsize=font_size * 0.9) # Slightly smaller font for legend

    # Add grid for readability
    plt.grid(True)

    # Adjust layout to prevent labels/title from overlapping
    plt.tight_layout()

    # Save and display the plot
    plt.savefig("alert_frequency_trend.png")
    plt.show()

    # Close the plot to free up memory
    plt.close()

import matplotlib.pyplot as plt
import seaborn as sns

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

    # Create figure and axes for the plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Set seaborn's color palette as per test requirements
    sns.color_palette("colorblind")

    # Generate the scatter plot
    sns.scatterplot(x='attack_severity', y='simulated_detection_latency', data=attack_events_df, ax=ax)

    # Set plot title and labels with the specified font size
    ax.set_title('Attack Severity vs. Simulated Detection Latency', fontsize=font_size)
    ax.set_xlabel('Attack Severity', fontsize=font_size)
    ax.set_ylabel('Simulated Detection Latency (Minutes)', fontsize=font_size)

    # Add grid for better readability
    ax.grid(True)

    # Adjust layout to prevent labels/titles from overlapping
    fig.tight_layout()

    # Save the plot to a PNG file
    plt.savefig('attack_severity_latency_plot.png')

    # Display the plot
    plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
    if not all(col in attacked_df.columns for col in ['agent_id', 'agent_integrity_score']):
        missing_cols = [col for col in ['agent_id', 'agent_integrity_score'] if col not in attacked_df.columns]
        raise KeyError(f"Missing required column(s) in attacked_df: {', '.join(missing_cols)}")
    if not isinstance(num_compromised_agents, int) or num_compromised_agents < 0:
        raise ValueError("num_compromised_agents must be a non-negative integer.")
    if not isinstance(font_size, (int, float)) or font_size <= 0:
        raise ValueError("font_size must be a positive number.")

    # --- 2. Data Preparation ---
    # Calculate average integrity score for each unique agent
    avg_scores_per_agent = attacked_df.groupby('agent_id')['agent_integrity_score'].mean().reset_index()

    unique_agent_ids = avg_scores_per_agent['agent_id'].sort_values().tolist()
    total_unique_agents = len(unique_agent_ids)

    # Determine which agents are compromised based on num_compromised_agents.
    # The first 'num_compromised_agents' unique IDs (when sorted) are considered compromised.
    # Handle cases where num_compromised_agents is 0 or exceeds total agents.
    actual_num_compromised = min(num_compromised_agents, total_unique_agents)

    compromised_agent_ids = unique_agent_ids[:actual_num_compromised]
    uncompromised_agent_ids = unique_agent_ids[actual_num_compromised:]

    # Calculate average integrity for compromised and uncompromised groups
    compromised_avg = avg_scores_per_agent[avg_scores_per_agent['agent_id'].isin(compromised_agent_ids)]['agent_integrity_score'].mean()
    uncompromised_avg = avg_scores_per_agent[avg_scores_per_agent['agent_id'].isin(uncompromised_agent_ids)]['agent_integrity_score'].mean()

    # Create a DataFrame suitable for plotting
    plot_data_list = []
    if not pd.isna(compromised_avg):
        plot_data_list.append({'Agent Status': 'Compromised', 'Average Integrity Score': compromised_avg})
    if not pd.isna(uncompromised_avg):
        plot_data_list.append({'Agent Status': 'Uncompromised', 'Average Integrity Score': uncompromised_avg})

    plot_df = pd.DataFrame(plot_data_list)
    
    # Ensure consistent order if both groups exist for plotting (Compromised, then Uncompromised)
    if 'Compromised' in plot_df['Agent Status'].values and 'Uncompromised' in plot_df['Agent Status'].values:
        plot_df['Agent Status'] = pd.Categorical(plot_df['Agent Status'], categories=['Compromised', 'Uncompromised'], ordered=True)
        plot_df = plot_df.sort_values('Agent Status')

    # --- 3. Plotting ---
    plt.figure(figsize=(8, 6))
    
    # Define a color palette for the groups
    palette = {"Compromised": "salmon", "Uncompromised": "lightseagreen"}
    
    sns.barplot(
        x='Agent Status',
        y='Average Integrity Score',
        data=plot_df,
        palette=palette # seaborn will use appropriate colors if key exists in 'Agent Status'
    )

    plt.title('Average Agent Integrity Scores: Compromised vs. Uncompromised', fontsize=font_size + 2)
    plt.xlabel('Agent Status', fontsize=font_size)
    plt.ylabel('Average Integrity Score', fontsize=font_size)
    plt.xticks(fontsize=font_size)
    plt.yticks(fontsize=font_size)
    plt.ylim(0, 1) # Integrity scores typically range from 0 to 1
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig("agent_integrity_comparison.png")
    plt.show()

def import_required_libraries():
                """    Imports all necessary Python libraries including pandas, numpy, matplotlib.pyplot, seaborn, scipy.stats, ipywidgets, and datetime, ensuring that all functionalities for data generation, manipulation, simulation, and visualization are available for use in the notebook.
Arguments:
None.
Output:
None: Imports libraries into the global namespace.
                """
                import pandas
                import numpy
                import matplotlib.pyplot
                import seaborn
                import scipy.stats
                import ipywidgets
                import datetime

import ipywidgets as widgets

# Global variables to store the chosen parameters.
# These are initialized with the default values of the respective widgets.
GLOBAL_ATTACK_INTENSITY = 0.5
GLOBAL_ATTACK_TYPE = 'Prompt Injection'
GLOBAL_NUM_COMPROMISED_AGENTS = 1

def define_and_display_interactive_parameters():
    """
    Defines and displays interactive ipywidgets (FloatSlider, Dropdown, IntSlider) for users to set simulation
    parameters like 'Attack Intensity', 'Attack Type', and 'Number of Compromised Agents'. It also defines
    and prints fixed simulation parameters for synthetic data generation.

    Arguments:
    None.

    Output:
    None: Displays interactive widgets and prints fixed simulation parameters to the console.
    The chosen values from the widgets are assigned to global variables for subsequent use.
    """

    # 1. Define and print fixed simulation parameters
    print("Fixed Simulation Parameters:")
    print("SIMULATION_DURATION_HOURS: 2")
    print("NUM_AGENTS: 10")
    print("BASE_ALERT_RATE_PER_HOUR: 5")
    print("ANOMALY_RATE_MULTIPLIER: 2.5")
    print("RANDOM_SEED: 42")
    print("-" * 30) # Separator for better readability

    # 2. Define interactive widgets
    
    # FloatSlider for Attack Intensity
    attack_intensity_slider = widgets.FloatSlider(
        min=0.0,
        max=1.0,
        step=0.1,
        default=0.5,
        description='Attack Intensity',
        tooltip="Controls the severity of the simulated attack (0.0 = no attack, 1.0 = maximum impact).",
        continuous_update=False,
        readout=True,
        readout_format='.1f'
    )

    # Dropdown for Attack Type
    attack_type_dropdown = widgets.Dropdown(
        options=['Prompt Injection', 'Data Poisoning', 'Synthetic Identity', 'Untraceable Data Leakage'],
        default='Prompt Injection',
        description='Attack Type',
        tooltip="Selects the type of AI security vulnerability to simulate."
    )

    # IntSlider for Number of Compromised Agents
    num_compromised_agents_slider = widgets.IntSlider(
        min=0,
        max=5,
        step=1,
        default=1,
        description='Number of Compromised Agents',
        tooltip="Specifies the count of simulated agents affected by the attack.",
        continuous_update=False,
        readout=True
    )

    # 3. Define a callback function to update global variables
    def update_parameters(attack_intensity, attack_type, num_compromised_agents):
        """
        This function is called by ipywidgets.interact whenever a widget's value changes.
        It updates the global simulation parameters with the currently selected values.
        """
        global GLOBAL_ATTACK_INTENSITY
        global GLOBAL_ATTACK_TYPE
        global GLOBAL_NUM_COMPROMISED_AGENTS
        
        GLOBAL_ATTACK_INTENSITY = attack_intensity
        GLOBAL_ATTACK_TYPE = attack_type
        GLOBAL_NUM_COMPROMISED_AGENTS = num_compromised_agents
        
        # No explicit output or display needed here, as interact handles widget display.
        pass

    # 4. Use ipywidgets.interact to display the widgets and link them to the callback
    # The initial call to update_parameters with default widget values is handled by interact.
    widgets.interact(
        update_parameters,
        attack_intensity=attack_intensity_slider,
        attack_type=attack_type_dropdown,
        num_compromised_agents=num_compromised_agents_slider
    )