import numpy as np
import pandas as pd
import re

df_bilboard = pd.read_csv("test.csv", sep=",")

df_b_cleared = df_bilboard.fillna("")

# print(df_b_cleared.head())

for i in range(len(df_b_cleared['artist'])):
    df_b_cleared['artist'][i] = re.sub(r"Featuring ", "",df_b_cleared['artist'][i])
    df_b_cleared['artist'][i] = re.sub(r"(\w*[!@#$%^&*]+\w*)", "",df_b_cleared['artist'][i])
    df_b_cleared['title'][i] = re.sub(r"(\w*[!@#$%^&*]+\w*)", "",df_b_cleared['title'][i])

print(df_b_cleared['title'][4857]) 



df_b_cleared.to_csv('out.csv',index=False)