import pytest
from definition_8a84927ae1d5471b8df80a7a1bc6d39e import plot_agent_integrity_comparison

def test_valid_data():
    import pandas as pd
    attacked_df = pd.DataFrame({
        "agent_id": [1, 2, 3],
        "agent_integrity_score": [0.8, 0.9, 0.95]
    })
    num_compromised_agents = 1
    font_size = 12
    
    try:
        plot_agent_integrity_comparison(attacked_df, num_compromised_agents, font_size)
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")

@pytest.mark.parametrize("attacked_df, num_compromised_agents, font_size, exception_type", [
    (None, 1, 12, AttributeError),
    ([], 1, 12, TypeError),
    ([1, 2, 3], 1, 12, AttributeError),
    ([{"agent_id": 1, "score": 0.8}], 1, 12, KeyError),
    ({"agent_id": [1, 2], "score": [0.8, 0.9]}, "one", 12, TypeError),
])
def test_invalid_data(attacked_df, num_compromised_agents, font_size, exception_type):
    with pytest.raises(exception_type):
        plot_agent_integrity_comparison(attacked_df, num_compromised_agents, font_size)

def test_compromised_agents_count_exceeds_total():
    import pandas as pd
    attacked_df = pd.DataFrame({
        "agent_id": [1, 2],
        "agent_integrity_score": [0.8, 0.9]
    })
    num_compromised_agents = 3
    font_size = 12
    
    try:
        plot_agent_integrity_comparison(attacked_df, num_compromised_agents, font_size)
    except ValueError as e:
        assert str(e) == "Number of compromised agents exceeds total available agents."

def test_zero_compromised_agents():
    import pandas as pd
    attacked_df = pd.DataFrame({
        "agent_id": [1, 2, 3],
        "agent_integrity_score": [0.8, 0.9, 0.95]
    })
    num_compromised_agents = 0
    font_size = 12
    
    try:
        plot_agent_integrity_comparison(attacked_df, num_compromised_agents, font_size)
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")

def test_large_font_size():
    import pandas as pd
    attacked_df = pd.DataFrame({
        "agent_id": [1, 2, 3],
        "agent_integrity_score": [0.8, 0.9, 0.95]
    })
    num_compromised_agents = 1
    font_size = 30
    
    try:
        plot_agent_integrity_comparison(attacked_df, num_compromised_agents, font_size)
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")