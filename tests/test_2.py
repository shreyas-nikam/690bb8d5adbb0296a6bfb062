import pytest
from definition_86010b0d9110413ea242a2f0477193e2 import simulate_vulnerability_impact
import pandas as pd

@pytest.fixture
def base_metrics_df():
    return pd.DataFrame({
        'timestamp': pd.date_range(start='2023-01-01', periods=10, freq='H'),
        'alert_frequency': [10] * 10,
        'agent_integrity_score': [0.95] * 10
    })

@pytest.fixture
def simulation_config():
    return {
        'L_base': 5,
        'C_type_dict': {
            'Prompt Injection': 0.5,
            'Data Poisoning': 0.8,
            'Synthetic Identity': 0.6,
            'Untraceable Data Leakage': 0.7
        },
        'K_type_dict': {
            'Prompt Injection': 0.4,
            'Data Poisoning': 0.7,
            'Synthetic Identity': 0.8,
            'Untraceable Data Leakage': 0.5
        },
        'D_type_dict': {
            'Prompt Injection': 20,
            'Data Poisoning': 60,
            'Synthetic Identity': 45,
            'Untraceable Data Leakage': 30
        }
    }

@pytest.mark.parametrize("attack_type, attack_intensity, num_compromised_agents, expected_alerts", [
    ('Prompt Injection', 0.5, 2, 15),
    ('Data Poisoning', 0.8, 3, 18),
    ('Synthetic Identity', 0.6, 1, 16),
    ('Untraceable Data Leakage', 0.3, 2, 13),
    ('Untraceable Data Leakage', 0, 0, 10),  # No attack
])
def test_simulate_vulnerability_impact_alert_frequency(
    base_metrics_df, attack_type, attack_intensity, num_compromised_agents, expected_alerts, simulation_config):
    
    attacked_metrics_df, attack_events_df = simulate_vulnerability_impact(
        base_metrics_df, attack_type, attack_intensity, num_compromised_agents, simulation_config)

    assert attacked_metrics_df['alert_frequency'].iloc[0] == expected_alerts

@pytest.mark.parametrize("attack_type, attack_intensity, num_compromised_agents, expected_integrity", [
    ('Prompt Injection', 0.5, 2, 0.9),
    ('Data Poisoning', 0.8, 3, 0.82),
    ('Synthetic Identity', 0.6, 1, 0.88),
    ('Untraceable Data Leakage', 0.3, 2, 0.935),
    ('Untraceable Data Leakage', 0, 0, 0.95),  # No attack
])
def test_simulate_vulnerability_impact_agent_integrity(
    base_metrics_df, attack_type, attack_intensity, num_compromised_agents, expected_integrity, simulation_config):

    attacked_metrics_df, attack_events_df = simulate_vulnerability_impact(
        base_metrics_df, attack_type, attack_intensity, num_compromised_agents, simulation_config)

    assert attacked_metrics_df['agent_integrity_score'].iloc[0] == expected_integrity

@pytest.mark.parametrize("attack_type, attack_intensity, num_compromised_agents, expected_latency", [
    ('Prompt Injection', 0.5, 2, 15),
    ('Data Poisoning', 0.8, 3, 85),
    ('Synthetic Identity', 0.6, 1, 32),
    ('Untraceable Data Leakage', 0.3, 2, 14),
    ('Untraceable Data Leakage', 0, 0, 5),  # No attack
])
def test_simulate_vulnerability_impact_detection_latency(
    base_metrics_df, attack_type, attack_intensity, num_compromised_agents, expected_latency, simulation_config):

    attacked_metrics_df, attack_events_df = simulate_vulnerability_impact(
        base_metrics_df, attack_type, attack_intensity, num_compromised_agents, simulation_config)

    assert attack_events_df['detection_latency'].iloc[0] == expected_latency

@pytest.mark.parametrize("attack_intensity", [-0.1, 1.1])
def test_simulate_vulnerability_impact_invalid_intensity(
    base_metrics_df, attack_intensity, simulation_config):
    
    with pytest.raises(ValueError):
        simulate_vulnerability_impact(
            base_metrics_df, 'Prompt Injection', attack_intensity, 2, simulation_config)

@pytest.mark.parametrize("num_compromised_agents", [-1, 'two'])
def test_simulate_vulnerability_impact_invalid_agent_count(
    base_metrics_df, num_compromised_agents, simulation_config):
    
    with pytest.raises(ValueError):
        simulate_vulnerability_impact(
            base_metrics_df, 'Prompt Injection', 0.5, num_compromised_agents, simulation_config)