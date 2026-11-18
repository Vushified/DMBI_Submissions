#!/usr/bin/env python3
"""Build comprehensive university-standard PDF report for Experiment 6 (K-Means Clustering)."""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
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
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))
        self.line(54, 45, 558, 45)
        self.drawString(54, 34, "Experiment 6: K-Means Clustering in Python (Smart EV Analytics)")
        self.drawRightString(558, 34, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def build_pdf(pdf_path, img_dir):
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=colors.HexColor('#0D47A1'), spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle', parent=styles['Normal'], fontName='Helvetica', fontSize=11, leading=14, textColor=colors.HexColor('#37474F'), spaceAfter=10
    )
    h1_style = ParagraphStyle(
        'Heading1_Custom', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=colors.HexColor('#1565C0'), spaceBefore=12, spaceAfter=6, keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'Heading2_Custom', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=10.5, leading=14, textColor=colors.HexColor('#2E7D32'), spaceBefore=8, spaceAfter=4, keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body_Custom', parent=styles['Normal'], fontName='Helvetica', fontSize=9, leading=13, textColor=colors.HexColor('#212121'), spaceAfter=6
    )
    table_cell = ParagraphStyle(
        'TableCell', fontName='Helvetica', fontSize=8, leading=10.5, textColor=colors.HexColor('#212121')
    )
    table_cell_bold = ParagraphStyle(
        'TableCellBold', fontName='Helvetica-Bold', fontSize=8, leading=10.5, textColor=colors.HexColor('#0D47A1')
    )
    table_hdr = ParagraphStyle(
        'TableHdr', fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=colors.white
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("Experiment 6 – K-Means Clustering Using Python", title_style))
    story.append(Paragraph("<b>Domain:</b> Smart Electric Vehicle (EV) Charging & Fleet Battery Telemetry Analytics", subtitle_style))
    
    meta_data = [
        [
            Paragraph("<b>Name:</b> Vidushi Singh", table_cell),
            Paragraph("<b>Roll No:</b> 53", table_cell),
            Paragraph("<b>Class / Div:</b> D15A", table_cell)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[200, 150, 154])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F0F4F8')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CFD8DC')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E0E0E0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # Aim & Objectives
    story.append(Paragraph("Aim", h1_style))
    story.append(Paragraph("To discover natural operational groupings, driver charging archetypes, and power dispatch personas across 20,000 empirical EV fleet charging records using the K-Means unsupervised clustering algorithm in Python, determining the optimal cluster number via the Elbow method and validating partition quality via Silhouette and Davies-Bouldin scores.", body_style))
    
    story.append(Paragraph("Objectives", h1_style))
    story.append(Paragraph("• Standardize high-dimensional EV charging telemetry vectors using Z-score standardization.", body_style))
    story.append(Paragraph("• Calculate Within-Cluster Sum of Squares (WCSS) across k = 2 to 8 to identify the optimal elbow point.", body_style))
    story.append(Paragraph("• Execute K-Means++ clustering with k = 4 and compute cluster validation metrics.", body_style))
    story.append(Paragraph("• Project high-dimensional telemetry into 2D PCA principal component space for visual validation.", body_style))
    story.append(Paragraph("• Extract actionable business insights and operational tariff strategies from cluster centroid profiles.", body_style))

    # Mathematical Foundations
    story.append(Paragraph("Mathematical Foundation of K-Means Clustering", h1_style))
    story.append(Paragraph("K-Means partitions an unlabelled dataset of N observations into <b>k</b> disjoint clusters S = {S<sub>1</sub>, S<sub>2</sub>, ..., S<sub>k</sub>} by minimizing the Within-Cluster Sum of Squares (WCSS / inertia):", body_style))
    story.append(Paragraph("<font face='Courier' size='8.5'><b>WCSS = &Sigma;<sub>i=1..k</sub> &Sigma;<sub>x &isin; S<sub>i</sub></sub> || x - &mu;<sub>i</sub> ||<sup>2</sup></b></font>", body_style))
    story.append(Paragraph("where <b>&mu;<sub>i</sub></b> denotes the centroid of cluster S<sub>i</sub>. Initialization uses the <b>k-means++</b> scheme, selecting initial seeds with probability proportional to their squared Euclidean distance from the nearest existing centroid to accelerate convergence and prevent sub-optimal local minima.", body_style))

    story.append(PageBreak())

    # Elbow & Cluster Validation
    story.append(Paragraph("1. Determining Optimal Clusters: Elbow Method & Validation", h1_style))
    story.append(Paragraph("The WCSS curve below displays a steep knee at <b>k = 4</b> (WCSS drops from 109,085 at k=2 to 30,696 at k=4, beyond which reductions diminish to marginal returns).", body_style))
    
    f_elbow = os.path.join(img_dir, "elbow_curve.png")
    if os.path.exists(f_elbow):
        story.append(Image(f_elbow, width=460, height=260))
        story.append(Spacer(1, 6))

    val_data = [
        [Paragraph("Validation Metric", table_hdr), Paragraph("Empirical Score", table_hdr), Paragraph("Theoretical Interpretation", table_hdr)],
        [Paragraph("Optimal Cluster Count (k)", table_cell_bold), Paragraph("4", table_cell), Paragraph("Distinct behavioral operational modes in EV charging", table_cell)],
        [Paragraph("Silhouette Score", table_cell_bold), Paragraph("0.5679", table_cell_bold), Paragraph("Strong intra-cluster cohesion and clean inter-cluster separation", table_cell)],
        [Paragraph("Davies-Bouldin Index", table_cell_bold), Paragraph("0.6806", table_cell_bold), Paragraph("Significantly below 1.0; confirms compact, well-separated clusters", table_cell)],
        [Paragraph("PCA Explained Variance (2D)", table_cell_bold), Paragraph("71.4%", table_cell), Paragraph("Captures the dominant operational variance across 10 telemetry features", table_cell)]
    ]
    t_val = Table(val_data, colWidths=[150, 110, 244])
    t_val.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0D47A1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CFD8DC')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_val)

    story.append(PageBreak())

    # Visualizations: Sizes & PCA
    story.append(Paragraph("2. Cluster Demographics & 2D PCA Spatial Distribution", h1_style))
    f_sizes = os.path.join(img_dir, "cluster_sizes.png")
    if os.path.exists(f_sizes):
        story.append(Image(f_sizes, width=440, height=210))
        story.append(Spacer(1, 6))

    f_scatter = os.path.join(img_dir, "cluster_scatter.png")
    if os.path.exists(f_scatter):
        story.append(Image(f_scatter, width=480, height=270))
        story.append(Spacer(1, 6))

    story.append(PageBreak())

    # Centroid Profiles Table
    story.append(Paragraph("3. Cluster Centroid Profiles & Behavioral Segmentation", h1_style))
    prof_data = [
        [Paragraph("Telemetry Feature", table_hdr), Paragraph("Cluster 0: Depot Slow AC", table_hdr), Paragraph("Cluster 1: Ultra-Fast Corridor", table_hdr), Paragraph("Cluster 2: Commuter Top-Up", table_hdr), Paragraph("Cluster 3: Fleet Express Fast DC", table_hdr)],
        [Paragraph("Duration (min)", table_cell_bold), Paragraph("240.4 m", table_cell), Paragraph("22.0 m", table_cell), Paragraph("25.1 m", table_cell), Paragraph("31.9 m", table_cell)],
        [Paragraph("Energy (kWh)", table_cell_bold), Paragraph("45.17 kWh", table_cell), Paragraph("54.91 kWh", table_cell), Paragraph("9.93 kWh", table_cell), Paragraph("34.98 kWh", table_cell)],
        [Paragraph("Initial SoC (%)", table_cell_bold), Paragraph("18.1%", table_cell), Paragraph("12.1%", table_cell), Paragraph("42.0%", table_cell), Paragraph("15.1%", table_cell)],
        [Paragraph("Final SoC (%)", table_cell_bold), Paragraph("97.8%", table_cell), Paragraph("85.1%", table_cell), Paragraph("78.0%", table_cell), Paragraph("82.0%", table_cell)],
        [Paragraph("Peak Power (kW)", table_cell_bold), Paragraph("7.4 kW", table_cell), Paragraph("134.6 kW", table_cell), Paragraph("21.9 kW", table_cell), Paragraph("65.1 kW", table_cell)],
        [Paragraph("C-Rate (Charge Speed)", table_cell_bold), Paragraph("0.25 C", table_cell), Paragraph("2.11 C", table_cell), Paragraph("0.60 C", table_cell), Paragraph("1.40 C", table_cell)],
        [Paragraph("Ambient Temp (°C)", table_cell_bold), Paragraph("24.1 °C", table_cell), Paragraph("37.9 °C", table_cell), Paragraph("29.0 °C", table_cell), Paragraph("34.0 °C", table_cell)],
        [Paragraph("Session Cost (₹)", table_cell_bold), Paragraph("₹ 444.10", table_cell), Paragraph("₹ 1,253.14", table_cell), Paragraph("₹ 161.61", table_cell), Paragraph("₹ 677.31", table_cell)],
        [Paragraph("Urgency Score (1-10)", table_cell_bold), Paragraph("1.83 (Low)", table_cell), Paragraph("9.17 (Critical)", table_cell), Paragraph("4.20 (Medium)", table_cell), Paragraph("8.50 (High)", table_cell)]
    ]
    t_prof = Table(prof_data, colWidths=[108, 98, 102, 98, 98])
    t_prof.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0D47A1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CFD8DC')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F0F4F8')]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_prof)
    story.append(Spacer(1, 10))

    # Conclusion
    story.append(Paragraph("Conclusion", h1_style))
    story.append(Paragraph("In this experiment, K-Means clustering was successfully executed on a 20,000-record EV fleet telemetry dataset in Python. The Elbow method firmly verified <b>k = 4</b> as the optimal configuration, achieving an impressive Silhouette Score of 0.5679 and Davies-Bouldin index of 0.6806. The derived archetypes provide EV charging network operators with direct operational utility: dynamically routing fleet vehicles to high-power DC hubs during urgent shifts while steering overnight residential users to low-power off-peak AC grids.", body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated {pdf_path} successfully!")

if __name__ == '__main__':
    base_dir = r'.\DMBI-Lab-Vidushi\Exp6_KMeans_Clustering'
    out_pdf = os.path.join(base_dir, "EXP-6_DMBI_53_KMeans_Clustering.pdf")
    build_pdf(out_pdf, base_dir)

