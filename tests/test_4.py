import pytest
from definition_027f6f68eaf24ae1a4de380a5eac6d2e import plot_attack_severity_vs_latency
import pandas as pd
import matplotlib.pyplot as plt

@pytest.fixture
def attack_events_df():
    data = {
        'timestamp': pd.date_range(start='2023-01-01', periods=5, freq='T'),
        'attack_severity': [0.2, 0.5, 0.7, 0.1, 0.9],
        'simulated_detection_latency': [10, 20, 30, 15, 45]
    }
    return pd.DataFrame(data)

def test_plot_attack_severity_vs_latency_basic(attack_events_df):
    try:
        plot_attack_severity_vs_latency(attack_events_df, font_size=12)
    except Exception as e:
        pytest.fail(f"Unexpected error occurred: {e}")

def test_plot_attack_severity_vs_latency_empty_df():
    empty_df = pd.DataFrame(columns=['attack_severity', 'simulated_detection_latency'])
    try:
        plot_attack_severity_vs_latency(empty_df, font_size=12)
    except ValueError as e:
        assert str(e) == "DataFrame is empty"

def test_plot_attack_severity_vs_latency_large_severity(attack_events_df):
    attack_events_df['attack_severity'] = [99999] * len(attack_events_df)
    try:
        plot_attack_severity_vs_latency(attack_events_df, font_size=12)
    except Exception as e:
        pytest.fail(f"Unexpected error with large severity values: {e}")

def test_plot_attack_severity_vs_latency_negative_latency(attack_events_df):
    attack_events_df['simulated_detection_latency'] = [-1, -2, -3, -4, -5]
    try:
        plot_attack_severity_vs_latency(attack_events_df, font_size=12)
    except ValueError as e:
        assert str(e) == "Negative latency values not allowed"

def test_plot_attack_severity_vs_latency_invalid_font_size(attack_events_df):
    try:
        plot_attack_severity_vs_latency(attack_events_df, font_size=-5)
    except ValueError as e:
        assert str(e) == "Font size must be positive"