from curses import def_prog_mode
import pandas as pd 
import numpy as np 
import sys, os 
import csv
import matplotlib.pyplot as plt


energy_file = sys.argv[1]  # grep 'Energy (' Output from gaussian'
oscstr_file = sys.argv[2]  # grep ' f=' Output from gaussian
base_output_name = sys.argv[3]


df_ener = pd.read_csv(energy_file, sep='\s+', header=None)
print('columns ', df_ener.columns)
df_ener.drop(df_ener.columns[[0,2,3]], axis=1, inplace=True)
column_labels = ['State', 'Energy']
df_ener.columns = column_labels
print('energy dataframe: ', df_ener.iloc[-1])

df_ener['DeltaE_meV'] = (df_ener['Energy'] - df_ener['Energy'][0])*27.21*1000

print(df_ener['DeltaE_meV'].iloc[-1])


df_osct = pd.read_csv(oscstr_file, sep='\s+', header=None)
#print(df_osct.head())
df_osct.drop(df_osct.columns[[0,1,2,3,5,7]], axis=1, inplace=True)
df_osct.columns = ['State', 'Excited State', 'Oscillator Strength']

print(df_osct[df_osct['State'] == 1].iloc[-1])

#df_total = df_ener.merge(df_osct, on='State')
#print(df_total[df_total['State']==2])

#df_ground = df_total[df_total['State'].isin([1 ,2])]
#df_total.groupby(by='DeltaE_meV')
#print(df_ener)
df_osct_gs1 = df_osct[df_osct['State'] == 1]
#print(df_ener['DeltaE_meV'][1:].reset_index(drop=True))
df_osct_gs1['Exc Energy'] = df_ener['DeltaE_meV'][1:].reset_index(drop=True)

print(df_osct_gs1.head())
print(df_ener)

df_osct_gs2 = df_osct[df_osct['State'] == 2].reset_index(drop=True)
print(df_osct_gs2)  
print(df_ener)
print(df_ener['DeltaE_meV'][2:].reset_index(drop=True))
#print(df_enerd()['DeltaE_meV'][1:].reset_index(drop=True))
df_osct_gs2['Exc Energy'] = df_ener['DeltaE_meV'][2:].reset_index(drop=True)

print(df_osct_gs2.head())

df_gs_total = pd.concat([df_osct_gs1, df_osct_gs2]).reset_index(drop=True)
print(df_gs_total.iloc[90:120])
print(df_gs_total[['State', 'Exc Energy','Oscillator Strength']])
print(df_gs_total.dtypes)

df_gs_total[['State', 'Exc Energy','Oscillator Strength']].to_csv(f'data_to_plot_{base_output_name}.txt', sep=' ', header=False, index=False)
df_gs_total[['State', 'Exc Energy','Oscillator Strength']].to_csv(f'data_to_plot_{base_output_name}.csv', sep=' ', header=False, index=False)

