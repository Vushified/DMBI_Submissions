#!/usr/bin/env python3
"""Build comprehensive university-standard PDF report for Experiment 8 (Apriori Association Mining)."""
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
        self.drawString(54, 34, "Experiment 8: Apriori Association Rule Mining (Smart EV Analytics)")
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
    story.append(Paragraph("Experiment 8 – Association Mining Using Apriori Algorithm", title_style))
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
    story.append(Paragraph("To implement the classical Apriori Association Rule Mining algorithm in Python on 20,000 binarized EV charging transactions, uncover frequent multi-item operational behavior patterns at a minimum support threshold (s = 0.08), and evaluate association rules using Confidence, Lift, and Leverage metrics.", body_style))
    
    story.append(Paragraph("Objectives", h1_style))
    story.append(Paragraph("• Transform continuous operational telemetry into binary discrete behavioural transaction items.", body_style))
    story.append(Paragraph("• Apply the downward-closure (Apriori) property to prune infrequent candidate itemsets efficiently.", body_style))
    story.append(Paragraph("• Extract multi-item frequent itemsets satisfying the minimum support threshold (s = 0.08).", body_style))
    story.append(Paragraph("• Generate high-confidence association rules (c >= 0.40) and filter for positive correlation (Lift >= 1.0).", body_style))
    story.append(Paragraph("• Derive grid management policies from high-lift co-occurrence rules (e.g., thermal throttling & dynamic tariffs).", body_style))

    # Theoretical Background & Formulas
    story.append(Paragraph("Theoretical Foundation of Apriori Association Mining", h1_style))
    story.append(Paragraph("The Apriori algorithm operates on the fundamental <b>Apriori Property</b> (Anti-monotonicity of support): <i>All non-empty subsets of a frequent itemset must also be frequent</i>. If an itemset I is infrequent (Support(I) < min_support), all supersets are immediately pruned without database scans.", body_style))
    story.append(Paragraph("Key quantitative metrics defining rule quality <b>A => B</b>:", body_style))
    story.append(Paragraph("<font face='Courier' size='8.5'><b>Support(A => B) = P(A &cup; B) = count(A &cup; B) / N</b></font>", body_style))
    story.append(Paragraph("<font face='Courier' size='8.5'><b>Confidence(A => B) = P(B|A) = Support(A &cup; B) / Support(A)</b></font>", body_style))
    story.append(Paragraph("<font face='Courier' size='8.5'><b>Lift(A => B) = Confidence(A => B) / Support(B)</b></font>", body_style))
    story.append(Paragraph("A <b>Lift > 1.0</b> indicates positive correlation between antecedent and consequent, confirming genuine operational synergy beyond random chance.", body_style))

    story.append(PageBreak())

    # Item Frequency & Top Frequent Itemsets
    story.append(Paragraph("1. EV Behavioral Telemetry Transaction Matrix & Top Frequent Itemsets", h1_style))
    
    freq_data = [
        [Paragraph("Transaction Item Name", table_hdr), Paragraph("Operational Definition", table_hdr), Paragraph("Frequency (Count)", table_hdr), Paragraph("Support (%)", table_hdr)],
        [Paragraph("High_Energy_Delivered", table_cell_bold), Paragraph("Session delivers >= 30 kWh", table_cell), Paragraph("11,708", table_cell), Paragraph("58.54%", table_cell)],
        [Paragraph("Low_Arrival_SoC", table_cell_bold), Paragraph("Vehicle arrives with SoC <= 20%", table_cell), Paragraph("10,930", table_cell), Paragraph("54.65%", table_cell)],
        [Paragraph("High_Turnaround_Urgency", table_cell_bold), Paragraph("Driver urgency index >= 7/10", table_cell), Paragraph("8,918", table_cell), Paragraph("44.59%", table_cell)],
        [Paragraph("Fast_DC_Charging", table_cell_bold), Paragraph("Port delivers peak power >= 50 kW", table_cell), Paragraph("8,838", table_cell), Paragraph("44.19%", table_cell)],
        [Paragraph("High_Session_Cost", table_cell_bold), Paragraph("Invoiced session cost >= ₹600", table_cell), Paragraph("7,675", table_cell), Paragraph("38.38%", table_cell)],
        [Paragraph("High_Ambient_Heat", table_cell_bold), Paragraph("Outdoor ambient temp >= 35°C", table_cell), Paragraph("4,981", table_cell), Paragraph("24.90%", table_cell)],
        [Paragraph("Full_100_Charge", table_cell_bold), Paragraph("Vehicle charged to >= 90% SoC", table_cell), Paragraph("4,537", table_cell), Paragraph("22.68%", table_cell)],
        [Paragraph("Long_Dwell_Duration", table_cell_bold), Paragraph("Vehicle connected for >= 60 min", table_cell), Paragraph("4,000", table_cell), Paragraph("20.00%", table_cell)]
    ]
    t_freq = Table(freq_data, colWidths=[130, 164, 110, 100])
    t_freq.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0D47A1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CFD8DC')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_freq)
    story.append(Spacer(1, 10))

    f1 = os.path.join(img_dir, "fig1_frequent_itemsets.png")
    if os.path.exists(f1):
        story.append(Image(f1, width=480, height=250))
        story.append(Spacer(1, 6))

    story.append(PageBreak())

    # Top Association Rules Table & Scatter
    story.append(Paragraph("2. Top Association Rules & Correlation Landscape", h1_style))
    story.append(Paragraph("75 frequent itemsets were generated, deriving <b>605 strong association rules</b> with confidence >= 40% and lift >= 1.0.", body_style))

    rule_data = [
        [Paragraph("Rule Antecedents (IF)", table_hdr), Paragraph("Consequents (THEN)", table_hdr), Paragraph("Supp (%)", table_hdr), Paragraph("Conf (%)", table_hdr), Paragraph("Lift", table_hdr)],
        [Paragraph("Long_Dwell_Duration", table_cell_bold), Paragraph("Full_100_Charge", table_cell), Paragraph("20.00%", table_cell), Paragraph("100.00%", table_cell), Paragraph("4.408", table_cell_bold)],
        [Paragraph("High_Energy, Long_Dwell", table_cell_bold), Paragraph("Full_100_Charge", table_cell), Paragraph("20.00%", table_cell), Paragraph("100.00%", table_cell), Paragraph("4.408", table_cell_bold)],
        [Paragraph("High_Session_Cost", table_cell_bold), Paragraph("Fast_DC_Charging", table_cell), Paragraph("29.98%", table_cell), Paragraph("78.12%", table_cell), Paragraph("1.768", table_cell_bold)],
        [Paragraph("High_Cost, Urgency", table_cell_bold), Paragraph("Fast_DC_Charging", table_cell), Paragraph("29.41%", table_cell), Paragraph("80.24%", table_cell), Paragraph("1.816", table_cell_bold)],
        [Paragraph("Fast_DC, Low_SoC", table_cell_bold), Paragraph("High_Turnaround_Urgency", table_cell), Paragraph("39.99%", table_cell), Paragraph("98.26%", table_cell), Paragraph("2.204", table_cell_bold)],
        [Paragraph("Fast_DC, High_Heat", table_cell_bold), Paragraph("High_Energy_Delivered", table_cell), Paragraph("15.22%", table_cell), Paragraph("88.45%", table_cell), Paragraph("1.511", table_cell_bold)]
    ]
    t_rule = Table(rule_data, colWidths=[150, 154, 60, 70, 70])
    t_rule.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1565C0')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CFD8DC')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F1F8E9')]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_rule)
    story.append(Spacer(1, 10))

    f2 = os.path.join(img_dir, "fig2_rules_scatter.png")
    if os.path.exists(f2):
        story.append(Image(f2, width=460, height=280))
        story.append(Spacer(1, 6))

    story.append(PageBreak())

    # Conclusion
    story.append(Paragraph("Conclusion", h1_style))
    story.append(Paragraph("In this experiment, the Apriori association mining algorithm was successfully implemented on 20,000 EV charging transactions. The downward-closure property efficiently curtailed candidate explosions, isolating 75 frequent patterns and 605 robust association rules. High-lift insights reveal that <b>{Long_Dwell_Duration} =&gt; {Full_100_Charge}</b> exhibits a massive Lift of 4.41 and 100% confidence, confirming residential slow AC user dedication to top-up completion. Furthermore, <b>{Fast_DC_Charging, Low_Arrival_SoC} =&gt; {High_Turnaround_Urgency}</b> (Lift: 2.20, Conf: 98.26%) underscores the acute operational demand of commercial fleets for prioritized fast-charging bay access.", body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated {pdf_path} successfully!")

if __name__ == '__main__':
    base_dir = r'.\DMBI-Lab-Vidushi\Exp8_Apriori_Association'
    out_pdf = os.path.join(base_dir, "EXP-8_DMBI_53_Apriori_Association.pdf")
    build_pdf(out_pdf, base_dir)

