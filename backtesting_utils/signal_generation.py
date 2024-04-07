from itertools import product
import pandas as pd 
from random import sample
import numpy as np 


def crossed_above(df, column_a, column_b):
    """
    Create a column indicating where 'column_a' crossed above 'column_b', returning boolean values.

    Args:
    df (pd.DataFrame): DataFrame containing the data.
    column_a (str): Name of the first column.
    column_b (str): Name of the second column.

    Returns:
    pd.DataFrame: Original DataFrame with an additional column indicating "crossed above" events as booleans.
    """
    # Create a flag where True if 'column_a' is greater than 'column_b'
    is_above = df[column_a] > df[column_b]
    # Shift the flag by one to compare with previous row
    is_above_previous = is_above.shift(1, fill_value=False)
    # Determine if 'column_a' crossed above 'column_b'
    crossed_above = ~is_above_previous & is_above
    # Add a new column to indicate "crossed above" events
    new_column_name = f"{column_a}_crossed_above_{column_b}"
    df[new_column_name] = crossed_above

    return df

def crossed_below(df, column_a, column_b):
    """
    Create a column indicating where 'column_a' crossed below 'column_b', returning boolean values.

    Args:
    df (pd.DataFrame): DataFrame containing the data.
    column_a (str): Name of the first column.
    column_b (str): Name of the second column.

    Returns:
    pd.DataFrame: Original DataFrame with an additional column indicating "crossed below" events as booleans.
    """
    # Create a flag where True if 'column_a' is less than 'column_b'
    is_below = df[column_a] < df[column_b]
    # Shift the flag by one to compare with previous row
    is_below_previous = is_below.shift(1, fill_value=False)
    # Determine if 'column_a' crossed below 'column_b'
    crossed_below = ~is_below_previous & is_below
    # Add a new column to indicate "crossed below" events
    new_column_name = f"{column_a}_crossed_below_{column_b}"
    df[new_column_name] = crossed_below

    return df


def generate_conditions_target(df, threshold_cols, target_col):
    conditions = {}
    for th_col in threshold_cols:
        # Greater than conditions
        conditions[f"{th_col} > {target_col}"] = (lambda x, th_col=th_col: x[th_col] > x[target_col])

        # Equal to conditions
        conditions[f"{th_col} == {target_col}"] = (lambda x, th_col=th_col: x[th_col] == x[target_col])

        # Less than conditions
        conditions[f"{th_col} < {target_col}"] = (lambda x, th_col=th_col: x[th_col] < x[target_col])

    return conditions





def generate_conditions_threshold(df, threshold_cols1, threshold_cols2, target_col):
    conditions = {}
    seen_pairs = set()  # To keep track of seen combinations to ensure uniqueness

    for th_col1, th_col2 in product(threshold_cols1, threshold_cols2):
        # Check if the combination is unique
        if th_col1 != th_col2 and (th_col1, th_col2) not in seen_pairs and (th_col2, th_col1) not in seen_pairs:
            seen_pairs.add((th_col1, th_col2))  # Mark this pair as seen

            # Greater than conditions
            condition_gt = f"{th_col1} > {th_col2}"
            conditions[condition_gt] = (lambda x, col1=th_col1, col2=th_col2: x[col1] > x[col2])

            # Equal to conditions
            condition_eq = f"{th_col1} == {th_col2}"
            conditions[condition_eq] = (lambda x, col1=th_col1, col2=th_col2: x[col1] == x[col2])

            # Less than conditions
            condition_lt = f"{th_col1} < {th_col2}"
            conditions[condition_lt] = (lambda x, col1=th_col1, col2=th_col2: x[col1] < x[col2])

    return conditions


def stack_signals(df, total_signals):
    # Initialize an empty DataFrame to store the result
    result_df = pd.DataFrame()

    # List to store all possible combinations
    all_combinations = []

    # Maximum length for k-mer combinations
    max_k = len(df.columns)

    # Generate all possible combinations for lengths 2 to max_k
    for k in range(2, max_k + 1):
        # Extend the list with all combinations of current length k
        all_combinations.extend(itertools.combinations(df.columns, k))
    
    # If the total requested signals is more than the available combinations,
    # use the total available combinations instead
    total_signals = min(total_signals, len(all_combinations))

    # Randomly sample the specified number of combinations
    selected_combinations = sample(all_combinations, total_signals)

    for combo in selected_combinations:
        # Generate a new column name by combining names from the selected combination
        new_col_name = '_'.join(combo)
        # Initialize the result column with the first column's data
        result_column = df[combo[0]]
        # Iterate over the remaining columns in the combination and perform bitwise AND
        for col_name in combo[1:]:
            result_column = result_column & df[col_name]
        # Assign the result to a new column in the result DataFrame
        result_df[new_col_name] = result_column

    return result_df