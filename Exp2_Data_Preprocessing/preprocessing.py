#!/usr/bin/env python3
"""
Experiment 2: Data Preprocessing on EV Charging Telemetry Dataset.
Student: Vidushi Singh (Roll No. 53, D15A)
Course: Data Mining & Business Intelligence (DMBI Lab)
"""
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler

# 1. Load Dataset
data_path = 'ev_charging_platform_dataset.csv' if os.path.exists('ev_charging_platform_dataset.csv') else os.path.join(os.path.dirname(__file__), 'ev_charging_platform_dataset.csv')
df = pd.read_csv(data_path)
print("=" * 60)
print(f"STEP 1: Initial Dataset Shape: {df.shape}")
print("=" * 60)

# 2. Duplicate Detection & Removal
dup_count = df.duplicated().sum()
print(f"STEP 2: Duplicate records identified: {dup_count}")
df = df.drop_duplicates()
print(f"Shape after removing duplicates: {df.shape}")

# 3. Missing Value Handling
print("\nSTEP 3: Missing Value Summary Before Imputation:")
print(df.isnull().sum()[df.isnull().sum() > 0])

num_impute_cols = ['energy_consumed_kwh', 'charging_duration_min', 'ambient_temp_c']
for col in num_impute_cols:
    col_mean = df[col].mean()
    df[col] = df[col].fillna(col_mean)
    print(f"  -> Imputed missing values in '{col}' with mean: {col_mean:.2f}")

cat_impute_cols = ['station_location']
for col in cat_impute_cols:
    col_mode = df[col].mode()[0]
    df[col] = df[col].fillna(col_mode)
    print(f"  -> Imputed missing values in '{col}' with mode: '{col_mode}'")

print(f"Remaining null values: {df.isnull().sum().sum()}")

# 4. Outlier Capping using IQR Method
print("\nSTEP 4: Outlier Detection & Capping (IQR 1.5x)")
outlier_cols = ['charging_duration_min', 'energy_consumed_kwh', 'charging_cost_inr']
for col in outlier_cols:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers_detected = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
    print(f"  -> '{col}': Bounds [{lower_bound:.2f}, {upper_bound:.2f}] | Outliers detected: {outliers_detected}")
    df[col] = np.clip(df[col], lower_bound, upper_bound)

# 5. Categorical Encoding
print("\nSTEP 5: Categorical Encoding (LabelEncoder)")
cat_cols = ['driver_type', 'vehicle_model', 'charger_type', 'station_location']
le_dict = {}
for col in cat_cols:
    le = LabelEncoder()
    df[col + '_encoded'] = le.fit_transform(df[col])
    le_dict[col] = le
    print(f"  -> Encoded '{col}': {list(le.classes_)}")

# 6. Feature Scaling
print("\nSTEP 6: Feature Scaling (StandardScaler)")
scale_cols = ['battery_capacity_kwh', 'initial_soc_pct', 'final_soc_pct', 
              'energy_consumed_kwh', 'charging_duration_min', 'charging_cost_inr', 'ambient_temp_c']
scaler = StandardScaler()
scaled_features = scaler.fit_transform(df[scale_cols])
scaled_df = pd.DataFrame(scaled_features, columns=[c + '_scaled' for c in scale_cols], index=df.index)
df_clean = pd.concat([df, scaled_df], axis=1)

# 7. Save Cleaned Dataset
out_path = os.path.join(os.path.dirname(data_path), 'ev_charging_clean_dataset.csv')
df_clean.to_csv(out_path, index=False)
print("=" * 60)
print(f"Preprocessed dataset saved to: {out_path}")
print(f"Final Preprocessed Shape: {df_clean.shape}")
print("=" * 60)

