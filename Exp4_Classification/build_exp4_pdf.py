#!/usr/bin/env python3
"""Build comprehensive university-standard PDF report for Experiment 4 (Classification)."""
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
        self.drawString(54, 755, "VESIT · Department of Information Technology · DMBI Laboratory")
        self.drawRightString(558, 755, "Vidushi Singh (Roll No. 53, D15A)")
        self.setStrokeColor(colors.HexColor("#B0BEC5"))
        self.setLineWidth(0.6)
        self.line(54, 750, 558, 750)
        
        self.line(54, 45, 558, 45)
        self.drawString(54, 34, "Experiment 4: Classification using RapidMiner & Python (Smart EV Analytics)")
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
    story.append(Paragraph("Experiment 4 – Classification using RapidMiner and Python", title_style))
    story.append(Paragraph("<b>Domain:</b> Smart Electric Vehicle (EV) Charging & Fleet Battery Telemetry Analytics", subtitle_style))
    
    meta_data = [
        [
            Paragraph("<b>Name:</b> Vidushi Singh", table_cell),
            Paragraph("<b>Roll No:</b> 53", table_cell),
            Paragraph("<b>Class / Div:</b> D15A", table_cell),
            Paragraph("<b>Group:</b> D15A_09", table_cell)
        ],
        [
            Paragraph("<b>Course:</b> Data Mining & Business Intelligence (DMBI)", table_cell),
            Paragraph("<b>Semester:</b> VI", table_cell),
            Paragraph("<b>Academic Year:</b> 2026–2027", table_cell),
            Paragraph("<b>Experiment:</b> 04", table_cell)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[160, 90, 110, 144])
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
    story.append(Paragraph("To explore classification concepts in RapidMiner and implement supervised machine learning algorithms (Decision Tree CART and Gaussian Naïve Bayes) in Python to classify EV charging sessions by Battery Thermal Stress Risk (<code>battery_stress_flag</code>).", body_style))
    
    story.append(Paragraph("Objectives", h1_style))
    story.append(Paragraph("• Model supervised predictive pipelines across continuous and encoded discrete telemetry features.", body_style))
    story.append(Paragraph("• Construct and prune a CART Decision Tree model using Gini Impurity criteria.", body_style))
    story.append(Paragraph("• Apply Gaussian Naïve Bayes assuming feature conditional independence.", body_style))
    story.append(Paragraph("• Replicate the visual operator pipeline workflow used in RapidMiner Studio.", body_style))
    story.append(Paragraph("• Evaluate and compare models on Accuracy, Precision, Recall, F1-Score, and ROC-AUC.", body_style))

    # Theory & RapidMiner Pipeline
    story.append(Paragraph("Theoretical Principles & RapidMiner Architecture", h1_style))
    story.append(Paragraph("<b>Decision Tree (CART):</b> Recursively partitions the feature space into orthogonal hyperplanes by maximizing information gain or Gini reduction: \\(\\text{Gini}(D) = 1 - \\sum_{i=1}^{k} p_i^2\\). It yields transparent, human-auditable IF-THEN rules directly applicable to Battery Management System (BMS) controllers.", body_style))
    story.append(Paragraph("<b>Gaussian Naïve Bayes:</b> Applies Bayes' Theorem: \\(P(Y|X) \\propto P(Y) \\prod_{j=1}^{d} P(X_j|Y)\\), modeling continuous features as Gaussian distributions: \\(P(X_j = x | Y = c) = \\frac{1}{\\sqrt{2\\pi\\sigma_c^2}} \\exp\\left(-\\frac{(x - \\mu_c)^2}{2\\sigma_c^2}\\right)\\). Despite the attribute independence assumption, it is computationally fast and highly robust against noisy telemetry.", body_style))
    story.append(Paragraph("<b>RapidMiner Studio Workflow:</b> The pipeline maps cleanly to standard operators: <code>[Retrieve EV_Dataset] \\(\\rightarrow\\) [Select Attributes] \\(\\rightarrow\\) [Set Role (battery_stress_flag as label)] \\(\\rightarrow\\) [Split Data (80:20)] \\(\\rightarrow\\) [Decision Tree / Naive Bayes] \\(\\rightarrow\\) [Apply Model] \\(\\rightarrow\\) [Performance (Classification)]</code>.", body_style))

    story.append(PageBreak())

    # Performance Comparison Table
    story.append(Paragraph("Comparative Experimental Performance Evaluation", h1_style))
    perf_data = [
        [Paragraph("Evaluation Metric", table_hdr), Paragraph("Decision Tree (CART, depth=4)", table_hdr), Paragraph("Gaussian Naïve Bayes", table_hdr)],
        [Paragraph("Classification Accuracy", table_cell_bold), Paragraph("63.37%", table_cell), Paragraph("67.33% (Higher)", table_cell)],
        [Paragraph("Precision (Positive Class)", table_cell_bold), Paragraph("62.07%", table_cell), Paragraph("65.00%", table_cell)],
        [Paragraph("Recall / Sensitivity", table_cell_bold), Paragraph("70.59%", table_cell), Paragraph("76.47% (Higher)", table_cell)],
        [Paragraph("F1-Score (Harmonic Mean)", table_cell_bold), Paragraph("66.06%", table_cell), Paragraph("70.27% (Higher)", table_cell)],
        [Paragraph("ROC - Area Under Curve (AUC)", table_cell_bold), Paragraph("0.7027", table_cell), Paragraph("0.7376 (Higher)", table_cell)],
        [Paragraph("Training Runtime Complexity", table_cell_bold), Paragraph("O(n · d · log(n))", table_cell), Paragraph("O(n · d) - Extremely Fast", table_cell)],
        [Paragraph("Model Interpretability", table_cell_bold), Paragraph("High (Explicit tree rules)", table_cell), Paragraph("Moderate (Probability densities)", table_cell)]
    ]
    t_perf = Table(perf_data, colWidths=[150, 177, 177])
    t_perf.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1565C0')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CFD8DC')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F0F4F8')]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_perf)
    story.append(Spacer(1, 10))

    # Visualizations
    story.append(Paragraph("1. Confusion Matrices & ROC Curves", h1_style))
    f2 = os.path.join(img_dir, "fig2_confusion_matrices.png")
    if os.path.exists(f2):
        story.append(Image(f2, width=490, height=200))
        story.append(Spacer(1, 6))

    f3 = os.path.join(img_dir, "fig3_roc_curves.png")
    if os.path.exists(f3):
        story.append(Image(f3, width=400, height=270))
        story.append(Spacer(1, 6))

    story.append(PageBreak())

    # Figure 1: Decision Tree
    story.append(Paragraph("2. Decision Tree Structure (CART)", h1_style))
    story.append(Paragraph("The visual decision tree demonstrates that the primary root splits isolate charging protocol (Fast DC / Ultra-Fast DC) followed by ambient operating temperature (>34.8°C) and delivered energy (>28.4 kWh), effectively establishing automated BMS safety cutoff thresholds.", body_style))
    f1 = os.path.join(img_dir, "fig1_decision_tree_vis.png")
    if os.path.exists(f1):
        story.append(Image(f1, width=500, height=260))
        story.append(Spacer(1, 8))

    # Conclusion
    story.append(Paragraph("Conclusion", h1_style))
    story.append(Paragraph("In this experiment, classification models were successfully designed and benchmarked to predict battery thermal stress in EV charging sessions. Gaussian Naïve Bayes achieved the strongest overall performance (Accuracy: 67.33%, Recall: 76.47%, ROC-AUC: 0.7376), effectively capturing probabilistic risk without overfitting noisy temperature measurements. The CART Decision Tree provided transparent rule pathways with a 70.59% recall rate, proving highly suitable for real-time edge BMS threshold alert systems.", body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated {pdf_path} successfully!")

if __name__ == '__main__':
    base_dir = r'.\DMBI-Lab-Vidushi\Exp4_Classification'
    out_pdf = os.path.join(base_dir, "EXP-4_DMBI_53_Classification.pdf")
    build_pdf(out_pdf, base_dir)

