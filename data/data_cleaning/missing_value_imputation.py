import pandas as pd
import numpy as np

def impute_missing_values(df, column_name, method='mean'):
    '''
    Impute missing values in a pandas DataFrame for a given column
    
    df: pandas DataFrame
    column_name: string, name of the column to impute missing values in
    method: string, method for imputing missing values (default is 'mean')
            Other options: 'median', 'mode', 'ffill', 'bfill'
    '''
    if method == 'mean':
        df[column_name].fillna(df[column_name].mean(), inplace=True)
    elif method == 'median':
        df[column_name].fillna(df[column_name].median(), inplace=True)
    elif method == 'mode':
        df[column_name].fillna(df[column_name].mode()[0], inplace=True)
    elif method == 'ffill':
        df[column_name].fillna(method='ffill', inplace=True)
    elif method == 'bfill':
        df[column_name].fillna(method='bfill', inplace=True)
    else:
        print('Invalid imputation method')
    return df
