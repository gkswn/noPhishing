import pandas as pd

def dataload():

    train_df = pd.read_csv('./data/vfdata.csv')

    train_X = train_df['txt']
    train_y  = train_df['label']

    return train_X, train_y