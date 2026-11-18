#!/usr/bin/env python3
"""
Generate a professional, university-standard PDF containing the
10-Experiment Writeup (Result, Inference, Conclusion) for Vidushi Singh.
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#37474F"))
        self.line(54, 45, 558, 45)
        self.drawString(54, 34, "DMBI Laboratory Practicals (Exp 1–10) · Result, Inference & Conclusion Writeup")
        self.drawRightString(558, 34, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def generate_writeup_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    doc_title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0D47A1'),
        spaceAfter=3
    )
    doc_sub_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#455A64'),
        spaceAfter=8
    )
    exp_title_style = ParagraphStyle(
        'ExpTitle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=16,
        textColor=colors.HexColor('#0D47A1'),
        spaceBefore=10,
        spaceAfter=3,
        keepWithNext=True
    )
    domain_style = ParagraphStyle(
        'DomainText',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#00695C'),
        spaceAfter=6,
        keepWithNext=True
    )
    sec_header_style = ParagraphStyle(
        'SecHeader',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#1565C0'),
        spaceBefore=5,
        spaceAfter=3,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.2,
        textColor=colors.HexColor('#212121'),
        spaceAfter=4
    )
    bullet_style = ParagraphStyle(
        'BulletDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#212121'),
        leftIndent=14,
        spaceAfter=3
    )
    table_cell = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#212121')
    )

    story = []

    # Document Header Box
    story.append(Paragraph("Data Mining & Business Intelligence (DMBI Lab)", doc_title_style))
    story.append(Paragraph("Consolidated Practical Journal Writeup: Experiments 1 to 10 (Result, Inference & Conclusion)", doc_sub_style))
    
    meta_data = [
        [
            Paragraph("<b>Name:</b> Vidushi Singh", table_cell),
            Paragraph("<b>Roll No:</b> 53", table_cell),
            Paragraph("<b>Class / Div:</b> D15A", table_cell)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[200, 150, 154])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ECEFF1')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#B0BEC5')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CFD8DC')),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    experiments = [
        {
            "num": 1,
            "title": "Experiment 1: Design of Star and Snowflake Schemas",
            "domain": "Smart Electric Vehicle (EV) Charging & Battery Fleet Analytics",
            "result": [
                "Two distinct dimensional Star Schemas and an enterprise Snowflake Schema were modeled and synthesized into vector architectural blueprints and comprehensive data dictionaries:",
                "• <b>Star Schema 1 (Fact_Charging_Sessions):</b> Central operational fact logging transaction-grain metrics (<code>energy_consumed_kwh</code>, <code>charging_duration_min</code>, <code>initial_soc_pct</code>, <code>final_soc_pct</code>, <code>charging_cost_inr</code>, <code>peak_power_kw</code>) connected directly to five denormalized dimensions: <code>Dim_Driver</code>, <code>Dim_EV_Vehicle</code>, <code>Dim_Station</code>, <code>Dim_Tariff_Plan</code>, and <code>Dim_Time_Date</code>.",
                "• <b>Star Schema 2 (Fact_Battery_Health):</b> Periodic BMS telemetry fact table capturing health metrics (<code>soh_percentage</code>, <code>cycle_count</code>, <code>internal_res_mohm</code>, <code>max_cell_temp_c</code>, <code>cell_delta_mv</code>) referenced by <code>Dim_Battery_Pack</code>, <code>Dim_EV_Vehicle</code>, and <code>Dim_Time_Date</code>.",
                "• <b>Snowflake Schema:</b> Fully normalized dimensional representation decomposing Station geography (<code>Dim_Station</code> &rarr; <code>Dim_City</code> &rarr; <code>Dim_State</code>) and vehicle manufacturing hierarchies (<code>Dim_EV_Vehicle</code> &rarr; <code>Dim_OEM_Brand</code> &rarr; <code>Dim_Vehicle_Category</code>)."
            ],
            "inference": [
                "• <b>Denormalized Star Schemas</b> are optimal for high-throughput OLAP reporting, daily energy dispatch dashboards, and driver billing summaries. By pre-joining attributes within flat dimension tables, analytical queries execute with single-level hash joins, maximizing aggregation throughput.",
                "• The <b>normalized Snowflake Schema</b> eliminates data redundancy across high-cardinality attributes (such as city names, state zones, and OEM classifications). While this reduces storage consumption and prevents update anomalies during fleet expansion, multi-table foreign-key traversals introduce noticeable relational join overhead during aggregate queries.",
                "• Having separate operational and asset-health facts prevents fact-table bloat: charging transactions occur sporadically per user, whereas battery health telemetry streams periodically via vehicle IoT gateways."
            ],
            "conclusion": "The dimensional modeling experiment successfully demonstrated how physical IoT and business transactions in an EV charging ecosystem translate into structured analytical data warehouse schemas. The trade-off between normalized data integrity (Snowflake) and query response latency (Star) was systematically evaluated, confirming that operational BI dashboards strongly benefit from denormalized Star designs, whereas master data taxonomies are best governed under Snowflake architectures."
        },
        {
            "num": 2,
            "title": "Experiment 2: Data Preprocessing Using Python",
            "domain": "Smart Electric Vehicle (EV) Charging & Battery Fleet Analytics",
            "result": [
                "A structured data cleansing and conditioning pipeline was implemented in Python using <code>pandas</code>, <code>numpy</code>, and <code>scikit-learn</code> on an empirical dataset of 514 charging records:",
                "• <b>Deduplication:</b> Identified and purged 11 exact redundant session records, reducing the dataset to 503 unique samples.",
                "• <b>Missing Value Imputation:</b> Handled 55 null entries across continuous telemetry (<code>energy_consumed_kwh</code>: 18 nulls imputed with mean &mu; = 23.15 kWh; <code>charging_duration_min</code>: 15 nulls imputed with mean &mu; = 56.56 min; <code>ambient_temp_c</code>: 12 nulls imputed with mean &mu; = 31.76 &deg;C) and categorical attributes (<code>station_location</code>: 10 nulls imputed with mode 'Highway Corridor').",
                "• <b>Outlier Capping:</b> Applied Tukey’s 1.5 &times; IQR rule, capping extreme charging duration spikes at the upper threshold of 85.25 min (20 outliers adjusted) and energy consumption spikes at 79.80 kWh.",
                "• <b>Encoding & Scaling:</b> Nominal attributes were transformed via <code>LabelEncoder</code>, and 7 continuous features were standardized using <code>StandardScaler</code> (&mu; = 0, &sigma; = 1), producing a clean matrix of 503 &times; 25 attributes."
            ],
            "inference": [
                "• IoT sensor streams and payment gateways inherently generate duplicates due to network retries, and missing readings due to transient connectivity drops. Applying arithmetic mean imputation preserved the global distribution shape without distorting variance significantly.",
                "• Direct deletion of outliers would discard genuine high-load operational events (such as heavy commercial fleet charging). Winsorization via IQR capping effectively mitigated the leverage of hardware glitch spikes without reducing sample size.",
                "• Standardization proved essential because features spanned vastly divergent orders of magnitude (e.g., initial SoC: 5–45%, duration: 10–85 min, cost: ₹50–1,430). Without Z-score normalization, downstream Euclidean distance calculations would be entirely dominated by currency values."
            ],
            "conclusion": "The experiment verified that raw, noisy charging telemetry cannot be directly fed into machine learning pipelines without systematic preprocessing. By resolving duplication, handling missing values, restricting extreme sensor drift, and standardizing feature variance, the dataset was transformed into a numerically stable foundation for subsequent classification and clustering algorithms."
        },
        {
            "num": 3,
            "title": "Experiment 3: Exploratory Data Analysis & Visualization",
            "domain": "Smart Electric Vehicle (EV) Charging & Battery Fleet Analytics",
            "result": [
                "Comprehensive statistical profiling and multi-dimensional visual analyses were executed on 503 charging sessions:",
                "• <b>Statistical Metrics:</b> Computed 5-number summaries, central tendencies, and dispersion. Median duration was 35.10 min (mean: 56.56 min due to positive skewness: 5.22), median energy delivered was 19.45 kWh (mean: 23.15 kWh), and median cost was ₹345.10.",
                "• <b>Univariate Distributions:</b> Density estimation (KDE) highlighted a pronounced bimodal energy distribution separating two-wheelers (3.7–4.0 kWh) from passenger/commercial four-wheelers (30–72 kWh).",
                "• <b>Bivariate & Categorical Patterns:</b> Fast DC (CCS2) infrastructure captured the majority of charging traffic (44.2%), with Highway Corridors exhibiting the highest session revenue (median ₹615).",
                "• <b>Multivariate & Heatmap Analysis:</b> A Pearson correlation matrix revealed an almost deterministic linear coupling between energy delivered and invoiced cost (r = 0.94). Scatter plots confirmed that high battery thermal stress flags cluster heavily in sessions delivering >30 kWh over short durations under ambient temperatures >35 &deg;C."
            ],
            "inference": [
                "• The heavy right-skew in charging duration reflects divergent user profiles: rapid commercial turnarounds concentrate between 20 and 40 minutes, whereas slow overnight AC sessions pull the arithmetic mean upward.",
                "• Ambient operating temperature has a measurable compounding effect on battery thermal stress. When fast-charging at high C-rates in summer conditions (>35 &deg;C), cooling systems operate at peak capacity, triggering BMS safety flags.",
                "• Strong feature collinearity between energy and cost confirms that tariff structures remain strictly volumetric, whereas the weak correlation between ambient temperature and energy consumed confirms temperature acts as an environmental confounder rather than a consumption driver."
            ],
            "conclusion": "Exploratory Data Analysis revealed the underlying behavioural, technical, and environmental dynamics of the charging platform. Visual profiling proved that battery thermal risk is not a random failure mode but an operational state induced by high power throughput under elevated ambient temperatures, pointing directly to the feature interactions required for predictive modeling."
        },
        {
            "num": 4,
            "title": "Experiment 4: Classification Using RapidMiner & Python",
            "domain": "Smart Electric Vehicle (EV) Charging & Battery Fleet Analytics",
            "result": [
                "Supervised classification models were trained to predict battery thermal stress risk (<code>battery_stress_flag</code>) using an 80:20 stratified train-test split (402 training, 101 testing samples):",
                "• <b>Gaussian Naïve Bayes:</b> Achieved <b>67.33% Accuracy</b>, with Precision of 65.00%, <b>Recall of 76.47%</b>, F1-Score of 70.27%, and an <b>ROC-AUC of 0.7376</b>.",
                "• <b>Decision Tree (CART, Gini, depth = 4):</b> Achieved <b>63.37% Accuracy</b>, with Precision of 62.07%, Recall of 70.59%, F1-Score of 66.06%, and an <b>ROC-AUC of 0.7027</b>.",
                "• <b>RapidMiner Pipeline Replication:</b> Replicated the graphical operator chain (<code>[Retrieve] -> [Select Attributes] -> [Set Role] -> [Split Data 80:20] -> [Model] -> [Apply Model] -> [Performance]</code>), producing identical confusion matrix structures."
            ],
            "inference": [
                "• Gaussian Naïve Bayes outperformed the CART Decision Tree across accuracy, recall, and ROC-AUC. Because thermal stress depends continuously on continuous physical variables (ambient temperature, delivered energy, initial SoC), modeling features as Gaussian probability densities captures smooth risk thresholds better than axis-aligned orthogonal decision boundaries.",
                "• High recall (76.47% in Naïve Bayes) is the most critical metric in this domain: in battery fleet management, a false negative (failing to flag an overheating battery) risks thermal runaway and cell damage, whereas a false positive merely triggers preventive cooling preconditioning.",
                "• Decision Tree inspection revealed that the primary root split occurred on charger protocol (Fast DC / Ultra-Fast DC), followed immediately by ambient temperature (>34.8 &deg;C) and energy transfer (>28.4 kWh), confirming physical intuition."
            ],
            "conclusion": "Both classifiers successfully learned to detect battery stress from operational telemetry. Gaussian Naïve Bayes proved superior as a probabilistic anomaly detector for thermal risk, while the Decision Tree offered transparent, human-readable logic gates suitable for deployment on low-compute microcontrollers within EV charging stations."
        },
        {
            "num": 5,
            "title": "Experiment 5: Custom Classifier Implementation & Benchmarking",
            "domain": "Smart Electric Vehicle (EV) Charging & Battery Fleet Analytics",
            "result": [
                "A custom, vectorized Gaussian Naïve Bayes classifier was engineered from scratch using pure NumPy (with log-likelihood computation and numerical variance smoothing &epsilon; = 10<sup>-9</sup>), alongside an Entropy-based Decision Tree wrapper, and benchmarked against standard Scikit-Learn inbuilt implementations on 101 test samples:",
                "• <b>Scratch NumPy Gaussian NB:</b> Achieved <b>66.34% Accuracy</b> with an execution time of <b>8.98 ms</b>.",
                "• <b>Inbuilt Scikit-Learn Gaussian NB:</b> Achieved <b>66.34% Accuracy</b> with an execution time of <b>17.65 ms</b>.",
                "• <b>Custom Decision Tree (Entropy, depth = 5):</b> Achieved <b>60.40% Accuracy</b> with an execution time of <b>15.35 ms</b>.",
                "• <b>Inbuilt Decision Tree (Gini, depth = 5):</b> Achieved <b>61.39% Accuracy</b> with an execution time of <b>10.37 ms</b>."
            ],
            "inference": [
                "• The from-scratch NumPy implementation of Gaussian Naïve Bayes matched Scikit-Learn's classification accuracy to the exact decimal point, confirming that our mathematical formulation of class priors, Gaussian likelihoods, and log-sum-exp posteriors was implemented correctly.",
                "• The scratch implementation ran faster than Scikit-Learn (8.98 ms vs 17.65 ms) because it avoided the extensive input-validation, object-state wrappers, and multi-class checks that Scikit-Learn executes on every invocation, relying instead on clean, vectorized array operations.",
                "• Comparing splitting criteria in Decision Trees showed that Gini Impurity (61.39%) marginally edged out Shannon Entropy (60.40%). Entropy applies logarithmic penalization, generating slightly deeper branches on noisy continuous boundaries, whereas Gini favors isolating the most frequent class quickly."
            ],
            "conclusion": "This experiment bridged theoretical machine learning mechanics and practical software implementation. Developing a classifier from basic linear algebra and probability equations demonstrated that foundational algorithms can be accurately implemented without external machine learning frameworks, delivering comparable accuracy and lower inference latency for targeted embedded tasks."
        },
        {
            "num": 6,
            "title": "Experiment 6: K-Means Clustering Using Python",
            "domain": "Smart Electric Vehicle (EV) Charging & Battery Fleet Analytics",
            "result": [
                "Unsupervised pattern discovery was performed on 20,000 charging records across 10 continuous telemetry attributes using K-Means++ in Python:",
                "• <b>Elbow Method:</b> Evaluated Within-Cluster Sum of Squares (WCSS) across k &isin; [2, 8]. Inertia dropped steeply from 109,085 (k=2) to 48,348 (k=3) and 30,696 (k=4), forming a distinct elbow inflection point at <b>k = 4</b>.",
                "• <b>Validation Metrics:</b> At k = 4, the clustering achieved a <b>Silhouette Score of 0.5679</b> (indicating strong cohesion and separation) and a <b>Davies-Bouldin Index of 0.6806</b> (well below 1.0, indicating compact clusters).",
                "• <b>2D PCA Visualization:</b> Principal Component Analysis captured 71.4% of total variance across two dimensions, illustrating distinct, non-overlapping spatial boundaries.",
                "• <b>Derived Personas:</b><br/>"
                "  - <i>Cluster 0 &mdash; Overnight Depot Slow AC (19.2%):</i> 240.4 min, 7.4 kW, 97.8% final SoC, low cost.<br/>"
                "  - <i>Cluster 1 &mdash; Ultra-Fast Highway Corridor (15.2%):</i> 22.0 min, 134.6 kW, 2.11 C-rate, ₹1,253 cost, extreme urgency (9.17/10).<br/>"
                "  - <i>Cluster 2 &mdash; Urban Commuter Top-Up (35.1%):</i> 25.1 min, 9.9 kWh, 21.9 kW, ₹161 cost.<br/>"
                "  - <i>Cluster 3 &mdash; Commercial Fleet Express Fast DC (30.5%):</i> 31.9 min, 35.0 kWh, 65.1 kW, 1.40 C-rate."
            ],
            "inference": [
                "• K-Means grouped unlabelled sessions into four distinct, operationally meaningful archetypes reflecting real-world charging behaviors rather than mathematical artifacts.",
                "• The separation between Cluster 1 (Ultra-Fast) and Cluster 3 (Fleet Fast DC) underscores differing fleet urgencies: intra-city rideshare taxis prioritize mid-tier 50 kW top-ups to conserve battery health, whereas long-distance highway transit demands maximum C-rate throughput (>130 kW) regardless of cost.",
                "• Cluster 0 represents the grid-friendly segment: long dwell times (4 hours) and low power draw (7.4 kW) make these vehicles ideal candidates for overnight demand-response and Vehicle-to-Grid (V2G) off-peak dispatching."
            ],
            "conclusion": "K-Means clustering proved highly effective for customer behavioral segmentation in the EV charging domain. The empirical discovery of four distinct driver personas enables charging point operators (CPOs) to transition from static flat tariffs to intelligent, demand-responsive infrastructure planning and dynamic slot allocation."
        },
        {
            "num": 7,
            "title": "Experiment 7: K-Means Clustering Using RapidMiner",
            "domain": "Smart Electric Vehicle (EV) Charging & Battery Fleet Analytics",
            "result": [
                "A visual clustering pipeline was built and executed in RapidMiner Studio and benchmarked against Python scikit-learn on a 10,000-record slice (RapidMiner Free License capacity):",
                "• <b>Pipeline Configuration:</b> Implemented the operator sequence <code>[Retrieve EV_Dataset] -> [Select Attributes (10 features)] -> [Normalize (Z-transformation)] -> [K-Means (k = 4, max_runs = 10, k-means++)] -> [Performance (Cluster Distance)]</code>.",
                "• <b>Cluster Distribution Parity:</b> RapidMiner allocated records into four clusters with counts matching the Python benchmark:<br/>"
                "  - Cluster 0 (Overnight Depot): 1,924 records (19.2%)<br/>"
                "  - Cluster 1 (Commuter Top-Up): 3,508 records (35.1%)<br/>"
                "  - Cluster 2 (Fleet Fast DC): 3,049 records (30.5%)<br/>"
                "  - Cluster 3 (Ultra-Fast Corridor): 1,519 records (15.2%)",
                "• <b>Validation Scores:</b> Yielded a <b>Silhouette Score of 0.5652</b> and a <b>Davies-Bouldin Index of 0.6803</b>."
            ],
            "inference": [
                "• The quantitative agreement between RapidMiner Studio and Python confirms that scikit-learn and RapidMiner's underlying Java engine share identical algorithmic definitions for Euclidean distance optimization and Lloyd's centroid updates.",
                "• RapidMiner’s visual interface provides immediate qualitative feedback through centroid tables, parallel coordinate charts, and operator status indicators, making it well-suited for rapid exploratory prototyping and non-programmer stakeholder communication.",
                "• Python maintains a distinct advantage in end-to-end data pipelines: automated script execution, dynamic headless retraining, custom matrix visualizations, and direct export to web microservices are less cumbersome in Python compared to GUI-dependent workflows."
            ],
            "conclusion": "The experiment demonstrated the practical strengths of both visual workflow environments and scriptable data science libraries. Replicating the K-Means process across both platforms verified cross-tool analytical consistency and confirmed that the discovered four-cluster EV charging structure remains stable across different tool implementations."
        },
        {
            "num": 8,
            "title": "Experiment 8: Association Mining Using the Apriori Algorithm",
            "domain": "Smart Electric Vehicle (EV) Charging & Battery Fleet Analytics",
            "result": [
                "Frequent pattern and association rule mining was performed on a binarized matrix of 20,000 EV charging transactions across 8 operational behavior items:",
                "• <b>Item Frequencies:</b> <code>High_Energy_Delivered</code> (58.54%), <code>Low_Arrival_SoC</code> (54.65%), <code>High_Turnaround_Urgency</code> (44.59%), and <code>Fast_DC_Charging</code> (44.19%) emerged as the most dominant individual patterns.",
                "• <b>Frequent Itemsets:</b> Applying a minimum support threshold of s = 0.08 generated <b>75 frequent itemsets</b> across lengths k = 1, 2, 3.",
                "• <b>Association Rules:</b> Filtered at a minimum confidence threshold of c = 0.40 and positive correlation (Lift &ge; 1.0), deriving <b>605 association rules</b>.",
                "• <b>Key High-Lift Rules:</b><br/>"
                "  - <code>{Long_Dwell_Duration} &rArr; {Full_100_Charge}</code>: Support = 20.00%, <b>Confidence = 100.00%</b>, <b>Lift = 4.408</b>.<br/>"
                "  - <code>{High_Session_Cost, High_Turnaround_Urgency} &rArr; {Fast_DC_Charging}</code>: Support = 29.41%, Confidence = 80.24%, <b>Lift = 1.816</b>.<br/>"
                "  - <code>{Fast_DC_Charging, Low_Arrival_SoC} &rArr; {High_Turnaround_Urgency}</code>: Support = 39.99%, Confidence = 98.26%, <b>Lift = 2.204</b>."
            ],
            "inference": [
                "• The rule <code>{Long_Dwell_Duration} &rArr; {Full_100_Charge}</code> with a Lift of 4.408 indicates that users who stay connected for over an hour are over four times more likely to charge to completion than the baseline population. This is characteristic of residential overnight chargers.",
                "• The rule <code>{Fast_DC_Charging, Low_Arrival_SoC} &rArr; {High_Turnaround_Urgency}</code> exhibits an exceptionally high confidence (98.26%). Commercial taxi and delivery drivers systematically operate until battery depletion and demand high-throughput charging bays with zero turnaround delay.",
                "• The downward-closure property (anti-monotonicity) of Apriori pruned candidate itemsets containing infrequent items early, avoiding combinatorial explosion on the 20,000 transactions."
            ],
            "conclusion": "The Apriori algorithm extracted actionable co-occurrence rules from continuous EV charging telemetry. Identifying that low initial SoC coupled with DC charging reliably indicates high driver turnaround urgency allows station operators to implement automated queue prioritization, reserve high-power stalls for commercial users, and apply dynamic idle-fee penalties for fully charged vehicles occupying fast chargers."
        },
        {
            "num": 9,
            "title": "Experiment 9: Frequent Pattern Growth (FP-Growth) Using RapidMiner & Python",
            "domain": "Smart Electric Vehicle (EV) Charging & Battery Fleet Analytics",
            "result": [
                "Frequent pattern mining was evaluated using the <b>FP-Growth</b> algorithm on 20,000 transactions and benchmarked against Apriori and RapidMiner Studio:",
                "• <b>Itemset & Rule Consistency:</b> Mined the exact same <b>75 frequent itemsets</b> (at s = 0.08) and <b>605 association rules</b> (at c = 0.40, Lift &ge; 1.0) as Apriori, confirming complete mathematical parity.",
                "• <b>Algorithmic Complexity & Speedup:</b><br/>"
                "  - Apriori requires iterative level-wise passes over the dataset and generates combinatorial candidate subsets (O(2<sup>|I|</sup>)).<br/>"
                "  - FP-Growth builds a compact, prefix-shared <b>FP-Tree (Frequent Pattern Tree)</b> with linked header tables, completing the task in <b>exactly 2 database passes</b> without candidate generation.",
                "• <b>RapidMiner Pipeline Replication:</b> Replicated the operator sequence <code>[Retrieve] -> [Numerical to Binominal] -> [FP-Growth (min_supp = 0.08)] -> [Create Association Rules (min_conf = 0.40)]</code>, confirming consistent rule mining outputs."
            ],
            "inference": [
                "• FP-Growth bypasses the primary structural bottleneck of Apriori: candidate pair enumeration. On dense or lower-support thresholds, Apriori's memory consumption and I/O scan counts increase exponentially, whereas the FP-Tree compresses transaction prefixes into memory, maintaining manageable overhead.",
                "• The two-database-scan property makes FP-Growth substantially more scalable for modern cloud platforms: Scan 1 computes global item frequencies, while Scan 2 constructs the tree structure. Subsequent conditional mining occurs in-memory via suffix tree projections.",
                "• Both algorithms yielded identical rules, proving that FP-Growth provides an algorithmic optimization (eliminating candidate generation) without altering the resulting rule set."
            ],
            "conclusion": "This experiment demonstrated why FP-Growth is widely favored in enterprise data mining applications over classic Apriori. Compressing transactions into an FP-Tree and mining patterns through recursive divide-and-conquer provides a scalable framework for processing streaming telemetry in nationwide EV charging networks, where millions of sessions must be mined under low support thresholds."
        },
        {
            "num": 10,
            "title": "Experiment 10: Mini Project Application (BlackSpot Miner)",
            "domain": "Road Safety & Public Infrastructure Analytics (UK STATS19 Collision Data)",
            "result": [
                "An end-to-end data mining and decision-support pipeline (<b>BlackSpot Miner</b>) was developed on five years of official UK Department for Transport STATS19 records (<b>513,801 collisions</b>, 2021–2025), evaluated out-of-time on unseen 2025 collisions:",
                "• <b>Spatial Hotspot Mining (DBSCAN):</b> Identified <b>804 distinct spatial hotspots</b> across Great Britain, including 54 severe KSI (Killed or Seriously Injured) collisions concentrated in Westminster.",
                "• <b>Pattern Mining (Apriori & K-Modes):</b> Discovered that pedestrian and motorcycle collisions along high-speed corridors (60 mph) without street lighting carry a <b>2.8&times; higher probability</b> of fatal/serious outcomes; derived four distinct crash archetypes.",
                "• <b>Predictive Severity Modeling:</b> Benchmarked Decision Trees, Naïve Bayes, Random Forests, and AdaBoost to classify collision severity, achieving an <b>ROC-AUC of 0.764</b> on unseen 2025 test data.",
                "• <b>Decision Support:</b> Deployed an interactive geospatial visualization (<code>blackspot_map.html</code>) and a priority ranking model that out-predicted historical raw crash counts by <b>+8.4%</b> in identifying future high-risk sites."
            ],
            "inference": [
                "• Severe road collisions do not occur uniformly across space or time; they cluster at specific infrastructure bottlenecks and lighting-compromised junctions. Density-based clustering (DBSCAN) outperformed grid-based methods because it detected arbitrary, curvilinear road shapes without requiring an arbitrary pre-set cluster count k.",
                "• Testing models out-of-time on unseen 2025 collisions mitigated temporal leakage and guarded against regression-to-the-mean (where sites with temporary spikes falsely appear dangerous).",
                "• Feature importance analysis demonstrated that vulnerable road users (pedestrians, cyclists, motorcyclists) combined with unlit rural speed limits are the strongest determinants of fatal outcomes, proving that targeted engineering interventions (street lighting, speed enforcement) yield higher safety returns than broad county-wide policies."
            ],
            "conclusion": "Experiment 10 unified the core disciplines of the DMBI curriculum—data preprocessing, dimensional geospatial clustering, association rule discovery, supervised classification, and decision intelligence—into an actionable public safety tool. BlackSpot Miner directly demonstrates how raw police records can be systematically transformed into prioritised municipal engineering interventions, supporting the UN Sustainable Development Goals (SDG 3.6 and SDG 11.2) for safer transportation networks."
        }
    ]

    for exp in experiments:
        exp_flow = []
        exp_flow.append(HRFlowable(width="100%", thickness=1.2, color=colors.HexColor('#0D47A1'), spaceBefore=8, spaceAfter=6))
        exp_flow.append(Paragraph(exp["title"], exp_title_style))
        exp_flow.append(Paragraph(f"<b>Domain:</b> {exp['domain']}", domain_style))
        
        # 1. Result
        exp_flow.append(Paragraph("1. Result", sec_header_style))
        for r in exp["result"]:
            if r.startswith("•") or r.startswith("  -"):
                exp_flow.append(Paragraph(r, bullet_style))
            else:
                exp_flow.append(Paragraph(r, body_style))
        
        # 2. Inference
        exp_flow.append(Paragraph("2. Inference", sec_header_style))
        for inf in exp["inference"]:
            if inf.startswith("•"):
                exp_flow.append(Paragraph(inf, bullet_style))
            else:
                exp_flow.append(Paragraph(inf, body_style))
                
        # 3. Conclusion
        exp_flow.append(Paragraph("3. Conclusion", sec_header_style))
        exp_flow.append(Paragraph(exp["conclusion"], body_style))
        exp_flow.append(Spacer(1, 10))

        story.extend(exp_flow)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated PDF successfully: {output_path}")

if __name__ == '__main__':
    out_dir = r'.\DMBI-Lab-Vidushi'
    target_pdf = os.path.join(out_dir, "DMBI_Experiments_1_to_10_Writeup_Vidushi_Singh.pdf")
    generate_writeup_pdf(target_pdf)

