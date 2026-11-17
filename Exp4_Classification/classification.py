#!/usr/bin/env python3
"""
Experiment 4: Classification using Decision Tree and Naive Bayes on EV Battery Stress.
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
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                             f1_score, confusion_matrix, roc_curve, auc)

np.random.seed(53)

out_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(out_dir, 'ev_charging_platform_dataset.csv')
df = pd.read_csv(data_path).drop_duplicates()

# Impute
for c in ['energy_consumed_kwh', 'charging_duration_min', 'ambient_temp_c']:
    df[c] = df[c].fillna(df[c].mean())
df['station_location'] = df['station_location'].fillna(df['station_location'].mode()[0])

# Encode
le_charger = LabelEncoder()
df['charger_type_enc'] = le_charger.fit_transform(df['charger_type'])
le_driver = LabelEncoder()
df['driver_type_enc'] = le_driver.fit_transform(df['driver_type'])

features = ['battery_capacity_kwh', 'initial_soc_pct', 'final_soc_pct',
            'energy_consumed_kwh', 'charging_duration_min', 'ambient_temp_c',
            'charger_type_enc', 'driver_type_enc']
X = df[features]
y = df['battery_stress_flag']

# Train/Test Split (80/20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=53, stratify=y)
print(f"Dataset split: Train={X_train.shape[0]} samples, Test={X_test.shape[0]} samples")

# 1. Decision Tree (CART)
dt = DecisionTreeClassifier(max_depth=4, criterion='gini', random_state=53)
dt.fit(X_train, y_train)
y_pred_dt = dt.predict(X_test)
y_prob_dt = dt.predict_proba(X_test)[:, 1]

# 2. Gaussian Naive Bayes
nb = GaussianNB()
nb.fit(X_train, y_train)
y_pred_nb = nb.predict(X_test)
y_prob_nb = nb.predict_proba(X_test)[:, 1]

# Evaluation Metrics
def eval_model(name, y_true, y_pred, y_prob):
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    fpr, tpr, _ = roc_curve(y_true, y_prob)
    roc_auc = auc(fpr, tpr)
    print(f"=== {name} Performance ===")
    print(f"Accuracy:  {acc*100:.2f}%")
    print(f"Precision: {prec*100:.2f}%")
    print(f"Recall:    {rec*100:.2f}%")
    print(f"F1-Score:  {f1*100:.2f}%")
    print(f"ROC-AUC:   {roc_auc:.4f}\n")
    return {'acc': acc, 'prec': prec, 'rec': rec, 'f1': f1, 'auc': roc_auc, 'cm': confusion_matrix(y_true, y_pred), 'fpr': fpr, 'tpr': tpr}

res_dt = eval_model("Decision Tree (CART)", y_test, y_pred_dt, y_prob_dt)
res_nb = eval_model("Gaussian Naive Bayes", y_test, y_pred_nb, y_prob_nb)

# Visualizations
# 1. Decision Tree Visualization
plt.figure(figsize=(16, 8))
plot_tree(dt, feature_names=features, class_names=['Normal', 'Stress'], filled=True, rounded=True, fontsize=9)
plt.title("Decision Tree Model: Predicting EV Battery Stress (CART, Max Depth = 4)", fontweight='bold', fontsize=12)
plt.tight_layout()
dt_vis_path = os.path.join(out_dir, "fig1_decision_tree_vis.png")
plt.savefig(dt_vis_path, dpi=200)
plt.close()
print(f"Saved: {dt_vis_path}")

# 2. Confusion Matrices
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
sns.heatmap(res_dt['cm'], annot=True, fmt='d', cmap='Blues', ax=axes[0], cbar=False,
            xticklabels=['Normal', 'Stress'], yticklabels=['Normal', 'Stress'])
axes[0].set_title(f"Decision Tree (Acc: {res_dt['acc']*100:.1f}%)", fontweight='bold')
axes[0].set_xlabel("Predicted Label")
axes[0].set_ylabel("True Label")

sns.heatmap(res_nb['cm'], annot=True, fmt='d', cmap='Greens', ax=axes[1], cbar=False,
            xticklabels=['Normal', 'Stress'], yticklabels=['Normal', 'Stress'])
axes[1].set_title(f"Gaussian Naive Bayes (Acc: {res_nb['acc']*100:.1f}%)", fontweight='bold')
axes[1].set_xlabel("Predicted Label")
axes[1].set_ylabel("True Label")

plt.tight_layout()
cm_path = os.path.join(out_dir, "fig2_confusion_matrices.png")
plt.savefig(cm_path, dpi=200)
plt.close()
print(f"Saved: {cm_path}")

# 3. ROC Curves
plt.figure(figsize=(7, 5.5))
plt.plot(res_dt['fpr'], res_dt['tpr'], color='#1565C0', lw=2.2, label=f"Decision Tree (AUC = {res_dt['auc']:.3f})")
plt.plot(res_nb['fpr'], res_nb['tpr'], color='#2E7D32', lw=2.2, label=f"Naive Bayes (AUC = {res_nb['auc']:.3f})")
plt.plot([0, 1], [0, 1], color='gray', linestyle='--', lw=1.2)
plt.xlabel("False Positive Rate (1 - Specificity)")
plt.ylabel("True Positive Rate (Sensitivity / Recall)")
plt.title("ROC Curve Benchmark: Decision Tree vs Naive Bayes", fontweight='bold')
plt.legend(loc='lower right')
plt.tight_layout()
roc_path = os.path.join(out_dir, "fig3_roc_curves.png")
plt.savefig(roc_path, dpi=200)
plt.close()
print(f"Saved: {roc_path}")

