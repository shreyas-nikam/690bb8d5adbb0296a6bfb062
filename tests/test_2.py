import pytest
import pandas as pd
import numpy as np
from datetime import timedelta

# Placeholder for the module import
from definition_778c4f99992a4472bc8c541f26dae73b import simulate_vulnerability_impact

# --- Helper functions for mock data and coefficients ---
def create_mock_base_metrics_df(num_agents=3, num_timestamps=2, base_alert=5.0, base_integrity=0.95):
    """
    Creates a mock DataFrame resembling base_metrics_df for testing.
    Each timestamp has entries for all agents.
    """
    timestamps = pd.to_datetime([f"2023-01-01 {i:02d}:00:00" for i in range(num_timestamps)])
    data = []
    for ts in timestamps:
        for agent_id in range(1, num_agents + 1):
            data.append({
                'timestamp': ts,
                'agent_id': agent_id,
                'alert_frequency': base_alert,  # System-wide, so constant per timestamp block
                'agent_integrity_score': base_integrity
            })
    df = pd.DataFrame(data)
    return df

# Mock simulation configuration. Includes a random_seed for deterministic agent selection.
mock_sim_config = {
    'start_time': pd.to_datetime("2023-01-01 00:00:00"),
    'end_time': pd.to_datetime("2023-01-01 01:00:00"),
    'random_seed': 42 # Ensures repeatable compromised agent selection in the actual function
}

# Coefficients as defined in the notebook specification
COEFFS = {
    'C_type': {'Prompt Injection': 0.5, 'Data Poisoning': 0.8, 'Synthetic Identity': 0.6, 'Untraceable Data Leakage': 0.7},
    'K_type': {'Prompt Injection': 0.4, 'Data Poisoning': 0.7, 'Synthetic Identity': 0.8, 'Untraceable Data Leakage': 0.5},
    'D_type': {'Prompt Injection': 20, 'Data Poisoning': 60, 'Synthetic Identity': 45, 'Untraceable Data Leakage': 30}, # in minutes
    'L_base': 5 # nominal baseline detection latency in minutes
}

# --- Pytest Test Cases ---

@pytest.mark.parametrize(
    "attack_type, attack_intensity, num_compromised_agents, num_agents_in_df, expected_exception, expected_alert_freq_ratio, expected_integrity_score_ratio, expected_detection_latency",
    [
        # Test Case 1: Standard 'Prompt Injection' Attack (1 compromised agent out of 3)
        # Expected functionality: alert frequency increases, one agent's integrity decreases, attack event recorded.
        ('Prompt Injection', 0.5, 1, 3, None,
         1 + 0.5 * COEFFS['C_type']['Prompt Injection'],
         1 - 0.5 * COEFFS['K_type']['Prompt Injection'],
         COEFFS['L_base'] + 0.5 * COEFFS['D_type']['Prompt Injection']),

        # Test Case 2: No Attack (attack_intensity = 0, 0 compromised agents)
        # Edge case: No impact should mean metrics remain unchanged, and no attack event is logged.
        ('Data Poisoning', 0.0, 0, 3, None,
         1 + 0.0 * COEFFS['C_type']['Data Poisoning'],
         1 - 0.0 * COEFFS['K_type']['Data Poisoning'],
         COEFFS['L_base'] + 0.0 * COEFFS['D_type']['Data Poisoning']),

        # Test Case 3: Maximum Attack Impact ('Synthetic Identity', all 3 agents compromised, max intensity)
        # Edge case: Verify maximum possible impact on all relevant metrics.
        ('Synthetic Identity', 1.0, 3, 3, None,
         1 + 1.0 * COEFFS['C_type']['Synthetic Identity'],
         1 - 1.0 * COEFFS['K_type']['Synthetic Identity'],
         COEFFS['L_base'] + 1.0 * COEFFS['D_type']['Synthetic Identity']),

        # Test Case 4: Invalid `attack_type`
        # Edge case: Function should handle unknown attack types gracefully, e.g., by raising ValueError.
        ('Invalid Attack Type', 0.5, 1, 3, ValueError, None, None, None),

        # Test Case 5: `num_compromised_agents` exceeds available agents
        # Edge case: Attempting to compromise more agents than exist should raise an error (e.g., ValueError from np.random.choice).
        ('Untraceable Data Leakage', 0.8, 4, 3, ValueError, None, None, None),
    ]
)
def test_simulate_vulnerability_impact(
    attack_type, attack_intensity, num_compromised_agents, num_agents_in_df, expected_exception,
    expected_alert_freq_ratio, expected_integrity_score_ratio, expected_detection_latency
):
    """
    Tests the simulate_vulnerability_impact function across various scenarios,
    including standard functionality and edge cases.
    """
    base_metrics_df = create_mock_base_metrics_df(num_agents=num_agents_in_df)

    if expected_exception:
        # Test cases expecting an exception
        with pytest.raises(expected_exception):
            simulate_vulnerability_impact(base_metrics_df.copy(), attack_type, attack_intensity, num_compromised_agents, mock_sim_config)
        return

    # Call the function for valid scenarios
    # Assumes simulate_vulnerability_impact uses `simulation_config['random_seed']`
    # for deterministic selection of compromised agents.
    attacked_df, attack_events_df = simulate_vulnerability_impact(
        base_metrics_df.copy(), attack_type, attack_intensity, num_compromised_agents, mock_sim_config
    )

    # --- Assertions for attacked_security_metrics_df ---
    assert isinstance(attacked_df, pd.DataFrame)
    assert not attacked_df.empty
    assert len(attacked_df) == len(base_metrics_df)

    # 1. Alert Frequency Check: Should be modified for all rows if attack_intensity > 0
    initial_alert_freq = base_metrics_df['alert_frequency'].iloc[0]
    expected_alert_freq = initial_alert_freq * expected_alert_freq_ratio
    pd.testing.assert_series_equal(
        attacked_df['alert_frequency'],
        pd.Series([expected_alert_freq] * len(attacked_df), index=attacked_df.index, name='alert_frequency'),
        check_exact=False, rtol=1e-6
    )

    # 2. Agent Integrity Score Check: Modified only for compromised agents
    all_agent_ids = base_metrics_df['agent_id'].unique()
    
    # Re-create the expected compromised agent IDs using the same seed for reproducibility
    if num_compromised_agents > 0:
        rng = np.random.RandomState(mock_sim_config['random_seed'])
        expected_compromised_agents_ids = set(rng.choice(all_agent_ids, size=num_compromised_agents, replace=False))
    else:
        expected_compromised_agents_ids = set()

    for agent_id in all_agent_ids:
        initial_integrity_score = base_metrics_df[base_metrics_df['agent_id'] == agent_id]['agent_integrity_score'].iloc[0]
        actual_integrity_score_series = attacked_df[attacked_df['agent_id'] == agent_id]['agent_integrity_score']

        if agent_id in expected_compromised_agents_ids:
            expected_integrity_score = initial_integrity_score * expected_integrity_score_ratio
            pd.testing.assert_series_equal(
                actual_integrity_score_series,
                pd.Series([expected_integrity_score] * len(actual_integrity_score_series), index=actual_integrity_score_series.index, name='agent_integrity_score'),
                check_exact=False, rtol=1e-6
            )
        else:
            # Uncompromised agents' scores should remain unchanged
            pd.testing.assert_series_equal(
                actual_integrity_score_series,
                pd.Series([initial_integrity_score] * len(actual_integrity_score_series), index=actual_integrity_score_series.index, name='agent_integrity_score'),
                check_exact=False, rtol=1e-6
            )
            
    # --- Assertions for attack_events_df ---
    assert isinstance(attack_events_df, pd.DataFrame)
    
    if attack_intensity == 0 and num_compromised_agents == 0:
        # If no attack, the events DataFrame should be empty.
        assert attack_events_df.empty
    else:
        # If an attack occurred, there should be at least one event record.
        assert len(attack_events_df) >= 1
        assert all(col in attack_events_df.columns for col in ['timestamp', 'attack_type', 'attack_intensity', 'num_compromised_agents', 'attack_severity', 'detection_latency'])

        # Check values in the first (and likely only) attack event
        assert attack_events_df['attack_type'].iloc[0] == attack_type
        assert np.isclose(attack_events_df['attack_intensity'].iloc[0], attack_intensity)
        assert attack_events_df['num_compromised_agents'].iloc[0] == num_compromised_agents
        assert np.isclose(attack_events_df['detection_latency'].iloc[0], expected_detection_latency)
        
        # Attack severity should be positive if there's any attack
        if attack_intensity > 0 or num_compromised_agents > 0:
            assert attack_events_df['attack_severity'].iloc[0] > 0
        else:
            assert attack_events_df['attack_severity'].iloc[0] == 0 # Should be covered by empty check, but for robustness