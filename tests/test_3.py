import pytest
from definition_e201f4b2a082401fa55d8779fac33379 import plot_alert_frequency_trend
import pandas as pd

# Mock DataFrames for baseline and attacked scenarios
base_df = pd.DataFrame({
    'timestamp': pd.date_range(start='2023-01-01', periods=5, freq='D'),
    'alert_frequency': [10, 15, 10, 5, 8],
    'agent_integrity_score': [0.9, 0.85, 0.88, 0.87, 0.9]
})

attacked_df = pd.DataFrame({
    'timestamp': pd.date_range(start='2023-01-01', periods=5, freq='D'),
    'alert_frequency': [12, 18, 14, 10, 13],
    'agent_integrity_score': [0.6, 0.5, 0.55, 0.57, 0.6]
})

@pytest.mark.parametrize("base_df, attacked_df, attack_type, attack_intensity, font_size, expected", [
    (base_df, attacked_df, "Data Poisoning", 0.5, 12, None),  # Nominal case
    (base_df.head(0), attacked_df.head(0), "Prompt Injection", 0.7, 14, ValueError),  # Empty DataFrames
    (base_df, attacked_df, "Synthetic Identity", 1.1, 12, ValueError),  # Invalid intensity > 1
    (None, attacked_df, "Data Poisoning", 0.5, 12, TypeError),  # None base_df
    (base_df, None, "Untraceable Data Leakage", 0.3, 12, TypeError),  # None attacked_df
])

def test_plot_alert_frequency_trend(base_df, attacked_df, attack_type, attack_intensity, font_size, expected):
    try:
        plot_alert_frequency_trend(base_df, attacked_df, attack_type, attack_intensity, font_size)
    except Exception as e:
        assert isinstance(e, expected)