#!/usr/bin/env python3
"""Generate large realistic EV fleet charging dataset for K-Means clustering and RapidMiner analysis."""
import os
import numpy as np
import pandas as pd

np.random.seed(53)
N = 20000

# Archetype 0: Commercial Fleet Express Fast DC (30%)
n0 = int(N * 0.30)
c0_duration = np.random.normal(32, 5, n0).clip(15, 55)
c0_energy = np.random.normal(35, 6, n0).clip(18, 55)
c0_init_soc = np.random.normal(15, 4, n0).clip(5, 28)
c0_final_soc = np.random.normal(82, 4, n0).clip(70, 95)
c0_peak_power = np.random.normal(65, 8, n0).clip(45, 90)
c0_c_rate = np.random.normal(1.4, 0.2, n0).clip(0.9, 1.9)
c0_bat_cap = np.random.choice([39.4, 40.5, 50.3], n0)
c0_temp = np.random.normal(34, 4, n0).clip(20, 45)
c0_cost = c0_energy * 18.5 + np.random.uniform(20, 40, n0)
c0_urgency = np.random.normal(8.5, 0.8, n0).clip(6, 10)

# Archetype 1: Daily Urban Commuter Top-Up (35%)
n1 = int(N * 0.35)
c1_duration = np.random.normal(25, 6, n1).clip(10, 45)
c1_energy = np.random.normal(10, 3, n1).clip(3, 18)
c1_init_soc = np.random.normal(42, 6, n1).clip(25, 65)
c1_final_soc = np.random.normal(78, 5, n1).clip(60, 90)
c1_peak_power = np.random.normal(22, 5, n1).clip(10, 35)
c1_c_rate = np.random.normal(0.6, 0.15, n1).clip(0.2, 0.9)
c1_bat_cap = np.random.choice([3.7, 4.0, 30.2, 40.5], n1)
c1_temp = np.random.normal(29, 3, n1).clip(18, 38)
c1_cost = c1_energy * 14.0 + np.random.uniform(15, 30, n1)
c1_urgency = np.random.normal(4.2, 1.2, n1).clip(1, 7)

# Archetype 2: Overnight Slow AC Depot / Residential (20%)
n2 = int(N * 0.20)
c2_duration = np.random.normal(240, 40, n2).clip(120, 380)
c2_energy = np.random.normal(45, 8, n2).clip(25, 70)
c2_init_soc = np.random.normal(18, 5, n2).clip(5, 30)
c2_final_soc = np.random.normal(98, 2, n2).clip(90, 100)
c2_peak_power = np.random.normal(7.4, 1.2, n2).clip(3.3, 11)
c2_c_rate = np.random.normal(0.25, 0.05, n2).clip(0.1, 0.4)
c2_bat_cap = np.random.choice([40.5, 50.3, 72.6], n2)
c2_temp = np.random.normal(24, 3, n2).clip(15, 32)
c2_cost = c2_energy * 9.5 + np.random.uniform(10, 20, n2)
c2_urgency = np.random.normal(1.8, 0.6, n2).clip(1, 4)

# Archetype 3: High-Drain Ultra-Fast Highway Corridor (15%)
n3 = N - (n0 + n1 + n2)
c3_duration = np.random.normal(22, 4, n3).clip(12, 35)
c3_energy = np.random.normal(55, 9, n3).clip(35, 75)
c3_init_soc = np.random.normal(12, 4, n3).clip(4, 22)
c3_final_soc = np.random.normal(85, 4, n3).clip(75, 95)
c3_peak_power = np.random.normal(135, 15, n3).clip(90, 160)
c3_c_rate = np.random.normal(2.1, 0.25, n3).clip(1.5, 2.7)
c3_bat_cap = np.random.choice([50.3, 72.6], n3)
c3_temp = np.random.normal(38, 4, n3).clip(28, 48)
c3_cost = c3_energy * 22.0 + np.random.uniform(30, 60, n3)
c3_urgency = np.random.normal(9.2, 0.6, n3).clip(7, 10)

def concat_arrs(arrs):
    return np.concatenate(arrs)

data = {
    'session_id': np.arange(10001, 10001 + N),
    'charging_duration_min': np.round(concat_arrs([c0_duration, c1_duration, c2_duration, c3_duration]), 1),
    'energy_consumed_kwh': np.round(concat_arrs([c0_energy, c1_energy, c2_energy, c3_energy]), 2),
    'initial_soc_pct': np.round(concat_arrs([c0_init_soc, c1_init_soc, c2_init_soc, c3_init_soc]), 1),
    'final_soc_pct': np.round(concat_arrs([c0_final_soc, c1_final_soc, c2_final_soc, c3_final_soc]), 1),
    'peak_power_kw': np.round(concat_arrs([c0_peak_power, c1_peak_power, c2_peak_power, c3_peak_power]), 1),
    'avg_charging_c_rate': np.round(concat_arrs([c0_c_rate, c1_c_rate, c2_c_rate, c3_c_rate]), 2),
    'battery_capacity_kwh': concat_arrs([c0_bat_cap, c1_bat_cap, c2_bat_cap, c3_bat_cap]),
    'ambient_temp_c': np.round(concat_arrs([c0_temp, c1_temp, c2_temp, c3_temp]), 1),
    'session_cost_inr': np.round(concat_arrs([c0_cost, c1_cost, c2_cost, c3_cost]), 2),
    'turnaround_urgency_score': np.round(concat_arrs([c0_urgency, c1_urgency, c2_urgency, c3_urgency]), 1),
}

df = pd.DataFrame(data)
# Shuffle rows
df = df.sample(frac=1.0, random_state=53).reset_index(drop=True)
df['session_id'] = np.arange(10001, 10001 + N)

# Save to Exp 6 and Exp 7
exp6_path = r'.\DMBI-Lab-Vidushi\Exp6_KMeans_Clustering\EV_Fleet_Preprocessed_Dataset.csv'
exp7_path = r'.\DMBI-Lab-Vidushi\Exp7_KMeans_RapidMiner\EV_Fleet_Preprocessed_Dataset.csv'
df.to_csv(exp6_path, index=False)
df.to_csv(exp7_path, index=False)
print(f"Generated {exp6_path} and {exp7_path} with shape {df.shape}")

