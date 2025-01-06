# Utility Start Audio to HORUS ===============================
# Standard Tools
#=============================================================
from scipy.io import wavfile
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Function to show audio information
def show_info(aname, a, r):
    print('----------------')
    print(f"Audio: {aname}")
    print('----------------')
    print(f"Rate: {r}")
    print('----------------')
    print(f"Shape: {a.shape}")
    print(f"Dtype: {a.dtype}")
    print(f"Min, Max: {a.min()}, {a.max()}")
    print('----------------')
    plot_info(aname, a, r)

# Function to plot audio signal
def plot_info(aname, a, r):        
    sTitle = f'Signal Wave - {aname} at {r}hz'
    plt.title(sTitle)
    sLegend = []
    for c in range(a.shape[1]):  # Dynamically handle channel count
        sLabel = f'Ch{c+1}'
        sLegend.append(sLabel)
        plt.plot(a[:, c], label=sLabel)
    plt.legend(sLegend)
    plt.show()

# File paths - Use raw string notation or escape backslashes properly
audio_files = [r"C:\Users\kazis\Desktop\NOTES MSC P1\Prac\DS\Audio to horus\audio.wav"]

# Process each audio file
for sInputFileName in audio_files:
    # Ensure the file exists before processing
    if not os.path.exists(sInputFileName):
        print(f"File does not exist: {sInputFileName}")
        continue
    
    print('=======================================================')
    print(f'Processing : {sInputFileName}')
    print('=======================================================')
    
    # Read audio data
    InputRate, InputData = wavfile.read(sInputFileName)
    
    # Show info about the audio file
    num_channels = InputData.shape[1] if len(InputData.shape) > 1 else 1  # Check for multiple channels
    show_info(f"{num_channels} channel", InputData, InputRate)
    
    # Create column names dynamically
    columns = [f'Ch{i+1}' for i in range(num_channels)]
    
    # Convert audio data to DataFrame
    ProcessData = pd.DataFrame(InputData)
    ProcessData.columns = columns
    
    # Define output file path
    output_filename = f'C:/VKHCG/05-DS/9999-Data/HORUS-Audio-{num_channels}ch.csv'
    
    # Save processed data to CSV
    ProcessData.to_csv(output_filename, index=False)
    
    print(f'Processed audio saved as {output_filename}')
    print('=======================================================')

print('Audio to HORUS - Done')
print('=======================================================')
