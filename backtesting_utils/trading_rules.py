
def calculate_bollingers(df, column_name, window,suffix=None):
    # Calculate the Exponential Weighted Moving Average (EWMA)
    ewm = df[column_name].ewm(span=window, adjust=False).mean()

    # Calculate the standard deviation of the data for the same window
    std = df[column_name].ewm(span=window, adjust=False).std()

    # Calculate Bollinger Bands for 1.5, 2, and 2.5 standard deviations from the EWMA
    for multiplier in [1.5, 2, 2.5]:
        upper_band = ewm + (std * multiplier)
        lower_band = ewm - (std * multiplier)

        if suffix is not None:
                  df[f'{window}_{column_name}_BB_upper_{multiplier}_{suffix}'] = upper_band
                  df[f'{window}_{column_name}_BB_lower_{multiplier}_{suffix}'] = lower_band

        else:

                  df[f'{window}_{column_name}_BB_upper_{multiplier}'] = upper_band
                  df[f'{window}_{column_name}_BB_lower_{multiplier}'] = lower_band

        # Add the Bollinger Bands to the DataFrame


    # Optionally, return the DataFrame if needed
    return df