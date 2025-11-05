import pytest
from definition_745b964084aa4a948859d4192cacaa5e import generate_synthetic_safety_data

@pytest.mark.parametrize("num_agents, simulation_duration_hours, base_alert_rate, anomaly_rate_multiplier, random_seed", [
    (10, 2, 5, 1.5, 42),
    (0, 1, 2, 1.2, 10),  # Edge case: No agents
    (5, 0, 3, 1.1, 15),  # Edge case: Zero-hour simulation
    (1, 1, -5, 1.0, 22),  # Edge case: Negative alert rate
    (3, 2, 4, 0, 5)  # Edge case: Zero anomaly multiplier
])
def test_generate_synthetic_safety_data(num_agents, simulation_duration_hours, base_alert_rate, anomaly_rate_multiplier, random_seed):
    try:
        sensor_data_df, agent_logs_df, base_security_metrics_df, simulation_config = generate_synthetic_safety_data(
            num_agents, simulation_duration_hours, base_alert_rate, anomaly_rate_multiplier, random_seed
        )
        assert sensor_data_df is not None
        assert agent_logs_df is not None
        assert base_security_metrics_df is not None
        assert isinstance(simulation_config, dict)
    except ValueError as ve:
        assert "alert rate" in str(ve) or "simulation duration" in str(ve)
    except Exception as e:
        assert isinstance(e, (TypeError, ValueError))