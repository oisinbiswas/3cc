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
import numpy as np

# Define paths
IMAGEJ_PATH = r'C:/Program Files (x86)/Fiji.app/ImageJ-win64.exe'
MACRO_PATH = r'C:\Users\path\to\3cc_macro.ijm'
INPUT_DIR = r"C:\Users\path\to\macro_output"
OUTPUT_DIR = r"C:\Users\path\to\analysis_output"

# Run ImageJ macro
def run_imagej_macro():
    command = [IMAGEJ_PATH, '--run', MACRO_PATH]
    subprocess.run(command)

# Determine dynamic prominence threshold
def determine_prominence(intensity_values):
    std_dev = np.std(intensity_values)
    dynamic_prominence = std_dev * 1.5  
    return max(dynamic_prominence, 10)  

# Analyze file
def analyze_file(file_path, prom_val=None):
    df = pd.read_csv(file_path)
    intensity_values = df.iloc[:, 1]  

    mean_intensity = np.mean(intensity_values)
    std_dev_intensity = np.std(intensity_values)
    median_intensity = np.median(intensity_values)

    if prom_val is None:
        prom_val = determine_prominence(intensity_values)

    peaks, _ = find_peaks(intensity_values, prominence=prom_val)

    # Clean file name by removing ".jpg.csv"
    file_name = os.path.basename(file_path).replace(".jpg.csv", "")

    return {
        "File": file_name,
        "Number of Peaks": len(peaks),
        "Mean": round(mean_intensity, 2),
        "Median": round(median_intensity, 2),
        "Standard Deviation": round(std_dev_intensity, 2),
        "Prominence Used": round(prom_val, 2)
    }, intensity_values, peaks

# Process all files and add text info to each graph
def process_all_files(prom_val=None):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    file_list = [os.path.join(root, file_name) for root, _, files in os.walk(INPUT_DIR, topdown=False) for file_name in files]

    if not file_list:
        print("No files found in the input directory.")
        return

    for file_path in file_list:
        summary, intensity_values, peaks = analyze_file(file_path, prom_val)

        # Create a figure
        fig, ax = plt.subplots(figsize=(10, 5))

        # Plot the intensity data and detected peaks
        ax.plot(intensity_values, label="Light Intensity")
        ax.plot(peaks, intensity_values[peaks], "x", label="Detected Peaks", color='red')
        ax.set_ylim([0, 255])
        ax.legend()
        ax.set_title(f"{summary['File']}")  # Display cleaned file name

        # Adjust text box position further to the right
        text_x = len(intensity_values) + 75  # Increase offset for better spacing
        text_y_start = 200  # Starting y position for text
        line_spacing = 15  # Spacing between lines

        stats_text = (
            f"File: {summary['File']}\n"
            f"Number of Peaks: {summary['Number of Peaks']}\n"
            f"Mean: {summary['Mean']}\n"
            f"Median: {summary['Median']}\n"
            f"Std Dev: {summary['Standard Deviation']}\n"
            f"Prominence Used: {summary['Prominence Used']}"
        )

        # Place the text box to the right of the graph
        ax.text(text_x, text_y_start, stats_text, fontsize=10, verticalalignment="top",
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='black'))

        # Adjust the x-limits to make space for the text
        ax.set_xlim([0, len(intensity_values) + 100])  # Increased to avoid cutting off text

        plt.show()

# Run the pipeline
if __name__ == "__main__":
    run_imagej_macro()
    process_all_files(prom_val=None)  