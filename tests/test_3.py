import pytest
import pandas as pd
import matplotlib.pyplot as plt
from unittest.mock import patch, MagicMock
import os

# Keep the definition_b0a4ea33d2c6485db808b417389f805c block as it is. DO NOT REPLACE or REMOVE the block.
from definition_b0a4ea33d2c6485db808b417389f805c import plot_alert_frequency_trend

# Helper function to create dummy dataframes for testing
def _create_dummy_df(num_rows=10, has_alerts=True, has_timestamp=True):
    data = {}
    if has_timestamp:
        data['timestamp'] = pd.to_datetime(pd.date_range(start='2023-01-01', periods=num_rows, freq='H'))
    if has_alerts:
        data['alert_frequency'] = [i + (10 if has_alerts else 0) for i in range(num_rows)]
    return pd.DataFrame(data)

@patch('matplotlib.pyplot.savefig')
@patch('matplotlib.pyplot.show')
@patch('matplotlib.pyplot.figure')
@patch('matplotlib.pyplot.title')
@patch('matplotlib.pyplot.xlabel')
@patch('matplotlib.pyplot.ylabel')
@patch('matplotlib.pyplot.legend')
@patch('matplotlib.pyplot.grid')
@patch('seaborn.color_palette', return_value=['blue', 'orange']) # Mock color palette for consistency
def test_plot_alert_frequency_trend_basic_functionality(
    mock_color_palette, mock_grid, mock_legend, mock_ylabel, mock_xlabel, mock_title, mock_figure, mock_show, mock_savefig
):
    """
    Test case 1: Verify basic functionality with valid data.
    Ensures that plotting functions are called and the file is attempted to be saved.
    """
    base_df = _create_dummy_df(num_rows=5)
    attacked_df = _create_dummy_df(num_rows=5, has_alerts=True)
    attack_type = "Prompt Injection"
    attack_intensity = 0.5
    font_size = 12

    plot_alert_frequency_trend(base_df, attacked_df, attack_type, attack_intensity, font_size)

    mock_figure.assert_called_once()
    mock_title.assert_called_once_with(f"Alert Frequency Over Time ({attack_type} at {attack_intensity*100:.0f}% Intensity)", fontsize=font_size)
    mock_xlabel.assert_called_once_with('Time', fontsize=font_size)
    mock_ylabel.assert_called_once_with('Alert Frequency', fontsize=font_size)
    mock_legend.assert_called_once()
    mock_grid.assert_called_once()
    mock_savefig.assert_called_once_with("alert_frequency_trend.png")
    mock_show.assert_called_once()

@patch('matplotlib.pyplot.savefig')
@patch('matplotlib.pyplot.show')
@patch('matplotlib.pyplot.figure')
@patch('matplotlib.pyplot.title')
@patch('matplotlib.pyplot.xlabel')
@patch('matplotlib.pyplot.ylabel')
@patch('matplotlib.pyplot.legend')
@patch('matplotlib.pyplot.grid')
@patch('seaborn.color_palette', return_value=['blue', 'orange'])
def test_plot_alert_frequency_trend_empty_dataframes(
    mock_color_palette, mock_grid, mock_legend, mock_ylabel, mock_xlabel, mock_title, mock_figure, mock_show, mock_savefig
):
    """
    Test case 2: Edge case - Input DataFrames are empty.
    The function should handle this gracefully, potentially plotting empty lines, but not crash.
    """
    base_df = pd.DataFrame(columns=['timestamp', 'alert_frequency'])
    attacked_df = pd.DataFrame(columns=['timestamp', 'alert_frequency'])
    attack_type = "Data Poisoning"
    attack_intensity = 0.8
    font_size = 14

    plot_alert_frequency_trend(base_df, attacked_df, attack_type, attack_intensity, font_size)

    mock_figure.assert_called_once()
    mock_title.assert_called_once() # Title still called
    mock_xlabel.assert_called_once()
    mock_ylabel.assert_called_once()
    mock_legend.assert_called_once()
    mock_grid.assert_called_once()
    mock_savefig.assert_called_once_with("alert_frequency_trend.png")
    mock_show.assert_called_once()

@pytest.mark.parametrize("base_df_missing_col, attacked_df_missing_col, expected_exception", [
    # Test case 3a: Base DF missing 'timestamp'
    (_create_dummy_df(has_timestamp=False), _create_dummy_df(), KeyError),
    # Test case 3b: Attacked DF missing 'alert_frequency'
    (_create_dummy_df(), _create_dummy_df(has_alerts=False), KeyError),
    # Test case 3c: Base DF missing 'alert_frequency'
    (_create_dummy_df(has_alerts=False), _create_dummy_df(), KeyError),
    # Test case 3d: Attacked DF missing 'timestamp'
    (_create_dummy_df(), _create_dummy_df(has_timestamp=False), KeyError),
])
def test_plot_alert_frequency_trend_missing_required_columns(
    base_df_missing_col, attacked_df_missing_col, expected_exception
):
    """
    Test case 3: Edge case - Input DataFrames are missing required columns.
    Should raise a KeyError when trying to access the non-existent column.
    """
    attack_type = "Synthetic Identity"
    attack_intensity = 0.7
    font_size = 10

    with pytest.raises(expected_exception):
        plot_alert_frequency_trend(base_df_missing_col, attacked_df_missing_col, attack_type, attack_intensity, font_size)

@pytest.mark.parametrize("base_df, attacked_df, attack_type, attack_intensity, font_size, expected_exception", [
    # Test case 4a: font_size is not an int
    (_create_dummy_df(), _create_dummy_df(), "Type", 0.5, "12", TypeError),
    # Test case 4b: attack_intensity is not a number (e.g., string)
    (_create_dummy_df(), _create_dummy_df(), "Type", "invalid", 12, TypeError),
    # Test case 4c: attack_type is not a string
    (_create_dummy_df(), _create_dummy_df(), 123, 0.5, 12, TypeError),
    # Test case 4d: base_df is None
    (None, _create_dummy_df(), "Type", 0.5, 12, AttributeError),
    # Test case 4e: attacked_df is None
    (_create_dummy_df(), None, "Type", 0.5, 12, AttributeError),
])
def test_plot_alert_frequency_trend_invalid_parameter_types(
    base_df, attacked_df, attack_type, attack_intensity, font_size, expected_exception
):
    """
    Test case 4: Edge case - Invalid data types for plot parameters or DataFrames themselves.
    Verifies that appropriate TypeErrors or AttributeErrors are raised.
    """
    with pytest.raises(expected_exception):
        plot_alert_frequency_trend(base_df, attacked_df, attack_type, attack_intensity, font_size)

@patch('matplotlib.pyplot.savefig')
@patch('matplotlib.pyplot.show')
@patch('matplotlib.pyplot.figure')
@patch('matplotlib.pyplot.title')
@patch('matplotlib.pyplot.xlabel')
@patch('matplotlib.pyplot.ylabel')
@patch('matplotlib.pyplot.legend')
@patch('matplotlib.pyplot.grid')
@patch('seaborn.color_palette', return_value=['blue', 'orange'])
def test_plot_alert_frequency_trend_title_and_labels_formatting(
    mock_color_palette, mock_grid, mock_legend, mock_ylabel, mock_xlabel, mock_title, mock_figure, mock_show, mock_savefig
):
    """
    Test case 5: Verify correct formatting of plot title and axis labels.
    Checks if dynamic values (attack_type, attack_intensity, font_size) are correctly used.
    """
    base_df = _create_dummy_df(num_rows=3)
    attacked_df = _create_dummy_df(num_rows=3)
    attack_type = "Untraceable Data Leakage"
    attack_intensity = 0.75
    font_size = 16 # Use a different font size to ensure it's passed

    plot_alert_frequency_trend(base_df, attacked_df, attack_type, attack_intensity, font_size)

    expected_title = f"Alert Frequency Over Time ({attack_type} at {attack_intensity*100:.0f}% Intensity)"
    mock_title.assert_called_once_with(expected_title, fontsize=font_size)
    mock_xlabel.assert_called_once_with('Time', fontsize=font_size)
    mock_ylabel.assert_called_once_with('Alert Frequency', fontsize=font_size)
    mock_legend.assert_called_once()
    mock_savefig.assert_called_once_with("alert_frequency_trend.png")
    mock_show.assert_called_once()