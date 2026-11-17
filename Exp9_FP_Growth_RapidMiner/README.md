# Experiment 9: FP-Growth Association Rule Mining & RapidMiner Comparison

**Course:** Data Mining and Business Intelligence (DMBI Lab)  
**Student:** Vidushi Singh (Roll No. 53, Div D15A, Group 09)  
**Domain:** Smart Electric Vehicle (EV) Charging & Battery Fleet Analytics  

---

## Overview

This experiment evaluates the **Frequent Pattern Growth (FP-Growth)** algorithm against the classical **Apriori** candidate generation algorithm, reproducing the operator pipeline in **RapidMiner Studio**.

### RapidMiner Studio Operator Pipeline
```text
[Retrieve EV_Association_Transactions]
  --> [Numerical to Binominal]
  --> [FP-Growth (min_support = 0.08)]
  --> [Create Association Rules (min_confidence = 0.40, min_lift = 1.0)]
```

### Core Advantages of FP-Growth
1. **Compresses transactions into a compact FP-Tree:** Retains item co-occurrence info without loss.
2. **Eliminates Candidate Generation:** Circumvents \\(O(2^{|I|})\\) combinatorial explosions.
3. **Restricted to 2 Database Passes:** Massively improves I/O performance over Apriori's iterative passes.

### Files in this Folder
- `EV_Association_Transactions.csv`: 20,000 binary EV transaction vectors.
- `fpgrowth_association.py`: Full FP-Growth tree construction and runtime comparison engine.
- `fpgrowth_association_rules.csv`: Mined high-confidence association rules.
- `EXP-9_DMBI_53_FPGrowth_RapidMiner.pdf`: Laboratory submission report.

