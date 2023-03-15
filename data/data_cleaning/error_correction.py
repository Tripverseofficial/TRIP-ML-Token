import pandas as pd
import numpy as np

def correct_errors(df, column_name, old_value, new_value):
    '''
    Correct errors in a pandas DataFrame for a given column
    
    df: pandas DataFrame
    column_name: string, name of the column to correct errors in
    old_value: any data type, value to be replaced
    new_value: any data type, replacement value
    '''
    df[column_name].replace(old_value, new_value, inplace=True)
    return df
