# data_processing.py

import pandas as pd

def load_data(file_paths):
    elementos_data = []
    aseos_data = []

    for file_path in file_paths:
        if 'elementos' in file_path.lower():
            df = pd.read_excel(file_path)
            elementos_data.append(df)
        elif 'aseos' in file_path.lower():
            df = pd.read_excel(file_path)
            aseos_data.append(df)

    elementos_df = pd.concat(elementos_data, ignore_index=True)
    aseos_df = pd.concat(aseos_data, ignore_index=True)

    # Select only the numeric columns for mean cleanliness calculation
    elementos_numeric_columns = elementos_df.select_dtypes(include='number').columns
    aseos_numeric_columns = aseos_df.select_dtypes(include='number').columns

    # Replace negative values with NaN using DataFrame.apply
    elementos_df[elementos_numeric_columns] = elementos_df[elementos_numeric_columns].apply(
        lambda col: col.where(col >= 0)
    )
    aseos_df[aseos_numeric_columns] = aseos_df[aseos_numeric_columns].apply(
        lambda col: col.where(col >= 0)
    )

    # Create the mean cleanliness column for both DataFrames
    elementos_df['mean_cleanliness'] = elementos_df[elementos_numeric_columns].mean(axis=1, skipna=True)
    aseos_df['mean_cleanliness'] = aseos_df[aseos_numeric_columns].mean(axis=1, skipna=True)

    return elementos_df, aseos_df


import logging

def get_min_max_dates(elementos_df, aseos_df):
    # Convert 'FECHAHORA' columns to datetime, coercing errors to NaT
    elementos_df['FECHAHORA'] = pd.to_datetime(elementos_df['FECHAHORA'], errors='coerce')
    aseos_df['FECHAHORA'] = pd.to_datetime(aseos_df['FECHAHORA'], errors='coerce')

    # Drop rows with NaT in 'FECHAHORA'
    elementos_df = elementos_df.dropna(subset=['FECHAHORA'])
    aseos_df = aseos_df.dropna(subset=['FECHAHORA'])

    # Get the min and max dates across both dataframes
    min_date = min(elementos_df['FECHAHORA'].min(), aseos_df['FECHAHORA'].min())
    max_date = max(elementos_df['FECHAHORA'].max(), aseos_df['FECHAHORA'].max())

    # Log the min and max dates before returning
    logging.info(f"Calculated min_date: {min_date}")
    logging.info(f"Calculated max_date: {max_date}")

    return min_date.strftime('%Y-%m-%d'), max_date.strftime('%Y-%m-%d')

