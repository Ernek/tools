import pandas as pd 
import numpy as np 
import sys, os 
import csv
import matplotlib.pyplot as plt
from sklearn.decomposition import dict_learning_online



def read_energy_file(energy_file):
    df_ener = pd.read_csv(energy_file, sep='\s+', header=None)
    df_ener.drop(df_ener.columns[[0,2,3]], axis=1, inplace=True)
    column_labels = ['State', 'Energy']
    df_ener.columns = column_labels
    #df_ener['DeltaE_meV'] = (df_ener['Energy'] - df_ener['Energy'][0])*27.21*1000

    return df_ener

def read_osct_file(osct_file, energy_file, nstates,nstate_to_keep):
    df_osct = pd.read_csv(osct_file, sep='\s+', header=None)
    df_osct.drop(df_osct.columns[[0,1,2,3,5,7]], axis=1, inplace=True)
    df_osct.columns = ['State', 'Excited State', 'Oscillator Strength']
    df_ener = read_energy_file(energy_file) 
    dict_gs_total = {}
    for i in range(1,nstates+1):
        df_osct_state = df_osct[df_osct['State'] == i].reset_index(drop=True)
        df_ener['DeltaE_meV'] = (df_ener['Energy'][i-1:] - df_ener['Energy'][i-1])*27.21*1000
        df_osct_state['Exc Energy'] = df_ener['DeltaE_meV'][i-1:].reset_index(drop=True) 
        dict_gs_total[f"{str(i)}"] = df_osct_state

    if nstate_to_keep:
        keys_to_check = [number for number in range(nstates - nstate_to_keep + 1, nstates + 1)]
        # { f"{x}": dict_gs_total[f"{x}"] for x in keys_to_check} generates a dictionary only keeping the key, value pairs of in keys_to_check : last 'nstate_to_keep' states 
        df_gs_total = pd.concat( { f"{x}": dict_gs_total[f"{x}"] for x in keys_to_check} )
    else: 
        df_gs_total = pd.concat(dict_gs_total).reset_index(drop=True)
    
    return df_osct, df_gs_total     

def save_energ_osct_data_to_file(osct_file, energy_file, base_output_name, nstates, nstate_to_keep):
    df_osct, df_gs_total = read_osct_file(osct_file, energy_file, nstates, nstate_to_keep)
    df_gs_total[['State', 'Exc Energy','Oscillator Strength']].to_csv(f'data_to_plot_{base_output_name}.txt', sep=' ', header=False, index=False)
    #df_gs_total[['State', 'Exc Energy','Oscillator Strength']].to_csv(f'data_to_plot_{base_output_name}.csv', sep=' ', header=False, index=False)

if __name__ == '__main__':
    #Criteria to decide whether two energies are or not degenerate 
    delta_e_threshold = 1/(27.21*1000)  # Threshold is 1 meV in hartree ( 1au => 27.21*1000 meV) 


    osct_file = sys.argv[1]  # grep ' f=' Output from gaussian
    energy_file = sys.argv[2]  # grep 'Energy (' Output from gaussian'
    base_output_name = sys.argv[3]
    nstates = int(sys.argv[4])
    nstate_to_keep = int(sys.argv[5])
    #df_osct , df_gs_total = read_osct_file(osct_file,energy_file,2)
    #print(df_gs_total)

    save_energ_osct_data_to_file(osct_file, energy_file, base_output_name, nstates, nstate_to_keep)