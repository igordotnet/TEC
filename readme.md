# TEC Mapping from GNSS Observations

[TECDataMapped.pdf](https://github.com/user-attachments/files/20007652/TECDataMapped.pdf)

## Background

In early 2025, I had the opportunity to travel to Alaska to conduct a small-scale ionospheric study using dual-frequency GNSS receivers. This was a personal research project aimed at understanding how Total Electron Content (TEC) varies with time and location in the upper atmosphere. The harsh yet beautiful landscape of Alaska provided a perfect setting — remote, open-sky visibility, and minimal interference. This repository documents the workflow I followed — from setting up the equipment to extracting TEC values from raw GNSS observation files.

## Section 1: Equipment Used

- Trimble NetR9: A high-precision GNSS reference receiver with dual-frequency logging support.
- Javad Triumph-2: Lightweight GNSS receiver suitable for mobile or backpack deployments.

Both receivers were configured to record RINEX-format observation files at a 30-second interval, with dual-frequency (L1/L2) measurements necessary for TEC derivation.

## Section 2: Setting Up the Equipment

### Trimble NetR9
1. Mount the receiver securely with a clear sky view.
2. Connect an external power supply or use internal battery.
3. Configure logging via Trimble Web UI:
   - Set sample rate (e.g. 30s)
   - Enable dual-frequency logging
   - Output format: RINEX 3.x

### Javad Triumph-2
1. Place in a stable environment away from reflective surfaces.
2. Use J-Field or NetView software to configure:
   - Satellite system: GPS only
   - Enable L1 and L2 frequencies
   - Export RINEX with timestamps

## 📥 Section 3: Collecting the Data

1. Let the receivers log continuously for at least 2–3 hours to capture diurnal variation.
2. Use Trimble or Javad tools to download `.zip` or `.rnx` observation files.
3. Place the `.zip` files inside the `ATEST/` directory at the root of this project:
   /Users/yourname/Desktop/ATEST/
4. Each `.zip` should contain at least one `.rnx` file with valid L1C observations.

## 🧮 Section 4: Running the Code on Your Data

### 1. Clone the repo:

```
git clone https://github.com/yourusername/TEC.git
cd TEC
```

### 2. Install requirements (optional, using Anaconda recommended):

```
conda create -n tec-env python=3.9
conda activate tec-env
pip install -r requirements.txt
```

### 3. Add your `.zip` files to the `/ATEST` directory

### 4. Run the script:

```
python ripit.py
```

### 5. Output:
- Extracted `.rnx` files stored in `/extracted_rinex_files`
- Computed CSV file: Average_Vertical_TEC_Per_Timestamp.csv
- Scatter plot: "Average Vertical TEC Over Time"

## 📊 Sample Plot

ADDIMAGE HERE

## 🧠 Notes & Future Work

- Currently supports only GPS L1C observations.
- Expandable to support more GNSS systems and elevation-angle corrections.
- Add automatic elevation mask filtering and TEC calibration constants.

## 📬 Contact

Feel free to reach out with questions or collaboration ideas.  
Email: igorlucic42@gmail.com
