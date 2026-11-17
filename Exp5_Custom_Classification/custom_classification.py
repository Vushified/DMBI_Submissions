#!/usr/bin/env python3
"""
Experiment 5: Custom Classifier Implementation (Scratch vs Inbuilt).
Student: Vidushi Singh (Roll No. 53, D15A)
Course: Data Mining & Business Intelligence (DMBI Lab)
"""
import os
import time
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_text
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

np.random.seed(53)
sns.set_theme(style="white")

out_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(out_dir, 'ev_charging_platform_dataset.csv')
df = pd.read_csv(data_path).drop_duplicates()

# Missing values imputation
for c in ['energy_consumed_kwh', 'charging_duration_min', 'ambient_temp_c']:
    df[c] = df[c].fillna(df[c].mean())
df['station_location'] = df['station_location'].fillna(df['station_location'].mode()[0])

feature_cols = ['battery_capacity_kwh', 'initial_soc_pct', 'final_soc_pct',
                'energy_consumed_kwh', 'charging_duration_min', 'ambient_temp_c']
X = df[feature_cols].copy()
y = df['battery_stress_flag'].copy()
classes = ['Normal_State', 'High_Thermal_Stress']

# Scale features
scaler = StandardScaler()
X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=feature_cols)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.20, random_state=53, stratify=y
)
print(f"Train samples: {X_train.shape[0]} | Test samples: {X_test.shape[0]}")

results = {"classes": classes, "train_size": int(X_train.shape[0]), "test_size": int(X_test.shape[0])}

def save_cm(cm, title, fname, cmap):
    plt.figure(figsize=(5.5, 4.5))
    sns.heatmap(cm, annot=True, fmt='d', cmap=cmap, xticklabels=classes, yticklabels=classes, cbar=False)
    plt.title(title, fontweight='bold', fontsize=11)
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, fname), dpi=180)
    plt.close()

# ============ 1) INBUILT DECISION TREE (Gini) ============
t0 = time.perf_counter()
dt_inbuilt = DecisionTreeClassifier(criterion="gini", max_depth=5, min_samples_leaf=8, random_state=53)
dt_inbuilt.fit(X_train, y_train)
t_dt_inbuilt = (time.perf_counter() - t0) * 1000
y_pred_dt_inbuilt = dt_inbuilt.predict(X_test)
acc_dt_inbuilt = accuracy_score(y_test, y_pred_dt_inbuilt)
cm_dt_inbuilt = confusion_matrix(y_test, y_pred_dt_inbuilt)
save_cm(cm_dt_inbuilt, 'Inbuilt Decision Tree (Gini) - Confusion Matrix', 'cm_dt_inbuilt.png', 'Blues')

plt.figure(figsize=(16, 8))
plot_tree(dt_inbuilt, feature_names=feature_cols, class_names=classes, filled=True, rounded=True, fontsize=9, max_depth=3)
plt.title("Inbuilt CART Decision Tree (Gini, max_depth=5)", fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'decision_tree_inbuilt.png'), dpi=180)
plt.close()

# ============ 2) CUSTOM DECISION TREE WRAPPER (Entropy) ============
def custom_decision_tree(X_tr, y_tr, X_te, criterion="entropy", max_depth=5):
    t_start = time.perf_counter()
    model = DecisionTreeClassifier(criterion=criterion, max_depth=max_depth, min_samples_leaf=8, random_state=53)
    model.fit(X_tr, y_tr)
    t_elapsed = (time.perf_counter() - t_start) * 1000
    return model.predict(X_te), model, t_elapsed

y_pred_dt_custom, dt_custom_model, t_dt_custom = custom_decision_tree(X_train, y_train, X_test)
acc_dt_custom = accuracy_score(y_test, y_pred_dt_custom)
cm_dt_custom = confusion_matrix(y_test, y_pred_dt_custom)
save_cm(cm_dt_custom, 'Custom Decision Tree (Entropy) - Confusion Matrix', 'cm_dt_custom.png', 'Greens')

# ============ 3) INBUILT NAIVE BAYES ============
t0 = time.perf_counter()
nb_inbuilt = GaussianNB()
nb_inbuilt.fit(X_train, y_train)
t_nb_inbuilt = (time.perf_counter() - t0) * 1000
y_pred_nb_inbuilt = nb_inbuilt.predict(X_test)
acc_nb_inbuilt = accuracy_score(y_test, y_pred_nb_inbuilt)
cm_nb_inbuilt = confusion_matrix(y_test, y_pred_nb_inbuilt)
save_cm(cm_nb_inbuilt, 'Inbuilt Gaussian Naive Bayes - Confusion Matrix', 'cm_nb_inbuilt.png', 'Blues')

# ============ 4) FROM-SCRATCH GAUSSIAN NAIVE BAYES (Pure NumPy) ============
class ScratchGaussianNB:
    """From-scratch Gaussian Naive Bayes implemented purely in NumPy."""
    def fit(self, X_arr, y_arr):
        self.classes_ = np.unique(y_arr)
        self.mean_ = {}
        self.var_ = {}
        self.priors_ = {}
        for c in self.classes_:
            X_c = X_arr[y_arr == c]
            self.mean_[c] = np.mean(X_c, axis=0)
            self.var_[c] = np.var(X_c, axis=0) + 1e-9  # Smoothing factor
            self.priors_[c] = len(X_c) / len(X_arr)
            
    def _pdf(self, class_idx, x):
        mean = self.mean_[class_idx]
        var = self.var_[class_idx]
        numerator = np.exp(-((x - mean) ** 2) / (2 * var))
        denominator = np.sqrt(2 * np.pi * var)
        return numerator / denominator
        
    def predict(self, X_arr):
        preds = []
        for x in X_arr:
            posteriors = []
            for c in self.classes_:
                prior = np.log(self.priors_[c])
                conditional = np.sum(np.log(self._pdf(c, x) + 1e-12))
                posteriors.append(prior + conditional)
            preds.append(self.classes_[np.argmax(posteriors)])
        return np.array(preds)

t0 = time.perf_counter()
scratch_nb = ScratchGaussianNB()
scratch_nb.fit(X_train.values, y_train.values)
y_pred_scratch_nb = scratch_nb.predict(X_test.values)
t_nb_scratch = (time.perf_counter() - t0) * 1000
acc_nb_scratch = accuracy_score(y_test, y_pred_scratch_nb)
cm_nb_scratch = confusion_matrix(y_test, y_pred_scratch_nb)
save_cm(cm_nb_scratch, 'Scratch NumPy Gaussian Naive Bayes - Confusion Matrix', 'cm_nb_scratch.png', 'Purples')

# Benchmark Summary
benchmark = {
    "DT_Inbuilt_Gini": {"accuracy": round(acc_dt_inbuilt*100, 2), "train_time_ms": round(t_dt_inbuilt, 3)},
    "DT_Custom_Entropy": {"accuracy": round(acc_dt_custom*100, 2), "train_time_ms": round(t_dt_custom, 3)},
    "NB_Inbuilt_Gaussian": {"accuracy": round(acc_nb_inbuilt*100, 2), "train_time_ms": round(t_nb_inbuilt, 3)},
    "NB_Scratch_NumPy": {"accuracy": round(acc_nb_scratch*100, 2), "train_time_ms": round(t_nb_scratch, 3)}
}
with open(os.path.join(out_dir, 'exp5_results.json'), 'w') as f:
    json.dump(benchmark, f, indent=2)

print("\n=== EXPERIMENT 5 BENCHMARK RESULTS ===")
for k, v in benchmark.items():
    print(f"{k}: Accuracy = {v['accuracy']}% | Runtime = {v['train_time_ms']} ms")

