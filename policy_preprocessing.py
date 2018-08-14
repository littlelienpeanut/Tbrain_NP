import pandas as pd
import csv

def acc(df):
    acc_cate = ['Premium']
    df_dict = {}
    update_cate = []
    cate = df.keys()
    for c in df.keys():
        if c.find('Insurance_Coverage') != -1 or c.find('Main_Insurance_Coverage_Group') != -1:
            update_cate.append(c)
    
    for i in range(len(df)):
        if i%100000 == 0:
            print(str(i) + '/' + str(len(df)))
        if df['Policy_Number'][i] in df_dict:
            for c in acc_cate:
                df_dict[df['Policy_Number'][i]][c] += df[c][i]
            for c in update_cate:
                if df[c][i] == 1:
                    df_dict[df['Policy_Number'][i]][c] = 1
                
        
        else:
            df_dict.update({df['Policy_Number'][i]:{}})
            for c in cate:
                df_dict[df['Policy_Number'][i]].update({c:df[c][i]})

    
    return df_dict

df = pd.read_csv('Lien_dataset/policy_v2.csv', low_memory=False)
df = acc(df)

print('writting csv')

new_fname = 'policy_0702_v3.csv'
with open('Lien_dataset/' + new_fname, 'w', newline = '', encoding='utf-8') as fout:
        wr = csv.writer(fout)
        title = []
        for key in df['79110176bf64b5094c19aad785aeac56e36cb609']:
            title.append(key)

        wr.writerow(title)

        for pn in df.keys():
            value = []
            for cate in title:
                value.append(df[pn][cate])

            wr.writerow(value)
