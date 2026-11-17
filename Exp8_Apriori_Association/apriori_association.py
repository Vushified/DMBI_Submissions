#!/usr/bin/env python3
"""
Experiment 8: Apriori Association Rule Mining on EV Charging Behaviour.
Student: Vidushi Singh (Roll No. 53, D15A)
Course: Data Mining & Business Intelligence (DMBI Lab)
"""
import os
import itertools
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

out_dir = os.path.dirname(os.path.abspath(__file__))
trx_path = os.path.join(out_dir, "EV_Association_Transactions.csv")
df_trx = pd.read_csv(trx_path)

print("=" * 60)
print(f"EXPERIMENT 8: APRIORI ASSOCIATION MINING (N = {len(df_trx):,})")
print("=" * 60)

# Item Frequency
item_counts = df_trx.sum().sort_values(ascending=False)
item_supp = (item_counts / len(df_trx)).round(4)
freq_df = pd.DataFrame({'Frequency': item_counts, 'Support': item_supp, 'Support_%': (item_supp * 100).round(2)})
print("\n--- Item Frequency & Support Table ---")
print(freq_df)

# Pure Python Apriori Implementation (Seamless standalone execution)
def run_apriori(df, min_support=0.08):
    N = len(df)
    cols = list(df.columns)
    
    # 1-itemsets
    c1 = {frozenset([col]): df[col].sum() for col in cols}
    l1 = {k: v/N for k, v in c1.items() if v/N >= min_support}
    
    frequent = dict(l1)
    k = 2
    current_L = list(l1.keys())
    
    while current_L:
        # Candidate generation
        candidates = set()
        for i in range(len(current_L)):
            for j in range(i+1, len(current_L)):
                union = current_L[i] | current_L[j]
                if len(union) == k:
                    candidates.add(union)
        
        # Support counting
        new_L = {}
        for cand in candidates:
            mask = df[list(cand)].all(axis=1)
            supp = mask.sum() / N
            if supp >= min_support:
                new_L[cand] = supp
                
        frequent.update(new_L)
        current_L = list(new_L.keys())
        k += 1
        
    res_df = pd.DataFrame([
        {'itemsets': set(k), 'support': v, 'length': len(k)} for k, v in frequent.items()
    ]).sort_values(by=['support', 'length'], ascending=[False, True]).reset_index(drop=True)
    return res_df

print("\nGenerating frequent itemsets (min_support = 0.08)...")
frequent_itemsets = run_apriori(df_trx, min_support=0.08)
print(f"Total Frequent Itemsets Generated: {len(frequent_itemsets)}")
print(frequent_itemsets.head(10))

# Association Rule Generation
def generate_rules(frequent_df, df_raw, min_confidence=0.40):
    N = len(df_raw)
    supp_dict = {frozenset(row['itemsets']): row['support'] for _, row in frequent_df.iterrows()}
    rules = []
    
    for itemset in supp_dict.keys():
        if len(itemset) >= 2:
            # Generate all non-empty antecedent subsets
            for r in range(1, len(itemset)):
                for ant in itertools.combinations(itemset, r):
                    ant = frozenset(ant)
                    con = itemset - ant
                    if ant in supp_dict:
                        conf = supp_dict[itemset] / supp_dict[ant]
                        if conf >= min_confidence:
                            supp_con = supp_dict.get(con, df_raw[list(con)].all(axis=1).sum() / N)
                            lift = conf / supp_con if supp_con > 0 else 1.0
                            rules.append({
                                'antecedents': ', '.join(ant),
                                'consequents': ', '.join(con),
                                'support': round(supp_dict[itemset], 4),
                                'confidence': round(conf, 4),
                                'lift': round(lift, 4)
                            })
    rdf = pd.DataFrame(rules).drop_duplicates()
    rdf = rdf[rdf['lift'] >= 1.0].sort_values(by=['confidence', 'lift'], ascending=[False, False]).reset_index(drop=True)
    return rdf

print("\nDeriving association rules (min_confidence = 0.40, lift >= 1.0)...")
rules_df = generate_rules(frequent_itemsets, df_trx, min_confidence=0.40)
print(f"Total Association Rules Derived: {len(rules_df)}")
print(rules_df.head(10))

rules_csv_path = os.path.join(out_dir, "association_rules.csv")
rules_df.to_csv(rules_csv_path, index=False)
print(f"Saved: {rules_csv_path}")

# Figure 1: Top 10 Frequent Itemsets
plt.figure(figsize=(9, 5))
top10_freq = frequent_itemsets.head(10)
labels = [', '.join(s) for s in top10_freq['itemsets']]
plt.barh(range(len(top10_freq)), top10_freq['support']*100, color='#1565C0', height=0.6)
plt.yticks(range(len(top10_freq)), labels, fontsize=9)
plt.gca().invert_yaxis()
plt.title("Top 10 Frequent EV Telemetry Itemsets (Support %)", fontweight='bold')
plt.xlabel("Support Percentage (%)")
plt.tight_layout()
fig1_path = os.path.join(out_dir, "fig1_frequent_itemsets.png")
plt.savefig(fig1_path, dpi=180)
plt.close()
print(f"Saved: {fig1_path}")

# Figure 2: Rules Scatter (Support vs Confidence vs Lift)
plt.figure(figsize=(8, 5.5))
sc = plt.scatter(rules_df['support']*100, rules_df['confidence']*100, c=rules_df['lift'], 
                 cmap='plasma', s=70, alpha=0.85, edgecolors='none')
cbar = plt.colorbar(sc)
cbar.set_label('Rule Lift')
plt.title("Association Rule Landscape (Support vs Confidence colored by Lift)", fontweight='bold')
plt.xlabel("Rule Support (%)")
plt.ylabel("Rule Confidence (%)")
plt.tight_layout()
fig2_path = os.path.join(out_dir, "fig2_rules_scatter.png")
plt.savefig(fig2_path, dpi=180)
plt.close()
print(f"Saved: {fig2_path}")

