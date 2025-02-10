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
MACRO_PATH = r"C:\Users\path\to\3cc_macro.ijm"
INPUT_DIR = r"C:\Users\path\to\macro_output"
OUTPUT_DIR = r"C:\Users\path\to\analysis_output"
SUMMARY_CSV_PATH = os.path.join(OUTPUT_DIR, "summary_statistics.csv")

# Run ImageJ macro in the background (hidden window)
def run_imagej_macro():
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW  # Hides the command prompt window
    command = [IMAGEJ_PATH, '--run', MACRO_PATH]
    subprocess.run(command, startupinfo=startupinfo, check=True)

# Determine dynamic prominence threshold
def determine_prominence(intensity_values):
    std_dev = np.std(intensity_values)
    return max(std_dev * 1.5, 10)

# Classify files based on given criteria
def classify_file(mean_intensity, std_dev_intensity, num_peaks):
    bad_criteria = sum([
        mean_intensity > 15,  
        std_dev_intensity > 5,
        num_peaks > 5
    ])

    if bad_criteria == 0:
        return "Good"
    elif bad_criteria == 1:
        return "Suspicious"
    elif bad_criteria == 2:
        return "Likely Bad"
    else:
        return "Bad"

# Analyze file and extract pixel intensity data
def analyze_file(file_path, prom_val=None):
    df = pd.read_csv(file_path)
    intensity_values = df.iloc[:, 1]  

    mean_intensity = np.mean(intensity_values)
    std_dev_intensity = np.std(intensity_values)
    median_intensity = np.median(intensity_values)

    if prom_val is None:
        prom_val = determine_prominence(intensity_values)

    peaks, _ = find_peaks(intensity_values, prominence=prom_val)

    file_name = os.path.basename(file_path).replace(".jpg.csv", "")

    # Classify file
    classification = classify_file(mean_intensity, std_dev_intensity, len(peaks))

    # Save pixel data
    pixel_data_path = os.path.join(OUTPUT_DIR, f"{file_name}_pixels.csv")
    pixel_df = pd.DataFrame({"Pixel Index": np.arange(len(intensity_values)), "Intensity": intensity_values})
    pixel_df.to_csv(pixel_data_path, index=False)

    return {
        "File": file_name,
        "Number of Peaks": len(peaks),
        "Mean": round(mean_intensity, 2),
        "Median": round(median_intensity, 2),
        "Standard Deviation": round(std_dev_intensity, 2),
        "Prominence Used": round(prom_val, 2),
        "Classification": classification
    }, intensity_values, peaks, classification

# Process all files and save results before displaying graphs
def process_all_files(prom_val=None):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    file_list = [os.path.join(root, file) for root, _, files in os.walk(INPUT_DIR) for file in files]

    if not file_list:
        print("No files found in the input directory.")
        return

    summary_data = []

    for file_path in file_list:
        summary, intensity_values, peaks, classification = analyze_file(file_path, prom_val)
        summary_data.append(summary)

    # Save summary statistics before displaying graphs
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_csv(SUMMARY_CSV_PATH, index=False)
    print(f"Summary CSV saved to: {SUMMARY_CSV_PATH}")

    # Now display graphs
    for file_path in file_list:
        summary, intensity_values, peaks, classification = analyze_file(file_path, prom_val)

        # Create a figure
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(intensity_values, label="Light Intensity")
        ax.plot(peaks, intensity_values[peaks], "x", label="Detected Peaks", color='red')
        ax.set_ylim([0, 255])
        ax.legend()
        ax.set_title(f"{summary['File']} - {classification}")  # Add classification to title

        # Adjust text box position
        text_x = len(intensity_values) + 75  
        stats_text = (
            f"File: {summary['File']}\n"
            f"Number of Peaks: {summary['Number of Peaks']}\n"
            f"Mean: {summary['Mean']}\n"
            f"Median: {summary['Median']}\n"
            f"Std Dev: {summary['Standard Deviation']}\n"
            f"Prominence Used: {summary['Prominence Used']}\n"
            f"Classification: {classification}"
        )
        ax.text(text_x, 200, stats_text, fontsize=10, verticalalignment="top",
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='black'))

        ax.set_xlim([0, len(intensity_values) + 100])  
        plt.show()

# Run the pipeline
if __name__ == "__main__":
    run_imagej_macro()
    process_all_files(prom_val=None)