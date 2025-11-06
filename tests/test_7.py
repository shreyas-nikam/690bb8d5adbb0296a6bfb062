import pytest
from unittest.mock import patch, call
import sys
from io import StringIO

# definition_75dc4274363b4ce98d7aaa6b5fefceec block - DO NOT REPLACE or REMOVE
from definition_75dc4274363b4ce98d7aaa6b5fefceec import define_and_display_interactive_parameters
# End definition_75dc4274363b4ce98d7aaa6b5fefceec block

# Test 1: Verify fixed simulation parameters are printed to the console.
@patch('builtins.print')
def test_fixed_parameters_are_printed(mock_print):
    """
    Tests that the define_and_display_interactive_parameters function
    prints all specified fixed simulation parameters to standard output.
    """
    define_and_display_interactive_parameters()

    # Capture all arguments passed to print calls for flexible checking
    printed_output = ""
    for c in mock_print.call_args_list:
        printed_output += ' '.join(str(arg) for arg in c.args) + '\n'

    # Check for the presence of key information about fixed parameters,
    # being flexible with exact formatting but ensuring content exists.
    assert "Fixed Simulation Parameters:" in printed_output
    assert "SIMULATION_DURATION_HOURS: 2" in printed_output
    assert "NUM_AGENTS: 10" in printed_output
    assert "BASE_ALERT_RATE_PER_HOUR: 5" in printed_output
    assert "ANOMALY_RATE_MULTIPLIER: 2.5" in printed_output
    assert "RANDOM_SEED: 42" in printed_output

# Test 2: Verify the 'Attack Intensity' FloatSlider is created with correct attributes.
@patch('ipywidgets.FloatSlider', autospec=True)
@patch('builtins.print') # Mock print to avoid stdout side effects in this specific test
def test_attack_intensity_float_slider_creation(mock_print, mock_float_slider):
    """
    Tests that a FloatSlider for 'Attack Intensity' is correctly instantiated
    with its specified min, max, step, default, description, and tooltip.
    """
    define_and_display_interactive_parameters()

    mock_float_slider.assert_called_once()
    
    # Extract keyword arguments passed to the FloatSlider constructor
    call_kwargs = mock_float_slider.call_args.kwargs

    assert call_kwargs.get('min') == 0.0
    assert call_kwargs.get('max') == 1.0
    assert call_kwargs.get('step') == 0.1
    assert call_kwargs.get('default') == 0.5
    assert call_kwargs.get('description') == 'Attack Intensity'
    assert call_kwargs.get('tooltip') == "Controls the severity of the simulated attack (0.0 = no attack, 1.0 = maximum impact)."
    # Also check specific ipywidgets attributes like continuous_update, readout, readout_format
    assert call_kwargs.get('continuous_update') is False
    assert call_kwargs.get('readout') is True
    assert call_kwargs.get('readout_format') == '.1f'

# Test 3: Verify the 'Attack Type' Dropdown is created with correct attributes.
@patch('ipywidgets.Dropdown', autospec=True)
@patch('builtins.print') # Mock print to avoid stdout side effects
def test_attack_type_dropdown_creation(mock_print, mock_dropdown):
    """
    Tests that a Dropdown for 'Attack Type' is correctly instantiated
    with its specified options, default, description, and tooltip.
    """
    define_and_display_interactive_parameters()

    mock_dropdown.assert_called_once()
    
    # Extract keyword arguments passed to the Dropdown constructor
    call_kwargs = mock_dropdown.call_args.kwargs

    expected_options = ['Prompt Injection', 'Data Poisoning', 'Synthetic Identity', 'Untraceable Data Leakage']
    assert call_kwargs.get('options') == expected_options
    assert call_kwargs.get('default') == 'Prompt Injection'
    assert call_kwargs.get('description') == 'Attack Type'
    assert call_kwargs.get('tooltip') == "Selects the type of AI security vulnerability to simulate."

# Test 4: Verify the 'Number of Compromised Agents' IntSlider is created with correct attributes.
@patch('ipywidgets.IntSlider', autospec=True)
@patch('builtins.print') # Mock print to avoid stdout side effects
def test_num_compromised_agents_int_slider_creation(mock_print, mock_int_slider):
    """
    Tests that an IntSlider for 'Number of Compromised Agents' is correctly instantiated
    with its specified min, max, step, default, description, and tooltip.
    """
    define_and_display_interactive_parameters()

    mock_int_slider.assert_called_once()
    
    # Extract keyword arguments passed to the IntSlider constructor
    call_kwargs = mock_int_slider.call_args.kwargs

    assert call_kwargs.get('min') == 0
    assert call_kwargs.get('max') == 5
    assert call_kwargs.get('step') == 1
    assert call_kwargs.get('default') == 1
    assert call_kwargs.get('description') == 'Number of Compromised Agents'
    assert call_kwargs.get('tooltip') == "Specifies the count of simulated agents affected by the attack."
    # Also check specific ipywidgets attributes
    assert call_kwargs.get('continuous_update') is False
    assert call_kwargs.get('readout') is True

# Test 5: Verify that ipywidgets.interact (or equivalent display mechanism) is called.
@patch('ipywidgets.interact', autospec=True)
@patch('ipywidgets.FloatSlider', autospec=True) # Mock these to allow interact to be called without actual widget creation
@patch('ipywidgets.Dropdown', autospec=True)
@patch('ipywidgets.IntSlider', autospec=True)
@patch('builtins.print') # Mock print to avoid stdout side effects
def test_interact_is_called(mock_print, mock_int_slider, mock_dropdown, mock_float_slider, mock_interact):
    """
    Tests that ipywidgets.interact is called within the function to display
    the interactive parameters, as indicated by the function's purpose.
    """
    define_and_display_interactive_parameters()

    # The `interact` function is responsible for displaying the widgets and linking their values.
    # Verifying it's called ensures the "display interactive widgets" part of the function's
    # purpose is attempted. The exact arguments to `interact` might vary depending on the
    # internal callback function, but its invocation is key.
    mock_interact.assert_called_once()