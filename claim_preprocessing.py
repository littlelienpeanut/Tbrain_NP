### claim ###

import pandas as pd
import numpy as np
import csv

def load_claim(fname):
    df = pd.read_csv('Lien_dataset/' + fname, low_memory=False)
    ig_column = ['Vehicle_identifier']
    one_hot_column = ['Accident_Time', "Driver's_Gender", 'Coverage',"Driver's_Relationship_with_Insured", 'Marital_Status_of_Driver', 'Cause_of_Loss', 'Accident_area']
    df = AT_onehot(df)
    df = bday2age(df)
    
    for name in ig_column:
        df = df.drop(name, axis=1)

    for name in one_hot_column:
        tmp = pd.get_dummies(df[name], prefix = name)
        df = df.drop(name, axis=1)
        df = df.join(tmp)

    return df

def acc(df):
    acc_cate = ['Paid_Loss_Amount', 'paid_Expenses_Amount', 'Salvage_or_Subrogation?', 'Deductible']
    df_dict = {}
    cate = df.keys()
    for i in range(len(df)):
        if df['Policy_Number'][i] in df_dict:
            for c in acc_cate:
                df_dict[df['Policy_Number'][i]][c] += df[c][i]
            for c in cate:
                if c.find('Coverage') != -1:
                    if df[c][i] == 1:
                        df_dict[df['Policy_Number'][i]][c] = 1
        
        else:
            df_dict.update({df['Policy_Number'][i]:{}})
            for c in cate:
                df_dict[df['Policy_Number'][i]].update({c:df[c][i]})

    
    return df_dict

def AT_onehot(df):
    df['Accident_Time'] = list(map(lambda x: str(x)[:2], df['Accident_Time']))
    return df

def bday2age(df):
    df['DOB_of_Driver'] = list(map(lambda x: 2017 - int(str(x)[-4:]), df['DOB_of_Driver']))
    return df

    

fname = 'claim_0702.csv'
print('data-preprocessing now')
df = load_claim(fname)
df = acc(df)
print('done!')
print('writting csv')
new_fname = 'claim_0702_v3.csv'
with open('Lien_dataset/' + new_fname, 'w', newline = '') as fout:
        wr = csv.writer(fout)
        title = []
        for key in df['91dc13e4e24dc9e0e0940c63924109e4ff66e18a']:
            title.append(key)

        wr.writerow(title)

        for pn in df.keys():
            value = []
            for cate in title:
                value.append(df[pn][cate])

            wr.writerow(value)



