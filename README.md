# Electrochemical-Wavelet-Denoising
This Python project showcases advanced signal processing for electrochemical time-series data, a critical challenge in modern sensor development. The Discrete Wavelet Transform (DWT) is used to achieve superior noise reduction from simulated electrochemical biding kinetic data.

## 🌟 Key Features

A Python script with multi-stage denoising pipeline utilizing the Savitzky-Golay filter for initial smoothing and the Wavelet Transform for robust spike removal, followed by anchored kinetic model to stabilize parameter estimation and prevent vertical shifting in the recovered signal..

---

## ⚙️ Requirements

Place the input CSV data file named **"sensor_data.csv"** in the **"data"** directory alongside the Python script(s).

Install required libraries using:

```
pip install numpy scipy pandas matplotlib PyWavelets
```

---

## 📁 Project Files

| File Name | Description |
| :--- | :--- |
| `01_generate_sensor_data.py` | Generate raw binding kinetic data with noise for input. |
| `02_denoise_and_analyze.py` | Signal processing and visualization. |

---

## 📊 Input Data

Script expects a **CSV file** with the following columns:

```
Time, Current_Raw, Current_Ideal
s, uA, uA
5, 1.234, 1.123
10, 1.345, 1.234
...
```


---
## ▶️ How to Run

Run script `01_generate_sensor_data.py`.

---

## 📈 Output

Script generates figure in the *results/* directory.

---
## 📊 Conclusion

*Spike Removal: Successfully eliminated high-frequency spikes and random noise (Savitzky-Golay and Wavelet Thresholding).

*Kinetic Stability: Anchoring the curve, eliminating vertical shifts.

*Acknowledging the Limitation

  *Source of Error: The final deviation between the "Final Recovered" signal (Red Line) and the "Ideal Signal" (Dotted Line) is attributed to the   residual complex, non-linear (sinusoidal) drift present in the simulated data.

  *Mathematical Constraint: It was mathematically incapable of perfectly modeling the sinusoidal noise, resulting in a final RMSE higher than the target.

*The method has extracted all physically identifiable information from the data.

---

## 🎯 Purpose of This Project

This project is designed for:

* Signal processing pipeline to accurately extract the binding rate **k** from noisy electrochemical sensor data.
* Maximize the Signal-to-Noise Ratio (SNR) and minimize the Root Mean Square Error (RMSE) of the final recovered kinetic curve against the ideal signal.
* GitHub portfolio demonstration.

---

## 📌 Future Improvements

* Implement Multi-Resolution Analysis (MRA) for Drift Subtraction..
* Modify/improve Kinetic Model.

--- 

## 🧑‍💻 Author

Developed by: Vu Bao Chau Nguyen, Ph.D.

Keywords: Binding Kinetics, Electrochemical Biosensor Denoising, Wavelet Transform.

---
