import zipfile
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Constants for TEC calculations
R_E = 6371  # Earth's radius in km
h = 350  # Ionospheric shell height in km
f_L1 = 1575.42e6  # L1 Frequency in Hz
TEC_coefficient = 40.3 * (f_L1 ** 2)

# Set up working directories
input_directory = "/Users/igorlucic/Desktop/ATEST/"
extracted_directory = "/Users/igorlucic/Desktop/ExtData"
os.makedirs(extracted_directory, exist_ok=True)

# Step 1: Extract all ZIP files
zip_files = [f for f in os.listdir(input_directory) if f.endswith(".zip")]
for zip_file in zip_files:
    with zipfile.ZipFile(os.path.join(input_directory, zip_file), 'r') as zip_ref:
        zip_ref.extractall(extracted_directory)

# Step 2: Identify observation files
rnx_files = [f for f in os.listdir(extracted_directory) if f.endswith(".rnx")]

# Initialize DataFrame to store all processed data
all_relative_tec_data = pd.DataFrame()

# Step 3: Process each RINEX file
for rnx_file in rnx_files:
    file_path = os.path.join(extracted_directory, rnx_file)
    
    with open(file_path, 'r') as file:
        file_content = file.readlines()

    # Extract observation types from the header
    observation_types = []
    header_end_index = 0
    for i, line in enumerate(file_content):
        if "SYS / # / OBS TYPES" in line and line.startswith('G'):  # Focus on GPS
            observation_types.extend(line.split()[3:])
        if "END OF HEADER" in line:
            header_end_index = i
            break

    # Observation data starts after the header
    observation_data = file_content[header_end_index + 1:]
    parsed_data = []
    current_timestamp = None

    # Parse observation data
    for line in observation_data:
        if line.startswith(">"):  # Timestamp line
            current_timestamp = " ".join(line.split()[1:7])
        elif current_timestamp:
            satellite_id = line[:3].strip()
            measurements = [line[i:i + 14].strip() for i in range(3, len(line), 14)]
            
            if 'L1C' in observation_types:
                l1c_index = observation_types.index('L1C')
                l1c_value = float(measurements[l1c_index]) if measurements[l1c_index] else None
                
                if l1c_value:
                    parsed_data.append([current_timestamp, satellite_id, l1c_value])

    # Convert parsed data to DataFrame
    df_parsed = pd.DataFrame(parsed_data, columns=["Timestamp", "Satellite", "L1C"])
    print(f"{rnx_file}: Parsed {len(parsed_data)} rows")
    
    # Compute Relative TEC
    df_parsed["Relative TEC"] = df_parsed["L1C"] / TEC_coefficient

    # Append to master DataFrame
    all_relative_tec_data = pd.concat([all_relative_tec_data, df_parsed], ignore_index=True)

# Step 4: Compute Vertical TEC
if 'Relative TEC' in all_relative_tec_data.columns and not all_relative_tec_data.empty:
    E_deg = 45  # Approximate elevation angle
    cos_E = np.cos(np.radians(E_deg))
    geom_factor = 1 / np.sqrt(1 - (R_E * cos_E / (R_E + h))**2)
    all_relative_tec_data['Vertical TEC'] = all_relative_tec_data['Relative TEC'] * geom_factor
else:
    print("Warning: No valid 'Relative TEC' data found. Skipping VTEC computation.")

# Step 5: Average Vertical TEC per Timestamp
if 'Timestamp' in all_relative_tec_data.columns and 'Vertical TEC' in all_relative_tec_data.columns:
    average_vtec_per_time = all_relative_tec_data.groupby('Timestamp')['Vertical TEC'].mean().reset_index()
    average_vtec_per_time.rename(columns={'Vertical TEC': 'Average Vertical TEC'}, inplace=True)
else:
    print("Warning: Required columns missing to compute average VTEC.")
    average_vtec_per_time = pd.DataFrame()
    average_vtec_per_time.rename(columns={'Vertical TEC': 'Average Vertical TEC'}, inplace=True)
    
# Step 6: Save and Plot Results
if not average_vtec_per_time.empty and 'Timestamp' in average_vtec_per_time.columns:
    output_csv_path = os.path.join(input_directory, "Average_Vertical_TEC_Per_Timestamp.csv")
    average_vtec_per_time.to_csv(output_csv_path, index=False)

    # Plot the results
    plt.figure(figsize=(12, 6))
    plt.scatter(
        pd.to_datetime(
            average_vtec_per_time['Timestamp'],
            format="%Y %m %d %H %M %S.%f",
            errors='coerce'
        ),
        average_vtec_per_time['Average Vertical TEC'],
        label='Average VTEC',
        alpha=0.7
    )
    plt.title("Average Vertical TEC Over Time")
    plt.xlabel("Timestamp")
    plt.ylabel("Average Vertical TEC (TECu)")
    plt.grid()
    plt.legend()
    plt.show()

    print(f"✅ Saved processed data to: {output_csv_path}")
else:
    print("⚠️ No data available to save or plot. Skipping output.")
#print(f"Saved processed data to: {output_csv_path}")