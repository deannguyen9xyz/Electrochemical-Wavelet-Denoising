import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# -- 1. Parameters --
N = 300  # Number of data points (measurements)
time_max = 1500  # Total time in seconds (25 minutes)
t = np.linspace(0, time_max, N)

# -- 2. Ideal Signal (Exponential Binding) --
I_baseline = 3.0 # Baseline SWV peak current in µA
I_max_change = 12.0 # Total change in current due to binding
k_bind = 0.004 # Binding rate constant (controls steepness)

I_Ideal = I_baseline + I_max_change * (1 - np.exp(-k_bind * t))

# -- 3. Noise Components --
# A. High-Frequency Gaussian Noise
sigma_high_freq = 0.4 # Standard deviation of the noise
N_Gaussian = np.random.normal(0, sigma_high_freq, N)

# B. Impulse Noise (Spikes/Artifacts)
noise_spikes = np.zeros(N)
# Add a few random sharp spikes
spike_indices = [31, 103, 183, 280] # Random points in time
spike_magnitudes = [5.0, -3.5, 3.0, -2.0] # Sharp jumps up or down

# The loop structure is cleaner for adding multiple spikes
for idx, mag in zip(spike_indices, spike_magnitudes):
    if idx < N:
        noise_spikes[idx] = mag

# C. Low-Frequency Drift (Baseline Wander)
# Create a slow sine wave mimics temperature changes or slow electrode fouling over 25 mins.
drift_frequency = 1.2 * np.pi / time_max  # Very slow oscillation
drift_amplitude = 1.1  # Drift up to 2 µA
noise_drift = drift_amplitude * np.sin(drift_frequency * t)

# -- 4. Raw Signal --
I_Raw = I_Ideal + N_Gaussian + noise_spikes + noise_drift

# -- 5. Visualization --
plt.figure(figsize=(20, 12))
plt.plot(t, I_Raw, label='Raw SWV Peak Current (with noise)', color='orange')
plt.plot(t, I_Ideal, label='Ideal Signal (Binding Kinetics)', color='blue', linestyle='--')
plt.title('Simulated Time-Series SWV Data', fontsize = 20)
plt.xlabel('Time (s)', fontsize = 18)
plt.ylabel('Peak Current (µA)', fontsize = 18)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.legend(fontsize=16)
plt.grid(True)

plt.show()

# -- 6. Save file --

# Create csv file
data_dir = 'data'
file_path = os.path.join(data_dir, 'sensor_data.csv')
os.makedirs(data_dir, exist_ok=True)

# Define DataFrame
df_data = pd.DataFrame({
    'Time': t,
    'Current_Raw': I_Raw,
    'Current_Ideal': I_Ideal
})

# Define the two header rows
header_names = ['Time', 'Current_Raw', 'Current_Ideal']
header_units = ['s', 'uA', 'uA'] 

# Write the names row
with open(file_path, 'w') as f:
    f.write(','.join(header_names) + '\n')
    
# Write the units row
with open(file_path, 'a') as f:
    f.write(','.join(header_units) + '\n')
    
# Append the actual data without the pandas default header and index
df_data.to_csv(file_path, mode='a', header=False, index=False)

print(f"✅ Data generated and saved to '{file_path}'.")