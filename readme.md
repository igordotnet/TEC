# TEC Mapping from GNSS Observations

<img width="1031" alt="Image" src="https://github.com/user-attachments/assets/bf916203-e8d4-4247-bdec-89673bd32b41" />

## Background

In March of 2025, I had the amazing opportunity to travel to Alaska to conduct a small-scale ionospheric study using dual-frequency GNSS receivers. This was a project under the University of Houston's Physics department aimed at understanding how Total Electron Content (TEC) varies with time and location in the upper atmosphere with a special focus on how they interacted under a Aurora Borealis event. The harsh yet beautiful landscape of Alaska provided a perfect setting with unique remote, open-sky visibility, and minimal interference. This repository documents the workflow I followed from setting up the equipment to extracting TEC values from raw GNSS observation files, in hopes it can guide the next generation of UH's Undergraduate Student Research Instrument Project. (USIP)

## Section 1: Equipment Used

![Image](https://github.com/user-attachments/assets/946cf954-5aa5-4d04-97a0-b321a7740372)
- Trimble NetR9: High-precision GNSS reference receiver with dual-frequency logging support
![Image](https://github.com/user-attachments/assets/3d63e7b7-aff2-4c67-9817-45ecd992d9e0)
- Javad Triumph-2: Lightweight GNSS receiver suitable for mobile or backpack deployments

- Extension cords

- Heavy duty Tripods

- Power over Ethernet power connector

- Laptop (Macbook)

- USB C to RJ45 adapter
 
Both receivers were configured to record RINEX-format observation files (version 3.04) at a 30-second interval, with dual-frequency (L1/L2) measurements necessary for TEC derivation.

## Section 2: Setting Up the Equipment

### Trimble NetR9
1. Mount the receiver securely with a clear sky view.
2. Connect an external power supply to the Power over Ethernet connector and use a CAT 6 cable to connect to the Trimble.
3. Power on the Trimble and use the arrows on the device to search for the IP Address.
4. Turn off the WiFi on your device and connect a CAT 6 network cable to the Trimble.
5. Type in the IP Address onto a web browser. (http://169.254.1.0/)
6. Configure logging via Trimble Web UI:
   - Set sample rate (e.g. 30s)
   - Enable dual-frequency logging
   - Output format: RINEX 3.04
7. When everything is set to log, at your own discretion, disconnect the laptop and network cable and you may now leave the Trimble to collect data.

### Javad Triumph-2
1. Mount the receiver securely with a clear sky view.
2. Connect the power connector to a power supply source.
3. Use a Micro USB cable to connect to the Javad and to your machine.
4. Launch 'NetView' a software from the Javad company. 
5. Select the Javad you are plugged into and a new menu should open if everything is connected correctly.
6. Use J-Field or NetView software to configure:
   - Satellite system: GPS only
   - Enable L1 and L2 frequencies
   - Export RINEX with timestamps

## Section 3: Collecting the Data

INSERT PICTURE

This is what your data should look like when you collect it. It basically lets us know: 
- What has collected the Data (Ex Trimble)
- Where it was (Lat 64, Long -14)
- When this is taking place (Noon on March 9th 2025)
And of course the satellite data:
- Which satellite (G = GPS (USA) R = GLONASS (Russian) E = Galileo (EU))
- Time the data was collected
- L1 and L2 data


Retrieval of the data from the machine will be reversal of setup. 
1. Let the receivers log continuously for at least 2–3 hours to capture diurnal variation.
2. Use Trimble or Javad tools to download `.zip` or `.rnx` observation files.
3. Place the `.zip` files inside a directory at the root on your machine. For example:
   /Users/yourname/Desktop/TECData/
4. Each `.zip` should contain at least one `.rnx` file with valid L1C observations.

## Section 4: Running the Code on Your Data

### 1. Clone this repo:


Go to your terminal and type in
```
git clone https://github.com/igordotnet/TEC.git
cd TEC
```

### 2. Install requirements (optional, using Anaconda recommended):

```
conda create -n tec-env python=3.9
conda activate tec-env
pip install -r requirements.txt
```

### 3. Add your `.zip` files to a file in your computer (Ex /Users/yourname/Desktop/TECData/) and update line 14 in ripit.py to match the directory
```
input_directory = "/Users/Desktop/Data" #Change this to a folder with all the Zipped RINEX files
```


### 4. Run the script:

```
python ripit.py
```

### 5. Output:
- Extracted `.rnx` files stored in `/extracted_rinex_files`
- Computed CSV file: Average_Vertical_TEC_Per_Timestamp.csv
- Scatter plot: "Average Vertical TEC Over Time"

## Sample Plot

ADD IMAGE HERE

This is data mapped from one RINEX file as a example, but you can run the program as many files you have in the folder!

## 🧠 Notes & Future Work

- Most upcoming - Map out the data via Dot products and vector algebra to maintain a more '3D' interpertation of the data
- Currently supports only GPS L1C observations.
- Expandable to support more GNSS systems and elevation-angle corrections.
- Add automatic elevation mask filtering and TEC calibration constants.

## 📬 Contact

Feel free to reach out with questions or collaboration ideas   
Email: igorlucic42@gmail.com
