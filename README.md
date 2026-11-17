# DMBI Lab — Vidushi Singh (Roll No. 53, D15A)

Repository for Data Mining and Business Intelligence (DMBI) coursework, laboratory practicals, and Continuous Assessment (CA) submissions.

**Lab experiments domain:** Smart Electric Vehicle (EV) Charging & Battery Fleet Analytics (Exp 1–9).  
**CA domain:** Road safety — BlackSpot Miner on UK STATS19 collision data (CA1, CA2, Exp 10) and High-Utility Itemset Mining (CA3).

---

## Continuous Assessment (CA) Submissions

| Component | Marks | Title / Topic | Folder |
|---|---|---|---|
| **CA1 Case Study** | 10 | BlackSpot Miner: A Case Study-Based Data Mining Analysis of Severe Road Collisions | [`CA1_Case_Study/`](CA1_Case_Study) |
| **CA2 Mini Project** | 10 | BlackSpot Miner: Mining Road Collision Data to Locate Severe-Crash Hotspots and Prioritise Road Safety Action | [`CA2_Mini_Project/`](CA2_Mini_Project) |
| **CA3 Content Beyond Syllabus** | 10 | High-Utility Itemset Mining: When the Most Frequent Pattern Is Not the Most Valuable One | [`CA3/`](CA3) |

CA work was done in VESIT D15A Group 09: Vidushi Singh (53), Jaiprakash Talreja (54), Adarsh Singh (52), Piyush Shukla (49).

---

## Laboratory Experiments (Syllabus Practical Sessions)

| Folder | Experiment | Description & Artifacts |
|---|---|---|
| [`Exp1_Star_Snowflake_Schema/`](Exp1_Star_Snowflake_Schema) | Experiment 1: Schema Design | Dimensional modeling for EV charging: Star schemas (`Fact_Charging_Sessions`, `Fact_Battery_Health`), Snowflake schema (`Dim_Station` & `Dim_Vehicle` hierarchies), architectural SVGs, data dictionaries, and PDF report [`EXP-1_DMBI_53_EV_Charging_Platform.pdf`](Exp1_Star_Snowflake_Schema/EXP-1_DMBI_53_EV_Charging_Platform.pdf) |
| [`Exp2_Data_Preprocessing/`](Exp2_Data_Preprocessing) | Experiment 2: Data Preprocessing | Handling missing telemetry, deduplication (11 duplicates dropped), 1.5× IQR outlier capping, categorical label encoding, Z-score feature scaling, clean dataset, and PDF report [`EXP-2_DMBI_53_DataPreprocessing.pdf`](Exp2_Data_Preprocessing/EXP-2_DMBI_53_DataPreprocessing.pdf) |
| [`Exp3_EDA_Visualization/`](Exp3_EDA_Visualization) | Experiment 3: EDA & Visualization | Statistical five-number profiling, skewness/kurtosis, KDE distributions, bivariate boxplots, multivariate scatter with stress hue, correlation heatmaps, and PDF report [`EXP-3_DMBI_53_EDA_Visualization.pdf`](Exp3_EDA_Visualization/EXP-3_DMBI_53_EDA_Visualization.pdf) |
| [`Exp4_Classification/`](Exp4_Classification) | Experiment 4: Classification Models | Decision Tree (CART) and Gaussian Naïve Bayes classification for battery thermal stress prediction, confusion matrices, ROC-AUC curves, and PDF report [`EXP-4_DMBI_53_Classification.pdf`](Exp4_Classification/EXP-4_DMBI_53_Classification.pdf) |
| [`Exp5_Custom_Classification/`](Exp5_Custom_Classification) | Experiment 5: Custom Classifier | Pure NumPy from-scratch Gaussian Naïve Bayes vs Scikit-learn inbuilt benchmarking, Shannon entropy decision trees, execution latency profiling, and PDF report [`EXP-5_DMBI_53_Classification_Custom.pdf`](Exp5_Custom_Classification/EXP-5_DMBI_53_Classification_Custom.pdf) |
| [`Exp6_KMeans_Clustering/`](Exp6_KMeans_Clustering) | Experiment 6: K-Means Clustering | Customer charging persona segmentation (20,000 records) using K-Means++ in Python, WCSS Elbow curve, Silhouette analysis, 2D PCA cluster projection, and PDF report [`EXP-6_DMBI_53_KMeans_Clustering.pdf`](Exp6_KMeans_Clustering/EXP-6_DMBI_53_KMeans_Clustering.pdf) |
| [`Exp7_KMeans_RapidMiner/`](Exp7_KMeans_RapidMiner) | Experiment 7: K-Means RapidMiner | Graphical operator workflow and cross-platform validation mirroring RapidMiner Studio's pipeline on a 10,000-sample slice, Davies-Bouldin index calculation, and PDF report [`EXP-7_DMBI_53_KMeans_RapidMiner.pdf`](Exp7_KMeans_RapidMiner/EXP-7_DMBI_53_KMeans_RapidMiner.pdf) |
| [`Exp8_Apriori_Association/`](Exp8_Apriori_Association) | Experiment 8: Apriori Association | Behavioral market basket analysis across 20,000 EV charging transactions using Apriori algorithm, downward-closure pruning, 605 association rules, and PDF report [`EXP-8_DMBI_53_Apriori_Association.pdf`](Exp8_Apriori_Association/EXP-8_DMBI_53_Apriori_Association.pdf) |
| [`Exp9_FP_Growth_RapidMiner/`](Exp9_FP_Growth_RapidMiner) | Experiment 9: FP-Growth RapidMiner | Frequent pattern mining using compact FP-Trees without candidate generation, runtime complexity comparison against Apriori, RapidMiner simulation, and PDF report [`EXP-9_DMBI_53_FPGrowth_RapidMiner.pdf`](Exp9_FP_Growth_RapidMiner/EXP-9_DMBI_53_FPGrowth_RapidMiner.pdf) |
| [`Exp10_Mini_Project_App/`](Exp10_Mini_Project_App) | Experiment 10: Mini Project (CA2) | BlackSpot Miner: DBSCAN hotspots, Apriori + K-Modes rules, severity classifiers, next-year site risk ranking, interactive map, Word report [`EXP-10_DMBI_53_MiniProject_BlackSpotMiner.docx`](Exp10_Mini_Project_App/EXP-10_DMBI_53_MiniProject_BlackSpotMiner.docx) and PDF report [`EXP-10_DMBI_53_MiniProject_BlackSpotMiner.pdf`](Exp10_Mini_Project_App/EXP-10_DMBI_53_MiniProject_BlackSpotMiner.pdf) |

---

## Quick Start

```bash
pip install -r requirements.txt
```

### Run the CA2 / Exp 10 BlackSpot Miner notebook
```bash
cd CA2_Mini_Project/POC
jupyter notebook DMBI_CA2_Group09_BlackSpot_Miner.ipynb
```
Download [`CA2_Mini_Project/blackspot_map.html`](CA2_Mini_Project/blackspot_map.html) and open it in a browser for the interactive hotspot map.

### Run the CA3 High-Utility Itemset Mining demo
```bash
cd CA3/POC
jupyter notebook DMBI_CA3_HUI_Demo.ipynb
```

### Run Individual Lab Experiments
Each experiment script can be executed directly from its respective directory:
```bash
# Exp 1 Schema Diagrams Generator
cd Exp1_Star_Snowflake_Schema && python gen_ev_schemas.py

# Exp 2 Preprocessing Pipeline
cd Exp2_Data_Preprocessing && python preprocessing.py

# Exp 3 Exploratory Data Analysis & Visualization
cd Exp3_EDA_Visualization && python eda.py

# Exp 4 Classification (Decision Tree & Naive Bayes)
cd Exp4_Classification && python classification.py

# Exp 5 Custom Classifier & Benchmark
cd Exp5_Custom_Classification && python custom_classification.py

# Exp 6 K-Means Clustering (Python)
cd Exp6_KMeans_Clustering && python kmeans_clustering.py

# Exp 7 K-Means RapidMiner Comparison
cd Exp7_KMeans_RapidMiner && python kmeans_rapidminer_comparison.py

# Exp 8 Apriori Association Rule Mining
cd Exp8_Apriori_Association && python apriori_association.py

# Exp 9 FP-Growth Association Rule Mining
cd Exp9_FP_Growth_RapidMiner && python fpgrowth_association.py
```

