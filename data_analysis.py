"""
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Script Name: data_analysis.py
    Author: Oisin Biswas
    Email: oisin-biswas@idexx.com
    Description: This script runs an imagej macro to analyze images and then subsequently ingest that light intensity data to csv format for peak detection and light intensity analysis.
    Version: 1.0.0
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""


from scipy.signal import find_peaks
import pandas as pd 
import matplotlib.pyplot as plt
import os 
import subprocess

imagej_path = r'C:/Program Files (x86)/Fiji.app/ImageJ-win64.exe'
macro_path = r'path/to/macro'

command = [
    imagej_path,
    '--run', macro_path
]

subprocess.run(command)


input = r"path/to/macro/output"
output = r'path/to/desired/output'

def data_analysis(prom_val):
    for root, dirs, files in os.walk(input, topdown=False):
        for i in files:
            file_loc = root + "\\" + i
            df = pd.read_csv(file_loc)
            print(df)
            x = (df.iloc[:,1])
            peaks,_ = find_peaks(x, prominence= prom_val)
            plt.plot(x)
            plt.ylim([0,100])
            plt.plot(peaks, x[peaks], "x")
            # plt.show()
            data = {peaks.size}
            df2 = pd.DataFrame(data, columns=["Number of Peaks"])
            df.to_csv(output + "\\" + i + "_light_intensity_data" + ".csv")
            df2.to_csv(output + "\\" + i + "_num_peaks" + ".csv")
data_analysis(10)
