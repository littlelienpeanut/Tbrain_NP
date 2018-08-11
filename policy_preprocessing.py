### policy ###

import pandas as pd
import numpy as np
import csv

def load_claim(fname):
    df = pd.read_csv(fname, low_memory=False)
    ig_column = ['Vehicle_identifier', 'Coverage_Deductible_if_applied']
    one_hot_column = ['Main_Insurance_Coverage_Group', 'Insurance_Coverage', 'fassured', 'fsex', 'fmarriage', 'aassured_zip']

    for name in ig_column:
        df = df.drop(name, axis=1)

    for name in one_hot_column:
        tmp = pd.get_dummies(df[name], prefix = name)
        df = df.drop(name, axis=1)
        df = df.join(tmp)

    return df

fname = 'policy_p.csv'
print('data-preprocessing now')
df = load_claim(fname)
df.to_csv('policy_onehot.csv', index = False)
