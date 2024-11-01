import cv2 as cv
import scipy as sp
from scipy.signal import find_peaks
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np 
import os 



input = r'C:\Users\obiswas\OneDrive - IDEXX\OneDrive\3qc\transition_output'
output = r'C:\Users\obiswas\OneDrive - IDEXX\OneDrive\3qc\transition_csv'

for root, dirs, files in os.walk(input, topdown=False):
    for i in files:
        file_loc = root + "\\" + i
        df = pd.read_csv(file_loc)
        x = (df.iloc[:,1])
        peaks,_ = find_peaks(x, prominence= 10)
        plt.plot(x)
        plt.ylim([0,100])
        plt.plot(peaks, x[peaks], "x")
        # plt.show()
        # print(peaks.size, i)
        # print(df, i)
        #TODO - create dataframe with 2 columns, file name and num_peaks, export to csv after analysis 
        data = {peaks.size}
        df2 = pd.DataFrame(data, columns=["Number of Peaks"])
        print(df2)
        # df2 = peaks.size
        # print(df, i)
        df.to_csv(output + "\\" + i + ".csv")
        df2.to_csv(output + "\\" + i + "num_peaks" + ".csv")
        #TODO if the average intensity is above or below, if the number of peaks is above or below, then classify 
        