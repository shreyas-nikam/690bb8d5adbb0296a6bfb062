import pytest
from definition_51c9c48039e34412b955fa6626bac174 import validate_and_summarize_data
import pandas as pd
import numpy as np

@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({
        'column1': [1, 2, 3],
        'column2': ['a', 'b', 'c'],
        'column3': pd.to_datetime(['2023-10-01', '2023-10-02', '2023-10-03'])
    })

def test_validate_and_summarize_data_columns(sample_dataframe):
    expected_columns = ['column1', 'column2', 'column3']
    validate_and_summarize_data(sample_dataframe, 'Test DataFrame', expected_columns, {}, [])

def test_validate_and_summarize_data_dtypes(sample_dataframe):
    expected_dtypes = {'column1': 'int64', 'column2': 'object', 'column3': 'datetime64[ns]'}
    validate_and_summarize_data(sample_dataframe, 'Test DataFrame', [], expected_dtypes, [])

def test_validate_and_summarize_data_no_nulls(sample_dataframe):
    critical_fields_no_null = ['column1', 'column2']
    validate_and_summarize_data(sample_dataframe, 'Test DataFrame', [], {}, critical_fields_no_null)

def test_validate_and_summarize_data_unique_key(sample_dataframe):
    unique_key = ['column3']
    validate_and_summarize_data(sample_dataframe, 'Test DataFrame', [], {}, [], unique_key)

def test_validate_and_summarize_data_invalid_columns(sample_dataframe):
    with pytest.raises(AssertionError):
        expected_columns = ['column1', 'column4']
        validate_and_summarize_data(sample_dataframe, 'Test DataFrame', expected_columns, {}, [])