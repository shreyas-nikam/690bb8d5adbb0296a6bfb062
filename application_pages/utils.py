
import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime, timedelta
import warnings
import plotly.express as px
import plotly.graph_objects as go

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

def plot_alert_frequency_trend_plotly(base_df, attacked_df, attack_type, attack_intensity):
    base_df_agg = base_df.groupby('timestamp')['alert_frequency'].mean().reset_index()
    attacked_df_agg = attacked_df.groupby('timestamp')['alert_frequency'].mean().reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=base_df_agg['timestamp'], y=base_df_agg['alert_frequency'],
                             mode='lines+markers', name='Baseline', marker=dict(symbol='circle')))
    fig.add_trace(go.Scatter(x=attacked_df_agg['timestamp'], y=attacked_df_agg['alert_frequency'],
                             mode='lines+markers', name='Attacked', marker=dict(symbol='x')))

    fig.update_layout(
        title=f"Alert Frequency Over Time: Baseline vs. Attacked<br>({attack_type} at {attack_intensity*100:.0f}% Intensity)",
        xaxis_title='Time',
        yaxis_title='Average Alert Frequency',
        hovermode='x unified',
        legend_title_text='Scenario',
        height=500,
        width=800
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_attack_severity_vs_latency_plotly(attack_events_df):
    if attack_events_df.empty:
        st.warning("No attack events to plot for Attack Severity vs. Detection Latency.")
        return

    fig = px.scatter(attack_events_df, x='attack_severity', y='simulated_detection_latency',
                     color='attack_type',
                     title='Attack Severity vs. Simulated Detection Latency',
                     labels={'attack_severity': 'Attack Severity',
                             'simulated_detection_latency': 'Simulated Detection Latency (Minutes)'},
                     hover_data=['attack_intensity', 'num_compromised_agents'],
                     height=500,
                     width=800)
    
    fig.update_layout(legend_title_text='Attack Type')
    st.plotly_chart(fig, use_container_width=True)

def plot_agent_integrity_comparison_plotly(attacked_df):
    if attacked_df.empty:
        st.warning("Attacked metrics DataFrame is empty, cannot plot agent integrity comparison.")
        return

    if 'is_compromised' not in attacked_df.columns:
        st.error("The 'is_compromised' column is missing in the attacked DataFrame. Cannot plot integrity comparison.")
        return
    
    integrity_comparison = attacked_df.groupby('is_compromised')['agent_integrity_score'].mean().reset_index()
    integrity_comparison['Agent Status'] = integrity_comparison['is_compromised'].map({True: 'Compromised', False: 'Uncompromised'})

    fig = px.bar(integrity_comparison, x='Agent Status', y='agent_integrity_score',
                 title='Average Agent Integrity Scores: Compromised vs. Uncompromised',
                 labels={'agent_integrity_score': 'Average Integrity Score'},
                 color='Agent Status',
                 height=500,
                 width=800)
    
    fig.update_traces(texttemplate='%{y:.2f}', textposition='outside')
    fig.update_layout(yaxis_range=[0, 1.1]) # Extend y-axis to show labels
    st.plotly_chart(fig, use_container_width=True)
