#!/usr/bin/env python3
"""
Experiment 3: Exploratory Data Analysis & Visualization on EV Charging Telemetry.
Student: Vidushi Singh (Roll No. 53, D15A)
Course: Data Mining & Business Intelligence (DMBI Lab)
"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({'font.sans-serif': 'DejaVu Sans', 'font.size': 10})

out_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(out_dir, 'ev_charging_platform_dataset.csv')
df = pd.read_csv(data_path)

print("=" * 60)
print("EXPERIMENT 3: EXPLORATORY DATA ANALYSIS & VISUALIZATION")
print("=" * 60)

# Impute missing values for clean visualization
df = df.drop_duplicates()
num_cols = ['battery_capacity_kwh', 'initial_soc_pct', 'final_soc_pct', 
            'energy_consumed_kwh', 'charging_duration_min', 'charging_cost_inr', 'ambient_temp_c']
for c in num_cols:
    df[c] = df[c].fillna(df[c].mean())
df['station_location'] = df['station_location'].fillna(df['station_location'].mode()[0])

# 1. Statistical Profiling
print("\n--- Summary Statistics (Five-Number Summary) ---")
desc = df[num_cols].describe().T[['mean', 'std', 'min', '25%', '50%', '75%', 'max']]
print(desc)

print("\n--- Shape Measures: Skewness & Kurtosis ---")
shape_df = pd.DataFrame({
    'Skewness': df[num_cols].skew(),
    'Kurtosis': df[num_cols].kurtosis()
})
print(shape_df)

# Figure 1: Univariate Distributions (Histograms & KDE)
fig, axes = plt.subplots(2, 2, figsize=(12, 9))
sns.histplot(df['energy_consumed_kwh'], kde=True, ax=axes[0, 0], color='#1976D2', bins=25)
axes[0, 0].set_title("Energy Consumed per Session (kWh)", fontweight='bold')
axes[0, 0].set_xlabel("Energy (kWh)")

sns.histplot(df['charging_duration_min'], kde=True, ax=axes[0, 1], color='#388E3C', bins=25)
axes[0, 1].set_title("Charging Duration Distribution (Minutes)", fontweight='bold')
axes[0, 1].set_xlabel("Duration (min)")

sns.histplot(df['charging_cost_inr'], kde=True, ax=axes[1, 0], color='#F57C00', bins=25)
axes[1, 0].set_title("Charging Session Cost (INR ₹)", fontweight='bold')
axes[1, 0].set_xlabel("Cost (₹)")

sns.histplot(df['ambient_temp_c'], kde=True, ax=axes[1, 1], color='#D32F2F', bins=20)
axes[1, 1].set_title("Ambient Operating Temperature (°C)", fontweight='bold')
axes[1, 1].set_xlabel("Temperature (°C)")

plt.tight_layout()
fig1_path = os.path.join(out_dir, "fig1_univariate_distributions.png")
plt.savefig(fig1_path, dpi=200)
plt.close()
print(f"Saved: {fig1_path}")

# Figure 2: Categorical Driver & Charger Distributions (Countplots)
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
sns.countplot(data=df, x='charger_type', ax=axes[0], palette='Blues_r', order=df['charger_type'].value_counts().index)
axes[0].set_title("Session Frequency by Charger Protocol", fontweight='bold')
axes[0].set_ylabel("Total Sessions")

sns.countplot(data=df, x='driver_type', ax=axes[1], palette='Purples_r', order=df['driver_type'].value_counts().index)
axes[1].set_title("EV Fleet Segment Distribution", fontweight='bold')
axes[1].set_ylabel("Total Sessions")

plt.tight_layout()
fig2_path = os.path.join(out_dir, "fig2_categorical_counts.png")
plt.savefig(fig2_path, dpi=200)
plt.close()
print(f"Saved: {fig2_path}")

# Figure 3: Bivariate Boxplots (Charging Duration by Charger Type & Location)
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
sns.boxplot(data=df, x='charger_type', y='charging_duration_min', ax=axes[0], palette='Set2')
axes[0].set_title("Charging Duration across Charger Infrastructure", fontweight='bold')
axes[0].set_ylabel("Duration (min)")

sns.boxplot(data=df, x='station_location', y='charging_cost_inr', ax=axes[1], palette='Pastel1')
axes[1].set_title("Revenue Invoiced across Station Locations", fontweight='bold')
axes[1].set_ylabel("Session Invoiced Cost (₹)")
axes[1].tick_params(axis='x', rotation=25)

plt.tight_layout()
fig3_path = os.path.join(out_dir, "fig3_bivariate_boxplots.png")
plt.savefig(fig3_path, dpi=200)
plt.close()
print(f"Saved: {fig3_path}")

# Figure 4: Multivariate Scatter Plot (Energy vs Duration by Battery Stress)
plt.figure(figsize=(9, 6))
sns.scatterplot(
    data=df,
    x='energy_consumed_kwh',
    y='charging_duration_min',
    hue='battery_stress_flag',
    style='charger_type',
    palette={0: '#2E7D32', 1: '#C62828'},
    alpha=0.85,
    s=70
)
plt.title("Multivariate Interaction: Energy Consumed vs Duration (Hue: Battery Stress)", fontweight='bold')
plt.xlabel("Energy Delivered (kWh)")
plt.ylabel("Charging Duration (Minutes)")
plt.legend(title="Battery Stress / Charger", bbox_to_anchor=(1.02, 1), loc='upper left')
plt.tight_layout()
fig4_path = os.path.join(out_dir, "fig4_multivariate_scatter.png")
plt.savefig(fig4_path, dpi=200)
plt.close()
print(f"Saved: {fig4_path}")

# Figure 5: Correlation Heatmap Matrix
plt.figure(figsize=(9, 7))
corr = df[num_cols].corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
cmap = sns.diverging_palette(230, 20, as_cmap=True)
sns.heatmap(corr, annot=True, fmt=".2f", cmap=cmap, vmin=-1, vmax=1, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .8})
plt.title("Pearson Correlation Heatmap Matrix of Numerical Telemetry", fontweight='bold')
plt.tight_layout()
fig5_path = os.path.join(out_dir, "fig5_correlation_matrix.png")
plt.savefig(fig5_path, dpi=200)
plt.close()
print(f"Saved: {fig5_path}")

print("EDA and visualizations completed successfully!")

