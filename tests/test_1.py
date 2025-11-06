import pytest
import pandas as pd
import numpy as np
from definition_3e2d49ee2ee747eb8e910638929c7bd6 import validate_and_summarize_data

# --- Test Data Setup ---

# Test Case 1: All Valid Inputs (Happy Path)
# DataFrame is well-formed, all columns present, correct dtypes, no nulls in critical fields, unique key is unique.
df1 = pd.DataFrame({
    'col1': [1, 2, 3],
    'col2': [1.1, 2.2, 3.3],
    'col3': ['a', 'b', 'c']
})
expected_cols1 = ['col1', 'col2', 'col3']
expected_dtypes1 = {'col1': 'int64', 'col2': 'float64', 'col3': 'object'}
critical_fields1 = ['col1']
unique_key1 = ['col1']

# Test Case 2: Missing Column
# 'col3' is expected but missing from the DataFrame.
df2 = pd.DataFrame({
    'col1': [1, 2, 3],
    'col2': [1.1, 2.2, 3.3]
})
expected_cols2 = ['col1', 'col2', 'col3'] # 'col3' is explicitly expected
expected_dtypes2 = {'col1': 'int64', 'col2': 'float64'} # dtypes for existing columns
critical_fields2 = ['col1']
unique_key2 = ['col1']


# Test Case 3: Incorrect Data Type
# 'col2' in df3 is int, but expected_dtypes3 specifies float64.
df3 = pd.DataFrame({
    'col1': [1, 2, 3],
    'col2': [1, 2, 3], # int instead of float
    'col3': ['a', 'b', 'c']
})
expected_cols3 = ['col1', 'col2', 'col3']
expected_dtypes3 = {'col1': 'int64', 'col2': 'float64', 'col3': 'object'} # Expect float for col2
critical_fields3 = ['col1']
unique_key3 = ['col1']


# Test Case 4: Null in Critical Field
# 'col1' is a critical field and contains a NaN value.
df4 = pd.DataFrame({
    'col1': [1.0, np.nan, 3.0], # NaN in critical field, type is float
    'col2': [1.1, 2.2, 3.3],
    'col3': ['a', 'b', 'c']
})
expected_cols4 = ['col1', 'col2', 'col3']
expected_dtypes4 = {'col1': 'float64', 'col2': 'float64', 'col3': 'object'} # Expect float for col1
critical_fields4 = ['col1'] # col1 is critical and should not have nulls
unique_key4 = ['col1']


# Test Case 5: Invalid DataFrame Type (not a pandas DataFrame)
# The 'df' argument is a string, which is an invalid type.
df5 = "this is not a pandas DataFrame"
expected_cols5 = ['col1']
expected_dtypes5 = {'col1': 'int64'}
critical_fields5 = None
unique_key5 = None


# --- Parametrized Test Function ---

@pytest.mark.parametrize(
    "df, df_name, expected_columns, expected_dtypes, critical_fields_no_null, unique_key, expected_exception",
    [
        # Test Case 1: All Valid Inputs (Happy Path) - No exception expected
        (df1, "Test Data 1", expected_cols1, expected_dtypes1, critical_fields1, unique_key1, None),
        # Test Case 2: Missing Column - Expect AssertionError
        (df2, "Test Data 2", expected_cols2, expected_dtypes2, critical_fields2, unique_key2, AssertionError),
        # Test Case 3: Incorrect Data Type - Expect AssertionError
        (df3, "Test Data 3", expected_cols3, expected_dtypes3, critical_fields3, unique_key3, AssertionError),
        # Test Case 4: Null in Critical Field - Expect AssertionError
        (df4, "Test Data 4", expected_cols4, expected_dtypes4, critical_fields4, unique_key4, AssertionError),
        # Test Case 5: Invalid DF Type - Expect TypeError
        (df5, "Test Data 5", expected_cols5, expected_dtypes5, critical_fields5, unique_key5, TypeError),
    ]
)
def test_validate_and_summarize_data(df, df_name, expected_columns, expected_dtypes, critical_fields_no_null, unique_key, expected_exception):
    """
    Tests the validate_and_summarize_data function for various scenarios
    including happy path, missing columns, incorrect dtypes, nulls in critical fields,
    and invalid DataFrame input type.
    """
    try:
        # Call the function under test
        validate_and_summarize_data(df, df_name, expected_columns, expected_dtypes, critical_fields_no_null, unique_key)
        
        # If an exception was expected but not raised, fail the test
        if expected_exception is not None:
            pytest.fail(f"Expected {expected_exception.__name__} but no exception was raised.")
            
    except Exception as e:
        # If an unexpected exception was raised (when no exception was expected), fail the test
        if expected_exception is None:
            pytest.fail(f"Unexpected exception {type(e).__name__} raised: {e}")
        
        # Assert that the raised exception is of the expected type
        assert isinstance(e, expected_exception), f"Expected {expected_exception.__name__}, but got {type(e).__name__}"