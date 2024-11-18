# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 13:01:37 2024

@author: ros
"""

import argparse
import chardet
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

#%% User input
def ramberg_osgood_evaluation(config_file_path):
    # Load JSON data
    with open(config_file_path, 'r') as file:
        config = json.load(file)
    
    l0 = config["l0"]
    d1, d2, d3 = config["d1"], config["d2"], config["d3"]
    skip_rows = config["skip_rows"]
    max_strain = config["max_strain"]
    youngs_modulus = config["youngs_modulus"]
    eval_block = config["eval_block"]
    path = config["txt_path"]
    print(path)
    
    #%% File processing
    # Read the file in binary mode
    with open(path, 'rb') as file:
        raw_data = file.read(10000)  # Read a portion of the file
        result = chardet.detect(raw_data)  # Detect encoding
        encoding = result["encoding"]
        # print(result)
    
    test_df = pd.read_csv(path, 
                          sep="\t", header=None,
                          names=["zeit", "kraft", "ext_ist", "mweg", "ext_soll", "td-soll", "zyklen"], 
                          skiprows=17,
                          encoding=encoding)
    
    folder = os.path.dirname(path)
    basename = os.path.splitext(os.path.basename(path))[0]
    
    d = (d1 + d2 + d3) / 3
    area = np.pi*d**2/4
    
    first_block_df = test_df.loc[test_df["zyklen"]==1]
    eval_block_df = test_df.loc[test_df["zyklen"]==eval_block]
    
    # Access the first time value
    error = first_block_df["ext_ist"][first_block_df["ext_ist"].index[0]]
    
    block_list = [1, eval_block]
    block_df_list = [first_block_df, eval_block_df]
    ramberg_osgood_data = {"block": [], "E": [], "n": [], "K": []}
    
    for i, df in enumerate(block_df_list):
        if (eval_block==1) and i>0:
            continue
        else:
            if i == 0:
                t0 = first_block_df["zeit"][first_block_df["zeit"].index[0]]
            else:
                t0 = eval_block_df["zeit"][eval_block_df["zeit"].index[0]]
    
            df["zeit_block"] = df["zeit"] - t0
            df["ext_ist_true"] = df["ext_ist"] - error
            df["ext_soll_true"] = df["ext_soll"] - error
            df["strain"] = df["ext_ist_true"] / l0
            df["true_strain"] = np.log((df["ext_ist_true"] + l0) / l0)
            df["stress"] = df["kraft"] * 1000 / area
            df["true_stress"] = df["stress"] * (1 + df["strain"])
            

            if i <= 1:
                # Assuming data_df has 'TRUE STRAIN', 'TRUE STRESS', and 'ZEIT_BLOCK'
                strain = df["true_strain"].values
                stress = df["true_stress"].values
                # time = df["zeit_block"].values
                
                # Step 1: Find zero-crossings in TRUE STRAIN to determine intervals
                # Zero-crossings occur where the strain sign changes
                zero_crossings = np.where(np.diff(np.sign(strain)))[0]
                
                # List to store turning points (maxima and minima)
                turning_points = []
                
                # Step 2: Iterate through each interval defined by zero-crossings
                for start, end in zip(zero_crossings[:-1], zero_crossings[1:]):
                    # Define the interval data
                    # interval_strain = strain[start:end+1]
                    interval_stress = stress[start:end+1]
                    # interval_time = time[start:end+1]
                    
                    # Find the local maximum and minimum within this interval
                    max_idx = start + np.argmax(interval_stress)  # Index of local maximum
                    min_idx = start + np.argmin(interval_stress)  # Index of local minimum
                    
                    # Append the maximum and minimum points
                    turning_points.extend([max_idx, min_idx])
                
                # Step 3: Extract turning points from the original data
                turning_points_df = df.iloc[sorted(set(turning_points))]
                ascending_turning_points_df = turning_points_df[turning_points_df["true_strain"]>0.0001]
                ascending_turning_points_df = ascending_turning_points_df.sort_values(by="true_strain").reset_index(drop=True)
                #%% Ramberg-Osgood
                true_strain = ascending_turning_points_df["true_strain"]
                true_stress = ascending_turning_points_df["true_stress"]
                
                true_elastic_strain = true_stress / youngs_modulus
                true_plastic_strain = true_strain - true_elastic_strain
                
                # Create a boolean mask for values where both true_elastic_strain and true_plastic_strain are non-negative
                mask = (true_elastic_strain >= 0) & (true_plastic_strain >= 0)
                # Apply the mask to filter out negative values in all arrays
                true_strain = true_strain[mask]
                true_stress = true_stress[mask]
                true_elastic_strain = true_elastic_strain[mask]
                true_plastic_strain = true_plastic_strain[mask]
                
                X = np.log10(np.array(true_stress).astype("float64"))
                Y = np.log10(np.array(true_plastic_strain).astype("float64"))
                XY = X * Y
                X2 = X**2
                
                N = len(X)
                sum_X = np.sum(X)
                sum_Y = np.sum(Y)
                sum_XY = np.sum(XY)
                sum_X2 = np.sum(X2)
                
                a1 = (N * sum_XY - sum_X * sum_Y) / (N * sum_X2 - sum_X * sum_X)
                a0 = 1 / N * (sum_Y - a1 * sum_X)
                
                n_ = 1 / a1
                K_ = 10**(-1 * n_ * a0)
                
                ramberg_osgood_stress = np.arange(0, 1000, 5)
                ramberg_osgood_strain = ramberg_osgood_stress / youngs_modulus + (ramberg_osgood_stress / K_)**(1 / n_)
                
                ramberg_osgood_data["block"].append(block_list[i])
                ramberg_osgood_data["E"].append(youngs_modulus)
                ramberg_osgood_data["n"].append(n_)
                ramberg_osgood_data["K"].append(K_)
                
                #%% plot results
                if i == 0:
                    IST = 1
                elif i == 1:
                    IST = eval_block
                # Define ticks and round up to next bigger dividable by 100
                eps_min = -max_strain / 100
                eps_max = max_strain / 100
                t_max = np.ceil(df["zeit_block"][df["zeit_block"].index[-1]] / 10) * 10
                if t_max > 600:
                    tckr = 120
                else:
                    tckr = 60
                f_min = np.floor(np.min(df["kraft"]) / 5) * 5
                f_max = np.ceil(np.max(df["kraft"]) / 5) * 5
                ext_min = np.floor(np.min(df["ext_soll_true"]) / 20) * 20
                ext_max = np.ceil(np.max(df["ext_soll_true"]) / 20) * 20
                min_stress = np.floor(np.min(df["true_stress"]) / 100) * 100
                max_stress = np.ceil(np.max(df["true_stress"]) / 100) * 100 
                
                fig, axs = plt.subplots(2, 2, figsize=(12, 9))
                       
                axs[0,0].plot(df["zeit_block"], df["kraft"], label=f"{basename}")
                axs[0,0].set(xlim=(0, t_max), xticks=np.arange(0, t_max+0.0001, tckr), xlabel=("$t_{block}$ [s]"),
                             ylim=(f_min, f_max), yticks=np.arange(f_min, f_max+0.0001, 5), ylabel=("Force [kN]"))
                axs[0,0].minorticks_on()  # Turn on minor ticks
                axs[0,0].xaxis.set_minor_locator(plt.MultipleLocator(10))  # Adjust x-axis minor ticks
                axs[0,0].yaxis.set_minor_locator(plt.MultipleLocator(1))      # Adjust y-axis minor ticks
                axs[0,0].legend(loc="upper left")
                
                axs[0,1].plot(df["zeit_block"], df["ext_ist_true"], label="$Δl_{ist}$", zorder=5)
                axs[0,1].plot(df["zeit_block"], df["ext_soll_true"], label="$Δl_{soll}$")
                axs[0,1].set(xlim=(0, t_max), xticks=np.arange(0, t_max+0.0001, tckr), xlabel=("$t_{block}$ [s]"),
                             ylim=(ext_min, ext_max), yticks=np.arange(ext_min, ext_max+0.0001, 20), ylabel=("Δl [µm]"))
                text = "$l_0$ = " + f"{l0} µm"
                axs[0,1].annotate(text, (10, ext_min+5))
                axs[0,1].minorticks_on()  # Turn on minor ticks
                axs[0,1].xaxis.set_minor_locator(plt.MultipleLocator(10))  # Adjust x-axis minor ticks
                axs[0,1].yaxis.set_minor_locator(plt.MultipleLocator(10))      # Adjust y-axis minor ticks
                axs[0,1].legend(loc="upper left")
                
                axs[1,0].plot(df["true_strain"], df["true_stress"], label=f"IST-block {IST}")
                axs[1,0].set(xlim=(eps_min-0.0005, eps_max+0.0005), xticks=np.arange(eps_min, eps_max+0.0000001, 0.005), xlabel=("True strain [-]"),
                             ylim=(min_stress-25, max_stress+25), yticks=np.arange(min_stress, max_stress+0.001, 100), ylabel=("True stress [MPa]"))
                axs[1,0].minorticks_on()  # Turn on minor ticks
                axs[1,0].xaxis.set_minor_locator(plt.MultipleLocator(0.001))  # Adjust x-axis minor ticks
                axs[1,0].yaxis.set_minor_locator(plt.MultipleLocator(50))      # Adjust y-axis minor ticks
                axs[1,0].legend(loc="upper left")
                
                axs[1,1].scatter(ascending_turning_points_df["true_strain"], ascending_turning_points_df["true_stress"], label = "Turning points")
                axs[1,1].plot(ramberg_osgood_strain, ramberg_osgood_stress, label="Ramberg-Osgood", color="r")
                axs[1,1].set(xlim=(0, eps_max), xticks=np.arange(0, eps_max+0.0025, 0.0025), xlabel=("True strain [-]"),
                             ylim=(0, max_stress), yticks=np.arange(0, max_stress+0.001, 100), ylabel=("True stress [MPa]"))
                text = "$ε = σ/E$ + $(σ/K')^{1/n'}$ \n" + f"$E={youngs_modulus}$ MPa \n$K'={np.round(K_,3)}$ MPa \n$n'={np.round(n_,3)}$"
                axs[1,1].annotate(text, (eps_max-eps_max/3, 10))
                axs[1,1].minorticks_on()  # Turn on minor ticks
                axs[1,1].xaxis.set_minor_locator(plt.MultipleLocator(0.0005))  # Adjust x-axis minor ticks
                axs[1,1].yaxis.set_minor_locator(plt.MultipleLocator(25))      # Adjust y-axis minor ticks
                axs[1,1].legend(loc="upper left")
                
                plt.savefig(f"{folder}/Evaluation_{basename}_block-{block_list[i]}.png")
                # plt.show(block=False)
        
    plt.show()
    # plt.pause(0.1)
    # Create a DataFrame and save to CSV
    ro_data_df = pd.DataFrame(ramberg_osgood_data)
    ro_data_df.to_csv(f"{folder}/Ramberg-Osgood_{basename}.csv", index=False)

if __name__ == "__main__":
    # Set up argparse to read command line arguments
    parser = argparse.ArgumentParser(description="Load parameters from a JSON file.")
    parser.add_argument("--config_path", type=str, default="H:\Privat\IST_config.json", help="Path to the JSON file")

    # Parse the arguments
    args = parser.parse_args()
    config_file_path=args.config_path
    ramberg_osgood_evaluation(config_file_path)
