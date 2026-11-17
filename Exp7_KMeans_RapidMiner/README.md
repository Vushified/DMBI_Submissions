# Experiment 7: K-Means Clustering RapidMiner Workflow & Python Benchmark

**Course:** Data Mining and Business Intelligence (DMBI Lab)  
**Student:** Vidushi Singh (Roll No. 53, Div D15A, Group 09)  
**Domain:** Smart Electric Vehicle (EV) Charging & Battery Fleet Analytics  

---

## Overview

This experiment demonstrates the graphical execution and comparative benchmarking of K-Means clustering in **RapidMiner Studio** alongside Python's **scikit-learn**.

### RapidMiner Studio Operator Pipeline
```text
[Retrieve EV_Fleet_Preprocessed_Dataset]
  --> [Select Attributes (10 Numerical Features)]
  --> [Normalize (Z-score Standardization)]
  --> [K-Means (k = 4, k-means++, max_runs = 10)]
  --> [Performance (Cluster Distance Evaluation)]
```

### Files in this Folder
- `EV_Fleet_Preprocessed_Dataset.csv`: 20,000 empirical EV charging records.
- `kmeans_rapidminer_comparison.py`: Python benchmark reproducing RapidMiner operators and license slicing.
- `DATASET.txt`: Dataset specifications and attribute roles.
- `EXP-7_DMBI_53_KMeans_RapidMiner.pdf`: Complete, university-formatted laboratory report.

