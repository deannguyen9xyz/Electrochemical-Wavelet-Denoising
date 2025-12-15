import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
import pywt
import os
from scipy.optimize import curve_fit

#=================
# 1. Load EIS data
#=================

scripts_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(scripts_dir)
data_path = os.path.join("data", "sensor_data.csv")

df = pd.read_csv(data_path, header=0, skiprows=[1])

t = df.iloc[:, 0].values
I_Raw = df.iloc[:, 1].values
I_Ideal = df.iloc[:, 2].values

#============================================
# 2. Initial Cleaning (Savitzky-Golay Filter)
#============================================
#The S-G filter works by taking a small, local section of your data, 
#fitting a smooth curve (a polynomial) through it, 
#and then using the value of that smooth curve to replace the noisy data point.

# S-G Parameters:
window_length = 21   # Must be odd. Controls how many points are used for the fit, small windows less smoothing. but preserve quick changes.
poly_order = 3       # Degree of the polynomial used for fitting. Lower order = smoother.

# Apply the filter to the raw current signal
I_Savgol = savgol_filter(I_Raw, 
                        window_length=window_length, 
                        polyorder=poly_order)

print(f"✅ Stage 1: Savitzky-Golay Filter applied (Window={window_length}, Order={poly_order}).")

#=====================
# 3. Wavelet Denoising
#=====================
# Split signal into frequency layers, remove spikes, reconstruct.

signal_in = I_Savgol 
WAVELET = 'sym5'
LEVEL = 8

# 4a. Decomposition
coeffs = pywt.wavedec(signal_in, WAVELET, level=LEVEL)

# 4b. Threshold Calculation & Filtering
sigma = np.median(np.abs(coeffs[-1])) / 0.6745 # Noise size estimation
threshold = sigma * np.sqrt(2 * np.log(len(signal_in))) # Remove spikes

coeffs_denoised = []
coeffs_denoised.append(coeffs[0]) # Keep cA (Signal + Drift) intact for now

for i in range(1, len(coeffs)):
    # Hard thresholding kills the spikes and fuzz
    cD_denoised = pywt.threshold(coeffs[i], threshold, mode='hard')
    coeffs_denoised.append(cD_denoised)

# 4c. Reconstruction
I_Wavelet = pywt.waverec(coeffs_denoised, WAVELET)
I_Wavelet = I_Wavelet[:len(I_Raw)] 

print(f"✅ Stage 2: Wavelet Denoising applied (Spikes removed).")

#=========================
# 4. Kinetic Model Fitting
#=========================

# DEFINING THE ANCHORED MODEL:
# Remove 'drift_offset'. Now 'drift' is forced to be 0 at t=0.
# Forces 'I_base' to match the actual starting data (~3.0 uA).
# Add 'drift_quad' (t^2) to handle the sine-wave curvature better.

def sensor_model_anchored(t, I_base, I_max, k, drift_slope, drift_quad):
    # 1. The Binding Signal
    binding = I_base + I_max * (1 - np.exp(-k * t))
    
    # 2. The Drift (Anchored at 0)
    # Uses t and t^2, so at t=0, drift is ALWAYS 0.
    drift = drift_slope * t + drift_quad * (t**2)
    
    return binding + drift

# Guess values: I_base~3, I_max~12, k~0.005, drifts~0
p0_guess = [3.0, 12.0, 0.005, 0.0, 0.0]

try:
    # Fit the Anchored Model
    popt, pcov = curve_fit(sensor_model_anchored, t, I_Wavelet, p0=p0_guess)
    
    # Extract fitted parameters
    fit_base = popt[0]
    fit_max = popt[1]
    fit_k = popt[2]
    
    # --- RECONSTRUCTION ---
    # We reconstruct using ONLY the binding parameters.
    # Because the model was anchored, 'fit_base' MUST be the true baseline (~3 uA).
    I_Final_Recovered = fit_base + fit_max * (1 - np.exp(-fit_k * t))
    
    print("✅ Stage 3: Kinetic Parameters Extracted Successfully.")
    print(f"   -> Fitted Base: {fit_base:.2f} µA (Should be close to 3.0)")
    print(f"   -> Fitted Max:  {fit_max:.2f} µA (Should be close to 12.0)")
    print(f"   -> Binding Rate: {fit_k:.5f} (True: 0.004)")

except Exception as e:
    print(f"Fitting failed: {e}")
    I_Final_Recovered = I_Wavelet # Fallback

#===========================
# 5. Quantitative Validation
#===========================

rmse_final = np.sqrt(np.mean((I_Final_Recovered - I_Ideal)**2))
snr_final = 10 * np.log10(np.sum(I_Ideal**2) / np.sum((I_Final_Recovered - I_Ideal)**2))

print("\n" + "="*50)
print(f"FINAL RMSE: {rmse_final:.4f} µA (Goal < 0.5 µA)")
print(f"FINAL SNR:  {snr_final:.2f} dB   (Goal > 30 dB)")
print("="*50)

#=================
# 6. Visualization
#=================

plt.figure(figsize=(20, 12))

plt.plot(t, I_Raw, label='Raw Signal', color='gray', alpha=0.3, linewidth=2)
plt.plot(t, I_Ideal, label='Ideal Signal (Truth)', color='black', linestyle=':', linewidth=2)
plt.plot(t, I_Savgol, label='Savitzky-Golay Filter', color='orange', linewidth=2)
plt.plot(t, I_Final_Recovered, label='Final Recovered (Corrected)', color='red', linewidth=3)

plt.title('Final Result: Wavelet Denoising + Anchored Kinetic Fit', fontsize = 20)
plt.xlabel('Time (s)', fontsize = 18)
plt.ylabel('Current (µA)', fontsize = 18)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.legend(fontsize=16)
plt.grid(True, alpha=0.5)

plt.show()