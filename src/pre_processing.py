import pandas as pd
import numpy as np

def history_preprocessing(df, remove_action_types):
    # Create features
    df['Time'] = pd.to_datetime(df['Time'],
                                format = "ISO8601")
    
    df['action_binary'] = np.where(df['Action'].isin(['Market buy', 'Limit buy']), 'buy',
                                   np.where(df['Action'].isin(['Market sell', 'Limit sell']), 'sell',
                                            'Unknown action') )
    

    df = df[~df['Action'].isin(remove_action_types)]

    return df.sort_values('Time').reset_index(drop = True)
