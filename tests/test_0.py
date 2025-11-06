import pytest
import pandas as pd
import numpy as np # Included for completeness as it's often a dependency for data generation and pandas

# definition_641ecf13b82d46c9982bd8307a1de982 block
from definition_641ecf13b82d46c9982bd8307a1de982 import generate_synthetic_safety_data
# End of definition_641ecf13b82d46c9982bd8307a1de982 block

# Helper function to check if a DataFrame is "empty" (None or 0 rows)
def is_df_empty(df):
    return df is None or df.empty

def test_generate_synthetic_safety_data_basic_functionality():
    """
    Test with typical valid inputs to ensure DataFrames are generated and not empty,
    and simulation config contains expected parameters.
    """
    num_agents = 3
    duration = 2
    alert_rate = 0.5
    anomaly_mult = 1.2
    seed = 42

    sensor_df, agent_logs_df, metrics_df, config = generate_synthetic_safety_data(
        num_agents, duration, alert_rate, anomaly_mult, seed
    )

    assert isinstance(sensor_df, pd.DataFrame), "Returned sensor_df is not a pandas DataFrame"
    assert not is_df_empty(sensor_df), "Sensor data DataFrame should not be empty for valid inputs"
    assert isinstance(agent_logs_df, pd.DataFrame), "Returned agent_logs_df is not a pandas DataFrame"
    assert not is_df_empty(agent_logs_df), "Agent logs DataFrame should not be empty for valid inputs"
    assert isinstance(metrics_df, pd.DataFrame), "Returned metrics_df is not a pandas DataFrame"
    assert not is_df_empty(metrics_df), "Base security metrics DataFrame should not be empty for valid inputs"
    assert isinstance(config, dict), "Returned config is not a dictionary"

    # Verify key parameters are present in the config
    assert config.get('num_agents') == num_agents, "Config 'num_agents' mismatch"
    assert config.get('simulation_duration_hours') == duration, "Config 'simulation_duration_hours' mismatch"
    assert config.get('base_alert_rate') == alert_rate, "Config 'base_alert_rate' mismatch"
    assert config.get('anomaly_rate_multiplier') == anomaly_mult, "Config 'anomaly_rate_multiplier' mismatch"
    assert config.get('random_seed') == seed, "Config 'random_seed' mismatch"

@pytest.mark.parametrize(
    "num_agents, simulation_duration_hours",
    [
        (0, 1), # Zero agents, non-zero duration
        (3, 0), # Non-zero agents, zero duration
        (0, 0), # Zero agents, zero duration
    ]
)
def test_generate_synthetic_safety_data_edge_cases_empty_dfs(
    num_agents, simulation_duration_hours
):
    """
    Test edge cases where input parameters (like zero agents or zero duration)
    should result in empty DataFrames.
    """
    base_alert_rate = 0.5
    anomaly_rate_multiplier = 1.0
    random_seed = 1

    sensor_df, agent_logs_df, metrics_df, config = generate_synthetic_safety_data(
        num_agents, simulation_duration_hours, base_alert_rate, anomaly_rate_multiplier, random_seed
    )

    assert isinstance(sensor_df, pd.DataFrame), "Returned sensor_df is not a pandas DataFrame"
    assert is_df_empty(sensor_df), f"Sensor DataFrame should be empty for num_agents={num_agents}, duration={simulation_duration_hours}"
    assert isinstance(agent_logs_df, pd.DataFrame), "Returned agent_logs_df is not a pandas DataFrame"
    assert is_df_empty(agent_logs_df), f"Agent logs DataFrame should be empty for num_agents={num_agents}, duration={simulation_duration_hours}"
    assert isinstance(metrics_df, pd.DataFrame), "Returned metrics_df is not a pandas DataFrame"
    assert is_df_empty(metrics_df), f"Base security metrics DataFrame should be empty for num_agents={num_agents}, duration={simulation_duration_hours}"
    assert isinstance(config, dict), "Returned config is not a dictionary"

    assert config.get('num_agents') == num_agents, "Config 'num_agents' mismatch for edge case"
    assert config.get('simulation_duration_hours') == simulation_duration_hours, "Config 'simulation_duration_hours' mismatch for edge case"


@pytest.mark.parametrize(
    "num_agents, simulation_duration_hours, base_alert_rate, anomaly_rate_multiplier, random_seed",
    [
        ("invalid", 2, 0.5, 1.2, 42), # num_agents not int
        (3, "invalid", 0.5, 1.2, 42), # simulation_duration_hours not int
        (3, 2, "invalid", 1.2, 42), # base_alert_rate not float
        (3, 2, 0.5, "invalid", 42), # anomaly_rate_multiplier not float
        (3, 2, 0.5, 1.2, "invalid"), # random_seed not int
    ]
)
def test_generate_synthetic_safety_data_invalid_input_types(
    num_agents, simulation_duration_hours, base_alert_rate, anomaly_rate_multiplier, random_seed
):
    """
    Test that the function raises TypeError for invalid input types.
    """
    with pytest.raises(TypeError):
        generate_synthetic_safety_data(
            num_agents, simulation_duration_hours, base_alert_rate, anomaly_rate_multiplier, random_seed
        )


@pytest.mark.parametrize(
    "num_agents, simulation_duration_hours, base_alert_rate, anomaly_rate_multiplier, random_seed",
    [
        (-1, 2, 0.5, 1.2, 42), # num_agents < 0
        (3, -1, 0.5, 1.2, 42), # simulation_duration_hours < 0
        (3, 2, -0.5, 1.2, 42), # base_alert_rate < 0
        (3, 2, 0.5, -1.2, 42), # anomaly_rate_multiplier < 0
    ]
)
def test_generate_synthetic_safety_data_invalid_input_values(
    num_agents, simulation_duration_hours, base_alert_rate, anomaly_rate_multiplier, random_seed
):
    """
    Test that the function raises ValueError for invalid input values (e.g., negative numbers for rates/counts).
    """
    with pytest.raises(ValueError):
        generate_synthetic_safety_data(
            num_agents, simulation_duration_hours, base_alert_rate, anomaly_rate_multiplier, random_seed
        )

def test_generate_synthetic_safety_data_reproducibility():
    """
    Test that the function produces identical outputs for the same inputs and random seed.
    """
    num_agents = 5
    duration = 3
    alert_rate = 0.7
    anomaly_mult = 1.5
    seed = 99

    # First call
    sensor_df1, agent_logs_df1, metrics_df1, config1 = generate_synthetic_safety_data(
        num_agents, duration, alert_rate, anomaly_mult, seed
    )

    # Second call with same parameters
    sensor_df2, agent_logs_df2, metrics_df2, config2 = generate_synthetic_safety_data(
        num_agents, duration, alert_rate, anomaly_mult, seed
    )

    # Assert DataFrames are equal using pandas testing utility
    pd.testing.assert_frame_equal(sensor_df1, sensor_df2, check_dtype=True, check_index_type=True)
    pd.testing.assert_frame_equal(agent_logs_df1, agent_logs_df2, check_dtype=True, check_index_type=True)
    pd.testing.assert_frame_equal(metrics_df1, metrics_df2, check_dtype=True, check_index_type=True)

    # Assert configs are equal
    assert config1 == config2, "Simulation configurations should be identical for the same random seed"
