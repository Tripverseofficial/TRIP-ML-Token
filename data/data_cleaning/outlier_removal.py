import pandas as pd
import numpy as np

def remove_outliers(df, column_name, threshold=3):
    '''
    Remove outliers from a pandas DataFrame for a given column
    
    df: pandas DataFrame
    column_name: string, name of the column to remove outliers from
    threshold: integer, number of standard deviations from the mean above which to consider a value an outlier
    '''
    mean = df[column_name].mean()
    std = df[column_name].std()
    lower_bound = mean - threshold * std
    upper_bound = mean + threshold * std
    df = df[(df[column_name] >= lower_bound) & (df[column_name] <= upper_bound)]
    return df
