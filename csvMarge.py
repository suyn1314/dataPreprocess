# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 16:37:17 2022

@author: Enor
"""

import pandas as pd
from glob import glob
import matplotlib.pyplot as plt
import statistics
from tsmoothie.smoother import LowessSmoother


#資料合併的前綴
files = glob('datasets/copData/2020copData*.csv')
print("資料合併中....")
df = pd.concat(
    (pd.read_csv(file, usecols=['time','COP','Month','operation_num','running_time'], dtype={ 'time': str, 'COP': float, 'Month':int ,'operation_num':str ,'running_time':str }) for file in files), ignore_index=True)
print("存檔中....")
df.to_csv('datasets/mergeCSV/2020mergeCOP.csv',encoding='utf-8')
#print(df)


#2020/1/10  12:01:12 PM
print("資料處理....")
cop = list(df.COP)
month = list (df.Month)
number_list = [*range(len(cop))]


print("畫圖中....")
fig1 = plt.figure(figsize=(20,5),dpi=500)
plt.ylim([0, 5])       
plt.title("COP 2020 Data") # title
plt.xlabel("number") # x label
plt.ylabel("COP Value") # y label
plt.plot(number_list,cop)#(x,y)
plt.savefig("2020DataMerge.png")





