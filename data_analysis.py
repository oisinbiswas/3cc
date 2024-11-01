import cv2 as cv
import scipy as sp
from scipy.signal import find_peaks
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np 
import os 



input = r'enter\path\to\macro_output'
output = r'enter\path\to\\py_output'

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
        data = {peaks.size}
        df2 = pd.DataFrame(data, columns=["Number of Peaks"])
        print(df2)
        df.to_csv(output + "\\" + i + "_light_intensity_data" + ".csv")
        df2.to_csv(output + "\\" + i + "_num_peaks" + ".csv")
        