import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


SIMULATION_DURATION_HOURS = 2
NUM_AGENTS = 10
BASE_ALERT_RATE_PER_HOUR = 5
ANOMALY_RATE_MULTIPLIER = 2.5
RANDOM_SEED = 42

COEFFS = {
    'C_type': {
        'Prompt Injection': 0.5,
        'Data Poisoning': 0.8,
        'Synthetic Identity': 0.6,
        'Untraceable Data Leakage': 0.7,
    },
    'K_type': {
        'Prompt Injection': 0.4,
        'Data Poisoning': 0.7,
        'Synthetic Identity': 0.8,
        'Untraceable Data Leakage': 0.5,
    },
    'D_type': {
        'Prompt Injection': 20,
        'Data Poisoning': 60,
        'Synthetic Identity': 45,
        'Untraceable Data Leakage': 30,
    },
    'L_base': 5,
}


def _init_session_state() -> None:
    if 'selected_attack_intensity' not in st.session_state:
        st.session_state.selected_attack_intensity = 0.5
    if 'selected_attack_type' not in st.session_state:
        st.session_state.selected_attack_type = 'Prompt Injection'
    if 'selected_num_compromised_agents' not in st.session_state:
        st.session_state.selected_num_compromised_agents = 1


@st.cache_data(ttl="2h")
def generate_synthetic_safety_data(num_agents: int,
                                   simulation_duration_hours: int,
                                   base_alert_rate: float,
                                   anomaly_rate_multiplier: float,
                                   random_seed: int):
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

    rng = np.random.default_rng(random_seed)

    simulation_config = {
        'num_agents': num_agents,
        'simulation_duration_hours': simulation_duration_hours,
        'base_alert_rate': base_alert_rate,
        'anomaly_rate_multiplier': anomaly_rate_multiplier,
        'random_seed': random_seed,
    }

    if num_agents == 0 or simulation_duration_hours == 0:
        empty_sensor_df = pd.DataFrame(
            columns=['timestamp', 'agent_id', 'sensor_type', 'value', 'unit', 'status']
        )
        empty_agent_logs_df = pd.DataFrame(
            columns=['timestamp', 'agent_id', 'log_type', 'severity', 'message']
        )
        empty_metrics_df = pd.DataFrame(
            columns=[
                'agent_id',
                'total_alerts_generated',
                'average_integrity_score',
                'last_alert_time',
            ]
        )
        return empty_sensor_df, empty_agent_logs_df, empty_metrics_df, simulation_config

    start_time = pd.Timestamp('2023-01-01 00:00:00')
    end_time = start_time + pd.Timedelta(hours=simulation_duration_hours)

    freq = '10min'
    if simulation_duration_hours < 1:
        freq = '1min'

    simulation_timestamps = pd.date_range(start=start_time, end=end_time, freq=freq)

    if len(simulation_timestamps) == 0:
        simulation_timestamps = pd.Series([start_time])

    num_timesteps = len(simulation_timestamps)

    sensor_data_records = []
    sensor_types = ['temperature', 'pressure', 'vibration']
    sensor_units = {'temperature': '°C', 'pressure': 'kPa', 'vibration': 'mm/s'}
    base_values = {'temperature': 25.0, 'pressure': 100.0, 'vibration': 5.0}
    noise_stds = {'temperature': 2.0, 'pressure': 5.0, 'vibration': 1.0}

    readings_per_hour_per_sensor = 60 / int(freq.replace('min', ''))
    total_sensor_readings_per_hour = num_agents * len(sensor_types) * readings_per_hour_per_sensor
    p_sensor_anomaly_per_reading = (base_alert_rate * anomaly_rate_multiplier) / total_sensor_readings_per_hour

    for agent_id in range(1, num_agents + 1):
        for ts in simulation_timestamps:
            for sensor_type in sensor_types:
                base_val = base_values[sensor_type]
                std = noise_stds[sensor_type]

                value = rng.normal(base_val, std)
                status = 'normal'

                if rng.random() < p_sensor_anomaly_per_reading:
                    anomaly_magnitude = rng.uniform(2, 5) * std
                    value += rng.choice([-1, 1]) * anomaly_magnitude
                    status = rng.choice(['warning', 'critical'], p=[0.7, 0.3])

                sensor_data_records.append(
                    {
                        'timestamp': ts,
                        'agent_id': agent_id,
                        'sensor_type': sensor_type,
                        'value': round(float(value), 2),
                        'unit': sensor_units[sensor_type],
                        'status': status,
                    }
                )

    sensor_data_df = pd.DataFrame(sensor_data_records)

    agent_log_records = []
    log_types = ['heartbeat', 'data_transfer', 'status_update', 'configuration_change']
    severities = {
        'heartbeat': 'INFO',
        'data_transfer': 'INFO',
        'status_update': 'INFO',
        'configuration_change': 'INFO',
        'alert_generated': 'WARNING',
    }
    messages = {
        'heartbeat': 'Agent operational check.',
        'data_transfer': 'Transferred sensor data to central server.',
        'status_update': 'Reporting system status as normal.',
        'configuration_change': 'Configuration updated successfully.',
    }

    expected_normal_logs_per_agent_per_hour = 2
    total_normal_logs = int(expected_normal_logs_per_agent_per_hour * num_agents * simulation_duration_hours)
    total_alert_logs = int(base_alert_rate * simulation_duration_hours * anomaly_rate_multiplier)

    min_logs_per_agent = 1
    total_normal_logs = max(total_normal_logs, min_logs_per_agent * num_agents)
    total_alert_logs = max(total_alert_logs, 1) if base_alert_rate > 0 and simulation_duration_hours > 0 else 0

    if total_normal_logs > 0:
        for _ in range(total_normal_logs):
            ts = rng.choice(simulation_timestamps)
            agent_id = int(rng.choice(range(1, num_agents + 1)))
            log_type = str(rng.choice(log_types))
            agent_log_records.append(
                {
                    'timestamp': ts,
                    'agent_id': agent_id,
                    'log_type': log_type,
                    'severity': severities[log_type],
                    'message': messages[log_type],
                }
            )

    if total_alert_logs > 0:
        for _ in range(total_alert_logs):
            ts = rng.choice(simulation_timestamps)
            agent_id = int(rng.choice(range(1, num_agents + 1)))
            severity = str(rng.choice(['WARNING', 'ERROR'], p=[0.7, 0.3]))
            if severity == 'ERROR':
                message = 'CRITICAL ALERT: Abnormal condition detected in monitored area.'
            else:
                message = 'ALERT: Potential anomaly detected.'

            agent_log_records.append(
                {
                    'timestamp': ts,
                    'agent_id': agent_id,
                    'log_type': 'alert_generated',
                    'severity': severity,
                    'message': message,
                }
            )

    agent_logs_df = (
        pd.DataFrame(agent_log_records)
        .sort_values(by='timestamp')
        .reset_index(drop=True)
    )

    metrics_records = []

    for agent_id in range(1, num_agents + 1):
        agent_alerts = agent_logs_df[
            (agent_logs_df['agent_id'] == agent_id)
            & (agent_logs_df['log_type'] == 'alert_generated')
        ]
        total_alerts_generated = int(len(agent_alerts))
        last_alert_time = agent_alerts['timestamp'].max() if not agent_alerts.empty else pd.NaT

        base_integrity = 95.0
        deviation_factor = total_alerts_generated / (simulation_duration_hours * num_agents + 1e-6)
        integrity_deviation = deviation_factor * 10.0

        integrity_score = max(
            0.0,
            min(100.0, base_integrity - integrity_deviation + float(rng.normal(0, 2))),
        )

        metrics_records.append(
            {
                'agent_id': int(agent_id),
                'total_alerts_generated': int(total_alerts_generated),
                'average_integrity_score': round(float(integrity_score), 2),
                'last_alert_time': last_alert_time,
            }
        )

    base_security_metrics_df = pd.DataFrame(metrics_records)

    return sensor_data_df, agent_logs_df, base_security_metrics_df, simulation_config


def validate_and_summarize_data(df: pd.DataFrame,
                                df_name: str,
                                expected_columns,
                                expected_dtypes,
                                critical_fields_no_null,
                                unique_key):
    st.write(f"--- Starting Validation for DataFrame: {df_name} ---")

    if not isinstance(df, pd.DataFrame):
        st.error(f"[{df_name}] ERROR: Expected a pandas DataFrame, but received type: {type(df)}")
        raise TypeError(
            f"[{df_name}] ERROR: Expected a pandas DataFrame, but received type: {type(df)}"
        )

    st.info(f"[{df_name}] INFO: DataFrame type check passed.")

    missing_columns = [col for col in expected_columns if col not in df.columns]
    if missing_columns:
        missing_str = ", ".join(missing_columns)
        st.error(f"[{df_name}] ERROR: Missing expected columns: {missing_str}")
        raise AssertionError(
            f"[{df_name}] ERROR: Missing expected columns: {missing_str}"
        )

    st.info(f"[{df_name}] INFO: All expected columns are present.")

    for col, expected_dtype in expected_dtypes.items():
        if col not in df.columns:
            continue
        actual_dtype = str(df[col].dtype)
        if actual_dtype != expected_dtype:
            st.error(
                f"[{df_name}] ERROR: Column '{col}' has incorrect data type. "
                f"Expected '{expected_dtype}', got '{actual_dtype}'."
            )
            raise AssertionError(
                f"[{df_name}] ERROR: Column '{col}' has incorrect data type. "
                f"Expected '{expected_dtype}', got '{actual_dtype}'."
            )

    st.info(f"[{df_name}] INFO: All column data types match expectations.")

    if critical_fields_no_null:
        for field in critical_fields_no_null:
            if field not in df.columns:
                continue
            if df[field].isnull().any():
                st.error(
                    f"[{df_name}] ERROR: Critical field '{field}' contains missing values (NaN/None)."
                )
                raise AssertionError(
                    f"[{df_name}] ERROR: Critical field '{field}' contains missing values (NaN/None)."
                )
        st.info(f"[{df_name}] INFO: Critical fields are free of missing values.")
    else:
        st.info(f"[{df_name}] INFO: No critical fields specified for null checks. Skipping.")

    if unique_key is not None:
        if isinstance(unique_key, str):
            key_list = [unique_key]
        elif isinstance(unique_key, list):
            key_list = unique_key
        else:
            st.error(
                f"[{df_name}] ERROR: 'unique_key' must be a string or a list of strings, got {type(unique_key)}."
            )
            raise TypeError(
                f"[{df_name}] ERROR: 'unique_key' must be a string or a list of strings, got {type(unique_key)}."
            )

        if not key_list:
            st.info(
                f"[{df_name}] INFO: 'unique_key' was provided as an empty list. Skipping unique key validation."
            )
        else:
            missing_key_cols = [col for col in key_list if col not in df.columns]
            if missing_key_cols:
                missing_str = ", ".join(missing_key_cols)
                st.error(
                    f"[{df_name}] ERROR: Unique key columns are missing from DataFrame: {missing_str}"
                )
                raise AssertionError(
                    f"[{df_name}] ERROR: Unique key columns are missing from DataFrame: {missing_str}"
                )

            if df.duplicated(subset=key_list).any():
                joined_keys = ", ".join(key_list)
                st.error(
                    f"[{df_name}] ERROR: Unique key '{joined_keys}' contains duplicate entries."
                )
                raise AssertionError(
                    f"[{df_name}] ERROR: Unique key '{joined_keys}' contains duplicate entries."
                )
            st.info(f"[{df_name}] INFO: Unique key validation passed.")
    else:
        st.info(f"[{df_name}] INFO: No unique key provided. Skipping unique key validation.")

    numeric_cols = df.select_dtypes(include=np.number).columns
    if not numeric_cols.empty:
        st.write(f"[{df_name}] INFO: Summary Statistics for Numeric Columns:")
        st.dataframe(df[numeric_cols].describe())
    else:
        st.info(f"[{df_name}] INFO: No numeric columns found for summary statistics.")

    st.write(f"--- Validation for DataFrame: {df_name} Completed Successfully ---")


def simulate_vulnerability_impact(base_metrics_df: pd.DataFrame,
                                  attack_type: str,
                                  attack_intensity: float,
                                  num_compromised_agents: int,
                                  simulation_config):
    if attack_type not in COEFFS['C_type']:
        raise ValueError(
            f"Unknown attack_type: '{attack_type}'. Must be one of {list(COEFFS['C_type'].keys())}"
        )

    if not (0 <= attack_intensity <= 1):
        raise ValueError(
            f"attack_intensity ({attack_intensity}) must be between 0 and 1."
        )

    attacked_security_metrics_df = base_metrics_df.copy()

    all_agent_ids = attacked_security_metrics_df['agent_id'].unique()
    total_agents = len(all_agent_ids)

    if num_compromised_agents < 0 or num_compromised_agents > total_agents:
        raise ValueError(
            f"num_compromised_agents ({num_compromised_agents}) must be between 0 and the total number of agents ({total_agents})."
        )

    rng = np.random.RandomState(simulation_config.get('random_seed'))

    compromised_agents_ids = set()
    if num_compromised_agents > 0:
        compromised_agents_ids = set(
            rng.choice(all_agent_ids, size=num_compromised_agents, replace=False)
        )

    c_coeff = COEFFS['C_type'][attack_type]
    k_coeff = COEFFS['K_type'][attack_type]
    d_coeff = COEFFS['D_type'][attack_type]
    l_base = COEFFS['L_base']

    if attack_intensity > 0:
        if 'alert_frequency' not in attacked_security_metrics_df.columns:
            sim_dur = simulation_config.get('simulation_duration_hours', 1) or 1
            attacked_security_metrics_df['alert_frequency'] = (
                attacked_security_metrics_df['total_alerts_generated'] / sim_dur
            )
        attacked_security_metrics_df['alert_frequency'] *= (1 + attack_intensity * c_coeff)

    if compromised_agents_ids:
        mask = attacked_security_metrics_df['agent_id'].isin(list(compromised_agents_ids))
        attacked_security_metrics_df.loc[mask, 'average_integrity_score'] *= (
            1 - attack_intensity * k_coeff
        )

    attack_events_df = pd.DataFrame(
        columns=[
            'timestamp',
            'attack_type',
            'attack_intensity',
            'num_compromised_agents',
            'attack_severity',
            'detection_latency',
        ]
    )

    if attack_intensity > 0 or num_compromised_agents > 0:
        detection_latency = float(l_base + attack_intensity * d_coeff)
        attack_severity = float(attack_intensity * num_compromised_agents)

        attack_events_data = {
            'timestamp': pd.Timestamp('2023-01-01 00:00:00'),
            'attack_type': attack_type,
            'attack_intensity': float(attack_intensity),
            'num_compromised_agents': int(num_compromised_agents),
            'attack_severity': attack_severity,
            'detection_latency': detection_latency,
        }
        attack_events_df = pd.DataFrame([attack_events_data])

    if 'alert_frequency' not in attacked_security_metrics_df.columns:
        sim_dur = simulation_config.get('simulation_duration_hours', 1) or 1
        if sim_dur > 0:
            attacked_security_metrics_df['alert_frequency'] = (
                attacked_security_metrics_df['total_alerts_generated'] / sim_dur
            )
        else:
            attacked_security_metrics_df['alert_frequency'] = 0.0

    return attacked_security_metrics_df, attack_events_df


def plot_alert_frequency_trend(base_df: pd.DataFrame,
                               attacked_df: pd.DataFrame,
                               attack_type: str,
                               attack_intensity: float,
                               font_size: int = 14):
    _ = base_df['timestamp']
    _ = base_df['alert_frequency']
    _ = attacked_df['timestamp']
    _ = attacked_df['alert_frequency']

    sns.set_style('whitegrid')
    colors = sns.color_palette('deep', 2)

    fig, ax = plt.subplots(figsize=(12, 7))

    ax.plot(
        base_df['timestamp'],
        base_df['alert_frequency'],
        label='Baseline',
        color=colors[0],
        linewidth=2,
    )

    ax.plot(
        attacked_df['timestamp'],
        attacked_df['alert_frequency'],
        label=f'Attacked ({attack_type})',
        color=colors[1],
        linewidth=2,
    )

    title_text = (
        f"Alert Frequency Over Time ({attack_type} at {attack_intensity * 100:.0f}% Intensity)"
    )
    ax.set_title(title_text, fontsize=font_size)
    ax.set_xlabel('Time', fontsize=font_size)
    ax.set_ylabel('Alert Frequency', fontsize=font_size)
    ax.legend(fontsize=int(font_size * 0.9))
    ax.grid(True)
    fig.tight_layout()
    return fig


def plot_attack_severity_vs_latency(attack_events_df: pd.DataFrame,
                                    font_size: int = 14):
    _ = attack_events_df['attack_severity']
    _ = attack_events_df['detection_latency']

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.set_palette('colorblind')

    sns.scatterplot(
        x='attack_severity',
        y='detection_latency',
        data=attack_events_df,
        ax=ax,
        s=100,
        hue='attack_type',
        style='attack_type',
    )

    ax.set_title('Attack Severity vs. Simulated Detection Latency', fontsize=font_size)
    ax.set_xlabel('Attack Severity', fontsize=font_size)
    ax.set_ylabel('Simulated Detection Latency (Minutes)', fontsize=font_size)
    ax.grid(True)

    if len(attack_events_df['attack_type'].unique()) > 1:
        ax.legend(title='Attack Type', fontsize=int(font_size * 0.9), title_fontsize=font_size)
    elif len(attack_events_df) > 1:
        ax.legend(title='Attack Event', fontsize=int(font_size * 0.9), title_fontsize=font_size)
    elif len(attack_events_df) == 1:
        ax.legend(title='Attack Type', fontsize=int(font_size * 0.9), title_fontsize=font_size)

    fig.tight_layout()
    return fig


def plot_agent_integrity_comparison(attacked_df: pd.DataFrame,
                                    num_compromised_agents: int,
                                    font_size: int = 14):
    if not isinstance(attacked_df, pd.DataFrame):
        raise TypeError('attacked_df must be a pandas DataFrame.')
    required_cols = ['agent_id', 'average_integrity_score']
    missing_cols = [col for col in required_cols if col not in attacked_df.columns]
    if missing_cols:
        missing_str = ", ".join(missing_cols)
        raise KeyError(f"Missing required column(s) in attacked_df: {missing_str}")
    if not isinstance(num_compromised_agents, int) or num_compromised_agents < 0:
        raise ValueError('num_compromised_agents must be a non-negative integer.')
    if not isinstance(font_size, (int, float)) or font_size <= 0:
        raise ValueError('font_size must be a positive number.')

    avg_scores_per_agent = (
        attacked_df.groupby('agent_id')['average_integrity_score']
        .mean()
        .reset_index()
    )

    unique_agent_ids = avg_scores_per_agent['agent_id'].sort_values().tolist()
    total_unique_agents = len(unique_agent_ids)

    actual_num_compromised = min(num_compromised_agents, total_unique_agents)

    compromised_agent_ids = unique_agent_ids[:actual_num_compromised]
    uncompromised_agent_ids = unique_agent_ids[actual_num_compromised:]

    compromised_avg = avg_scores_per_agent[
        avg_scores_per_agent['agent_id'].isin(compromised_agent_ids)
    ]['average_integrity_score'].mean()
    uncompromised_avg = avg_scores_per_agent[
        avg_scores_per_agent['agent_id'].isin(uncompromised_agent_ids)
    ]['average_integrity_score'].mean()

    plot_data_list = []
    if not pd.isna(compromised_avg):
        plot_data_list.append(
            {'Agent Status': 'Compromised', 'Average Integrity Score': float(compromised_avg)}
        )
    if not pd.isna(uncompromised_avg):
        plot_data_list.append(
            {
                'Agent Status': 'Uncompromised',
                'Average Integrity Score': float(uncompromised_avg),
            }
        )

    plot_df = pd.DataFrame(plot_data_list)

    if 'Agent Status' in plot_df.columns and not plot_df.empty:
        if 'Compromised' in plot_df['Agent Status'].values and 'Uncompromised' in plot_df['Agent Status'].values:
            plot_df['Agent Status'] = pd.Categorical(
                plot_df['Agent Status'],
                categories=['Compromised', 'Uncompromised'],
                ordered=True,
            )
            plot_df = plot_df.sort_values('Agent Status')

    fig, ax = plt.subplots(figsize=(8, 6))
    palette = {'Compromised': 'salmon', 'Uncompromised': 'lightseagreen'}

    sns.barplot(
        x='Agent Status',
        y='Average Integrity Score',
        data=plot_df,
        palette=palette,
        ax=ax,
    )

    ax.set_title(
        'Average Agent Integrity Scores: Compromised vs. Uncompromised',
        fontsize=font_size + 2,
    )
    ax.set_xlabel('Agent Status', fontsize=font_size)
    ax.set_ylabel('Average Integrity Score', fontsize=font_size)
    ax.tick_params(axis='x', labelsize=font_size)
    ax.tick_params(axis='y', labelsize=font_size)
    ax.set_ylim(0, 100)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    fig.tight_layout()
    return fig


def _sidebar_controls() -> None:
    st.sidebar.markdown("### 🎛️ Attack Configuration Panel")
    st.sidebar.markdown(
        "Use these controls to simulate different AI security vulnerabilities and immediately see their impact on the monitoring system."
    )

    st.session_state.selected_attack_intensity = st.sidebar.slider(
        label="Select Attack Intensity ($A_{intensity}$)",
        min_value=0.0,
        max_value=1.0,
        value=float(st.session_state.selected_attack_intensity),
        step=0.05,
        help=(
            "Controls the severity of the simulated attack, ranging from $0.0$ (no attack) "
            "to $1.0$ (maximum intensity)."
        ),
    )

    attack_type_options = list(COEFFS['C_type'].keys())
    default_index = attack_type_options.index(st.session_state.selected_attack_type)
    st.session_state.selected_attack_type = st.sidebar.selectbox(
        label="Select Attack Type",
        options=attack_type_options,
        index=int(default_index),
        help=(
            "Determines the specific type of AI security vulnerability being simulated. "
            "Examples include prompt injection and data poisoning."
        ),
    )

    st.session_state.selected_num_compromised_agents = st.sidebar.slider(
        label="Select Number of Compromised Agents ($N_{agents}$)",
        min_value=0,
        max_value=NUM_AGENTS,
        value=int(st.session_state.selected_num_compromised_agents),
        step=1,
        help=(
            f"Specifies how many of the simulated agents (out of {NUM_AGENTS}) are affected by the attack."
        ),
    )


@st.fragment
def _show_configuration_summary() -> None:
    st.markdown("### ⚙️ Current Simulation Configuration")
    st.write(f"**Selected Attack Intensity:** {st.session_state.selected_attack_intensity:.2f}")
    st.write(f"**Selected Attack Type:** {st.session_state.selected_attack_type}")
    st.write(
        f"**Selected Number of Compromised Agents:** {st.session_state.selected_num_compromised_agents}"
    )
    st.write(f"**Simulation Duration (Hours):** {SIMULATION_DURATION_HOURS}")
    st.write(f"**Number of Agents:** {NUM_AGENTS}")
    st.write(f"**Base Alert Rate (Per Hour):** {BASE_ALERT_RATE_PER_HOUR}")
    st.write(f"**Anomaly Rate Multiplier:** {ANOMALY_RATE_MULTIPLIER}")
    st.write(f"**Random Seed:** {RANDOM_SEED}")


def _render_math_foundations() -> None:
    st.markdown("## Section 4: Mathematical Foundations of Attack Simulation")
    st.markdown(
        r"""
To simulate the impact of AI security vulnerabilities concretely, we define mathematical relationships that govern how attacks influence key system metrics.
        """
    )
    st.markdown(
        r"""
#### Alert Frequency Over Time
The alert frequency under attack, $F_{alerts\_attacked}(t)$, is modeled as an increase over the baseline frequency, $F_{alerts\_base}(t)$:

$$F_{alerts\_attacked}(t) = F_{alerts\_base}(t) \cdot (1 + A_{intensity} \cdot C_{type})$$
        """
    )
    st.markdown(
        r"""
#### Detection Latency
The simulated detection latency, $L_{detection}$, represents the delay between an attack and its detection:

$$L_{detection} = L_{base} + A_{intensity} \cdot D_{type}$$
        """
    )
    st.markdown(
        r"""
#### Agent Integrity Score
The integrity score for a compromised agent, $I_{agent\_attacked}$, is reduced from its baseline, $I_{agent\_base}$:

$$I_{agent\_attacked} = I_{agent\_base} \cdot (1 - A_{intensity} \cdot K_{type})$$
        """
    )
    st.info(
        "These equations are used to perturb the baseline security metrics whenever you change the attack controls on the sidebar."
    )


def main() -> None:
    _init_session_state()

    _sidebar_controls()

    st.markdown(
        "# 🧪 AI Security Vulnerability Simulation Lab – Full Workspace",
    )

    st.markdown(
        """
This page is your full simulation cockpit. On the left, you configure the attack. On the right, you will see how the industrial safety monitoring system reacts across multiple views: data tables, validation feedback, and security-focused visualizations.
        """
    )

    _show_configuration_summary()

    st.markdown("## Section 2: Setup and Library Imports")
    st.markdown(
        "All core libraries (pandas, numpy, matplotlib, seaborn, and Streamlit) are already imported. They power data generation, numerical simulation, and visualization in this lab."
    )

    st.markdown("## Section 5: Synthetic Data Generation")
    st.markdown(
        "We generate a synthetic industrial environment with time-stamped sensor readings, agent communication logs, and baseline security metrics. This lets you study attacks without needing access to real factory data."
    )

    sensor_data_baseline, agent_logs_baseline, security_metrics_baseline, sim_config = generate_synthetic_safety_data(
        num_agents=NUM_AGENTS,
        simulation_duration_hours=SIMULATION_DURATION_HOURS,
        base_alert_rate=BASE_ALERT_RATE_PER_HOUR,
        anomaly_rate_multiplier=ANOMALY_RATE_MULTIPLIER,
        random_seed=RANDOM_SEED,
    )

    st.subheader("Synthetic Data (Baseline)")
    st.write("--- Sensor Data (Baseline) ---")
    st.dataframe(sensor_data_baseline.head())
    st.write("--- Agent Logs (Baseline) ---")
    st.dataframe(agent_logs_baseline.head())
    st.write("--- Security Metrics (Baseline) ---")
    st.dataframe(security_metrics_baseline.head())

    st.markdown(
        "The baseline tables show how the system behaves before any explicit security attack is introduced. Look for normal alert volumes and high integrity scores."
    )

    st.markdown("## Section 6: Data Validation and Initial Statistics")
    st.markdown(
        "Now we run a lightweight validation suite to confirm that the synthetic data is structurally sound before we simulate any attacks."
    )

    sensor_expected_columns = ['timestamp', 'agent_id', 'sensor_type', 'value', 'unit', 'status']
    sensor_expected_dtypes = {
        'timestamp': 'datetime64[ns]',
        'agent_id': 'int64',
        'sensor_type': 'object',
        'value': 'float64',
        'unit': 'object',
        'status': 'object',
    }

    agent_logs_expected_columns = [
        'timestamp',
        'agent_id',
        'log_type',
        'severity',
        'message',
    ]
    agent_logs_expected_dtypes = {
        'timestamp': 'datetime64[ns]',
        'agent_id': 'int64',
        'log_type': 'object',
        'severity': 'object',
        'message': 'object',
    }

    security_metrics_expected_columns = [
        'agent_id',
        'total_alerts_generated',
        'average_integrity_score',
        'last_alert_time',
    ]
    security_metrics_expected_dtypes = {
        'agent_id': 'int64',
        'total_alerts_generated': 'int64',
        'average_integrity_score': 'float64',
        'last_alert_time': 'datetime64[ns]',
    }

    try:
        validate_and_summarize_data(
            sensor_data_baseline,
            "Sensor Data",
            sensor_expected_columns,
            sensor_expected_dtypes,
            critical_fields_no_null=['timestamp', 'value'],
            unique_key=['timestamp', 'agent_id', 'sensor_type'],
        )
        validate_and_summarize_data(
            agent_logs_baseline,
            "Agent Logs",
            agent_logs_expected_columns,
            agent_logs_expected_dtypes,
            critical_fields_no_null=['timestamp', 'log_type'],
            unique_key=None,
        )
        validate_and_summarize_data(
            security_metrics_baseline,
            "Security Metrics",
            security_metrics_expected_columns,
            security_metrics_expected_dtypes,
            critical_fields_no_null=['agent_id', 'average_integrity_score'],
            unique_key=['agent_id'],
        )
        st.success("All baseline datasets passed validation checks.")
    except (TypeError, AssertionError) as e:
        st.error(f"Data validation failed: {e}")

    st.markdown(
        "If validation fails, read the error message and think about how corrupted or incomplete telemetry could itself be a symptom of an ongoing attack."
    )

    st.markdown("## Section 7: Vulnerability Simulation – Attack Logic")
    st.markdown(
        "Next, we apply your chosen attack configuration to the baseline security metrics. This simulates how many alerts fire, how agent integrity changes, and how long detection might take."
    )

    sim_config['start_time'] = pd.Timestamp('2023-01-01 00:00:00')

    security_metrics_attacked, attack_events = simulate_vulnerability_impact(
        base_metrics_df=security_metrics_baseline,
        attack_type=st.session_state.selected_attack_type,
        attack_intensity=float(st.session_state.selected_attack_intensity),
        num_compromised_agents=int(st.session_state.selected_num_compromised_agents),
        simulation_config=sim_config,
    )

    st.subheader("Simulated Attack Results")
    st.write("--- Attacked Security Metrics ---")
    st.dataframe(security_metrics_attacked.head())
    st.write("--- Attack Events ---")
    st.dataframe(attack_events.head())

    st.markdown(
        "Compare these attacked metrics to the baseline. Notice how integrity scores drop for compromised agents and how alert-related fields change as you increase intensity."
    )

    _render_math_foundations()

    st.markdown("## Section 8: Trend Plot – Alert Frequency Over Time")
    st.markdown(
        "This view helps you see how the attack inflates or distorts alert behavior over the simulation window."
    )

    start_time_plot = pd.Timestamp('2023-01-01 00:00:00')
    end_time_plot = start_time_plot + pd.Timedelta(hours=SIMULATION_DURATION_HOURS)
    freq_plot = '10min'
    if SIMULATION_DURATION_HOURS < 1:
        freq_plot = '1min'

    plot_timestamps = pd.date_range(start=start_time_plot, end=end_time_plot, freq=freq_plot)
    if len(plot_timestamps) == 0:
        plot_timestamps = pd.Series([start_time_plot])

    baseline_alert_frequencies = [
        BASE_ALERT_RATE_PER_HOUR + np.random.normal(0, 0.5)
        for _ in range(len(plot_timestamps))
    ]

    base_df_for_plot = pd.DataFrame(
        {
            'timestamp': plot_timestamps,
            'alert_frequency': baseline_alert_frequencies,
        }
    )

    c_coeff_plot = COEFFS['C_type'][st.session_state.selected_attack_type]
    attacked_alert_rates = [
        rate * (1 + float(st.session_state.selected_attack_intensity) * c_coeff_plot)
        + np.random.normal(0, 0.5)
        for rate in baseline_alert_frequencies
    ]
    attacked_df_for_plot = pd.DataFrame(
        {
            'timestamp': plot_timestamps,
            'alert_frequency': attacked_alert_rates,
        }
    )

    fig_trend = plot_alert_frequency_trend(
        base_df=base_df_for_plot,
        attacked_df=attacked_df_for_plot,
        attack_type=st.session_state.selected_attack_type,
        attack_intensity=float(st.session_state.selected_attack_intensity),
        font_size=14,
    )
    st.pyplot(fig_trend)
    plt.close(fig_trend)

    st.markdown(
        "Try increasing intensity or switching attack types to see how much noisier the alert stream becomes. Would your SOC treat this as noise or a warning sign?"
    )

    st.markdown("## Section 9: Relationship Plot – Attack Severity vs. Detection Latency")
    st.markdown(
        "Here you explore whether more severe attacks tend to be detected later. This is a key question for designing SLAs and incident response playbooks."
    )

    if not attack_events.empty:
        fig_rel = plot_attack_severity_vs_latency(
            attack_events_df=attack_events,
            font_size=14,
        )
        st.pyplot(fig_rel)
        plt.close(fig_rel)
    else:
        st.info("No attack events to plot for Attack Severity vs. Detection Latency.")

    st.markdown(
        "If you see long detection latencies for even moderate severities, consider which monitoring rules or anomaly detectors you would strengthen."
    )

    st.markdown("## Section 10: Aggregated Comparison – Agent Integrity Scores")
    st.markdown(
        "This bar chart aggregates agent integrity so you can quickly compare the health of compromised vs. uncompromised agents."
    )

    if not security_metrics_attacked.empty:
        fig_comp = plot_agent_integrity_comparison(
            attacked_df=security_metrics_attacked,
            num_compromised_agents=int(st.session_state.selected_num_compromised_agents),
            font_size=14,
        )
        st.pyplot(fig_comp)
        plt.close(fig_comp)
    else:
        st.info("No security metrics data available to compare agent integrity scores.")

    st.markdown(
        "Look for large gaps between compromised and uncompromised integrity. How might you automatically quarantine low-integrity agents in a real deployment?"
    )

    st.markdown("## Section 11: Discussion and Reflection Prompts")
    st.markdown(
        """
Use the current configuration and charts to answer:

- Under which attack types does alert frequency spike the most?
- When you increase $N_{agents}$ while keeping intensity fixed, how does that change severity and latency?
- Which combination of $A_{intensity}$ and attack type would you prioritize for red-teaming in a real system?
        """
    )

    st.markdown("## Section 12: Key Takeaways")
    st.markdown(
        """
- AI security vulnerabilities can be explored through synthetic simulations before deployment.
- Simple mathematical models are enough to stress-test monitoring logic and understand failure modes.
- Visualization of alerts, latency, and integrity makes it easier to communicate risk to non-technical stakeholders.
        """
    )


if __name__ == "__main__":
    main()
