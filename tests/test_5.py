import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
import matplotlib.pyplot
import seaborn

# Block for module import. DO NOT REPLACE or REMOVE.
from definition_af529e8fe2324c7491e4a43454db030d import plot_agent_integrity_comparison
# END OF BLOCK

@pytest.fixture(autouse=True)
def mock_plotting(mocker):
    """
    Fixture to mock matplotlib and seaborn functions to prevent actual plotting
    and file saving during tests.
    """
    mocker.patch('matplotlib.pyplot.figure')
    mocker.patch('matplotlib.pyplot.title')
    mocker.patch('matplotlib.pyplot.xlabel')
    mocker.patch('matplotlib.pyplot.ylabel')
    mocker.patch('matplotlib.pyplot.xticks')
    mocker.patch('matplotlib.pyplot.yticks')
    mocker.patch('matplotlib.pyplot.grid')
    mocker.patch('matplotlib.pyplot.tight_layout')
    mocker.patch('matplotlib.pyplot.savefig')
    mocker.patch('matplotlib.pyplot.show')
    mocker.patch('seaborn.barplot')
    mocker.patch('seaborn.color_palette')

# Define DataFrames for various test scenarios
df_happy_path = pd.DataFrame({
    'agent_id': [1, 1, 2, 2, 3, 3, 4, 4],
    'agent_integrity_score': [0.75, 0.70, 0.90, 0.88, 0.60, 0.65, 0.95, 0.93]
})

df_no_compromised = pd.DataFrame({
    'agent_id': [1, 1, 2, 2],
    'agent_integrity_score': [0.90, 0.88, 0.95, 0.93]
})

df_all_compromised = pd.DataFrame({
    'agent_id': [1, 1, 2, 2],
    'agent_integrity_score': [0.50, 0.45, 0.60, 0.55]
})

df_missing_integrity_col = pd.DataFrame({
    'agent_id': [1, 2],
    'some_other_column': [10, 20]
})

df_missing_agent_id_col = pd.DataFrame({
    'agent_integrity_score': [0.8, 0.7]
})

df_single_agent_valid = pd.DataFrame({'agent_id': [1], 'agent_integrity_score': [0.9]})


@pytest.mark.parametrize(
    "attacked_df, num_compromised_agents, font_size, expected_exception, expected_match",
    [
        # Test Case 1: Happy Path - Some Compromised Agents
        (df_happy_path, 2, 12, None, None),

        # Test Case 2: Edge Case - No Compromised Agents
        (df_no_compromised, 0, 12, None, None),

        # Test Case 3: Edge Case - All Agents Compromised
        (df_all_compromised, 2, 12, None, None),

        # Test Case 4.1: Error - Missing 'agent_integrity_score' column
        (df_missing_integrity_col, 1, 12, KeyError, "agent_integrity_score"),

        # Test Case 4.2: Error - Missing 'agent_id' column
        (df_missing_agent_id_col, 1, 12, KeyError, "agent_id"),

        # Test Case 5.1: Error - Invalid num_compromised_agents (negative)
        (df_single_agent_valid, -1, 12, ValueError, "num_compromised_agents must be a non-negative integer."),

        # Test Case 5.2: Error - Invalid font_size (zero)
        (df_single_agent_valid, 0, 0, ValueError, "font_size must be a positive number."),

        # Test Case 5.3: Error - Invalid attacked_df type
        ("not a dataframe", 1, 12, TypeError, "attacked_df must be a pandas DataFrame."),

        # Test Case 5.4: Edge Case - num_compromised_agents > total agents
        (df_single_agent_valid, 5, 12, None, None),
    ]
)
def test_plot_agent_integrity_comparison(
    mock_plotting, attacked_df, num_compromised_agents, font_size, expected_exception, expected_match
):
    """
    Tests the plot_agent_integrity_comparison function across various scenarios,
    including happy path, edge cases for agent counts, and error conditions.
    """
    if expected_exception is None:
        # Scenario: Expected to pass and generate a plot
        plot_agent_integrity_comparison(attacked_df, num_compromised_agents, font_size)

        # Assert that plotting functions were called
        matplotlib.pyplot.figure.assert_called_once()
        seaborn.barplot.assert_called_once()
        matplotlib.pyplot.title.assert_called_once()
        matplotlib.pyplot.xlabel.assert_called_once_with('Agent Status', fontsize=font_size)
        matplotlib.pyplot.ylabel.assert_called_once_with('Average Integrity Score', fontsize=font_size)
        matplotlib.pyplot.savefig.assert_called_once_with("agent_integrity_comparison.png")
        matplotlib.pyplot.show.assert_called_once()

        # Extract data passed to seaborn.barplot for detailed assertions
        _, call_kwargs = seaborn.barplot.call_args
        plot_data = call_kwargs['data']
        assert isinstance(plot_data, pd.DataFrame)
        assert 'Agent Status' in plot_data.columns
        assert 'Average Integrity Score' in plot_data.columns

        # Specific assertions for each successful scenario
        if attacked_df is df_happy_path and num_compromised_agents == 2:
            # Agent 1 avg: (0.75 + 0.70) / 2 = 0.725
            # Agent 2 avg: (0.90 + 0.88) / 2 = 0.89
            # Agent 3 avg: (0.60 + 0.65) / 2 = 0.625
            # Agent 4 avg: (0.95 + 0.93) / 2 = 0.94
            # Compromised (IDs 1, 2): Avg = (0.725 + 0.89) / 2 = 0.8075
            # Uncompromised (IDs 3, 4): Avg = (0.625 + 0.94) / 2 = 0.7825
            compromised_score = plot_data[plot_data['Agent Status'] == 'Compromised']['Average Integrity Score'].iloc[0]
            uncompromised_score = plot_data[plot_data['Agent Status'] == 'Uncompromised']['Average Integrity Score'].iloc[0]
            assert compromised_score == pytest.approx(0.8075)
            assert uncompromised_score == pytest.approx(0.7825)
            matplotlib.pyplot.title.assert_called_once_with(
                'Average Agent Integrity Scores: Compromised vs. Uncompromised', fontsize=font_size + 2
            )

        elif attacked_df is df_no_compromised and num_compromised_agents == 0:
            # Only 'Uncompromised' group expected
            assert 'Compromised' not in plot_data['Agent Status'].values
            assert 'Uncompromised' in plot_data['Agent Status'].values
            assert len(plot_data) == 1
            uncompromised_score = plot_data['Average Integrity Score'].iloc[0]
            # Agent 1 avg: (0.90 + 0.88) / 2 = 0.89
            # Agent 2 avg: (0.95 + 0.93) / 2 = 0.94
            # Overall avg: (0.89 + 0.94) / 2 = 0.915
            assert uncompromised_score == pytest.approx(0.915)

        elif attacked_df is df_all_compromised and num_compromised_agents == 2:
            # Only 'Compromised' group expected
            assert 'Uncompromised' not in plot_data['Agent Status'].values
            assert 'Compromised' in plot_data['Agent Status'].values
            assert len(plot_data) == 1
            compromised_score = plot_data['Average Integrity Score'].iloc[0]
            # Agent 1 avg: (0.50 + 0.45) / 2 = 0.475
            # Agent 2 avg: (0.60 + 0.55) / 2 = 0.575
            # Overall avg: (0.475 + 0.575) / 2 = 0.525
            assert compromised_score == pytest.approx(0.525)

        elif attacked_df is df_single_agent_valid and num_compromised_agents == 5: # num_compromised_agents > total_agents
            # Only 'Compromised' group expected (the single agent becomes compromised)
            assert 'Uncompromised' not in plot_data['Agent Status'].values
            assert 'Compromised' in plot_data['Agent Status'].values
            assert len(plot_data) == 1
            compromised_score = plot_data['Average Integrity Score'].iloc[0]
            assert compromised_score == pytest.approx(0.9) # Single agent with score 0.9

    else:
        # Scenario: Expected to raise an exception
        with pytest.raises(expected_exception, match=expected_match):
            plot_agent_integrity_comparison(attacked_df, num_compromised_agents, font_size)

        # Ensure no plotting functions were called if an exception was raised
        matplotlib.pyplot.figure.assert_not_called()
        seaborn.barplot.assert_not_called()
        matplotlib.pyplot.savefig.assert_not_called()