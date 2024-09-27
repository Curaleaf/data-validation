import pandas as pd
import numpy as np

def compare_numeric_cols(df_1: pd.DataFrame, df_2: pd.DataFrame):
    """
    Used to get the count/mean/min/max of two dataframes with the 
    same column names and will compare their values side-by-side.
    
    Columns MUST be the exact same name.
    Args:
        df_1 (dataframe) : first table to compare (must share the same exact col names)
        df_2 (dataframe) : second table to compare (must share the same exact col names)
    Returns:
        df : comparison table
    """
    stats_df_1 = df_1.describe().T[['count', 'mean', 'min', 'max']]
    stats_df_2 = df_2.describe().T[['count', 'mean', 'min', 'max']]

    stats_df_1 = stats_df_1.rename(columns={
        'count': 'count_1',
        'mean': 'mean_1',
        'min': 'min_1',
        'max': 'max_1'
    })

    stats_df_2 = stats_df_2.rename(columns={
        'count': 'count_2',
        'mean': 'mean_2',
        'min': 'min_2',
        'max': 'max_2'
    })

    comparison_df = pd.concat([stats_df_1, stats_df_2], axis=1)


    comparison_df = comparison_df[['count_1', 'count_2', 'mean_1', 'mean_2', 
                                'min_1', 'min_2', 'max_1', 'max_2']]

    return comparison_df

def compare_categorical_cols(df_1: pd.DataFrame, df_2: pd.DataFrame):
    """
    Performs categorical comparisons between two dataframes. Columns MUST be the exact same name.

    Calculates the average frequency ratio and frequency differences of categorical values
    between the dataframes.
        - Avg Frequency ratio: the closer to 1, the closer the match
        - Frequency Differences : the closer percent diff is to 0, the closer the match
        
    Args:
        df_1 (dataframe) : first table to compare (must share the same exact col names)
        df_2 (dataframe) : second table to compare (must share the same exact col names)
    Returns:
        tuple : avg_frequency_ratio, frequency_differences
    """
    avg_frequency_ratio = {}
    frequency_differences = {}

    cols = [col for col in df_1.select_dtypes(exclude=np.number).columns if col in df_2.columns]

    for col in cols:
        # Calculate frequency ratios
        frequency_ratio = (
            df_1[col].value_counts().sort_index()
            / df_2[col].value_counts().sort_index()
        ).mean()
        avg_frequency_ratio[col] = frequency_ratio

        # Calculate frequency differences
        frequency_diff = pd.DataFrame(df_1[col].value_counts()).merge(
            pd.DataFrame(df_2[col].value_counts()),
            left_index=True,
            right_index=True,
            suffixes=("_df1", "_df2"),
        )
        frequency_diff.columns = ['count_df1', 'count_df2']

        frequency_diff["absolute_difference"] = abs(
            frequency_diff["count_df1"] - frequency_diff["count_df2"]
        )
        frequency_diff["percent_difference"] = (
            frequency_diff["absolute_difference"]
            / (frequency_diff["count_df1"] + frequency_diff["count_df2"])
        ) * 100

        # Calculate percent of total
        total_count_df1 = frequency_diff["count_df1"].sum()
        total_count_df2 = frequency_diff["count_df2"].sum()
        frequency_diff["percent_total_df1"] = (
            frequency_diff["count_df1"] / total_count_df1
        ) * 100
        frequency_diff["percent_total_df2"] = (
            frequency_diff["count_df2"] / total_count_df2
        ) * 100

        frequency_differences[col] = frequency_diff
    
    return avg_frequency_ratio, frequency_differences