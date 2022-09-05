# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 16:37:17 2022

@author: Enor
"""

import pandas as pd
from glob import glob
import matplotlib.pyplot as plt



#資料合併的前綴
files = glob('datasets/copData/2020copData*.csv')
print("資料合併中....")
df = pd.concat(
    (pd.read_csv(file, usecols=['time','COP','operation_num','running_time'], dtype={ 'time': str, 'COP':str ,'operation_num':str ,'running_time':str }) for file in files), ignore_index=True)
print("存檔中....")
df.to_csv('datasets/mergeCSV/2020mergeCOP.csv',encoding='utf-8')
#print(df)
print("畫圖中....")

time = len(df.COP)
time_list = []
count = -1

cop = list(df.COP)

print(time)
while time:
    time_list.insert(count, count)
    pass

fig1 = plt.figure(figsize=(10,5),dpi=200)       
plt.title("COP Data") # title
plt.ylabel("COP") # y label
plt.xlabel("Time 3 min/number") # x label
plt.plot(time_list,cop)#(x,y)
plt.ylim([0, 5])
plt.savefig("2020DataMerge.png")
