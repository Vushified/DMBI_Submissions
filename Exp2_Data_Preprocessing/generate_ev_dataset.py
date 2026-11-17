#!/usr/bin/env python3
"""Generate realistic synthetic EV charging dataset with controlled missing values, duplicates, and outliers."""
import numpy as np
import pandas as pd
import os

np.random.seed(53)  # Vidushi's Roll No

n_samples = 500

driver_types = ['Commercial Fleet', 'Daily Commuter', 'Rideshare Taxi']
p_driver = [0.35, 0.45, 0.20]

vehicles = [
    ('Tata Nexon EV', 40.5, 'Fast DC (CCS2)'),
    ('MG ZS EV', 50.3, 'Fast DC (CCS2)'),
    ('Ather 450X', 3.7, 'Slow AC (Level 2)'),
    ('Ola S1 Pro', 4.0, 'Slow AC (Level 2)'),
    ('Mahindra XUV400', 39.4, 'Fast DC (CCS2)'),
    ('Hyundai Ioniq 5', 72.6, 'Ultra-Fast DC (150kW)')
]

locations = ['Highway Corridor', 'Tech Park', 'Shopping Mall', 'Fleet Depot', 'Residential Hub']

records = []
for i in range(1, n_samples + 1):
    session_id = 1000 + i
    driver_id = np.random.randint(101, 350)
    d_type = np.random.choice(driver_types, p=p_driver)
    
    veh_idx = np.random.choice(len(vehicles))
    v_model, b_cap, default_charger = vehicles[veh_idx]
    
    if np.random.rand() < 0.8:
        c_type = default_charger
    else:
        c_type = np.random.choice(['Slow AC (Level 2)', 'Fast DC (CCS2)', 'Ultra-Fast DC (150kW)'])
        
    init_soc = np.clip(np.random.normal(22, 8), 5, 45)
    final_soc = np.clip(np.random.normal(85, 7), 60, 100)
    soc_gain = max(5.0, final_soc - init_soc)
    
    # Energy delivered (kWh)
    energy_kwh = round((soc_gain / 100.0) * b_cap * np.random.uniform(1.02, 1.08), 2)
    
    # Duration based on charger type
    if 'Ultra-Fast' in c_type:
        duration = round(energy_kwh / np.random.uniform(100, 140) * 60 + np.random.normal(5, 2), 1)
    elif 'Fast' in c_type:
        duration = round(energy_kwh / np.random.uniform(40, 50) * 60 + np.random.normal(10, 3), 1)
    else:
        duration = round(energy_kwh / np.random.uniform(3.3, 7.2) * 60 + np.random.normal(20, 5), 1)
    duration = max(8.0, duration)
    
    # Cost (INR)
    rate = 21.0 if 'Ultra-Fast' in c_type else (16.5 if 'Fast' in c_type else 10.5)
    cost = round(energy_kwh * rate + np.random.uniform(20, 50), 2)
    
    ambient_temp = round(np.random.normal(32, 5.5), 1)
    loc = np.random.choice(locations)
    
    # Battery stress classification target:
    # High stress if fast charging at high ambient temp with high SoC change
    stress_prob = 0.15
    if 'DC' in c_type: stress_prob += 0.35
    if ambient_temp > 35: stress_prob += 0.25
    if energy_kwh > 30: stress_prob += 0.15
    battery_stress = 1 if np.random.rand() < min(0.9, stress_prob) else 0
    
    records.append({
        'session_id': session_id,
        'driver_id': driver_id,
        'driver_type': d_type,
        'vehicle_model': v_model,
        'charger_type': c_type,
        'battery_capacity_kwh': b_cap,
        'initial_soc_pct': round(init_soc, 1),
        'final_soc_pct': round(final_soc, 1),
        'energy_consumed_kwh': energy_kwh,
        'charging_duration_min': round(duration, 1),
        'charging_cost_inr': cost,
        'ambient_temp_c': ambient_temp,
        'station_location': loc,
        'battery_stress_flag': battery_stress
    })

df = pd.DataFrame(records)

# Introduce 14 duplicate rows
dup_indices = np.random.choice(len(df), size=14, replace=False)
duplicates = df.iloc[dup_indices].copy()
df = pd.concat([df, duplicates], ignore_index=True)

# Introduce Missing Values (NaN)
nan_mask_energy = np.random.choice(len(df), size=18, replace=False)
df.loc[nan_mask_energy, 'energy_consumed_kwh'] = np.nan

nan_mask_duration = np.random.choice(len(df), size=15, replace=False)
df.loc[nan_mask_duration, 'charging_duration_min'] = np.nan

nan_mask_temp = np.random.choice(len(df), size=12, replace=False)
df.loc[nan_mask_temp, 'ambient_temp_c'] = np.nan

nan_mask_loc = np.random.choice(len(df), size=10, replace=False)
df.loc[nan_mask_loc, 'station_location'] = np.nan

# Introduce Outliers
df.loc[12, 'charging_duration_min'] = 480.0   # Extreme stuck charging session
df.loc[45, 'charging_duration_min'] = 520.0
df.loc[78, 'energy_consumed_kwh'] = 195.0     # Faulty meter spike
df.loc[110, 'charging_cost_inr'] = 8500.0

out_dir = r'.\DMBI-Lab-Vidushi\Exp2_Data_Preprocessing'
out_csv = os.path.join(out_dir, 'ev_charging_platform_dataset.csv')
df.to_csv(out_csv, index=False)
print(f"Generated {out_csv} with shape {df.shape}")

