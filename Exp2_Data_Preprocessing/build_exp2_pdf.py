#!/usr/bin/env python3
"""Build comprehensive university-standard PDF report for Experiment 2 (Data Preprocessing)."""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
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
        self.drawString(54, 34, "Experiment 2: Data Preprocessing Using Python (Smart EV Charging Analytics)")
        self.drawRightString(558, 34, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def build_pdf(pdf_path):
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
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0D47A1'),
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#37474F'),
        spaceAfter=10
    )
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#1565C0'),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#2E7D32'),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#212121'),
        spaceAfter=6
    )
    code_style = ParagraphStyle(
        'Code_Custom',
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#1A237E')
    )
    table_cell = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#212121')
    )
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#0D47A1')
    )
    table_hdr = ParagraphStyle(
        'TableHdr',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("Experiment 2 – Data Preprocessing Using Python", title_style))
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
            Paragraph("<b>Date of Submission:</b> November 2026", table_cell)
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
    story.append(Paragraph("To perform comprehensive data preprocessing on an empirical Smart Electric Vehicle (EV) Charging Telemetry dataset using Python, executing duplicate detection, statistical missing value imputation, Interquartile Range (IQR) outlier capping, categorical encoding, and Z-score feature standardization.", body_style))
    
    story.append(Paragraph("Objectives", h1_style))
    story.append(Paragraph("• Identify and purge redundant / duplicate telemetry session records.", body_style))
    story.append(Paragraph("• Diagnose mechanisms of missingness (MCAR, MAR) and apply appropriate mean and mode imputations.", body_style))
    story.append(Paragraph("• Detect extreme anomalous spikes via IQR 1.5× boundaries and perform robust Winsorization / clipping.", body_style))
    story.append(Paragraph("• Transform nominal / ordinal categorical descriptors into numerical formats via Label Encoding.", body_style))
    story.append(Paragraph("• Standardize multi-scale continuous features to zero mean and unit variance using StandardScaler.", body_style))

    # Theory
    story.append(Paragraph("Theoretical Background", h1_style))
    story.append(Paragraph("Real-world IoT telemetry from EV charging networks frequently suffers from packet drops, faulty meter readings, inconsistent hardware protocols, and sensor drift. Data preprocessing constitutes the foundational phase of the Knowledge Discovery in Databases (KDD) process, converting raw, noisy records into clean, standardized inputs suitable for downstream classification and clustering algorithms.", body_style))
    story.append(Paragraph("<b>1. Missing Value Imputation:</b> Missing continuous readings such as energy consumption or ambient temperature are imputed using column-wise arithmetic mean: \\(\\bar{x} = \\frac{1}{n} \\sum_{i=1}^{n} x_i\\). For categorical attributes such as station location, mode imputation selects the most frequent observation.", body_style))
    story.append(Paragraph("<b>2. Outlier Treatment (IQR Rule):</b> Outliers are identified using Tukey's fences: \\([Q_1 - 1.5 \\times \\text{IQR}, Q_3 + 1.5 \\times \\text{IQR}]\\), where \\(\\text{IQR} = Q_3 - Q_1\\). Values lying outside these boundaries are capped to prevent distortion in distance-based models.", body_style))
    story.append(Paragraph("<b>3. Feature Standardization:</b> Continuous features exhibit vastly different scales (e.g., duration in minutes vs cost in ₹). Standard scaling normalizes values via \\(z = \\frac{x - \\mu}{\\sigma}\\), ensuring equal weighting during clustering and distance computations.", body_style))

    story.append(PageBreak())

    # Pipeline Steps
    story.append(Paragraph("Data Preprocessing Execution & Pipeline Results", h1_style))
    
    pipe_summary = [
        [Paragraph("Preprocessing Stage", table_hdr), Paragraph("Original State", table_hdr), Paragraph("Action Taken", table_hdr), Paragraph("Transformed State", table_hdr)],
        [Paragraph("Record Deduplication", table_cell_bold), Paragraph("514 Total Rows", table_cell), Paragraph("Identified exact session duplicates via df.drop_duplicates()", table_cell), Paragraph("503 Unique Rows (11 removed)", table_cell)],
        [Paragraph("Missing Value: Energy", table_cell_bold), Paragraph("18 null values", table_cell), Paragraph("Mean imputation (μ = 23.15 kWh)", table_cell), Paragraph("0 null values", table_cell)],
        [Paragraph("Missing Value: Duration", table_cell_bold), Paragraph("15 null values", table_cell), Paragraph("Mean imputation (μ = 56.56 min)", table_cell), Paragraph("0 null values", table_cell)],
        [Paragraph("Missing Value: Temp", table_cell_bold), Paragraph("12 null values", table_cell), Paragraph("Mean imputation (μ = 31.76 °C)", table_cell), Paragraph("0 null values", table_cell)],
        [Paragraph("Missing Value: Location", table_cell_bold), Paragraph("10 null values", table_cell), Paragraph("Mode imputation ('Highway Corridor')", table_cell), Paragraph("0 null values", table_cell)],
        [Paragraph("Outlier Capping: Duration", table_cell_bold), Paragraph("20 outliers (>85.25m / <4.85m)", table_cell), Paragraph("Capped at [4.85, 85.25] min via 1.5× IQR", table_cell), Paragraph("Normalized bounds", table_cell)],
        [Paragraph("Categorical Encoding", table_cell_bold), Paragraph("4 Text attributes", table_cell), Paragraph("LabelEncoder mapping to numeric discrete bins", table_cell), Paragraph("4 encoded features added", table_cell)],
        [Paragraph("Feature Scaling", table_cell_bold), Paragraph("Multi-scale continuous", table_cell), Paragraph("StandardScaler Z-score transformation (μ=0, σ=1)", table_cell), Paragraph("7 standardized columns", table_cell)]
    ]
    t_pipe = Table(pipe_summary, colWidths=[120, 110, 150, 124])
    t_pipe.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0D47A1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CFD8DC')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F5F5F5')]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_pipe)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Python Implementation Code (preprocessing.py)", h1_style))
    code_text = """# --- Core Preprocessing Routine ---
import pandas as pd, numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler

df = pd.read_csv('ev_charging_platform_dataset.csv')
df = df.drop_duplicates()

# Mean/Mode Imputation
for col in ['energy_consumed_kwh', 'charging_duration_min', 'ambient_temp_c']:
    df[col] = df[col].fillna(df[col].mean())
df['station_location'] = df['station_location'].fillna(df['station_location'].mode()[0])

# IQR Outlier Capping
for col in ['charging_duration_min', 'energy_consumed_kwh', 'charging_cost_inr']:
    q1, q3 = df[col].quantile(0.25), df[col].quantile(0.75)
    iqr = q3 - q1
    df[col] = np.clip(df[col], q1 - 1.5*iqr, q3 + 1.5*iqr)

# Label Encoding & Feature Scaling
for col in ['driver_type', 'vehicle_model', 'charger_type', 'station_location']:
    df[col + '_encoded'] = LabelEncoder().fit_transform(df[col])

scaler = StandardScaler()
scale_cols = ['battery_capacity_kwh', 'initial_soc_pct', 'final_soc_pct', 
              'energy_consumed_kwh', 'charging_duration_min', 'charging_cost_inr', 'ambient_temp_c']
scaled_arr = scaler.fit_transform(df[scale_cols])
df_clean = pd.concat([df, pd.DataFrame(scaled_arr, columns=[c+'_scaled' for c in scale_cols], index=df.index)], axis=1)
df_clean.to_csv('ev_charging_clean_dataset.csv', index=False)"""
    
    code_table = Table([[Paragraph(code_text.replace('\n', '<br/>'), code_style)]], colWidths=[504])
    code_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ECEFF1')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#90A4AE')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(code_table)
    story.append(Spacer(1, 10))

    # Conclusion
    story.append(Paragraph("Conclusion", h1_style))
    story.append(Paragraph("Through this experiment, a structured data preprocessing pipeline was developed and validated in Python. 11 redundant records were eliminated, 55 missing telemetry values across continuous and discrete attributes were imputed using robust measures of central tendency, sensor spikes were capped using the 1.5× IQR rule, and all attributes were converted into numeric, standardized representations. The resulting clean dataset (503 records × 25 features) is fully conditioned for exploratory analysis and model training in subsequent experiments.", body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated {pdf_path} successfully!")

if __name__ == '__main__':
    base_dir = r'.\DMBI-Lab-Vidushi\Exp2_Data_Preprocessing'
    out_pdf = os.path.join(base_dir, "EXP-2_DMBI_53_DataPreprocessing.pdf")
    build_pdf(out_pdf)

