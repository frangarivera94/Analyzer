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