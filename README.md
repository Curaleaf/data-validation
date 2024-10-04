# Data Diff Validation

## Purpose:
- This Python package is a utility that abstracts and streamlines the work of calculating general data diffs between development and production tables
- A lot of the adhod code to run comparisons between two tables is repetitive and time consuming and these functions provide an easy way to compare both categorical and numeric columns

## Installation in Hex
#### 1. `pip install` straight from GitHub 
```
!pip install git+https://github.com/Curaleaf/data-validation.git

from data_validation import compare_categorical_cols, compare_numeric_cols, compare_shapes
```

#### 2. Install package within Hex
![image](https://github.com/user-attachments/assets/603e8d10-28d2-4d14-bd73-c7e61b52a103)

1. Import the package to the workspace via UI under the Environments tab (integration was already done between GitHub/Hex)
    - [Hex docs on Git Package Installation](https://learn.hex.tech/docs/explore-data/projects/environment-configuration/using-packages#git-packages) 
3. Run `from data_validation import compare_categorical_cols, compare_numeric_cols, compare_shapes`
4. If the module cannot be found, explicitly add the Python path to the workspace by running:

 ```
import sys, os
sys.path.append(os.path.abspath('Curaleaf-data_validation/src/'))
 ```
4. Re-run command from step #3


## Functions
1. `compare_shapes()`
```
compare_shapes(df_1: pd.DataFrame, df_2: pd.DataFrame):
    Prints the col and rows of both tables.
    Args:
        df_1 (dataframe) : first table to compare (must share the same exact col names)
        df_2 (dataframe) : second table to compare (must share the same exact col names)
    Returns:
        None
```

2. `compare_numeric_cols()`
```
compare_numeric_cols(df_1: pandas.core.frame.DataFrame, df_2: pandas.core.frame.DataFrame)
    Used to get the count/mean/min/max of two dataframes with the 
    same column names and will compare their values side-by-side.
    
    Columns MUST be the exact same name.
    Args:
        df_1 (dataframe) : first table to compare (must share the same exact col names)
        df_2 (dataframe) : second table to compare (must share the same exact col names)
    Returns:
        df : comparison table
```
3. `compare_categorical_cols()`
```
compare_categorical_cols(df_1: pandas.core.frame.DataFrame, df_2: pandas.core.frame.DataFrame)
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
```

## What will functions output?

If you are working on existing models and want to compare your changes in the development environment to that of the production environment, you can get metrics about the
1. Differences in shape for the two resulting tables
2. Side-by-side descriptive statistics of the two tables

![image](https://github.com/user-attachments/assets/3a5cc401-1d96-476b-8236-d55124e7c49b)

3. Average mean frequency ratio/frequency differences for each categorical column

![image](https://github.com/user-attachments/assets/13f0af24-3533-4077-8af2-48874b3aeb29)

![image](https://github.com/user-attachments/assets/c1cde009-c417-42e6-9f3f-d759dd51e5b8)


Note:
- Both tables should have the same exact structure and should ideally have correct type casting.

## What do the categorical comparison metrics mean?
- Average Frequency Ratio
  - Gets the __average frequency ratio__ of each unique categorical value in a column of one table and divides it by the same value of the second table
    - This metric shows how aligned the values / value counts of each categorical column is between the two tables
        - Captures frequency/ordinance and presence of distinct values
    - __The closer the mean frequency ratio is to 1, the better__
  - Outputs:
    - Prints our a dictionary object with each column name and its corresponding avg_frequency_ratio
- Frequency Difference
    - Gets the frequency difference stats of the actual values between development and production
        - This metric allows you to see in more detail how off or discrepant the two tables are
        - Gives counts, absolute differences, percent difference, percents of total
    - Outputs:
        - Returns a dictionary object that contains column names as keys and values as dataframes which contain the differnce metrics


## Example Usage
[AdHoc Data Diff Hex Notebook](https://app.hex.tech/ee7be01c-5b3b-4920-aeb2-5e155dd24840/hex/e666faad-715d-42ee-8f3d-5de4442d4364/draft/logic)
